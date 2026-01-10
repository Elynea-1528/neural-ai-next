# D01PriceFactory - D1 dimenzió factory

## 🎯 Cél és Feladat

A `D01PriceFactory` osztály a D01PriceProcessor példányosításáért felelős Factory osztály. Biztosítja a Dependency Injection pattern konzisztens megvalósítását és a megfelelő interfész implementációt.

## 🏗️ Architektúra

A Factory pattern implementációja, amely középpontba helyezi a `IDimensionProcessor` interfészt és biztosítja a lazacsatolást.

```python
from neural_ai.core.processing.dimensions.d01_price import D01PriceFactory

processor = D01PriceFactory.create()
```

## 🔧 Használat

### Példa Kód

```python
from neural_ai.core.processing.dimensions.d01_price import D01PriceFactory
from neural_ai.core.processing.interfaces.dimension_processor_interface import IDimensionProcessor

# Processor létrehozása Factory-n keresztül
processor: IDimensionProcessor = D01PriceFactory.create()

# Használat
result = processor.process(ohlcv_data)
assert processor.dimension_id == 1
```

## 📝 API Referencia

### Metódusok

#### `create() -> IDimensionProcessor` (staticmethod)

Létrehozza és visszaadja a D01PriceProcessor példányt.

**Visszatérési érték:**
- `IDimensionProcessor`: D01PriceProcessor példány

**Dobott kivételek:**
- Nincs (stateless implementáció)

## 🧪 Tesztelés

A Factory teljes mértékben le van fedve unit tesztekkel:

- Helyes típus visszaadása
- Új példány minden híváskor
- Létrehozott processor működőképessége

```bash
pytest tests/core/processing/dimensions/d01_price/test_factory.py --cov-report=term-missing
# Coverage: Stmt: 100% | Brch: 100%
```

## 🔗 Kapcsolatok

- **Implementáció:** `D01PriceProcessor`
- **Interfész:** `IDimensionProcessor`
- **Felsőbb réteg:** `create_dimension_processor(1)` függvény
- **Modul:** `neural_ai.core.processing.dimensions.d01_price`

## 📊 Teljesítmény

- **Komplexitás:** O(1) példányosítás
- **Memória:** Minimális overhead
- **Párhuzamosság:** Thread-safe