# CoreComponentFactory API

## Áttekintés

A `CoreComponentFactory` osztály a Neural AI Next projekt core komponenseinek létrehozásáért és konfigurálásáért felelős. Ez az osztály implementálja a factory mintát, és singletonként viselkedik, biztosítva, hogy mindig ugyanaz a példány legyen használva.

## Osztály: CoreComponentFactory

```python
class CoreComponentFactory(metaclass=SingletonMeta):
    """Factory for creating core components with lazy loading."""
```

### Konstruktor

```python
def __init__(self, container: DIContainer):
    """Initialize the factory with lazy-loaded dependencies."""
```

**Leírás:** Létrehoz egy új CoreComponentFactory példányt a megadott konténerrel. A factory singleton, így minden hívás ugyanazt a példányt adja vissza.

**Paraméterek:**
- `container`: A DIContainer példány, amelyet a factory használni fog

**Példa:**
```python
from neural_ai.core.base import DIContainer, CoreComponentFactory

# Konténer létrehozása
container = DIContainer()

# Factory létrehozása (első hívás)
factory1 = CoreComponentFactory(container)

# Factory lekérése (ugyanaz a példány)
factory2 = CoreComponentFactory(container)

# Ellenőrzés
assert factory1 is factory2  # True
```

## Statikus metódusok

### create_components

```python
@staticmethod
def create_components(
    config_path: Optional[Union[str, Path]] = None,
    log_path: Optional[Union[str, Path]] = None,
    storage_path: Optional[Union[str, Path]] = None,
) -> CoreComponents:
    """Core komponensek létrehozása és inicializálása."""
```

**Leírás:** Létrehozza és inicializálja a core komponenseket a megadott konfigurációval. Ez az elsődleges metódus a komponensek létrehozásához.

**Paraméterek:**
- `config_path`: A konfigurációs fájl elérési útja (opcionális)
- `log_path`: A naplófájl elérési útja (opcionális)
- `storage_path`: A tároló könyvtár elérési útja (opcionális)

**Visszatérési érték:**
- Egy `CoreComponents` példány a létrehozott komponensekkel

**Kivételek:**
- `ConfigurationError`: Ha a konfiguráció érvénytelen
- `DependencyError`: Ha szükséges függőségek hiányoznak

**Példa:**
```python
from neural_ai.core.base import CoreComponentFactory
from pathlib import Path

# Komponensek létrehozása teljes konfigurációval
components = CoreComponentFactory.create_components(
    config_path=Path('configs/system_config.yaml'),
    log_path=Path('logs/application.log'),
    storage_path=Path('./data')
)

# Komponensek használata
components.logger.info("Alkalmazás elindult")
settings = components.config.get_section('database')
components.storage.save_object({"status": "ok"}, "app_status.json")
```

### create_minimal

```python
@staticmethod
def create_minimal() -> CoreComponents:
    """Minimális core komponens készlet létrehozása."""
```

**Leírás:** Létrehoz egy minimális core komponens készletet alapértelmezett beállításokkal. Ez hasznos gyors teszteléshez vagy fejlesztéshez.

**Visszatérési érték:**
- Egy `CoreComponents` példány minimális komponensekkel

**Példa:**
```python
from neural_ai.core.base import CoreComponentFactory

# Minimális komponensek létrehozása
components = CoreComponentFactory.create_minimal()

# Használat
components.logger.info("Minimális konfigurációval működik")
# A logger és storage elérhető, de config lehet None
```

### create_with_container

```python
@staticmethod
def create_with_container(container: DIContainer) -> CoreComponents:
    """Core komponensek létrehozása meglévő konténerből."""
```

**Leírás:** Létrehozza a core komponenseket egy már létező konténerből. Ez hasznos, ha egyedi komponenseket szeretnénk hozzáadni a konténerhez.

**Paraméterek:**
- `container`: A meglévő DIContainer példány

**Visszatérési érték:**
- Egy `CoreComponents` példány

