# neural_ai/ui/interfaces/dashboard_service_interface.py

Dashboard Service interfész definíciója.

Ez az interfész definiálja a dashboard szolgáltatás szerződését,
amely a fő irányítópult adatait és állapotát kezeli.

## Importok

```python
from typing import TYPE_CHECKING
from typing import Any
from typing import Protocol
from typing import runtime_checkable
```

## Osztály: `DashboardServiceInterface(Protocol)`

Dashboard Service interfész - Fő irányítópult kezeléséért felelős.

Ez az interfész definiálja a dashboard adatok lekérdezését és
kezelését végző metódusokat.

### Metódusok

#### `get_system_overview()`

```python
def get_system_overview(self) -> dict[str, Any]
```

Rendszer áttekintő adatok lekérdezése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `dict[str, Any]`
- Dict[str, Any]: A rendszer aktuális állapota

#### `get_health_status()`

```python
def get_health_status(self) -> dict[str, str]
```

Rendszer egészségügyi állapotának lekérdezése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `dict[str, str]`
- Dict[str, str]: A komponensek állapota (OK/ERROR/WARNING)

#### `get_performance_metrics()`

```python
def get_performance_metrics(self) -> dict[str, float]
```

Teljesítmény metrikák lekérdezése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `dict[str, float]`
- Dict[str, float]: A rendszer teljesítményadatok

#### `get_recent_activities()`

```python
def get_recent_activities(self) -> list[dict[str, Any]]
```

Legutóbbi tevékenységek lekérdezése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `list[dict[str, Any]]`
- List[Dict[str, Any]]: A tevékenységek listája

#### `refresh_data()`

```python
def refresh_data(self) -> None
```

Dashboard adatok frissítése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `subscribe_to_updates()`

```python
def subscribe_to_updates(self, callback: Any) -> None
```

Feliratkozás dashboard frissítésekre.

**Paraméterek:**

- **`self`**
- **`callback`** (`Any`): A hívandó callback függvény

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`neural_ai/ui/interfaces/dashboard_service_interface.py`](../../neural_ai/ui/interfaces/dashboard_service_interface.py)
