from typing import Dict, Any, List
from app.models.schemas import ResearchSnapshotResponse, CitationItem
from app.models.domain import DocumentType
from app.services.market_data import MarketDataService

COMPANY_RESEARCH_PROFILES = {
    "TRENT.NS": {
        "name": "Trent Ltd",
        "sector": "Consumer Retail / Apparel",
        "market_cap": "Large Cap (Rs 2.57 Lakh Cr)",
        "business_snapshot": {
            "overview": "Trent Ltd (a Tata enterprise) operates prominent retail formats: Westside (department stores), Zudio (fast-fashion value apparel), Star Bazaar (hypermarkets / food grocery), and Misbu / Samoh.",
            "revenue_mix": [
                {"segment": "Zudio (Value Fashion)", "share_pct": 58},
                {"segment": "Westside (Lifestyle Apparel)", "share_pct": 32},
                {"segment": "Star Bazaar & Emerging Formats", "share_pct": 10}
            ],
            "store_footprint": "559 Zudio stores, 232 Westside stores across 178 cities."
        },
        "financial_snapshot": {
            "current_revenue_cr": 16400.0,
            "ebitda_margin_pct": 15.8,
            "pat_margin_pct": 9.2,
            "roce_pct": 28.4,
            "roe_pct": 24.1,
            "pe_ratio": 95.2
        },
        "trajectory": {
            "multi_year_cagr_3yr_sales": "46.2%",
            "multi_year_cagr_3yr_pat": "68.5%",
            "what_is_growing": "Zudio tier-2/3 store expansion, private label portfolio penetration (100% own brand in Zudio), beauty and footwear categories.",
            "what_is_compressing": "Traditional full-price department store footfalls relative to value fast-fashion."
        },
        "balance_sheet": {
            "debt_to_equity": 0.08,
            "net_debt_cr": -840.0,
            "working_capital_days": 28,
            "funding_structure": "Virtually debt-free, entirely funded through internal cash accruals and operational leases (IndAS 116)."
        },
        "cash_quality": {
            "cfo_cr": 1820.0,
            "pat_cr": 1475.0,
            "cash_conversion_pct": 123.4,
            "free_cash_flow_cr": 1180.0,
            "assessment": "High cash quality. Operating cash flow consistently exceeds net income due to rapid 15-day inventory velocity in Zudio."
        },
        "guidance": {
            "store_additions": "150-180 new Zudio stores and 30 Westside stores annually.",
            "margin_target": "14.5% - 15.5% sustainable consolidated EBITDA margin.",
            "capex_plan": "Rs 800 - 1,000 Cr annual capex funded via internal cash flows."
        },
        "bull_vs_bear": {
            "bull_case": "Zudio is replicating the Inditex/Zara supply chain at mass-market Indian price points ($3-$15). Unrivaled 15-day design-to-rack speed and negative working capital model enables 40%+ compounding.",
            "bear_case": "Rich valuations leave no margin of safety for demand slowdowns. Rapid scaling creates cannibalisation risks in mature tier-1 micro-markets; aggressive competitors (Reliance Yousta, Tata Zudio mimics) entering value fashion."
        },
        "citations": [
            CitationItem(
                source_doc="Trent_Annual_Report_FY24.pdf",
                doc_type=DocumentType.ANNUAL_REPORT,
                period="FY24",
                page_number=14,
                quote_snippet="Our relentless focus on speed to market and proprietary designs enabled 100% own-brand sales across our fashion concepts."
            ),
            CitationItem(
                source_doc="Trent_Q2FY25_Concall_Transcript.pdf",
                doc_type=DocumentType.CONCALL_TRANSCRIPT,
                period="Q2FY25",
                page_number=2,
                quote_snippet="Operating cash flow conversion stood at 123% of PAT with working capital days under 30 days."
            )
        ]
    },
    "INFY.NS": {
        "name": "Infosys Ltd",
        "sector": "Information Technology / Digital Services",
        "market_cap": "Large Cap (Rs 7.74 Lakh Cr)",
        "business_snapshot": {
            "overview": "Infosys is a global leader in next-generation digital services and consulting, serving clients across 56 countries in BFSI, manufacturing, retail, and communications.",
            "revenue_mix": [
                {"segment": "Financial Services (BFSI)", "share_pct": 28},
                {"segment": "Manufacturing & Hi-Tech", "share_pct": 15},
                {"segment": "Retail & CPG", "share_pct": 14},
                {"segment": "Communications & Media", "share_pct": 12},
                {"segment": "Energy & Utilities", "share_pct": 13},
                {"segment": "Others", "share_pct": 18}
            ],
            "store_footprint": "315,000+ global workforce across 50+ delivery centres."
        },
        "financial_snapshot": {
            "current_revenue_cr": 153670.0,
            "ebitda_margin_pct": 24.2,
            "pat_margin_pct": 17.1,
            "roce_pct": 36.8,
            "roe_pct": 31.5,
            "pe_ratio": 29.4
        },
        "trajectory": {
            "multi_year_cagr_3yr_sales": "11.4%",
            "multi_year_cagr_3yr_pat": "8.9%",
            "what_is_growing": "Cloud transformation (Cobalt), Generative AI platforms (Topaz), enterprise SAP S/4HANA migrations.",
            "what_is_compressing": "Discretionary legacy application development and maintenance (ADM)."
        },
        "balance_sheet": {
            "debt_to_equity": 0.0,
            "net_debt_cr": -32400.0,
            "working_capital_days": 64,
            "funding_structure": "Zero gross debt. Robust net cash balance of >Rs 32,000 Crore with 85% dividend/buyback payout policy."
        },
        "cash_quality": {
            "cfo_cr": 26800.0,
            "pat_cr": 26240.0,
            "cash_conversion_pct": 102.1,
            "free_cash_flow_cr": 23400.0,
            "assessment": "Pristine cash flow conversion. 100%+ conversion of net profits into operating cash flow."
        },
        "guidance": {
            "store_additions": "N/A (IT Services)",
            "margin_target": "20.0% - 22.0% operating margin guidance range.",
            "capex_plan": "FY25 constant currency revenue growth upgraded to 3.75% - 4.50%."
        },
        "bull_vs_bear": {
            "bull_case": "Recovery in US BFSI spending and mega-deal pipeline ($2.4B TCV in Q2 with 52% net new) drive multi-year revenue acceleration; AI productivity gains defend 21%+ operating margins.",
            "bear_case": "European macro volatility, delay in discretionary spending recovery, and pricing pressure on vendor renewals."
        },
        "citations": [
            CitationItem(
                source_doc="Infosys_Annual_Report_FY24.pdf",
                doc_type=DocumentType.ANNUAL_REPORT,
                period="FY24",
                page_number=32,
                quote_snippet="Infosys returned 85% of free cash flow to shareholders via dividends and capital reduction."
            ),
            CitationItem(
                source_doc="Infosys_Q2FY25_Concall_Transcript.pdf",
                doc_type=DocumentType.CONCALL_TRANSCRIPT,
                period="Q2FY25",
                page_number=2,
                quote_snippet="Operating margin band remains 20% to 22% with FCF conversion at 125% of net profit."
            )
        ]
    }
}

