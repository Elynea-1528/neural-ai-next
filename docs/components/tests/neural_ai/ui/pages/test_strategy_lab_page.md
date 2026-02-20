# tests/neural_ai/ui/pages/test_strategy_lab_page.py

Tesztelési modul a Strategy Lab oldalhoz.

Ez a modul tartalmazza a StrategyLabPage osztály egységtesztjeit,
amelyek ellenőrzik az oldal alapvető funkcionalitását és a session_state persistence-t.

## Importok

```python
import importlib.util
import sys
from datetime import date
from unittest.mock import MagicMock
from unittest.mock import patch
import pytest
from neural_ai.ui.interfaces.core_bridge_interface import CoreBridgeInterface
from neural_ai.ui.interfaces.strategy_service_interface import StrategyServiceInterface
import pandas
import pandas
# ... és még 2 import
```

## Konstansok

- **`spec`**
: `importlib.util.spec_from_file_location('strategy_lab_page', 'neural_ai/ui/pages/05_🪲_Strategy_Lab.py')`


- **`strategy_lab_module`**
: `importlib.util.module_from_spec(spec)`


- **`StrategyLabPage`**
: `strategy_lab_module.StrategyLabPage`


## Osztály: `TestStrategyLabPage`

StrategyLabPage osztály tesztjei.

Ezek a tesztek ellenőrzik az oldal inicializálását, renderelését,
navigációs metódusait és a szimbólum lekérést.

### Metódusok

#### `mock_bridge()`

```python
def mock_bridge(self) -> MagicMock
```

Mock CoreBridgeInterface létrehozása.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `MagicMock`
- MagicMock: A mockolt bridge példány.

#### `strategy_lab_page()`

```python
def strategy_lab_page(self, mock_bridge: MagicMock) -> StrategyLabPage
```

StrategyLabPage példány létrehozása teszteléshez.

**Paraméterek:**

- **`self`**
- **`mock_bridge`** (`MagicMock`): A mockolt bridge példány.

**Visszatérési érték:**

- Típus: `StrategyLabPage`
- StrategyLabPage: A tesztelendő oldal példány.

#### `test_init()`

```python
def test_init(self, mock_bridge: MagicMock) -> None
```

Teszteli az osztály inicializálását.

**Paraméterek:**

- **`self`**
- **`mock_bridge`** (`MagicMock`): A mockolt bridge példány.

**Visszatérési érték:**

- Típus: `None`

#### `test_init_with_kwargs()`

```python
def test_init_with_kwargs(self, mock_bridge: MagicMock) -> None
```

Teszteli az inicializálást további paraméterekkel.

**Paraméterek:**

- **`self`**
- **`mock_bridge`** (`MagicMock`): A mockolt bridge példány.

**Visszatérési érték:**

- Típus: `None`

#### `test_title_property()`

```python
def test_title_property(self, strategy_lab_page: StrategyLabPage) -> None
```

Teszteli a title property-t.

**Paraméterek:**

- **`self`**
- **`strategy_lab_page`** (`StrategyLabPage`): A tesztelendő oldal példány.

**Visszatérési érték:**

- Típus: `None`

#### `test_is_loaded_property_initial()`

```python
def test_is_loaded_property_initial(self, strategy_lab_page: StrategyLabPage) -> None
```

Teszteli az is_loaded property kezdeti állapotát.

**Paraméterek:**

- **`self`**
- **`strategy_lab_page`** (`StrategyLabPage`): A tesztelendő oldal példány.

**Visszatérési érték:**

- Típus: `None`

#### `test_on_navigate_to_resets_state()`

```python
def test_on_navigate_to_resets_state(self, strategy_lab_page: StrategyLabPage) -> None
```

Teszteli, hogy a navigálás visszaállítja az állapotot (session_state-kel).

**Paraméterek:**

- **`self`**
- **`strategy_lab_page`** (`StrategyLabPage`): A tesztelendő oldal példány.

