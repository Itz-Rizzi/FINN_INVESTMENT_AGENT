from fastapi import APIRouter
from app.api.v1.endpoints import portfolio, digest, announcements, alerts, results, research, copilot

api_router = APIRouter()

@api_router.get("/health")
def api_health():
    return {"status": "healthy", "api_version": "v1"}

api_router.include_router(portfolio.router, prefix="/portfolio", tags=["Portfolio"])
api_router.include_router(digest.router, prefix="/digest", tags=["Daily Digest"])
api_router.include_router(announcements.router, prefix="/announcements", tags=["Announcements"])
api_router.include_router(alerts.router, prefix="/alerts", tags=["Triggered Alerts"])
api_router.include_router(results.router, prefix="/results", tags=["Quarterly Results"])
api_router.include_router(research.router, prefix="/research", tags=["Deep Research"])
api_router.include_router(copilot.router, prefix="/copilot", tags=["FINN Copilot"])
