# neural_ai/core/base/factory.py

Core komponensek factory implementáció.

Ez a modul biztosítja a core komponensek (config, logger, storage) létrehozását
és kezelését dependency injection pattern használatával. A factory támogatja
a lazy loadinget, bootstrap inicializálást és NullObject pattern-t fallback-ként.

## Importok

```python
import time
from pathlib import Path
from typing import TYPE_CHECKING
from typing import Any
from typing import cast
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import ValidationError
from neural_ai.core.base.exceptions import ConfigurationError
# ... és még 30 import
```

## Konstansok

- **`DEFAULT_CONFIG_FILE`**
: `'configs/system.yaml'`


## Osztály: `BaseConfig(BaseModel)`

Alap konfigurációs schema.

## Osztály: `LoggerConfig(BaseConfig)`

Logger komponens konfigurációja.

## Osztály: `ConfigManagerConfig(BaseConfig)`

Config manager komponens konfigurációja.

## Osztály: `StorageConfig(BaseConfig)`

Storage komponens konfigurációja.

## Osztály: `CoreComponentFactory`

Core komponensek létrehozásáért felelős factory lazy loadinggel.

Ez az osztály biztosítja a core komponensek (config, logger, storage) egységes
létrehozását és kezelését. Singleton minta használatával biztosítja, hogy csak
egy példány létezik, és lazy loading technikával optimalizálja a teljesítményt.

A factory támogatja a komponensek validációját, függőségi injektálást és
automatikus inicializálást különböző konfigurációs forgatókönyvekben.

Attributes:
    _container: A dependency injection konténer
    _logger_loader: Lazy loader a logger komponenshez
    _config_loader: Lazy loader a config manager komponenshez
    _storage_loader: Lazy loader a storage komponenshez

### Metódusok

#### `__init__()`

```python
def __init__(self, container: DIContainer)
```

Inicializálja a factory-t lazy-loaded függőségekkel.

**Paraméterek:**

- **`self`**
- **`container`** (`DIContainer`)

#### `_get_logger()`

```python
def _get_logger(self) -> 'LoggerInterface'
```

Lazy loadinggel tölti be a logger komponenst.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `'LoggerInterface'`

#### `_get_config_manager()`

```python
def _get_config_manager(self) -> 'ConfigManagerInterface'
```

Lazy loadinggel tölti be a config manager komponenst.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `'ConfigManagerInterface'`

#### `_get_storage()`

```python
def _get_storage(self) -> 'StorageInterface'
```

Lazy loadinggel tölti be a storage komponenst.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `'StorageInterface'`

#### `logger()`

```python
def logger(self) -> 'LoggerInterface'
```

Visszaadja a logger példányt (lazy-loaded).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `'LoggerInterface'`

#### `config_manager()`

```python
def config_manager(self) -> 'ConfigManagerInterface'
```

Visszaadja a config manager példányt (lazy-loaded).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `'ConfigManagerInterface'`

#### `storage()`

```python
def storage(self) -> 'StorageInterface'
```

Visszaadja a storage példányt (lazy-loaded).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `'StorageInterface'`

#### `_expensive_config()`

```python
def _expensive_config(self) -> dict[str, Any]
```

Lazy loadinggel tölti be a drága konfigurációt.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `dict[str, Any]`

#### `_component_cache()`

```python
def _component_cache(self) -> dict[str, Any]
```

Lazy loadinggel tölti be a komponens gyorsítótárát.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `dict[str, Any]`

#### `_process_config()`

```python
def _process_config(self, config: dict[str, Any]) -> dict[str, Any]
```

Feldolgozza a konfigurációt (szimulált drága művelet).

**Paraméterek:**

- **`self`**
- **`config`** (`dict[str, Any]`)

**Visszatérési érték:**

- Típus: `dict[str, Any]`

#### `_load_component_cache()`

```python
def _load_component_cache(self) -> dict[str, Any]
```

Betölti a komponens gyorsítótárát (szimulált drága művelet).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `dict[str, Any]`

#### `reset_lazy_loaders()`

```python
def reset_lazy_loaders(self) -> None
```

Visszaállítja az összes lazy loadert. Ez a metódus visszaállítja az összes lazy loader állapotát, amely hasznos lehet tesztelés során vagy újrainicializáláskor. A lazy property-ket is törli.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `_validate_dependencies()`

```python
def _validate_dependencies(component_type: str, config: dict[str, Any] | None = None) -> None
```

Ellenőrzi, hogy minden szükséges függőség elérhető-e.

**Paraméterek:**

