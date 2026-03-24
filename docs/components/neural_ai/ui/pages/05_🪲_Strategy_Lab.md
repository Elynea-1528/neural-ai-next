# neural_ai/ui/pages/05_🪲_Strategy_Lab.py

Strategy Lab Page - Stratégia fejlesztő labor.

Ez a modul implementálja a Strategy Lab oldalt, ahol a felhasználók
interaktív módon vizsgálhatják a gyertyadiagramokat és stratégiákat.

## Importok

```python
from datetime import date
from typing import TYPE_CHECKING
from typing import Any
import pandas
import polars
import streamlit
from neural_ai.ui.interfaces.page_interface import PageInterface
from neural_ai.ui.interfaces.core_bridge_interface import CoreBridgeInterface
from neural_ai.ui.interfaces.strategy_service_interface import StrategyServiceInterface
import plotly.graph_objects
# ... és még 4 import
```

## Konstansok

- **`bridge`**
: `CoreBridge()`


- **`page`**
: `StrategyLabPage(bridge)`


## Osztály: `StrategyLabPage(PageInterface)`

Strategy Lab oldal - Interaktív stratégia vizualizáció.

Ez az osztály implementálja a Strategy Lab felületét, amely lehetővé
teszi a felhasználók számára a gyertyadiagramok megjelenítését és
a stratégiák tesztelését.

### Metódusok

#### `__init__()`

```python
def __init__(self, bridge: 'CoreBridgeInterface') -> None
```

A Strategy Lab oldal inicializálása.

**Paraméterek:**

- **`self`**
- **`bridge`** (`'CoreBridgeInterface'`): A backend bridge példány **kwargs: További opcionális paraméterek

**Visszatérési érték:**

- Típus: `None`

#### `render()`

```python
def render(self) -> None
```

A Strategy Lab oldal megjelenítése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `_render_sidebar()`

```python
def _render_sidebar(self) -> None
```

Oldalsáv megjelenítése szűrőkkel és beállításokkal.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `_render_main_area()`

```python
def _render_main_area(self) -> None
```

Fő terület megjelenítése diagrammal és táblázattal.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `_render_backtest_results()`

```python
def _render_backtest_results(self) -> None
```

Backtest eredmények megjelenítése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `_prepare_data_for_view()`

```python
def _prepare_data_for_view(self, df: pd.DataFrame, price_type: str) -> pd.DataFrame
```

Adatok előkészítése megjelenítéshez - oszlopok átnevezése price_type alapján.

**Paraméterek:**

- **`self`**
- **`df`** (`pd.DataFrame`): Az eredeti Pandas DataFrame
- **`price_type`** (`str`): Az ár típus ('Bid' vagy 'Mid')

**Visszatérési érték:**

- Típus: `pd.DataFrame`
- pd.DataFrame: Az átnevezett oszlopokkal rendelkező Pandas DataFrame

#### `_render_candlestick_chart()`

```python
def _render_candlestick_chart(self, signals: dict[str, list[int]] | None = None) -> None
```

Interaktív Plotly candlestick chart megjelenítése jelekkel.

**Paraméterek:**

- **`self`**
- **`signals`** (`dict[str, list[int]] | None`) = `None`

**Visszatérési érték:**

- Típus: `None`

#### `_render_data_table()`

```python
def _render_data_table(self) -> None
```

Az első 10 sor megjelenítése táblázatban Spread és Z-Score oszlopokkal.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `_get_symbols()`

```python
def _get_symbols(self) -> list[str]
```

Szimbólumok lekérése a konfigurációból.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `list[str]`
- List[str]: Az elérhető szimbólumok listája

#### `_load_and_visualize()`

```python
def _load_and_visualize(self, symbol: str, selected_date: date, timeframe: str) -> None
```

Adatok betöltése és vizualizálása.

**Paraméterek:**

- **`self`**
- **`symbol`** (`str`): A kiválasztott szimbólum
- **`selected_date`** (`date`): A kiválasztott dátum
- **`timeframe`** (`str`): A kiválasztott idősík

**Visszatérési érték:**

- Típus: `None`

#### `_run_backtest()`

```python
def _run_backtest(self, symbol: str, date: str, timeframe: str, fast_period: int, slow_period: int, initial_capital: float) -> None
```

VectorBT backteszt futtatása.

**Paraméterek:**

- **`self`**
- **`symbol`** (`str`): A kiválasztott szimbólum
- **`date`** (`str`): A kiválasztott dátum
- **`timeframe`** (`str`): A kiválasztott idősík
- **`fast_period`** (`int`): A gyors SMA periódusa
- **`slow_period`** (`int`): A lassú SMA periódusa
- **`initial_capital`** (`float`): A kezdeti tőke

**Visszatérési érték:**

- Típus: `None`

#### `_get_strategy_service()`

```python
def _get_strategy_service(self) -> 'StrategyServiceInterface | None'
```

Strategy Service példány lekérése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `'StrategyServiceInterface | None'`
- StrategyServiceInterface: A Strategy Service vagy None

#### `on_navigate_to()`

```python
def on_navigate_to(self, params: 'dict[str, Any] | None' = None) -> None
```

Navigálás az oldalra.

**Paraméterek:**

- **`self`**
- **`params`** (`'dict[str, Any] | None'`) = `None`: Opcionális navigációs paraméterek

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

**Forrásfájl:** [`neural_ai/ui/pages/05_🪲_Strategy_Lab.py`](../../neural_ai/ui/pages/05_🪲_Strategy_Lab.py)
