# Component Bundle - Komponens gyűjtemény

## Áttekintés

Ez a modul a core komponensek gyűjteményét és a lusta betöltés mechanizmusát tartalmazza. A `CoreComponents` osztály egyesíti a config, logger és storage komponenseket, és biztosítja azok egységes elérését lusta betöltéssel.

## Osztályok

### `LazyLoader[T]`

**Hely:** [`neural_ai.core.base.implementations.component_bundle:19`](neural_ai/core/base/implementations/component_bundle.py:19)

Generikus lusta betöltő osztály drága erőforrásokhoz. Szálbiztos implementációval rendelkezik.

#### Metódusok

##### `__init__(loader_func: Callable[[], T]) -> None`
Inicializálja a lustabetöltőt.

**Paraméterek:**
- `loader_func`: A függvény, amely az erőforrás betöltését végzi

##### `_load() -> T`
Betölti az erőforrást, ha még nincs betöltve.

**Visszatérési érték:** A betöltött erőforrás

##### `__call__() -> T`
Visszaadja a betöltött erőforrást. Ha még nincs betöltve, először meghívja a betöltő függvényt.

**Visszatérési érték:** A betöltött erőforrás

##### `is_loaded` property
Ellenőrzi, hogy az erőforrás betöltődött-e.

**Visszatérési érték:** `bool` - True, ha az erőforrás betöltve van, különben False

##### `reset() -> None`
Visszaállítja a betöltőt, hogy kirakja az erőforrást. Lehetővé teszi az erőforrás újbóli betöltését.

**Példa:**
```python
from neural_ai.core.base.implementations.component_bundle import LazyLoader

def load_expensive_resource():
    print("Betöltés...")
    return "drága adatok"

loader = LazyLoader(load_expensive_resource)
# A betöltő függvény még nem fut le

data = loader()  # Most fut le először: "Betöltés..."
print(data)  # "drága adatok"

data2 = loader()  # Már nem fut le újra, gyorsítótárból jön
print(data2)  # "drága adatok"

loader.reset()  # Visszaállítás
data3 = loader()  # Újra lefut: "Betöltés..."
```

### `CoreComponents`

**Hely:** [`neural_ai.core.base.implementations.component_bundle:74`](neural_ai/core/base/implementations/component_bundle.py:74)

Alap komponensek gyűjteménye lusta betöltéssel. Ez az osztály egyesíti a config, logger és storage komponenseket, és biztosítja azok egységes elérését.

#### Metódusok

##### `__init__(container: Optional[DIContainer] = None) -> None`
Inicializálja a core komponenseket.

**Paraméterek:**
- `container`: Egy függőséginjektáló konténer példány. Ha nincs megadva, új konténert hoz létre.

##### `config` property
Konfiguráció kezelő komponens lekérése.

**Visszatérési érték:** `Optional[ConfigManagerInterface]` - A konfiguráció kezelő példánya, vagy None ha nincs regisztrálva

##### `logger` property
Naplózó komponens lekérése.

**Visszatérési érték:** `Optional[LoggerInterface]` - A naplózó példánya, vagy None ha nincs regisztrálva

##### `storage` property
Tároló komponens lekérése.

**Visszatérési érték:** `Optional[StorageInterface]` - A tároló példánya, vagy None ha nincs regisztrálva

##### `set_config(config: ConfigManagerInterface) -> None`
Beállítja a konfiguráció komponenst (csak teszteléshez).

**Paraméterek:**
- `config`: A konfiguráció kezelő implementáció példánya

##### `set_logger(logger: LoggerInterface) -> None`
Beállítja a naplózó komponenst (csak teszteléshez).

**Paraméterek:**
- `logger`: A naplózó implementáció példánya

##### `set_storage(storage: StorageInterface) -> None`
Beállítja a tároló komponenst (csak teszteléshez).

**Paraméterek:**
- `storage`: A tároló implementáció példánya

##### `has_config() -> bool`
Ellenőrzi, hogy van-e config komponens.

**Visszatérési érték:** `bool` - True ha van config komponens, False ha nincs

##### `has_logger() -> bool`
Ellenőrzi, hogy van-e logger komponens.

**Visszatérési érték:** `bool` - True ha van logger komponens, False ha nincs

##### `has_storage() -> bool`
Ellenőrzi, hogy van-e storage komponens.

**Visszatérési érték:** `bool` - True ha van storage komponens, False ha nincs

##### `validate() -> bool`
Ellenőrzi, hogy minden szükséges komponens megvan-e.

**Visszatérési érték:** `bool` - True ha minden komponens megvan, False ha valamelyik hiányzik

**Példa:**
```python
from neural_ai.core.base import CoreComponents, DIContainer
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
from neural_ai.core.storage.interfaces.storage_interface import StorageInterface

# Konténer létrehozása
container = DIContainer()

# Komponensek regisztrálása
config = ConfigManagerInterface()
logger = LoggerInterface()
storage = StorageInterface()

container.register_instance(ConfigManagerInterface, config)
container.register_instance(LoggerInterface, logger)
container.register_instance(StorageInterface, storage)

# Core komponensek létrehozása
components = CoreComponents(container)

# Komponensek elérése
if components.has_config():
    config = components.config

if components.has_logger():
    logger = components.logger

if components.has_storage():
    storage = components.storage

# Validálás
if components.validate():
    print("Minden komponens elérhető")
else:
    print("Néhány komponens hiányzik")
```

## Függőségek

- `threading` - Szálbiztosság érdekében
- `collections.abc.Callable` - Függvény típusokhoz
- `typing.TYPE_CHECKING` - Körkörös importok elkerüléséhez
- `neural_ai.core.base.factory.CoreComponentFactory` - Factory hozzáféréshez

## Jellemzők

- **Lazy Loading:** A komponensek csak akkor töltődnek be, amikor először használják őket
- **Szálbiztosság:** Az összes művelet szálbiztos, így többszálú környezetben is biztonságosan használható
- **DI támogatás:** Teljes mértékben integrálható a dependency injection konténerrel
- **Type Safety:** Erős típusosság generikus típusokkal

## Használati területek

- Core komponensek egységes kezelése
- Drága erőforrások lusta betöltése
- Tesztelés során mock komponensek beállítása
- Komponens életciklus kezelése

## Kapcsolódó dokumentáció

- [Core Component Factory](neural_ai/core/base/factory.md)
- [DI Container](neural_ai/core/base/implementations/di_container.md)
- [Lazy Loader](neural_ai/core/base/implementations/lazy_loader.md)