from typing import Optional
from datetime import datetime

from service_management.status import HealthStatus, RunningStatus


class Service:
    def __init__(self, name: str):
        self.name = name
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.reconnects = 0
        self.events_processed = 0
        self.health_status = HealthStatus.UNKNOWN
        self.running_status = RunningStatus.INITIALIZED

    async def start(self):
        self.start_time = datetime.utcnow()
        self.running_status = RunningStatus.STARTED
        self.health_status = HealthStatus.HEALTHY
        print(f"[{self.name}] Started at {self.start_time}")

    async def stop(self):
        self.end_time = datetime.utcnow()
        self.running_status = RunningStatus.STOPPED
        print(f"[{self.name}] Stopped at {self.end_time}")

    def health_check(self) -> dict:
        return {
            "name": self.name,
            "health_status": self.health_status.value,
            "running_status": self.running_status.value,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "reconnects": self.reconnects,
            "events_processed": self.events_processed,
        }

    def increment_events(self, count: int = 1):
        self.events_processed += count

    def increment_reconnects(self):
        self.reconnects += 1
