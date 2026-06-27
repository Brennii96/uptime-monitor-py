from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions.monitor import MonitorNotFoundError, MonitorAlreadyExistsError
from app.models import Monitor
from app.schemas import MonitorCreate, MonitorUpdate


class MonitorService:
    def __init__(self, db: Session):
        self.db = db

    def _url_exists(self, url: str, exclude_monitor_id: int | None = None) -> bool:
        query = self.db.query(Monitor).filter(Monitor.url == url)
        if exclude_monitor_id is not None:
            query = query.filter(Monitor.id != exclude_monitor_id)
        return query.first() is not None

    def _raise_if_duplicate_url(self, exc: IntegrityError, url: str) -> None:
        self.db.rollback()
        message = str(exc.orig)

        if "UNIQUE constraint failed: monitors.url" in message:
            raise MonitorAlreadyExistsError(url)

        raise exc

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
        url = str(data.url)
        if self._url_exists(url):
            raise MonitorAlreadyExistsError(url)

        monitor = Monitor(
            name=data.name,
            description=data.description,
            url=url,
        )
        self.db.add(monitor)
        try:
            self.db.commit()
        except IntegrityError as exc:
            self._raise_if_duplicate_url(exc, url)
        self.db.refresh(monitor)
        return monitor

    def update(self, monitor_id: int, data: MonitorUpdate) -> type[Monitor]:
        monitor = self.get_or_fail(monitor_id)
        url = str(data.url)

        if self._url_exists(url, exclude_monitor_id=monitor_id):
            raise MonitorAlreadyExistsError(url)

        monitor.name = data.name
        monitor.description = data.description
        monitor.url = url

        try:
            self.db.commit()
        except IntegrityError as exc:
            self._raise_if_duplicate_url(exc, url)
        self.db.refresh(monitor)
        return monitor

    def delete(self, monitor_id: int) -> bool:
        monitor = self.get_or_fail(monitor_id)
        self.db.delete(monitor)
        self.db.commit()
        return True
