from enum import Enum
from typing import Dict, Any

class AnnouncementCategory(str, Enum):
    RESULTS = "results"
    MA = "M&A"
    FUND_RAISE = "fund_raise"
    MANAGEMENT_CHANGE = "management_change"
    LITIGATION = "litigation"
    INSIDER_TRADING = "insider_trading"
    EARNINGS_CALL = "earnings_call"
    INVESTOR_MEETINGS = "investor_meetings"
    CREDIT_RATING = "credit_rating"
    DIVIDEND = "dividend"
    BONUS_SPLIT = "bonus_split"
    CAPEX = "capex"
    PRESS_RELEASE = "press_release"
    POSTAL_BALLOT = "postal_ballot"
    AGM_EGM = "agm_egm"
    PLEDGING = "pledging"
    UNCLASSIFIED = "unclassified"

class PriorityLevel(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class AlertType(str, Enum):
    VOLUME_SURGE = "VOLUME_SURGE"
    PRICE_SWING = "PRICE_SWING"
    MATERIAL_ANNOUNCEMENT = "MATERIAL_ANNOUNCEMENT"

class DocumentType(str, Enum):
    ANNUAL_REPORT = "ANNUAL_REPORT"
    CONCALL_TRANSCRIPT = "CONCALL_TRANSCRIPT"
    RESULTS_FILING = "RESULTS_FILING"
    INVESTOR_PRESENTATION = "INVESTOR_PRESENTATION"

# Default category priority mapping based on ENAM Reference brief
CATEGORY_PRIORITY_MAP: Dict[AnnouncementCategory, PriorityLevel] = {
    AnnouncementCategory.RESULTS: PriorityLevel.HIGH,
    AnnouncementCategory.MA: PriorityLevel.HIGH,
    AnnouncementCategory.MANAGEMENT_CHANGE: PriorityLevel.HIGH,
    AnnouncementCategory.LITIGATION: PriorityLevel.HIGH,
    AnnouncementCategory.FUND_RAISE: PriorityLevel.HIGH,
    
    AnnouncementCategory.CAPEX: PriorityLevel.MEDIUM,
    AnnouncementCategory.CREDIT_RATING: PriorityLevel.MEDIUM,
    AnnouncementCategory.DIVIDEND: PriorityLevel.MEDIUM,
    AnnouncementCategory.BONUS_SPLIT: PriorityLevel.MEDIUM,
    AnnouncementCategory.INSIDER_TRADING: PriorityLevel.MEDIUM,
    AnnouncementCategory.PRESS_RELEASE: PriorityLevel.MEDIUM,
    
    AnnouncementCategory.EARNINGS_CALL: PriorityLevel.LOW,
    AnnouncementCategory.INVESTOR_MEETINGS: PriorityLevel.LOW,
    AnnouncementCategory.POSTAL_BALLOT: PriorityLevel.LOW,
    AnnouncementCategory.AGM_EGM: PriorityLevel.LOW,
    AnnouncementCategory.PLEDGING: PriorityLevel.LOW,
    AnnouncementCategory.UNCLASSIFIED: PriorityLevel.LOW,
}
