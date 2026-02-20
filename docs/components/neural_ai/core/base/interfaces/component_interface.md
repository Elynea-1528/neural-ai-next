# neural_ai/core/base/interfaces/component_interface.py

Core komponens interfészek.

Ez a modul tartalmazza a core komponensekhez kapcsolódó interfészeket.

## Importok

```python
from abc import ABC
from abc import abstractmethod
from typing import TYPE_CHECKING
from neural_ai.core.base.interfaces.container_interface import DIContainerInterface
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
from neural_ai.data.storage.interfaces.storage_interface import StorageInterface
```

## Osztály: `CoreComponentsInterface(ABC)`

Core komponensek interfész.

Ez az interfész definiálja a core komponensek gyűjteményének
alapvető funkcionalitását és hozzáférését.

### Metódusok

#### `config()`

```python
def config(self) -> 'ConfigManagerInterface | None'
```

Konfiguráció kezelő komponens.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `'ConfigManagerInterface | None'`
- A konfiguráció kezelő komponens vagy None

#### `logger()`

```python
def logger(self) -> 'LoggerInterface | None'
```

Logger komponens.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `'LoggerInterface | None'`
- A logger komponens vagy None

#### `storage()`

```python
def storage(self) -> 'StorageInterface | None'
```

Storage komponens.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `'StorageInterface | None'`
- A storage komponens vagy None

#### `has_config()`

```python
def has_config(self) -> bool
```

Ellenőrzi, hogy van-e konfigurációs komponens.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `bool`
- True ha van konfigurációs komponens, különben False

#### `has_logger()`

```python
def has_logger(self) -> bool
```

Ellenőrzi, hogy van-e logger komponens.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `bool`
- True ha van logger komponens, különben False

#### `has_storage()`

```python
def has_storage(self) -> bool
```

Ellenőrzi, hogy van-e storage komponens.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `bool`
- True ha van storage komponens, különben False

#### `validate()`

```python
def validate(self) -> bool
```

Ellenőrzi, hogy minden szükséges komponens rendelkezésre áll-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `bool`
- True ha minden komponens elérhető, különben False

## Osztály: `CoreComponentFactoryInterface(ABC)`

Core komponens factory interfész.

Ez az interfész definiálja a core komponensek létrehozásáért
és inicializálásáért felelős factory osztály alapvető funkcionalitását.

### Metódusok

#### `create_components()`

```python
def create_components(config_path: str | None = None, log_path: str | None = None, storage_path: str | None = None) -> CoreComponentsInterface
```

Core komponensek létrehozása és inicializálása.

**Paraméterek:**

- **`config_path`** (`str | None`) = `None`: Konfiguráció útvonala (opcionális)
- **`log_path`** (`str | None`) = `None`: Log fájl útvonala (opcionális)
- **`storage_path`** (`str | None`) = `None`: Storage alap útvonal (opcionális)

**Visszatérési érték:**

- Típus: `CoreComponentsInterface`
- Az inicializált komponensek

#### `create_with_container()`

```python
def create_with_container(container: DIContainerInterface) -> CoreComponentsInterface
```

Core komponensek létrehozása meglévő konténerből.

**Paraméterek:**

- **`container`** (`DIContainerInterface`): A dependency injection konténer

**Visszatérési érték:**

- Típus: `CoreComponentsInterface`
- Az inicializált komponensek

#### `create_minimal()`

```python
def create_minimal() -> CoreComponentsInterface
```

Minimális core komponens készlet létrehozása alapértelmezett beállításokkal.

**Visszatérési érték:**

- Típus: `CoreComponentsInterface`
- Az alapértelmezett komponensek

---

**Forrásfájl:** [`neural_ai/core/base/interfaces/component_interface.py`](../../neural_ai/core/base/interfaces/component_interface.py)
