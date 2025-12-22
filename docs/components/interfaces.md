# Base Interfészek

Ez a dokumentáció a Neural AI Next base komponens rendszerének interfészeit és absztrakt osztályait írja le.

## Áttekintés

A base interfész modul (`neural_ai.core.base.interfaces`) a rendszer alapvető építőköveit definiálja, amelyek a dependency injection, komponens kezelés és lusta betöltés funkcionalitását biztosítják.

## Interfészek

### DIContainerInterface

A dependency injection konténer interfésze, amely a komponensek közötti függőségek kezelését biztosítja.

#### Metódusok

- **register_instance(interface: InterfaceT, instance: InterfaceT) -> None**
  - Komponens példány regisztrálása a konténerben
  - Args:
    - `interface`: Az interfész típusa, amihez a példányt regisztráljuk
    - `instance`: A regisztrálandó példány

- **register_factory(interface: InterfaceT, factory: Callable[[], InterfaceT]) -> None**
  - Factory függvény regisztrálása a konténerben
  - Args:
    - `interface`: Az interfész típusa, amihez a factory-t regisztráljuk
    - `factory`: A factory függvény, ami létrehozza az implementációt

- **resolve(interface: InterfaceT) -> InterfaceT | None**
  - Függőség feloldása a konténerből
  - Args:
    - `interface`: Az interfész típusa, amit fel szeretnénk oldani
  - Returns:
    - A regisztrált példány vagy None ha nem található

- **register_lazy(component_name: str, factory_func: Callable[[], T]) -> None**
  - Lusta betöltésű komponens regisztrálása
  - Args:
    - `component_name`: A komponens neve
    - `factory_func`: A komponens létrehozásához használt factory függvény
  - Raises:
    - `ValueError`: Ha a komponens név érvénytelen vagy a factory függvény nem hívható

- **get(component_name: str) -> object**
  - Komponens példány lekérése (lusta betöltéssel)
  - Args:
    - `component_name`: A lekérendő komponens neve
  - Returns:
    - A komponens példánya
  - Raises:
    - `ComponentNotFoundError`: Ha a komponens nem található

- **clear() -> None**
  - Konténer ürítése

### CoreComponentsInterface

A core komponensek interfésze, amely a rendszer alapvető komponenseinek (config, logger, storage) hozzáférését biztosítja.

#### Property-k

- **config: ConfigManagerInterface | None**
  - Konfiguráció kezelő komponens lekérése
  - Returns: A konfiguráció kezelő komponens vagy None

- **logger: LoggerInterface | None**
  - Logger komponens lekérése
  - Returns: A logger komponens vagy None

- **storage: StorageInterface | None**
  - Storage komponens lekérése
  - Returns: A storage komponens vagy None

#### Metódusok

- **has_config() -> bool**
  - Ellenőrzi, hogy van-e konfigurációs komponens
  - Returns: True ha van konfigurációs komponens, különben False

- **has_logger() -> bool**
  - Ellenőrzi, hogy van-e logger komponens
  - Returns: True ha van logger komponens, különben False

- **has_storage() -> bool**
  - Ellenőrzi, hogy van-e storage komponens
  - Returns: True ha van storage komponens, különben False

- **validate() -> bool**
  - Ellenőrzi, hogy minden szükséges komponens rendelkezésre áll-e
  - Returns: True ha minden komponens elérhető, különben False

### CoreComponentFactoryInterface

A core komponensek létrehozásáért felelős factory interfész.

#### Metódusok

- **create_components(config_path: str | None = None, log_path: str | None = None, storage_path: str | None = None) -> CoreComponentsInterface**
  - Core komponensek létrehozása és inicializálása
  - Args:
    - `config_path`: Konfiguráció útvonala (opcionális)
    - `log_path`: Log fájl útvonala (opcionális)
    - `storage_path`: Storage alap útvonal (opcionális)
  - Returns: Az inicializált komponensek

- **create_with_container(container: DIContainerInterface) -> CoreComponentsInterface**
  - Core komponensek létrehozása meglévő konténerből
  - Args:
    - `container`: A dependency injection konténer
  - Returns: Az inicializált komponensek

- **create_minimal() -> CoreComponentsInterface**
  - Minimális core komponens készlet létrehozása alapértelmezett beállításokkal
  - Returns: Az alapértelmezett komponensek

### LazyComponentInterface

A lusta betöltésű komponensek interfésze.

#### Metódusok

- **get() -> object**
  - Komponens példány lekérése (lusta betöltéssel)
  - Returns: A komponens példánya

#### Property-k

- **is_loaded: bool**
  - Ellenőrzi, hogy a komponens betöltődött-e már
  - Returns: True, ha a komponens már betöltődött, egyébként False

## Type Hints és Generikus Típusok

Az interfészek erős típusos megkötéseket használnak a következő TypeVar-ekkel:

- **InterfaceT**: Interfész típusokhoz használt generikus típusváltozó
- **T**: Általános komponens típusokhoz használt generikus típusváltozó

## Használati Példák

### DIContainerInterface használata

```python
from neural_ai.core.base.interfaces import DIContainerInterface
from neural_ai.core.base.container import DIContainer

# Konténer létrehozása
container: DIContainerInterface = DIContainer()

# Példány regisztrálása
config_manager = ConfigManager()
container.register_instance(ConfigManagerInterface, config_manager)

# Factory regisztrálása
container.register_factory(LoggerInterface, lambda: Logger())

# Függőség feloldása
resolved_config = container.resolve(ConfigManagerInterface)
```

### CoreComponentsInterface használata

```python
from neural_ai.core.base.interfaces import CoreComponentsInterface

class MyComponents(CoreComponentsInterface):
    @property
    def config(self) -> ConfigManagerInterface | None:
        return self._config
    
    @property
    def logger(self) -> LoggerInterface | None:
        return self._logger
    
    @property
    def storage(self) -> StorageInterface | None:
        return self._storage
    
    def has_config(self) -> bool:
        return self._config is not None
    
    def has_logger(self) -> bool:
        return self._logger is not None
    
    def has_storage(self) -> bool:
        return self._storage is not None
    
    def validate(self) -> bool:
        return all([self.has_config(), self.has_logger(), self.has_storage()])
```

## Kapcsolódó Dokumentáció

- [Base Komponensek](base.md)
- [Dependency Injection Konténer](container.md)
- [Core Komponensek](core_components.md)
- [Base Factory](base_factory.md)