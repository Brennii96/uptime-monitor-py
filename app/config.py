import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./uptime_monitor.db")
