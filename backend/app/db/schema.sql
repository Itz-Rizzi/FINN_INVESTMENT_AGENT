-- ====================================================================
-- FINN: Financial Investment Agent - Database Schema for Supabase / PostgreSQL
-- ====================================================================

-- 1. Companies Table
CREATE TABLE IF NOT EXISTS companies (
    ticker VARCHAR(20) PRIMARY KEY, -- e.g., 'RELIANCE.NS', 'TRENT.NS'
    name VARCHAR(255) NOT NULL,
    sector VARCHAR(100) NOT NULL,
    market_cap_category VARCHAR(50) NOT NULL, -- 'Large', 'Mid', 'Small'
    is_in_portfolio BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. EOD Prices Table
CREATE TABLE IF NOT EXISTS eod_prices (
    id VARCHAR(100) PRIMARY KEY,
    ticker VARCHAR(20) NOT NULL REFERENCES companies(ticker) ON DELETE CASCADE,
    trade_date DATE NOT NULL,
    open_price NUMERIC(12, 2) NOT NULL,
    high_price NUMERIC(12, 2) NOT NULL,
    low_price NUMERIC(12, 2) NOT NULL,
    close_price NUMERIC(12, 2) NOT NULL,
    volume BIGINT NOT NULL,
    volume_sma_20 NUMERIC(14, 2),
    daily_change_pct NUMERIC(6, 2),
    UNIQUE(ticker, trade_date)
);
CREATE INDEX IF NOT EXISTS idx_eod_ticker_date ON eod_prices(ticker, trade_date DESC);

-- 3. Corporate Announcements Table (17 Categories)
CREATE TABLE IF NOT EXISTS announcements (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ticker VARCHAR(20) NOT NULL REFERENCES companies(ticker) ON DELETE CASCADE,
    company_name VARCHAR(255),
    broadcast_time TIMESTAMPTZ NOT NULL,
    category VARCHAR(50) NOT NULL, -- 1 of 17 categories: results, M&A, management_change, etc.
    title TEXT NOT NULL,
    attachment_url TEXT,
    local_pdf_path TEXT,
    is_material BOOLEAN DEFAULT FALSE,
    materiality_score NUMERIC(3, 2) DEFAULT 0.50,
    priority_level VARCHAR(20) NOT NULL, -- 'HIGH', 'MEDIUM', 'LOW'
    one_line_summary TEXT,
    enriched_data JSONB, -- Executive bio, extracted headline numbers, litigation details
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_announcements_ticker_time ON announcements(ticker, broadcast_time DESC);
CREATE INDEX IF NOT EXISTS idx_announcements_priority ON announcements(priority_level, broadcast_time DESC);

-- 4. Quarterly Results Table
CREATE TABLE IF NOT EXISTS quarterly_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ticker VARCHAR(20) NOT NULL REFERENCES companies(ticker) ON DELETE CASCADE,
    company_name VARCHAR(255) NOT NULL,
    period VARCHAR(20) NOT NULL, -- e.g. 'Q2FY25'
    filing_date DATE NOT NULL,
    revenue_cr NUMERIC(14, 2) NOT NULL,
    ebitda_cr NUMERIC(14, 2) NOT NULL,
    pbt_cr NUMERIC(14, 2) NOT NULL,
    pat_cr NUMERIC(14, 2) NOT NULL,
    ebitda_margin_pct NUMERIC(6, 2) NOT NULL,
    pat_margin_pct NUMERIC(6, 2) NOT NULL,
    revenue_qoq_pct NUMERIC(6, 2),
    revenue_yoy_pct NUMERIC(6, 2),
    ebitda_qoq_pct NUMERIC(6, 2),
    ebitda_yoy_pct NUMERIC(6, 2),
    pat_qoq_pct NUMERIC(6, 2),
    pat_yoy_pct NUMERIC(6, 2),
    citations JSONB, -- Traceable citations with source document, page number, and quote
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(ticker, period)
);

-- 5. Alert Configurations Table
CREATE TABLE IF NOT EXISTS alert_configs (
    id VARCHAR(100) PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL UNIQUE,
    price_change_threshold_pct NUMERIC(5, 2) DEFAULT 3.00,
    volume_surge_multiplier NUMERIC(4, 2) DEFAULT 2.00,
    notify_categories JSONB DEFAULT '["results", "M&A", "management_change", "litigation", "fund_raise"]'::jsonb,
    is_active BOOLEAN DEFAULT TRUE,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 6. Triggered Alerts Table
CREATE TABLE IF NOT EXISTS triggered_alerts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ticker VARCHAR(20) NOT NULL REFERENCES companies(ticker) ON DELETE CASCADE,
    company_name VARCHAR(255) NOT NULL,
    alert_type VARCHAR(50) NOT NULL, -- 'VOLUME_SURGE', 'PRICE_SWING', 'MATERIAL_ANNOUNCEMENT'
    severity VARCHAR(20) NOT NULL, -- 'CRITICAL', 'WARNING', 'INFO'
    headline TEXT NOT NULL,
    details TEXT NOT NULL,
    metrics JSONB, -- Quantitative metrics at trigger time
    is_read BOOLEAN DEFAULT FALSE,
    triggered_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_alerts_triggered_at ON triggered_alerts(triggered_at DESC);

-- 7. Document Chunks (for Grounded RAG & FAISS vector metadata sync)
CREATE TABLE IF NOT EXISTS document_chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ticker VARCHAR(20) NOT NULL REFERENCES companies(ticker) ON DELETE CASCADE,
    doc_type VARCHAR(50) NOT NULL, -- 'ANNUAL_REPORT', 'CONCALL_TRANSCRIPT', 'RESULTS_FILING'
    period VARCHAR(20) NOT NULL,
    source_filename TEXT NOT NULL,
    page_number INT NOT NULL,
    chunk_index INT NOT NULL,
    chunk_text TEXT NOT NULL,
    faiss_vector_id INT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_chunks_ticker_doc ON document_chunks(ticker, doc_type);
