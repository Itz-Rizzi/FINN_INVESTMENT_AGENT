import json
import uuid
from datetime import datetime, timedelta, timezone
from app.db.database import db
from app.models.domain import AnnouncementCategory, PriorityLevel, AlertType, DocumentType

def seed_rich_data():
    now = datetime.now(timezone.utc)
    
    with db.get_connection() as conn:
        cursor = conn.cursor()
        
        # Check if already seeded announcements
        cursor.execute("SELECT COUNT(*) FROM announcements")
        if cursor.fetchone()[0] > 0:
            print("Database already has rich announcement seed data.")
            return

        print("Seeding rich corporate announcements, results, alerts, and narrative audits...")

        # 1. Announcements (within 24h, 3d, 7d, 30d windows)
        announcements = [
            # HIGH PRIORITY - MANAGEMENT CHANGE (with Bio Enrichment)
            (
                str(uuid.uuid4()),
                "TITAN.NS",
                "Titan Company Ltd",
                (now - timedelta(hours=3)).isoformat(),
                AnnouncementCategory.MANAGEMENT_CHANGE.value,
                "Intimation under Regulation 30: Appointment of Chief Financial Officer (CFO)",
                "https://www.bseindia.com/xml-data/corpfiling/AttachLive/titan_cfo_app.pdf",
                1,
                0.95,
                PriorityLevel.HIGH.value,
                "Titan announces appointment of Mr. Vikram Srivatsa as Chief Financial Officer succeeding Mr. Ashok Sonthalia.",
                json.dumps({
                    "name": "Mr. Vikram Srivatsa",
                    "role_change": "Appointment as CFO",
                    "effective_date": "December 1, 2026",
                    "prior_experience": "Over 22 years in corporate finance and treasury. Previously Senior VP of Finance at Tata Consumer Products and Unilever Group.",
                    "education": "Chartered Accountant (ICAI) and MBA from IIM Bangalore.",
                    "key_strengths": ["Capital allocation", "Retail supply chain finance", "Hedging & precious metals treasury"],
                    "source": "BSE Intimation & LinkedIn Public IR Profile"
                }),
                now.isoformat()
            ),
            # HIGH PRIORITY - RESULTS
            (
                str(uuid.uuid4()),
                "TRENT.NS",
                "Trent Ltd",
                (now - timedelta(hours=6)).isoformat(),
                AnnouncementCategory.RESULTS.value,
                "Unaudited Financial Results (Standalone and Consolidated) for the quarter ended September 30, 2026",
                "https://www.bseindia.com/xml-data/corpfiling/AttachLive/trent_q2_results.pdf",
                1,
                0.98,
                PriorityLevel.HIGH.value,
                "Revenue up 39.4% YoY at Rs 4,157 Cr; EBITDA margin expands to 15.8% powered by Zudio expansion.",
                json.dumps({
                    "revenue_cr": 4157.0,
                    "ebitda_cr": 656.8,
                    "pbt_cr": 512.4,
                    "pat_cr": 381.2,
                    "revenue_yoy_pct": 39.4,
                    "pat_yoy_pct": 46.9,
                    "highlight": "Added 43 new Zudio stores during the quarter, taking total footprint to 559 stores."
                }),
                now.isoformat()
            ),
            # HIGH PRIORITY - LITIGATION / REGULATORY
            (
                str(uuid.uuid4()),
                "HDFCBANK.NS",
                "HDFC Bank Ltd",
                (now - timedelta(hours=14)).isoformat(),
                AnnouncementCategory.LITIGATION.value,
                "Disclosure under Regulation 30: Receipt of Order from Office of the Commissioner of Commercial Taxes",
                "https://www.bseindia.com/xml-data/corpfiling/AttachLive/hdfc_gst_order.pdf",
                1,
                0.88,
                PriorityLevel.HIGH.value,
                "HDFC Bank received GST demand order of Rs 14.8 Cr including interest/penalties; bank states no material financial impact and will appeal.",
                json.dumps({
                    "authority": "Office of the Commissioner of Commercial Taxes, Bengaluru",
                    "dispute_amount_cr": 14.8,
                    "bank_position": "Bank has strong legal grounds based on prevailing judicial precedents and will file an appeal before Appellate Authority."
                }),
                now.isoformat()
            ),
            # HIGH PRIORITY - M&A
            (
                str(uuid.uuid4()),
                "RELIANCE.NS",
                "Reliance Industries Ltd",
                (now - timedelta(hours=18)).isoformat(),
                AnnouncementCategory.MA.value,
                "Media Release: Strategic Joint Venture between Reliance Industries, Viacom18 and The Walt Disney Company",
                "https://www.bseindia.com/xml-data/corpfiling/AttachLive/ril_disney_jv.pdf",
                1,
                0.92,
                PriorityLevel.HIGH.value,
                "Completion of transaction creating Rs 70,352 Cr digital entertainment & sports powerhouse; RIL injects Rs 11,500 Cr growth capital.",
                json.dumps({
                    "venture_value_cr": 70352.0,
                    "ril_capital_injection_cr": 11500.0,
                    "ownership": "RIL (16.34%), Viacom18 (46.82%), Disney (36.84%)"
                }),
                now.isoformat()
            ),
            # HIGH PRIORITY - FUND RAISE
            (
                str(uuid.uuid4()),
                "SUZLON.NS",
                "Suzlon Energy Ltd",
                (now - timedelta(days=1, hours=4)).isoformat(),
                AnnouncementCategory.FUND_RAISE.value,
                "Outcome of Board Meeting: Approval for raising of funds up to Rs 2,000 Crore via QIP / Convertible Securities",
                "https://www.bseindia.com/xml-data/corpfiling/AttachLive/suzlon_qip_board.pdf",
                1,
                0.85,
                PriorityLevel.HIGH.value,
                "Board approves enabling resolution for fund raise up to Rs 2,000 Cr to accelerate WTG blade manufacturing capacity and debt retirement.",
                json.dumps({
                    "amount_cr": 2000.0,
                    "instrument": "Qualified Institutions Placement (QIP) / Equity Shares",
                    "use_of_funds": "Capex for 3.x MW turbine production and working capital cushion"
                }),
                now.isoformat()
            ),
            # MEDIUM PRIORITY - CAPEX
            (
                str(uuid.uuid4()),
                "LT.NS",
                "Larsen & Toubro Ltd",
                (now - timedelta(days=1, hours=8)).isoformat(),
                AnnouncementCategory.CAPEX.value,
                "Press Release: L&T Hydrocarbon Onshore Business Secures Mega Order Valued Between Rs 5,000 to 10,000 Crore",
                "https://www.bseindia.com/xml-data/corpfiling/AttachLive/lt_mega_order.pdf",
                1,
                0.78,
                PriorityLevel.MEDIUM.value,
                "L&T onshore EPC division bags mega engineering order in Middle East for gas compression facilities.",
                json.dumps({
                    "order_range": "Mega (Rs 5,000 - 10,000 Cr)",
                    "client": "National Oil Company in Middle East",
                    "execution_period_months": 36
                }),
                now.isoformat()
            ),
            # MEDIUM PRIORITY - DIVIDEND
            (
                str(uuid.uuid4()),
                "TCS.NS",
                "Tata Consultancy Services Ltd",
                (now - timedelta(days=2, hours=3)).isoformat(),
                AnnouncementCategory.DIVIDEND.value,
                "Intimation of Record Date for Second Interim Dividend of Rs 10 per Equity Share",
                "https://www.bseindia.com/xml-data/corpfiling/AttachLive/tcs_dividend_rec.pdf",
                1,
                0.72,
                PriorityLevel.MEDIUM.value,
                "TCS declares 2nd interim dividend of Rs 10 per equity share with record date fixed as October 18.",
                json.dumps({"dividend_per_share": 10.0, "face_value": 1.0, "record_date": "October 18, 2026"}),
                now.isoformat()
            ),
            # MEDIUM PRIORITY - BONUS / SPLIT
            (
                str(uuid.uuid4()),
                "CDSL.NS",
                "Central Depository Services Ltd",
                (now - timedelta(days=3, hours=5)).isoformat(),
                AnnouncementCategory.BONUS_SPLIT.value,
                "Allotment of Bonus Equity Shares in the ratio of 1:1 (One Bonus Share for every One existing share)",
                "https://www.bseindia.com/xml-data/corpfiling/AttachLive/cdsl_bonus_allotment.pdf",
                1,
                0.75,
                PriorityLevel.MEDIUM.value,
                "CDSL completes allotment of 10.45 crore bonus shares; paid-up capital increases to Rs 209 Crore.",
                json.dumps({"bonus_ratio": "1:1", "post_bonus_shares": 209000000}),
                now.isoformat()
            ),
            # MEDIUM PRIORITY - CREDIT RATING
            (
                str(uuid.uuid4()),
                "TATAMOTORS.NS",
                "Tata Motors Ltd",
                (now - timedelta(days=4, hours=2)).isoformat(),
                AnnouncementCategory.CREDIT_RATING.value,
                "CRISIL Ratings Upgrades Long-Term Debt Instruments of Tata Motors to CRISIL AA+/Positive",
                "https://www.bseindia.com/xml-data/corpfiling/AttachLive/tatamotors_rating_upgrade.pdf",
                1,
                0.70,
                PriorityLevel.MEDIUM.value,
                "CRISIL upgrades long-term credit rating to AA+ from AA with Positive outlook citing JLR debt reduction and domestic EV leadership.",
                json.dumps({"agency": "CRISIL", "new_rating": "CRISIL AA+/Positive", "old_rating": "CRISIL AA/Stable"}),
                now.isoformat()
            ),
            # LOW PRIORITY / ROUTINE - UNCLASSIFIED (ESOP Allotment)
            (
                str(uuid.uuid4()),
                "ITC.NS",
                "ITC Ltd",
                (now - timedelta(hours=2)).isoformat(),
                AnnouncementCategory.UNCLASSIFIED.value,
                "Allotment of 1,42,800 Ordinary Shares of Re 1/- each under Employee Stock Option Schemes",
                "https://www.bseindia.com/xml-data/corpfiling/AttachLive/itc_esop_allot.pdf",
                0,
                0.15,
                PriorityLevel.LOW.value,
                "Routine administrative allotment of 1.42 lakh ESOP equity shares.",
                json.dumps({"shares_allotted": 142800, "type": "ESOP Allotment"}),
                now.isoformat()
            ),
            # LOW PRIORITY / ROUTINE - COMPLIANCE CERTIFICATE
            (
                str(uuid.uuid4()),
                "ICICIBANK.NS",
                "ICICI Bank Ltd",
                (now - timedelta(hours=7)).isoformat(),
                AnnouncementCategory.UNCLASSIFIED.value,
                "Certificate under Regulation 74(5) of SEBI (Depositories and Participants) Regulations, 2018 for the quarter ended Sept 30",
                "https://www.bseindia.com/xml-data/corpfiling/AttachLive/icici_reg74.pdf",
                0,
                0.10,
                PriorityLevel.LOW.value,
                "Routine depository dematerialisation compliance certificate.",
                None,
                now.isoformat()
            ),
            # LOW PRIORITY / ROUTINE - INVESTOR MEETINGS
            (
                str(uuid.uuid4()),
                "INFY.NS",
                "Infosys Ltd",
                (now - timedelta(days=1, hours=2)).isoformat(),
                AnnouncementCategory.INVESTOR_MEETINGS.value,
                "Intimation of Schedule of Analyst / Institutional Investor Meeting on October 22",
                "https://www.bseindia.com/xml-data/corpfiling/AttachLive/infy_analyst_meet.pdf",
                0,
                0.25,
                PriorityLevel.LOW.value,
                "Scheduled one-on-one virtual interaction with institutional investors.",
                None,
                now.isoformat()
            ),
        ]

        cursor.executemany("""
        INSERT INTO announcements (id, ticker, company_name, broadcast_time, category, title, attachment_url, is_material, materiality_score, priority_level, one_line_summary, enriched_data, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, announcements)

        # 2. Quarterly Results (For QoQ & YoY calculations and headline cards)
        results = [
            # Trent Ltd Q2FY25 (Current)
            (
                str(uuid.uuid4()),
                "TRENT.NS",
                "Trent Ltd",
                "Q2FY25",
                "2026-10-24",
                4157.0,  # Revenue Cr
                656.8,   # EBITDA Cr
                512.4,   # PBT Cr
                381.2,   # PAT Cr
                15.8,    # EBITDA Margin %
                9.17,    # PAT Margin %
                12.4,    # Revenue QoQ %
                39.4,    # Revenue YoY %
                16.8,    # EBITDA QoQ %
                45.2,    # EBITDA YoY %
                18.2,    # PAT QoQ %
                46.9,    # PAT YoY %
                json.dumps([
                    {"source_doc": "Trent_Q2FY25_Results_Filing.pdf", "doc_type": "RESULTS_FILING", "period": "Q2FY25", "page_number": 3, "quote_snippet": "Consolidated Revenue from Operations for Q2FY25 stood at Rs 4,156.98 Crores compared to Rs 2,982.42 Crores in Q2FY24."},
                    {"source_doc": "Trent_Q2FY25_Results_Filing.pdf", "doc_type": "RESULTS_FILING", "period": "Q2FY25", "page_number": 4, "quote_snippet": "Profit After Tax for the quarter was Rs 381.24 Crores, reflecting strong operating leverage in fashion retail."}
                ]),
                now.isoformat()
            ),
            # Trent Ltd Q1FY25 (Previous Quarter for QoQ)
            (
                str(uuid.uuid4()),
                "TRENT.NS",
                "Trent Ltd",
                "Q1FY25",
                "2026-07-28",
                3698.0,
                562.4,
                438.1,
                322.5,
                15.2,
                8.72,
                16.1,
                56.2,
                22.4,
                64.1,
                21.0,
                67.2,
                json.dumps([
                    {"source_doc": "Trent_Q1FY25_Results.pdf", "doc_type": "RESULTS_FILING", "period": "Q1FY25", "page_number": 2, "quote_snippet": "Revenue from operations came in at Rs 3,698 Crores with PAT of Rs 322.5 Crores."}
                ]),
                now.isoformat()
            ),
            # Trent Ltd Q2FY24 (Previous Year Quarter for YoY)
            (
                str(uuid.uuid4()),
                "TRENT.NS",
                "Trent Ltd",
                "Q2FY24",
                "2025-10-22",
                2982.4,
                452.3,
                348.6,
                259.5,
                15.1,
                8.70,
                8.2,
                52.7,
                11.0,
                58.4,
                9.5,
                55.9,
                json.dumps([
                    {"source_doc": "Trent_Q2FY24_Results.pdf", "doc_type": "RESULTS_FILING", "period": "Q2FY24", "page_number": 2, "quote_snippet": "Revenue for the period was Rs 2,982.4 Crores with PAT of Rs 259.5 Crores."}
                ]),
                now.isoformat()
            ),
            # Dixon Technologies Q2FY25
            (
                str(uuid.uuid4()),
                "DIXON.NS",
                "Dixon Technologies Ltd",
                "Q2FY25",
                "2026-10-25",
                5420.0,
                216.8,
                178.5,
                135.2,
                4.0,
                2.49,
                18.2,
                112.5,
                15.6,
                105.8,
                16.2,
                108.4,
                json.dumps([
                    {"source_doc": "Dixon_Q2FY25_Financial_Results.pdf", "doc_type": "RESULTS_FILING", "period": "Q2FY25", "page_number": 1, "quote_snippet": "Consolidated revenue crossed Rs 5,420 Crores with mobile manufacturing volumes scaling 2.2x."}
                ]),
                now.isoformat()
            ),
        ]

        cursor.executemany("""
        INSERT OR REPLACE INTO quarterly_results (id, ticker, company_name, period, filing_date, revenue_cr, ebitda_cr, pbt_cr, pat_cr, ebitda_margin_pct, pat_margin_pct, revenue_qoq_pct, revenue_yoy_pct, ebitda_qoq_pct, ebitda_yoy_pct, pat_qoq_pct, pat_yoy_pct, citations, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, results)

        # 3. Triggered Alerts
        alerts = [
            (
                str(uuid.uuid4()),
                "DIXON.NS",
                "Dixon Technologies Ltd",
                AlertType.VOLUME_SURGE.value,
                "WARNING",
                "Unusual Volume Surge: 2.45× 20-Day SMA",
                "Dixon traded 2,840,120 shares today vs. 20-day average of 1,159,200 shares (+145% surge).",
                json.dumps({"volume": 2840120, "volume_sma_20": 1159200, "ratio": 2.45}),
                0,
                (now - timedelta(hours=2)).isoformat()
            ),
            (
                str(uuid.uuid4()),
                "TRENT.NS",
                "Trent Ltd",
                AlertType.PRICE_SWING.value,
                "INFO",
                "Price Move Alert: +4.82% Daily Gain",
                "Trent surged +4.82% to close at Rs 7,240.00 crossing the configured 3.0% threshold.",
                json.dumps({"price": 7240.0, "change_pct": 4.82, "threshold_pct": 3.0}),
                0,
                (now - timedelta(hours=4)).isoformat()
            ),
            (
                str(uuid.uuid4()),
                "TITAN.NS",
                "Titan Company Ltd",
                AlertType.MATERIAL_ANNOUNCEMENT.value,
                "CRITICAL",
                "Material Disclosure: CFO Appointment",
                "Titan appointed Mr. Vikram Srivatsa as Chief Financial Officer.",
                json.dumps({"category": "management_change", "priority": "HIGH"}),
                0,
                (now - timedelta(hours=3)).isoformat()
            )
        ]

        cursor.executemany("""
        INSERT INTO triggered_alerts (id, ticker, company_name, alert_type, severity, headline, details, metrics, is_read, triggered_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, alerts)

        conn.commit()
        print("Rich seed data populated successfully!")

if __name__ == "__main__":
    seed_rich_data()
