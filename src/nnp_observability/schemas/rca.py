from pydantic import BaseModel, Field

type JSONValue = (
    str | int | float | bool | None | list["JSONValue"] | dict[str, "JSONValue"]
)


# RCA Schema
class RcaScoreBreakdown(BaseModel):
    metric_evidence: float
    dependency_impact: float
    temporal_precedence: float
    log_evidence: float
    fault_signature: float


class EvidenceItem(BaseModel):
    type: str = Field(min_length=1)  # metric | log | topology | timing
    description: str = Field(min_length=1)
    severity: str = Field(min_length=1)  # info | warn | error
    value: str | None = None


class RcaCandidateResponse(BaseModel):
    id: str = Field(min_length=1)
    incident_id: str = Field(min_length=1)
    candidate_service_id: str = Field(min_length=1)
    candidate_service_name: str = Field(min_length=1)
    candidate_type: str = Field(min_length=1)
    rank: int
    score: float
    score_breakdown: RcaScoreBreakdown
    evidence_item: list[dict[str, JSONValue]] = Field(default_factory=list)
    evidence_summary: str = Field(min_length=1)
    fault_signature_matched: str | None = None
    lead_lag_relationship: str = Field(min_length=1)
    confidence: float


class DiagnoseIncidentRequest(BaseModel):
    incident_id: str | None = None
    service_id: str | None = None
    lookback_seconds: int = Field(default=300, ge=30, le=3600)
