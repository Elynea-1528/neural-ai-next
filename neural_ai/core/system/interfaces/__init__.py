"""Rendszer egészségügyi komponens interfészei.

Ez a csomag tartalmazza a rendszer egészségügyi monitorozáshoz szükséges interfészeket
és típusokat.
"""

from neural_ai.core.system.interfaces.health_interface import (
    ComponentHealth,
    ComponentStatus,
    HealthCheckInterface,
    HealthMonitorInterface,
    HealthStatus,
    SystemHealth,
)

__all__ = [
    "ComponentHealth",
    "ComponentStatus",
    "HealthCheckInterface",
    "HealthMonitorInterface",
    "HealthStatus",
    "SystemHealth",
]
