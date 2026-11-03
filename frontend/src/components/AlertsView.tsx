"use client";
import React from "react";
import { AlertItem, AlertConfig } from "../lib/types";
import { Sliders, RefreshCw } from "lucide-react";

interface AlertsViewProps {
  alerts: AlertItem[];
  alertConfig: AlertConfig | null;
  priceThreshold: number;
  setPriceThreshold: (val: number) => void;
  volumeThreshold: number;
  setVolumeThreshold: (val: number) => void;
  savingConfig: boolean;
  onSaveConfig: () => void;
  scanningAlerts: boolean;
  onScanNow: () => void;
  onMarkRead: (id: string) => void;
}

export default function AlertsView({
  alerts,
  alertConfig,
  priceThreshold,
  setPriceThreshold,
  volumeThreshold,
  setVolumeThreshold,
  savingConfig,
  onSaveConfig,
  scanningAlerts,
  onScanNow,
  onMarkRead,
}: AlertsViewProps) {
  return (
    <div className="space-y-5">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-lg font-extrabold tracking-tight">Triggered Alerts</h1>
          <p className="text-xs text-finn-subtext">Real-time alerts triggered when price, volume, or filings cross thresholds.</p>
        </div>
        <button
          onClick={onScanNow}
          disabled={scanningAlerts}
          className="flex items-center gap-1.5 bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-white text-xs font-bold px-3 py-1.5 rounded-lg transition-all shadow"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${scanningAlerts ? "animate-spin" : ""}`} />
          <span>Scan Now</span>
        </button>
      </div>

      {/* Threshold Configuration Drawer */}
      <div className="bg-finn-card border border-finn-border rounded-xl p-4 shadow-md">
        <div className="flex items-center gap-1.5 font-bold text-xs uppercase tracking-wider text-blue-400 mb-3">
          <Sliders className="w-4 h-4" />
          <span>Configurable Alert Watchdogs</span>
        </div>

        <div className="space-y-4">
          {/* Price swing slider */}
          <div>
            <div className="flex justify-between text-xs mb-1">
              <span className="text-gray-300 font-medium">Daily Price Move Threshold</span>
              <span className="font-bold text-white font-mono">±{priceThreshold}%</span>
            </div>
            <input
              type="range"
              min="1.0"
              max="8.0"
              step="0.5"
              value={priceThreshold}
              onChange={(e) => setPriceThreshold(parseFloat(e.target.value))}
              className="w-full accent-blue-500 cursor-pointer"
            />
            <div className="flex justify-between text-[10px] text-finn-subtext mt-0.5">
              <span>±1.0% (Sensitive)</span>
              <span>±3.0% (Standard)</span>
              <span>±8.0% (High Conviction)</span>
            </div>
          </div>

          {/* Volume surge slider */}
          <div>
            <div className="flex justify-between text-xs mb-1">
              <span className="text-gray-300 font-medium">Unusual Volume Multiplier</span>
              <span className="font-bold text-white font-mono">{volumeThreshold}× 20-Day SMA</span>
            </div>
            <input
              type="range"
              min="1.5"
              max="4.0"
              step="0.25"
              value={volumeThreshold}
              onChange={(e) => setVolumeThreshold(parseFloat(e.target.value))}
              className="w-full accent-blue-500 cursor-pointer"
            />
            <div className="flex justify-between text-[10px] text-finn-subtext mt-0.5">
              <span>1.5×</span>
              <span>2.0× (Standard)</span>
              <span>4.0× (Extreme Spikes)</span>
            </div>
          </div>

          <div className="pt-2 flex justify-end">
            <button
              onClick={onSaveConfig}
              disabled={savingConfig}
              className="text-xs bg-blue-600/20 hover:bg-blue-600/30 text-blue-400 border border-blue-500/40 px-3 py-1.5 rounded-lg font-bold transition-colors"
            >
              {savingConfig ? "Saving..." : "Save Preferences"}
            </button>
          </div>
        </div>
      </div>

      {/* Alerts Feed */}
      <div className="space-y-2.5">
        <h2 className="text-xs font-bold uppercase tracking-wider text-finn-subtext">Recent Triggers</h2>
        {alerts.length === 0 ? (
          <div className="bg-finn-card border border-finn-border rounded-xl p-8 text-center text-xs text-finn-subtext">
            No alerts triggered. Market volume and price moves are within normal bands.
          </div>
        ) : (
          alerts.map((al) => (
            <div
              key={al.id}
              onClick={() => onMarkRead(al.id)}
              className={`p-3.5 rounded-xl border transition-all cursor-pointer ${
                al.is_read
                  ? "bg-finn-dark/50 border-finn-border/60 opacity-75"
                  : "bg-finn-card border-blue-500/40 shadow-md"
              }`}
            >
              <div className="flex items-start justify-between gap-2 mb-1.5">
                <div className="flex items-center gap-2">
                  <span className={`text-[10px] font-bold px-2 py-0.5 rounded uppercase ${
                    al.severity === "CRITICAL"
                      ? "bg-rose-500/20 text-rose-400 border border-rose-500/30"
                      : al.severity === "WARNING"
                      ? "bg-amber-500/20 text-amber-400 border border-amber-500/30"
                      : "bg-blue-500/20 text-blue-400 border border-blue-500/30"
                  }`}>
                    {al.severity}
                  </span>
                  <span className="font-extrabold text-xs text-white">{al.ticker}</span>
                  <span className="text-xs text-finn-subtext font-medium">{al.company_name}</span>
                </div>
                <span className="text-[10px] text-finn-subtext font-mono">
                  {new Date(al.triggered_at).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
                </span>
              </div>

              <h4 className="font-bold text-xs text-gray-100">{al.headline}</h4>
              <p className="text-[11px] text-gray-300 mt-1 leading-snug">{al.details}</p>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
