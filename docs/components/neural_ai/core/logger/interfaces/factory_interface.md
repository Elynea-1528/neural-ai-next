# neural_ai/core/logger/interfaces/factory_interface.py

Logger factory interfész.

Ez az interfész definiálja a logger factory-k alapvető működését,
beleértve a logger típusok regisztrálását, példányosítását és
a logger rendszer konfigurálását.

## Importok

```python
from abc import ABC
from abc import abstractmethod
from typing import Any
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
```

## Osztály: `LoggerFactoryInterface(ABC)`

Logger factory interfész.

Az interfész lehetővé teszi különböző logger implementációk
dinamikus regisztrálását és példányosítását factory pattern
segítségével.

### Metódusok

#### `register_logger()`

```python
def register_logger(cls, logger_type: str, logger_class: type[LoggerInterface]) -> None
```

Új logger típus regisztrálása a factory számára.

**Paraméterek:**

- **`cls`**
- **`logger_type`** (`str`): A logger típus egyedi azonosítója
- **`logger_class`** (`type[LoggerInterface]`): A logger osztály, amely implementálja a LoggerInterface-t

**Visszatérési érték:**

- Típus: `None`

**Kivételek:**

- **`ValueError`**: Ha a logger_type már létezik
- **`TypeError`**: Ha a logger_class nem implementálja a LoggerInterface-t

#### `get_logger()`

```python
def get_logger(cls, name: str, logger_type: str = 'default') -> LoggerInterface
```

Logger példány létrehozása vagy visszaadása.

**Paraméterek:**

- **`cls`**
- **`name`** (`str`): A logger egyedi neve
- **`logger_type`** (`str`) = `'default'`: A kért logger típus (alapértelmezett: "default") **kwargs: További paraméterek a logger inicializálásához

**Visszatérési érték:**

- Típus: `LoggerInterface`
- LoggerInterface: Az inicializált logger példány

**Kivételek:**

- **`KeyError`**: Ha a logger_type nincs regisztrálva
- **`ValueError`**: Ha a name üres string

#### `configure()`

```python
def configure(cls, config: dict[str, Any]) -> None
```

Logger rendszer konfigurálása.

**Paraméterek:**

- **`cls`**
- **`config`** (`dict[str, Any]`): Konfigurációs beállítások dictionary formátumban

**Visszatérési érték:**

- Típus: `None`

**Kivételek:**

- **`ValueError`**: Ha a konfiguráció érvénytelen

---

**Forrásfájl:** [`neural_ai/core/logger/interfaces/factory_interface.py`](../../neural_ai/core/logger/interfaces/factory_interface.py)