**Visszatérési érték:**

- Típus: `None`

#### `test_on_navigate_to_with_params()`

```python
def test_on_navigate_to_with_params(self, strategy_lab_page: StrategyLabPage) -> None
```

Teszteli a navigációt paraméterekkel.

**Paraméterek:**

- **`self`**
- **`strategy_lab_page`** (`StrategyLabPage`): A tesztelendő oldal példány.

**Visszatérési érték:**

- Típus: `None`

#### `test_on_navigate_from()`

```python
def test_on_navigate_from(self, strategy_lab_page: StrategyLabPage) -> None
```

Teszteli az oldal elhagyásakor történő akciót.

**Paraméterek:**

- **`self`**
- **`strategy_lab_page`** (`StrategyLabPage`): A tesztelendő oldal példány.

**Visszatérési érték:**

- Típus: `None`

#### `test_get_symbols_from_config()`

```python
def test_get_symbols_from_config(self, mock_bridge: MagicMock) -> None
```

Teszteli a szimbólumok lekérését a konfigurációból.

**Paraméterek:**

- **`self`**
- **`mock_bridge`** (`MagicMock`): A mockolt bridge példány.

**Visszatérési érték:**

- Típus: `None`

#### `test_get_symbols_from_config_empty()`

```python
def test_get_symbols_from_config_empty(self, mock_bridge: MagicMock) -> None
```

Teszteli a szimbólumok lekérését üres konfigurációval.

**Paraméterek:**

- **`self`**
- **`mock_bridge`** (`MagicMock`): A mockolt bridge példány.

**Visszatérési érték:**

- Típus: `None`

#### `test_get_symbols_config_returns_none()`

```python
def test_get_symbols_config_returns_none(self, mock_bridge: MagicMock) -> None
```

Teszteli a szimbólumok lekérését, ha a konfiguráció None.

**Paraméterek:**

- **`self`**
- **`mock_bridge`** (`MagicMock`): A mockolt bridge példány.

**Visszatérési érték:**

- Típus: `None`

#### `test_get_symbols_config_exception()`

```python
def test_get_symbols_config_exception(self, mock_bridge: MagicMock) -> None
```

Teszteli a szimbólumok lekérését, ha a konfiguráció hibát dob.

**Paraméterek:**

- **`self`**
- **`mock_bridge`** (`MagicMock`): A mockolt bridge példány.

**Visszatérési érték:**

- Típus: `None`

#### `test_get_strategy_service_success()`

```python
def test_get_strategy_service_success(self, strategy_lab_page: StrategyLabPage) -> None
```

Teszteli a Strategy Service sikeres lekérését.

**Paraméterek:**

- **`self`**
- **`strategy_lab_page`** (`StrategyLabPage`): A tesztelendő oldal példány.

**Visszatérési érték:**

- Típus: `None`

#### `test_get_strategy_service_exception()`

```python
def test_get_strategy_service_exception(self, strategy_lab_page: StrategyLabPage) -> None
```

Teszteli a Strategy Service lekérését, ha hibát dob.

**Paraméterek:**

- **`self`**
- **`strategy_lab_page`** (`StrategyLabPage`): A tesztelendő oldal példány.

**Visszatérési érték:**

- Típus: `None`

#### `test_render_sidebar()`

```python
def test_render_sidebar(self, mock_info: MagicMock, mock_button: MagicMock, mock_date_input: MagicMock, mock_selectbox: MagicMock, mock_columns: MagicMock, mock_sidebar: MagicMock, mock_markdown: MagicMock, mock_title: MagicMock, strategy_lab_page: StrategyLabPage) -> None
```

Teszteli az oldalsáv renderelését.

**Paraméterek:**

