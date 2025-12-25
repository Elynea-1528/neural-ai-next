# Core Component Factory

## Áttekintés

Ez a modul biztosítja a core komponensek (config, logger, storage) létrehozását és kezelését dependency injection pattern használatával. A factory támogatja a lazy loadinget, bootstrap inicializálást és NullObject pattern-t fallback-ként.

## Osztályok

### `CoreComponentFactory`

**Hely:** [`neural_ai.core.base.factory:27`](neural_ai/core/base/factory.py:27)

Singleton osztály, amely a core komponensek egységes létrehozásáért és kezeléséért felelős.

#### Attribútumok

- `_container: DIContainer` - A dependency injection konténer
- `_logger_loader: LazyLoader` - Lazy loader a logger komponenshez
- `_config_loader: LazyLoader` - Lazy loader a config manager komponenshez
- `_storage_loader: LazyLoader` - Lazy loader a storage komponenshez

#### Metódusok

##### `__init__(container: DIContainer)`
Inicializálja a factory-t lazy-loaded függőségekkel.

**Paraméterek:**
- `container`: A dependency injection konténer

##### `logger` property
Visszaadja a logger példányt (lazy-loaded).

**Visszatérési érték:** `LoggerInterface`

##### `config_manager` property
Visszaadja a config manager példányt (lazy-loaded).

**Visszatérési érték:** `ConfigManagerInterface`

##### `storage` property
Visszaadja a storage példányt (lazy-loaded).

**Visszatérési érték:** `StorageInterface`

##### `reset_lazy_loaders() -> None`
Visszaállítja az összes lazy loader állapotát. Hasznos tesztelés során vagy újrainicializáláskor.

##### `create_components(config_path, log_path, storage_path) -> CoreComponents` (static)
Core komponensek létrehozása és inicializálása.

**Paraméterek:**
- `config_path: str | Path | None` - A konfigurációs fájl elérési útja (opcionális)
- `log_path: str | Path | None` - A log fájl elérési útja (opcionális)
- `storage_path: str | Path | None` - A tároló alapkönyvtára (opcionális)

**Visszatérési érték:** `CoreComponents` - Az inicializált core komponensek gyűjteménye

**Kivételek:**
- `ConfigurationError`: Ha a konfiguráció érvénytelen
- `DependencyError`: Ha szükséges függőségek hiányoznak

**Példa:**
```python
from neural_ai.core.base import CoreComponentFactory

# Komponensek létrehozása
components = CoreComponentFactory.create_components(
    config_path="config.yml",
    log_path="logs/app.log",
    storage_path="data/"
)

# Komponensek használata
logger = components.logger
config = components.config
storage = components.storage
```

##### `create_with_container(container) -> CoreComponents` (static)
Core komponensek létrehozása meglévő konténerből.

**Paraméterek:**
- `container: DIContainer` - A DI konténer, amely tartalmazza a komponenseket

**Visszatérési érték:** `CoreComponents`

##### `create_minimal() -> CoreComponents` (static)
Minimális core komponens készlet létrehozása alapértelmezett beállításokkal.

**Visszatérési érték:** `CoreComponents`

##### `create_logger(name, config) -> LoggerInterface` (static)
Logger példány létrehozása.

**Paraméterek:**
- `name: str` - A logger neve
- `config: dict[str, Any] | None` - Konfigurációs dictionary (opcionális)

**Visszatérési érték:** `LoggerInterface`

**Kivételek:**
- `ConfigurationError`: Ha a konfiguráció érvénytelen
- `DependencyError`: Ha szükséges függőségek hiányoznak

##### `create_config_manager(config_file_path, config) -> ConfigManagerInterface` (static)
Config manager példány létrehozása.

**Paraméterek:**
- `config_file_path: str` - A konfigurációs fájl elérési útja
- `config: dict[str, Any] | None` - Konfigurációs dictionary

**Visszatérési érték:** `ConfigManagerInterface`

**Kivételek:**
- `ConfigurationError`: Ha a konfiguráció érvénytelen
- `DependencyError`: Ha szükséges függőségek hiányoznak

##### `create_storage(base_directory, config) -> StorageInterface` (static)
Storage példány létrehozása.

**Paraméterek:**
- `base_directory: str` - A tároló alapkönyvtára
- `config: dict[str, Any] | None` - Konfigurációs dictionary

**Visszatérési érték:** `StorageInterface`

**Kivételek:**
- `ConfigurationError`: Ha a konfiguráció érvénytelen
- `DependencyError`: Ha szükséges függőségek hiányoznak

## Lazy Loading

A factory lazy loading technikát használ a komponensek betöltéséhez:

- `_expensive_config`: Drága konfiguráció lusta betöltése
- `_component_cache`: Komponens gyorsítótár lusta betöltése

## NullObject Pattern

Ha a logger komponens nem érhető el, a factory visszaad egy `DefaultLogger` példányt, amely implementálja a NullObject pattern-t.

## Függőségek

- `neural_ai.core.base.implementations.di_container.DIContainer`
- `neural_ai.core.base.implementations.lazy_loader.LazyLoader`
- `neural_ai.core.base.implementations.singleton.SingletonMeta`
- `neural_ai.core.base.exceptions.ConfigurationError`
- `neural_ai.core.base.exceptions.DependencyError`

## Kapcsolódó dokumentáció

- [Core Components](neural_ai/core/base/implementations/component_bundle.md)
- [DI Container](neural_ai/core/base/implementations/di_container.md)
- [Lazy Loader](neural_ai/core/base/implementations/lazy_loader.md)
- [Singleton](neural_ai/core/base/implementations/singleton.md)