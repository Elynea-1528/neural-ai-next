# neural_ai/ui/interfaces/live_ops_service_interface.py

Live Ops Service interfész definíciója.

Ez az interfész definiálja a live műveletek szolgáltatás szerződését,
amely a valós idejű kereskedést és monitorozást végzi.

## Importok

```python
from typing import TYPE_CHECKING
from typing import Any
from typing import Protocol
from typing import runtime_checkable
```

## Osztály: `LiveOpsServiceInterface(Protocol)`

Live Ops Service interfész - Valós idejű műveletekért felelős.

Ez az interfész definiálja a live kereskedést és monitorozást
végző metódusokat.

### Metódusok

#### `get_active_positions()`

```python
def get_active_positions(self) -> list[dict[str, Any]]
```

Aktív pozíciók lekérdezése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `list[dict[str, Any]]`
- List[Dict[str, Any]]: Az aktív pozíciók listája

#### `get_account_status()`

```python
def get_account_status(self) -> dict[str, Any]
```

Fiók állapotának lekérdezése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `dict[str, Any]`
- Dict[str, Any]: A fiók aktuális állapota

#### `place_order()`

```python
def place_order(self, symbol: str, order_type: str, volume: float, price: float | None = None, stop_loss: float | None = None, take_profit: float | None = None) -> str
```

Új rendelés leadása.

**Paraméterek:**

- **`self`**
- **`symbol`** (`str`): A kereskedendő szimbólum
- **`order_type`** (`str`): A rendelés típusa (BUY/SELL)
- **`volume`** (`float`): A kereskedési volumen
- **`price`** (`float | None`) = `None`: A rendelés ára (opcionális)
- **`stop_loss`** (`float | None`) = `None`: Stop loss szint (opcionális)
- **`take_profit`** (`float | None`) = `None`: Take profit szint (opcionális)

**Visszatérési érték:**

- Típus: `str`
- str: A rendelés azonosítója

#### `modify_order()`

```python
def modify_order(self, order_id: str, price: float | None = None, stop_loss: float | None = None, take_profit: float | None = None) -> bool
```

Meglévő rendelés módosítása.

**Paraméterek:**

- **`self`**
- **`order_id`** (`str`): A rendelés azonosítója
- **`price`** (`float | None`) = `None`: Az új ár
- **`stop_loss`** (`float | None`) = `None`: Az új stop loss
- **`take_profit`** (`float | None`) = `None`: Az új take profit

**Visszatérési érték:**

- Típus: `bool`
- bool: True, ha sikeres a módosítás

#### `cancel_order()`

```python
def cancel_order(self, order_id: str) -> bool
```

Rendelés visszavonása.

**Paraméterek:**

- **`self`**
- **`order_id`** (`str`): A rendelés azonosítója

**Visszatérési érték:**

- Típus: `bool`
- bool: True, ha sikeres a visszavonás

#### `close_position()`

```python
def close_position(self, position_id: str) -> bool
```

Pozíció lezárása.

**Paraméterek:**

- **`self`**
- **`position_id`** (`str`): A pozíció azonosítója

**Visszatérési érték:**

- Típus: `bool`
- bool: True, ha sikeres a lezárás

#### `get_market_data()`

```python
def get_market_data(self, symbol: str) -> dict[str, Any]
```

Piaci adatok lekérdezése.

**Paraméterek:**

- **`self`**
- **`symbol`** (`str`): A szimbólum

**Visszatérési érték:**

- Típus: `dict[str, Any]`
- Dict[str, Any]: A piaci adatok

#### `subscribe_to_market_updates()`

```python
def subscribe_to_market_updates(self, symbol: str, callback: Any) -> None
```

Feliratkozás piaci frissítésekre.

**Paraméterek:**

- **`self`**
- **`symbol`** (`str`): A szimbólum
- **`callback`** (`Any`): A hívandó callback függvény

**Visszatérési érték:**

- Típus: `None`

#### `get_performance_summary()`

```python
def get_performance_summary(self) -> dict[str, Any]
```

Teljesítmény összegzés lekérdezése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `dict[str, Any]`
- Dict[str, Any]: A teljesítmény adatok

---

**Forrásfájl:** [`neural_ai/ui/interfaces/live_ops_service_interface.py`](../../neural_ai/ui/interfaces/live_ops_service_interface.py)
