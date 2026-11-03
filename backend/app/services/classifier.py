import re
import json
import logging
from typing import Dict, Any, Tuple
from app.models.domain import AnnouncementCategory, PriorityLevel, CATEGORY_PRIORITY_MAP
from app.core.config import settings

logger = logging.getLogger(__name__)

# Heuristic taxonomy rules for deterministic zero-latency classification
KEYWORD_RULES = [
    # 1. results
    (AnnouncementCategory.RESULTS, [
        r"financial result", r"unaudited.*result", r"audited.*result", r"quarter ended",
        r"half year ended", r"results deck", r"board meeting.*to consider.*result"
    ]),
    # 2. management_change
    (AnnouncementCategory.MANAGEMENT_CHANGE, [
        r"appointment of.*(?:cfo|ceo|md|director|key managerial|officer|president)",
        r"resignation of.*(?:cfo|ceo|md|director|key managerial|officer)",
        r"cessation of.*(?:cfo|ceo|md|director)", r"superannuation of",
        r"retirement of.*(?:cfo|ceo|md|director)", r"change in management"
    ]),
    # 3. M&A
    (AnnouncementCategory.MA, [
        r"acquisition of", r"merger", r"demerger", r"amalgamation", r"joint venture",
        r"strategic alliance", r"purchase of.*stake", r"sale of.*stake", r"subsidiary"
    ]),
    # 4. fund_raise
    (AnnouncementCategory.FUND_RAISE, [
        r"qualified institutions placement", r"\bqip\b", r"rights issue", r"preferential allotment",
        r"issuance of.*debentures", r"commercial paper", r"raising of funds", r"buyback"
    ]),
    # 5. litigation
    (AnnouncementCategory.LITIGATION, [
        r"order.*commissioner", r"tax demand", r"penalty", r"fine imposed", r"gst order",
        r"litigation", r"arbitration", r"insolvency", r"nclt", r"show cause notice", r"regulatory order"
    ]),
    # 6. dividend
    (AnnouncementCategory.DIVIDEND, [
        r"interim dividend", r"final dividend", r"special dividend", r"declaration of dividend",
        r"record date.*dividend"
    ]),
    # 7. bonus_split
    (AnnouncementCategory.BONUS_SPLIT, [
        r"bonus issue", r"bonus shares", r"sub-division of shares", r"stock split",
        r"allotment of bonus"
    ]),
    # 8. capex
    (AnnouncementCategory.CAPEX, [
        r"new plant", r"new facility", r"capacity expansion", r"capital expenditure",
        r"manufacturing unit", r"capex approval"
    ]),
    # 9. credit_rating
    (AnnouncementCategory.CREDIT_RATING, [
        r"credit rating", r"crisil", r"icra", r"care ratings", r"ind-ra", r"rating upgrade",
        r"rating downgrade", r"reaffirmation of rating"
    ]),
    # 10. insider_trading
    (AnnouncementCategory.INSIDER_TRADING, [
        r"sast", r"pit regulations", r"insider trading", r"disclosures under regulation 7\(2\)",
        r"promoter acquisition of shares", r"disposal of shares by promoter"
    ]),
    # 11. pledging
    (AnnouncementCategory.PLEDGING, [
        r"pledge of shares", r"release of pledge", r"revocation of pledge", r"encumbrance"
    ]),
    # 12. earnings_call
    (AnnouncementCategory.EARNINGS_CALL, [
        r"earnings call", r"concall transcript", r"investor call transcript",
        r"audio recording of concall", r"conference call.*transcript"
    ]),
    # 13. investor_meetings
    (AnnouncementCategory.INVESTOR_MEETINGS, [
        r"schedule of analyst", r"investor meet", r"investor conference", r"one-on-one meeting"
    ]),
    # 14. postal_ballot
    (AnnouncementCategory.POSTAL_BALLOT, [
        r"postal ballot notice", r"postal ballot result", r"voting results.*postal ballot"
    ]),
    # 15. agm_egm
    (AnnouncementCategory.AGM_EGM, [
        r"annual general meeting", r"extraordinary general meeting", r"\bagm\b", r"\begm\b",
        r"scrutinizer.*report"
    ]),
    # 16. press_release
    (AnnouncementCategory.PRESS_RELEASE, [
        r"press release", r"media release", r"order win", r"secures.*order", r"clarification on"
    ]),
    # 17. unclassified (routine compliance)
    (AnnouncementCategory.UNCLASSIFIED, [
        r"esop", r"employee stock option", r"regulation 74\(5\)", r"compliance certificate",
        r"loss of share certificate", r"duplicate share certificate", r"closure of trading window",
        r"demat", r"auditor appointment"
    ]),
]

