from fastapi import FastAPI
from app.routers import kodekloud_report

app = FastAPI(title="KodeKloud License API")

app.include_router(kodekloud_report.router)


@app.get("/")
def read_root():
    return {"message": "Backend running"}

