# ConfigManagerFactory

## Áttekintés

A `ConfigManagerFactory` egy gyártó (factory) osztály, amely felelős a különböző típusú konfiguráció kezelők létrehozásáért, regisztrálásáért és életciklusuk kezeléséért. Ez az osztály alkalmazza a **Factory Method** és **Dependency Injection** tervezési mintákat, biztosítva a rugalmas és bővíthető konfiguráció kezelést.

## Főbb jellemzők

- **Szinkron és aszinkron támogatás**: Képes kezelni a fájl-alapú (YAML) és adatbázis-alapú (dinamikus) konfiguráció kezelőket is.
- **Dependency Injection**: A konkrét implementációk függőségeit a factory injektálja, nem a kliensek hozzák létre őket.
- **Lazy Loading**: A konkrét implementációk csak akkor kerülnek betöltésre, amikor valóban szükség van rájuk, elkerülve a körkörös import problémákat.
- **Bővíthetőség**: Új konfiguráció kezelő típusok egyszerűen regisztrálhatók futásidőben.
- **Interfész-alapú**: Minden kommunikáció interfészeken keresztül történik, a konkrét implementációk el vannak rejtve.

## Osztály struktúra

```python
class ConfigManagerFactory(ConfigManagerFactoryInterface):
    _manager_types: dict[str, type[ConfigManagerInterface]] = {}
    _async_manager_types: dict[str, type[AsyncConfigManagerInterface]] = {}
```

### Attribútumok

- `_manager_types`: Regisztrált szinkron konfiguráció kezelő típusok tárolója.
- `_async_manager_types`: Regisztrált aszinkron konfiguráció kezelő típusok tárolója.

## Metódusok

### `register_manager()`

Új szinkron konfiguráció kezelő típus regisztrálása.

```python
@classmethod
def register_manager(
    cls, 
    extension: str, 
    manager_class: type[ConfigManagerInterface]
) -> None
```

**Paraméterek:**
- `extension`: A kezelt fájl kiterjesztése (pl: ".yml", ".json")
- `manager_class`: A kezelő osztály, amely implementálja a `ConfigManagerInterface`-t

**Kivételek:**
- `ValueError`: Ha az extension érvénytelen
- `TypeError`: Ha a manager_class nem megfelelő típusú

**Példa:**
```python
from neural_ai.core.config.factory import ConfigManagerFactory
from neural_ai.core.config.implementations.yaml_config_manager import YAMLConfigManager

# YAML konfiguráció kezelő regisztrálása
ConfigManagerFactory.register_manager(".yml", YAMLConfigManager)
ConfigManagerFactory.register_manager(".yaml", YAMLConfigManager)
```

### `register_async_manager()`

Új aszinkron konfiguráció kezelő típus regisztrálása.

```python
@classmethod
def register_async_manager(
    cls, 
    manager_type: str, 
    manager_class: type[AsyncConfigManagerInterface]
) -> None
```

**Paraméterek:**
- `manager_type`: A kezelő típusának azonosítója (pl: "dynamic", "database")
- `manager_class`: A kezelő osztály, amely implementálja az `AsyncConfigManagerInterface`-t

**Kivételek:**
- `ValueError`: Ha a manager_type érvénytelen
- `TypeError`: Ha a manager_class nem megfelelő típusú

**Példa:**
```python
from neural_ai.core.config.factory import ConfigManagerFactory
from neural_ai.core.config.implementations.dynamic_config_manager import DynamicConfigManager

# Dinamikus konfiguráció kezelő regisztrálása
ConfigManagerFactory.register_async_manager("dynamic", DynamicConfigManager)
```

### `get_manager()`

Megfelelő szinkron konfiguráció kezelő létrehozása fájlnév vagy típus alapján.

```python
@classmethod
def get_manager(
    cls, 
    filename: str | Path, 
    manager_type: str | None = None
) -> ConfigManagerInterface
```

**Paraméterek:**
- `filename`: Konfigurációs fájl teljes neve (elérési úttal együtt)
- `manager_type`: Opcionális kezelő típus azonosító

**Visszatérési érték:**
- `ConfigManagerInterface`: A létrehozott konfiguráció kezelő példány

**Kivételek:**
- `ConfigLoadError`: Ha nem található megfelelő kezelő
- `ValueError`: Ha a fájlnév kiterjesztése nem regisztrált

**Példa:**
```python
from neural_ai.core.config.factory import ConfigManagerFactory

# Automatikus típusfelismerés kiterjesztés alapján
yaml_manager = ConfigManagerFactory.get_manager("configs/database.yaml")

# Explicit típusmegadás
yaml_manager = ConfigManagerFactory.get_manager("config.txt", manager_type="yaml")
```

