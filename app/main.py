from fastapi import FastAPI
from .routers import ca
from contextlib import asynccontextmanager
from caproto.asyncio.client import Context


async def ca_context():
    return Context()


ctx = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    ctx["ca"] = await ca_context()
    yield
    ctx.clear()


app = FastAPI(
    lifespan=lifespan,
    title="EPICS PV API",
    description="An API for interacting with EPICS PVs",
    version="0.1.0",
)

app.include_router(ca.router)


@app.middleware("http")
async def add_ca_context(request, call_next):
    request.state.ca = ctx["ca"]
    response = await call_next(request)
    return response


@app.get("/")
def read_root():
    return {"Hello": "World"}
