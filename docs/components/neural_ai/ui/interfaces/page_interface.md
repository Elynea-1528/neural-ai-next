# neural_ai/ui/interfaces/page_interface.py

Page interfész definíciója.

Ez az interfész definiálja az oldal komponensek szerződését.

## Importok

```python
from typing import TYPE_CHECKING
from typing import Protocol
from typing import runtime_checkable
from neural_ai.ui.interfaces.core_bridge_interface import CoreBridgeInterface
```

## Osztály: `PageInterface(Protocol)`

Page interfész - Oldal komponensek alapja.

Ez az interfész definiálja az oldalak által implementálandó metódusokat.

### Metódusok

#### `__init__()`

```python
def __init__(self, bridge: 'CoreBridgeInterface') -> None
```

Oldal inicializálása.

**Paraméterek:**

- **`self`**
- **`bridge`** (`'CoreBridgeInterface'`): A backend bridge példány **kwargs: További paraméterek

**Visszatérési érték:**

- Típus: `None`

#### `render()`

```python
def render(self) -> object
```

Az oldal tartalmának renderelése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `object`
- Any: A renderelt tartalom

#### `on_navigate_to()`

```python
def on_navigate_to(self, params: dict[str, object] | None = None) -> None
```

Akció, amikor az oldalra navigálnak.

**Paraméterek:**

- **`self`**
- **`params`** (`dict[str, object] | None`) = `None`: Navigációs paraméterek

**Visszatérési érték:**

- Típus: `None`

#### `on_navigate_from()`

```python
def on_navigate_from(self) -> None
```

Akció, amikor elnavigálnak az oldalról.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `title()`

```python
def title(self) -> str
```

Az oldal címét visszaadó property.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `str`
- str: Az oldal címe

#### `is_loaded()`

```python
def is_loaded(self) -> bool
```

Az oldal betöltöttségi állapotát ellenőrző property.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `bool`
- bool: True, ha az oldal betöltött, egyébként False

---

**Forrásfájl:** [`neural_ai/ui/interfaces/page_interface.py`](../../neural_ai/ui/interfaces/page_interface.py)
