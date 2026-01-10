# Processing Factory - Feldolgozási komponensek factory

## 🎯 Cél és Feladat

A `factory.py` modul a processing komponensek központi Factory függvényeit biztosítja. Ez a bootstrap pont a TimeAlignmentService és Dimension Processor komponensek számára.

## 🏗️ Architektúra

A modul két fő Factory függvényt exportál:

- `create_time_alignment_service()`: TimeAlignmentService példányosítás
- `create_dimension_processor(dimension_id)`: Dimension processor példányosítás ID alapján

## 🔧 Használat

### TimeAlignmentService létrehozása

```python
from neural_ai.core.processing.factory import create_time_alignment_service

aligner = create_time_alignment_service()
aligned_df = aligner.reindex_to_grid(ohlcv_df, timeframe="1m")
```

### Dimension Processor létrehozása

```python
from neural_ai.core.processing.factory import create_dimension_processor

# D1 processor létrehozása
d1_processor = create_dimension_processor(1)
result = d1_processor.process(aligned_df)
```

## 📝 API Referencia

### Függvények

#### `create_time_alignment_service() -> ITimeAlignmentService`

TimeAlignmentService példányt hoz létre.

**Visszatérési érték:**
- `ITimeAlignmentService`: TimeAlignmentService példány

#### `create_dimension_processor(dimension_id: int) -> IDimensionProcessor`

Dimension processor példányt hoz létre a megadott ID alapján.

**Paraméterek:**
- `dimension_id`: Dimenzió azonosító (1-15)

**Visszatérési érték:**
- `IDimensionProcessor`: A megfelelő dimenzió processor

**Dobott kivételek:**
- `ValueError`: Ismeretlen dimenzió ID esetén

**Támogatott dimenziók:**
- `1`: D01PriceProcessor (alap adatok)

## 🧪 Tesztelés

A Factory függvények teljes mértékben le vannak fedve unit tesztekkel:

```bash
pytest tests/core/processing/test_processing_factory.py --cov-report=term-missing
# Coverage: Stmt: 100% | Brch: 100%
```

## 🔗 Kapcsolatok

- **TimeAlignmentService:** `neural_ai.core.processing.implementations.time_alignment_service`
- **D01PriceProcessor:** `neural_ai.core.processing.dimensions.d01_price`
- **Interfészek:** `neural_ai.core.processing.interfaces`

## 📊 Implementáció

A jelenlegi implementáció csak a D1 dimenziót támogatja, de könnyen bővíthető további dimenziókkal:

```python
def create_dimension_processor(dimension_id: int) -> IDimensionProcessor:
    if dimension_id == 1:
        return D01PriceFactory.create()
    elif dimension_id == 2:
        return D02SupportFactory.create()  # Jövőbeli implementáció
    else:
        raise ValueError(f"Ismeretlen dimenzió ID: {dimension_id}")