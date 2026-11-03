import pytest
from app.services.classifier import AnnouncementClassifier
from app.services.enrichment import EnrichmentService
from app.models.domain import AnnouncementCategory, PriorityLevel

def test_classifier_results():
    res = AnnouncementClassifier.classify_announcement("TRENT.NS", "Unaudited Financial Results for the quarter ended September 30, 2026")
    assert res["category"] == AnnouncementCategory.RESULTS
    assert res["priority_level"] == PriorityLevel.HIGH
    assert res["is_material"] is True

def test_classifier_management_change():
    res = AnnouncementClassifier.classify_announcement("TITAN.NS", "Intimation under Regulation 30: Appointment of Chief Financial Officer")
    assert res["category"] == AnnouncementCategory.MANAGEMENT_CHANGE
    assert res["priority_level"] == PriorityLevel.HIGH

def test_classifier_litigation():
    res = AnnouncementClassifier.classify_announcement("HDFCBANK.NS", "Receipt of GST Tax Demand Order from Commissioner of Commercial Taxes")
    assert res["category"] == AnnouncementCategory.LITIGATION
    assert res["priority_level"] == PriorityLevel.HIGH

def test_classifier_ma():
    res = AnnouncementClassifier.classify_announcement("RELIANCE.NS", "Completion of Strategic Joint Venture with The Walt Disney Company")
    assert res["category"] == AnnouncementCategory.MA
    assert res["priority_level"] == PriorityLevel.HIGH

def test_classifier_fund_raise():
    res = AnnouncementClassifier.classify_announcement("SUZLON.NS", "Board approves raising of funds via Qualified Institutions Placement (QIP)")
    assert res["category"] == AnnouncementCategory.FUND_RAISE
    assert res["priority_level"] == PriorityLevel.HIGH

def test_classifier_dividend_and_bonus():
    res_div = AnnouncementClassifier.classify_announcement("TCS.NS", "Declaration of Second Interim Dividend of Rs 10 per share")
    assert res_div["category"] == AnnouncementCategory.DIVIDEND
    assert res_div["priority_level"] == PriorityLevel.MEDIUM

    res_bonus = AnnouncementClassifier.classify_announcement("CDSL.NS", "Record Date for Allotment of Bonus Shares in 1:1 ratio")
    assert res_bonus["category"] == AnnouncementCategory.BONUS_SPLIT
    assert res_bonus["priority_level"] == PriorityLevel.MEDIUM

def test_classifier_routine_unclassified():
    res_esop = AnnouncementClassifier.classify_announcement("ITC.NS", "Allotment of 1,42,800 shares under Employee Stock Option Schemes (ESOP)")
    assert res_esop["category"] == AnnouncementCategory.UNCLASSIFIED
    assert res_esop["priority_level"] == PriorityLevel.LOW
    assert res_esop["is_material"] is False

def test_executive_bio_enrichment():
    bio = EnrichmentService.get_executive_bio("Vikram Srivatsa", "Titan Company Ltd", "CFO")
    assert "name" in bio
    assert "prior_experience" in bio
    assert "education" in bio
    assert "key_strengths" in bio
    assert len(bio["key_strengths"]) > 0
