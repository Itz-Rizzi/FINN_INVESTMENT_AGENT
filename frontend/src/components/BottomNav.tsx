"use client";
import React from "react";
import { Newspaper, Bell, PieChart, SearchCode, MessageSquareText } from "lucide-react";

interface BottomNavProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  unreadAlertCount: number;
}

export default function BottomNav({ activeTab, setActiveTab, unreadAlertCount }: BottomNavProps) {
  const navItems = [
    { id: "digest", label: "Digest", icon: Newspaper },
    { id: "alerts", label: "Alerts", icon: Bell, badge: unreadAlertCount },
    { id: "portfolio", label: "Portfolio", icon: PieChart },
    { id: "research", label: "Research", icon: SearchCode },
    { id: "copilot", label: "Copilot", icon: MessageSquareText },
  ];

  return (
    <nav className="fixed bottom-0 left-0 right-0 z-40 bg-finn-dark/95 backdrop-blur-md border-t border-finn-border py-1.5 px-3">
      <div className="max-w-2xl mx-auto flex items-center justify-around">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`flex flex-col items-center justify-center py-1 px-3 rounded-xl transition-all relative ${
                isActive ? "text-blue-400 scale-105" : "text-finn-subtext hover:text-gray-300"
              }`}
            >
              <div className="relative">
                <Icon className={`w-5 h-5 ${isActive ? "stroke-[2.5]" : "stroke-[1.8]"}`} />
                {item.badge && item.badge > 0 ? (
                  <span className="absolute -top-1 -right-2 w-3.5 h-3.5 bg-rose-500 rounded-full text-[9px] text-white font-bold flex items-center justify-center">
                    {item.badge}
                  </span>
                ) : null}
              </div>
              <span className={`text-[10px] mt-1 font-medium ${isActive ? "font-bold text-white" : ""}`}>
                {item.label}
              </span>
              {isActive && (
                <span className="w-1 h-1 rounded-full bg-blue-500 absolute bottom-0.5"></span>
              )}
            </button>
          );
        })}
      </div>
    </nav>
  );
}
