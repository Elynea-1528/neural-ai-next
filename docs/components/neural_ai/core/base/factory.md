# CoreComponentFactory

## Áttekintés

A `CoreComponentFactory` osztály a core komponensek (config, logger, storage) létrehozásáért és kezeléséért felelős factory, amely a dependency injection (DI) mintát használja. Singleton minta alkalmazásával biztosítja, hogy csak egy példány létezzen, és lazy loading technikával optimalizálja a teljesítményt.

## Jellemzők

- **Singleton Pattern**: Csak egy példány létezik a rendszerben
- **Lazy Loading**: A komponensek csak akkor töltődnek be, amikor először használják őket
- **Dependency Injection**: A függőségeket a konstruktorban injektálja
- **NullObject Pattern**: Fallback implementáció hiányzó komponensek esetén
- **Bootstrap Támogatás**: Többféle inicializálási módot támogat

## Osztály Struktúra

```python
class CoreComponentFactory(metaclass=SingletonMeta):
    """Core komponensek létrehozásáért felelős factory lazy loadinggel."""
    
    def __init__(self, container: DIContainer):
        """Inicializálja a factory-t lazy-loaded függőségekkel."""
        
    @property
    def logger(self) -> "LoggerInterface":
        """Visszaadja a logger példányt (lazy-loaded)."""
        
    @property
    def config_manager(self) -> "ConfigManagerInterface":
        """Visszaadja a config manager példányt (lazy-loaded)."""
        
    @property
    def storage(self) -> "StorageInterface":
        """Visszaadja a storage példányt (lazy-loaded)."""
```

## Metódusok

### Inicializálás

#### `__init__(container: DIContainer)`

A factory inicializálása dependency injection konténerrel.

**Paraméterek:**
- `container`: A DI konténer, amely tartalmazza a komponenseket

**Példa:**
```python
container = DIContainer()
factory = CoreComponentFactory(container)
```

### Lazy Loading Property-k

#### `logger`
Lazy-loaded logger komponens. Csak akkor töltődik be, amikor először hivatkoznak rá.

**Visszatérési érték:** `LoggerInterface`

#### `config_manager`
Lazy-loaded config manager komponens. Csak akkor töltődik be, amikor először hivatkoznak rá.

**Visszatérési érték:** `ConfigManagerInterface`

#### `storage`
Lazy-loaded storage komponens. Csak akkor töltődik be, amikor először hivatkoznak rá.

**Visszatérési érték:** `StorageInterface`

### Statikus Factory Metódusok

#### `create_components(config_path, log_path, storage_path)`

Core komponensek létrehozása és inicializálása elérési utak alapján.

**Paraméterek:**
- `config_path` (str | Path | None): A konfigurációs fájl elérési útja
- `log_path` (str | Path | None): A log fájl elérési útja
- `storage_path` (str | Path | None): A tároló alapkönyvtára

**Visszatérési érték:** `CoreComponents`

**Példa:**
```python
components = CoreComponentFactory.create_components(
    config_path="config.yml",
    log_path="app.log",
    storage_path="/tmp/storage"
)
```

#### `create_with_container(container)`

Core komponensek létrehozása meglévő konténerből.

**Paraméterek:**
- `container` (DIContainer): A DI konténer

**Visszatérési érték:** `CoreComponents`

**Példa:**
```python
container = DIContainer()
# ... regisztráljuk a komponenseket
components = CoreComponentFactory.create_with_container(container)
```

#### `create_minimal()`

Minimális core komponens készlet létrehozása alapértelmezett beállításokkal.

**Visszatérési érték:** `CoreComponents`

**Példa:**
```python
components = CoreComponentFactory.create_minimal()
```

### Komponens Létrehozó Metódusok

#### `create_logger(name, config)`

Logger példány létrehozása.

**Paraméterek:**
- `name` (str): A logger neve
- `config` (dict[str, Any] | None): Konfigurációs dictionary

**Visszatérési érték:** `LoggerInterface`

**Példa:**
```python
logger = CoreComponentFactory.create_logger(
    name="my_logger",
    config={"level": "INFO"}
)
```

#### `create_config_manager(config_file_path, config)`

Config manager példány létrehozása.

**Paraméterek:**
- `config_file_path` (str): A konfigurációs fájl elérési útja
- `config` (dict[str, Any] | None): Konfigurációs dictionary

**Visszatérési érték:** `ConfigManagerInterface`

**Példa:**
```python
config_manager = CoreComponentFactory.create_config_manager(
    config_file_path="config.yml"
)
```

#### `create_storage(base_directory, config)`

Storage példány létrehozása.

**Paraméterek:**
- `base_directory` (str): A tároló alapkönyvtára
- `config` (dict[str, Any] | None): Konfigurációs dictionary

**Visszatérési érték:** `StorageInterface`

**Példa:**
```python
storage = CoreComponentFactory.create_storage(
    base_directory="/tmp/storage"
)
```

### Helper Metódusok

#### `reset_lazy_loaders()`

Visszaállítja az összes lazy loader állapotát. Hasznos tesztelés során.

**Példa:**
```python
factory.reset_lazy_loaders()
```

#### `_validate_dependencies(component_type, config)`

Ellenőrzi, hogy minden szükséges függőség elérhető-e.

**Paraméterek:**
- `component_type` (str): A létrehozandó komponens típusa
- `config` (dict[str, Any] | None): Konfigurációs dictionary

**Kivételek:**
- `ConfigurationError`: Ha a konfiguráció érvénytelen vagy hiányzik
- `DependencyError`: Ha szükséges függőségek nem érhetők el

## Lazy Loading

