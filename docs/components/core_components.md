# Core Components

## Áttekintés

A `CoreComponents` osztály az alap komponensek (config, logger, storage) egységes kezelését biztosítja. Ez az osztály a dependency injection (DI) pattern-t használja a komponensek közötti függőségek kezelésére, és lusta betöltést (lazy loading) támogat a hatékonyság növelése érdekében.

## Jellemzők

### LazyLoader

A `LazyLoader` egy általános osztály drága erőforrások lusta betöltéséhez. Ez azt jelenti, hogy az erőforrás csak akkor jön létre, amikor először használják.

**Metódusok:**

- `__init__(loader_func: Callable[[], T]) -> None`: Inicializálja a lustabetöltőt a megadott betöltőfüggvénnyel.
- `__call__() -> T`: Visszaadja a betöltött erőforrást (első hívásra betölti).
- `is_loaded: bool`: Tulajdonság, amely jelzi, hogy az erőforrás betöltődött-e már.
- `reset() -> None`: Visszaállítja a betöltőt, lehetővé téve az erőforrás újbóli betöltését.

**Példa:**

```python
def load_expensive_resource() -> str:
    # Szimulált drága művelet
    time.sleep(2)
    return "betöltött_adat"

loader = LazyLoader(load_expensive_resource)
# Az erőforrás még nincs betöltve
print(loader.is_loaded)  # False

# Első hozzáféréskor betöltődik
data = loader()
print(loader.is_loaded)  # True
print(data)  # "betöltött_adat"
```

### CoreComponents

A `CoreComponents` osztály a core komponensek (config, logger, storage) egységes kezelését biztosítja.

**Metódusok:**

#### Inicializálás

- `__init__(container: Optional[DIContainer] = None) -> None`: Inicializálja a core komponenseket egy opcionális DI konténerrel.

#### Komponens Hozzáférés

- `config: Optional[ConfigManagerInterface]`: Visszaadja a konfiguráció kezelő komponenst.
- `logger: Optional[LoggerInterface]`: Visszaadja a naplózó komponenst.
- `storage: Optional[StorageInterface]`: Visszaadja a tároló komponenst.

#### Komponens Beállítás (Teszteléshez)

- `set_config(config: ConfigManagerInterface) -> None`: Beállítja a konfiguráció komponenst.
- `set_logger(logger: LoggerInterface) -> None`: Beállítja a naplózó komponenst.
- `set_storage(storage: StorageInterface) -> None`: Beállítja a tároló komponenst.

#### Ellenőrzés

- `has_config() -> bool`: Ellenőrzi, hogy van-e config komponens.
- `has_logger() -> bool`: Ellenőrzi, hogy van-e logger komponens.
- `has_storage() -> bool`: Ellenőrzi, hogy van-e storage komponens.
- `validate() -> bool`: Ellenőrzi, hogy minden szükséges komponens elérhető-e.

## Használat

### Alap Használat

```python
from neural_ai.core.base.core_components import CoreComponents
from neural_ai.core.base.container import DIContainer

# Létrehozás alapértelmezett konténerrel
components = CoreComponents()

# Komponensek elérése
config = components.config
logger = components.logger
storage = components.storage

# Ellenőrzés
if components.validate():
    print("Minden komponens elérhető")
```

### DI Konténer Használata

```python
from neural_ai.core.base.core_components import CoreComponents
from neural_ai.core.base.container import DIContainer
from neural_ai.core.config.implementations import ConfigManagerFactory
from neural_ai.core.logger.implementations import LoggerFactory
from neural_ai.core.storage.implementations import FileStorage

# Konténer létrehozása
container = DIContainer()

# Komponensek regisztrálása
config = ConfigManagerFactory.get_manager("config.yml")
logger = LoggerFactory.get_logger("app")
storage = FileStorage(base_path="/tmp/storage")

container.register_instance(ConfigManagerInterface, config)
container.register_instance(LoggerInterface, logger)
container.register_instance(StorageInterface, storage)

# CoreComponents létrehozása a konténerrel
components = CoreComponents(container=container)

# Komponensek használata
config = components.config
logger = components.logger
storage = components.storage
```

### Bootstrap Pattern

A `CoreComponentFactory` osztályt használva egyszerűen inicializálhatjuk a core komponenseket:

```python
from neural_ai.core.base.factory import CoreComponentFactory

# Teljes inicializálás
core = CoreComponentFactory.create_components(
    config_path="config.yml",
    log_path="app.log",
    storage_path="/tmp/storage"
)

# Komponensek használata
config = core.config
logger = core.logger
storage = core.storage
```

### NullObject Pattern

Ha egy komponens nincs regisztrálva, a `CoreComponents` osztály `None` értéket ad vissza. Ez lehetővé teszi a biztonságos használatot:

```python
components = CoreComponents()

# Biztonságos használat
if components.has_logger():
    components.logger.info("Üzenet")
else:
    print("Logger nincs elérhető")

# Vagy egyszerűen:
logger = components.logger
if logger:
    logger.info("Üzenet")
```

## Függőségi Injektálás (DI Pattern)

A `CoreComponents` osztály szigorúan betartja a dependency injection pattern-t:

