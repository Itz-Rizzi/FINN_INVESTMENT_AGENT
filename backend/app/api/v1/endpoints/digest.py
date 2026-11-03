from fastapi import APIRouter, Query
from typing import Optional
from app.services.digest_service import digest_service
from app.models.schemas import DigestResponse

router = APIRouter()

@router.get("", response_model=DigestResponse)
def get_digest(
    window_hours: int = Query(24, ge=1, le=720, description="Window in hours (e.g. 24 for 1 day, 168 for 7 days)"),
    ticker: Optional[str] = Query(None, description="Optional ticker filter")
):
    return digest_service.get_windowed_digest(window_hours=window_hours, ticker=ticker)