### `get_async_manager()`

Aszinkron konfiguráció kezelő létrehozása.

```python
@classmethod
async def get_async_manager(
    cls,
    manager_type: str,
    session: AsyncSession,
    logger: LoggerInterface | None = None,
    **kwargs: Any,
) -> AsyncConfigManagerInterface
```

**Paraméterek:**
- `manager_type`: A kért kezelő típus azonosítója (pl: "dynamic", "database")
- `session`: Az adatbázis session (kötelező a DynamicConfigManager-hez)
- `logger`: Logger interfész a naplózásra (opcionális)
- `**kwargs`: További kulcsszavas argumentumok a kezelő konstruktorának

**Visszatérési érték:**
- `AsyncConfigManagerInterface`: A létrehozott aszinkron konfiguráció kezelő példány

**Kivételek:**
- `ConfigLoadError`: Ha a megadott manager_type nem létezik
- `ValueError`: Ha a session nincs megadva, ahol az szükséges

**Példa:**
```python
import asyncio
from neural_ai.core.config.factory import ConfigManagerFactory
from neural_ai.core.db.factory import DatabaseFactory
from neural_ai.core.logger.factory import LoggerFactory

async def main():
    # Függőségek létrehozása
    session = await DatabaseFactory.get_session()
    logger = LoggerFactory.get_logger()
    
    # Dinamikus konfiguráció kezelő létrehozása
    config_manager = await ConfigManagerFactory.get_async_manager(
        manager_type="dynamic",
        session=session,
        logger=logger
    )
    
    # Konfiguráció használata
    value = await config_manager.get("database.host", default="localhost")
    print(f"Database host: {value}")

asyncio.run(main())
```

### `create_manager()`

Szinkron konfiguráció kezelő létrehozása típus alapján.

```python
@classmethod
def create_manager(
    cls, 
    manager_type: str, 
    *args: Any, 
    **kwargs: Any
) -> ConfigManagerInterface
```

**Paraméterek:**
- `manager_type`: A kért kezelő típus azonosítója
- `*args`: Pozícionális argumentumok a kezelő konstruktorának
- `**kwargs`: Kulcsszavas argumentumok a kezelő konstruktorának

**Visszatérési érték:**
- `ConfigManagerInterface`: A létrehozott konfiguráció kezelő példány

**Kivételek:**
- `ConfigLoadError`: Ha a megadott manager_type nem létezik

**Példa:**
```python
from neural_ai.core.config.factory import ConfigManagerFactory

# YAML kezelő létrehozása paraméterekkel
yaml_manager = ConfigManagerFactory.create_manager(
    ".yaml",
    filename="configs/app.yaml"
)
```

### `get_supported_extensions()`

Támogatott fájl kiterjesztések lekérése.

```python
@classmethod
def get_supported_extensions(cls) -> list[str]
```

**Visszatérési érték:**
- `list[str]`: A támogatott kiterjesztések listája

**Példa:**
```python
from neural_ai.core.config.factory import ConfigManagerFactory

extensions = ConfigManagerFactory.get_supported_extensions()
print(f"Támogatott kiterjesztések: {extensions}")
# Output: Támogatott kiterjesztések: ['.yml', '.yaml']
```

### `get_supported_async_types()`

Támogatott aszinkron konfiguráció kezelő típusok lekérése.

```python
@classmethod
def get_supported_async_types(cls) -> list[str]
```

**Visszatérési érték:**
- `list[str]`: A támogatott aszinkron típusok listája

**Példa:**
```python
from neural_ai.core.config.factory import ConfigManagerFactory

async_types = ConfigManagerFactory.get_supported_async_types()
print(f"Támogatott aszinkron típusok: {async_types}")
# Output: Támogatott aszinkron típusok: ['dynamic', 'database']
```

## Használati minták

### 1. Alap YAML konfiguráció kezelés

```python
from neural_ai.core.config.factory import ConfigManagerFactory

# YAML konfiguráció kezelő létrehozása
config_manager = ConfigManagerFactory.get_manager("configs/app.yaml")

# Érték lekérése
host = config_manager.get("database", "host", default="localhost")
port = config_manager.get("database", "port", default=5432)

# Érték beállítása
config_manager.set("database", "host", "192.168.1.100")
config_manager.save()
```

### 2. Dinamikus konfiguráció kezelés adatbázissal

