from fastapi import APIRouter, HTTPException
from app.services.screener_scraper import screener_scraper
from app.services.research_service import research_service
from app.services.narrative_analyzer import narrative_service
from app.models.schemas import ResearchSnapshotResponse, NarrativeVsNumbersResponse

router = APIRouter()

@router.get("/{ticker}/snapshot", response_model=ResearchSnapshotResponse)
def get_research_snapshot(ticker: str):
    """
    On-demand 8-dimension deep research dossier for ANY arbitrary NSE ticker,
    scraped live from official filings and Screener.in.
    """
    try:
        return screener_scraper.get_dynamic_research_dossier(ticker)
    except Exception as e:
        return research_service.get_research_dossier(ticker)

@router.get("/{ticker}/narrative-vs-numbers", response_model=NarrativeVsNumbersResponse)
def get_narrative_vs_numbers(ticker: str):
    """
    Flagship 4-quarter Guidance vs. Delivered audit cross-examining statements
    against actual reported numbers with primary document citations.
    """
    try:
        return screener_scraper.get_dynamic_narrative_vs_numbers(ticker)
    except Exception as e:
        return narrative_service.analyze_company(ticker)