- **`self`**
- **`mock_info`** (`MagicMock`): Mockolt info.
- **`mock_button`** (`MagicMock`): Mockolt button.
- **`mock_date_input`** (`MagicMock`): Mockolt date_input.
- **`mock_selectbox`** (`MagicMock`): Mockolt selectbox.
- **`mock_columns`** (`MagicMock`): Mockolt columns.
- **`mock_sidebar`** (`MagicMock`): Mockolt sidebar.
- **`mock_markdown`** (`MagicMock`): Mockolt markdown.
- **`mock_title`** (`MagicMock`): Mockolt title.
- **`strategy_lab_page`** (`StrategyLabPage`): A tesztelendő oldal példány.

**Visszatérési érték:**

- Típus: `None`

#### `test_render_without_data()`

```python
def test_render_without_data(self, mock_info: MagicMock, mock_button: MagicMock, mock_date_input: MagicMock, mock_selectbox: MagicMock, mock_columns: MagicMock, mock_sidebar: MagicMock, mock_markdown: MagicMock, mock_title: MagicMock, strategy_lab_page: StrategyLabPage) -> None
```

Teszteli a renderelést adatok nélkül.

**Paraméterek:**

- **`self`**
- **`mock_info`** (`MagicMock`): Mockolt info.
- **`mock_button`** (`MagicMock`): Mockolt button.
- **`mock_date_input`** (`MagicMock`): Mockolt date_input.
- **`mock_selectbox`** (`MagicMock`): Mockolt selectbox.
- **`mock_columns`** (`MagicMock`): Mockolt columns.
- **`mock_sidebar`** (`MagicMock`): Mockolt sidebar.
- **`mock_markdown`** (`MagicMock`): Mockolt markdown.
- **`mock_title`** (`MagicMock`): Mockolt title.
- **`strategy_lab_page`** (`StrategyLabPage`): A tesztelendő oldal példány.

**Visszatérési érték:**

- Típus: `None`

#### `test_render_without_errors()`

```python
def test_render_without_errors(self, strategy_lab_page: StrategyLabPage) -> None
```

Teszteli, hogy a render metódus hiba nélkül lefut.

**Paraméterek:**

