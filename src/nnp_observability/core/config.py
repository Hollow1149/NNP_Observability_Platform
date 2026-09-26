from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application Metadata
    PROJECT_NAME: str = "Real Time Log-Based Anomaly Detection For Microservices"
    VERSION: str = "1.5.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = False

    # Server Bindings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    API_V1_PREFIX: str = "/api/v1"

    # Database (PostgreSQL)
    DATABASE_URL: str = Field(
        default="", description="PostgreSQL connection string with pooling credentials"
    )

    # CORS Security
    # Supports JSON list or comma-seperated string from .env
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",  # Default Vite dev port
        "http://127.0.0.1:5173",
    ]

    # ML Anomaly Detection bounds and weights
    DEFAULT_ANOMALY_THRESHOLD: float = Field(default=0.60, ge=0.1, le=0.99)
    IF_WEIGHT: float = Field(default=0.45, ge=0.0, le=1.0)
    AL_WEIGHT: float = Field(default=0.35, ge=0.0, le=1.0)
    CONTEXT_WEIGHT: float = Field(default=0.20, ge=0.0, le=1.0)

    # External Monitoring Targets
    PROMETHEUS_URL: str = "http://localhost:9090"
    NODE_EXPORTER_URL: str = "http://localhost:9100/metrics"

    # Pydantic v2 Settings Configuration
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True, extra="ignore"
    )


settings = Settings()
