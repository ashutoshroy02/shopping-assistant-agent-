import time
import uuid

from fastapi import APIRouter, Depends

from api.middleware.error_handler import NotFoundException
from api.routes.auth import get_current_user
from database.connection import get_db
from database.models import User
from database.schemas import AutonomousResearchRequest, AutonomousResearchResponse
from graph.workflow import execute_workflow

router = APIRouter()


@router.post("", response_model=AutonomousResearchResponse)
async def autonomous_research(
    request: AutonomousResearchRequest,
    user: User = Depends(get_current_user),
    db=None,
):
    start_time = time.time()
    research_id = uuid.uuid4()

    workflow_result = await execute_workflow(request.query, str(user.id))

    processing_time = int((time.time() - start_time) * 1000)

    recommendations = workflow_result.get("products", [])
    metadata = workflow_result.get("metadata", {})

    report = {
        "summary": workflow_result.get("response", ""),
        "top_picks": recommendations[:5],
        "comparison_table": metadata.get("comparison", {}),
        "price_insights": metadata.get("price_insights", {}),
        "deals_found": metadata.get("deals", []),
        "recommendations": {
            "best_overall": recommendations[0] if recommendations else None,
            "budget_pick": min(recommendations, key=lambda x: x.get("price", 0)) if recommendations else None,
            "premium_choice": max(recommendations, key=lambda x: x.get("price", 0)) if recommendations else None,
        },
    }

    return AutonomousResearchResponse(
        research_id=research_id,
        status="completed",
        report=report,
        metadata={
            "products_analyzed": metadata.get("products_found", 0),
            "reviews_processed": metadata.get("reviews_processed", 0),
            "processing_time_ms": processing_time,
        },
    )
