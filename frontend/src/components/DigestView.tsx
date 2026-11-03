"use client";
import React, { useState } from "react";
import { DigestData, Announcement } from "../lib/types";
import { ChevronDown, ChevronUp, UserCheck, Sparkles, ExternalLink, RefreshCw } from "lucide-react";

interface DigestViewProps {
  digest: DigestData | null;
  loading: boolean;
  windowHours: number;
  onSelectWindow: (hours: number) => void;
  onOpenBio: (bio: any) => void;
  onOpenResearch: (ticker: string) => void;
}

export default function DigestView({
  digest,
  loading,
  windowHours,
  onSelectWindow,
  onOpenBio,
  onOpenResearch,
}: DigestViewProps) {
  const [showRoutine, setShowRoutine] = useState<boolean>(false);

  return (
    <div className="space-y-4">
      {/* Window Selector */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-lg font-extrabold tracking-tight">Push Digest</h1>
          <p className="text-xs text-finn-subtext">Material announcements prioritized; routine noise collapsed.</p>
        </div>
        <div className="flex items-center gap-1 bg-finn-card border border-finn-border p-1 rounded-xl">
          {[
            { label: "24h", hours: 24 },
            { label: "3d", hours: 72 },
            { label: "7d", hours: 168 },
            { label: "30d", hours: 720 },
          ].map((w) => (
            <button
              key={w.hours}
              onClick={() => onSelectWindow(w.hours)}
              className={`text-xs px-2.5 py-1 rounded-lg font-medium transition-all ${
                windowHours === w.hours
                  ? "bg-blue-600 text-white font-bold shadow"
                  : "text-finn-subtext hover:text-white"
              }`}
            >
              {w.label}
            </button>
          ))}
        </div>
      </div>

      {loading ? (
        <div className="p-8 text-center text-xs text-finn-subtext">
          <RefreshCw className="w-5 h-5 animate-spin mx-auto text-blue-400 mb-2" />
          Aggregating exchange filings across portfolio...
        </div>
      ) : digest ? (
        <div className="space-y-4">
          {/* Section: Material Announcements */}
          <div>
            <div className="flex items-center justify-between mb-2.5">
              <div className="flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
                <h2 className="text-xs font-bold uppercase tracking-wider text-white">
                  Material Developments ({digest.material_count})
                </h2>
              </div>
              <span className="text-[11px] text-finn-subtext font-mono">
                Window: Last {digest.window_hours} Hours
              </span>
            </div>

            {digest.material_announcements.length === 0 ? (
              <div className="bg-finn-card border border-finn-border rounded-xl p-6 text-center text-xs text-finn-subtext">
                No high-materiality filings in this window. Routine compliance filings are collapsed below.
              </div>
            ) : (
              <div className="space-y-3">
                {digest.material_announcements.map((ann) => (
                  <div
                    key={ann.id}
                    className="bg-finn-card border border-finn-border hover:border-blue-500/40 rounded-xl p-4 transition-all shadow-md"
                  >
                    <div className="flex items-start justify-between gap-2 mb-2">
                      <div className="flex items-center gap-2 flex-wrap">
                        <span className="font-extrabold text-white text-xs bg-finn-dark px-2 py-0.5 rounded border border-finn-border">
                          {ann.ticker}
                        </span>
                        <span className="text-[11px] font-semibold text-blue-400">
                          {ann.company_name}
                        </span>
                        <span className="text-[10px] font-bold uppercase px-2 py-0.5 rounded bg-blue-500/10 text-blue-300 border border-blue-500/20">
                          {ann.category}
                        </span>
                      </div>
                      <span className="text-[10px] text-finn-subtext shrink-0">
                        {new Date(ann.broadcast_time).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
                      </span>
                    </div>

                    <h3 className="font-bold text-sm text-gray-100 leading-snug mb-2">
                      {ann.title}
                    </h3>

                    {ann.one_line_summary && (
                      <p className="text-xs text-gray-300 bg-finn-dark/80 p-2.5 rounded-lg border border-finn-border/60 mb-2 leading-relaxed">
                        {ann.one_line_summary}
                      </p>
                    )}

                    {/* Action Badges */}
                    <div className="flex items-center justify-between pt-1">
                      <div className="flex items-center gap-2">
                        {ann.category === "management_change" && ann.enriched_data && (
                          <button
                            onClick={() => onOpenBio(ann.enriched_data)}
                            className="inline-flex items-center gap-1 text-[11px] font-bold bg-blue-600/20 hover:bg-blue-600/30 text-blue-400 border border-blue-500/30 px-2.5 py-1 rounded-lg transition-colors"
                          >
                            <UserCheck className="w-3.5 h-3.5" />
                            <span>Executive Bio</span>
                          </button>
                        )}

                        {ann.category === "results" && (
                          <button
                            onClick={() => onOpenResearch(ann.ticker)}
                            className="inline-flex items-center gap-1 text-[11px] font-bold bg-emerald-600/20 hover:bg-emerald-600/30 text-emerald-400 border border-emerald-500/30 px-2.5 py-1 rounded-lg transition-colors"
                          >
                            <Sparkles className="w-3.5 h-3.5" />
                            <span>QoQ / YoY Extraction</span>
                          </button>
                        )}
                      </div>

                      {ann.attachment_url && (
                        <a
                          href={ann.attachment_url}
                          target="_blank"
                          rel="noreferrer"
                          className="inline-flex items-center gap-1 text-[11px] text-finn-subtext hover:text-white transition-colors"
                        >
                          <span>Filing</span>
                          <ExternalLink className="w-3 h-3" />
                        </a>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Routine Section (Collapsed) */}
          <div className="pt-2">
            <button
              onClick={() => setShowRoutine(!showRoutine)}
              className="w-full flex items-center justify-between p-3 bg-finn-card/60 hover:bg-finn-card border border-finn-border rounded-xl text-xs text-finn-subtext transition-all"
            >
              <div className="flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-gray-500"></span>
                <span>
                  Routine Administrative Filings ({digest.routine_count}) — ESOPs, compliance certificates
                </span>
              </div>
              {showRoutine ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
            </button>

            {showRoutine && (
              <div className="mt-2 space-y-2 animate-in fade-in duration-150">
                {digest.routine_announcements.map((ann) => (
                  <div
                    key={ann.id}
                    className="p-3 bg-finn-dark/60 border border-finn-border/60 rounded-lg text-xs flex items-center justify-between gap-3"
                  >
                    <div>
                      <div className="flex items-center gap-2 mb-1">
                        <span className="font-bold text-gray-300">{ann.ticker}</span>
                        <span className="text-[10px] text-gray-500 font-medium uppercase px-1.5 py-0.2 bg-gray-800 rounded">
                          {ann.category}
                        </span>
                      </div>
                      <p className="text-gray-400 text-[11px] leading-tight">
                        {ann.one_line_summary || ann.title}
                      </p>
                    </div>
                    <span className="text-[10px] text-gray-500 shrink-0 font-mono">
                      {new Date(ann.broadcast_time).toLocaleDateString([], { month: "short", day: "numeric" })}
                    </span>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      ) : null}
    </div>
  );
}