**Példa:**
```python
from neural_ai.core.base import DIContainer, CoreComponentFactory

# Konténer létrehozása és egyedi komponensekkel való feltöltése
container = DIContainer()
container.register_instance(MyCustomInterface, MyCustomImplementation())

# Core komponensek létrehozása a konténerrel
components = CoreComponentFactory.create_with_container(container)

# Használat
components.logger.info("Egyedi komponenssel működik")
custom_component = container.get('my_custom_component')
```

### create_logger

```python
@staticmethod
def create_logger(name: str, config: Optional[Dict[str, Any]] = None) -> LoggerInterface:
    """Create a logger instance.

    Args:
        name: The name of the logger
        config: Configuration dictionary

    Returns:
        LoggerInterface: The created logger instance

    Raises:
        ConfigurationError: If configuration is invalid
        DependencyError: If required dependencies are missing
    """
```

**Leírás:** Létrehoz egy logger példányt a megadott névvel és konfigurációval.

**Paraméterek:**
- `name`: A logger neve
- `config`: Konfigurációs szótár (opcionális)

**Visszatérési érték:**
- Egy `LoggerInterface` implementáció

**Kivételek:**
- `ConfigurationError`: Ha a konfiguráció érvénytelen
- `DependencyError`: Ha szükséges függőségek hiányoznak

**Példa:**
```python
from neural_ai.core.base import CoreComponentFactory

# Logger létrehozása
logger = CoreComponentFactory.create_logger(
    name='my_application',
    config={
        'level': 'INFO',
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        'log_file': 'app.log'
    }
)

# Használat
logger.info("Logger sikeresen létrehozva")
```

### create_config_manager

```python
@staticmethod
def create_config_manager(
    config_file_path: str,
    config: Optional[Dict[str, Any]] = None
) -> ConfigManagerInterface:
    """Create a config manager instance.

    Args:
        config_file_path: Path to the configuration file
        config: Configuration dictionary

    Returns:
        ConfigManagerInterface: The created config manager instance

    Raises:
        ConfigurationError: If configuration is invalid
        DependencyError: If required dependencies are missing
    """
```

**Leírás:** Létrehoz egy konfiguráció kezelő példányt a megadott konfigurációs fájllal.

**Paraméterek:**
- `config_file_path`: A konfigurációs fájl elérési útja
- `config`: További konfigurációs beállítások (opcionális)

**Visszatérési érték:**
- Egy `ConfigManagerInterface` implementáció

**Kivételek:**
- `ConfigurationError`: Ha a konfigurációs fájl nem létezik vagy érvénytelen
- `DependencyError`: Ha szükséges függőségek hiányoznak

**Példa:**
```python
from neural_ai.core.base import CoreComponentFactory

# Config manager létrehozása
config_manager = CoreComponentFactory.create_config_manager(
    config_file_path='configs/app_config.yaml'
)

# Használat
database_config = config_manager.get_section('database')
print(f"Database host: {database_config.get('host')}")
```

### create_storage

```python
@staticmethod
def create_storage(base_directory: str, config: Optional[Dict[str, Any]] = None) -> StorageInterface:
    """Create a storage instance.

    Args:
        base_directory: The base directory for storage
        config: Configuration dictionary

    Returns:
        StorageInterface: The created storage instance

    Raises:
        ConfigurationError: If configuration is invalid
        DependencyError: If required dependencies are missing
    """
```

**Leírás:** Létrehoz egy tároló példányt a megadott alapkönyvtárral.

**Paraméterek:**
- `base_directory`: A tároló alapkönyvtárának elérési útja
- `config`: Konfigurációs szótár (opcionális)

**Visszatérési érték:**
- Egy `StorageInterface` implementáció

**Kivételek:**
- `ConfigurationError`: Ha az alapkönyvtár érvénytelen
- `DependencyError`: Ha szükséges függőségek hiányoznak

