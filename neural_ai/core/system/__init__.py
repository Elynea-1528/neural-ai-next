"""Rendszer komponensek modul.

Ez a modul a rendszer szintű komponensek (pl. HealthMonitor) interfészeit
és factory osztályait exportálja.
"""

from neural_ai.core.system.factory import SystemComponentFactory
from neural_ai.core.system.interfaces.health_interface import (
    ComponentHealth,
    ComponentStatus,
    HealthCheckInterface,
    HealthMonitorInterface,
    HealthStatus,
    SystemHealth,
)

__all__ = [
    # Factory
    "SystemComponentFactory",
    # Interfaces
    "HealthMonitorInterface",
    "HealthCheckInterface",
    # Models
    "ComponentHealth",
    "ComponentStatus",
    "HealthStatus",
    "SystemHealth",
]