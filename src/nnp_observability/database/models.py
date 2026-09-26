from nnp_observability.database.session import Base


class TelementryMetric(Base):
    __tablename__: str = "telementry_metrics"


class LogEntry(Base):
    __tablename__: str = "log_entries"


class AnomalyEvent(Base):
    __tablename__: str = "anomaly_events"


class Incident(Base):
    __tablename__: str = "incidents"


class RcaResult(Base):
    __tablename__: str = "rca_results"


class RemediationAudit(Base):
    __tablename__: str = "remediation_audits"
