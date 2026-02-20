# neural_ai/ui/services/strategy_service.py

Strategy Service implementáció.

Ez a modul implementálja a kereskedési stratégia szolgáltatást,
 amely a stratégiák létrehozását, módosítását és tesztelését végzi.

## Importok

```python
from datetime import datetime
from typing import TYPE_CHECKING
from typing import Any
from neural_ai.ui.interfaces.strategy_service_interface import StrategyServiceInterface
import pandas
import polars
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
from neural_ai.processors.resampler_service.interfaces.resampler_interface import ResamplerInterface
from neural_ai.processors.resampler_service.factory import ResamplerServiceFactory
# ... és még 3 import
```

## Osztály: `StrategyService(StrategyServiceInterface)`

Strategy Service - Kereskedési stratégiák kezeléséért felelős.

Ez az osztály implementálja a stratégiák létrehozását, szerkesztését és
tesztelését végző metódusokat.

### Metódusok

#### `__init__()`

```python
def __init__(self, logger: Any, config: dict[str, Any], core_components: Any) -> None
```

A Strategy Service inicializálása.

**Paraméterek:**

- **`self`**
- **`logger`** (`Any`): A logger példány
- **`config`** (`dict[str, Any]`): A szolgáltatás konfiguráció
- **`core_components`** (`Any`): A core komponensek

**Visszatérési érték:**

- Típus: `None`

#### `get_strategies()`

```python
def get_strategies(self) -> list[dict[str, str]]
```

Elérhető stratégiák lekérdezése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `list[dict[str, str]]`
- List[Dict[str, Any]]: A stratégiák listája

#### `create_strategy()`

```python
def create_strategy(self, name: str, config: dict[str, Any], code: str) -> str
```

Új stratégia létrehozása.

**Paraméterek:**

- **`self`**
- **`name`** (`str`): A stratégia neve
- **`config`** (`dict[str, Any]`): A stratégia konfigurációja
- **`code`** (`str`): A stratégia kódja

**Visszatérési érték:**

- Típus: `str`
- str: A létrehozott stratégia azonosítója

#### `update_strategy()`

```python
def update_strategy(self, strategy_id: str, config: dict[str, Any] | None = None, code: str | None = None) -> bool
```

Meglévő stratégia módosítása.

**Paraméterek:**

- **`self`**
- **`strategy_id`** (`str`): A stratégia azonosítója
- **`config`** (`dict[str, Any] | None`) = `None`: Az új konfiguráció
- **`code`** (`str | None`) = `None`: Az új kód

**Visszatérési érték:**

- Típus: `bool`
- bool: True, ha sikeres a módosítás

#### `delete_strategy()`

```python
def delete_strategy(self, strategy_id: str) -> bool
```

Stratégia törlése.

**Paraméterek:**

- **`self`**
- **`strategy_id`** (`str`): A stratégia azonosítója

**Visszatérési érték:**

- Típus: `bool`
- bool: True, ha sikeres a törlés

#### `backtest_strategy()`

```python
def backtest_strategy(self, strategy_id: str, start_date: str, end_date: str, initial_capital: float) -> dict[str, Any]
```

Stratégia backtestelése.

**Paraméterek:**

- **`self`**
- **`strategy_id`** (`str`): A stratégia azonosítója
- **`start_date`** (`str`): A teszt kezdő dátuma
- **`end_date`** (`str`): A teszt záró dátuma
- **`initial_capital`** (`float`): A kezdeti tőke

**Visszatérési érték:**

- Típus: `dict[str, Any]`
- Dict[str, Any]: A backtest eredménye

#### `get_backtest_status()`

```python
def get_backtest_status(self, backtest_id: str) -> dict[str, Any]
```

Backtest állapotának lekérdezése.

**Paraméterek:**

- **`self`**
- **`backtest_id`** (`str`): A backtest azonosítója

**Visszatérési érték:**

- Típus: `dict[str, Any]`
- Dict[str, Any]: A backtest állapota

#### `optimize_strategy()`

