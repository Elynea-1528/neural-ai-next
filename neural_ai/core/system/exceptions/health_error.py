"""Rendszer egészségügyi komponens kivételei.

Ez a modul tartalmazza a rendszer egészségügyi komponenshez tartozó kivételeket.
"""


class HealthError(Exception):
    """Alap kivétel a rendszer egészségügyi komponenshez."""

    pass


class HealthMonitorError(HealthError):
    """HealthMonitor általános hiba."""

    pass


class HealthCheckError(HealthError):
    """Egészségügyi ellenőrzés hiba."""

    pass


class ComponentNotFoundError(HealthMonitorError):
    """Komponens nem található hiba."""

    pass
