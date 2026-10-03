from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

type JSONValue = (
    str | int | float | bool | None | list["JSONValue"] | dict[str, "JSONValue"]
)


# Log Schemas
class LogEntryCreate(BaseModel):
    id: str | None = None
    timestamp: datetime | None = None
    service_id: str = Field(min_length=1, max_length=64)
    service_name: str = Field(min_length=1, max_length=128)
    level: str = Field(pattern="^(DEBUG|INFO|WARN|ERROR|FATAL)$")
    message: str = Field(min_length=1)
    request_id: str | None = None
    trace_id: str | None = None
    endpoint: str | None = None
    exception_type: str | None = None
    duration_ms: float | None = Field(default=None, ge=0)
    status_code: int | None = Field(default=None, ge=100, le=599)
    extra_metadata: dict[str, JSONValue] | None = None


class LogEntryResponse(LogEntryCreate):
    model_config = ConfigDict(from_attributes=True)  # pyright: ignore[reportUnannotatedClassAttribute]


class IngestLogBatchRequest(BaseModel):
    logs: list[LogEntryCreate]
