from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg
from psycopg.rows import dict_row

app = FastAPI()

# Database configuration
DB_URL = "postgresql://postgres:mlue@localhost:5432/observability_db"


def get_db_conn():
    return psycopg.connect(DB_URL, row_factory=dict_row)


class LogEntry(BaseModel):
    level: str
    source: str
    message: str
    data: Optional[Dict[str, Any]] = None


class MetricEntry(BaseModel):
    name: str
    value: float
    tags: Optional[Dict[str, Any]] = None


@app.post("/logs")
async def create_log(log: LogEntry):
    try:
        with get_db_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO logs (level, source, message, data) VALUES (%s, %s, %s, %s) RETURNING id",
                    (
                        log.level,
                        log.source,
                        log.message,
                        psycopg.types.json.Jsonb(log.data) if log.data else None,
                    ),
                )
                log_id = cur.fetchone()["id"]
                conn.commit()
                return {"status": "success", "id": log_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/metrics")
async def create_metric(metric: MetricEntry):
    try:
        with get_db_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO metrics (name, value, tags) VALUES (%s, %s, %s) RETURNING id",
                    (
                        metric.name,
                        metric.value,
                        psycopg.types.json.Jsonb(metric.tags) if metric.tags else None,
                    ),
                )
                metric_id = cur.fetchone()["id"]
                conn.commit()
                return {"status": "success", "id": metric_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
