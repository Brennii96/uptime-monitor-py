from fastapi import FastAPI, status

from app.database import init_db
from app.schemas import MonitorCreate, MonitorResponse

app = FastAPI()
init_db()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/monitors", response_model=MonitorResponse, status_code=status.HTTP_201_CREATED)
async def create_monitor(monitor: MonitorCreate) -> MonitorResponse:
    monitor_dict = monitor.model_dump()
    monitor_dict.update({"id": 1})
    return monitor_dict


@app.get("/monitors/{monitor_id}")
def get_monitor(monitor_id: int):
    return {"id": monitor_id}