```python
import asyncio
from neural_ai.core.config.factory import ConfigManagerFactory
from neural_ai.core.db.factory import DatabaseFactory

async def main():
    # Adatbázis session létrehozása
    session = await DatabaseFactory.get_session()
    
    # Dinamikus konfiguráció kezelő létrehozása
    config_manager = await ConfigManagerFactory.get_async_manager(
        manager_type="dynamic",
        session=session
    )
    
    # Konfiguráció beállítása
    await config_manager.set("app.timeout", 30)
    await config_manager.set_with_metadata(
        key="app.max_connections",
        value=100,
        category="performance",
        description="Maximum number of database connections"
    )
    
    # Konfiguráció lekérdezése
    timeout = await config_manager.get("app.timeout", default=10)
    print(f"Timeout: {timeout}")
    
    # Hot reload indítása
    await config_manager.start_hot_reload(interval=5.0)
    
    # Hot reload leállítása
    await config_manager.stop_hot_reload()

asyncio.run(main())
```

### 3. Konfiguráció változások figyelése

```python
import asyncio
from neural_ai.core.config.factory import ConfigManagerFactory

async def config_change_handler(key: str, value: Any) -> None:
    """Callback függvény konfiguráció változásokhoz."""
    print(f"Konfiguráció megváltozott: {key} = {value}")

async def main():
    session = await DatabaseFactory.get_session()
    config_manager = await ConfigManagerFactory.get_async_manager(
        manager_type="dynamic",
        session=session
    )
    
    # Listener hozzáadása
    config_manager.add_listener(config_change_handler)
    
    # Konfiguráció változtatása (a listener automatikusan meghívódik)
    await config_manager.set("app.debug", True)
    
    # Listener eltávolítása
    config_manager.remove_listener(config_change_handler)

asyncio.run(main())
```

### 4. Egyéni konfiguráció kezelő regisztrálása

```python
from neural_ai.core.config.factory import ConfigManagerFactory
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface

class JSONConfigManager(ConfigManagerInterface):
    """Egyéni JSON konfiguráció kezelő."""
    
    def __init__(self, filename: str | None = None) -> None:
        # Implementáció...
        pass
    
    def get(self, *keys: str, default: Any = None) -> Any:
        # Implementáció...
        pass
    
    # További metódusok implementálása...
    def set(self, *keys: str, value: Any) -> None:
        pass
    
    def save(self, filename: str | None = None) -> None:
        pass
    
    def load(self, filename: str) -> None:
        pass
    
    def load_directory(self, path: str) -> None:
        pass
    
    def validate(self, schema: dict[str, Any]) -> tuple[bool, dict[str, str] | None]:
        pass

# Egyéni kezelő regisztrálása
ConfigManagerFactory.register_manager(".json", JSONConfigManager)

# Használat
json_manager = ConfigManagerFactory.get_manager("configs/app.json")
```

## Lazy Loading mechanizmus

A `ConfigManagerFactory` alkalmazza a **Lazy Loading** tervezési mintát a körkörös import problémák elkerülésére. A konkrét implementációk csak akkor kerülnek betöltésre, amikor valóban szükség van rájuk.

```python
@classmethod
def _lazy_load_implementations(cls) -> None:
    """Lazy betölti a konkrét implementációkat a körkörös importok elkerülésére."""
    if not cls._manager_types:
        from neural_ai.core.config.implementations.yaml_config_manager import (
            YAMLConfigManager,
        )
        cls._manager_types.update({
            ".yml": YAMLConfigManager,
            ".yaml": YAMLConfigManager,
        })

    if not cls._async_manager_types:
        from neural_ai.core.config.implementations.dynamic_config_manager import (
            DynamicConfigManager,
        )
        cls._async_manager_types.update({
            "dynamic": DynamicConfigManager,
            "database": DynamicConfigManager,
        })
```

Ez a mechanizmus biztosítja, hogy:
- A betöltési idő minimalizálva legyen
- Ne legyenek körkörös import hibák
- A memóriahasználat optimalizálva legyen

## Dependency Injection

A factory alkalmazza a **Dependency Injection** elvet, ami azt jelenti, hogy a konkrét implementációk függőségeit a factory injektálja, nem a kliensek hozzák létre őket.

**Előnyök:**
- **Laza csatolás**: A kliensek nem függenek a konkrét implementációktól.
- **Tesztelhetőség**: A függőségek egyszerűen kicserélhetők mock objektumokra.
- **Karbantarthatóság**: A függőségek központilag kezelhetők.

**Példa:**
```python
# Helyes: A factory injektálja a függőségeket
config_manager = await ConfigManagerFactory.get_async_manager(
    manager_type="dynamic",
    session=session,  # Dependency Injection
    logger=logger     # Dependency Injection
)

# Helytelen: Direkt példányosítás
from neural_ai.core.config.implementations.dynamic_config_manager import DynamicConfigManager
config_manager = DynamicConfigManager(session=session, logger=logger)  # ❌ Tilos!
```

