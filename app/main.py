from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.database import init_db
from app.exceptions.base import NotFoundError
from app.routers import monitor_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Uptime Monitor", lifespan=lifespan)


@app.exception_handler(NotFoundError)
async def not_found_exception_handler(request, exc: NotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})


app.include_router(router=monitor_router)

@app.get("/health")
def health():
    return {"status": "ok"}
