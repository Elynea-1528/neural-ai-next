# neural_ai/data/storage/interfaces/factory_interface.py

Tárolási factory interfész a különböző tárolási megoldások létrehozásához.

Ez az interfész egy gyártó (factory) mintát definiál, amely lehetővé teszi a tárolási
implementációk dinamikus regisztrálását és példányosítását. Az interfész segítségével
a rendszer függetlenítetté válik a konkrét tárolási osztályoktól.

## Importok

```python
from abc import ABC
from abc import abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.events.interfaces.event_bus_interface import EventBusInterface
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
from neural_ai.core.utils.interfaces.hardware_interface import HardwareInterface
from neural_ai.data.storage.interfaces.storage_interface import StorageInterface
```

## Osztály: `StorageFactoryInterface(ABC)`

Tárolási factory interfész a tárolási implementációk gyártásához.

Ez egy absztrakt alaposztály, amely meghatározza a tárolási factory-k
alapvető viselkedését. A konkrét implementációknak ezt az interfészt kell
megvalósítaniuk a saját factory osztályaikban.

### Metódusok

#### `register_storage()`

```python
def register_storage(cls, storage_type: str, storage_class: 'type[StorageInterface]') -> None
```

Új tárolási típus regisztrálása a factory számára.

**Paraméterek:**

- **`cls`**
- **`storage_type`** (`str`): A tárolási típus egyedi azonosítója (pl. 'file', 's3').
- **`storage_class`** (`'type[StorageInterface]'`): A tárolási osztály, amely megvalósítja a StorageInterface-t.

**Visszatérési érték:**

- Típus: `None`

**Kivételek:**

- **`NotImplementedError`**: Ha az alosztály nem valósítja meg ezt a metódust.

#### `get_storage()`

```python
def get_storage(cls, logger: 'LoggerInterface | None' = None, config: 'ConfigManagerInterface | None' = None, event_bus: 'EventBusInterface | None' = None, storage_type: str = 'file', base_path: str | Path | None = None, hardware: 'HardwareInterface | None' = None) -> 'StorageInterface'
```

Tárolási példány létrehozása a megadott típus alapján.

**Paraméterek:**

- **`cls`**
- **`logger`** (`'LoggerInterface | None'`) = `None`: A naplózásért felelős interfész (opcionális, alapértelmezett: új példány).
- **`config`** (`'ConfigManagerInterface | None'`) = `None`: A konfigurációért felelős interfész (opcionális, alapértelmezett: új példány).
- **`event_bus`** (`'EventBusInterface | None'`) = `None`: Az eseménybusz interfész (opcionális, alapértelmezett: új példány).
- **`storage_type`** (`str`) = `'file'`: A kért tárolási típus azonosítója. Alapértelmezett: 'file'.
- **`base_path`** (`str | Path | None`) = `None`: Az alap könyvtár útvonala a fájl alapú tároláshoz.
- **`hardware`** (`'HardwareInterface | None'`) = `None`: A hardverképességek detektálásáért felelős interfész (opcionális). **kwargs: További, a tárolási implementáció specifikus paraméterek.

**Visszatérési érték:**

- Típus: `'StorageInterface'`
- StorageInterface: Egy inicializált tárolási példány.

**Kivételek:**

- **`NotImplementedError`**: Ha az alosztály nem valósítja meg ezt a metódust.
- **`KeyError`**: Ha a megadott tárolási típus nincs regisztrálva.
- **`ValueError`**: Ha a megadott paraméterek érvénytelenek.

---

**Forrásfájl:** [`neural_ai/data/storage/interfaces/factory_interface.py`](../../neural_ai/data/storage/interfaces/factory_interface.py)
