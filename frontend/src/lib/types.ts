export interface Company {
  ticker: string;
  name: string;
  sector: string;
  market_cap_category: string;
  is_in_portfolio: boolean;
  last_price?: number;
  change_pct?: number;
  volume?: number;
  volume_sma_20?: number;
  volume_ratio?: number;
  latest_announcement_date?: string;
  latest_announcement_title?: string;
}

export interface CitationItem {
  source_doc: string;
  doc_type: string;
  period: string;
  page_number: number;
  quote_snippet: string;
}

export interface Announcement {
  id: string;
  ticker: string;
  company_name?: string;
  broadcast_time: string;
  category: string;
  title: string;
  attachment_url?: string;
  is_material: boolean;
  materiality_score: number;
  priority_level: "HIGH" | "MEDIUM" | "LOW";
  one_line_summary?: string;
  enriched_data?: any;
}

export interface DigestData {
  window_hours: number;
  generated_at: string;
  total_announcements: number;
  material_count: number;
  routine_count: number;
  material_announcements: Announcement[];
  routine_announcements: Announcement[];
}

export interface QuarterlyResult {
  ticker: string;
  company_name: string;
  period: string;
  filing_date: string;
  revenue_cr: number;
  ebitda_cr: number;
  pbt_cr: number;
  pat_cr: number;
  ebitda_margin_pct: number;
  pat_margin_pct: number;
  revenue_qoq_pct?: number;
  revenue_yoy_pct?: number;
  ebitda_qoq_pct?: number;
  ebitda_yoy_pct?: number;
  pat_qoq_pct?: number;
  pat_yoy_pct?: number;
  citations: CitationItem[];
}

export interface ResultsComparison {
  ticker: string;
  company_name: string;
  current_quarter: QuarterlyResult;
  previous_quarter?: QuarterlyResult;
  previous_year_quarter?: QuarterlyResult;
  headline_takeaway: string;
}

export interface AlertItem {
  id: string;
  ticker: string;
  company_name: string;
  alert_type: "VOLUME_SURGE" | "PRICE_SWING" | "MATERIAL_ANNOUNCEMENT";
  severity: "CRITICAL" | "WARNING" | "INFO";
  headline: string;
  details: string;
  metrics: Record<string, any>;
  triggered_at: string;
  is_read: boolean;
}

export interface AlertConfig {
  user_id: string;
  price_change_threshold_pct: number;
  volume_surge_multiplier: number;
  notify_categories: string[];
  is_active: boolean;
}

export interface NarrativeComparisonItem {
  quarter: string;
  promised_guidance: string;
  actual_delivered: string;
  variance_analysis: string;
  verdict: "BEAT" | "MET" | "MISSED" | "SHIFTED_GOALPOSTS";
  guidance_citation: CitationItem;
  actual_citation: CitationItem;
}

export interface NarrativeData {
  ticker: string;
  company_name: string;
  executive_summary: string;
  credibility_score: "HIGH" | "MODERATE" | "LOW";
  items: NarrativeComparisonItem[];
}

export interface ResearchDossier {
  ticker: string;
  name: string;
  sector: string;
  market_cap: string;
  business_snapshot: {
    overview: string;
    revenue_mix: Array<{ segment: string; share_pct: number }>;
    store_footprint: string;
  };
  financial_snapshot: {
    current_revenue_cr: number;
    ebitda_margin_pct: number;
    pat_margin_pct: number;
    roce_pct: number;
    roe_pct: number;
    pe_ratio: number;
  };
  trajectory: {
    multi_year_cagr_3yr_sales: string;
    multi_year_cagr_3yr_pat: string;
    what_is_growing: string;
    what_is_compressing: string;
  };
  balance_sheet: {
    debt_to_equity: number;
    net_debt_cr: number;
    working_capital_days: number;
    funding_structure: string;
  };
  cash_quality: {
    cfo_cr: number;
    pat_cr: number;
    cash_conversion_pct: number;
    free_cash_flow_cr: number;
    assessment: string;
  };
  guidance: {
    store_additions: string;
    margin_target: string;
    capex_plan: string;
  };
  bull_vs_bear: {
    bull_case: string;
    bear_case: string;
  };
  citations: CitationItem[];
}

export interface CopilotResponse {
  answer: string;
  citations: CitationItem[];
  suggested_followups: string[];
}
