# Dashboard Service

## Áttekintés

A Dashboard Service a Neural AI Next rendszer fő irányítópultjának adatait és állapotát kezeli. Ez az osztály implementálja a dashboard adatok lekérdezését és kezelését végző metódusokat.

## Architektúra

### Osztály

```python
class DashboardService(DashboardServiceInterface)
```

### Interfész

- [`DashboardServiceInterface`](../../../neural_ai/ui/interfaces/dashboard_service_interface.py)

### Függőségek

- `CoreBridgeInterface`: Backend kapcsolatért felelős bridge
- `HealthMonitorInterface`: Rendszer egészségügyi állapotának monitorozásához
- `ComponentHealth`, `ComponentStatus`, `SystemHealth`: Egészségügyi állapot modellek

## Metódusok

### `get_health_status()`

Rendszer egészségügyi állapotának lekérdezése.

A metódus a valós HealthMonitor komponenst kérdezi le a backend rendszerből, és leképezi a komponens állapotokat UI-barát formátumba.

**Visszatérési érték:**
```python
Dict[str, str]  # A komponensek állapota (OK/WARNING/ERROR/CRITICAL/UNKNOWN)
```

**Implementáció:**

1. **Fallback ellenőrzés**: Ha a bridge vagy a health monitor nem elérhető, `{"system": "UNKNOWN"}` értékkel tér vissza.

2. **Valós lekérdezés**: A HealthMonitor `check_health()` metódusát hívja meg.

3. **Állapot mapping**: A `ComponentStatus` enum értékeket sztringekké konvertálja:
   - `HEALTHY` → `"OK"`
   - `WARNING` → `"WARNING"`
   - `CRITICAL` → `"ERROR"`
   - `UNKNOWN` → `"UNKNOWN"`
   - `OFFLINE` → `"OFFLINE"`

4. **Rendszer állapot**: Hozzáadja a rendszer általános állapotát is (`health.overall_status`).

**Példa kimenet:**
```python
{
    "core": "OK",
    "database": "WARNING", 
    "event_bus": "OK",
    "storage": "OK",
    "system": "DEGRADED"
}
```

### `get_system_overview()`

Rendszer áttekintő adatok lekérdezése.

**Visszatérési érték:**
```python
Dict[str, Any]  # A rendszer aktuális állapota
```

### `get_performance_metrics()`

Teljesítmény metrikák lekérdezése.

**Visszatérési érték:**
```python
Dict[str, float]  # A rendszer teljesítményadatok
```

Tartalmazza a következő metrikákat:
- `cpu_usage`: CPU használat százalékban
- `memory_usage`: Memória használat százalékban
- `disk_usage`: Lemez használat százalékban
- `network_io`: Hálózati I/O (mock adat)
- `disk_io`: Lemez I/O (mock adat)
- `response_time`: Válaszidő (mock adat)

### `get_recent_activities()`

Legutóbbi tevékenységek lekérdezése.

**Visszatérési érték:**
```python
List[Dict[str, Any]]  # A tevékenységek listája
```

### `refresh_data()`

Dashboard adatok frissítése. Törli a gyorsítótárazott adatokat és értesíti a feliratkozókat.

### `subscribe_to_updates(callback)`

Feliratkozás dashboard frissítésekre.

**Paraméterek:**
- `callback`: A hívandó callback függvény

## Használati példa

```python
from neural_ai.ui.services.dashboard_service import DashboardService
from neural_ai.ui.core_bridge import CoreBridge

# Bridge inicializálása
bridge = CoreBridge()
bridge.initialize()

# Service létrehozása
dashboard_service = DashboardService(bridge)

# Egészségügyi állapot lekérdezése
health_status = dashboard_service.get_health_status()
print(f"Rendszer állapota: {health_status}")

# Teljesítmény metrikák lekérdezése
metrics = dashboard_service.get_performance_metrics()
print(f"CPU használat: {metrics['cpu_usage']}%")

# Frissítés
dashboard_service.refresh_data()
```

## Adattárolás

A service gyorsítótárazza a lekérdezett adatokat a `_cached_data` szótárban:
- `overview`: Rendszer áttekintő adatok
- `health`: Egészségügyi állapot
- `metrics`: Teljesítmény metrikák
- `activities`: Legutóbbi tevékenységek

## Feliratkozói rendszer

A service támogatja a feliratkozói mintát:
- `_subscribers`: Callback függvények listája
- `subscribe_to_updates()`: Új feliratkozó hozzáadása
- `_notify_subscribers()`: Értesítés küldése minden feliratkozónak

## Hibakezelés

- **Callback hibák**: Ha egy feliratkozó callback hibát dob, a rendszer logolja a hibát, de nem áll le.
- **HealthMonitor elérhetetlenség**: Ha a HealthMonitor nem elérhető, a rendszer `UNKNOWN` állapottal tér vissza.

## Fejlesztési jegyzetek

- A metódusok magyar docstring-et használnak (Google Style).
- Szigorú típusos annotációk (`Dict`, `List`, `Optional`, stb.).
- A `TYPE_CHECKING` blokk segítségével kerülik a körkörös importokat.
- A `cast()` függvény használata a típuskonverzióhoz.