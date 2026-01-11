# StrategyService

## Áttekintés

A `StrategyService` osztály a kereskedési stratégiák kezeléséért felelős szolgáltatás implementációja. Ez az osztály biztosítja a stratégiák létrehozását, módosítását, törlését, valamint backtestelését és optimalizálását.

## Architektúra

- **Interfész**: `StrategyServiceInterface`
- **Elhelyezkedés**: `neural_ai/ui/services/strategy_service.py`
- **Függőségek**:
  - `StrategyServiceInterface`
  - `ResamplerService` (Factory-n keresztül)
  - `vectorbt` könyvtár backteszteléshez
  - `pandas` adatkezeléshez

## Metódusok

### `__init__(bridge: CoreBridgeInterface | None = None)`

A StrategyService inicializálása.

**Paraméterek:**
- `bridge`: Opcionális backend bridge példány (backward compatibility)

### `get_strategies() -> list[dict[str, Any]]`

Elérhető stratégiák lekérdezése.

**Visszatérési érték:**
- Lista a rendelkezésre álló stratégiák szótárával

### `create_strategy(name: str, config: dict[str, Any], code: str) -> str`

Új stratégia létrehozása.

**Paraméterek:**
- `name`: Stratégia neve
- `config`: Stratégia konfiguráció
- `code`: Stratégia kódja

**Visszatérési érték:**
- Az új stratégia azonosítója

### `update_strategy(strategy_id: str, config: dict[str, Any] | None = None, code: str | None = None) -> bool`

Meglévő stratégia módosítása.

**Paraméterek:**
- `strategy_id`: Stratégia azonosító
- `config`: Új konfiguráció (opcionális)
- `code`: Új kód (opcionális)

**Visszatérési érték:**
- `True` ha sikeres a módosítás

### `delete_strategy(strategy_id: str) -> bool`

Stratégia törlése.

**Paraméterek:**
- `strategy_id`: Stratégia azonosító

**Visszatérési érték:**
- `True` ha sikeres a törlés

### `backtest_strategy(strategy_id: str, start_date: str, end_date: str, initial_capital: float) -> dict[str, Any]`

Stratégia backtestelése (jelenleg mock implementáció).

**Paraméterek:**
- `strategy_id`: Stratégia azonosító
- `start_date`: Kezdő dátum
- `end_date`: Záró dátum
- `initial_capital`: Kezdeti tőke

**Visszatérési érték:**
- Backtest eredmény szótár

### `get_backtest_status(backtest_id: str) -> dict[str, Any]`

Backtest állapotának lekérdezése.

**Paraméterek:**
- `backtest_id`: Backtest azonosító

**Visszatérési érték:**
- Backtest állapot szótár

### `optimize_strategy(strategy_id: str, parameters: dict[str, list[Any]], optimization_method: str = "grid") -> dict[str, Any]`

Stratégia paraméterek optimalizálása (jelenleg mock implementáció).

**Paraméterek:**
- `strategy_id`: Stratégia azonosító
- `parameters`: Optimalizálandó paraméterek
- `optimization_method`: Optimalizálási módszer (default: "grid")

**Visszatérési érték:**
- Optimalizálás eredmény szótár

### `get_candles(symbol: str, date: str, timeframe: str) -> DataFrame` (async)

OHLCV gyertyák lekérdezése a ResamplerService-en keresztül.

**Paraméterek:**
- `symbol`: Kereskedési szimbólum
- `date`: Dátum
- `timeframe`: Időkeret

**Visszatérési érték:**
- Resample-ölt OHLCV DataFrame

### `run_sma_backtest(symbol: str, date: str, timeframe: str, fast_period: int, slow_period: int, initial_capital: float = 10000.0, df: DataFrame | None = None) -> dict[str, Any]` (async)

SMA kereszt stratégia backtesztelése VectorBT-vel.

**Paraméterek:**
- `symbol`: Kereskedési szimbólum
- `date`: Dátum
- `timeframe`: Időkeret
- `fast_period`: Gyors SMA periódus
- `slow_period`: Lassú SMA periódus
- `initial_capital`: Kezdeti tőke (default: 10000.0)
- `df`: Opcionális DataFrame (ha None, akkor betölti get_candles-szel)

**Visszatérési érték:**
- Backtest eredmény szótár (stats, equity, trades, signals, parameters)

## Adatstruktúrák

### Trades Data

A `run_sma_backtest` metódus által visszaadott trades adat szerkezete:

```python
{
    "count": int,           # Tradesh száma
    "pnl": list[float],     # Profit/Loss értékek
    "duration": list[str],  # Trade időtartamok (string formátumban)
    "entry_time": list[str], # Belépési idők
    "exit_time": list[str]   # Kilépési idők
}
```

## Megjegyzések

- A trades feldolgozás során `records_readable` használatos a stabilabb adatelérés érdekében
- Duration értékek string-ként kerülnek visszaadásra JSON kompatibilitás miatt
- Hiányzó PnL értékek 0.0-val töltődnek fel
- Az osztály Dependency Injection elvet követ, Factory-kon keresztül példányosít