A factory lazy loadinget használ a komponensek betöltéséhez:

```python
# A logger csak itt töltődik be először
logger = factory.logger
logger.info("Ez az első használat")
```

### Lazy Property-k

A factory támogatja a lazy property-ket is:

```python
@lazy_property
def _expensive_config(self) -> dict[str, Any]:
    """Lazy loadinggel tölti be a drága konfigurációt."""
    config = self.config_manager.get()
    time.sleep(1)  # Szimulált drága művelet
    return self._process_config(config)
```

## Függőségi Injektálás

A factory a DI mintát követi:

```python
class CoreComponentFactory:
    def __init__(self, container: DIContainer):
        self._container = container
        self._logger_loader = LazyLoader(self._get_logger)
        # ...
```

## NullObject Pattern

Hiányzó komponensek esetén a factory NullObject pattern-t használ:

```python
def _get_logger(self) -> "LoggerInterface":
    logger = self._container.resolve(LoggerInterface)
    if logger is not None:
        return logger
    
    # Fallback to default logger (NullObject pattern)
    from neural_ai.core.logger.implementations.default_logger import DefaultLogger
    return DefaultLogger(name="CoreComponentFactory")
```

## Bootstrap Folyamat

A factory többféle inicializálási módot támogat:

### 1. Teljes Inicializálás

```python
components = CoreComponentFactory.create_components(
    config_path="config.yml",
    log_path="app.log",
    storage_path="/tmp/storage"
)
```

### 2. Meglévő Konténerrel

```python
container = DIContainer()
# Regisztráljuk a komponenseket
container.register_instance(LoggerInterface, logger)
container.register_instance(ConfigManagerInterface, config)
container.register_instance(StorageInterface, storage)

components = CoreComponentFactory.create_with_container(container)
```

### 3. Minimális Készlet

```python
components = CoreComponentFactory.create_minimal()
```

## Hibakezelés

A factory a következő kivételeket dobhatja:

- `ConfigurationError`: Konfigurációs hiba esetén
- `DependencyError`: Függőségi hiba esetén

**Példa hibakezelésre:**
```python
try:
    components = CoreComponentFactory.create_components(
        config_path="config.yml"
    )
except ConfigurationError as e:
    print(f"Konfigurációs hiba: {e}")
except DependencyError as e:
    print(f"Függőségi hiba: {e}")
```

## Teljesítményoptimalizálás

A factory a következő optimalizálásokat használja:

1. **Lazy Loading**: A komponensek csak akkor töltődnek be, amikor szükség van rájuk
2. **Singleton Pattern**: Csak egy példány létezik
3. **Lazy Property-k**: Drága műveletek csak egyszer hajtódnak végre
4. **Thread Safety**: A lazy loading szálbiztos

## Tesztelés

A factory-t a `tests/core/base/test_factory.py` fájl teszteli.

**Fontosabb tesztesetek:**
- Inicializálás és lazy loading
- Függőség ellenőrzés
- Komponens létrehozás
- Hibakezelés
- Lazy loader reset

## Kapcsolódó Komponensek

- [`DIContainer`](container.md): Dependency injection konténer
- [`LazyLoader`](lazy_loading.md): Lazy loading implementáció
- [`CoreComponents`](core_components.md): Core komponensek gyűjteménye
- [`ConfigManagerInterface`](../config/interfaces/config_interface.md): Konfiguráció kezelő interface
- [`LoggerInterface`](../logger/interfaces/logger_interface.md): Logger interface
- [`StorageInterface`](../storage/interfaces/storage_interface.md): Tároló interface

## Használati Példák

### Alap Használat

```python
from neural_ai.core.base.factory import CoreComponentFactory
from neural_ai.core.base.container import DIContainer

# Konténer létrehozása
container = DIContainer()

# Factory létrehozása
factory = CoreComponentFactory(container)

# Komponensek használata (lazy-loaded)
logger = factory.logger
config = factory.config_manager
storage = factory.storage

# Naplózás
logger.info("Alkalmazás indítása")
```

### Teljes Inicializálás

```python
from neural_ai.core.base.factory import CoreComponentFactory

# Komponensek létrehozása
components = CoreComponentFactory.create_components(
    config_path="config.yml",
    log_path="app.log",
    storage_path="/tmp/storage"
)

# Komponensek használata
logger = components.logger
config = components.config
storage = components.storage
```

### Egyéni Konfigurációval

```python
from neural_ai.core.base.factory import CoreComponentFactory

# Logger létrehozása egyéni konfigurációval
logger = CoreComponentFactory.create_logger(
    name="my_app",
    config={
        "level": "DEBUG",
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    }
)

# Config manager létrehozása
config_manager = CoreComponentFactory.create_config_manager(
    config_file_path="my_config.yml"
)

# Storage létrehozása
storage = CoreComponentFactory.create_storage(
    base_directory="/custom/storage/path"
)
```

### Teszteléshez

```python
import pytest
from neural_ai.core.base.factory import CoreComponentFactory
from neural_ai.core.base.container import DIContainer

def test_factory():
    # Konténer létrehozása
    container = DIContainer()
    factory = CoreComponentFactory(container)
    
    # Tesztelés
    assert factory._container == container
    
    # Lazy loader reset teszteléshez
    factory.reset_lazy_loaders()
```

## Jövőbeli Fejlesztések

- **Plugin Rendszer**: Dinamikusan cserélhető implementációk
- **Metrikák és Monitorozás**: Függőségi gráf vizualizáció
- **Életciklus Management**: Komponensek életciklusának kezelése
- **Scope Kezelés**: Különböző scope-ok támogatása (request, session, stb.)