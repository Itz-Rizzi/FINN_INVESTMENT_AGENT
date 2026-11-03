import { 
  Company, 
  DigestData, 
  AlertItem, 
  AlertConfig, 
  ResultsComparison, 
  NarrativeData, 
  ResearchDossier, 
  CopilotResponse 
} from "./types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

async function fetchJson<T>(url: string, options?: RequestInit): Promise<T> {
  const res = await fetch(url, options);
  if (!res.ok) {
    const errorText = await res.text();
    throw new Error(`API error ${res.status}: ${errorText}`);
  }
  return res.json();
}

export async function fetchPortfolio(): Promise<{ total: number; companies: Company[] }> {
  return fetchJson<{ total: number; companies: Company[] }>(`${API_BASE}/portfolio`);
}

export async function fetchDigest(windowHours: number = 24, ticker?: string): Promise<DigestData> {
  let url = `${API_BASE}/digest?window_hours=${windowHours}`;
  if (ticker) url += `&ticker=${encodeURIComponent(ticker)}`;
  return fetchJson<DigestData>(url);
}

export async function fetchAlertsFeed(limit: number = 50, unreadOnly: boolean = false): Promise<AlertItem[]> {
  return fetchJson<AlertItem[]>(`${API_BASE}/alerts/feed?limit=${limit}&unread_only=${unreadOnly}`);
}

export async function fetchAlertConfig(): Promise<AlertConfig> {
  return fetchJson<AlertConfig>(`${API_BASE}/alerts/config`);
}

export async function updateAlertConfig(config: AlertConfig): Promise<AlertConfig> {
  return fetchJson<AlertConfig>(`${API_BASE}/alerts/config`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(config),
  });
}

export async function markAlertRead(alertId: string): Promise<void> {
  await fetchJson(`${API_BASE}/alerts/${alertId}/read`, { method: "POST" });
}

export async function triggerScanAlerts(): Promise<{ triggered_count: number; alerts: any[] }> {
  return fetchJson(`${API_BASE}/alerts/scan`, { method: "POST" });
}

export async function fetchQuarterlyResults(ticker: string): Promise<ResultsComparison> {
  return fetchJson<ResultsComparison>(`${API_BASE}/results/${encodeURIComponent(ticker)}`);
}

export async function fetchNarrativeVsNumbers(ticker: string): Promise<NarrativeData> {
  return fetchJson<NarrativeData>(`${API_BASE}/research/${encodeURIComponent(ticker)}/narrative-vs-numbers`);
}

export async function fetchResearchDossier(ticker: string): Promise<ResearchDossier> {
  return fetchJson<ResearchDossier>(`${API_BASE}/research/${encodeURIComponent(ticker)}/snapshot`);
}

export async function queryCopilot(query: string, ticker?: string): Promise<CopilotResponse> {
  return fetchJson<CopilotResponse>(`${API_BASE}/copilot/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query, ticker }),
  });
}
