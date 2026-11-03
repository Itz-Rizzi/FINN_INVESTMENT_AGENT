"use client";
import React from "react";
import { X, UserCheck, Briefcase, GraduationCap, Award, ExternalLink } from "lucide-react";

interface ExecutiveBioModalProps {
  bio: {
    name: string;
    role_change: string;
    company: string;
    prior_experience: string;
    education?: string;
    key_strengths?: string[];
    source?: string;
  } | null;
  onClose: () => void;
}

export default function ExecutiveBioModal({ bio, onClose }: ExecutiveBioModalProps) {
  if (!bio) return null;

  return (
    <div className="fixed inset-0 z-50 bg-black/75 backdrop-blur-sm flex items-end sm:items-center justify-center p-0 sm:p-4 animate-in fade-in duration-200">
      <div className="bg-finn-card border border-finn-border rounded-t-2xl sm:rounded-2xl w-full max-w-lg max-h-[85vh] overflow-y-auto p-5 text-white shadow-2xl">
        {/* Header */}
        <div className="flex items-start justify-between border-b border-finn-border pb-3">
          <div className="flex items-center gap-2.5">
            <div className="w-10 h-10 rounded-full bg-blue-600/20 border border-blue-500/40 flex items-center justify-center text-blue-400">
              <UserCheck className="w-5 h-5" />
            </div>
            <div>
              <h3 className="font-bold text-base leading-snug">{bio.name}</h3>
              <p className="text-xs text-blue-400 font-medium">{bio.role_change} • {bio.company}</p>
            </div>
          </div>
          <button onClick={onClose} className="p-1 rounded-full text-finn-subtext hover:text-white hover:bg-finn-border transition-colors">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Body */}
        <div className="mt-4 space-y-4 text-xs">
          <div>
            <div className="flex items-center gap-1.5 text-finn-subtext font-semibold uppercase tracking-wider mb-1">
              <Briefcase className="w-3.5 h-3.5 text-blue-400" />
              <span>Executive Career & Prior Experience</span>
            </div>
            <p className="bg-finn-dark/60 p-3 rounded-lg border border-finn-border/60 text-gray-200 leading-relaxed">
              {bio.prior_experience}
            </p>
          </div>

          {bio.education && (
            <div>
              <div className="flex items-center gap-1.5 text-finn-subtext font-semibold uppercase tracking-wider mb-1">
                <GraduationCap className="w-3.5 h-3.5 text-emerald-400" />
                <span>Education & Credentials</span>
              </div>
              <p className="bg-finn-dark/60 p-3 rounded-lg border border-finn-border/60 text-gray-200">
                {bio.education}
              </p>
            </div>
          )}

          {bio.key_strengths && bio.key_strengths.length > 0 && (
            <div>
              <div className="flex items-center gap-1.5 text-finn-subtext font-semibold uppercase tracking-wider mb-1.5">
                <Award className="w-3.5 h-3.5 text-amber-400" />
                <span>Key Competencies & Value Drivers</span>
              </div>
              <div className="flex flex-wrap gap-1.5">
                {bio.key_strengths.map((str, i) => (
                  <span key={i} className="bg-blue-950/60 text-blue-300 border border-blue-800/60 px-2.5 py-1 rounded-md text-[11px] font-medium">
                    {str}
                  </span>
                ))}
              </div>
            </div>
          )}

          <div className="pt-2 border-t border-finn-border/60 flex items-center justify-between text-[11px] text-finn-subtext">
            <span>Source: {bio.source || "Public Filings"}</span>
            <span className="text-emerald-400 font-medium flex items-center gap-1">
              Verified Primary Disclosure
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
