# neural_ai/ui/components/base_widget.py

Base Widget - Alap widget osztály.

Ez a modul implementálja az alap widget osztályt, amelyet
az összes UI komponens örököl.

## Importok

```python
from typing import Any
```

## Osztály: `BaseWidget`

Base Widget - Alap widget osztály.

Ez az osztály az összes UI komponens alapját képezi.

### Metódusok

#### `__init__()`

```python
def __init__(self, config: dict[str, Any] | None = None) -> None
```

A widget inicializálása.

**Paraméterek:**

- **`self`**
- **`config`** (`dict[str, Any] | None`) = `None`: A widget konfigurációja

**Visszatérési érték:**

- Típus: `None`

#### `render()`

```python
def render(self) -> str
```

A widget tartalmának renderelése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `str`
- str: A renderelt tartalom

#### `show()`

```python
def show(self) -> None
```

A widget megjelenítése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `hide()`

```python
def hide(self) -> None
```

A widget elrejtése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `is_visible()`

```python
def is_visible(self) -> bool
```

A widget láthatóságát ellenőrző property.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `bool`
- bool: True, ha a widget látható, egyébként False

---

**Forrásfájl:** [`neural_ai/ui/components/base_widget.py`](../../neural_ai/ui/components/base_widget.py)
