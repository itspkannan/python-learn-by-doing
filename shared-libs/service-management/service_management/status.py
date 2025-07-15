from enum import Enum, auto


class HealthStatus(Enum):
    UNKNOWN = "UNKNOWN"
    HEALTHY = "HEALTHY"
    UNHEALTHY = "UNHEALTHY"
    ERROR = "ERROR"


class RunningStatus(Enum):
    INITIALIZED = "INITIALIZED"
    STARTED = "STARTED"
    STOPPED = "STOPPED"
