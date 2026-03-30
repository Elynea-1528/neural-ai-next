# neural_ai/core/__init__.py

Neural-AI-Next core komponensek inicializációs modul.

Ez a modul a rendszer alapvető infrastrukturális komponenseit tartalmazza:
- Logger rendszer
- Konfiguráció kezelés
- Adattárolás
- Rendszer monitorozás

A modul biztosítja a core komponensek megfelelő inicializálását és
függőségi injektálását, elkerülve a körkörös függőségeket.

## Importok

```python
from typing import TYPE_CHECKING
from typing import Any
from typing import cast
from neural_ai.core.config.interfaces.types import IngestionConfig
from neural_ai.core.config.interfaces.types import JForexLiveConfig
from neural_ai.core.config.interfaces.types import LoggingConfig
from neural_ai.core.config.interfaces.types import StorageConfig
from neural_ai.core.utils.decorators import trace
from neural_ai.core.base.implementations.component_bundle import CoreComponents
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
# ... és még 26 import
```

## Konstansok

- **`container`**
: `DIContainer()`


- **`path_to_load`**
: `config_path if config_path else 'configs'`


- **`config`**
: `ConfigManagerFactory.create_manager('yaml')`


- **`logging_config_dict`**
: `config.get_section('logging') or {}`


- **`logging_config`**
: `LoggingConfig(**logging_config_dict)`


- **`logger`**
: `LoggerFactory.get_logger(__name__, logger_type='default')`


- **`hardware`**
: `HardwareFactory.get_hardware_info()`


- **`db_factory`**
: `DatabaseFactory(logger=logger, config_manager=config)`


- **`database`**
: `db_factory.create_manager()`


- **`event_bus_factory`**
: `EventBusFactory(logger, config)`


- **`event_bus`**
: `event_bus_factory.create_from_config()`


- **`storage_conf_dict`**
: `cast(dict[str, Any], config.get('storage') or {})`


- **`storage_conf`**
: `StorageConfig(**storage_conf_dict)`


- **`storage_type`**
: `storage_conf.type or 'parquet'`


- **`storage`**
: `StorageFactory.get_storage(storage_type=storage_type, base_path=storage_conf.base_path, logger=logger, config=config, hardware=hardware)`


- **`health_monitor`**
: `SystemComponentFactory.create_health_monitor(name='core', logger=logger)`


- **`ingestion_dict`**
: `config.get_section('ingestion') or {}`


- **`valid_fields`**
: `{'buffer_size_limit', 'flush_interval_minutes'}`


- **`filtered_dict`**
: `{k: v for k, v in ingestion_dict.items() if k in valid_fields}`


- **`ingestion_config`**
: `IngestionConfig(**filtered_dict) if filtered_dict else IngestionConfig(buffer_size_limit=None, flush_interval_minutes=None)`


- **`market_data_persister`**
: `MarketDataPersister(event_bus=event_bus, storage=storage, logger=logger, config=ingestion_config)`


- **`live_conf_dict`**
: `cast(dict[str, Any], config.get('collectors', 'jforex_live') or {})`


- **`live_conf`**
: `JForexLiveConfig(**live_conf_dict)`


- **`live_feed`**
: `JForexFactory.create_live_feed(config, logger, event_bus)`


- **`_core_components_instance`**
: `bootstrap_core()`


- **`__all__`**
: `['bootstrap_core', 'get_core_components', 'get_version', 'get_schema_version', 'ConfigManagerInterface', 'DatabaseManager', 'EventBusInterface', 'LoggerInterface', 'HealthMonitorInterface', 'HardwareInterface']`


### `get_version()`

```python
def get_version() -> str
```

Dynamikusan betölti a csomag verzióját.

**Visszatérési érték:**

- Típus: `str`
- A csomag verziója stringként. Ha a verzió nem érhető el, 'unknown' értékkel tér vissza.

### `get_schema_version()`

```python
def get_schema_version() -> str
```

Visszaadja az aktuális séma verziót.

**Visszatérési érték:**

- Típus: `str`
- Az aktuális séma verziója stringként.

### `bootstrap_core()`

```python
def bootstrap_core(config_path: str | None = None, log_level: str | None = None) -> 'CoreComponents'
```

Bootstrap funkció a core komponensek inicializálásához. Ez a függvény biztosítja a core komponensek megfelelő sorrendű inicializálását, elkerülve a körkörös függőségeket. A bootstrap folyamat: 1. HardwareFactory - Hardver információk lekérdezése 2. ConfigFactory - Konfiguráció betöltése 3. LoggerFactory - Logger inicializálása a konfiguráció alapján 4. DatabaseFactory - Adatbázis kapcsolat létrehozása (Config+Logger) 5. EventBusFactory - Esemény busz inicializálása (Config+Logger) 6. StorageFactory - Tárhely inicializálása (Config+Logger+HardwareInfo) 7. SystemFactory - Rendszer monitorozás (Config+Logger)

**Paraméterek:**

- **`config_path`** (`str | None`) = `None`: Opcionális konfigurációs fájl útvonala. Ha None, akkor a 'configs' könyvtárat tölti be.
- **`log_level`** (`str | None`) = `None`: Opcionális log szint beállítás. Ha None, akkor a konfigurációból olvassa ki.

**Visszatérési érték:**

- Típus: `'CoreComponents'`
- A teljesen inicializált CoreComponents példány

**Kivételek:**

- **`ConfigError`**: Ha a konfiguráció betöltése sikertelen
- **`LoggerError`**: Ha a logger inicializálása sikertelen
- **`DatabaseError`**: Ha az adatbázis kapcsolat létrehozása sikertelen

**Példák:**

```python
    >>> core = bootstrap_core()
    >>> core.logger.info("Alkalmazás elindult")
    >>> await core.database.initialize()
    >>> await core.event_bus.start()
```

### `get_core_components()`

```python
def get_core_components() -> 'CoreComponents'
```

Globális core komponensek lekérdezése. Ez a függvény egy szingleton példányt ad vissza a core komponensekből, biztosítva, hogy az alkalmazás egészében ugyanazok a komponensek legyenek elérhetőek.

**Visszatérési érték:**

- Típus: `'CoreComponents'`
- A globális CoreComponents példány

**Példák:**

```python
    >>> core = get_core_components()
    >>> core.logger.info("Komponens használatban")
```

---

**Forrásfájl:** [`neural_ai/core/__init__.py`](../../neural_ai/core/__init__.py)
