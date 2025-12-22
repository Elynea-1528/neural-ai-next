# Interfaces Modul

## Áttekintés

Az `interfaces` modul tartalmazza a Neural AI Next base komponens rendszerének alapvető interfészeit és absztrakt osztályait. Ezek az interfészek definiálják a rendszer alapvető szerkezetét és a komponensek közötti kommunikációt.

## Tartalomjegyzék

- [Interfaces Modul](#interfaces-modul)
  - [Áttekintés](#áttekintés)
  - [Tartalomjegyzék](#tartalomjegyzék)
  - [Interfészek](#interfészek)
    - [DIContainerInterface](#dicontainerinterface)
    - [CoreComponentsInterface](#corecomponentsinterface)
    - [CoreComponentFactoryInterface](#corecomponentfactoryinterface)
    - [LazyComponentInterface](#lazycomponentinterface)
  - [Típusok](#típusok)
  - [Használat](#használat)
  - [Fejlesztés](#fejlesztés)

## Interfészek

### DIContainerInterface

Dependency Injection (DI) konténer interfész, amely a komponensek közötti függőségek kezelését biztosítja.

#### Metódusok

- **`register_instance(interface: InterfaceT, instance: InterfaceT) -> None`**
  - Komponens példány regisztrálása a konténerben
  - **Paraméterek:**
    - `interface`: Az interfész típusa, amihez a példányt regisztráljuk
    - `instance`: A regisztrálandó példány

- **`register_factory(interface: InterfaceT, factory: Callable[[], InterfaceT]) -> None`**
  - Factory függvény regisztrálása a konténerben
  - **Paraméterek:**
    - `interface`: Az interfész típusa, amihez a factory-t regisztráljuk
    - `factory`: A factory függvény, ami létrehozza az implementációt

- **`resolve(interface: InterfaceT) -> InterfaceT | None`**
  - Függőség feloldása a konténerből
  - **Paraméterek:**
    - `interface`: Az interfész típusa, amit fel szeretnénk oldani
  - **Visszatérési érték:** A regisztrált példány vagy None ha nem található

- **`register_lazy(component_name: str, factory_func: Callable[[], T]) -> None`**
  - Lusta betöltésű komponens regisztrálása
  - **Paraméterek:**
    - `component_name`: A komponens neve
    - `factory_func`: A komponens létrehozásához használt factory függvény
  - **Kivételek:**
    - `ValueError`: Ha a komponens név érvénytelen vagy a factory függvény nem hívható

- **`get(component_name: str) -> object`**
  - Komponens példány lekérése (lusta betöltéssel)
  - **Paraméterek:**
    - `component_name`: A lekérendő komponens neve
  - **Visszatérési érték:** A komponens példánya
  - **Kivételek:**
    - `ComponentNotFoundError`: Ha a komponens nem található

- **`clear() -> None`**
  - Konténer ürítése

### CoreComponentsInterface

Core komponensek interfésze, amely a rendszer alapvető komponenseinek gyűjteményét definiálja.

#### Tulajdonságok

- **`config: ConfigManagerInterface | None`** (read-only)
  - Konfiguráció kezelő komponens
  - **Visszatérési érték:** A konfiguráció kezelő komponens vagy None

- **`logger: LoggerInterface | None`** (read-only)
  - Logger komponens
  - **Visszatérési érték:** A logger komponens vagy None

- **`storage: StorageInterface | None`** (read-only)
  - Storage komponens
  - **Visszatérési érték:** A storage komponens vagy None

#### Metódusok

- **`has_config() -> bool`**
  - Ellenőrzi, hogy van-e konfigurációs komponens
  - **Visszatérési érték:** True ha van konfigurációs komponens, különben False

- **`has_logger() -> bool`**
  - Ellenőrzi, hogy van-e logger komponens
  - **Visszatérési érték:** True ha van logger komponens, különben False

- **`has_storage() -> bool`**
  - Ellenőrzi, hogy van-e storage komponens
  - **Visszatérési érték:** True ha van storage komponens, különben False

- **`validate() -> bool`**
  - Ellenőrzi, hogy minden szükséges komponens rendelkezésre áll-e
  - **Visszatérési érték:** True ha minden komponens elérhető, különben False

### CoreComponentFactoryInterface

Core komponens factory interfész, amely a core komponensek létrehozásáért és inicializálásáért felelős.

#### Statikus Metódusok

- **`create_components(config_path: str | None = None, log_path: str | None = None, storage_path: str | None = None) -> CoreComponentsInterface`**
  - Core komponensek létrehozása és inicializálása
  - **Paraméterek:**
    - `config_path`: Konfiguráció útvonala (opcionális)
    - `log_path`: Log fájl útvonala (opcionális)
    - `storage_path`: Storage alap útvonal (opcionális)
  - **Visszatérési érték:** Az inicializált komponensek

- **`create_with_container(container: DIContainerInterface) -> CoreComponentsInterface`**
  - Core komponensek létrehozása meglévő konténerből
  - **Paraméterek:**
    - `container`: A dependency injection konténer
  - **Visszatérési érték:** Az inicializált komponensek

- **`create_minimal() -> CoreComponentsInterface`**
  - Minimális core komponens készlet létrehozása alapértelmezett beállításokkal
  - **Visszatérési érték:** Az alapértelmezett komponensek

### LazyComponentInterface

Lusta betöltésű komponens interfész, amely a lusta (lazy) betöltésű komponensek alapvető funkcionalitását definiálja.

#### Tulajdonságok

- **`is_loaded: bool`** (read-only)
  - Ellenőrzi, hogy a komponens betöltődött-e már
  - **Visszatérési érték:** True, ha a komponens már betöltődött, egyébként False

#### Metódusok

- **`get() -> object`**
  - Komponens példány lekérése (lusta betöltéssel)
  - **Visszatérési érték:** A komponens példánya

## Típusok

A modul a következő típusváltozókat exportálja:

- **`T`**: Általános típusváltozó
- **`InterfaceT`**: Interfész típusváltozó

## Használat

### Alapvető példa

```python
from neural_ai.core.base.interfaces import (
    DIContainerInterface,
    CoreComponentsInterface,
    CoreComponentFactoryInterface
)

# Core komponensek létrehozása
components = CoreComponentFactoryInterface.create_minimal()

# Komponensek ellenőrzése
if components.has_config():
    config = components.config
    # Konfiguráció használata

# DI konténer használata
class MyContainer(DIContainerInterface):
    def register_instance(self, interface, instance):
        # Implementáció
        pass
    
    def resolve(self, interface):
        # Implementáció
        pass
    
    # További metódusok implementációja
```

### Lusta betöltés

```python
from neural_ai.core.base.interfaces import LazyComponentInterface

class MyLazyComponent(LazyComponentInterface):
    def __init__(self):
        self._loaded = False
        self._instance = None
    
    def get(self):
        if not self._loaded:
            self._instance = self._create_instance()
            self._loaded = True
        return self._instance
    
    @property
    def is_loaded(self):
        return self._loaded
    
    def _create_instance(self):
        # Példány létrehozása
        pass
```

## Fejlesztés

### Tesztelés

A modulhoz tartozó tesztek a `tests/core/base/test_interfaces.py` fájlban találhatók. A tesztek lefuttathatók a következő paranccsal:

```bash
pytest tests/core/base/test_interfaces.py -v
```

### Kódminőség

- **Linter:** `ruff` (0 hiba szükséges)
- **Típusellenőrzés:** `mypy` (0 hiba szükséges)
- **Tesztlefedettség:** 100% coverage kötelező

### Frissítések

A modul frissítésekor ügyeljünk a következőkre:

1. Minden új metódus legyen dokumentálva
2. A típus-hintek legyenek pontosak (ne használjunk `Any` típust)
3. Az interfészek maradjanak kompatibilisek a meglévő implementációkkal
4. A tesztlefedettség maradjon 100%-os