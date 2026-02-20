# tests/neural_ai/ui/services/test_strategy_service.py

Strategy Service tesztek.

Ez a modul tartalmazza a StrategyService osztály tesztjeit,
beleértve az új get_candles metódust.

## Importok

```python
import sys
from datetime import datetime
from typing import Any
from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch
import pytest
from neural_ai.ui.services.strategy_service import StrategyService
import pandas
# ... és még 2 import
```

## Osztály: `TestStrategyService`

Strategy Service tesztek.

### Metódusok

#### `mock_dependencies()`

```python
def mock_dependencies(self)
```

Mock external dependencies.

**Paraméterek:**

- **`self`**

#### `mock_components()`

```python
def mock_components(self) -> MagicMock
```

Mock CoreComponents.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `MagicMock`

#### `mock_logger()`

```python
def mock_logger(self) -> MagicMock
```

Mock Logger.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `MagicMock`

#### `mock_config()`

```python
def mock_config(self) -> dict[str, Any]
```

Mock Config.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `dict[str, Any]`

#### `strategy_service()`

```python
def strategy_service(self, mock_logger: MagicMock, mock_config: dict[str, Any], mock_components: MagicMock) -> StrategyService
```

StrategyService példány létrehozása mock komponensekkel.

**Paraméterek:**

- **`self`**
- **`mock_logger`** (`MagicMock`)
- **`mock_config`** (`dict[str, Any]`)
- **`mock_components`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `StrategyService`

#### `test_init()`

```python
def test_init(self, strategy_service: StrategyService, mock_components: MagicMock) -> None
```

StrategyService inicializáció tesztelése.

**Paraméterek:**

