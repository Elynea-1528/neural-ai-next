# neural_ai/ui/interfaces/core_bridge_interface.py

Core Bridge interfész definíciója.

Ez az interfész definiálja a backend rendszerrel való kommunikációt
biztosító osztályok szerződését.

## Importok

```python
from typing import TYPE_CHECKING
from typing import Protocol
from typing import runtime_checkable
```

## Osztály: `CoreBridgeInterface(Protocol)`

Core Bridge interfész - Backend kapcsolatért felelős.

Ez az interfész definiálja a backend rendszerrel való kommunikációt
biztosító metódusokat Singleton minta szerint.

### Metódusok

#### `get_instance()`

```python
def get_instance(self) -> 'CoreBridgeInterface'
```

A Singleton példányt visszaadó metódus.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `'CoreBridgeInterface'`
- CoreBridgeInterface: A Singleton példány

#### `initialize()`

```python
def initialize(self) -> None
```

A bridge inicializálása a backend core komponensekkel. Ez a metódus elindítja a bootstrap_core() függvényt, amely inicializálja az összes core komponenst.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `get_component()`

```python
def get_component(self, component_type: str) -> object | None
```

Komponens lekérése a backend rendszerből.

**Paraméterek:**

- **`self`**
- **`component_type`** (`str`): A lekérdezni kívánt komponens típusa

**Visszatérési érték:**

- Típus: `object | None`
- Optional[Any]: A lekérdezett komponens vagy None

#### `send_command()`

```python
def send_command(self, command: str, params: dict[str, object]) -> dict[str, object]
```

Parancs küldése a backend rendszernek.

**Paraméterek:**

- **`self`**
- **`command`** (`str`): A végrehajtandó parancs
- **`params`** (`dict[str, object]`): A parancshoz tartozó paraméterek

**Visszatérési érték:**

- Típus: `dict[str, object]`
- Dict[str, Any]: A parancs válasza

#### `get_system_info()`

```python
def get_system_info(self) -> dict[str, object]
```

Rendszerinformáció lekérése a backendről.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `dict[str, object]`
- Dict[str, Any]: A rendszer aktuális állapotinformációi

#### `is_connected()`

```python
def is_connected(self) -> bool
```

A backendkel való kapcsolat állapotát ellenőrző property.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `bool`
- bool: True, ha a kapcsolat aktív, egyébként False

---

**Forrásfájl:** [`neural_ai/ui/interfaces/core_bridge_interface.py`](../../neural_ai/ui/interfaces/core_bridge_interface.py)
