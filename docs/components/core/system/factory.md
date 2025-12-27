# SystemComponentFactory - Rendszer komponensek factory

## 🎯 Cél és Feladat

A `SystemComponentFactory` osztály a rendszer szintű komponensek (elsősorban a `HealthMonitor`) létrehozásáért és kezeléséért felelős. A factory mintát követve centralizálja a komponens példányosítást és életciklus kezelést, biztosítva a dependency injection elv alkalmazását.

## 🏗️ Architektúra

### Osztálydiagram

```
┌─────────────────────────────────────────────┐
│     SystemComponentFactory                  │
│                                             │
│  - _health_monitors: dict[str,              │
│              HealthMonitorInterface]        │
│                                             │
│  + create_health_monitor()                  │
│  + create_health_check()                    │
│  + register_component()                     │
│  + unregister_component()                   │
│  + get_health_monitor()                     │
│  + get_registered_monitors()                │
│  + clear_monitors()                         │
└─────────────────────────────────────────────┘
                      │
                      ▼
        ┌─────────────────────────────┐
        │   HealthMonitorInterface    │
        └─────────────────────────────┘
                      ▲
                      │
        ┌─────────────────────────────┐
        │      HealthMonitor          │
        └─────────────────────────────┘
```

### Függőségi injektálás

A factory alkalmazza a dependency injection elvet, és csak interfészeken keresztül kommunikál a konkrét implementációkkal:

- **LoggerInterface**: Opcionális naplózó komponens
- **HealthCheckInterface**: Egyedi egészségügyi ellenőrzések

## 🔧 Használat

### Alapvető példa

```python
from neural_ai.core.system import SystemComponentFactory

# HealthMonitor létrehozása
monitor = SystemComponentFactory.create_health_monitor(name="main")

# Komponensek regisztrálása
SystemComponentFactory.register_component(
    monitor_name="main",
    component_name="database"
)

# Egészségügyi állapot ellenőrzése
health = monitor.check_health()
print(f"Rendszer állapota: {health.overall_status.value}")
```

### Logger használata

```python
from neural_ai.core.logger import LoggerFactory
from neural_ai.core.system import SystemComponentFactory

# Logger létrehozása
logger = LoggerFactory.get_logger(name="system")

# HealthMonitor létrehozása loggerrel
monitor = SystemComponentFactory.create_health_monitor(
    name="monitored",
    logger=logger
)

# Komponens regisztrálása
SystemComponentFactory.register_component(
    monitor_name="monitored",
    component_name="storage"
)

# Komponens ellenőrzése
component_health = monitor.check_component("storage")
print(f"Storage állapota: {component_health.status.value}")
```

### Egyedi HealthCheck használata

```python
from neural_ai.core.system import SystemComponentFactory
from neural_ai.core.system.interfaces.health_interface import (
    ComponentHealth,
    ComponentStatus,
    HealthCheckInterface,
)
from datetime import datetime

# Egyedi HealthCheck implementáció
class DatabaseHealthCheck(HealthCheckInterface):
    def check(self) -> ComponentHealth:
        # Adatbázis kapcsolat ellenőrzése
        is_healthy = self._check_database_connection()
        
        return ComponentHealth(
            name="database",
            status=ComponentStatus.HEALTHY if is_healthy else ComponentStatus.CRITICAL,
            message="Adatbázis kapcsolat ellenőrizve" if is_healthy else "Adatbázis nem elérhető",
            timestamp=datetime.now(),
        )
    
    def get_name(self) -> str:
        return "database"
    
    def _check_database_connection(self) -> bool:
        # Implementáció
        return True

# Monitor és egyedi ellenőrzés létrehozása
monitor = SystemComponentFactory.create_health_monitor(name="custom")
custom_check = DatabaseHealthCheck()

SystemComponentFactory.register_component(
    monitor_name="custom",
    component_name="database",
    health_check=custom_check
)
```

### Több monitor kezelése

```python
from neural_ai.core.system import SystemComponentFactory

# Több monitor létrehozása
main_monitor = SystemComponentFactory.create_health_monitor(name="main")
backup_monitor = SystemComponentFactory.create_health_monitor(name="backup")

# Komponensek regisztrálása különböző monitorokhoz
SystemComponentFactory.register_component("main", "database")
SystemComponentFactory.register_component("backup", "storage")

# Monitorok listázása
monitors = SystemComponentFactory.get_registered_monitors()
print(f"Regisztrált monitorok: {monitors}")

# Monitor lekérdezése név alapján
retrieved_monitor = SystemComponentFactory.get_health_monitor("main")
if retrieved_monitor:
    health = retrieved_monitor.check_health()
    print(f"Main monitor állapota: {health.overall_status.value}")
```

## 📝 API Referencia

### Osztály metódusok

#### `create_health_monitor(name, logger, **kwargs)`

HealthMonitor példány létrehozása vagy visszaadása.

