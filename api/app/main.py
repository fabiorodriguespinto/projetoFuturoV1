##api/app/main.py

from fastapi import FastAPI
from app.routers.predict import router as predict_router

app = FastAPI(
    title="Projeto FuturoV1 API",
    version="1.0.0"
)

app.include_router(predict_router)

@app.get("/health")
def healthcheck():
    return {"status": "ok"}

