"use client";
import React, { useState } from "react";
import { Send, Sparkles, BookOpen, User, Bot, AlertCircle } from "lucide-react";
import { queryCopilot } from "../lib/api";
import { CitationItem } from "../lib/types";

interface CopilotDrawerProps {
  currentTicker: string;
  onOpenCitation: (cite: CitationItem) => void;
}

interface Message {
  role: "user" | "assistant";
  content: string;
  citations?: CitationItem[];
}

export default function CopilotDrawer({ currentTicker, onOpenCitation }: CopilotDrawerProps) {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content: `Hello! I am FINN, your investment research copilot. Ask me anything about **${currentTicker}** or any portfolio company. My analysis is strictly grounded in primary company filings (quarterly results, annual reports, earnings transcripts).`,
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [suggestedPrompts, setSuggestedPrompts] = useState<string[]>([
    `Show me Narrative vs Numbers for ${currentTicker}`,
    `What did management state on margin guidance?`,
    `How is ${currentTicker}'s cash flow conversion?`,
  ]);

  const handleSend = async (queryText: string) => {
    if (!queryText.trim() || loading) return;
    const userMsg = queryText.trim();
    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: userMsg }]);
    setLoading(true);

    try {
      const res = await queryCopilot(userMsg, currentTicker);
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: res.answer,
          citations: res.citations,
        },
      ]);
      if (res.suggested_followups && res.suggested_followups.length > 0) {
        setSuggestedPrompts(res.suggested_followups);
      }
    } catch (err: any) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: `Sorry, encountered an issue communicating with the intelligence service: ${err.message}`,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-140px)] max-w-2xl mx-auto">
      {/* Messages Scroll Area */}
      <div className="flex-1 overflow-y-auto space-y-3.5 pr-1">
        {messages.map((m, idx) => (
          <div
            key={idx}
            className={`flex gap-2.5 ${
              m.role === "user" ? "justify-end" : "justify-start"
            }`}
          >
            {m.role === "assistant" && (
              <div className="w-7 h-7 rounded-lg bg-blue-600/20 border border-blue-500/30 flex items-center justify-center text-blue-400 shrink-0">
                <Bot className="w-4 h-4" />
              </div>
            )}
            <div
              className={`max-w-[85%] rounded-2xl p-3 text-xs leading-relaxed ${
                m.role === "user"
                  ? "bg-blue-600 text-white rounded-br-none"
                  : "bg-finn-card border border-finn-border text-gray-200 rounded-bl-none shadow-md"
              }`}
            >
              <div className="whitespace-pre-line">{m.content}</div>

              {/* Citations Chips */}
              {m.citations && m.citations.length > 0 && (
                <div className="mt-2.5 pt-2 border-t border-finn-border/80 flex flex-wrap gap-1.5">
                  {m.citations.map((cite, i) => (
                    <button
                      key={i}
                      onClick={() => onOpenCitation(cite)}
                      className="inline-flex items-center gap-1 text-[10px] bg-emerald-500/15 text-emerald-300 border border-emerald-500/30 px-2 py-0.5 rounded-full hover:bg-emerald-500/25 transition-colors font-medium"
                    >
                      <BookOpen className="w-3 h-3 text-emerald-400" />
                      <span>{cite.source_doc} (p.{cite.page_number})</span>
                    </button>
                  ))}
                </div>
              )}
            </div>
            {m.role === "user" && (
              <div className="w-7 h-7 rounded-lg bg-gray-700 flex items-center justify-center text-gray-300 shrink-0">
                <User className="w-4 h-4" />
              </div>
            )}
          </div>
        ))}
        {loading && (
          <div className="flex items-center gap-2 text-xs text-finn-subtext pl-9">
            <Sparkles className="w-3.5 h-3.5 text-blue-400 animate-spin" />
            <span>FINN is analyzing primary filings...</span>
          </div>
        )}
      </div>

      {/* Suggested Followups */}
      {suggestedPrompts.length > 0 && (
        <div className="pt-2 pb-1.5 flex gap-1.5 overflow-x-auto no-scrollbar">
          {suggestedPrompts.map((p, i) => (
            <button
              key={i}
              onClick={() => handleSend(p)}
              className="whitespace-nowrap text-[11px] bg-finn-card hover:bg-finn-cardHover border border-finn-border text-blue-300 px-2.5 py-1 rounded-full transition-colors shrink-0"
            >
              {p}
            </button>
          ))}
        </div>
      )}

      {/* Input bar */}
      <form
        onSubmit={(e) => {
          e.preventDefault();
          handleSend(input);
        }}
        className="mt-2 flex items-center gap-2 bg-finn-card border border-finn-border rounded-xl p-1.5 shadow-lg"
      >
        <input
          type="text"
          placeholder={`Ask about ${currentTicker} guidance, margins, balance sheet...`}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          className="flex-1 bg-transparent px-3 py-1.5 text-xs text-white placeholder-finn-subtext focus:outline-none"
        />
        <button
          type="submit"
          disabled={!input.trim() || loading}
          className="p-2 bg-blue-600 hover:bg-blue-500 disabled:opacity-40 text-white rounded-lg transition-all"
        >
          <Send className="w-4 h-4" />
        </button>
      </form>
    </div>
  );
}
