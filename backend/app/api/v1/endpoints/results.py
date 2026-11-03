from fastapi import APIRouter, HTTPException
from app.services.results_extractor import results_service
from app.models.schemas import ResultsComparisonResponse

router = APIRouter()

@router.get("/{ticker}", response_model=ResultsComparisonResponse)
def get_quarterly_results(ticker: str):
    data = results_service.get_company_results(ticker)
    if not data:
        raise HTTPException(status_code=404, detail=f"No results found for {ticker}")
    return data
