# neural_ai/core/logger/interfaces/logger_interface.py

Logger interfész definíció a naplózási rendszer számára.

## Importok

```python
from abc import ABC
from abc import abstractmethod
from typing import TYPE_CHECKING
from typing import Optional
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.events.interfaces.event_bus_interface import EventBusInterface
```

## Osztály: `LoggerInterface(ABC)`

Logger interfész a naplózási műveletek absztrakt definíciójához.

Ez az interfész definiálja azokat a metódusokat, amelyeket minden logger
implementációnak implementálnia kell a konzisztens naplózási viselkedés
érdekében.

### Metódusok

#### `__init__()`

```python
def __init__(self, name: str, config: Optional['ConfigManagerInterface'] = None, event_bus: Optional['EventBusInterface'] = None) -> None
```

Logger inicializálása.

**Paraméterek:**

- **`self`**
- **`name`** (`str`): A logger egyedi azonosítója.
- **`config`** (`Optional['ConfigManagerInterface']`) = `None`: Opcionális konfigurációs interfész a logger beállításaihoz.
- **`event_bus`** (`Optional['EventBusInterface']`) = `None`: Opcionális esemény busz interfész az aszinkron kommunikációhoz. **kwargs: További opcionális paraméterek (pl. file_path, level).

**Visszatérési érték:**

- Típus: `None`

#### `debug()`

```python
def debug(self, message: str) -> None
```

Debug szintű üzenet naplózása. Részletes hibakeresési információk naplózására szolgál, amelyek általában csak fejlesztés közben relevánsak.

**Paraméterek:**

- **`self`**
- **`message`** (`str`): A naplózandó üzenet szövege. **kwargs: További kontextusparaméterek (pl. extra, exc_info).

**Visszatérési érték:**

- Típus: `None`

#### `info()`

```python
def info(self, message: str) -> None
```

Információs szintű üzenet naplózása. Általános információk naplózására szolgál, amelyek a rendszer normál működéséről adnak tájékoztatást.

**Paraméterek:**

- **`self`**
- **`message`** (`str`): A naplózandó üzenet szövege. **kwargs: További kontextusparaméterek (pl. extra, exc_info).

**Visszatérési érték:**

- Típus: `None`

#### `warning()`

```python
def warning(self, message: str) -> None
```

Figyelmeztető szintű üzenet naplózása. Olyan helyzetek naplózására szolgál, amelyek nem kritikusak, de figyelmet igényelnek.

**Paraméterek:**

- **`self`**
- **`message`** (`str`): A naplózandó üzenet szövege. **kwargs: További kontextusparaméterek (pl. extra, exc_info).

**Visszatérési érték:**

- Típus: `None`

#### `error()`

```python
def error(self, message: str) -> None
```

Hiba szintű üzenet naplózása. Hibák naplózására szolgál, amelyek befolyásolják a rendszer működését, de nem okoznak alkalmazásleállást.

**Paraméterek:**

- **`self`**
- **`message`** (`str`): A naplózandó üzenet szövege. **kwargs: További kontextusparaméterek (pl. extra, exc_info).

**Visszatérési érték:**

- Típus: `None`

#### `critical()`

```python
def critical(self, message: str) -> None
```

Kritikus szintű üzenet naplózása. Súlyos hibák naplózására szolgál, amelyek alkalmazásleállást okozhatnak.

**Paraméterek:**

- **`self`**
- **`message`** (`str`): A naplózandó üzenet szövege. **kwargs: További kontextusparaméterek (pl. extra, exc_info).

**Visszatérési érték:**

- Típus: `None`

#### `set_level()`

```python
def set_level(self, level: int) -> None
```

Logger naplózási szintjének beállítása. Beállítja a minimális naplózási szintet. A szintnél alacsonyabb prioritású üzenetek nem lesznek naplózva.

**Paraméterek:**

- **`self`**
- **`level`** (`int`): Az új naplózási szint (0-50 közötti egész szám).

**Visszatérési érték:**

- Típus: `None`

#### `get_level()`

```python
def get_level(self) -> int
```

Aktuális naplózási szint lekérdezése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `int`
- int: A jelenleg beállított naplózási szint értéke.

---

**Forrásfájl:** [`neural_ai/core/logger/interfaces/logger_interface.py`](../../neural_ai/core/logger/interfaces/logger_interface.py)
