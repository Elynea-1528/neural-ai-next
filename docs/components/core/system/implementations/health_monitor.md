# core/system/implementations/health_monitor.py

Rendszer egészségügyi monitorozás implementációja.

Ez a modul a `HealthMonitorInterface` interfész konkrét implementációját tartalmazza,
amely a rendszer komponenseinek egészségügyi állapotát monitorozza, és metrikákat gyűjt.

## Osztályok

### `HealthMonitor`

Rendszer egészségügyi monitorozást implementáló osztály.

    Ez az osztály a `HealthMonitorInterface` interfészt implementálja, és felelős
    a rendszer komponenseinek egészségügyi állapotának monitorozásáért, valamint
    a rendszer szintű metrikák (CPU, memória, stb.) gyűjtéséért.

    Attributes:
        _components: A monitorozott komponensek szótárát tárolja
        _logger: A naplózó interfész (opcionális)

### `DefaultHealthCheck`

Alapértelmezett egészségügyi ellenőrzés implementációja.

    Ez az osztály egy egyszerű egészségügyi ellenőrzést valósít meg,
    amely mindig HEALTHY státuszt ad vissza. Használható olyan komponensekhez,
    amelyeknek nincs specifikus egészségügyi ellenőrzésük.

    Attributes:
        _name: A komponens neve
        _logger: A naplózó interfész (opcionális)


## Függvények

### `__init__`

Inicializálja a DefaultHealthCheck osztályt.

        Args:
            name: A komponens neve
            logger: A naplózó interfész (opcionális)

### `check_health`

Ellenőrzi a teljes rendszer egészségügyi állapotát.

        A metódus összegyűjti az összes komponens és a rendszer
        egészségügyi információit, majd összesíti azokat.

        Returns:
            SystemHealth: A rendszer teljes egészségügyi állapota

        Examples:
            >>> monitor = HealthMonitor()
            >>> health = monitor.check_health()
            >>> print(f"Rendszer állapota: {health.overall_status.value}")

### `check_component`

Ellenőrzi egy adott komponens egészségügyi állapotát.

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

### `get_registered_components`

Visszaadja a monitorozott komponensek listáját.

        Returns:
            list[str]: A monitorozott komponensek nevei

        Examples:
            >>> monitor = HealthMonitor()
            >>> monitor.register_component("database")
            >>> monitor.register_component("storage")
            >>> components = monitor.get_registered_components()
            >>> print(f"Monitorozott komponensek: {components}")

### `register_component`

Regisztrál egy új komponenst a monitorozásra.

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

### `unregister_component`

Eltávolít egy komponenst a monitorozás alól.

        Args:
            component_name: A komponens neve

        Examples:
            >>> monitor = HealthMonitor()
            >>> monitor.register_component("database")
            >>> monitor.unregister_component("database")

### `_collect_system_metrics`

Gyűjti a rendszer szintű metrikákat.

        A metódus a rendszer erőforrás-használatát gyűjti (CPU, memória, stb.).

        Returns:
            Dict[str, float]: A rendszer metrikák szótára

### `check`

Végrehajtja az egészségügyi ellenőrzést.

        Returns:
            ComponentHealth: Az ellenőrzés eredménye (mindig HEALTHY)

### `get_name`

Visszaadja az ellenőrzés nevét.

        Returns:
            str: Az ellenőrzés neve


---

**Forrásfájl:** [`core/system/implementations/health_monitor.py`](../../../neural_ai/core/system/implementations/health_monitor.py)
