from fastapi import FastAPI
from app.routers import report

app = FastAPI(title="KodeKloud License API")

app.include_router(report.router)


@app.get("/")
def read_root():
    return {"message": "Backend running"}