- **`self`**
- **`strategy_service`** (`StrategyService`)
- **`mock_components`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_get_strategies()`

```python
def test_get_strategies(self, strategy_service: StrategyService) -> None
```

Stratégiák lekérdezésének tesztelése.

**Paraméterek:**

- **`self`**
- **`strategy_service`** (`StrategyService`)

**Visszatérési érték:**

- Típus: `None`

#### `test_create_strategy()`

```python
def test_create_strategy(self, strategy_service: StrategyService) -> None
```

Új stratégia létrehozásának tesztelése.

**Paraméterek:**

- **`self`**
- **`strategy_service`** (`StrategyService`)

**Visszatérési érték:**

- Típus: `None`

#### `test_update_strategy()`

```python
def test_update_strategy(self, strategy_service: StrategyService) -> None
```

Stratégia módosításának tesztelése.

**Paraméterek:**

- **`self`**
- **`strategy_service`** (`StrategyService`)

**Visszatérési érték:**

- Típus: `None`

#### `test_update_strategy_not_found()`

```python
def test_update_strategy_not_found(self, strategy_service: StrategyService) -> None
```

Ismeretlen stratégia módosításának tesztelése.

**Paraméterek:**

- **`self`**
- **`strategy_service`** (`StrategyService`)

**Visszatérési érték:**

- Típus: `None`

#### `test_delete_strategy()`

```python
def test_delete_strategy(self, strategy_service: StrategyService) -> None
```

Stratégia törlésének tesztelése.

**Paraméterek:**

- **`self`**
- **`strategy_service`** (`StrategyService`)

**Visszatérési érték:**

- Típus: `None`

#### `test_delete_strategy_not_found()`

```python
def test_delete_strategy_not_found(self, strategy_service: StrategyService) -> None
```

Ismeretlen stratégia törlésének tesztelése.

**Paraméterek:**

- **`self`**
- **`strategy_service`** (`StrategyService`)

**Visszatérési érték:**

- Típus: `None`

#### `test_backtest_strategy()`

```python
def test_backtest_strategy(self, strategy_service: StrategyService) -> None
```

Backtest indításának tesztelése.

**Paraméterek:**

- **`self`**
- **`strategy_service`** (`StrategyService`)

**Visszatérési érték:**

- Típus: `None`

#### `test_backtest_strategy_not_found()`

```python
def test_backtest_strategy_not_found(self, strategy_service: StrategyService) -> None
```

Ismeretlen stratégia backtestelésének tesztelése.

**Paraméterek:**

- **`self`**
- **`strategy_service`** (`StrategyService`)

**Visszatérési érték:**

- Típus: `None`

#### `test_get_backtest_status()`

```python
def test_get_backtest_status(self, strategy_service: StrategyService) -> None
```

Backtest állapot lekérdezésének tesztelése.

**Paraméterek:**

- **`self`**
- **`strategy_service`** (`StrategyService`)

**Visszatérési érték:**

- Típus: `None`

#### `test_get_backtest_status_not_found()`

```python
def test_get_backtest_status_not_found(self, strategy_service: StrategyService) -> None
```

Ismeretlen backtest állapot lekérdezésének tesztelése.

**Paraméterek:**

- **`self`**
- **`strategy_service`** (`StrategyService`)

**Visszatérési érték:**

- Típus: `None`

#### `test_optimize_strategy()`

```python
def test_optimize_strategy(self, strategy_service: StrategyService) -> None
```

Optimalizálás indításának tesztelése.

**Paraméterek:**

- **`self`**
- **`strategy_service`** (`StrategyService`)

**Visszatérési érték:**

- Típus: `None`

#### `test_optimize_strategy_not_found()`

```python
def test_optimize_strategy_not_found(self, strategy_service: StrategyService) -> None
```

Ismeretlen stratégia optimalizálásának tesztelése.

**Paraméterek:**

- **`self`**
- **`strategy_service`** (`StrategyService`)

**Visszatérési érték:**

- Típus: `None`

#### `test_get_candles()`

```python
async def test_get_candles(self, strategy_service: StrategyService) -> None
```

OHLCV gyertyák lekérdezésének tesztelése.

**Paraméterek:**

- **`self`**
- **`strategy_service`** (`StrategyService`)

**Visszatérési érték:**

- Típus: `None`

#### `test_get_candles_date_format()`

```python
async def test_get_candles_date_format(self, strategy_service: StrategyService) -> None
```

Dátum formátum konverzió tesztelése.

**Paraméterek:**

- **`self`**
- **`strategy_service`** (`StrategyService`)

**Visszatérési érték:**

- Típus: `None`

#### `test_get_candles_different_timeframes()`

```python
async def test_get_candles_different_timeframes(self, strategy_service: StrategyService) -> None
```

Különböző időkeretek tesztelése.

**Paraméterek:**

- **`self`**
- **`strategy_service`** (`StrategyService`)

**Visszatérési érték:**

- Típus: `None`

#### `test_run_sma_backtest_success_with_trades()`

```python
async def test_run_sma_backtest_success_with_trades(self, strategy_service: StrategyService) -> None
```

SMA backtest sikerességének tesztelése trades adatokkal.

**Paraméterek:**

- **`self`**
- **`strategy_service`** (`StrategyService`)

**Visszatérési érték:**

- Típus: `None`

#### `test_run_sma_backtest_no_trades()`

```python
async def test_run_sma_backtest_no_trades(self, strategy_service: StrategyService) -> None
```

SMA backtest tesztelése trades nélkül.

**Paraméterek:**

- **`self`**
- **`strategy_service`** (`StrategyService`)

**Visszatérési érték:**

- Típus: `None`

#### `test_run_sma_backtest_missing_pnl_column()`

```python
async def test_run_sma_backtest_missing_pnl_column(self, strategy_service: StrategyService) -> None
```

SMA backtest tesztelése hiányzó PnL oszloppal.

**Paraméterek:**

- **`self`**
- **`strategy_service`** (`StrategyService`)

**Visszatérési érték:**

- Típus: `None`

#### `test_analyze_market_structure_with_df()`

```python
async def test_analyze_market_structure_with_df(self, strategy_service: StrategyService) -> None
```

Piaci struktúra elemzés tesztelése meglévő DataFrame-mel.

**Paraméterek:**

- **`self`**
- **`strategy_service`** (`StrategyService`)

**Visszatérési érték:**

- Típus: `None`

#### `test_analyze_market_structure_without_df()`

```python
async def test_analyze_market_structure_without_df(self, strategy_service: StrategyService) -> None
```

Piaci struktúra elemzés tesztelése DataFrame betöltéssel.

**Paraméterek:**

- **`self`**
- **`strategy_service`** (`StrategyService`)

**Visszatérési érték:**

- Típus: `None`

#### `test_analyze_market_structure_no_data()`

```python
async def test_analyze_market_structure_no_data(self, strategy_service: StrategyService) -> None
```

Piaci struktúra elemzés tesztelése adatok hiányában.

**Paraméterek:**

- **`self`**
- **`strategy_service`** (`StrategyService`)

**Visszatérési érték:**

- Típus: `None`

#### `test_analyze_market_structure_empty_data()`

```python
async def test_analyze_market_structure_empty_data(self, strategy_service: StrategyService) -> None
```

Piaci struktúra elemzés tesztelése üres adatokkal.

**Paraméterek:**

- **`self`**
- **`strategy_service`** (`StrategyService`)

**Visszatérési érték:**

- Típus: `None`

#### `test_analyze_market_structure_missing_components()`

```python
async def test_analyze_market_structure_missing_components(self, strategy_service: StrategyService) -> None
```

Piaci struktúra elemzés tesztelése hiányzó komponensekkel.

**Paraméterek:**

- **`self`**
- **`strategy_service`** (`StrategyService`)

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/neural_ai/ui/services/test_strategy_service.py`](../../tests/neural_ai/ui/services/test_strategy_service.py)