## Hibakezelés

A `ConfigManagerFactory` átfogó hibakezelést biztosít:

### `ConfigLoadError`

A konfiguráció betöltése során fellépő hibák esetén.

```python
from neural_ai.core.config.exceptions import ConfigLoadError

try:
    config_manager = ConfigManagerFactory.get_manager("configs/invalid.xml")
except ConfigLoadError as e:
    print(f"Konfiguráció betöltési hiba: {e}")
```

### `ValueError`

Érvénytelen paraméterek esetén.

```python
try:
    ConfigManagerFactory.register_manager("", SomeManager)
except ValueError as e:
    print(f"Érvénytelen paraméter: {e}")
```

### `TypeError`

Helytelen típusú paraméterek esetén.

```python
try:
    ConfigManagerFactory.register_manager(".json", str)  # str nem ConfigManagerInterface
except TypeError as e:
    print(f"Típushiba: {e}")
```

## Teljesítményoptimalizálás

### Cache-elés

A factory nem alkalmaz cache-elést, mivel minden hívásnál új példányt hoz létre. A konfiguráció kezelők saját cache-elési mechanizmust implementálhatnak.

### Lazy Loading

A lazy loading minimalizálja a betöltési időt és a memóriahasználatot.

### Aszinkron műveletek

Az aszinkron konfiguráció kezelők nem blokkolják a fő szálat, ami javítja az alkalmazás teljesítményét.

## Biztonság

### Típusbiztonság

A factory szigorú típusellenőrzést alkalmaz a bemeneti paraméterekre.

```python
# Típusellenőrzés a regisztráció során
if not issubclass(manager_class, ConfigManagerInterface):
    raise TypeError("A manager_class-nak implementálnia kell a ConfigManagerInterface-t")
```

### Érvényesség ellenőrzés

A bemeneti paraméterek érvényessége ellenőrzésre kerül.

```python
# Extension normalizálás
if not extension.startswith("."):
    extension = f".{extension}"
```

## Fejlesztői útmutató

### Új konfiguráció kezelő hozzáadása

1. **Interfész implementálása:**
   ```python
   from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
   
   class CustomConfigManager(ConfigManagerInterface):
       def __init__(self, filename: str | None = None) -> None:
           pass
       
       def get(self, *keys: str, default: Any = None) -> Any:
           pass
       
       # További metódusok...
   ```

2. **Regisztráció a factory-ban:**
   ```python
   from neural_ai.core.config.factory import ConfigManagerFactory
   
   ConfigManagerFactory.register_manager(".custom", CustomConfigManager)
   ```

3. **Használat:**
   ```python
   config_manager = ConfigManagerFactory.get_manager("configs/app.custom")
   ```

### Aszinkron konfiguráció kezelő hozzáadása

1. **Interfész implementálása:**
   ```python
   from neural_ai.core.config.interfaces.async_config_interface import AsyncConfigManagerInterface
   
   class CustomAsyncConfigManager(AsyncConfigManagerInterface):
       def __init__(self, session: AsyncSession, logger: LoggerInterface | None = None) -> None:
           pass
       
       async def get(self, *keys: str, default: Any = None) -> Any:
           pass
       
       # További aszinkron metódusok...
   ```

2. **Regisztráció a factory-ban:**
   ```python
   from neural_ai.core.config.factory import ConfigManagerFactory
   
   ConfigManagerFactory.register_async_manager("custom", CustomAsyncConfigManager)
   ```

3. **Használat:**
   ```python
   config_manager = await ConfigManagerFactory.get_async_manager(
       manager_type="custom",
       session=session,
       logger=logger
   )
   ```

## Kapcsolódó dokumentáció

- [`ConfigManagerInterface`](interfaces/config_interface.md): Szinkron konfiguráció kezelő interfész
- [`AsyncConfigManagerInterface`](interfaces/async_config_interface.md): Aszinkron konfiguráció kezelő interfész
- [`YAMLConfigManager`](implementations/yaml_config_manager.md): YAML fájl-alapú konfiguráció kezelő
- [`DynamicConfigManager`](implementations/dynamic_config_manager.md): Dinamikus adatbázis-alapú konfiguráció kezelő
- [`ConfigLoadError`](../exceptions/config_error.md): Konfiguráció betöltési hiba

## Verziótörténet

- **v1.0.0** (2025-01-XX): Kezdeti implementáció
  - Alap factory funkcionalitás
  - YAML konfiguráció támogatás
  - Dinamikus konfiguráció támogatás
  - Dependency Injection
  - Lazy Loading