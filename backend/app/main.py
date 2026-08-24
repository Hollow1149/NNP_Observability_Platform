from fastapi import FastAPI
from app.routers import health

app = FastAPI(
    title="NNP Observability Platform",
    version="1.0.0",
)

app.include_router(health.router)


@app.get("/")
def root():
    return {"message": "NNP Observability Platform API is running"}