class AnnouncementClassifier:
    @classmethod
    def rule_based_classify(cls, title: str, text: str = "") -> Tuple[AnnouncementCategory, float, str]:
        combined = f"{title} {text}".lower()
        
        for category, patterns in KEYWORD_RULES:
            for pat in patterns:
                if re.search(pat, combined):
                    return category, 0.95, f"Matched keyword rule '{pat}' for {category.value}"
        
        return AnnouncementCategory.UNCLASSIFIED, 0.50, "No distinct category pattern detected; default to unclassified."

    @classmethod
    def classify_announcement(cls, ticker: str, title: str, text: str = "") -> Dict[str, Any]:
        """
        Classifies corporate filing into 1 of 17 ENAM categories and assigns priority and one-line summary.
        Uses rule heuristics + Gemini Flash when configured.
        """
        category, confidence, reasoning = cls.rule_based_classify(title, text)
        
        # If Gemini API key is configured and confidence is moderate, attempt LLM refinement
        if settings.GEMINI_API_KEY and confidence < 0.8:
            try:
                from google import genai
                client = genai.Client(api_key=settings.GEMINI_API_KEY)
                prompt = f"""
                You are a senior equity analyst classifying an Indian stock exchange corporate filing.
                Ticker: {ticker}
                Title: {title}
                Snippet: {text}

                Choose EXACTLY ONE category from this list:
                [results, M&A, fund_raise, management_change, litigation, insider_trading, earnings_call,
                investor_meetings, credit_rating, dividend, bonus_split, capex, press_release, postal_ballot,
                agm_egm, pledging, unclassified]

                Return JSON only:
                {{
                  "category": "<one of above>",
                  "confidence": 0.95,
                  "is_material": true/false,
                  "one_line_summary": "<dense high-signal 1-sentence summary>"
                }}
                """
                response = client.models.generate_content(
                    model=settings.GEMINI_FLASH_MODEL,
                    contents=prompt,
                )
                raw_json = response.text.strip().replace("```json", "").replace("```", "")
                data = json.loads(raw_json)
                cat_val = data.get("category", category.value)
                # Match to enum
                for ac in AnnouncementCategory:
                    if ac.value.lower() == cat_val.lower():
                        category = ac
                        break
                confidence = float(data.get("confidence", 0.9))
                reasoning = "Refined via Gemini Flash LLM classification"
            except Exception as e:
                logger.debug(f"LLM classification skipped/failed: {e}")

        priority = CATEGORY_PRIORITY_MAP.get(category, PriorityLevel.LOW)
        is_material = priority in [PriorityLevel.HIGH, PriorityLevel.MEDIUM]
        materiality_score = 0.95 if priority == PriorityLevel.HIGH else (0.70 if priority == PriorityLevel.MEDIUM else 0.20)
        
        # Build concise one-line summary
        one_line_summary = cls._generate_one_liner(ticker, category, title)

        return {
            "category": category,
            "confidence": confidence,
            "priority_level": priority,
            "is_material": is_material,
            "materiality_score": materiality_score,
            "one_line_summary": one_line_summary,
            "reasoning": reasoning
        }

    @staticmethod
    def _generate_one_liner(ticker: str, category: AnnouncementCategory, title: str) -> str:
        t = title.strip()
        if category == AnnouncementCategory.MANAGEMENT_CHANGE:
            return f"Key managerial personnel change reported: {t[:90]}"
        elif category == AnnouncementCategory.RESULTS:
            return f"Quarterly / annual financial results disclosure for {ticker}."
        elif category == AnnouncementCategory.MA:
            return f"Strategic M&A, joint venture, or subsidiary transaction."
        elif category == AnnouncementCategory.LITIGATION:
            return f"Regulatory, tax, or legal order received by {ticker}."
        elif category == AnnouncementCategory.DIVIDEND:
            return f"Dividend declaration and record date notice."
        elif category == AnnouncementCategory.FUND_RAISE:
            return f"Capital raising / securities issuance disclosure."
        elif category == AnnouncementCategory.UNCLASSIFIED:
            return f"Routine administrative compliance notice ({t[:60]})."
        return f"{category.value.capitalize()} filing: {t[:80]}"

classifier_service = AnnouncementClassifier()
