"use client";
import React from "react";
import { X, FileText, CheckCircle2, Bookmark } from "lucide-react";
import { CitationItem } from "../lib/types";

interface CitationModalProps {
  citation: CitationItem | null;
  onClose: () => void;
}

export default function CitationModal({ citation, onClose }: CitationModalProps) {
  if (!citation) return null;

  return (
    <div className="fixed inset-0 z-50 bg-black/75 backdrop-blur-sm flex items-end sm:items-center justify-center p-0 sm:p-4 animate-in fade-in duration-200">
      <div className="bg-finn-card border border-finn-border rounded-t-2xl sm:rounded-2xl w-full max-w-lg p-5 text-white shadow-2xl">
        <div className="flex items-start justify-between border-b border-finn-border pb-3">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
              <FileText className="w-4 h-4" />
            </div>
            <div>
              <h4 className="font-bold text-sm">{citation.source_doc}</h4>
              <p className="text-[11px] text-finn-subtext">
                {citation.doc_type} • {citation.period} • <span className="text-emerald-400 font-semibold">Page {citation.page_number}</span>
              </p>
            </div>
          </div>
          <button onClick={onClose} className="p-1 rounded-full text-finn-subtext hover:text-white hover:bg-finn-border transition-colors">
            <X className="w-4 h-4" />
          </button>
        </div>

        <div className="mt-4">
          <div className="flex items-center gap-1 text-[11px] text-emerald-400 font-semibold uppercase tracking-wider mb-2">
            <CheckCircle2 className="w-3.5 h-3.5" />
            <span>Verbatim Primary Source Excerpt</span>
          </div>
          <div className="bg-finn-dark p-3.5 rounded-lg border border-finn-border text-xs text-gray-200 leading-relaxed font-mono">
            &ldquo;{citation.quote_snippet}&rdquo;
          </div>
          <p className="text-[10px] text-finn-subtext mt-2 italic">
            Extracted directly from exchange filings and investor disclosures via PyMuPDF with zero LLM extrapolation.
          </p>
        </div>
      </div>
    </div>
  );
}
