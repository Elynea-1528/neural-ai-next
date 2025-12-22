# Core Components

## Áttekintés

A `core_components` modul az alapvető komponenseket és lusta betöltési mechanizmusokat tartalmazza a Neural AI Next rendszerhez. Ez a modul biztosítja a konfiguráció, naplózás és tároló komponensek egységes kezelését.

## Osztályok

### LazyLoader[T]

Drága erőforrások lusta (lazy) betöltését végző generikus osztály.

#### Metódusok

- `__init__(loader_func: Callable[[], T]) -> None`
  - Inicializálja a lusta betöltőt a megadott betöltő függvénnyel.

- `__call__() -> T`
  - Visszaadja a betöltött erőforrást. Ha még nincs betöltve, meghívja a betöltő függvényt.

- `is_loaded: bool` (property)
  - Visszaadja, hogy az erőforrás betöltődött-e már.

- `reset() -> None`
  - Visszaállítja a betöltőt, lehetővé téve az erőforrás újbóli betöltését.

#### Példa

```python
def nehez_szamolas() -> int:
    # Drága számítás
    return 42

loader = LazyLoader(nehez_szamolas)
print(loader.is_loaded)  # False
ertek = loader()  # Most történik meg a számítás
print(ertek)  # 42
print(loader.is_loaded)  # True
```

### CoreComponents

Alap komponensek egységes hozzáférését biztosító osztály. Ez az osztály felelős a konfiguráció, naplózó és tároló komponensek kezeléséért.

#### Metódusok

- `__init__(container: Optional[DIContainer] = None) -> None`
  - Inicializálja a komponenseket a megadott DI konténerrel.

##### Tulajdonságok (Properties)

- `config: Optional[ConfigManagerInterface]`
  - Visszaadja a konfiguráció kezelő komponenst, ha elérhető.

- `logger: Optional[LoggerInterface]`
  - Visszaadja a naplózó komponenst, ha elérhető.

- `storage: Optional[StorageInterface]`
  - Visszaadja a tároló komponenst, ha elérhető.

##### Beállító Metódusok (Teszteléshez)

- `set_config(config: ConfigManagerInterface) -> None`
  - Beállítja a konfiguráció komponenst.

- `set_logger(logger: LoggerInterface) -> None`
  - Beállítja a naplózó komponenst.

- `set_storage(storage: StorageInterface) -> None`
  - Beállítja a tároló komponenst.

##### Ellenőrző Metódusok

- `has_config() -> bool`
  - Ellenőrzi, hogy van-e konfiguráció komponens.

- `has_logger() -> bool`
  - Ellenőrzi, hogy van-e naplózó komponens.

- `has_storage() -> bool`
  - Ellenőrzi, hogy van-e tároló komponens.

- `validate() -> bool`
  - Ellenőrzi, hogy minden szükséges komponens elérhető-e.

#### Példa

```python
# Alap inicializálás
core = CoreComponents()

# Komponensek beállítása
config = YamlConfigManager("config.yaml")
logger = ColoredLogger()
storage = FileStorage()

core.set_config(config)
core.set_logger(logger)
core.set_storage(storage)

# Használat
if core.validate():
    core.config.get("database.host")
    core.logger.info("Rendszer elindult")
    core.storage.save("data.txt", b"adat")
else:
    print("Hiányzó komponensek!")
```

## Függőségek

- `neural_ai.core.base.container` - DI konténer implementáció
- `neural_ai.core.base.factory` - Komponens gyártó
- `neural_ai.core.config.interfaces.config_interface` - Konfiguráció interfész
- `neural_ai.core.logger.interfaces.logger_interface` - Naplózó interfész
- `neural_ai.core.storage.interfaces.storage_interface` - Tároló interfész

## Használati Minták

### 1. Egyszerű inicializálás

```python
from neural_ai.core.base.core_components import CoreComponents

# Alapértelmezett konténerrel
core = CoreComponents()

# Komponensek ellenőrzése
if core.has_config():
    print("Konfiguráció elérhető")
```

### 2. Testreszabott konténerrel

```python
from neural_ai.core.base.core_components import CoreComponents
from neural_ai.core.base.container import DIContainer

# Saját konténer létrehozása
container = DIContainer()
container.register_instance(ConfigManagerInterface, my_config)

# CoreComponents inicializálása a konténerrel
core = CoreComponents(container)
```

### 3. Lusta betöltés használata

```python
from neural_ai.core.base.core_components import LazyLoader

def betolt_adatbazis():
    # Drága adatbázis kapcsolat létrehozása
    return DatabaseConnection()

loader = LazyLoader(betolt_adatbazis)

# A kapcsolat csak itt jön létre
db = loader()
```

## Jellemzők

- **Lusta betöltés:** Az erőforrások csak akkor töltődnek be, amikor először használják őket.
- **Szálbiztonság:** A `LazyLoader` szálbiztos, többszálú környezetben is használható.
- **DI támogatás:** A `CoreComponents` támogatja a függőséginjektálást egyedi konténerekkel.
- **Típusbiztonság:** Minden metódus rendelkezik pontos típusannotációkkal.

## Korlátozások

- A `CoreComponents` csak a regisztrált komponensekhez biztosít hozzáférést.
- A lusta betöltés nem támogatja az argumentumokat a betöltő függvénynek.

## Jövőbeli Fejlesztések

- Aszinkron lusta betöltés támogatása
- Komponens életciklus kezelés
- Konfiguráció alapú automatikus komponens regisztráció