from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


# Anomaly Schema
class AnomalyEventResponse(BaseModel):
    id: str = Field(min_length=1)
    detected_at: datetime
    service_id: str = Field(min_length=1)
    service_name: str = Field(min_length=1)
    metric_name: str = Field(min_length=1)
    isolation_forest_score: float
    autoencoder_recon_error: float
    context_score: float
    final_anomaly_score: float
    threshold: float
    severity: str = Field(min_length=1)
    details: str | None = None
    incident_id: str | None = None
    model_config = ConfigDict(from_attributes=True)  # pyright: ignore[reportUnannotatedClassAttribute]


class AnomalyThresholdUpdate(BaseModel):
    threshold: float = Field(ge=0.1, le=0.99)
    if_weight: float = Field(default=0.45, ge=0.0, le=1.0)
    ae_weight: float = Field(default=0.35, ge=0.0, le=1.0)
    context_weight: float = Field(default=0.20, ge=0.0, le=1.0)
