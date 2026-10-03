from datetime import UTC, datetime

from sqlalchemy import (
    JSON,
    DateTime,
    ForeignKeyConstraint,
    Index,
    PrimaryKeyConstraint,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from nnp_observability.database.session import Base

type JSONValue = (
    str | int | float | bool | None | list["JSONValue"] | dict[str, "JSONValue"]
)


class TelemetryMetric(Base):
    __tablename__: str = "telemetry_metrics"
    id: Mapped[int] = mapped_column()
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )
    service_id: Mapped[str] = mapped_column(String(64))
    service_name: Mapped[str] = mapped_column(String(128))
    cpu_percent: Mapped[float] = mapped_column()
    memory_mb: Mapped[float] = mapped_column()
    request_rate: Mapped[float] = mapped_column(default=0.0)
    latency_p95_ms: Mapped[float] = mapped_column()
    error_rate_percent: Mapped[float] = mapped_column(default=0.0)
    db_query_latency_ms: Mapped[float] = mapped_column(default=0.0)
    db_connections: Mapped[int] = mapped_column(default=0)
    queue_backlog: Mapped[int] = mapped_column(default=0)
    source: Mapped[str] = mapped_column(String(32), default="collector")

    __table_args__: tuple[PrimaryKeyConstraint, Index] = (
        PrimaryKeyConstraint("id"),
        Index("ix_metric_data", "timestamp", "service_id"),
    )


class LogEntry(Base):
    __tablename__: str = "log_entries"

    id: Mapped[str] = mapped_column(String(64))
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )
    service_id: Mapped[str] = mapped_column(String(64))
    service_name: Mapped[str] = mapped_column(String(128))
    level: Mapped[str] = mapped_column(String(16))  # DEBUG, INFO, WARN, ERROR, FATAL
    message: Mapped[str] = mapped_column(Text)
    request_id: Mapped[str | None] = mapped_column(String(64))
    trace_id: Mapped[str | None] = mapped_column(String(64))
    endpoint: Mapped[str | None] = mapped_column(String(256))
    exception_type: Mapped[str | None] = mapped_column(String(128))
    duration_ms: Mapped[float | None] = mapped_column()
    status_code: Mapped[int | None] = mapped_column()
    extra_metadata: Mapped[dict[str, JSONValue] | None] = mapped_column(
        JSON, default=dict
    )

    __table_args__: tuple[PrimaryKeyConstraint, Index] = (
        PrimaryKeyConstraint("id"),
        Index(
            "ix_log_data",
            "timestamp",
            "service_id",
            "level",
            "request_id",
            "trace_id",
        ),
    )


class AnomalyEvent(Base):
    __tablename__: str = "anomaly_events"

    id: Mapped[str] = mapped_column(String(64))
    detected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )
    service_id: Mapped[str] = mapped_column(String(64))
    service_name: Mapped[str] = mapped_column(String(128))
    metric_name: Mapped[str] = mapped_column(String(64))
    isolation_forest_score: Mapped[float] = mapped_column()
    autoencoder_recon_error: Mapped[float] = mapped_column()
    context_score: Mapped[float] = mapped_column()
    final_anomaly_score: Mapped[float] = mapped_column()
    threshold: Mapped[float] = mapped_column(default=0.60)
    severity: Mapped[str] = mapped_column(String(32))
    details: Mapped[str | None] = mapped_column(Text)
    incident_id: Mapped[str | None] = mapped_column(String(64))
    incident: Mapped["Incident | None"] = relationship(back_populates="anomalies")

    __table_args__: tuple[PrimaryKeyConstraint, ForeignKeyConstraint, Index] = (
        PrimaryKeyConstraint("id"),
        ForeignKeyConstraint(
            ["incident_id"],
            ["incidents.id"],
            ondelete="SET NULL",
            name="fk_anomalyEvent_Incident",
        ),
        Index("ix_anomaly_data", "detected_at", "service_id", "final_anomaly_score"),
    )


