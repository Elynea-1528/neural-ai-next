# D01PriceProcessor - Alap adatok processzor

## 🎯 Cél és Feladat

A `D01PriceProcessor` osztály a hierarchikus AI rendszer alapvető pénzügyi adatfeldolgozási komponense. Feladata a normalizált OHLCV adatok biztosítása és validálása az AI modellek számára. Ez az első dimenzió (D1) processzor, amely kiválasztja az alap oszlopokat és matematikai transzformációkat számít: log return, rolling Z-score és árnyékokat (shadows).

## 🏗️ Architektúra

Az osztály az `IDimensionProcessor` interfészt implementálja, biztosítva a konzisztens API-t az összes dimenzió processzor számára.

```python
from neural_ai.core.processing.dimensions.d01_price.processor import D01PriceProcessor

processor = D01PriceProcessor()
result = processor.process(ohlcv_dataframe)
```

## 🔧 Használat

### Példa Kód

```python
import polars as pl
from datetime import datetime
from neural_ai.core.processing.dimensions.d01_price.processor import D01PriceProcessor

# Példa OHLCV adatok
ohlcv_data = pl.DataFrame({
    "timestamp": [datetime(2023, 1, 1, 9, 0, 0)],
    "open": [1.0500],
    "high": [1.0520],
    "low": [1.0480],
    "close": [1.0510],
    "tick_volume": [1000],
    "spread": [0.0002],
    "real_volume": [1500.0]
})

# Processor példányosítása és futtatása
processor = D01PriceProcessor()
result = processor.process(ohlcv_data)

print(result.columns)
# ['timestamp', 'open', 'high', 'low', 'close', 'tick_volume', 'spread', 'real_volume', 'mid_close', 'log_return', 'rolling_z_score', 'upper_shadow', 'lower_shadow']
```

## 📝 API Referencia

### Konstruktor

```python
D01PriceProcessor() -> None
```

Nincs paraméter, stateless implementáció.

### Metódusok

#### `process(df: pl.DataFrame) -> pl.DataFrame`

Polars Expr alapú dimenzió számítás matematikai transzformációkkal. Számítja a mid_close, log_return, rolling_z_score, upper_shadow és lower_shadow oszlopokat.

**Matematikai transzformációk:**
- `mid_close`: (open + close) / 2
- `log_return`: ln(mid_close / mid_close.shift(1))
- `rolling_z_score`: (log_return - log_return.rolling_mean(60)) / log_return.rolling_std(60)
- `upper_shadow`: high - max(open, close)
- `lower_shadow`: min(open, close) - low

**Paraméterek:**
- `df`: Polars DataFrame normalizált OHLCV adatokkal

**Visszatérési érték:**
- Polars DataFrame az alap oszlopokkal és matematikai transzformációkkal

**Dobott kivételek:**
- `polars.exceptions.ColumnNotFoundError`: Ha hiányzik valamely szükséges oszlop

#### `dimension_id: int` (property)

Visszaadja a dimenzió azonosítóját.

**Visszatérési érték:**
- `1`: D1 dimenzió azonosító

## 🧪 Tesztelés

A processzor teljes mértékben le van fedve unit tesztekkel:

- Érvényes adatok feldolgozása
- Üres DataFrame kezelése
- Hiányzó oszlopok esetén hiba dobás
- Extra oszlopok figyelmen kívül hagyása
- Adattípusok megőrzése
- Sorrend megőrzése

```bash
pytest tests/core/processing/dimensions/d01_price/test_processor.py --cov-report=term-missing
# Coverage: Stmt: 100% | Brch: 100%
```

## 🔗 Kapcsolatok

- **Interfész:** `IDimensionProcessor`
- **Factory:** `D01PriceFactory`
- **Felsőbb réteg:** `create_dimension_processor(1)` függvény
- **Adatfolyam:** TimeAlignmentService -> D01PriceProcessor -> AI Modellek

## 🐛 Hibakezelés

- **Hiányzó oszlopok:** ColumnNotFoundError dobása
- **Üres DataFrame:** Üres DataFrame visszaadása helyes sémával
- **Adattípusok:** Strict type hints használata, runtime ellenőrzés nélkül

## 📊 Teljesítmény

- **Komplexitás:** O(n) ahol n a sorok száma
- **Memória:** Zero-copy szelektálás Polars Expr-rel
- **Párhuzamosság:** Thread-safe (stateless)