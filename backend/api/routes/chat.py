import time
import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import get_db
from database.schemas import ChatRequest
from graph.workflow import execute_workflow

router = APIRouter()


@router.post("")
async def chat(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db),
):
    start_time = time.time()

    workflow_result = await execute_workflow(request.message, "anonymous")

    response_text = workflow_result.get("response", "I couldn't process your request.")
    products = workflow_result.get("products", [])
    metadata = workflow_result.get("metadata", {})

    processing_time = int((time.time() - start_time) * 1000)

    return {
        "response": response_text,
        "products": products,
        "metadata": {
            **metadata,
            "processing_time_ms": processing_time,
        },
    }
