from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


# Telemetry Metric Schemas
class TelemetryMetricBase(BaseModel):
    service_id: str = Field(min_length=1)
    service_name: str = Field(min_length=1)
    cpu_percent: float = Field(ge=0.0, le=100)
    memory_mb: float = Field(ge=0.0)
    request_rate: float = Field(default=0.0, ge=0.0)
    latency_p95_ms: float = Field(ge=0.0)
    error_rate_percent: float = Field(default=0.0, ge=0.0, le=100)
    db_query_latency_ms: float = Field(default=0.0, ge=0.0)
    db_connections: int = Field(default=0, ge=0)
    queue_backlog: int = Field(default=0, ge=0)
    source: str | None = "collector"


class TelemetryMetricCreate(TelemetryMetricBase):
    timestamp: datetime | None = None


class TelemetryMetricResponse(TelemetryMetricBase):
    id: int
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)  # pyright: ignore[reportUnannotatedClassAttribute]


class IngestMetricsBatchRequest(BaseModel):
    metrics: list[TelemetryMetricCreate] = Field(min_length=1)
