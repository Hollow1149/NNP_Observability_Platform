from datetime import datetime

from pydantic import BaseModel, Field


# Local AI Explanation Schemas
class EvidenceChainItem(BaseModel):
    source: str = Field(min_length=1)
    telemetry_fact: str = Field(min_length=1)
    correlation: str = Field(min_length=1)


class AiDiagnosisReportResponse(BaseModel):
    incident_id: str = Field(min_length=1)
    executive_summary: str = Field(min_length=1)
    probable_root_cause: str = Field(min_length=1)
    evidence_chain: list[EvidenceChainItem] = Field(min_length=1)
    dependency_impact_description: str = Field(min_length=1)
    confidence_score: float
    confidence_justification: str = Field(min_length=1)
    limitations: list[str] = Field(min_length=1)
    generated_at: datetime
    model_used: str = Field(min_length=1)