class Incident(Base):
    __tablename__: str = "incidents"

    id: Mapped[str] = mapped_column(String(64))
    service_id: Mapped[str] = mapped_column(String(64))
    service_name: Mapped[str] = mapped_column(String(128))
    title: Mapped[str] = mapped_column(String(256))
    incident_type: Mapped[str] = mapped_column(String(128))
    start_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )
    end_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    severity: Mapped[str] = mapped_column(
        String(32), default="high"
    )  # low, medium, high, critical
    status: Mapped[str] = mapped_column(
        String(32), default="active"
    )  # active, investigating, mitigating, resolved
    current_stage: Mapped[str] = mapped_column(String(64), default="anomaly_detected")
    summary: Mapped[str | None] = mapped_column(Text)
    confidence_score: Mapped[float] = mapped_column(default=90.0)
    affected_services: Mapped[list[dict[str, JSONValue]]] = mapped_column(
        JSON, default=dict
    )
    anomalies_detected: Mapped[int] = mapped_column(default=0)
    primary_metric_impacted: Mapped[str | None] = mapped_column(String(64))
    mttd_seconds: Mapped[float] = mapped_column(default=0.0)
    mttr_seconds: Mapped[float | None] = mapped_column()
    root_cause_service: Mapped[str | None] = mapped_column(String(128))
    remediation_action_taken: Mapped[str | None] = mapped_column(String(256))
    lifecycle_timeline: Mapped[list[dict[str, JSONValue]]] = mapped_column(
        JSON, default=dict
    )
    operator_comments: Mapped[list[dict[str, JSONValue]]] = mapped_column(
        JSON, default=dict
    )

    anomalies: Mapped[list["AnomalyEvent"]] = relationship(back_populates="incident")
    rca_results: Mapped[list["RcaResult"]] = relationship(
        back_populates="incident", cascade="all, delete-orphan"
    )
    remediation_audits: Mapped[list["RemediationAudit"]] = relationship(
        back_populates="incident", cascade="all, delete-orphan"
    )

    __table_args__: tuple[PrimaryKeyConstraint, Index] = (
        PrimaryKeyConstraint("id"),
        Index("ix_incident_data", "start_time", "status"),
    )


class RcaResult(Base):
    __tablename__: str = "rca_results"

    id: Mapped[str] = mapped_column(String(64))
    incident_id: Mapped[str] = mapped_column(String(64))
    incident: Mapped["Incident"] = relationship(back_populates="rca_results")
    candidate_service_id: Mapped[str] = mapped_column(String(64))
    candidate_service_name: Mapped[str] = mapped_column(String(128))
    candidate_type: Mapped[str] = mapped_column(String(64), default="microservice")
    rank: Mapped[int] = mapped_column()
    score: Mapped[float] = mapped_column()
    metric_evidence_score: Mapped[float] = mapped_column(default=0.0)
    dependency_impact_score: Mapped[float] = mapped_column(default=0.0)
    temporal_precedence_score: Mapped[float] = mapped_column(default=0.0)
    log_evidence_score: Mapped[float] = mapped_column(default=0.0)
    fault_signature_score: Mapped[float] = mapped_column(default=0.0)
    evidence_summary: Mapped[str] = mapped_column(Text)
    evidence_items: Mapped[list[dict[str, JSONValue]]] = mapped_column(
        JSON, default=dict
    )
    fault_signature_matched: Mapped[str | None] = mapped_column(String(256))
    lead_lag_relationship: Mapped[str] = mapped_column(String(128))
    confidence: Mapped[float] = mapped_column(default=90.0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )

    __table_args__: tuple[PrimaryKeyConstraint, ForeignKeyConstraint] = (
        PrimaryKeyConstraint("id"),
        ForeignKeyConstraint(
            ["incident_id"],
            ["incidents.id"],
            name="fk_rcaResult_incident",
        ),
    )


class RemediationAudit(Base):
    __tablename__: str = "remediation_audits"

    id: Mapped[str] = mapped_column(String(64))
    incident_id: Mapped[str] = mapped_column(String(64))
    incident: Mapped["Incident"] = relationship(back_populates="remediation_audits")
    recommendation_id: Mapped[str] = mapped_column(String(64))
    playbook_id: Mapped[str] = mapped_column(String(64))
    action_title: Mapped[str] = mapped_column(String(256))
    target_service: Mapped[str] = mapped_column(String(128))
    action_type: Mapped[str] = mapped_column(String(64))
    approver: Mapped[str] = mapped_column(String(128), default="SRE On-Call Operator")
    status: Mapped[str] = mapped_column(String(32), default="pending")
    decision_comment: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )
    executed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    verification_status: Mapped[str] = mapped_column(String(64), default="unresolved")
    execution_logs: Mapped[dict[str, JSONValue]] = mapped_column(JSON, default=dict)

    __table_args__: tuple[PrimaryKeyConstraint, ForeignKeyConstraint, Index] = (
        PrimaryKeyConstraint("id"),
        ForeignKeyConstraint(
            ["incident_id"],
            ["incidents.id"],
            name="fk_remediationAudit_incident",
        ),
        Index("ix_remediationAudit_data", "incident_id"),
    )
