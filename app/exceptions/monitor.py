from app.exceptions.base import IntegrityConstraintError, NotFoundError


class MonitorNotFoundError(NotFoundError):
    def __init__(self, monitor_id: int):
        super().__init__(f"Monitor {monitor_id} not found")


class MonitorAlreadyExistsError(IntegrityConstraintError):
    def __init__(self, url: str):
        super().__init__(f"Monitor with url {url} already exists")
