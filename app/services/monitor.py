from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions.monitor import MonitorNotFoundError, MonitorAlreadyExistsError
from app.models import Monitor
from app.schemas import MonitorCreate, MonitorUpdate


class MonitorService:
    def __init__(self, db: Session):
        self.db = db

    def get_or_fail(self, monitor_id: int) -> type[Monitor]:
        monitor = self.db.get(Monitor, monitor_id)
        if monitor is None:
            raise MonitorNotFoundError(monitor_id)
        return monitor

    def get(self, monitor_id: int) -> type[Monitor]:
        monitor = self.get_or_fail(monitor_id)
        return monitor

    def list(self, skip=0, limit=100) -> list[type[Monitor]]:
        return self.db.query(Monitor).offset(skip).limit(limit).all()

    def create(self, data: MonitorCreate) -> Monitor:
        monitor = Monitor(
            name=data.name,
            description=data.description,
            url=str(data.url),
        )
        self.db.add(monitor)
        try:
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            raise MonitorAlreadyExistsError(str(data.url))
        self.db.refresh(monitor)
        return monitor

    def update(self, monitor_id: int, data: MonitorUpdate) -> type[Monitor]:
        monitor = self.get_or_fail(monitor_id)

        monitor.name = data.name
        monitor.description = data.description
        monitor.url = str(data.url)

        try:
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            raise MonitorAlreadyExistsError(str(data.url))
        self.db.refresh(monitor)
        return monitor

    def delete(self, monitor_id: int) -> bool:
        monitor = self.get_or_fail(monitor_id)
        self.db.delete(monitor)
        self.db.commit()
        return True
