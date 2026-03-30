# neural_ai/ui/pages/02_🛠️_Dev_Center.py

Dev Center Page - Fejlesztői központ.

Ez a modul implementálja a fejlesztői központ oldalt.

## Importok

```python
import streamlit
from neural_ai.ui.interfaces.core_bridge_interface import CoreBridgeInterface
from neural_ai.ui.interfaces.page_interface import PageInterface
from neural_ai.ui.core_bridge import CoreBridge
```

## Konstansok

- **`bridge`**
: `CoreBridge()`


- **`page`**
: `DevCenterPage(bridge)`


## Osztály: `DevCenterPage(PageInterface)`

Dev Center oldal.

### Metódusok

#### `__init__()`

```python
def __init__(self, bridge: CoreBridgeInterface) -> None
```

A Dev Center oldal inicializálása.

**Paraméterek:**

- **`self`**
- **`bridge`** (`CoreBridgeInterface`): A backend bridge példány **kwargs: További opcionális paraméterek

**Visszatérési érték:**

- Típus: `None`

#### `render()`

```python
def render(self) -> None
```

A Dev Center oldal megjelenítése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `on_navigate_to()`

```python
def on_navigate_to(self, params: dict[str, object] | None = None) -> None
```

Navigálás az oldalra.

**Paraméterek:**

- **`self`**
- **`params`** (`dict[str, object] | None`) = `None`: Opcionális navigációs paraméterek

**Visszatérési érték:**

- Típus: `None`

#### `on_navigate_from()`

```python
def on_navigate_from(self) -> None
```

Navigálás az oldalról.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `title()`

```python
def title(self) -> str
```

Az oldal címe.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `str`
- str: Az oldal címe

#### `is_loaded()`

```python
def is_loaded(self) -> bool
```

Az oldal betöltött állapota.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `bool`
- bool: True, ha az oldal betöltött

---

**Forrásfájl:** [`neural_ai/ui/pages/02_🛠️_Dev_Center.py`](../../neural_ai/ui/pages/02_🛠️_Dev_Center.py)
