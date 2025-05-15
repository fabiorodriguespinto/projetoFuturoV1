
from fastapi import FastAPI
from app.routers import predict, healthcheck

app = FastAPI()

app.include_router(predict.router)
app.include_router(healthcheck.router)

@app.get("/")
def root():
    return {"message": "API OK"}