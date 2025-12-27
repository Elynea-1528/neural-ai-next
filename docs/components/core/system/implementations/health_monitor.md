# HealthMonitor Implementáció

## Áttekintés

A `HealthMonitor` osztály a [`HealthMonitorInterface`](../interfaces/health_interface.md) interfész konkrét implementációja, amely a rendszer komponenseinek egészségügyi állapotát monitorozza, és rendszer szintű metrikákat gyűjt.

## Jellemzők

- **Komponens Monitorozás**: A rendszer komponenseinek egészségügyi állapotának nyomon követése
- **Rendszer Metrikák**: CPU, memória, lemez és hálózati metrikák automatikus gyűjtése
- **Állapot Összesítés**: A komponensek állapotának összesítése rendszer szintű egészségügyi állapotba
- **Rugalmas Ellenőrzés**: Egyedi egészségügyi ellenőrzések támogatása
- **Naplózás**: Opcionális naplózási támogatás

## Osztályok

### HealthMonitor

A fő monitorozó osztály, amely implementálja a `HealthMonitorInterface` interfészt.

#### Metódusok

##### `__init__(logger: Optional[LoggerInterface] = None) -> None`

Inicializálja a HealthMonitor osztályt.

**Paraméterek:**
- `logger`: A naplózó interfész (opcionális)

**Példa:**
```python
from neural_ai.core.logger.factory import LoggerFactory
from neural_ai.core.system.implementations.health_monitor import HealthMonitor

# Naplózóval
logger = LoggerFactory.create_logger("health_monitor")
monitor = HealthMonitor(logger=logger)

# Naplózó nélkül
monitor = HealthMonitor()
```

##### `check_health() -> SystemHealth`

Ellenőrzi a teljes rendszer egészségügyi állapotát.

**Visszatérési érték:**
- `SystemHealth`: A rendszer teljes egészségügyi állapota

**Példa:**
```python
health = monitor.check_health()
print(f"Rendszer állapota: {health.overall_status.value}")
print(f"Üzenet: {health.message}")
print(f"Komponensek száma: {len(health.components)}")

# Rendszer metrikák kiírása
if health.system_metrics:
    print(f"CPU használat: {health.system_metrics['cpu_percent']}%")
    print(f"Memória használat: {health.system_metrics['memory_percent']}%")
```

##### `check_component(component_name: str) -> ComponentHealth`

Ellenőrzi egy adott komponens egészségügyi állapotát.

**Paraméterek:**
- `component_name`: A komponens neve

**Visszatérési érték:**
- `ComponentHealth`: A komponens egészségügyi információi

**Kivételek:**
- `ValueError`: Ha a komponens nem létezik

**Példa:**
```python
try:
    health = monitor.check_component("database")
    print(f"Komponens állapota: {health.status.value}")
    print(f"Üzenet: {health.message}")
except ValueError as e:
    print(f"Hiba: {e}")
```

##### `get_registered_components() -> list[str]`

Visszaadja a monitorozott komponensek listáját.

**Visszatérési érték:**
- `list[str]`: A monitorozott komponensek nevei

**Példa:**
```python
components = monitor.get_registered_components()
print(f"Monitorozott komponensek: {components}")
```

##### `register_component(component_name: str, health_check: Optional[HealthCheckInterface] = None) -> None`

Regisztrál egy új komponenst a monitorozásra.

**Paraméterek:**
- `component_name`: A komponens neve
- `health_check`: Az egészségügyi ellenőrzés interfésze (opcionális)

**Példa:**
```python
# Alapértelmezett ellenőrzéssel
monitor.register_component("database")

# Egyedi ellenőrzéssel
from neural_ai.core.system.interfaces.health_interface import HealthCheckInterface

class CustomHealthCheck(HealthCheckInterface):
    def check(self) -> ComponentHealth:
        # Egyedi ellenőrzési logika
        return ComponentHealth(
            name=self.get_name(),
            status=ComponentStatus.HEALTHY,
            message="Custom check passed",
            timestamp=datetime.now()
        )
    
    def get_name(self) -> str:
        return "database"

custom_check = CustomHealthCheck()
monitor.register_component("database", custom_check)
```

##### `unregister_component(component_name: str) -> None`

Eltávolít egy komponenst a monitorozás alól.

**Paraméterek:**
- `component_name`: A komponens neve

**Példa:**
```python
monitor.unregister_component("database")
```

### DefaultHealthCheck

Alapértelmezett egészségügyi ellenőrzés implementációja, amely mindig `HEALTHY` státuszt ad vissza. Használható olyan komponensekhez, amelyeknek nincs specifikus egészségügyi ellenőrzésük.

#### Metódusok

##### `__init__(name: str, logger: Optional[LoggerInterface] = None) -> None`

Inicializálja a DefaultHealthCheck osztályt.

**Paraméterek:**
- `name`: A komponens neve
- `logger`: A naplózó interfész (opcionális)

##### `check() -> ComponentHealth`

Végrehajtja az egészségügyi ellenőrzést.

**Visszatérési érték:**
- `ComponentHealth`: Az ellenőrzés eredménye (mindig HEALTHY)

##### `get_name() -> str`

Visszaadja az ellenőrzés nevét.

**Visszatérési érték:**
- `str`: Az ellenőrzés neve

