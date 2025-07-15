import logging
from abc import ABC
from datetime import datetime

from service_management.core import HealthStatus, Registry, RunningStatus


class Service(ABC):
    def __init__(self, name: str):
        self.name = name
        self.start_time: datetime | None = None
        self.end_time: datetime | None = None
        self.reconnects = 0
        self.events_processed = 0
        self.health_status = HealthStatus.UNKNOWN
        self.running_status = RunningStatus.INITIALIZED
        self.logger = logging.getLogger(f"service.{name}")

    async def start(self):
        start_timestamp = datetime.utcnow()
        self.start_time = start_timestamp
        self.running_status = RunningStatus.STARTED
        self.health_status = HealthStatus.HEALTHY
        Registry.register_instance(self.name, self)
        self.__log_status_change("Started", start_timestamp)

    def __log_status_change(self, action: str, timestamp: datetime) -> None:
        self.logger.info(f"{action} at {timestamp}")

    def _update_service_status(self, status: RunningStatus, timestamp: datetime) -> None:
        self.running_status = status
        if status == RunningStatus.STOPPED:
            self.end_time = timestamp
        elif status == RunningStatus.STARTED:
            self.start_time = timestamp

    async def stop(self) -> None:
        stop_timestamp = datetime.utcnow()
        self._update_service_status(RunningStatus.STOPPED, stop_timestamp)
        Registry.deregister_instance(self.name)
        self.__log_status_change("Stopped", stop_timestamp)

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
