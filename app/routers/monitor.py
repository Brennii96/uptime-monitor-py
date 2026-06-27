from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_monitor_service
from app.schemas import MonitorRead, MonitorCreate
from app.services.monitor import MonitorService

router = APIRouter(prefix="/monitors", tags=["monitors"])


@router.get("/", response_model=list[MonitorRead])
def list_monitors(service: MonitorService = Depends(get_monitor_service)):
    return service.list()


@router.get("/{monitor_id}", response_model=MonitorRead)
def get_monitor(monitor_id: int, service: MonitorService = Depends(get_monitor_service)):
    monitor = service.get(monitor_id)
    if monitor is None:
        raise HTTPException(status_code=404, detail="Monitor not found")
    return monitor


@router.post("/", response_model=MonitorRead, status_code=201)
def create_monitor(data: MonitorCreate, service: MonitorService = Depends(get_monitor_service)):
    return service.create(data)


@router.delete("/{monitor_id}", status_code=204)
def delete_monitor(monitor_id: int, service: MonitorService = Depends(get_monitor_service)):
    deleted = service.delete(monitor_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Monitor not found")
    return None

