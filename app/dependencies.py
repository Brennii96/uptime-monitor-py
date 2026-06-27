from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.services.check import CheckService
from app.services.monitor import MonitorService


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_monitor_service(db: Session = Depends(get_db)) -> MonitorService:
    return MonitorService(db)


def get_check_service(db: Session = Depends(get_db)) -> CheckService:
    return CheckService(db)

