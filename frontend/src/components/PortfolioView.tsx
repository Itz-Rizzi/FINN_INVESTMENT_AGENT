"use client";
import React from "react";
import { Company } from "../lib/types";
import { RefreshCw } from "lucide-react";

interface PortfolioViewProps {
  portfolio: Company[];
  loading: boolean;
  onSelectTicker: (ticker: string) => void;
}

export default function PortfolioView({
  portfolio,
  loading,
  onSelectTicker,
}: PortfolioViewProps) {
  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-lg font-extrabold tracking-tight">Monitored Portfolio</h1>
          <p className="text-xs text-finn-subtext">17 High-conviction Indian equities across Large, Mid & Growth sectors.</p>
        </div>
      </div>

      {loading ? (
        <div className="p-8 text-center text-xs text-finn-subtext">
          <RefreshCw className="w-5 h-5 animate-spin mx-auto text-blue-400 mb-2" />
          Fetching live quotes and 20-day SMA volume...
        </div>
      ) : (
        <div className="space-y-2.5">
          {portfolio.map((c) => {
            const isPos = (c.change_pct || 0) >= 0;
            const isVolSpike = (c.volume_ratio || 0) >= 2.0;

            return (
              <div
                key={c.ticker}
                onClick={() => onSelectTicker(c.ticker)}
                className="bg-finn-card border border-finn-border hover:border-blue-500/40 p-3.5 rounded-xl transition-all cursor-pointer flex items-center justify-between gap-3 shadow-md"
              >
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <span className="font-extrabold text-sm text-white">{c.ticker}</span>
                    <span className="text-[10px] font-semibold bg-finn-dark px-1.5 py-0.2 rounded border border-finn-border text-finn-subtext">
                      {c.sector}
                    </span>
                    <span className="text-[10px] font-medium text-blue-400">
                      {c.market_cap_category}
                    </span>
                  </div>
                  <div className="text-xs text-gray-300 font-medium">{c.name}</div>
                  {c.latest_announcement_title && (
                    <p className="text-[10px] text-finn-subtext truncate max-w-xs mt-1">
                      Latest: {c.latest_announcement_title}
                    </p>
                  )}
                </div>

                <div className="text-right shrink-0">
                  <div className="font-bold text-sm text-white">
                    ₹{c.last_price?.toLocaleString()}
                  </div>
                  <div className={`text-xs font-bold inline-flex items-center gap-0.5 mt-0.5 ${
                    isPos ? "text-emerald-400" : "text-rose-400"
                  }`}>
                    {isPos ? "+" : ""}{c.change_pct}%
                  </div>
                  <div className="mt-1">
                    {isVolSpike ? (
                      <span className="text-[10px] font-bold text-amber-400 bg-amber-500/10 px-1.5 py-0.5 rounded border border-amber-500/20">
                        {c.volume_ratio}× Vol Surge
                      </span>
                    ) : (
                      <span className="text-[10px] text-finn-subtext">
                        {c.volume_ratio}× SMA
                      </span>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
