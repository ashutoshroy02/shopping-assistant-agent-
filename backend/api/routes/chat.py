import time
import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.middleware.error_handler import NotFoundException
from api.routes.auth import get_current_user
from database.connection import get_db
from database.models import ChatMessage, ChatSession, User
from database.schemas import ChatRequest, ChatResponse
from graph.workflow import execute_workflow

router = APIRouter()


@router.post("", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    start_time = time.time()

    session_id = request.session_id

    if session_id:
        result = await db.execute(
            select(ChatSession).where(
                ChatSession.id == session_id, ChatSession.user_id == user.id
            )
        )
        session = result.scalar_one_or_none()
        if not session:
            raise NotFoundException("Chat session not found")
    else:
        session = ChatSession(
            user_id=user.id,
            title=request.message[:100] if request.message else None,
        )
        db.add(session)
        await db.flush()
        session_id = session.id

    user_message = ChatMessage(
        session_id=session_id,
        role="user",
        content=request.message,
        metadata_=request.context or {},
    )
    db.add(user_message)
    await db.flush()

    workflow_result = await execute_workflow(request.message, str(user.id))

    response_text = workflow_result.get("response", "I couldn't process your request.")
    products = workflow_result.get("products", [])
    metadata = workflow_result.get("metadata", {})

    processing_time = int((time.time() - start_time) * 1000)

    assistant_message = ChatMessage(
        session_id=session_id,
        role="assistant",
        content=response_text,
        metadata_={"products": products, "metadata": metadata},
    )
    db.add(assistant_message)
    await db.flush()

    return ChatResponse(
        response=response_text,
        session_id=session_id,
        products=products,
        metadata={
            **metadata,
            "processing_time_ms": processing_time,
        },
    )


@router.get("/sessions")
async def list_sessions(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    result = await db.execute(
        select(ChatSession)
        .where(ChatSession.user_id == user.id)
        .order_by(ChatSession.updated_at.desc())
        .limit(limit)
        .offset(offset)
    )
    sessions = result.scalars().all()

    count_result = await db.execute(
        select(ChatSession).where(ChatSession.user_id == user.id)
    )
    total = len(count_result.scalars().all())

    return {
        "sessions": [
            {
                "id": str(s.id),
                "title": s.title,
                "created_at": s.created_at.isoformat(),
                "updated_at": s.updated_at.isoformat(),
            }
            for s in sessions
        ],
        "total": total,
        "limit": limit,
        "offset": offset,
    }


@router.get("/history/{session_id}")
async def get_chat_history(
    session_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(ChatSession).where(
            ChatSession.id == session_id, ChatSession.user_id == user.id
        )
    )
    session = result.scalar_one_or_none()
    if not session:
        raise NotFoundException("Chat session not found")

    messages_result = await db.execute(
        select(ChatMessage)
        .where(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.created_at)
    )
    messages = messages_result.scalars().all()

    return {
        "session_id": session_id,
        "session": {
            "id": str(session.id),
            "title": session.title,
            "created_at": session.created_at.isoformat(),
        },
        "messages": [
            {
                "id": str(msg.id),
                "role": msg.role,
                "content": msg.content,
                "metadata": msg.metadata_,
                "timestamp": msg.created_at.isoformat(),
            }
            for msg in messages
        ],
    }


@router.delete("/sessions/{session_id}")
async def delete_session(
    session_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(ChatSession).where(
            ChatSession.id == session_id, ChatSession.user_id == user.id
        )
    )
    session = result.scalar_one_or_none()
    if not session:
        raise NotFoundException("Chat session not found")

    await db.delete(session)
    await db.flush()

    return {"message": "Session deleted successfully"}
