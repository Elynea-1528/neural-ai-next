# Core Component Factory

## Áttekintés

A `CoreComponentFactory` egy singleton osztály, amely a core komponensek (config, logger, storage) létrehozásáért és kezeléséért felelős. A factory a dependency injection (DI) pattern-t használja, és támogatja a lazy loadinget, bootstrap inicializálást és a NullObject pattern-t fallback-ként.

## Főbb Jellemzők

- **Singleton Pattern**: Biztosítja, hogy csak egy példány létezzen a rendszerben
- **Lazy Loading**: A komponensek csak akkor jönnek létre, amikor először használják őket
- **Dependency Injection**: A függőségeket a konstruktorban injektálja
- **Bootstrap Minta**: Támogatja a komponensek egymás utáni inicializálását
- **NullObject Pattern**: Fallback implementációt biztosít, ha egy komponens nem érhető el

## Osztály Struktúra

```python
class CoreComponentFactory(metaclass=SingletonMeta):
    """Core komponensek létrehozásáért felelős factory lazy loadinggel."""
    
    def __init__(self, container: DIContainer):
        """Inicializálja a factory-t lazy-loaded függőségekkel."""
        
    @property
    def logger(self) -> LoggerInterface:
        """Visszaadja a logger példányt (lazy-loaded)."""
        
    @property
    def config_manager(self) -> ConfigManagerInterface:
        """Visszaadja a config manager példányt (lazy-loaded)."""
        
    @property
    def storage(self) -> StorageInterface:
        """Visszaadja a storage példányt (lazy-loaded)."""
```

## Metódusok

### Inicializálás

#### `__init__(container: DIContainer)`
Inicializálja a factory-t egy DI konténerrel.

**Paraméterek:**
- `container`: A dependency injection konténer, amely tartalmazza a komponenseket

**Példa:**
```python
container = DIContainer()
factory = CoreComponentFactory(container)
```

### Lazy Loading Property-k

#### `logger`
Visszaadja a logger komponenst. Ha még nincs létrehozva, akkor létrehozza.

**Visszatérési érték:** `LoggerInterface`

**Példa:**
```python
logger = factory.logger
logger.info("Ez egy teszt üzenet")
```

#### `config_manager`
Visszaadja a config manager komponenst. Ha még nincs létrehozva, akkor létrehozza.

**Visszatérési érték:** `ConfigManagerInterface`

**Példa:**
```python
config = factory.config_manager
value = config.get("section.key")
```

#### `storage`
Visszaadja a storage komponenst. Ha még nincs létrehozva, akkor létrehozza.

**Visszatérési érték:** `StorageInterface`

**Példa:**
```python
storage = factory.storage
data = storage.read_file("data.txt")
```

### Statikus Factory Metódusok

#### `create_components(config_path, log_path, storage_path)`
Core komponensek létrehozása és inicializálása.

**Paraméterek:**
- `config_path` (opcionális): A konfigurációs fájl elérési útja
- `log_path` (opcionális): A log fájl elérési útja
- `storage_path` (opcionális): A tároló alapkönyvtára

**Visszatérési érték:** `CoreComponents`

**Példa:**
```python
components = CoreComponentFactory.create_components(
    config_path="config.yml",
    log_path="app.log",
    storage_path="/tmp/storage"
)
```

#### `create_minimal()`
Minimális core komponens készlet létrehozása alapértelmezett beállításokkal.

**Visszatérési érték:** `CoreComponents`

**Példa:**
```python
components = CoreComponentFactory.create_minimal()
```

#### `create_with_container(container)`
Core komponensek létrehozása meglévő konténerből.

**Paraméterek:**
- `container`: A DI konténer, amely tartalmazza a komponenseket

**Visszatérési érték:** `CoreComponents`

**Példa:**
```python
container = DIContainer()
# ... regisztráljuk a komponenseket ...
components = CoreComponentFactory.create_with_container(container)
```

### Egyedi Komponens Létrehozása

#### `create_logger(name, config)`
Létrehoz egy logger példányt.

**Paraméterek:**
- `name`: A logger neve
- `config` (opcionális): Konfigurációs dictionary

**Visszatérési érték:** `LoggerInterface`

**Példa:**
```python
logger = CoreComponentFactory.create_logger(
    name="my_logger",
    config={"level": "DEBUG"}
)
```

#### `create_config_manager(config_file_path, config)`
Létrehoz egy config manager példányt.

**Paraméterek:**
- `config_file_path`: A konfigurációs fájl elérési útja
- `config` (opcionális): Konfigurációs dictionary

**Visszatérési érték:** `ConfigManagerInterface`

**Példa:**
```python
config_manager = CoreComponentFactory.create_config_manager(
    config_file_path="config.yml"
)
```

#### `create_storage(base_directory, config)`
Létrehoz egy storage példányt.

**Paraméterek:**
- `base_directory`: A tároló alapkönyvtára
- `config` (opcionális): Konfigurációs dictionary

**Visszatérési érték:** `StorageInterface`

**Példa:**
```python
storage = CoreComponentFactory.create_storage(
    base_directory="/tmp/storage"
)
```

### Egyéb Metódusok

#### `reset_lazy_loaders()`
Visszaállítja az összes lazy loader állapotát. Hasznos tesztelés során.

**Példa:**
```python
factory.reset_lazy_loaders()
```