**Példa:**
```python
from neural_ai.core.base import CoreComponentFactory

# Storage létrehozása
storage = CoreComponentFactory.create_storage(
    base_directory='./data',
    config={
        'auto_create_dirs': True,
        'max_file_size': 1024 * 1024  # 1MB
    }
)

# Használat
storage.save_object({"key": "value"}, "test.json")
data = storage.load_object("test.json")
print(data)  # {'key': 'value'}
```

## Példány metódusok

### reset_lazy_loaders

```python
def reset_lazy_loaders(self) -> None:
    """Reset all lazy loaders (useful for testing)."""
```

**Leírás:** Visszaállítja az összes lazy loadert az alaphelyzetbe. Ez különösen hasznos tesztelés során.

**Példa:**
```python
from neural_ai.core.base import DIContainer, CoreComponentFactory

# Factory létrehozása
container = DIContainer()
factory = CoreComponentFactory(container)

# Lazy loader-ek használata
logger = factory.logger

# Lazy loader-ek resetelése (teszteléshez)
factory.reset_lazy_loaders()

# Most újra betöltődik a logger
logger2 = factory.logger
```

## Tulajdonságok

### logger

```python
@property
def logger(self) -> LoggerInterface:
    """Get the logger instance (lazy-loaded)."""
```

**Leírás:** Visszaadja a logger példányt. Lazy-loaded, azaz csak akkor töltődik be, amikor először használják.

### config_manager

```python
@property
def config_manager(self) -> ConfigManagerInterface:
    """Get the config manager instance (lazy-loaded)."""
```

**Leírás:** Visszaadja a konfiguráció kezelő példányt. Lazy-loaded, azaz csak akkor töltődik be, amikor először használják.

### storage

```python
@property
def storage(self) -> StorageInterface:
    """Get the storage instance (lazy-loaded)."""
```

**Leírás:** Visszaadja a tároló példányt. Lazy-loaded, azaz csak akkor töltődik be, amikor először használják.

## Belső metódusok

### _get_logger

```python
def _get_logger(self) -> LoggerInterface:
    """Lazy load the logger."""
```

**Leírás:** Belső metódus a logger lazy loadingjéhez.

### _get_config_manager

```python
def _get_config_manager(self) -> ConfigManagerInterface:
    """Lazy load the config manager."""
```

**Leírás:** Belső metódus a konfiguráció kezelő lazy loadingjéhez.

### _get_storage

```python
def _get_storage(self) -> StorageInterface:
    """Lazy load the storage."""
```

**Leírás:** Belső metódus a tároló lazy loadingjéhez.

### _validate_dependencies

```python
@staticmethod
def _validate_dependencies(component_type: str, config: Optional[Dict[str, Any]] = None) -> None:
    """Validate that all required dependencies are available.

    Args:
        component_type: The type of component being created
        config: Configuration dictionary

    Raises:
        ConfigurationError: If configuration is invalid or missing
        DependencyError: If required dependencies are not available
    """
```

**Leírás:** Ellenőrzi, hogy az összes szükséges függőség elérhető-e a komponens létrehozásához.

## Használati példák

### 1. Alapvető használat

```python
from neural_ai.core.base import CoreComponentFactory

# Komponensek létrehozása
components = CoreComponentFactory.create_components(
    config_path='configs/app_config.yaml',
    log_path='logs/app.log',
    storage_path='./data'
)

# Komponensek használata
components.logger.info("Alkalmazás elindult")
app_config = components.config.get_section('app')
components.storage.save_object({"status": "running"}, "status.json")
```

### 2. Minimális konfiguráció

```python
from neural_ai.core.base import CoreComponentFactory

# Minimális komponensek
components = CoreComponentFactory.create_minimal()

# Használat
components.logger.info("Minimális konfigurációval működik")
if components.has_storage():
    components.storage.save_object({"test": "data"}, "test.json")
```

### 3. Egyedi komponensekkel

```python
from neural_ai.core.base import DIContainer, CoreComponentFactory

# Konténer létrehozása
container = DIContainer()

# Egyedi komponens hozzáadása
class MyCustomService:
    def process(self, data):
        return f"Processed: {data}"

container.register_instance(MyCustomService, MyCustomService())

# Core komponensek létrehozása
components = CoreComponentFactory.create_with_container(container)

# Használat
custom_service = container.get(MyCustomService)
result = custom_service.process("test data")
components.logger.info(result)
```