- **`self`**
- **`strategy_lab_page`** (`StrategyLabPage`): A tesztelendő oldal példány.

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestStrategyLabPageSessionState`

Session State tesztek a Strategy Lab oldalhoz.

Ezek a tesztek ellenőrzik a session_state alapú adat persistence funkcionalitást.

### Metódusok

#### `mock_bridge()`

```python
def mock_bridge(self) -> MagicMock
```

Mock CoreBridgeInterface létrehozása.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `MagicMock`
- MagicMock: A mockolt bridge példány.

#### `strategy_lab_page()`

```python
def strategy_lab_page(self, mock_bridge: MagicMock) -> StrategyLabPage
```

StrategyLabPage példány létrehozása teszteléshez.

**Paraméterek:**

- **`self`**
- **`mock_bridge`** (`MagicMock`): A mockolt bridge példány.

**Visszatérési érték:**

- Típus: `StrategyLabPage`
- StrategyLabPage: A tesztelendő oldal példány.

#### `test_init_session_state_candles_initialization()`

```python
def test_init_session_state_candles_initialization(self, mock_bridge: MagicMock) -> None
```

Teszteli, hogy az __init__ metódus inicializálja a session state candles-t.

**Paraméterek:**

- **`self`**
- **`mock_bridge`** (`MagicMock`): A mockolt bridge példány.

**Visszatérési érték:**

- Típus: `None`

#### `test_render_syncs_session_state_candles()`

```python
def test_render_syncs_session_state_candles(self, mock_bridge: MagicMock) -> None
```

Teszteli, hogy a render metódus szinkronizálja a session state candles értékét.

**Paraméterek:**

- **`self`**
- **`mock_bridge`** (`MagicMock`): A mockolt bridge példány.

**Visszatérési érték:**

- Típus: `None`

#### `test_on_navigate_to_clears_session_state()`

```python
def test_on_navigate_to_clears_session_state(self, mock_bridge: MagicMock) -> None
```

Teszteli, hogy az on_navigate_to metódus törli a session state candles értékét.

**Paraméterek:**

- **`self`**
- **`mock_bridge`** (`MagicMock`): A mockolt bridge példány.

**Visszatérési érték:**

- Típus: `None`

#### `test_candles_persistence_between_interactions()`

```python
def test_candles_persistence_between_interactions(self, mock_bridge: MagicMock) -> None
```

Teszteli, hogy a gyertyák megmaradnak a felhasználói interakciók között.

**Paraméterek:**

- **`self`**
- **`mock_bridge`** (`MagicMock`): A mockolt bridge példány.

**Visszatérési érték:**

- Típus: `None`

#### `test_backtest_result_persistence()`

```python
def test_backtest_result_persistence(self, mock_bridge: MagicMock) -> None
```

Teszteli, hogy a backteszt eredménye megmarad a session state-ben.

**Paraméterek:**

- **`self`**
- **`mock_bridge`** (`MagicMock`): A mockolt bridge példány.

**Visszatérési érték:**

- Típus: `None`

#### `test_price_type_session_state_initialization()`

```python
def test_price_type_session_state_initialization(self, mock_bridge: MagicMock) -> None
```

Teszteli a price_type session state inicializálását.

**Paraméterek:**

- **`self`**
- **`mock_bridge`** (`MagicMock`): A mockolt bridge példány.

**Visszatérési érték:**

- Típus: `None`

#### `test_render_data_table_with_price_type_bid()`

```python
def test_render_data_table_with_price_type_bid(self, strategy_lab_page: StrategyLabPage) -> None
```

Teszteli a _render_data_table metódust Bid price type-pal.

**Paraméterek:**

- **`self`**
- **`strategy_lab_page`** (`StrategyLabPage`): A tesztelendő oldal példány.

**Visszatérési érték:**

- Típus: `None`

#### `test_render_data_table_with_price_type_mid()`

```python
def test_render_data_table_with_price_type_mid(self, strategy_lab_page: StrategyLabPage) -> None
```

Teszteli a _render_data_table metódust Mid price type-pal.

**Paraméterek:**

- **`self`**
- **`strategy_lab_page`** (`StrategyLabPage`): A tesztelendő oldal példány.

**Visszatérési érték:**

- Típus: `None`

#### `test_render_candlestick_chart_with_bid_price_type()`

```python
def test_render_candlestick_chart_with_bid_price_type(self, mock_candlestick: MagicMock, mock_figure: MagicMock, mock_plotly_chart: MagicMock, strategy_lab_page: StrategyLabPage) -> None
```

Teszteli a candlestick chart renderelését Bid price type-pal.

**Paraméterek:**

- **`self`**
- **`mock_candlestick`** (`MagicMock`): Mockolt Candlestick.
- **`mock_figure`** (`MagicMock`): Mockolt Figure.
- **`mock_plotly_chart`** (`MagicMock`): Mockolt plotly_chart.
- **`strategy_lab_page`** (`StrategyLabPage`): A tesztelendő oldal példány.

**Visszatérési érték:**

- Típus: `None`

#### `test_render_candlestick_chart_with_mid_price_type()`

```python
def test_render_candlestick_chart_with_mid_price_type(self, mock_candlestick: MagicMock, mock_figure: MagicMock, mock_plotly_chart: MagicMock, strategy_lab_page: StrategyLabPage) -> None
```

Teszteli a candlestick chart renderelését Mid price type-pal.

**Paraméterek:**

- **`self`**
- **`mock_candlestick`** (`MagicMock`): Mockolt Candlestick.
- **`mock_figure`** (`MagicMock`): Mockolt Figure.
- **`mock_plotly_chart`** (`MagicMock`): Mockolt plotly_chart.
- **`strategy_lab_page`** (`StrategyLabPage`): A tesztelendő oldal példány.

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/neural_ai/ui/pages/test_strategy_lab_page.py`](../../tests/neural_ai/ui/pages/test_strategy_lab_page.py)
