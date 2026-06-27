from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import init_db
from app.routers import monitor_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Uptime Monitor", lifespan=lifespan)

app.include_router(router=monitor_router)

@app.get("/health")
def health():
    return {"status": "ok"}
