from pydantic import BaseModel
from pydantic import HttpUrl


class MonitorCreate(BaseModel):
    name: str
    description: str
    url: HttpUrl


class MonitorResponse(MonitorCreate):
    id: int