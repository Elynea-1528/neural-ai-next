# neural_ai/core/config/factory.py

Konfiguráció kezelő factory implementáció.

Ez a modul implementálja a ConfigManagerFactory osztályt, amely felelős a különböző
konfiguráció kezelők (YAML, dinamikus adatbázis-alapú) létrehozásáért és életciklusuk
kezeléséért. A factory támogatja a szinkron és aszinkron konfiguráció kezelőket is.

## Importok

```python
from pathlib import Path
from typing import TYPE_CHECKING
from typing import Any
from pydantic import ValidationError
from neural_ai.core.config.exceptions.config_error import ConfigLoadError
from neural_ai.core.config.exceptions.config_error import ConfigValidationError
from neural_ai.core.config.interfaces.async_config_interface import AsyncConfigManagerInterface
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.config.interfaces.factory_interface import ConfigManagerFactoryInterface
from neural_ai.core.logger.interfaces import LoggerInterface
# ... és még 7 import
```

## Osztály: `ConfigManagerFactory(ConfigManagerFactoryInterface)`

Factory osztály konfiguráció kezelők létrehozásához.

Ez az osztály felelős a különböző típusú konfiguráció kezelők létrehozásáért,
regisztrálásáért és életciklusuk kezeléséért. Támogatja a szinkron (YAML fájl)
és aszinkron (adatbázis-alapú dinamikus) konfiguráció kezelőket is.

A factory alkalmazza a Dependency Injection elvet, és csak interfészeken keresztül
kommunikál a konkrét implementációkkal.

Attributes:
    _manager_types: Regisztrált szinkron konfiguráció kezelő típusok.
    _async_manager_types: Regisztrált aszinkron konfiguráció kezelő típusok.
    _logger: Logger interfész a naplózáshoz.

### Metódusok

#### `_lazy_load_implementations()`

```python
def _lazy_load_implementations(cls) -> None
```

Lazy betölti a konkrét implementációkat a körkörös importok elkerülésére. Ez a metódus biztosítja, hogy a konkrét implementációk csak akkor kerüljenek betöltésre, amikor valóban szükség van rájuk.

**Paraméterek:**

- **`cls`**

**Visszatérési érték:**

- Típus: `None`

#### `register_manager()`

```python
def register_manager(cls, extension: str, manager_class: type[ConfigManagerInterface]) -> None
```

Új szinkron konfiguráció kezelő típus regisztrálása.

**Paraméterek:**

- **`cls`**
- **`extension`** (`str`): A kezelt fájl kiterjesztése (pl: ".yml", ".json")
- **`manager_class`** (`type[ConfigManagerInterface]`): A kezelő osztály, amely implementálja a ConfigManagerInterface-t

**Visszatérési érték:**

- Típus: `None`

**Kivételek:**

- **`ValueError`**: Ha az extension vagy manager_class érvénytelen
- **`TypeError`**: Ha a manager_class nem megfelelő típusú

#### `register_async_manager()`

```python
def register_async_manager(cls, manager_type: str, manager_class: type[AsyncConfigManagerInterface]) -> None
```

Új aszinkron konfiguráció kezelő típus regisztrálása.

**Paraméterek:**

- **`cls`**
- **`manager_type`** (`str`): A kezelő típusának azonosítója (pl: "dynamic", "database")
- **`manager_class`** (`type[AsyncConfigManagerInterface]`): A kezelő osztály, amely implementálja az AsyncConfigManagerInterface-t

**Visszatérési érték:**

- Típus: `None`

**Kivételek:**

- **`ValueError`**: Ha a manager_type érvénytelen
- **`TypeError`**: Ha a manager_class nem megfelelő típusú

#### `get_manager()`

```python
def get_manager(cls, filename: str | Path, manager_type: str | None = None, logger: 'LoggerInterface | None' = None) -> ConfigManagerInterface
```

