from fastapi import FastAPI
from app.routers import kodekloudreport

app = FastAPI(title="KodeKloud License API")

app.include_router(kodekloudreport.router)


@app.get("/")
def read_root():
    return {"message": "Backend running"}

