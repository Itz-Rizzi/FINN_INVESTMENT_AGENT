# FINN: Launch script for both Backend and Frontend
$env:PATH = "C:\Program Files\nodejs;" + $env:PATH

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "   FINN: Financial Investment Agent (ENAM Build Challenge)" -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Start FastAPI Backend in background
Write-Host "[1/2] Starting FastAPI Backend on http://localhost:8000..." -ForegroundColor Green
$backendJob = Start-Job -ScriptBlock {
    Set-Location "C:\Users\yenni\.gemini\antigravity\scratch\finn\backend"
    python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
}

# 2. Start Next.js Frontend
Write-Host "[2/2] Starting Next.js Frontend on http://localhost:3000..." -ForegroundColor Green
Set-Location "C:\Users\yenni\.gemini\antigravity\scratch\finn\frontend"
& "C:\Program Files\nodejs\npm.cmd" run dev
