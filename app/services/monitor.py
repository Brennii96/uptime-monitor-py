from sqlalchemy.orm import Session

from app.models import Monitor
from app.schemas import MonitorCreate, MonitorUpdate


class MonitorService:
    def __init__(self, db: Session):
        self.db = db

    def get(self, monitor_id: int) -> type[Monitor] | None:
        return self.db.get(Monitor, monitor_id)

    def list(self, skip=0, limit=100) -> list[type[Monitor]]:
        return self.db.query(Monitor).offset(skip).limit(limit).all()

    def create(self, data: MonitorCreate) -> Monitor:
        monitor = Monitor(
            name=data.name,
            description=data.description,
            url=str(data.url),
        )
        self.db.add(monitor)
        self.db.commit()
        self.db.refresh(monitor)
        return monitor

    def update(self, monitor_id: int, data: MonitorUpdate) -> type[Monitor] | None:
        monitor = self.get(monitor_id)
        if monitor is None:
            return None

        monitor.name = data.name
        monitor.description = data.description
        monitor.url = str(data.url)

        self.db.commit()
        self.db.refresh(monitor)
        return monitor

    def delete(self, monitor_id: int) -> bool:
        monitor = self.get(monitor_id)
        if monitor is None:
            return False
        self.db.delete(monitor)
        self.db.commit()
        return True
