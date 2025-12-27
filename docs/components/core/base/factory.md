# CoreComponentFactory

A [`CoreComponentFactory`](neural_ai/core/base/factory.py:27) egy singleton factory osztály, amely a core komponensek (config, logger, storage) létrehozásáért és kezeléséért felelős. A factory támogatja a dependency injection pattern-t, lazy loadinget, bootstrap inicializálást és NullObject pattern-t fallback-ként.

## Osztálystruktúra

```python
class CoreComponentFactory(metaclass=SingletonMeta):
    """Core komponensek létrehozásáért felelős factory lazy loadinggel."""
```

## Főbb jellemzők

- **Singleton minta**: Csak egy példány létezik a rendszerben
- **Lazy loading**: A komponensek csak akkor jönnek létre, amikor először használják őket
- **Dependency Injection**: A függőségeket konténeren keresztül injektálja
- **NullObject pattern**: Fallback implementáció hiányzó komponensek esetén

## Attribútumok

- `_container`: A dependency injection konténer
- `_logger_loader`: Lazy loader a logger komponenshez
- `_config_loader`: Lazy loader a config manager komponenshez
- `_storage_loader`: Lazy loader a storage komponenshez

## Metódusok

### Inicializálás

```python
def __init__(self, container: DIContainer) -> None:
    """Inicializálja a factory-t lazy-loaded függőségekkel."""
```

### Property-k (Lazy-loaded)

#### `logger`
```python
@property
def logger(self) -> "LoggerInterface":
    """Visszaadja a logger példányt (lazy-loaded)."""
```
- **Visszatérési érték**: [`LoggerInterface`](neural_ai/core/logger/interfaces/logger_interface.py:1)
- **Leírás**: Visszaadja a logger komponenst. Ha nincs regisztrálva, alapértelmezett loggerrel tér vissza (NullObject pattern).

#### `config_manager`
```python
@property
def config_manager(self) -> "ConfigManagerInterface":
    """Visszaadja a config manager példányt (lazy-loaded)."""
```
- **Visszatérési érték**: [`ConfigManagerInterface`](neural_ai/core/config/interfaces/config_interface.py:1)
- **Kivételek**: `DependencyError` - ha a config manager nem érhető el

#### `storage`
```python
@property
def storage(self) -> "StorageInterface":
    """Visszaadja a storage példányt (lazy-loaded)."""
```
- **Visszatérési érték**: [`StorageInterface`](neural_ai/core/storage/interfaces/storage_interface.py:1)
- **Kivételek**: `DependencyError` - ha a storage nem érhető el

### Statikus factory metódusok

#### `create_components`
```python
@staticmethod
def create_components(
    config_path: str | Path | None = None,
    log_path: str | Path | None = None,
    storage_path: str | Path | None = None,
) -> "CoreComponents":
```
- **Paraméterek**:
  - `config_path`: A konfigurációs fájl elérési útja (opcionális)
  - `log_path`: A log fájl elérési útja (opcionális)
  - `storage_path`: A tároló alapkönyvtára (opcionális)
- **Visszatérési érték**: [`CoreComponents`](neural_ai/core/base/implementations/component_bundle.py:77)
- **Kivételek**: `ConfigurationError`, `DependencyError`
- **Leírás**: Létrehozza és inicializálja az összes core komponenst lazy loadinggel.

#### `create_with_container`
```python
@staticmethod
def create_with_container(container: DIContainer) -> "CoreComponents":
```
- **Paraméterek**:
  - `container`: A DI konténer, amely tartalmazza a komponenseket
- **Visszatérési érték**: [`CoreComponents`](neural_ai/core/base/implementations/component_bundle.py:77)
- **Leírás**: Core komponensek létrehozása meglévő konténerből.

#### `create_minimal`
```python
@staticmethod
def create_minimal() -> "CoreComponents":
```
- **Visszatérési érték**: [`CoreComponents`](neural_ai/core/base/implementations/component_bundle.py:77)
- **Leírás**: Minimális core komponens készlet létrehozása alapértelmezett beállításokkal.

#### `create_logger`
```python
@staticmethod
def create_logger(name: str, config: dict[str, Any] | None = None) -> "LoggerInterface":
```
- **Paraméterek**:
  - `name`: A logger neve
  - `config`: Konfigurációs dictionary (opcionális)
- **Visszatérési érték**: [`LoggerInterface`](neural_ai/core/logger/interfaces/logger_interface.py:1)
- **Kivételek**: `ConfigurationError`, `DependencyError`

#### `create_config_manager`
```python
@staticmethod
def create_config_manager(
    config_file_path: str, 
    config: dict[str, Any] | None = None
) -> "ConfigManagerInterface":
```
- **Paraméterek**:
  - `config_file_path`: A konfigurációs fájl elérési útja
  - `config`: Konfigurációs dictionary
- **Visszatérési érték**: [`ConfigManagerInterface`](neural_ai/core/config/interfaces/config_interface.py:1)
- **Kivételek**: `ConfigurationError`, `DependencyError`

#### `create_storage`
```python
@staticmethod
def create_storage(
    base_directory: str, 
    config: dict[str, Any] | None = None
) -> "StorageInterface":
```
- **Paraméterek**:
  - `base_directory`: A tároló alapkönyvtára
  - `config`: Konfigurációs dictionary