1. **Nincs top-level import**: A komponensek interfészeit csak `TYPE_CHECKING` blokkban importáljuk.
2. **Függőségek injektálása**: A komponenseket a konstruktorban vagy metódusokban injektáljuk.
3. **Konténer használata**: A `DIContainer` osztályt használjuk a függőségek feloldására.

### Előnyök

- **Laza csatolás**: A komponensek egymástól függetlenül fejleszthetők.
- **Tesztelhetőség**: A komponensek egyszerűen kicserélhetők mock objektumokra teszteléskor.
- **Konfigurálhatóság**: A komponensek konfigurációja egyszerűen módosítható.

## Bootstrap Folyamat

A bootstrap folyamat a core komponensek inicializálását végzi a megfelelő sorrendben:

1. **Konfiguráció létrehozása**: A konfigurációs fájl betöltése.
2. **Logger inicializálása**: A logger létrehozása a konfiguráció alapján.
3. **Storage inicializálása**: A tároló létrehozása a konfigurációval és loggerrel.
4. **Komponensek összekötése**: A komponensek regisztrálása a DI konténerben.

### Példa Bootstrap-re

```python
from neural_ai.core.base.core_components import CoreComponents
from neural_ai.core.base.container import DIContainer
from neural_ai.core.config.implementations import ConfigManagerFactory
from neural_ai.core.logger.implementations import LoggerFactory
from neural_ai.core.storage.implementations import FileStorage

def bootstrap_core() -> CoreComponents:
    """Core komponensek inicializálása."""
    container = DIContainer()
    
    # 1. Konfiguráció létrehozása
    config = ConfigManagerFactory.get_manager("config.yml")
    container.register_instance(ConfigManagerInterface, config)
    
    # 2. Logger inicializálása
    logger = LoggerFactory.get_logger("app", config.get_section("logger"))
    container.register_instance(LoggerInterface, logger)
    
    # 3. Storage inicializálása
    storage = FileStorage(base_path=config.get("storage_path", "/tmp/storage"))
    container.register_instance(StorageInterface, storage)
    
    # 4. CoreComponents létrehozása
    return CoreComponents(container=container)
```

## Type Hints és Biztonság

A `CoreComponents` osztály szigorú type hint-eket használ:

- **Nincs `Any` típus**: Minden típus explicit módon van deklarálva.
- **Optional típusok**: A komponensek `Optional` típusúak, mivel előfordulhat, hogy nincsenek regisztrálva.
- **Interfész alapú programozás**: A komponensek interfészein keresztül érjük el, nem konkrét implementációkon.

### Példa Type Hints-re

```python
from typing import Optional
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
from neural_ai.core.storage.interfaces.storage_interface import StorageInterface

class CoreComponents:
    @property
    def config(self) -> Optional[ConfigManagerInterface]:
        """Konfiguráció kezelő komponens lekérése."""
        return self._container.resolve(ConfigManagerInterface)
```

## Hibakezelés

A `CoreComponents` osztály a következő hibakezelési stratégiákat alkalmazza:

1. **NullObject Pattern**: Ha egy komponens nincs regisztrálva, `None` értéket ad vissza.
2. **Validáció**: A `validate()` metódussal ellenőrizhetjük, hogy minden szükséges komponens elérhető-e.
3. **Biztonságos hozzáférés**: A `has_*()` metódusokkal ellenőrizhetjük a komponensek elérhetőségét.

### Példa Hibakezelésre

```python
components = CoreComponents()

# Ellenőrzés a használat előtt
if not components.validate():
    raise RuntimeError("Nem minden szükséges komponens elérhető")

# Biztonságos használat
logger = components.logger
if logger:
    logger.info("Alkalmazás indítása")
else:
    print("Figyelmeztetés: Logger nincs elérhető")
```

## Teljesítményoptimalizálás

A `CoreComponents` osztály a következő optimalizációkat alkalmazza:

1. **Lustabetöltés (Lazy Loading)**: A komponensek csak akkor jönnek létre, amikor először használják őket.
2. **DI Konténer**: A függőségek gyors feloldását biztosítja.
3. **Singleton Pattern**: A komponensek csak egyszer jönnek létre.

## Tesztelés

A `CoreComponents` osztályt a [`tests/core/base/test_core_components.py`](../tests/core/base/test_core_components.py) fájlban teszteljük. A tesztek a következőket ellenőrzik:

- Lusta betöltés működése
- Komponensek regisztrálása és lekérése
- DI pattern helyes implementációja
- NullObject pattern helyes működése
- Validáció helyes működése

### Tesztelés Mock Objektumokkal

```python
from unittest.mock import MagicMock
from neural_ai.core.base.core_components import CoreComponents
from neural_ai.core.base.container import DIContainer

def test_core_components():
    container = DIContainer()
    components = CoreComponents(container=container)
    
    # Mock objektum létrehozása
    mock_logger = MagicMock()
    components.set_logger(mock_logger)
    
    # Tesztelés
    assert components.logger == mock_logger
    assert components.has_logger() == True
```

## Kapcsolódó Dokumentáció

- [Container](container.md): A DI konténer dokumentációja
- [Factory](base_factory.md): A core komponensek factory dokumentációja
- [Core Dependencies](../../development/core_dependencies.md): A core komponensek függőségi analízise
- [Implementation Guide](../../development/implementation_guide.md): Fejlesztési útmutató