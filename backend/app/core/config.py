import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="allow")
    
    PROJECT_NAME: str = "FINN - Financial Investment Agent"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Storage & Database
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    SQLITE_DB_PATH: str = str(BASE_DIR / "app" / "data" / "finn.db")
    
    # Gemini LLM API
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", os.getenv("GOOGLE_API_KEY", ""))
    GEMINI_FLASH_MODEL: str = "gemini-2.5-flash"
    GEMINI_PRO_MODEL: str = "gemini-1.5-pro"
    
    # Paths
    DOCUMENTS_DIR: Path = BASE_DIR / "app" / "data" / "documents"
    FAISS_INDEX_DIR: Path = BASE_DIR / "app" / "data" / "faiss_index"
    
    # Default Alert Thresholds
    DEFAULT_PRICE_CHANGE_THRESHOLD_PCT: float = 3.0
    DEFAULT_VOLUME_SURGE_MULTIPLIER: float = 2.0

settings = Settings()
settings.DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)
settings.FAISS_INDEX_DIR.mkdir(parents=True, exist_ok=True)
