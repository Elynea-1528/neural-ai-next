"""Rendszer komponensek factory implementáció.

Ez a modul biztosítja a SystemComponentFactory osztályt, amely felelős a rendszer
szintű komponensek (pl. HealthMonitor) létrehozásáért és kezeléséért. A factory
mintát követve centralizálja a komponens példányosítást és életciklus kezelést.

A factory támogatja a következő komponenseket:
- health_monitor: Rendszer egészségügyi monitorozás
"""

from typing import TYPE_CHECKING, Any

from neural_ai.core.system.interfaces.health_interface import (
    HealthCheckInterface,
    HealthMonitorInterface,
)

if TYPE_CHECKING:
    from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface


class SystemComponentFactory:
    """Factory osztály rendszer komponensek létrehozásához.

    A factory mintát követve centralizálja a rendszer szintű komponensek
    létrehozását és életciklus kezelését. Támogatja a különböző komponens
    implementációk regisztrálását és lekérdezését.

    A factory alkalmazza a Dependency Injection elvet, és csak interfészeken
    keresztül kommunikál a konkrét implementációkkal.

    Attributes:
        _health_monitors: Létrehozott HealthMonitor példányok gyorsítótárban.
    """

    _health_monitors: dict[str, HealthMonitorInterface] = {}

    @classmethod
    def create_health_monitor(
        cls,
        name: str = "default",
        logger: "LoggerInterface | None" = None,
        **kwargs: Any,
    ) -> HealthMonitorInterface:
        """HealthMonitor példány létrehozása vagy visszaadása.

        A metódus létrehozza a HealthMonitor komponenst a megadott paraméterekkel,
        vagy visszaadja a meglévő példányt, ha már létezik az adott névvel.

        Args:
            name: A HealthMonitor egyedi neve (alapértelmezett: "default")
            logger: Logger interfész a naplózásra (opcionális)
            **kwargs: További paraméterek a HealthMonitor konstruktorának

        Returns:
            HealthMonitorInterface: Az inicializált HealthMonitor példány

        Példa:
            >>> from neural_ai.core.logger import LoggerFactory
            >>> logger = LoggerFactory.get_logger("system")
            >>> monitor = SystemComponentFactory.create_health_monitor(
            ...     name="main",
            ...     logger=logger
            ... )
            >>> health = monitor.check_health()
            >>> print(f"Rendszer állapota: {health.overall_status.value}")
        """
        # Ha már létezik ilyen nevű HealthMonitor, azt adjuk vissza
        if name in cls._health_monitors:
            return cls._health_monitors[name]

        # Lazy loading a konkrét implementációhoz
        from neural_ai.core.system.implementations.health_monitor import HealthMonitor

        # Dependency Injection: logger átadása
        monitor = HealthMonitor(logger=logger, **kwargs)

        cls._health_monitors[name] = monitor
        return monitor

    @classmethod
    def create_health_check(
        cls,
        component_name: str,
        logger: "LoggerInterface | None" = None,
        health_check_type: str = "default",
        **kwargs: Any,
    ) -> HealthCheckInterface:
        """HealthCheck példány létrehozása.

        A metódus létrehozza a megadott típusú HealthCheck komponenst.

        Args:
            component_name: A komponens neve, amelyet az ellenőrzés monitoroz
            logger: Logger interfész a naplózásra (opcionális)
            health_check_type: Az ellenőrzés típusa (alapértelmezett: "default")
            **kwargs: További paraméterek a HealthCheck konstruktorának

        Returns:
            HealthCheckInterface: Az inicializált HealthCheck példány

        Raises:
            ValueError: Ha az ismeretlen health_check_type van megadva

        Példa:
            >>> check = SystemComponentFactory.create_health_check(
            ...     component_name="database",
            ...     health_check_type="default"
            ... )
            >>> health = check.check()
            >>> print(f"Komponens állapota: {health.status.value}")
        """
        # Jelenleg csak a DefaultHealthCheck támogatott
        if health_check_type != "default":
            raise ValueError(f"Ismeretlen health check típus: {health_check_type}")

        # Lazy loading a konkrét implementációhoz
        from neural_ai.core.system.implementations.health_monitor import DefaultHealthCheck

        return DefaultHealthCheck(name=component_name, logger=logger, **kwargs)

    @classmethod
    def register_component(
        cls,
        monitor_name: str,
        component_name: str,
        health_check: "HealthCheckInterface | None" = None,
    ) -> None:
        """Regisztrál egy komponenst a HealthMonitor-ban.

        A metódus regisztrálja a megadott komponenst a monitorozásra a
        HealthMonitor-ban. Ha nincs megadva egyedi HealthCheck, akkor
        alapértelmezett ellenőrzést használ.

        Args:
            monitor_name: A HealthMonitor neve, amelybe regisztrálunk
            component_name: A regisztrálandó komponens neve
            health_check: Egyedi HealthCheck interfész (opcionális)

        Raises:
            ValueError: Ha a megadott monitor_name nem létezik

        Példa:
            >>> monitor = SystemComponentFactory.create_health_monitor("main")
            >>> SystemComponentFactory.register_component(
            ...     monitor_name="main",
            ...     component_name="database"
            ... )
            >>> SystemComponentFactory.register_component(
            ...     monitor_name="main",
            ...     component_name="storage",
            ...     health_check=custom_check
            ... )
        """
        if monitor_name not in cls._health_monitors:
            raise ValueError(f"A '{monitor_name}' HealthMonitor nem létezik")

        monitor = cls._health_monitors[monitor_name]
        # Lazy loading a konkrét implementációhoz
        from neural_ai.core.system.implementations.health_monitor import HealthMonitor

        if isinstance(monitor, HealthMonitor):
            # A HealthMonitor.register_component metódusának szignatúrája:
            # register_component(self, component_name: str,
            #                    health_check: Optional["HealthCheckInterface"] = None)
            monitor.register_component(component_name, health_check)
        else:
            # Fallback, ha más implementációt használnánk
            monitor.register_component(component_name)

    @classmethod
    def unregister_component(cls, monitor_name: str, component_name: str) -> None:
        """Eltávolít egy komponenst a HealthMonitor-ból.

        Args:
            monitor_name: A HealthMonitor neve, amelyből eltávolítunk
            component_name: Az eltávolítandó komponens neve

        Raises:
            ValueError: Ha a megadott monitor_name nem létezik

        Példa:
            >>> SystemComponentFactory.unregister_component("main", "database")
        """
        if monitor_name not in cls._health_monitors:
            raise ValueError(f"A '{monitor_name}' HealthMonitor nem létezik")

        monitor = cls._health_monitors[monitor_name]
        monitor.unregister_component(component_name)

    @classmethod
    def get_health_monitor(cls, name: str) -> "HealthMonitorInterface | None":
        """Lekéri a megadott névvel rendelkező HealthMonitor-t.

        Args:
            name: A HealthMonitor neve

        Returns:
            HealthMonitorInterface | None: A HealthMonitor példány, ha létezik,
                egyébként None
        """
        return cls._health_monitors.get(name)

    @classmethod
    def get_registered_monitors(cls) -> list[str]:
        """Visszaadja a regisztrált HealthMonitor-ok neveit.

        Returns:
            list[str]: A regisztrált HealthMonitor-ok neveinek listája
        """
        return list(cls._health_monitors.keys())

    @classmethod
    def clear_monitors(cls) -> None:
        """Törli az összes HealthMonitor példányt a gyorsítótárból.

        Ez a metódus hasznos teszteléskor vagy amikor teljesen új
        HealthMonitor példányokat szeretnénk létrehozni.
        """
        cls._health_monitors.clear()
