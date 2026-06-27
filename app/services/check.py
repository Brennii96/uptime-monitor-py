from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import Check


class CheckService:
    def __init__(self, db: Session):
        self.db = db

    def list_by_monitor(self, monitor_id: int, skip=0, limit=100) -> list[Check]:
        return self.db.query(Check).filter(Check.monitor_id == monitor_id).offset(skip).limit(limit).all()

    def uptime_percentage(self, monitor_id: int) -> float:
        total = self.db.query(func.count(Check.id)).filter(Check.monitor_id == monitor_id).scalar()
        if total == 0:
            return 0.0
        up = self.db.query(func.count(Check.id)).filter(Check.monitor_id == monitor_id, Check.is_up.is_(True)).scalar()
        return (up / total) * 100
