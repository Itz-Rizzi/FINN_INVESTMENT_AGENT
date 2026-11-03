import sys
import json
import urllib.request

if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

tickers = ['RELIANCE', 'HAL', 'PIDILITIND']
base_url = 'http://127.0.0.1:8000/api/v1'

for sym in tickers:
    print(f"\n==========================================")
    print(f"TESTING DYNAMIC RESEARCH FOR: {sym}")
    print(f"==========================================")
    
    # 1. Snapshot
    snap_url = f"{base_url}/research/{sym}/snapshot"
    with urllib.request.urlopen(snap_url, timeout=30) as resp:
        snap = json.loads(resp.read().decode('utf-8'))
        print(f"Name: {snap.get('name')}")
        print(f"Sector: {snap.get('sector')}")
        print(f"Market Cap: {snap.get('market_cap')}")
        
        # 8 Dimensions check matching ResearchView
        bs = snap.get('business_snapshot', {})
        fs = snap.get('financial_snapshot', {})
        tr = snap.get('trajectory', {})
        bl = snap.get('balance_sheet', {})
        cq = snap.get('cash_quality', {})
        gd = snap.get('guidance', {})
        bb = snap.get('bull_vs_bear', {})
        cites = snap.get('citations', [])

        print("\n[8 DIMENSIONS VERIFICATION]:")
        print(f"1. Business Snapshot: Overview='{bs.get('overview', '')[:90]}...', Footprint='{bs.get('store_footprint')}'")
        print(f"   Revenue Mix: {bs.get('revenue_mix')}")
        print(f"2. Financial Snapshot: P/E={fs.get('pe_ratio')}, ROCE={fs.get('roce_pct')}%, ROE={fs.get('roe_pct')}%, Revenue=Rs {fs.get('current_revenue_cr')} Cr, EBITDA Margin={fs.get('ebitda_margin_pct')}%")
        print(f"3. Trajectory: Sales Trend={tr.get('multi_year_cagr_3yr_sales')}, PAT CAGR={tr.get('multi_year_cagr_3yr_pat')}")
        print(f"   Growing: '{tr.get('what_is_growing')}' | Compressing: '{tr.get('what_is_compressing')}'")
        print(f"4. Balance Sheet: Debt/Equity={bl.get('debt_to_equity')}, Net Debt=Rs {bl.get('net_debt_cr')} Cr, Working Capital={bl.get('working_capital_days')} days")
        print(f"   Structure: '{bl.get('funding_structure')}'")
        print(f"5. Cash Quality: CFO=Rs {cq.get('cfo_cr')} Cr, PAT=Rs {cq.get('pat_cr')} Cr, Conversion={cq.get('cash_conversion_pct')}%, FCF=Rs {cq.get('free_cash_flow_cr')} Cr")
        print(f"   Assessment: '{cq.get('assessment')}'")
        print(f"6. Guidance: Store Additions/Pipeline='{gd.get('store_additions')}', Margin Target='{gd.get('margin_target')}', Capex Plan='{gd.get('capex_plan')}'")
        print(f"7. Bull vs Bear:")
        print(f"   - Bull Case: '{bb.get('bull_case')}'")
        print(f"   - Bear Case: '{bb.get('bear_case')}'")
        print(f"8. Citations: {len(cites)} primary citations generated")
        for idx, c in enumerate(cites[:2]):
            print(f"   - Cite {idx+1}: [{c.get('doc_type')}] '{c.get('source_doc')}' (Page {c.get('page_number')})")
            print(f"     Quote: \"{c.get('quote_snippet', '')[:100]}...\"")

    # 2. Flagship Narrative vs Numbers
    nvn_url = f"{base_url}/research/{sym}/narrative-vs-numbers"
    with urllib.request.urlopen(nvn_url, timeout=30) as resp:
        nvn = json.loads(resp.read().decode('utf-8'))
        print(f"\n[FLAGSHIP NARRATIVE VS NUMBERS (4 QUARTERS)]:")
        print(f"Credibility Score: {nvn.get('credibility_score')}")
        print(f"Executive Summary: {nvn.get('executive_summary')[:130]}...")
        items = nvn.get('items', [])
        print(f"Total Quarters Cross-Examined: {len(items)}")
        for it in items:
            p_text = it.get('promised_guidance', '')[:60].replace('\u20b9', 'Rs.')
            d_text = it.get('actual_delivered', '')[:60].replace('\u20b9', 'Rs.')
            v_text = it.get('variance_analysis', '')[:60].replace('\u20b9', 'Rs.')
            print(f"  * [{it.get('quarter')}] Verdict: {it.get('verdict')}")
            print(f"    - Guidance: \"{p_text}...\" -> Cite: {it.get('guidance_citation', {}).get('source_doc')} p.{it.get('guidance_citation', {}).get('page_number')}")
            print(f"    - Delivered: \"{d_text}...\" -> Cite: {it.get('actual_citation', {}).get('source_doc')} p.{it.get('actual_citation', {}).get('page_number')}")
            print(f"    - Variance: \"{v_text}...\"")

print("\nALL DYNAMIC RESEARCH AND AI AUDIT CHECKS COMPLETED.")
