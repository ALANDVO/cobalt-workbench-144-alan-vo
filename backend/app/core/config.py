from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    APP_NAME: str = "Cobalt Workbench"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]
    
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./data/app.db"
    
    # Auth (Keycloak/OIDC) - configured via env
    OIDC_ISSUER_URL: str = ""
    OIDC_CLIENT_ID: str = ""
    OIDC_CLIENT_SECRET: str = ""
    
    # Demo mode - binds to localhost only, refuses in production
    DEMO_MODE: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()