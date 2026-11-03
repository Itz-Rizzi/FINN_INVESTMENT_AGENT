"use client";
import React, { useState, useEffect } from "react";
import Header from "../components/Header";
import BottomNav from "../components/BottomNav";
import ExecutiveBioModal from "../components/ExecutiveBioModal";
import CitationModal from "../components/CitationModal";
import DigestView from "../components/DigestView";
import AlertsView from "../components/AlertsView";
import PortfolioView from "../components/PortfolioView";
import ResearchView from "../components/ResearchView";
import CopilotDrawer from "../components/CopilotDrawer";
import { 
  fetchPortfolio, 
  fetchDigest, 
  fetchAlertsFeed, 
  fetchAlertConfig, 
  updateAlertConfig, 
  markAlertRead, 
  triggerScanAlerts, 
  fetchQuarterlyResults, 
  fetchNarrativeVsNumbers, 
  fetchResearchDossier 
} from "../lib/api";
import { 
  Company, 
  DigestData, 
  AlertItem, 
  AlertConfig, 
  ResultsComparison, 
  NarrativeData, 
  ResearchDossier, 
  CitationItem 
} from "../lib/types";

export default function Home() {
  const [activeTab, setActiveTab] = useState<string>("digest");
  const [selectedTicker, setSelectedTicker] = useState<string>("TRENT.NS");

  // Digest state
  const [windowHours, setWindowHours] = useState<number>(24);
  const [digest, setDigest] = useState<DigestData | null>(null);
  const [loadingDigest, setLoadingDigest] = useState<boolean>(true);

  // Alerts state
  const [alerts, setAlerts] = useState<AlertItem[]>([]);
  const [alertConfig, setAlertConfig] = useState<AlertConfig | null>(null);
  const [priceThreshold, setPriceThreshold] = useState<number>(3.0);
  const [volumeThreshold, setVolumeThreshold] = useState<number>(2.0);
  const [savingConfig, setSavingConfig] = useState<boolean>(false);
  const [scanningAlerts, setScanningAlerts] = useState<boolean>(false);

  // Portfolio state
  const [portfolio, setPortfolio] = useState<Company[]>([]);
  const [loadingPortfolio, setLoadingPortfolio] = useState<boolean>(true);

  // Research state
  const [researchDossier, setResearchDossier] = useState<ResearchDossier | null>(null);
  const [narrativeData, setNarrativeData] = useState<NarrativeData | null>(null);
  const [resultsComparison, setResultsComparison] = useState<ResultsComparison | null>(null);
  const [loadingResearch, setLoadingResearch] = useState<boolean>(false);

  // Modals state
  const [activeBio, setActiveBio] = useState<any | null>(null);
  const [activeCitation, setActiveCitation] = useState<CitationItem | null>(null);

  useEffect(() => {
    if (typeof window !== 'undefined') {
      const params = new URLSearchParams(window.location.search);
      const tab = params.get('tab');
      if (tab) setActiveTab(tab);
      const ticker = params.get('ticker');
      if (ticker) {
        setSelectedTicker(ticker);
        loadResearch(ticker);
      } else {
        loadResearch(selectedTicker);
      }
    } else {
      loadResearch(selectedTicker);
    }
    loadDigest(24);
    loadAlerts();
    loadPortfolio();
  }, []);

  const loadDigest = async (hours: number) => {
    setLoadingDigest(true);
    setWindowHours(hours);
    try {
      const data = await fetchDigest(hours);
      setDigest(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoadingDigest(false);
    }
  };

  const loadAlerts = async () => {
    try {
      const feed = await fetchAlertsFeed();
      setAlerts(feed);
      const cfg = await fetchAlertConfig();
      setAlertConfig(cfg);
      setPriceThreshold(cfg.price_change_threshold_pct);
      setVolumeThreshold(cfg.volume_surge_multiplier);
    } catch (e) {
      console.error(e);
    }
  };

  const loadPortfolio = async () => {
    setLoadingPortfolio(true);
    try {
      const data = await fetchPortfolio();
      setPortfolio(data.companies);
    } catch (e) {
      console.error(e);
    } finally {
      setLoadingPortfolio(false);
    }
  };

  const loadResearch = async (ticker: string) => {
    setLoadingResearch(true);
    setSelectedTicker(ticker);
    try {
      const [dossier, narrative, results] = await Promise.all([
        fetchResearchDossier(ticker).catch(() => null),
        fetchNarrativeVsNumbers(ticker).catch(() => null),
        fetchQuarterlyResults(ticker).catch(() => null),
      ]);
      setResearchDossier(dossier);
      setNarrativeData(narrative);
      setResultsComparison(results);
    } catch (e) {
      console.error(e);
    } finally {
      setLoadingResearch(false);
    }
  };

  const handleSaveConfig = async () => {
    if (!alertConfig) return;
    setSavingConfig(true);
    try {
      const updated = await updateAlertConfig({
        ...alertConfig,
        price_change_threshold_pct: priceThreshold,
        volume_surge_multiplier: volumeThreshold,
      });
      setAlertConfig(updated);
    } catch (e) {
      console.error(e);
    } finally {
      setSavingConfig(false);
    }
  };

  const handleScanNow = async () => {
    setScanningAlerts(true);
    try {
      await triggerScanAlerts();
      await loadAlerts();
    } catch (e) {
      console.error(e);
    } finally {
      setScanningAlerts(false);
    }
  };

  const unreadAlertCount = alerts.filter((a) => !a.is_read).length;

  return (
    <div className="min-h-screen bg-finn-dark text-white selection:bg-blue-600">
      <Header
        onSearchTicker={(ticker) => {
          loadResearch(ticker);
          setActiveTab("research");
        }}
        unreadAlertCount={unreadAlertCount}
        activeTab={activeTab}
        setActiveTab={setActiveTab}
      />

      <div className="max-w-2xl mx-auto px-4 py-4">
        {activeTab === "digest" && (
          <DigestView
            digest={digest}
            loading={loadingDigest}
            windowHours={windowHours}
            onSelectWindow={(hours) => loadDigest(hours)}
            onOpenBio={(bio) => setActiveBio(bio)}
            onOpenResearch={(ticker) => {
              loadResearch(ticker);
              setActiveTab("research");
            }}
          />
        )}

        {activeTab === "alerts" && (
          <AlertsView
            alerts={alerts}
            alertConfig={alertConfig}
            priceThreshold={priceThreshold}
            setPriceThreshold={setPriceThreshold}
            volumeThreshold={volumeThreshold}
            setVolumeThreshold={setVolumeThreshold}
            savingConfig={savingConfig}
            onSaveConfig={handleSaveConfig}
            scanningAlerts={scanningAlerts}
            onScanNow={handleScanNow}
            onMarkRead={(id) => {
              markAlertRead(id);
              setAlerts((prev) => prev.map((a) => (a.id === id ? { ...a, is_read: true } : a)));
            }}
          />
        )}

        {activeTab === "portfolio" && (
          <PortfolioView
            portfolio={portfolio}
            loading={loadingPortfolio}
            onSelectTicker={(ticker) => {
              loadResearch(ticker);
              setActiveTab("research");
            }}
          />
        )}

        {activeTab === "research" && (
          <ResearchView
            selectedTicker={selectedTicker}
            researchDossier={researchDossier}
            narrativeData={narrativeData}
            resultsComparison={resultsComparison}
            loading={loadingResearch}
            onOpenCitation={(cite) => setActiveCitation(cite)}
          />
        )}

        {activeTab === "copilot" && (
          <div>
            <div className="mb-3">
              <h1 className="text-lg font-extrabold tracking-tight">Grounded Copilot</h1>
              <p className="text-xs text-finn-subtext">Conversational research anchored strictly in verified filings & transcripts.</p>
            </div>
            <CopilotDrawer
              currentTicker={selectedTicker}
              onOpenCitation={(cite) => setActiveCitation(cite)}
            />
          </div>
        )}
      </div>

      <ExecutiveBioModal bio={activeBio} onClose={() => setActiveBio(null)} />
      <CitationModal citation={activeCitation} onClose={() => setActiveCitation(null)} />

      <BottomNav
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        unreadAlertCount={unreadAlertCount}
      />
    </div>
  );
}