Megfelelő szinkron konfiguráció kezelő létrehozása. A metódus a fájlnév kiterjesztése alapján automatikusan kiválasztja a megfelelő kezelőt, vagy a megadott típus alapján hozza létre a kezelőt.

**Paraméterek:**

- **`cls`**
- **`filename`** (`str | Path`): Konfigurációs fájl teljes neve (elérési úttal együtt)
- **`manager_type`** (`str | None`) = `None`: Opcionális kezelő típus azonosító
- **`logger`** (`'LoggerInterface | None'`) = `None`: Logger interfész a naplózásra (opcionális)

**Visszatérési érték:**

- Típus: `ConfigManagerInterface`
- ConfigManagerInterface: A létrehozott konfiguráció kezelő példány

**Kivételek:**

- **`ConfigLoadError`**: Ha nem található megfelelő kezelő
- **`ConfigValidationError`**: Ha a konfiguráció validációja sikertelen
- **`ValueError`**: Ha a fájlnév kiterjesztése nem regisztrált

#### `get_async_manager()`

```python
async def get_async_manager(cls, manager_type: str, session: 'AsyncSession', logger: 'LoggerInterface | None' = None) -> AsyncConfigManagerInterface
```

Aszinkron konfiguráció kezelő létrehozása. A metódus explicit típusmegadással hozza létre az aszinkron konfiguráció kezelőt, lehetővé téve a paraméterek átadását a konstruktornak.

**Paraméterek:**

- **`cls`**
- **`manager_type`** (`str`): A kért kezelő típus azonosítója (pl: "dynamic", "database")
- **`session`** (`'AsyncSession'`): Az adatbázis session (kötelező a DynamicConfigManager-hez)
- **`logger`** (`'LoggerInterface | None'`) = `None`: Logger interfész a naplózásra (opcionális) **kwargs: További kulcsszavas argumentumok a kezelő konstruktorának

**Visszatérési érték:**

- Típus: `AsyncConfigManagerInterface`
- AsyncConfigManagerInterface: A létrehozott aszinkron konfiguráció kezelő példány

**Kivételek:**

- **`ConfigLoadError`**: Ha a megadott manager_type nem létezik
- **`ConfigValidationError`**: Ha a konfiguráció validációja sikertelen
- **`ValueError`**: Ha a session nincs megadva, ahol az szükséges

#### `create_manager()`

```python
def create_manager(cls, manager_type: str) -> ConfigManagerInterface
```

Szinkron konfiguráció kezelő létrehozása típus alapján. A metódus explicit típusmegadással hozza létre a konfiguráció kezelőt, lehetővé téve a paraméterek átadását a konstruktornak.

**Paraméterek:**

- **`cls`**
- **`manager_type`** (`str`): A kért kezelő típus azonosítója *args: Pozícionális argumentumok a kezelő konstruktorának **kwargs: Kulcsszavas argumentumok a kezelő konstruktorának

**Visszatérési érték:**

- Típus: `ConfigManagerInterface`
- ConfigManagerInterface: A létrehozott konfiguráció kezelő példány

**Kivételek:**

- **`ConfigLoadError`**: Ha a megadott manager_type nem létezik
- **`ConfigValidationError`**: Ha a konfiguráció validációja sikertelen

#### `get_supported_extensions()`

```python
def get_supported_extensions(cls) -> list[str]
```

Támogatott fájl kiterjesztések lekérése.

**Paraméterek:**

- **`cls`**

**Visszatérési érték:**

- Típus: `list[str]`
- list[str]: A támogatott kiterjesztések listája

#### `get_supported_async_types()`

```python
def get_supported_async_types(cls) -> list[str]
```

Támogatott aszinkron konfiguráció kezelő típusok lekérése.

**Paraméterek:**

- **`cls`**

**Visszatérési érték:**

- Típus: `list[str]`
- list[str]: A támogatott aszinkron típusok listája

---

**Forrásfájl:** [`neural_ai/core/config/factory.py`](../../neural_ai/core/config/factory.py)
