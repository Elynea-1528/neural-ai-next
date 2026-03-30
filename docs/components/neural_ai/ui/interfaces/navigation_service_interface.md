# neural_ai/ui/interfaces/navigation_service_interface.py

Navigation Service interfész definíciója.

Ez az interfész definiálja a navigációs szolgáltatás szerződését,
amely az oldalak közötti navigációt kezeli.

## Importok

```python
from collections.abc import Callable
from typing import TYPE_CHECKING
from typing import Optional
from typing import Protocol
from typing import runtime_checkable
from neural_ai.ui.interfaces.page_interface import PageInterface
```

## Osztály: `NavigationServiceInterface(Protocol)`

Navigation Service interfész - Oldalak közötti navigációért felelős.

Ez az interfész definiálja a navigációs logikát kezelő metódusokat.

### Metódusok

#### `navigate_to()`

```python
def navigate_to(self, page_name: str, params: dict[str, object] | None = None) -> None
```

Navigálás egy adott oldalra.

**Paraméterek:**

- **`self`**
- **`page_name`** (`str`): A céloldal neve
- **`params`** (`dict[str, object] | None`) = `None`: Navigációs paraméterek

**Visszatérési érték:**

- Típus: `None`

#### `go_back()`

```python
def go_back(self) -> None
```

Visszalépés az előző oldalra.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `get_current_page()`

```python
def get_current_page(self) -> Optional['PageInterface']
```

Az aktuális oldal lekérdezése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `Optional['PageInterface']`
- Optional[PageInterface]: Az aktuális oldal vagy None

#### `get_page_history()`

```python
def get_page_history(self) -> list[str]
```

A navigációs előzmények lekérdezése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `list[str]`
- list[str]: Az oldalnevek listája

#### `register_page()`

```python
def register_page(self, page_name: str, page: 'PageInterface') -> None
```

Oldal regisztrálása a navigációs rendszerben.

**Paraméterek:**

- **`self`**
- **`page_name`** (`str`): Az oldal neve
- **`page`** (`'PageInterface'`): Az oldal példánya

**Visszatérési érték:**

- Típus: `None`

#### `subscribe()`

```python
def subscribe(self, callback: Callable[[str, dict[str, object]], None]) -> None
```

Feliratkozás navigációs eseményekre.

**Paraméterek:**

- **`self`**
- **`callback`** (`Callable[[str, dict[str, object]], None]`): A hívandó callback függvény

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`neural_ai/ui/interfaces/navigation_service_interface.py`](../../neural_ai/ui/interfaces/navigation_service_interface.py)