```python
def optimize_strategy(self, strategy_id: str, parameters: dict[str, list[Any]], optimization_method: str = 'grid') -> dict[str, Any]
```

Stratégia paraméterek optimalizálása.

**Paraméterek:**

- **`self`**
- **`strategy_id`** (`str`): A stratégia azonosítója
- **`parameters`** (`dict[str, list[Any]]`): Az optimalizálandó paraméterek
- **`optimization_method`** (`str`) = `'grid'`: Az optimalizálási módszer

**Visszatérési érték:**

- Típus: `dict[str, Any]`
- Dict[str, Any]: Az optimalizálás eredménye

#### `get_candles()`

```python
async def get_candles(self, symbol: str, date: str, timeframe: str) -> 'pl.DataFrame'
```

OHLCV gyertyák lekérdezése a ResamplerService-en keresztül. Ez a metódus a megadott szimbólumhoz, dátumhoz és időkerethez tartozó resample-ölt OHLCV adatokat kérdezi le.

**Paraméterek:**

- **`self`**
- **`symbol`** (`str`): A kereskedési szimbólum (pl. 'EURUSD')
- **`date`** (`str`): A dátum (pl. '2024-03-20')
- **`timeframe`** (`str`): Az időkeret (pl. '1m', '5m', '1h', '4h')

**Visszatérési érték:**

- Típus: `'pl.DataFrame'`
- pl.DataFrame: A resample-ölt OHLCV gyertyák DataFrame-ben

#### `run_sma_backtest()`

```python
async def run_sma_backtest(self, symbol: str, date: str, timeframe: str, fast_period: int, slow_period: int, initial_capital: float = 10000.0, df: 'pd.DataFrame | None' = None) -> dict[str, Any]
```

SMA kereszt stratégia backtesztelése VectorBT-vel. Ez a metódus betölti az adatokat, kiszámolja az SMA indikátorokat, generálja a belépési és kilépési jeleket, majd lefuttatja a backtestet.

**Paraméterek:**

- **`self`**
- **`symbol`** (`str`): A kereskedési szimbólum (pl. 'EURUSD')
- **`date`** (`str`): A dátum (pl. '2024-03-20')
- **`timeframe`** (`str`): Az időkeret (pl. '1m', '5m', '1h', '4h')
- **`fast_period`** (`int`): A gyors SMA periódusa
- **`slow_period`** (`int`): A lassú SMA periódusa
- **`initial_capital`** (`float`) = `10000.0`: A kezdeti tőke (default: 10000.0)
- **`df`** (`'pd.DataFrame | None'`) = `None`: Opcionális DataFrame az adatokhoz (ha None, akkor betölti get_candles-szel)

**Visszatérési érték:**

- Típus: `dict[str, Any]`
- Dict[str, Any]: A backtest eredménye (stats, equity, trades, signals)

#### `analyze_market_structure()`

```python
async def analyze_market_structure(self, symbol: str, date: str, timeframe: str, df: 'pl.DataFrame | None' = None) -> 'pl.DataFrame'
```

Piaci struktúra elemzése swing pontokkal és szintekkel. Ez a metódus a D2 dimenzió processor-t használja a swing pontok és piaci szintek kiszámítására az adott szimbólum adataiból.

**Paraméterek:**

- **`self`**
- **`symbol`** (`str`): A kereskedési szimbólum (pl. 'EURUSD')
- **`date`** (`str`): A dátum (pl. '2024-03-20')
- **`timeframe`** (`str`): Az időkeret (pl. '1m', '5m', '1h', '4h')
- **`df`** (`'pl.DataFrame | None'`) = `None`: Opcionális Polars DataFrame (ha None, akkor betölti get_candles-szel)

**Visszatérési érték:**

- Típus: `'pl.DataFrame'`
- pl.DataFrame: A feldolgozott DataFrame swing pontokkal és szintekkel

---

**Forrásfájl:** [`neural_ai/ui/services/strategy_service.py`](../../neural_ai/ui/services/strategy_service.py)
