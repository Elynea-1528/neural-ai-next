# D01 Price Dimension Modul

## 🎯 Cél és Feladat

A `d01_price` modul a hierarchikus AI rendszer alapvető pénzügyi adatfeldolgozási komponensét implementálja. Ez a D1 dimenzió biztosítja a normalizált OHLCV adatok konszisztens kezelését és validálását az AI modellek számára.

## 🏗️ Architektúra

A modul a strict Interface/Implementation/Factory szerkezetet követi:

- **Interfész:** `IDimensionProcessor`
- **Implementáció:** `D01PriceProcessor`
- **Factory:** `D01PriceFactory`

## 📦 Exportált Komponensek

```python
from neural_ai.core.processing.dimensions.d01_price import (
    D01PriceFactory,      # Factory osztály példányosításhoz
    IDimensionProcessor,  # Publikus interfész
)
```

## 🔧 Használat

### Közvetlen használat

```python
from neural_ai.core.processing.dimensions.d01_price import D01PriceFactory

processor = D01PriceFactory.create()
result = processor.process(ohlcv_data)
```

### Factory függvényen keresztül

```python
from neural_ai.core.processing.factory import create_dimension_processor

processor = create_dimension_processor(1)  # D1 dimenzió
result = processor.process(ohlcv_data)
```

## 📝 API Referencia

### Exportált osztályok

#### `D01PriceFactory`

Factory osztály a D01PriceProcessor létrehozásához.

#### `IDimensionProcessor`

Publikus interfész minden dimenzió processzor számára.

## 🧪 Tesztelés

A teljes modul le van fedve unit tesztekkel:

```bash
pytest tests/core/processing/dimensions/d01_price/ --cov-report=term-missing
# Coverage: Stmt: 100% | Brch: 100%
```

## 🔗 Kapcsolatok

- **Felsőbb modul:** `neural_ai.core.processing`
- **Interfész:** `neural_ai.core.processing.interfaces.dimension_processor_interface`
- **Függőségek:** Polars DataFrame könyvtár
- **Adatfolyam:** TimeAlignmentService → D01PriceProcessor → AI Modellek

## 📋 Specifikáció

A D1 dimenzió a következő oszlopokat biztosítja:

- `timestamp`: Időbélyeg (datetime)
- `open`: Nyitó ár (float)
- `high`: Maximum ár (float)
- `low`: Minimum ár (float)
- `close`: Záró ár (float)
- `tick_volume`: Tick volumen (int)
- `spread`: Spread érték (float)
- `real_volume`: Valós volumen (float)

## 🐛 Hibakezelés

- Hiányzó oszlopok esetén `ColumnNotFoundError`
- Strict type hints használata mindenhol
- Comprehensive unit teszt lefedettség