#### `_validate_dependencies(component_type, config)`
Ellenőrzi, hogy minden szükséges függőség elérhető-e.

**Paraméterek:**
- `component_type`: A létrehozandó komponens típusa
- `config` (opcionális): Konfigurációs dictionary

## Használati Példák

### Alap Használat

```python
from neural_ai.core.base.factory import CoreComponentFactory
from neural_ai.core.base.container import DIContainer

# DI konténer létrehozása
container = DIContainer()

# Factory inicializálása
factory = CoreComponentFactory(container)

# Komponensek használata
logger = factory.logger
config = factory.config_manager
storage = factory.storage

# Naplózás
logger.info("Alkalmazás elindult")
```

### Bootstrap Inicializálás

```python
from neural_ai.core.base.factory import CoreComponentFactory

# Komponensek létrehozása bootstrap módszerrel
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

### Minimális Konfiguráció

```python
from neural_ai.core.base.factory import CoreComponentFactory

# Minimális komponens készlet létrehozása
components = CoreComponentFactory.create_minimal()

# Komponensek használata
logger = components.logger
storage = components.storage
```

### Egyedi Komponens Létrehozása

```python
from neural_ai.core.base.factory import CoreComponentFactory

# Egyedi logger létrehozása
logger = CoreComponentFactory.create_logger(
    name="custom_logger",
    config={"level": "DEBUG", "format": "%(message)s"}
)

# Egyedi storage létrehozása
storage = CoreComponentFactory.create_storage(
    base_directory="/custom/storage"
)
```

## NullObject Pattern

A factory NullObject pattern-t használ fallback-ként, ha egy komponens nem érhető el a DI konténerben. Például, ha a logger nem érhető el, akkor a factory visszaad egy `DefaultLogger` példányt, amely biztonságosan kezeli a naplózási műveleteket.

```python
def _get_logger(self) -> LoggerInterface:
    logger = self._container.resolve(LoggerInterface)
    if logger is not None:
        return logger
    
    # Fallback to default logger (NullObject pattern)
    from neural_ai.core.logger.implementations.default_logger import DefaultLogger
    return DefaultLogger(name="CoreComponentFactory")
```

## Lazy Loading

A lazy loading technikával a komponensek csak akkor jönnek létre, amikor először használják őket. Ez optimalizálja a teljesítményt és csökkenti a memóriahasználatot.

```python
# A logger csak itt jön létre, amikor először hozzáférésed
logger = factory.logger
logger.info("Első naplóbejegyzés")
```

## Dependency Injection

A factory a DI pattern-t használja a függőségek kezelésére. A komponenseket a DI konténerben regisztráljuk, és a factory innen oldja fel őket.

```python
from neural_ai.core.base.container import DIContainer
from neural_ai.core.base.factory import CoreComponentFactory
from neural_ai.core.logger.implementations.default_logger import DefaultLogger
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface

# DI konténer létrehozása
container = DIContainer()

# Logger regisztrálása
logger = DefaultLogger(name="app")
container.register_instance(LoggerInterface, logger)

# Factory inicializálása
factory = CoreComponentFactory(container)

# A factory használja a regisztrált loggert
app_logger = factory.logger
```

## Hibakezelés

A factory kivételeket dob, ha probléma adódik a komponensek létrehozásakor:

- `ConfigurationError`: Ha a konfiguráció érvénytelen vagy hiányzik
- `DependencyError`: Ha szükséges függőségek hiányoznak

**Példa hibakezelésre:**
```python
from neural_ai.core.base.exceptions import ConfigurationError, DependencyError

try:
    components = CoreComponentFactory.create_components(
        config_path="config.yml"
    )
except ConfigurationError as e:
    print(f"Konfigurációs hiba: {e}")
except DependencyError as e:
    print(f"Függőségi hiba: {e}")
```

## Tesztelés

A factory-t kiterjedten teszteljük a `tests/core/base/test_factory.py` fájlban. A tesztek a következőket ellenőrzik:

- Singleton pattern működése
- Lazy loading funkcionalitás
- Komponensek létrehozása
- Függőség validáció
- Hibakezelés

**Teszt futtatása:**
```bash
pytest tests/core/base/test_factory.py -v
```

## Teljesítményoptimalizálás

A factory a következő technikákat használja a teljesítmény optimalizálására:

1. **Lazy Loading**: A komponensek csak akkor jönnek létre, amikor szükség van rájuk
2. **Singleton Pattern**: Csak egy példány létezik a rendszerben
3. **Caching**: A létrehozott komponensek gyorsítótárba kerülnek
4. **NullObject Pattern**: Fallback implementációk biztonságos használatra

## Best Practices

1. **Mindig használj DI konténert** a komponensek regisztrálásához
2. **Használd a lazy loading property-ket** a teljesítmény optimalizálásához
3. **Implementálj NullObject pattern-t** a fallback komponensekhez
4. **Validáld a konfigurációt** a komponens létrehozásakor
5. **Dokumentáld a komponensek függőségeit** a könnyebb karbantartás érdekében

## Kapcsolódó Dokumentáció

- [Core Components](base.md)
- [Dependency Injection Container](container.md)
- [Lazy Loading](lazy_loading.md)
- [Singleton Pattern](singleton.md)
- [Exception Handling](../development/error_handling.md)