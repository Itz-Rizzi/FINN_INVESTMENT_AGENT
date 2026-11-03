"use client";
import React from "react";
import { TrendingUp, TrendingDown, ArrowUpRight, FileCheck } from "lucide-react";
import { ResultsComparison, CitationItem } from "../lib/types";

interface ResultsCardProps {
  data: ResultsComparison;
  onOpenCitation: (cite: CitationItem) => void;
}

export default function ResultsCard({ data, onOpenCitation }: ResultsCardProps) {
  const cur = data.current_quarter;

  const renderDelta = (val?: number, label: string = "") => {
    if (val === undefined || val === null) return <span className="text-gray-500 text-xs">--</span>;
    const isPositive = val >= 0;
    return (
      <span className={`inline-flex items-center gap-0.5 text-[11px] font-bold px-1.5 py-0.5 rounded ${
        isPositive ? "bg-emerald-500/15 text-emerald-400" : "bg-rose-500/15 text-rose-400"
      }`}>
        {isPositive ? <TrendingUp className="w-3 h-3" /> : <TrendingDown className="w-3 h-3" />}
        {isPositive ? `+${val}%` : `${val}%`} {label}
      </span>
    );
  };

  return (
    <div className="bg-finn-card border border-finn-border rounded-xl p-4 shadow-lg">
      <div className="flex items-center justify-between border-b border-finn-border/80 pb-2.5 mb-3">
        <div>
          <div className="flex items-center gap-1.5">
            <h3 className="font-extrabold text-white text-base">{data.company_name}</h3>
            <span className="text-[10px] font-semibold bg-blue-500/20 text-blue-400 px-1.5 py-0.2 rounded border border-blue-500/30">
              {cur.period}
            </span>
          </div>
          <p className="text-[11px] text-finn-subtext mt-0.5">Reported on {cur.filing_date}</p>
        </div>
        {cur.citations && cur.citations.length > 0 && (
          <button
            onClick={() => onOpenCitation(cur.citations[0])}
            className="flex items-center gap-1 text-[11px] font-semibold text-emerald-400 hover:text-emerald-300 bg-emerald-500/10 px-2 py-1 rounded-md border border-emerald-500/20 transition-colors"
          >
            <FileCheck className="w-3.5 h-3.5" />
            <span>Citation [p.{cur.citations[0].page_number}]</span>
          </button>
        )}
      </div>

      {/* Headline Takeaway */}
      <div className="bg-finn-dark/70 p-2.5 rounded-lg border border-finn-border/60 text-xs text-gray-200 mb-3.5 leading-relaxed">
        {data.headline_takeaway}
      </div>

      {/* 4 Headline Metrics Grid */}
      <div className="grid grid-cols-2 gap-2.5">
        {/* Revenue */}
        <div className="bg-finn-dark/50 p-3 rounded-lg border border-finn-border/60">
          <div className="text-[11px] text-finn-subtext font-medium">Revenue (Total Sales)</div>
          <div className="text-base font-bold text-white mt-1">₹{cur.revenue_cr.toLocaleString()} Cr</div>
          <div className="flex flex-wrap items-center gap-1.5 mt-2">
            {renderDelta(cur.revenue_qoq_pct, "QoQ")}
            {renderDelta(cur.revenue_yoy_pct, "YoY")}
          </div>
        </div>

        {/* EBITDA */}
        <div className="bg-finn-dark/50 p-3 rounded-lg border border-finn-border/60">
          <div className="text-[11px] text-finn-subtext font-medium">EBITDA (Operating Profit)</div>
          <div className="text-base font-bold text-white mt-1">₹{cur.ebitda_cr.toLocaleString()} Cr</div>
          <div className="flex flex-wrap items-center gap-1.5 mt-2">
            <span className="text-[11px] font-semibold text-blue-400 bg-blue-500/10 px-1.5 py-0.5 rounded border border-blue-500/20">
              {cur.ebitda_margin_pct}% Mgn
            </span>
            {renderDelta(cur.ebitda_yoy_pct, "YoY")}
          </div>
        </div>

        {/* PBT */}
        <div className="bg-finn-dark/50 p-3 rounded-lg border border-finn-border/60">
          <div className="text-[11px] text-finn-subtext font-medium">PBT (Profit Before Tax)</div>
          <div className="text-base font-bold text-white mt-1">₹{cur.pbt_cr.toLocaleString()} Cr</div>
          <div className="flex items-center gap-1.5 mt-2">
            <span className="text-[11px] text-finn-subtext">Pre-tax Profit</span>
          </div>
        </div>

        {/* PAT */}
        <div className="bg-finn-dark/50 p-3 rounded-lg border border-finn-border/60">
          <div className="text-[11px] text-finn-subtext font-medium">PAT (Net Profit)</div>
          <div className="text-base font-bold text-emerald-400 mt-1">₹{cur.pat_cr.toLocaleString()} Cr</div>
          <div className="flex flex-wrap items-center gap-1.5 mt-2">
            <span className="text-[11px] font-semibold text-emerald-400 bg-emerald-500/10 px-1.5 py-0.5 rounded border border-emerald-500/20">
              {cur.pat_margin_pct}% Mgn
            </span>
            {renderDelta(cur.pat_yoy_pct, "YoY")}
          </div>
        </div>
      </div>
    </div>
  );
}
