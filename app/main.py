from fastapi import FastAPI
from .routers import ca

app = FastAPI(
    title="EPICS PV API",
    root_path="/api",
    description="An API for interacting with EPICS PVs",
    version="0.1.0",
)

app.include_router(ca.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
