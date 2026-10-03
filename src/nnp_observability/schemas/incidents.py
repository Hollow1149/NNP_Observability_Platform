from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

type JSONValue = (
    str | int | float | bool | None | list["JSONValue"] | dict[str, "JSONValue"]
)


# Incident Schemas
class IncidentResponse(BaseModel):
    id: str = Field(min_length=1)
    service_id: str = Field(min_length=1)
    service_name: str = Field(min_length=1)
    title: str = Field(min_length=1)
    incident_type: str = Field(min_length=1)
    start_time: datetime
    end_time: datetime | None = None
    severity: str = Field(min_length=1)
    status: str = Field(min_length=1)
    current_stage: str = Field(min_length=1)
    summary: str | None = None
    confidence_score: float
    affected_services: list[str] = Field(default_factory=list)
    anomalies_detected: int = 0
    primary_metric_impacted: str | None = None
    mttd_seconds: float
    mttr_seconds: float | None = None
    root_cause_service: str | None = None
    remediation_action_taken: str | None = None
    lifecycle_timeline: list[dict[str, JSONValue]] = Field(default_factory=list)
    operator_comments: list[dict[str, JSONValue]] = Field(default_factory=list)
    model_config = ConfigDict(from_attributes=True)  # pyright: ignore[reportUnannotatedClassAttribute]
