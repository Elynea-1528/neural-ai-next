# Strategy Service (`neural_ai/ui/services/strategy_service.py`)

## Áttekintés

A Strategy Service a kereskedési stratégiák kezelését végző szolgáltatás, amely a stratégiák létrehozását, módosítását és tesztelését biztosítja. A szolgáltatás Polars DataFrame-eken működik és VectorBT-vel integrálódik a backteszteléshez.

## Architektúra

- **Interface**: `StrategyServiceInterface`
- **Implementáció**: `StrategyService`
- **Factory**: `UIServiceFactory.get_strategy_service()`
- **Dependency Injection**: Bridge-en keresztül kapja meg a szükséges komponenseket

## Főbb Metódusok

### `get_strategies() -> list[dict[str, str]]`
Az elérhető stratégiák listáját adja vissza.

**Visszatérési érték:**
```python
[
    {
        "id": "strategy_id",
        "name": "Stratégia neve",
        "description": "Leírás",
        "type": "technical",
        "status": "active"
    }
]
```

### `get_candles(symbol: str, date: str, timeframe: str) -> pl.DataFrame`
OHLCV gyertyák lekérdezése a ResamplerService-en keresztül.

**Paraméterek:**
- `symbol`: Kereskedési szimbólum (pl. 'EURUSD')
- `date`: Dátum (pl. '2024-03-20')
- `timeframe`: Időkeret (pl. '1m', '5m', '1h')

**Visszatérési érték:** Polars DataFrame OHLCV adatokkal

### `run_sma_backtest(...) -> dict[str, Any]`
SMA kereszt stratégia backtesztelése VectorBT-vel.

**Paraméterek:**
- `symbol`: Szimbólum
- `date`: Dátum
- `timeframe`: Időkeret
- `fast_period`: Gyors SMA periódusa
- `slow_period`: Lassú SMA periódusa
- `initial_capital`: Kezdeti tőke (alapértelmezett: 10000.0)
- `df`: Opcionális Polars DataFrame

**Visszatérési érték:**
```python
{
    "stats": {...},  # VectorBT statisztikák
    "equity": [...], # Equity görbe
    "trades": {...}, # Kereskedések adatai
    "signals": {"entries": [...], "exits": [...]}, # Jelek
    "parameters": {...} # Használt paraméterek
}
```

## Big Data Támogatás

- Polars DataFrame használata nagy teljesítményű adatkezeléshez
- Chunk-olás támogatása nagy adathalmazoknál
- Aszinkron műveletek a nem-blokkoló feldolgozáshoz

## Tesztelés

A szolgáltatás teljes tesztlefedettséggel rendelkezik:
- Unit tesztek minden metódusra
- Mock objektumok használata a függőségekhez
- Async függvények tesztelése

## Használat

```python
# Factory-n keresztül
strategy_service = ui_factory.get_strategy_service()

# Adatok lekérdezése
candles = await strategy_service.get_candles("EURUSD", "2024-03-20", "1h")

# Backteszt futtatása
result = await strategy_service.run_sma_backtest(
    "EURUSD", "2024-03-20", "1h", 10, 50, 10000.0, candles
)
