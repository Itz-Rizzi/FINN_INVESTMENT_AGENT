from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime, date
from app.models.domain import AnnouncementCategory, PriorityLevel, AlertType, DocumentType

class CompanyBase(BaseModel):
    ticker: str
    name: str
    sector: str
    market_cap_category: str  # Large, Mid, Small
    is_in_portfolio: bool = True

class CompanyResponse(CompanyBase):
    last_price: Optional[float] = None
    change_pct: Optional[float] = None
    volume: Optional[int] = None
    volume_sma_20: Optional[int] = None
    volume_ratio: Optional[float] = None
    latest_announcement_date: Optional[str] = None
    latest_announcement_title: Optional[str] = None

class CompanyListResponse(BaseModel):
    total: int
    companies: List[CompanyResponse]

class EODPriceItem(BaseModel):
    trade_date: str
    open: float
    high: float
    low: float
    close: float
    volume: int
    volume_sma_20: Optional[float] = None
    daily_change_pct: Optional[float] = None

class MarketSnapshotResponse(BaseModel):
    ticker: str
    name: str
    current_price: float
    change_pct: float
    volume: int
    volume_sma_20: float
    volume_ratio: float
    is_volume_unusual: bool
    is_price_unusual: bool
    history: List[EODPriceItem] = []

class AnnouncementBase(BaseModel):
    id: str
    ticker: str
    company_name: Optional[str] = None
    broadcast_time: datetime
    category: AnnouncementCategory
    title: str
    attachment_url: Optional[str] = None
    is_material: bool = False
    materiality_score: float = 0.5
    priority_level: PriorityLevel = PriorityLevel.LOW
    one_line_summary: Optional[str] = None
    enriched_data: Optional[Dict[str, Any]] = None

class AnnouncementResponse(AnnouncementBase):
    pass

class AnnouncementClassifyRequest(BaseModel):
    ticker: str
    title: str
    text_snippet: Optional[str] = None

class AnnouncementClassifyResponse(BaseModel):
    category: AnnouncementCategory
    confidence: float
    priority_level: PriorityLevel
    is_material: bool
    one_line_summary: str
    reasoning: str

class ExecutiveBioResponse(BaseModel):
    name: str
    role_change: str  # Appointment / Resignation
    company: str
    prior_experience: str
    education: Optional[str] = None
    key_strengths: List[str] = []
    source: str = "Verified Public IR & Professional Filings"

class DigestResponse(BaseModel):
    window_hours: int
    generated_at: datetime
    total_announcements: int
    material_count: int
    routine_count: int
    material_announcements: List[AnnouncementResponse]
    routine_announcements: List[AnnouncementResponse]

class CitationItem(BaseModel):
    source_doc: str  # e.g., "Q2FY25_Results_Filing.pdf" or "Annual_Report_FY24.pdf"
    doc_type: DocumentType
    period: str
    page_number: int
    quote_snippet: str

class QuarterlyResultResponse(BaseModel):
    ticker: str
    company_name: str
    period: str  # e.g. "Q2FY25"
    filing_date: str
    revenue_cr: float
    ebitda_cr: float
    pbt_cr: float
    pat_cr: float
    ebitda_margin_pct: float
    pat_margin_pct: float
    revenue_qoq_pct: Optional[float] = None
    revenue_yoy_pct: Optional[float] = None
    ebitda_qoq_pct: Optional[float] = None
    ebitda_yoy_pct: Optional[float] = None
    pat_qoq_pct: Optional[float] = None
    pat_yoy_pct: Optional[float] = None
    citations: List[CitationItem] = []

class ResultsComparisonResponse(BaseModel):
    ticker: str
    company_name: str
    current_quarter: QuarterlyResultResponse
    previous_quarter: Optional[QuarterlyResultResponse] = None
    previous_year_quarter: Optional[QuarterlyResultResponse] = None
    headline_takeaway: str

class AlertConfigModel(BaseModel):
    user_id: str = "default_investor"
    price_change_threshold_pct: float = 3.0
    volume_surge_multiplier: float = 2.0
    notify_categories: List[AnnouncementCategory] = [
        AnnouncementCategory.RESULTS,
        AnnouncementCategory.MA,
        AnnouncementCategory.MANAGEMENT_CHANGE,
        AnnouncementCategory.LITIGATION,
        AnnouncementCategory.FUND_RAISE,
    ]
    is_active: bool = True

class TriggeredAlertResponse(BaseModel):
    id: str
    ticker: str
    company_name: str
    alert_type: AlertType
    severity: str  # CRITICAL, WARNING, INFO
    headline: str
    details: str
    metrics: Dict[str, Any]
    triggered_at: datetime
    is_read: bool = False

class NarrativeComparisonItem(BaseModel):
    quarter: str
    promised_guidance: str
    actual_delivered: str
    variance_analysis: str
    verdict: str  # BEAT, MET, MISSED, SHIFTED_GOALPOSTS
    guidance_citation: CitationItem
    actual_citation: CitationItem

class NarrativeVsNumbersResponse(BaseModel):
    ticker: str
    company_name: str
    executive_summary: str
    credibility_score: str  # HIGH, MODERATE, LOW
    items: List[NarrativeComparisonItem]

class ResearchSnapshotResponse(BaseModel):
    ticker: str
    name: str
    sector: str
    market_cap: str
    business_snapshot: Dict[str, Any]
    financial_snapshot: Dict[str, Any]
    trajectory: Dict[str, Any]
    balance_sheet: Dict[str, Any]
    cash_quality: Dict[str, Any]
    guidance: Dict[str, Any]
    bull_vs_bear: Dict[str, Any]
    citations: List[CitationItem] = []

class CopilotQueryRequest(BaseModel):
    ticker: Optional[str] = None
    query: str
    conversation_history: List[Dict[str, str]] = []

class CopilotQueryResponse(BaseModel):
    answer: str
    citations: List[CitationItem]
    suggested_followups: List[str]
