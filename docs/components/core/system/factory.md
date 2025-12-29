# core/system/factory.py

Rendszer komponensek factory implementáció.

Ez a modul biztosítja a SystemComponentFactory osztályt, amely felelős a rendszer
szintű komponensek (pl. HealthMonitor) létrehozásáért és kezeléséért. A factory
mintát követve centralizálja a komponens példányosítást és életciklus kezelést.

A factory támogatja a következő komponenseket:
- health_monitor: Rendszer egészségügyi monitorozás

## Osztályok

### `SystemComponentFactory`

Factory osztály rendszer komponensek létrehozásához.

    A factory mintát követve centralizálja a rendszer szintű komponensek
    létrehozását és életciklus kezelését. Támogatja a különböző komponens
    implementációk regisztrálását és lekérdezését.

    A factory alkalmazza a Dependency Injection elvet, és csak interfészeken
    keresztül kommunikál a konkrét implementációkkal.

    Attributes:
        _health_monitors: Létrehozott HealthMonitor példányok gyorsítótárban.


## Függvények

### `create_health_monitor`

HealthMonitor példány létrehozása vagy visszaadása.

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

### `create_health_check`

HealthCheck példány létrehozása.

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

### `register_component`

Regisztrál egy komponenst a HealthMonitor-ban.

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

### `unregister_component`

Eltávolít egy komponenst a HealthMonitor-ból.

        Args:
            monitor_name: A HealthMonitor neve, amelyből eltávolítunk
            component_name: Az eltávolítandó komponens neve

        Raises:
            ValueError: Ha a megadott monitor_name nem létezik

        Példa:
            >>> SystemComponentFactory.unregister_component("main", "database")

### `get_health_monitor`

Lekéri a megadott névvel rendelkező HealthMonitor-t.

        Args:
            name: A HealthMonitor neve

        Returns:
            HealthMonitorInterface | None: A HealthMonitor példány, ha létezik,
                egyébként None

### `get_registered_monitors`

Visszaadja a regisztrált HealthMonitor-ok neveit.

        Returns:
            list[str]: A regisztrált HealthMonitor-ok neveinek listája

### `clear_monitors`

Törli az összes HealthMonitor példányt a gyorsítótárból.

        Ez a metódus hasznos teszteléskor vagy amikor teljesen új
        HealthMonitor példányokat szeretnénk létrehozni.


---

**Forrásfájl:** [`core/system/factory.py`](../../../neural_ai/core/system/factory.py)
