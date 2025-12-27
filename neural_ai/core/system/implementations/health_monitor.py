"""Rendszer egészségügyi monitorozás implementációja.

Ez a modul a `HealthMonitorInterface` interfész konkrét implementációját tartalmazza,
amely a rendszer komponenseinek egészségügyi állapotát monitorozza, és metrikákat gyűjt.
"""

from datetime import datetime
from typing import TYPE_CHECKING, Optional

import psutil

from neural_ai.core.system.interfaces.health_interface import (
    ComponentHealth,
    ComponentStatus,
    HealthCheckInterface,
    HealthMonitorInterface,
    HealthStatus,
    SystemHealth,
)

if TYPE_CHECKING:
    from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface


class HealthMonitor(HealthMonitorInterface):
    """Rendszer egészségügyi monitorozást implementáló osztály.

    Ez az osztály a `HealthMonitorInterface` interfészt implementálja, és felelős
    a rendszer komponenseinek egészségügyi állapotának monitorozásáért, valamint
    a rendszer szintű metrikák (CPU, memória, stb.) gyűjtéséért.

    Attributes:
        _components: A monitorozott komponensek szótárát tárolja
        _logger: A naplózó interfész (opcionális)
    """

    def __init__(self, logger: Optional["LoggerInterface"] = None) -> None:
        """Inicializálja a HealthMonitor osztályt.

        Args:
            logger: A naplózó interfész (opcionális)
        """
        self._components: dict[str, HealthCheckInterface] = {}
        self._logger = logger

    def check_health(self) -> SystemHealth:
        """Ellenőrzi a teljes rendszer egészségügyi állapotát.

        A metódus összegyűjti az összes komponens és a rendszer
        egészségügyi információit, majd összesíti azokat.

        Returns:
            SystemHealth: A rendszer teljes egészségügyi állapota

        Examples:
            >>> monitor = HealthMonitor()
            >>> health = monitor.check_health()
            >>> print(f"Rendszer állapota: {health.overall_status.value}")
        """
        component_healths: list[ComponentHealth] = []
        critical_count = 0
        warning_count = 0
        unknown_count = 0

        # Ellenőrizzük az összes regisztrált komponenst
        for component_name in self._components:
            try:
                component_health = self.check_component(component_name)
                component_healths.append(component_health)

                if component_health.status == ComponentStatus.CRITICAL:
                    critical_count += 1
                elif component_health.status == ComponentStatus.WARNING:
                    warning_count += 1
                elif component_health.status == ComponentStatus.UNKNOWN:
                    unknown_count += 1
            except Exception as e:
                # Ha hiba történik egy komponens ellenőrzésekor, akkor is
                # hozzáadjuk a listához CRITICAL státusszal
                error_health = ComponentHealth(
                    name=component_name,
                    status=ComponentStatus.CRITICAL,
                    message=f"Hiba a komponens ellenőrzésekor: {str(e)}",
                    timestamp=datetime.now(),
                )
                component_healths.append(error_health)
                critical_count += 1

        # Meghatározzuk az általános rendszerállapotot
        if critical_count > 0:
            overall_status = HealthStatus.CRITICAL
            message = f"Kritikus állapotú komponensek: {critical_count}"
        elif warning_count > 0:
            overall_status = HealthStatus.DEGRADED
            message = f"Figyelmeztetés állapotú komponensek: {warning_count}"
        elif unknown_count > 0:
            overall_status = HealthStatus.UNKNOWN
            message = f"Ismeretlen állapotú komponensek: {unknown_count}"
        else:
            overall_status = HealthStatus.OK
            message = "Minden komponens egészséges"

        # Rendszer metrikák gyűjtése
        system_metrics = self._collect_system_metrics()

        return SystemHealth(
            overall_status=overall_status,
            message=message,
            timestamp=datetime.now(),
            components=component_healths,
            system_metrics=system_metrics,
        )

    def check_component(self, component_name: str) -> ComponentHealth:
        """Ellenőrzi egy adott komponens egészségügyi állapotát.

        Args:
            component_name: A komponens neve

        Returns:
            ComponentHealth: A komponens egészségügyi információi

        Raises:
            ValueError: Ha a komponens nem létezik

        Examples:
            >>> monitor = HealthMonitor()
            >>> monitor.register_component("database")
            >>> health = monitor.check_component("database")
            >>> print(f"Komponens állapota: {health.status.value}")
        """
        if component_name not in self._components:
            raise ValueError(f"A '{component_name}' komponens nincs regisztrálva")

        try:
            health_check = self._components[component_name]
            return health_check.check()
        except Exception as e:
            # Ha hiba történik az ellenőrzés során, akkor CRITICAL státuszt adunk vissza
            return ComponentHealth(
                name=component_name,
                status=ComponentStatus.CRITICAL,
                message=f"Hiba a komponens ellenőrzésekor: {str(e)}",
                timestamp=datetime.now(),
            )

    def get_registered_components(self) -> list[str]:
        """Visszaadja a monitorozott komponensek listáját.

        Returns:
            list[str]: A monitorozott komponensek nevei

        Examples:
            >>> monitor = HealthMonitor()
            >>> monitor.register_component("database")
            >>> monitor.register_component("storage")
            >>> components = monitor.get_registered_components()
            >>> print(f"Monitorozott komponensek: {components}")
        """
        return list(self._components.keys())

    def register_component(
        self, component_name: str, health_check: Optional["HealthCheckInterface"] = None
    ) -> None:
        """Regisztrál egy új komponenst a monitorozásra.

        Args:
            component_name: A komponens neve
            health_check: Az egészségügyi ellenőrzés interfésze (opcionális)

        Examples:
            >>> monitor = HealthMonitor()
            >>> # Alapértelmezett ellenőrzéssel
            >>> monitor.register_component("database")
            >>> # Egyedi ellenőrzéssel
            >>> custom_check = CustomHealthCheck()
            >>> monitor.register_component("storage", custom_check)
        """
        if component_name in self._components:
            if self._logger:
                self._logger.warning(
                    f"A '{component_name}' komponens már regisztrálva van, felülírás"
                )

        if health_check is None:
            # Alapértelmezett egészségügyi ellenőrzés létrehozása
            health_check = DefaultHealthCheck(component_name, self._logger)

        self._components[component_name] = health_check

        if self._logger:
            self._logger.info(f"'{component_name}' komponens regisztrálva")

    def unregister_component(self, component_name: str) -> None:
        """Eltávolít egy komponenst a monitorozás alól.

        Args:
            component_name: A komponens neve

        Examples:
            >>> monitor = HealthMonitor()
            >>> monitor.register_component("database")
            >>> monitor.unregister_component("database")
        """
        if component_name in self._components:
            del self._components[component_name]
            if self._logger:
                self._logger.info(f"'{component_name}' komponens eltávolítva")
        else:
            if self._logger:
                self._logger.warning(
                    f"A '{component_name}' komponens nem volt regisztrálva"
                )

    def _collect_system_metrics(self) -> dict[str, float]:
        """Gyűjti a rendszer szintű metrikákat.

        A metódus a rendszer erőforrás-használatát gyűjti (CPU, memória, stb.).

        Returns:
            Dict[str, float]: A rendszer metrikák szótára
        """
        metrics: dict[str, float] = {}

        try:
            # CPU használat
            cpu_percent = psutil.cpu_percent(interval=0.1)
            metrics["cpu_percent"] = round(cpu_percent, 2)

            # Memória használat
            memory = psutil.virtual_memory()
            metrics["memory_percent"] = round(memory.percent, 2)
            metrics["memory_used_gb"] = round(memory.used / (1024**3), 2)
            metrics["memory_total_gb"] = round(memory.total / (1024**3), 2)

            # Lemez használat (ha elérhető)
            try:
                disk = psutil.disk_usage("/")
                metrics["disk_percent"] = round((disk.used / disk.total) * 100, 2)
                metrics["disk_used_gb"] = round(disk.used / (1024**3), 2)
                metrics["disk_total_gb"] = round(disk.total / (1024**3), 2)
            except (PermissionError, OSError):
                pass

            # Hálózati metrikák (ha elérhető)
            try:
                net_io = psutil.net_io_counters()
                metrics["net_bytes_sent_mb"] = round(net_io.bytes_sent / (1024**2), 2)
                metrics["net_bytes_recv_mb"] = round(net_io.bytes_recv / (1024**2), 2)
            except (PermissionError, OSError):
                pass

        except Exception as e:
            if self._logger:
                self._logger.error(f"Hiba a rendszer metrikák gyűjtésekor: {str(e)}")

        return metrics