- **`component_type`** (`str`): A létrehozandó komponens típusa
- **`config`** (`dict[str, Any] | None`) = `None`: Konfigurációs dictionary

**Visszatérési érték:**

- Típus: `None`

**Kivételek:**

- **`ConfigurationError`**: Ha a konfiguráció érvénytelen vagy hiányzik
- **`DependencyError`**: Ha szükséges függőségek nem érhetők el

#### `create_components()`

```python
def create_components(config_path: str | Path | None = None, log_path: str | Path | None = None, storage_path: str | Path | None = None) -> 'CoreComponents'
```

Core komponensek létrehozása és inicializálása. Létrehozza és inicializálja az összes core komponenst (config, logger, storage) a megadott elérési utak alapján. A komponensek lazy loadinggel kerülnek betöltésre.

**Paraméterek:**

- **`config_path`** (`str | Path | None`) = `None`: A konfigurációs fájl elérési útja (opcionális)
- **`log_path`** (`str | Path | None`) = `None`: A log fájl elérési útja (opcionális)
- **`storage_path`** (`str | Path | None`) = `None`: A tároló alapkönyvtára (opcionális)

**Visszatérési érték:**

- Típus: `'CoreComponents'`
- CoreComponents: Az inicializált core komponensek gyűjteménye

**Kivételek:**

- **`ConfigurationError`**: Ha a konfiguráció érvénytelen
- **`DependencyError`**: Ha szükséges függőségek hiányoznak

#### `create_with_container()`

```python
def create_with_container(container: DIContainer) -> 'CoreComponents'
```

Core komponensek létrehozása meglévő konténerből.

**Paraméterek:**

- **`container`** (`DIContainer`): A DI konténer, amely tartalmazza a komponenseket

**Visszatérési érték:**

- Típus: `'CoreComponents'`
- CoreComponents: Az inicializált core komponensek

#### `create_minimal()`

```python
def create_minimal() -> 'CoreComponents'
```

Minimális core komponens készlet létrehozása. Létrehoz egy alapvető komponens készletet alapértelmezett beállításokkal. Megpróbálja betölteni a config.yml fájlt, ha létezik, különben alapértelmezett konfigurációt használ.

**Visszatérési érték:**

- Típus: `'CoreComponents'`
- CoreComponents: Az inicializált minimális komponensek

#### `create_logger()`

```python
def create_logger(name: str, config: dict[str, Any] | None = None) -> 'LoggerInterface'
```

Létrehoz egy logger példányt.

**Paraméterek:**

- **`name`** (`str`): A logger neve
- **`config`** (`dict[str, Any] | None`) = `None`: Konfigurációs dictionary (opcionális)

**Visszatérési érték:**

- Típus: `'LoggerInterface'`
- LoggerInterface: A létrehozott logger példány

**Kivételek:**

- **`ConfigurationError`**: Ha a konfiguráció érvénytelen
- **`DependencyError`**: Ha szükséges függőségek hiányoznak

#### `create_config_manager()`

```python
def create_config_manager(config_file_path: str, config: dict[str, Any] | None = None) -> 'ConfigManagerInterface'
```

Létrehoz egy config manager példányt.

**Paraméterek:**

- **`config_file_path`** (`str`): A konfigurációs fájl elérési útja
- **`config`** (`dict[str, Any] | None`) = `None`: Konfigurációs dictionary

**Visszatérési érték:**

- Típus: `'ConfigManagerInterface'`
- ConfigManagerInterface: A létrehozott config manager példány

**Kivételek:**

- **`ConfigurationError`**: Ha a konfiguráció érvénytelen
- **`DependencyError`**: Ha szükséges függőségek hiányoznak

#### `create_storage()`

```python
def create_storage(base_path: str | None, logger: 'LoggerInterface', config_manager: 'ConfigManagerInterface') -> 'StorageInterface'
```

Létrehoz egy storage példányt.

**Paraméterek:**

- **`base_path`** (`str | None`): A tároló alapkönyvtára
- **`logger`** (`'LoggerInterface'`): Logger interfész példány
- **`config_manager`** (`'ConfigManagerInterface'`): Config manager interfész példány

**Visszatérési érték:**

- Típus: `'StorageInterface'`
- StorageInterface: A létrehozott storage példány

**Kivételek:**

- **`ConfigurationError`**: Ha a konfiguráció érvénytelen
- **`DependencyError`**: Ha szükséges függőségek hiányoznak

---

**Forrásfájl:** [`neural_ai/core/base/factory.py`](../../neural_ai/core/base/factory.py)
