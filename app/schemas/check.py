from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CheckBase(BaseModel):
    status_code: int
    response_time_ms: int | None
    is_up: bool


class CheckRead(CheckBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    monitor_id: int
    checked_at: datetime