- **Visszatérési érték**: [`StorageInterface`](neural_ai/core/storage/interfaces/storage_interface.py:1)
- **Kivételek**: `ConfigurationError`, `DependencyError`

### Helper metódusok

#### `reset_lazy_loaders`
```python
def reset_lazy_loaders(self) -> None:
    """Visszaállítja az összes lazy loadert."""
```
- **Leírás**: Visszaállítja az összes lazy loader állapotát. Hasznos tesztelés során vagy újrainicializáláskor.

#### `_validate_dependencies`
```python
@staticmethod
def _validate_dependencies(
    component_type: str, 
    config: dict[str, Any] | None = None
) -> None:
```
- **Paraméterek**:
  - `component_type`: A létrehozandó komponens típusa
  - `config`: Konfigurációs dictionary
- **Kivételek**: `ConfigurationError`, `DependencyError`
- **Leírás**: Ellenőrzi, hogy minden szükséges függőség elérhető-e.

## Lazy Property-k

#### `_expensive_config`
```python
@lazy_property
def _expensive_config(self) -> dict[str, Any]:
    """Lazy loadinggel tölti be a drága konfigurációt."""
```
- **Leírás**: Drága konfiguráció lusta betöltése. Csak egyszer számolódik ki.

#### `_component_cache`
```python
@lazy_property
def _component_cache(self) -> dict[str, Any]:
    """Lazy loadinggel tölti be a komponens gyorsítótárát."""
```
- **Leírás**: Komponens gyorsítótár lusta betöltése. Csak egyszer töltődik be.

## Használati példák

### Alap inicializálás

```python
from neural_ai.core.base.factory import CoreComponentFactory
from neural_ai.core.base.implementations.di_container import DIContainer

# Konténer létrehozása
container = DIContainer()

# Factory inicializálása
factory = CoreComponentFactory(container)

# Komponensek használata
logger = factory.logger
logger.info("Hello from CoreComponentFactory!")
```

### Komponensek létrehozása elérési utakkal

```python
from neural_ai.core.base.factory import CoreComponentFactory

# Komponensek létrehozása
components = CoreComponentFactory.create_components(
    config_path="config.yml",
    log_path="app.log",
    storage_path="./data"
)

# Komponensek használata
if components.has_logger():
    components.logger.info("Components created successfully!")
```

### Logger létrehozása

```python
from neural_ai.core.base.factory import CoreComponentFactory

# Logger létrehozása
logger = CoreComponentFactory.create_logger(
    name="my_app",
    config={"level": "INFO", "format": "%(levelname)s: %(message)s"}
)

logger.info("Application started")
```

### Storage létrehozása

```python
from neural_ai.core.base.factory import CoreComponentFactory

# Storage létrehozása
storage = CoreComponentFactory.create_storage(
    base_directory="./data",
    config={"auto_create": True}
)

# DataFrame mentése
import pandas as pd
df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
storage.save_dataframe(df, "test.csv")
```

## Tesztelés

A modulhoz 27 egységteszt tartozik, amelyek 94% kódlefedettséget érnek el. A tesztek a [`tests/core/base/test_factory.py`](tests/core/base/test_factory.py:1) fájlban találhatók.

### Tesztfuttatás

```bash
# Összes teszt futtatása
pytest tests/core/base/test_factory.py -v

# Coverage jelentéssel
pytest tests/core/base/test_factory.py --cov=neural_ai.core.base.factory --cov-report=term-missing
```

## Kapcsolódó dokumentáció

- [`CoreComponents`](neural_ai/core/base/implementations/component_bundle.py:77) - A core komponensek gyűjteménye
- [`DIContainer`](neural_ai/core/base/implementations/di_container.py:57) - Dependency injection konténer
- [`LazyLoader`](neural_ai/core/base/implementations/lazy_loader.py:22) - Lusta betöltő implementáció
- [`LoggerInterface`](neural_ai/core/logger/interfaces/logger_interface.py:1) - Logger interfész
- [`ConfigManagerInterface`](neural_ai/core/config/interfaces/config_interface.py:1) - Config manager interfész
- [`StorageInterface`](neural_ai/core/storage/interfaces/storage_interface.py:1) - Storage interfész

## Hibakezelés

A factory a következő kivételeket dobhatja:

- [`ConfigurationError`](neural_ai/core/base/exceptions/base_error.py:1): Konfigurációs hiba esetén
- [`DependencyError`](neural_ai/core/base/exceptions/base_error.py:1): Függőségi hiba esetén

## Teljesítményoptimalizálás

A factory a következő technikákat használja a teljesítmény optimalizálására:

1. **Lazy Loading**: A komponensek csak akkor jönnek létre, amikor először használják őket
2. **Singleton Pattern**: Csak egy példány létezik a rendszerben
3. **Lazy Property-k**: Drága műveletek csak egyszer hajtódnak végre
4. **Dependency Injection**: A függőségek konténeren keresztül kerülnek injektálásra

## Verziótörténet

- **v1.0**: Alap factory implementáció lazy loadinggel és DI támogatással
- **v2.0**: Típusos visszatérési értékek hozzáadása, Pylance hibák javítása