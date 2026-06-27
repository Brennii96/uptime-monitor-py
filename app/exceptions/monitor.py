from app.exceptions.base import NotFoundError


class MonitorNotFoundError(NotFoundError):
    def __init__(self, monitor_id: int):
        super().__init__(f"Monitor {monitor_id} not found")
