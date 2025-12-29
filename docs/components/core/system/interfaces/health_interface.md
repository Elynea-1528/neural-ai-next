# core/system/interfaces/health_interface.py

Rendszer egészségügyi monitorozás interfészei.

Ez a modul a rendszer egészségügyi állapotának monitorozásához szükséges
interfészeket definiálja, beleértve a komponens állapotokat, erőforrás-használatot
és rendszer metrikákat.

## Osztályok

### `ComponentStatus`

Komponens állapot enum.

    A rendszer komponenseinek állapotát definiálja.

### `HealthStatus`

Rendszer egészségügyi állapot enum.

    A teljes rendszer egészségügyi állapotát definiálja.

### `ComponentHealth`

Komponens egészségügyi információi.

    Egy adott komponens egészségügyi állapotát és metrikáit tartalmazza.

    Attributes:
        name: A komponens neve
        status: A komponens állapota (ComponentStatus enum)
        message: Részletes üzenet vagy hiba
        timestamp: Az állapot ellenőrzésének időpontja
        metrics: Opcionális metrikák (pl. response time, error rate)

### `SystemHealth`

Rendszer egészségügyi információi.

    A teljes rendszer egészségügyi állapotát és komponenseinek állapotát tartalmazza.

    Attributes:
        overall_status: A rendszer általános állapota (HealthStatus enum)
        message: Részletes üzenet
        timestamp: Az ellenőrzés időpontja
        components: A komponensek egészségügyi információi
        system_metrics: Rendszer szintű metrikák (CPU, memória, stb.)

### `HealthMonitorInterface`

Rendszer egészségügyi monitorozás interfész.

    Ez az interfész definiálja a rendszer egészségügyi állapotának
    monitorozásához szükséges metódusokat.

### `HealthCheckInterface`

Egyedi egészségügyi ellenőrzés interfész.

    Ez az interfész egy specifikus egészségügyi ellenőrzést definiál,
    amelyet a HealthMonitorInterface implementációk használhatnak.


## Függvények

### `check_health`

Ellenőrzi a teljes rendszer egészségügyi állapotát.

        A metódus összegyűjti az összes komponens és a rendszer
        egészségügyi információit, majd összesíti azokat.

        Returns:
            SystemHealth: A rendszer teljes egészségügyi állapota

### `check_component`

Ellenőrzi egy adott komponens egészségügyi állapotát.

        Args:
            component_name: A komponens neve

        Returns:
            ComponentHealth: A komponens egészségügyi információi

        Raises:
            ValueError: Ha a komponens nem létezik

### `get_registered_components`

Visszaadja a monitorozott komponensek listáját.

        Returns:
            list[str]: A monitorozott komponensek nevei

### `register_component`

Regisztrál egy új komponenst a monitorozásra.

        Args:
            component_name: A komponens neve

### `unregister_component`

Eltávolít egy komponenst a monitorozás alól.

        Args:
            component_name: A komponens neve

### `check`

Végrehajtja az egészségügyi ellenőrzést.

        Returns:
            ComponentHealth: Az ellenőrzés eredménye

### `get_name`

Visszaadja az ellenőrzés nevét.

        Returns:
            str: Az ellenőrzés neve


---

**Forrásfájl:** [`core/system/interfaces/health_interface.py`](../../../neural_ai/core/system/interfaces/health_interface.py)