## Rendszer Metrikák

A `HealthMonitor` automatikusan gyűjti a következő rendszer metrikákat:

### CPU Metrikák
- `cpu_percent`: CPU használat százalékban

### Memória Metrikák
- `memory_percent`: Memória használat százalékban
- `memory_used_gb`: Használt memória GB-ban
- `memory_total_gb`: Teljes memória GB-ban

### Lemez Metrikák
- `disk_percent`: Lemez használat százalékban
- `disk_used_gb`: Használt lemezterület GB-ban
- `disk_total_gb`: Teljes lemezterület GB-ban

### Hálózati Metrikák
- `net_bytes_sent_mb`: Elküldött adatok MB-ban
- `net_bytes_recv_mb`: Fogadott adatok MB-ban

## Használati Példák

### Alapvető Használat

```python
from neural_ai.core.system.implementations.health_monitor import HealthMonitor
from neural_ai.core.system.interfaces.health_interface import ComponentStatus, HealthStatus

# Monitor létrehozása
monitor = HealthMonitor()

# Komponensek regisztrálása
monitor.register_component("database")
monitor.register_component("storage")
monitor.register_component("api")

# Rendszer egészségügyi állapot ellenőrzése
health = monitor.check_health()

print(f"Általános állapot: {health.overall_status.value}")
print(f"Üzenet: {health.message}")
print(f"Timestamp: {health.timestamp}")

# Komponensek állapotának kiírása
for component in health.components:
    print(f"  {component.name}: {component.status.value} - {component.message}")

# Rendszer metrikák
if health.system_metrics:
    print("\nRendszer metrikák:")
    for key, value in health.system_metrics.items():
        print(f"  {key}: {value}")
```

### Egyedi Egészségügyi Ellenőrzés

```python
from datetime import datetime
from neural_ai.core.system.implementations.health_monitor import HealthMonitor
from neural_ai.core.system.interfaces.health_interface import (
    ComponentHealth,
    ComponentStatus,
    HealthCheckInterface,
)

class DatabaseHealthCheck(HealthCheckInterface):
    def __init__(self, database_connection):
        self.database_connection = database_connection
    
    def check(self) -> ComponentHealth:
        try:
            # Adatbázis kapcsolat ellenőrzése
            self.database_connection.ping()
            return ComponentHealth(
                name="database",
                status=ComponentStatus.HEALTHY,
                message="Database connection OK",
                timestamp=datetime.now(),
                metrics={"response_time_ms": 10.5}
            )
        except Exception as e:
            return ComponentHealth(
                name="database",
                status=ComponentStatus.CRITICAL,
                message=f"Database connection failed: {str(e)}",
                timestamp=datetime.now()
            )
    
    def get_name(self) -> str:
        return "database"

# Monitor létrehozása egyedi ellenőrzéssel
monitor = HealthMonitor()
db_check = DatabaseHealthCheck(database_connection)
monitor.register_component("database", db_check)

# Adatbázis állapot ellenőrzése
db_health = monitor.check_component("database")
print(f"Adatbázis állapota: {db_health.status.value}")
```

### Állapot Szűrése

```python
from neural_ai.core.system.implementations.health_monitor import HealthMonitor
from neural_ai.core.system.interfaces.health_interface import ComponentStatus

monitor = HealthMonitor()
# ... komponensek regisztrálása ...

health = monitor.check_health()

# Kritikus állapotú komponensek szűrése
critical_components = [
    c for c in health.components 
    if c.status == ComponentStatus.CRITICAL
]

if critical_components:
    print("Kritikus állapotú komponensek:")
    for component in critical_components:
        print(f"  - {component.name}: {component.message}")
```

## Hibakezelés

A `HealthMonitor` robusztus hibakezelést valósít meg:

1. **Komponens Ellnőrzési Hibák**: Ha egy komponens ellenőrzése során hiba történik, a komponens `CRITICAL` státuszt kap
2. **Rendszer Metrika Hibák**: Ha a rendszer metrikák gyűjtése során hiba történik, a metrikák szótára üres marad
3. **Nem Létező Komponens**: A `check_component` metódus `ValueError` kivételt dob, ha a komponens nem létezik

## Tesztelés

A `HealthMonitor` osztályt átfogó egységtesztek ellenőrzik:

- Komponens regisztráció és eltávolítás
- Egészségügyi állapot ellenőrzés
- Rendszer metrikák gyűjtése
- Hibakezelés
- Naplózási integráció

Tesztfájl: [`test_health_monitor.py`](../../../../tests/core/system/implementations/test_health_monitor.py)

**Teszt Coverage**: 87% (Statement Coverage)

## Függőségek

- `psutil`: Rendszer metrikák gyűjtéséhez
- `neural_ai.core.system.interfaces.health_interface`: Az interfész definíciók
- `neural_ai.core.logger.interfaces.logger_interface`: Naplózási támogatáshoz (opcionális)

## Kapcsolódó Dokumentáció

- [HealthMonitorInterface](../interfaces/health_interface.md) - Az interfész definíciója
- [System Architecture](../../../planning/specs/01_system_architecture.md) - Rendszer architektúra
- [Observability & Logging](../../../planning/specs/03_observability_logging.md) - Megfigyelhetőség specifikáció