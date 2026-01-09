# Strategy Service

## Áttekintés

A `StrategyService` a kereskedési stratégiák kezeléséért felelős UI szolgáltatás. Ez az osztály implementálja a [`StrategyServiceInterface`](neural_ai/ui/interfaces/strategy_service_interface.py:1) interfészt, és lehetővé teszi a stratégiák létrehozását, szerkesztését, tesztelését és optimalizálását.

## Architektúra

```
neural_ai/ui/services/strategy_service.py
neural_ai/ui/interfaces/strategy_service_interface.py
```

## Fő funkciók

### Stratégia kezelés

- **Stratégiák listázása**: [`get_strategies()`](neural_ai/ui/services/strategy_service.py:52)
- **Új stratégia létrehozása**: [`create_strategy()`](neural_ai/ui/services/strategy_service.py:71)
- **Stratégia módosítása**: [`update_strategy()`](neural_ai/ui/services/strategy_service.py:98)
- **Stratégia törlése**: [`delete_strategy()`](neural_ai/ui/services/strategy_service.py:127)

### Backtesting

- **Backtest indítása**: [`backtest_strategy()`](neural_ai/ui/services/strategy_service.py:144)
- **Backtest állapot lekérdezése**: [`get_backtest_status()`](neural_ai/ui/services/strategy_service.py:182)

### Optimalizálás

- **Stratégia optimalizálása**: [`optimize_strategy()`](neural_ai/ui/services/strategy_service.py:215)

### Adat lekérdezés

- **OHLCV gyertyák lekérdezése**: [`get_candles()`](neural_ai/ui/services/strategy_service.py:251) - ÚJ

## get_candles metódus

Az új [`get_candles()`](neural_ai/ui/services/strategy_service.py:251) metódus lehetővé teszi az OHLCV gyertyák lekérdezését a ResamplerService-en keresztül.

### Használat

```python
from neural_ai.ui.services.strategy_service import StrategyService

# StrategyService példányosítása (a bridge-en keresztül)
service = StrategyService(bridge=bridge)

# Gyertyák lekérése aszinkron módon
candles = await service.get_candles(
    symbol="EURUSD",
    date="2024-03-20",
    timeframe="1m"
)
```

### Paraméterek

| Paraméter | Típus | Leírás |
|-----------|-------|--------|
| `symbol` | `str` | A kereskedési szimbólum (pl. 'EURUSD', 'GBPUSD') |
| `date` | `str` | A dátum ISO formátumban (pl. '2024-03-20') |
| `timeframe` | `str` | Az időkeret (pl. '1m', '5m', '15m', '1h', '4h', '1d') |

### Visszatérési érték

- **`DataFrame**: A resample-ölt OHLCV gyertyák Pandas DataFrame-ben

### Implementáció részletek

A metódus a [`ResamplerServiceFactory`](neural_ai/core/processing/resampler_service/factory.py:1) segítségével példányosítja a ResamplerService-t, és meghívja annak [`resample()`](neural_ai/core/processing/resampler_service/interfaces/resampler_interface.py:16) metódusát az adatok lekéréséhez.

```python
async def get_candles(self, symbol: str, date: str, timeframe: str) -> "DataFrame":
    # Factory-n keresztül ResamplerService példány lekérése
    resampler = ResamplerServiceFactory.get_instance()
    
    # Dátum konvertálás
    start_date = datetime.strptime(date, "%Y-%m-%d")
    end_date = datetime.strptime(f"{date} 23:59:59", "%Y-%m-%d %H:%M:%S")
    
    # Async resample hívás
    candles = await resampler.resample(
        symbol=symbol,
        start=start_date,
        end=end_date,
        timeframe=timeframe
    )
    
    return candles
```

## Elérhető stratégiák

A szolgáltatás alapértelmezetten két beépített stratégiával rendelkezik:

1. **moving_avg_cross**: Mozgóátlag kereszt stratégia
2. **rsi_strategy**: RSI indikátoron alapuló stratégia

## Tesztelés

A [`test_strategy_service.py`](tests/ui/services/test_strategy_service.py:1) modul tartalmazza az összes tesztet, beleértve:

- Stratégia CRUD műveletek
- Backtest indítás és állapot lekérdezés
- Optimalizálás
- **get_candles metódus tesztelése** (100% coverage)

## Függőségek

- `neural_ai.core.processing.resampler_service`: OHLCV adatok resampling-hez
- `neural_ai.ui.interfaces.core_bridge_interface`: Backend bridge-hez
- `pandas`: DataFrame kezeléshez