class DefaultHealthCheck(HealthCheckInterface):
    """Alapértelmezett egészségügyi ellenőrzés implementációja.

    Ez az osztály egy egyszerű egészségügyi ellenőrzést valósít meg,
    amely mindig HEALTHY státuszt ad vissza. Használható olyan komponensekhez,
    amelyeknek nincs specifikus egészségügyi ellenőrzésük.

    Attributes:
        _name: A komponens neve
        _logger: A naplózó interfész (opcionális)
    """

    def __init__(self, name: str, logger: Optional["LoggerInterface"] = None) -> None:
        """Inicializálja a DefaultHealthCheck osztályt.

        Args:
            name: A komponens neve
            logger: A naplózó interfész (opcionális)
        """
        self._name = name
        self._logger = logger

    def check(self) -> ComponentHealth:
        """Végrehajtja az egészségügyi ellenőrzést.

        Returns:
            ComponentHealth: Az ellenőrzés eredménye (mindig HEALTHY)
        """
        return ComponentHealth(
            name=self._name,
            status=ComponentStatus.HEALTHY,
            message="Komponens egészséges",
            timestamp=datetime.now(),
        )

    def get_name(self) -> str:
        """Visszaadja az ellenőrzés nevét.

        Returns:
            str: Az ellenőrzés neve
        """
        return self._name
