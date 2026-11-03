"use client";
import React, { useState } from "react";
import { Search, Bell, Activity, Sparkles } from "lucide-react";

interface HeaderProps {
  onSearchTicker: (ticker: string) => void;
  unreadAlertCount: number;
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

export default function Header({ onSearchTicker, unreadAlertCount, activeTab, setActiveTab }: HeaderProps) {
  const [searchInput, setSearchInput] = useState("");

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchInput.trim()) {
      onSearchTicker(searchInput.trim().toUpperCase());
      setActiveTab("research");
      setSearchInput("");
    }
  };

  return (
    <header className="sticky top-0 z-40 bg-finn-dark/95 backdrop-blur-md border-b border-finn-border px-4 py-3">
      <div className="max-w-2xl mx-auto flex items-center justify-between gap-3">
        {/* Brand & Status */}
        <div className="flex items-center gap-2 cursor-pointer" onClick={() => setActiveTab("digest")}>
          <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center font-bold text-white shadow-md shadow-blue-500/20">
            F
          </div>
          <div>
            <div className="flex items-center gap-1.5">
              <span className="font-extrabold text-base tracking-tight text-white">FINN</span>
              <span className="text-[10px] font-semibold bg-blue-500/10 text-blue-400 border border-blue-500/20 px-1.5 py-0.2 rounded">
                ENAM AGENT
              </span>
            </div>
            <div className="flex items-center gap-1 text-[11px] text-emerald-400 font-medium">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
              <span>17 Stocks Active</span>
            </div>
          </div>
        </div>

        {/* Universal Search Bar */}
        <form onSubmit={handleSearch} className="flex-1 max-w-[200px] sm:max-w-xs relative">
          <input
            type="text"
            placeholder="Search any NSE ticker..."
            value={searchInput}
            onChange={(e) => setSearchInput(e.target.value)}
            className="w-full bg-finn-card border border-finn-border rounded-full pl-8 pr-3 py-1.5 text-xs text-white placeholder-finn-subtext focus:outline-none focus:border-blue-500 transition-colors"
          />
          <Search className="w-3.5 h-3.5 text-finn-subtext absolute left-2.5 top-2.5" />
        </form>

        {/* Alerts Pill */}
        <button
          onClick={() => setActiveTab("alerts")}
          className={`relative p-2 rounded-full border transition-colors ${
            activeTab === "alerts"
              ? "bg-blue-600/20 border-blue-500/40 text-blue-400"
              : "bg-finn-card border-finn-border text-finn-subtext hover:text-white"
          }`}
          aria-label="Alerts"
        >
          <Bell className="w-4 h-4" />
          {unreadAlertCount > 0 && (
            <span className="absolute -top-1 -right-1 w-4 h-4 bg-rose-500 text-white text-[10px] font-bold rounded-full flex items-center justify-center animate-bounce">
              {unreadAlertCount}
            </span>
          )}
        </button>
      </div>
    </header>
  );
}
