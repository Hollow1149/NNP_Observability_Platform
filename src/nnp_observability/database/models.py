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


class TelementryMetric(Base):
    __tablename__: str = "telementry_metrics"
    id: Mapped[int] = mapped_column()
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )
    service_id: Mapped[str] = mapped_column(String(64))
    service_name: Mapped[str] = mapped_column(String(128))
    cpu_precent: Mapped[float] = mapped_column()
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
        Index("ix_metric_data", "id", "timestamp", "service_id"),
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
            "id",
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
    # TODO: Properly setup the relationship btw AnomalyEvent and Incident table
    incident_id: Mapped[None] = relationship(back_populates="")

    __table_args__: tuple[PrimaryKeyConstraint, ForeignKeyConstraint, Index] = (
        PrimaryKeyConstraint("id"),
        ForeignKeyConstraint(
            ["incident_id"],
            ["incidents.id"],
            ondelete="SET NULL",
            name="fk_anomalyEvent_2_Incident",
        ),
        Index(
            "ix_anomaly_data", "id", "detected_at", "service_id", "final_anomaly_score"
        ),
    )


class Incident(Base):
    __tablename__: str = "incidents"

    id: Mapped[str] = mapped_column(String(64))
    service_id: Mapped[str] = mapped_column(String(64))


class RcaResult(Base):
    __tablename__: str = "rca_results"


class RemediationAudit(Base):
    __tablename__: str = "remediation_audits"
