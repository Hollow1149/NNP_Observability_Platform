from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

type JSONValue = (
    str | int | float | bool | None | list["JSONValue"] | dict[str, "JSONValue"]
)


# Remediation Schema
class RemediationPlaybookResponse(BaseModel):
    id: str = Field(min_length=1)
    failure_type: str = Field(min_length=1)
    root_cause_type: str = Field(min_length=1)
    title: str = Field(min_length=1)
    recommendation_text: str = Field(min_length=1)
    action_type: str = Field(min_length=1)
    category: str = Field(min_length=1)
    safe_auto_action: bool
    approval_required: bool
    priority: str = Field(min_length=1)
    estimated_recovery_time_sec: int
    steps: list[str] = Field(min_length=1)


class RemediationApprovalRequest(BaseModel):
    incident_id: str = Field(min_length=1)
    recommendation_id: str = Field(min_length=1)
    playbook_id: str = Field(min_length=1)
    action_title: str = Field(min_length=1)
    target_service: str = Field(min_length=1)
    action_type: str = Field(min_length=1)
    approver: str | None = "SRE On-Call Operator"
    decision_comment: str | None = "Approved after telemetry validation"


class RemediationRejectRequest(BaseModel):
    incident_id: str = Field(min_length=1)
    recommendation_id: str = Field(min_length=1)
    reason: str = Field(min_length=1)
    approver: str | None = "SRE On-Call Operator"


class RemediationAuditResponse(BaseModel):
    id: str = Field(min_length=1)
    incident_id: str = Field(min_length=1)
    recommendation_id: str = Field(min_length=1)
    playbook_id: str = Field(min_length=1)
    action_title: str = Field(min_length=1)
    target_service: str = Field(min_length=1)
    action_type: str = Field(min_length=1)
    approver: str = Field(min_length=1)
    decision_comment: str | None = None
    created_at: datetime
    executed_at: datetime | None = None
    verification_status: str = Field(min_length=1)
    execution_logs: dict[str, JSONValue] = {}
    model_config = ConfigDict(from_attributes=True)  # pyright: ignore[reportUnannotatedClassAttribute]


class FaultInjectionRequest(BaseModel):
    scenario: str = Field(min_length=1)
    intensity: float | None = 1.0
    duration_seconds: int | None = 120
