import sqlite3
import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import List, Dict, Any, Optional

from app.core.config import settings
from app.models.domain import AnnouncementCategory, PriorityLevel, AlertType, DocumentType

class Database:
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or settings.SQLITE_DB_PATH
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self.init_db()

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # 1. Companies Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS companies (
                ticker TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                sector TEXT NOT NULL,
                market_cap_category TEXT NOT NULL,
                is_in_portfolio INTEGER DEFAULT 1,
                created_at TEXT NOT NULL
            )
            """)

            # 2. EOD Prices Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS eod_prices (
                id TEXT PRIMARY KEY,
                ticker TEXT NOT NULL,
                trade_date TEXT NOT NULL,
                open_price REAL NOT NULL,
                high_price REAL NOT NULL,
                low_price REAL NOT NULL,
                close_price REAL NOT NULL,
                volume INTEGER NOT NULL,
                volume_sma_20 REAL,
                daily_change_pct REAL,
                UNIQUE(ticker, trade_date),
                FOREIGN KEY (ticker) REFERENCES companies(ticker)
            )
            """)

            # 3. Announcements Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS announcements (
                id TEXT PRIMARY KEY,
                ticker TEXT NOT NULL,
                company_name TEXT,
                broadcast_time TEXT NOT NULL,
                category TEXT NOT NULL,
                title TEXT NOT NULL,
                attachment_url TEXT,
                local_pdf_path TEXT,
                is_material INTEGER DEFAULT 0,
                materiality_score REAL DEFAULT 0.5,
                priority_level TEXT NOT NULL,
                one_line_summary TEXT,
                enriched_data TEXT, -- JSON
                created_at TEXT NOT NULL,
                FOREIGN KEY (ticker) REFERENCES companies(ticker)
            )
            """)

            # 4. Quarterly Results Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS quarterly_results (
                id TEXT PRIMARY KEY,
                ticker TEXT NOT NULL,
                company_name TEXT NOT NULL,
                period TEXT NOT NULL,
                filing_date TEXT NOT NULL,
                revenue_cr REAL NOT NULL,
                ebitda_cr REAL NOT NULL,
                pbt_cr REAL NOT NULL,
                pat_cr REAL NOT NULL,
                ebitda_margin_pct REAL NOT NULL,
                pat_margin_pct REAL NOT NULL,
                revenue_qoq_pct REAL,
                revenue_yoy_pct REAL,
                ebitda_qoq_pct REAL,
                ebitda_yoy_pct REAL,
                pat_qoq_pct REAL,
                pat_yoy_pct REAL,
                citations TEXT, -- JSON array
                created_at TEXT NOT NULL,
                UNIQUE(ticker, period),
                FOREIGN KEY (ticker) REFERENCES companies(ticker)
            )
            """)

            # 5. Alert Configs Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS alert_configs (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                price_change_threshold_pct REAL DEFAULT 3.0,
                volume_surge_multiplier REAL DEFAULT 2.0,
                notify_categories TEXT, -- JSON array
                is_active INTEGER DEFAULT 1,
                updated_at TEXT NOT NULL
            )
            """)

            # 6. Triggered Alerts Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS triggered_alerts (
                id TEXT PRIMARY KEY,
                ticker TEXT NOT NULL,
                company_name TEXT NOT NULL,
                alert_type TEXT NOT NULL,
                severity TEXT NOT NULL,
                headline TEXT NOT NULL,
                details TEXT NOT NULL,
                metrics TEXT, -- JSON
                is_read INTEGER DEFAULT 0,
                triggered_at TEXT NOT NULL,
                FOREIGN KEY (ticker) REFERENCES companies(ticker)
            )
            """)

            # 7. Document Chunks Table (for Grounded FAISS / RAG)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS document_chunks (
                id TEXT PRIMARY KEY,
                ticker TEXT NOT NULL,
                doc_type TEXT NOT NULL,
                period TEXT NOT NULL,
                source_filename TEXT NOT NULL,
                page_number INTEGER NOT NULL,
                chunk_index INTEGER NOT NULL,
                chunk_text TEXT NOT NULL,
                faiss_vector_id INTEGER NOT NULL,
                created_at TEXT NOT NULL
            )
            """)

            conn.commit()

        self.seed_defaults()

    def seed_defaults(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Check if already seeded
            cursor.execute("SELECT COUNT(*) FROM companies")
            if cursor.fetchone()[0] > 0:
                return

            now_iso = datetime.now(timezone.utc).isoformat()
            
            # 16 Core Portfolio Companies across diverse sectors + sizes
            companies = [
                ("RELIANCE.NS", "Reliance Industries Ltd", "Energy & Conglomerate", "Large"),
                ("TCS.NS", "Tata Consultancy Services Ltd", "IT Services", "Large"),
                ("HDFCBANK.NS", "HDFC Bank Ltd", "Banking & Finance", "Large"),
                ("INFY.NS", "Infosys Ltd", "IT Services", "Large"),
                ("ICICIBANK.NS", "ICICI Bank Ltd", "Banking & Finance", "Large"),
                ("TITAN.NS", "Titan Company Ltd", "Consumer Goods / Luxury", "Large"),
                ("TATAMOTORS.NS", "Tata Motors Ltd", "Automotive", "Large"),
                ("LT.NS", "Larsen & Toubro Ltd", "Capital Goods & Infra", "Large"),
                ("ITC.NS", "ITC Ltd", "FMCG / Diversified", "Large"),
                ("SUNPHARMA.NS", "Sun Pharmaceutical Industries Ltd", "Pharmaceuticals", "Large"),
                ("TRENT.NS", "Trent Ltd", "Retail & Apparel", "Mid"),
                ("DIXON.NS", "Dixon Technologies Ltd", "Electronics Manufacturing", "Mid"),
                ("POLYCAB.NS", "Polycab India Ltd", "Cables & Industrial", "Mid"),
                ("ZOMATO.NS", "Zomato Ltd", "Consumer Internet", "Mid"),
                ("KPITTECH.NS", "KPIT Technologies Ltd", "Automotive Software", "Small"),
                ("CDSL.NS", "Central Depository Services Ltd", "Capital Markets FinTech", "Small"),
                ("SUZLON.NS", "Suzlon Energy Ltd", "Renewable Energy", "Small"),
            ]

            cursor.executemany(
                "INSERT INTO companies (ticker, name, sector, market_cap_category, is_in_portfolio, created_at) VALUES (?, ?, ?, ?, 1, ?)",
                [(c[0], c[1], c[2], c[3], now_iso) for c in companies]
            )

            # Default alert config
            cursor.execute("""
            INSERT OR REPLACE INTO alert_configs (id, user_id, price_change_threshold_pct, volume_surge_multiplier, notify_categories, is_active, updated_at)
            VALUES (?, ?, ?, ?, ?, 1, ?)
            """, (
                "default_config",
                "default_investor",
                3.0,
                2.0,
                json.dumps(["results", "M&A", "management_change", "litigation", "fund_raise"]),
                now_iso
            ))

            conn.commit()

db = Database()