### 4. Komponensek külön-külön

```python
from neural_ai.core.base import CoreComponentFactory

# Logger létrehozása
logger = CoreComponentFactory.create_logger(
    name='my_app',
    config={'level': 'DEBUG', 'log_file': 'debug.log'}
)

# Config manager létrehozása
config_manager = CoreComponentFactory.create_config_manager(
    config_file_path='configs/settings.yaml'
)

# Storage létrehozása
storage = CoreComponentFactory.create_storage(
    base_directory='./data',
    config={'auto_create_dirs': True}
)

# Használat
logger.info("Komponensek létrehozva")
settings = config_manager.get_section('database')
storage.save_object({"config": settings}, "config_backup.json")
```

### 5. Tesztelés lazy loader reseteléssel

```python
from neural_ai.core.base import DIContainer, CoreComponentFactory

# Factory létrehozása
container = DIContainer()
factory = CoreComponentFactory(container)

# Lazy loader-ek használata
print("Első logger használat:")
logger1 = factory.logger
logger1.info("Első üzenet")

# Lazy loader-ek resetelése
print("\nLazy loader-ek resetelése...")
factory.reset_lazy_loaders()

# Újra használat
print("Második logger használat:")
logger2 = factory.logger
logger2.info("Második üzenet")

# Ellenőrzés
print(f"Azonos logger: {logger1 is logger2}")  # False (mert újra betöltődött)
```

## Hibakezelés

### ConfigurationError

Akkor dobódik, ha a konfiguráció érvénytelen vagy hiányos.

```python
from neural_ai.core.base import CoreComponentFactory
from neural_ai.core.base.exceptions import ConfigurationError

try:
    # Érvénytelen konfigurációs fájl
    components = CoreComponentFactory.create_components(
        config_path='non_existent_config.yaml'
    )
except ConfigurationError as e:
    print(f"Konfigurációs hiba: {e}")
```

### DependencyError

Akkor dobódik, ha szükséges függőségek hiányoznak.

```python
from neural_ai.core.base import CoreComponentFactory
from neural_ai.core.base.exceptions import DependencyError

try:
    # Hiányzó függőségek
    components = CoreComponentFactory.create_components()
    # Ha nincs config, de a komponensnek szüksége van rá
except DependencyError as e:
    print(f"Függőségi hiba: {e}")
```

## Teljesítmény optimalizációk

### 1. Lazy Loading

A factory lazy loadinget használ a drága erőforrásokhoz:

```python
# A logger csak akkor töltődik be, amikor először használják
factory = CoreComponentFactory(container)
# A logger még nincs betöltve
logger = factory.logger  # Most töltődik be
```

### 2. Singleton Pattern

A factory singleton, így mindig ugyanaz a példány van használva:

```python
factory1 = CoreComponentFactory(container)
factory2 = CoreComponentFactory(container)
assert factory1 is factory2  # True
```

### 3. Lazy Properties

A factory lazy property-ket használ a drága konfigurációkhoz:

```python
# A drága konfiguráció csak akkor töltődik be, amikor először használják
expensive_config = factory._expensive_config  # Most töltődik be
```

## Kapcsolódó dokumentáció

- [API Áttekintés](overview.md)
- [DIContainer API](container.md)
- [CoreComponents API](core_components.md)
- [Singleton API](singleton.md)
- [Architektúra áttekintés](../architecture/overview.md)
- [Tervezési alapelvek](../architecture/design_principles.md)

## Példák

- [Alap használati példák](../examples/basic_usage.md)
- [Haladó példák](../examples/advanced_usage.md)
- [Tesztelési példák](../examples/testing.md)

---

**Dokumentum verzió:** 1.0
**Utolsó frissítés:** 2025-12-19
**Osztály:** CoreComponentFactory
