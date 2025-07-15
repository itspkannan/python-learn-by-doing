
from service_management.core import HealthStatus, Service


class ServiceManager:
    def __init__(self):
        self.services: list[Service] = []

    def register(self, service: Service):
        self.services.append(service)

    async def start_all(self):
        for service in self.services:
            try:
                await service.start()
            except Exception as e:
                service.health_status = HealthStatus.ERROR
                print(f"[{service.name}] Failed to start: {e}")

    async def stop_all(self):
        for service in self.services:
            try:
                await service.stop()
            except Exception as e:
                print(f"[{service.name}] Failed to stop: {e}")

    def get_health_report(self) -> dict[str, dict]:
        return {svc.name: svc.health_check() for svc in self.services}

    def get_status(self) -> dict[str, str]:
        return {
            svc.name: f"{svc.running_status.value} / {svc.health_status.value}"
            for svc in self.services
        }

    def get_metrics(self) -> dict[str, dict[str, int]]:
        return {
            svc.name: {
                "events_processed": svc.events_processed,
                "reconnects": svc.reconnects,
            }
            for svc in self.services
        }

    def get_service(self, name: str) -> Service:
        for svc in self.services:
            if svc.name == name:
                return svc
        raise KeyError(f"Service '{name}' not registered.")
