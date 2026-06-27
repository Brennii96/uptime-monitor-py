from fastapi import APIRouter, Depends

from app.dependencies import get_monitor_service
from app.schemas import MonitorRead, MonitorCreate, MonitorUpdate
from app.services.monitor import MonitorService

router = APIRouter(prefix="/monitors", tags=["monitors"])


@router.get("/", response_model=list[MonitorRead])
def list_monitors(service: MonitorService = Depends(get_monitor_service)):
    return service.list()


@router.get("/{monitor_id}", response_model=MonitorRead)
def get_monitor(monitor_id: int, service: MonitorService = Depends(get_monitor_service)):
    return service.get(monitor_id)


@router.post("/", response_model=MonitorRead, status_code=201)
def create_monitor(data: MonitorCreate, service: MonitorService = Depends(get_monitor_service)):
    return service.create(data)


@router.put("/{monitor_id}", response_model=MonitorRead)
def update_monitor(
    monitor_id: int,
    data: MonitorUpdate,
    service: MonitorService = Depends(get_monitor_service),
):
    return service.update(monitor_id, data)


@router.delete("/{monitor_id}", status_code=204)
def delete_monitor(monitor_id: int, service: MonitorService = Depends(get_monitor_service)):
    service.delete(monitor_id)