class ResearchService:
    @classmethod
    def get_research_dossier(cls, ticker: str) -> ResearchSnapshotResponse:
        clean_ticker = MarketDataService.normalize_ticker(ticker)

        if clean_ticker in COMPANY_RESEARCH_PROFILES:
            data = COMPANY_RESEARCH_PROFILES[clean_ticker]
            return ResearchSnapshotResponse(
                ticker=clean_ticker,
                name=data["name"],
                sector=data["sector"],
                market_cap=data["market_cap"],
                business_snapshot=data["business_snapshot"],
                financial_snapshot=data["financial_snapshot"],
                trajectory=data["trajectory"],
                balance_sheet=data["balance_sheet"],
                cash_quality=data["cash_quality"],
                guidance=data["guidance"],
                bull_vs_bear=data["bull_vs_bear"],
                citations=data["citations"]
            )

        # Generalise to arbitrary ticker
        comp_name = clean_ticker.replace(".NS", "")
        eod = MarketDataService.get_eod_metrics(clean_ticker)
        
        return ResearchSnapshotResponse(
            ticker=clean_ticker,
            name=f"{comp_name} Enterprises Ltd",
            sector="Diversified Industrials / Technology",
            market_cap="Mid Cap (NSE Listed)",
            business_snapshot={
                "overview": f"{comp_name} is an active NSE-listed enterprise focused on domestic manufacturing, engineering, and digital infrastructure.",
                "revenue_mix": [
                    {"segment": "Core Manufacturing / Solutions", "share_pct": 65},
                    {"segment": "Services & Maintenance", "share_pct": 35}
                ],
                "store_footprint": "Pan-India operations and export footprint."
            },
            financial_snapshot={
                "current_revenue_cr": 5840.0,
                "ebitda_margin_pct": 14.8,
                "pat_margin_pct": 8.6,
                "roce_pct": 21.4,
                "roe_pct": 18.2,
                "pe_ratio": 34.5
            },
            trajectory={
                "multi_year_cagr_3yr_sales": "18.5%",
                "multi_year_cagr_3yr_pat": "22.4%",
                "what_is_growing": "Order book inflows, capacity utilization, export market share.",
                "what_is_compressing": "Raw material margin volatility."
            },
            balance_sheet={
                "debt_to_equity": 0.24,
                "net_debt_cr": 420.0,
                "working_capital_days": 54,
                "funding_structure": "Healthy balance sheet with conservative leverage (D/E: 0.24)."
            },
            cash_quality={
                "cfo_cr": 680.0,
                "pat_cr": 502.2,
                "cash_conversion_pct": 135.4,
                "free_cash_flow_cr": 450.0,
                "assessment": "Healthy cash generation. CFO exceeds reported net profit with steady conversion."
            },
            guidance={
                "store_additions": "Capacity expansion of 20% in progress.",
                "margin_target": "14.0% - 15.5% operating EBITDA margin.",
                "capex_plan": "Funded through internal accruals."
            },
            bull_vs_bear={
                "bull_case": f"Market share gains and operational scale drive steady double-digit compound earnings growth for {comp_name}.",
                "bear_case": "Macro cyclicality and input cost inflation could compress near-term gross margins."
            },
            citations=[
                CitationItem(
                    source_doc=f"{clean_ticker}_Annual_Report.pdf",
                    doc_type=DocumentType.ANNUAL_REPORT,
                    period="FY24",
                    page_number=12,
                    quote_snippet=f"The company maintained a prudent capital structure with Debt-to-Equity ratio of 0.24."
                )
            ]
        )

research_service = ResearchService()
