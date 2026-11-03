from fastapi import APIRouter
from app.services.copilot_service import copilot_service
from app.models.schemas import CopilotQueryRequest, CopilotQueryResponse

router = APIRouter()

@router.post("/query", response_model=CopilotQueryResponse)
def query_copilot(req: CopilotQueryRequest):
    return copilot_service.answer_query(
        query=req.query,
        ticker=req.ticker,
        conversation_history=req.conversation_history
    )
