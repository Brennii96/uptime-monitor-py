from datetime import datetime

from pydantic import BaseModel, HttpUrl, ConfigDict

from app.schemas.check import CheckRead


class MonitorBase(BaseModel):
    name: str
    description: str | None = None
    url: HttpUrl


class MonitorCreate(MonitorBase):
    pass


class MonitorUpdate(MonitorBase):
    pass


class MonitorRead(MonitorBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    checks: list[CheckRead] = []
