# Base Komponens API Referencia

## DIContainer

A dependency injection konténer osztály biztosítja a komponensek közötti függőségek kezelését.

### Konstruktor

```python
DIContainer()
```

### Metódusok

#### register_instance
```python
def register_instance(self, interface: Any, instance: Any) -> None
```
Komponens példány regisztrálása a konténerben.

**Paraméterek:**
- `interface`: Az interfész típusa, amihez a példányt regisztráljuk
- `instance`: A regisztrálandó példány

#### register_factory
```python
def register_factory(self, interface: Any, factory: Any) -> None
```
Factory függvény regisztrálása a konténerben.

**Paraméterek:**
- `interface`: Az interfész típusa, amihez a factory-t regisztráljuk
- `factory`: A factory függvény, ami létrehozza az implementációt

#### resolve
```python
def resolve(self, interface: Any) -> Optional[Any]
```
Függőség feloldása a konténerből.

**Paraméterek:**
- `interface`: Az interfész típusa, amit fel szeretnénk oldani

**Visszatérési érték:**
- A regisztrált példány vagy None ha nem található

#### clear
```python
def clear(self) -> None
```
Konténer ürítése, minden regisztrált példány és factory törlése.

## CoreComponents

A core komponensek gyűjteményét kezelő osztály.

### Konstruktor

```python
CoreComponents(container: Optional[DIContainer] = None)
```

**Paraméterek:**
- `container`: A dependency injection konténer (opcionális)

### Tulajdonságok

- `config`: A konfiguráció kezelő komponens (read-only)
- `logger`: A logger komponens (read-only)
- `storage`: A storage komponens (read-only)

### Metódusok

#### has_config
```python
def has_config(self) -> bool
```
Ellenőrzi, hogy van-e konfigurációs komponens.

#### has_logger
```python
def has_logger(self) -> bool
```
Ellenőrzi, hogy van-e logger komponens.

#### has_storage
```python
def has_storage(self) -> bool
```
Ellenőrzi, hogy van-e storage komponens.

#### set_config
```python
def set_config(self, config: ConfigManagerInterface) -> None
```
Beállítja a config komponenst (csak teszteléshez).

#### set_logger
```python
def set_logger(self, logger: LoggerInterface) -> None
```
Beállítja a logger komponenst (csak teszteléshez).

#### set_storage
```python
def set_storage(self, storage: StorageInterface) -> None
```
Beállítja a storage komponenst (csak teszteléshez).

#### validate
```python
def validate(self) -> bool
```
Ellenőrzi, hogy minden szükséges komponens rendelkezésre áll-e.

## CoreComponentFactory

A komponensek létrehozásáért és inicializálásáért felelős factory osztály.

### Metódusok

#### create_components
```python
@staticmethod
def create_components(
    config_path: Optional[Union[str, Path]] = None,
    log_path: Optional[Union[str, Path]] = None,
    storage_path: Optional[Union[str, Path]] = None,
) -> CoreComponents
```
Core komponensek létrehozása és inicializálása.

**Paraméterek:**
- `config_path`: Konfiguráció útvonala (opcionális)
- `log_path`: Log fájl útvonala (opcionális)
- `storage_path`: Storage alap útvonal (opcionális)

**Visszatérési érték:**
- Az inicializált komponensek

#### create_with_container
```python
@staticmethod
def create_with_container(container: DIContainer) -> CoreComponents
```
Core komponensek létrehozása meglévő konténerből.

**Paraméterek:**
- `container`: A dependency injection konténer

**Visszatérési érték:**
- Az inicializált komponensek

#### create_minimal
```python
@staticmethod
def create_minimal() -> CoreComponents
```
Minimális core komponens készlet létrehozása alapértelmezett beállításokkal.

**Visszatérési érték:**
- Az alapértelmezett komponensek

## Kivételek

A base modul definiálja az összes alap kivétel osztályt a Neural AI Next projektben:

### Alap kivételek

- `NeuralAIException`: Az összes Neural AI Next kivétel alaposztálya

### Tárolási kivételek

- `StorageException`: Alap kivétel a tárolással kapcsolatos hibákhoz
- `StorageWriteError`: Fájlírási művelet sikertelensége
- `StorageReadError`: Fájlolvasási művelet sikertelensége
- `StoragePermissionError`: Jogosultsági problémák
- `InsufficientDiskSpaceError`: Nincs elég lemezterület
- `PermissionDeniedError`: Jogosultság megtagadva

### Konfigurációs kivételek

- `ConfigurationError`: Érvénytelen vagy hiányos konfiguráció

### Függőségi kivételek

- `DependencyError`: Szükséges függőségek nem elérhetőek

### Komponens kivételek

- `SingletonViolationError`: Singleton minta megsértése
- `ComponentNotFoundError`: Komponens nem található a konténerben

### Hálózati kivételek

- `NetworkException`: Alap kivétel a hálózati hibákhoz
- `TimeoutError`: Művelet időtúllépése
- `ConnectionError`: Kapcsolódás sikertelensége

## Típusok

```python
from typing import Optional, Union, Any
from pathlib import Path

# Komponens interfészek
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
from neural_ai.core.storage.interfaces.storage_interface import StorageInterface

# Útvonal típusok
PathLike = Union[str, Path]
```

## Használati példák

### 1. Minimális inicializálás

```python
from neural_ai.core.base import CoreComponentFactory

components = CoreComponentFactory.create_minimal()
components.logger.info("Application started")
```

### 2. Teljes konfiguráció

```python
from neural_ai.core.base import CoreComponentFactory

components = CoreComponentFactory.create_components(
    config_path="config.yml",
    log_path="logs/app.log",
    storage_path="data"
)

if components.validate():
    components.logger.info("All components initialized")
```

### 3. Saját konténer

```python
from neural_ai.core.base import DIContainer, CoreComponentFactory
from neural_ai.core.logger import ColoredLogger
from neural_ai.core.logger.interfaces import LoggerInterface

container = DIContainer()
container.register_instance(LoggerInterface, ColoredLogger())

components = CoreComponentFactory.create_with_container(container)
