"use client";
import React, { useState } from "react";
import { ResearchDossier, NarrativeData, ResultsComparison, CitationItem } from "../lib/types";
import ResultsCard from "./ResultsCard";
import { 
  Scale, 
  FileText, 
  Building2, 
  TrendingUp, 
  TrendingDown, 
  Layers, 
  Coins, 
  Compass, 
  RefreshCw 
} from "lucide-react";

interface ResearchViewProps {
  selectedTicker: string;
  researchDossier: ResearchDossier | null;
  narrativeData: NarrativeData | null;
  resultsComparison: ResultsComparison | null;
  loading: boolean;
  onOpenCitation: (cite: CitationItem) => void;
}

export default function ResearchView({
  selectedTicker,
  researchDossier,
  narrativeData,
  resultsComparison,
  loading,
  onOpenCitation,
}: ResearchViewProps) {
  const [subTab, setSubTab] = useState<string>("narrative");

  return (
    <div className="space-y-4">
      {/* Header with Ticker Badge */}
      <div className="flex items-start justify-between">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-xl font-extrabold tracking-tight text-white">{selectedTicker}</h1>
            <span className="text-xs font-semibold bg-blue-500/10 text-blue-400 border border-blue-500/20 px-2 py-0.5 rounded">
              Primary Data Only
            </span>
          </div>
          <p className="text-xs text-finn-subtext mt-0.5">
            {researchDossier ? `${researchDossier.name} • ${researchDossier.sector}` : "On-demand pull analysis"}
          </p>
        </div>
      </div>

      {/* Sub-menu Pills */}
      <div className="flex gap-1.5 overflow-x-auto no-scrollbar py-1">
        {[
          { id: "narrative", label: "Narrative vs. Numbers", icon: Scale },
          { id: "results", label: "Quarterly Results", icon: FileText },
          { id: "business", label: "Business Snapshot", icon: Building2 },
          { id: "trajectory", label: "Trajectory", icon: TrendingUp },
          { id: "balance", label: "Balance Sheet", icon: Layers },
          { id: "cash", label: "Cash Quality", icon: Coins },
          { id: "bullbear", label: "Bull vs. Bear", icon: Compass },
        ].map((item) => {
          const Icon = item.icon;
          const isSelected = subTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setSubTab(item.id)}
              className={`flex items-center gap-1.5 whitespace-nowrap text-xs px-3 py-1.5 rounded-xl font-medium transition-all shrink-0 ${
                isSelected
                  ? "bg-blue-600 text-white font-bold shadow-md shadow-blue-500/20"
                  : "bg-finn-card border border-finn-border text-finn-subtext hover:text-white"
              }`}
            >
              <Icon className="w-3.5 h-3.5" />
              <span>{item.label}</span>
            </button>
          );
        })}
      </div>

      {loading ? (
        <div className="p-8 text-center text-xs text-finn-subtext">
          <RefreshCw className="w-5 h-5 animate-spin mx-auto text-blue-400 mb-2" />
          Fetching filings and computing primary ratios...
        </div>
      ) : (
        <div className="space-y-4">
          {/* 1. NARRATIVE VS NUMBERS (FLAGSHIP) */}
          {subTab === "narrative" && narrativeData && (
            <div className="space-y-3.5">
              <div className="bg-finn-card border border-finn-border rounded-xl p-4 shadow-md">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-bold uppercase tracking-wider text-blue-400">
                    Management Credibility Audit
                  </span>
                  <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-500/15 text-emerald-300 border border-emerald-500/30">
                    Credibility: {narrativeData.credibility_score}
                  </span>
                </div>
                <p className="text-xs text-gray-200 leading-relaxed bg-finn-dark/70 p-3 rounded-lg border border-finn-border/60">
                  {narrativeData.executive_summary}
                </p>
              </div>

              <div className="space-y-3">
                {narrativeData.items.map((item, idx) => {
                  const isBeat = item.verdict === "BEAT";
                  const isMet = item.verdict === "MET";
                  const isMissed = item.verdict === "MISSED";

                  return (
                    <div
                      key={idx}
                      className="bg-finn-card border border-finn-border rounded-xl p-4 shadow-md space-y-3"
                    >
                      <div className="flex items-center justify-between border-b border-finn-border/70 pb-2">
                        <span className="font-extrabold text-sm text-white">{item.quarter}</span>
                        <span className={`text-[10px] font-extrabold px-2 py-0.5 rounded tracking-wide ${
                          isBeat
                            ? "bg-emerald-500/20 text-emerald-300 border border-emerald-500/30"
                            : isMet
                            ? "bg-blue-500/20 text-blue-300 border border-blue-500/30"
                            : isMissed
                            ? "bg-rose-500/20 text-rose-300 border border-rose-500/30"
                            : "bg-amber-500/20 text-amber-300 border border-amber-500/30"
                        }`}>
                          {item.verdict.replace("_", " ")}
                        </span>
                      </div>

                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5 text-xs">
                        <div className="bg-finn-dark/60 p-2.5 rounded-lg border border-finn-border/60 space-y-1.5">
                          <div className="text-[10px] font-bold uppercase tracking-wider text-blue-400">
                            Management Guidance & Story
                          </div>
                          <p className="text-gray-300 leading-relaxed">{item.promised_guidance}</p>
                          <button
                            onClick={() => onOpenCitation(item.guidance_citation)}
                            className="text-[10px] font-semibold text-emerald-400 hover:text-emerald-300 flex items-center gap-1 pt-1"
                          >
                            <FileText className="w-3 h-3" />
                            <span>Citation [p.{item.guidance_citation.page_number}]</span>
                          </button>
                        </div>

                        <div className="bg-finn-dark/60 p-2.5 rounded-lg border border-finn-border/60 space-y-1.5">
                          <div className="text-[10px] font-bold uppercase tracking-wider text-emerald-400">
                            Actual Delivered Financials
                          </div>
                          <p className="text-gray-300 leading-relaxed">{item.actual_delivered}</p>
                          <button
                            onClick={() => onOpenCitation(item.actual_citation)}
                            className="text-[10px] font-semibold text-emerald-400 hover:text-emerald-300 flex items-center gap-1 pt-1"
                          >
                            <FileText className="w-3 h-3" />
                            <span>Citation [p.{item.actual_citation.page_number}]</span>
                          </button>
                        </div>
                      </div>

                      <div className="text-[11px] text-gray-300 bg-finn-cardHover p-2 rounded-lg border border-finn-border/50">
                        <span className="font-bold text-white">Variance Analysis: </span>
                        {item.variance_analysis}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {/* 2. QUARTERLY RESULTS COMPARISON */}
          {subTab === "results" && resultsComparison && (
            <ResultsCard
              data={resultsComparison}
              onOpenCitation={onOpenCitation}
            />
          )}

          {/* 3. BUSINESS SNAPSHOT */}
          {subTab === "business" && researchDossier && (
            <div className="bg-finn-card border border-finn-border rounded-xl p-4 shadow-md space-y-4 text-xs">
              <div>
                <h3 className="font-bold text-sm text-white mb-1.5">Business Overview</h3>
                <p className="text-gray-300 leading-relaxed bg-finn-dark/60 p-3 rounded-lg border border-finn-border/60">
                  {researchDossier.business_snapshot.overview}
                </p>
              </div>

              <div>
                <h3 className="font-bold text-xs uppercase tracking-wider text-finn-subtext mb-2">Revenue Mix by Segment</h3>
                <div className="space-y-2">
                  {researchDossier.business_snapshot.revenue_mix.map((seg, i) => (
                    <div key={i} className="space-y-1">
                      <div className="flex justify-between text-xs">
                        <span className="text-gray-200">{seg.segment}</span>
                        <span className="font-bold text-blue-400">{seg.share_pct}%</span>
                      </div>
                      <div className="w-full bg-finn-dark rounded-full h-2">
                        <div
                          className="bg-blue-500 h-2 rounded-full"
                          style={{ width: `${seg.share_pct}%` }}
                        ></div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="pt-2 border-t border-finn-border/60">
                <span className="text-finn-subtext">Operating Footprint: </span>
                <span className="text-gray-200 font-medium">{researchDossier.business_snapshot.store_footprint}</span>
              </div>
            </div>
          )}

          {/* 4. TRAJECTORY */}
          {subTab === "trajectory" && researchDossier && (
            <div className="bg-finn-card border border-finn-border rounded-xl p-4 shadow-md space-y-3.5 text-xs">
              <div className="grid grid-cols-2 gap-2.5">
                <div className="bg-finn-dark/60 p-3 rounded-lg border border-finn-border/60">
                  <span className="text-finn-subtext text-[11px]">3-Year Sales CAGR</span>
                  <div className="text-lg font-bold text-emerald-400 mt-1">
                    {researchDossier.trajectory.multi_year_cagr_3yr_sales}
                  </div>
                </div>
                <div className="bg-finn-dark/60 p-3 rounded-lg border border-finn-border/60">
                  <span className="text-finn-subtext text-[11px]">3-Year PAT CAGR</span>
                  <div className="text-lg font-bold text-emerald-400 mt-1">
                    {researchDossier.trajectory.multi_year_cagr_3yr_pat}
                  </div>
                </div>
              </div>

              <div className="space-y-2 pt-1">
                <div className="bg-finn-dark/60 p-3 rounded-lg border border-finn-border/60">
                  <div className="font-bold text-emerald-400 mb-1 flex items-center gap-1.5">
                    <TrendingUp className="w-3.5 h-3.5" />
                    <span>What is Growing</span>
                  </div>
                  <p className="text-gray-300 leading-relaxed">{researchDossier.trajectory.what_is_growing}</p>
                </div>

                <div className="bg-finn-dark/60 p-3 rounded-lg border border-finn-border/60">
                  <div className="font-bold text-rose-400 mb-1 flex items-center gap-1.5">
                    <TrendingDown className="w-3.5 h-3.5" />
                    <span>What is Compressing</span>
                  </div>
                  <p className="text-gray-300 leading-relaxed">{researchDossier.trajectory.what_is_compressing}</p>
                </div>
              </div>
            </div>
          )}

          {/* 5. BALANCE SHEET */}
          {subTab === "balance" && researchDossier && (
            <div className="bg-finn-card border border-finn-border rounded-xl p-4 shadow-md space-y-3 text-xs">
              <div className="grid grid-cols-2 gap-2.5">
                <div className="bg-finn-dark/60 p-3 rounded-lg border border-finn-border/60">
                  <span className="text-finn-subtext text-[11px]">Debt-to-Equity (D/E)</span>
                  <div className="text-lg font-bold text-white mt-1">
                    {researchDossier.balance_sheet.debt_to_equity}
                  </div>
                  <span className="text-[10px] text-emerald-400">Conservative Leverage</span>
                </div>
                <div className="bg-finn-dark/60 p-3 rounded-lg border border-finn-border/60">
                  <span className="text-finn-subtext text-[11px]">Working Capital Cycle</span>
                  <div className="text-lg font-bold text-white mt-1">
                    {researchDossier.balance_sheet.working_capital_days} Days
                  </div>
                  <span className="text-[10px] text-blue-400">Rapid inventory turn</span>
                </div>
              </div>

              <div className="bg-finn-dark/60 p-3 rounded-lg border border-finn-border/60">
                <span className="font-bold text-white">Funding Structure: </span>
                <p className="text-gray-300 mt-1 leading-relaxed">
                  {researchDossier.balance_sheet.funding_structure}
                </p>
              </div>
            </div>
          )}

          {/* 6. CASH QUALITY */}
          {subTab === "cash" && researchDossier && (
            <div className="bg-finn-card border border-finn-border rounded-xl p-4 shadow-md space-y-3.5 text-xs">
              <div className="grid grid-cols-2 gap-2.5">
                <div className="bg-finn-dark/60 p-3 rounded-lg border border-finn-border/60">
                  <span className="text-finn-subtext text-[11px]">Cash Conversion (CFO / PAT)</span>
                  <div className="text-lg font-bold text-emerald-400 mt-1">
                    {researchDossier.cash_quality.cash_conversion_pct}%
                  </div>
                  <span className="text-[10px] text-gray-400">High earnings quality</span>
                </div>
                <div className="bg-finn-dark/60 p-3 rounded-lg border border-finn-border/60">
                  <span className="text-finn-subtext text-[11px]">Free Cash Flow (FCF)</span>
                  <div className="text-lg font-bold text-white mt-1">
                    ₹{researchDossier.cash_quality.free_cash_flow_cr.toLocaleString()} Cr
                  </div>
                  <span className="text-[10px] text-emerald-400">Surplus post capex</span>
                </div>
              </div>

              <div className="bg-finn-dark/60 p-3 rounded-lg border border-finn-border/60 leading-relaxed text-gray-200">
                <span className="font-bold text-emerald-400">Cash Flow Assessment: </span>
                {researchDossier.cash_quality.assessment}
              </div>
            </div>
          )}

          {/* 7. BULL VS BEAR */}
          {subTab === "bullbear" && researchDossier && (
            <div className="space-y-3 text-xs">
              <div className="bg-finn-card border border-emerald-500/30 rounded-xl p-4 shadow-md">
                <div className="flex items-center gap-1.5 font-bold text-emerald-400 text-xs uppercase tracking-wider mb-2">
                  <TrendingUp className="w-4 h-4" />
                  <span>The Bull Case (Core Value Drivers)</span>
                </div>
                <p className="text-gray-200 leading-relaxed bg-finn-dark/60 p-3 rounded-lg border border-finn-border/60">
                  {researchDossier.bull_vs_bear.bull_case}
                </p>
              </div>

              <div className="bg-finn-card border border-rose-500/30 rounded-xl p-4 shadow-md">
                <div className="flex items-center gap-1.5 font-bold text-rose-400 text-xs uppercase tracking-wider mb-2">
                  <TrendingDown className="w-4 h-4" />
                  <span>The Bear Case (Key Structural Risks)</span>
                </div>
                <p className="text-gray-200 leading-relaxed bg-finn-dark/60 p-3 rounded-lg border border-finn-border/60">
                  {researchDossier.bull_vs_bear.bear_case}
                </p>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