**Paraméterek:**
- `name` (str, alapértelmezett: "default"): A HealthMonitor egyedi neve
- `logger` (LoggerInterface | None, opcionális): Logger interfész
- `**kwargs`: További paraméterek a HealthMonitor konstruktorának

**Visszatérési érték:**
- `HealthMonitorInterface`: Az inicializált HealthMonitor példány

**Példa:**
```python
monitor = SystemComponentFactory.create_health_monitor(
    name="main",
    logger=logger
)
```

#### `create_health_check(component_name, logger, health_check_type, **kwargs)`

HealthCheck példány létrehozása.

**Paraméterek:**
- `component_name` (str): A komponens neve
- `logger` (LoggerInterface | None, opcionális): Logger interfész
- `health_check_type` (str, alapértelmezett: "default"): Az ellenőrzés típusa
- `**kwargs`: További paraméterek

**Visszatérési érték:**
- `HealthCheckInterface`: Az inicializált HealthCheck példány

**Kivételek:**
- `ValueError`: Ha ismeretlen health_check_type van megadva

**Példa:**
```python
check = SystemComponentFactory.create_health_check(
    component_name="database",
    logger=logger
)
```

#### `register_component(monitor_name, component_name, health_check)`

Komponens regisztrálása a HealthMonitor-ban.

**Paraméterek:**
- `monitor_name` (str): A HealthMonitor neve
- `component_name` (str): A regisztrálandó komponens neve
- `health_check` (HealthCheckInterface | None, opcionális): Egyedi HealthCheck

**Kivételek:**
- `ValueError`: Ha a megadott monitor_name nem létezik

**Példa:**
```python
SystemComponentFactory.register_component(
    monitor_name="main",
    component_name="database"
)
```

#### `unregister_component(monitor_name, component_name)`

Komponens eltávolítása a HealthMonitor-ból.

**Paraméterek:**
- `monitor_name` (str): A HealthMonitor neve
- `component_name` (str): Az eltávolítandó komponens neve

**Kivételek:**
- `ValueError`: Ha a megadott monitor_name nem létezik

**Példa:**
```python
SystemComponentFactory.unregister_component("main", "database")
```

#### `get_health_monitor(name)`

HealthMonitor lekérdezése név alapján.

**Paraméterek:**
- `name` (str): A HealthMonitor neve

**Visszatérési érték:**
- `HealthMonitorInterface | None`: A HealthMonitor példány, ha létezik

**Példa:**
```python
monitor = SystemComponentFactory.get_health_monitor("main")
```

#### `get_registered_monitors()`

Regisztrált monitorok listázása.

**Visszatérési érték:**
- `list[str]`: A regisztrált monitorok neveinek listája

**Példa:**
```python
monitors = SystemComponentFactory.get_registered_monitors()
```

#### `clear_monitors()`

Összes HealthMonitor törlése a gyorsítótárból.

**Példa:**
```python
SystemComponentFactory.clear_monitors()
```

## 🐛 Hibakezelés

### Nem létező monitor kezelése

```python
try:
    SystemComponentFactory.register_component("nonexistent", "database")
except ValueError as e:
    print(f"Hiba: {e}")
    # Kimenet: Hiba: A 'nonexistent' HealthMonitor nem létezik
```

### Érvénytelen HealthCheck típus

```python
try:
    check = SystemComponentFactory.create_health_check(
        component_name="test",
        health_check_type="invalid"
    )
except ValueError as e:
    print(f"Hiba: {e}")
    # Kimenet: Hiba: Ismeretlen health check típus: invalid
```

### Komponens ellenőrzése hiba esetén

```python
monitor = SystemComponentFactory.create_health_monitor("test")
SystemComponentFactory.register_component("test", "database")

try:
    health = monitor.check_component("database")
    print(f"Komponens állapota: {health.status.value}")
except ValueError as e:
    print(f"Hiba a komponens ellenőrzésénél: {e}")
```

## 🔍 Tesztelés

A factory-t kiterjedten teszteltük a `tests/core/system/test_factory.py` fájlban. A tesztek lefedik:

- Alapvető létrehozási funkcionalitás
- Logger integráció
- Komponens regisztráció és eltávolítás
- Egyedi HealthCheck használata
- Integrációs tesztek
- Rendszer metrikák gyűjtése

### Teszt futtatása

```bash
# Teljes tesztcsomag
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/core/system/test_factory.py -v

# Coverage report-pal
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/core/system/test_factory.py --cov=neural_ai.core.system.factory --cov-report=term-missing
```

### Coverage eredmények

- **Statement Coverage**: 98%
- **Branch Coverage**: 100%

## 📚 Kapcsolódó dokumentáció

- [HealthMonitor implementáció](implementations/health_monitor.md)
- [HealthInterface definíció](interfaces/health_interface.md)
- [Architektúra szabványok](../../development/architecture_standards.md)