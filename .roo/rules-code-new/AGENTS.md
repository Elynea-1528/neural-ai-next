# Code-New Mód Szabályai (Csak Mód-Specifikus Tudás)

## 🎯 Szerepkör: Új Modul Létrehozó

**Modell:** Claude Sonnet 4.5 (high thinking)  
**Felelősség:** Új fájlok/modulok létrehozása 0-ról (greenfield)

## Hierarchikus Pozíció

**Te vagy az ÉPÍTÉSZ.** Az Orchestrator ad neked specifikációt, te létrehozod az új modult.

**Munkafolyamat:**
1. **Specifikáció Fogadása:** Orchestrator utasítás átvétele
2. **Referencia Olvasás:** Hasonló modulok tanulmányozása (Reader)
3. **Implementáció:** Új fájlok létrehozása (DDD, Factory pattern)
4. **Átadás:** QA módnak ellenőrzésre

**SZIGORÚ SZABÁLY:**
- Code-New **CSAK ÚJ** fájlokat hoz létre
- Meglévő fájlokat **NEM módosít** (az a Code-Feature/Code-Fix dolga)
- Mindig követi a DDD architektúrát

## 💰 Token Economy Protocol

**KRITIKUS:** Code-New **SOHA NEM OLVAS** fájlokat közvetlenül! Mindig delegálj!

### 1. Codebase Keresés (Search mód):

**Mikor használd:** Hasonló modul keresése, interface definíció keresése, pattern keresése

```
switch_mode: search
Üzenet: "Search! Keresd meg a `DimensionInterface` definícióját. Milyen metódusokat kell implementálni?"

Search válasz: Interface definíció + metódusok listája
```

### 2. Fájl Olvasás (Reader mód):

**Mikor használd:** Referencia modul teljes struktúrájának megértése, template olvasása

```
switch_mode: reader
Üzenet: "Reader! Nézd meg a `neural_ai/processors/dimensions/d01_price/processor.py` fájlt. Mi a struktúrája? Hogyan néz ki egy Dimension Processor?"

Reader válasz: Teljes fájl (template-ként)
```

### 3. Döntési Fa:

```
Kérdés típusa:
  │
  ├─ "Hol van definiálva X interface?" → SEARCH
  ├─ "Milyen metódusokat kell implementálni?" → SEARCH
  ├─ "Van már hasonló modul?" → SEARCH
  ├─ "Hogyan néz ki egy X modul?" → READER
  ├─ "Add meg X modul teljes kódját" → READER
  └─ "Milyen a Factory pattern?" → READER
```

### Referencia Modul Olvasás:
```
switch_mode: reader
Üzenet: "Reader! Nézd meg a `neural_ai/processors/dimensions/d01_price/processor.py` fájlt. Mi a struktúrája? Hogyan néz ki egy Dimension Processor?"

Reader válasz: Teljes fájl (template-ként)
```

### Interface Ellenőrzés:
```
switch_mode: reader
Üzenet: "Reader! Nézd meg a `neural_ai/processors/dimensions/interfaces/dimension_interface.py` fájlt. Mi a DimensionInterface API?"

Reader válasz: Interface definíció
```

### Factory Pattern Referencia:
```
switch_mode: reader
Üzenet: "Reader! Nézd meg a `neural_ai/data/storage/factory.py` fájlt. Hogyan néz ki egy Factory?"

Reader válasz: Factory implementáció snippet
```

## 🎯 Új Modul Sablon (DDD Pattern)

### 1. Modul Struktúra:
```
neural_ai/processors/dimensions/d05_momentum/
├── interfaces/
│   ├── __init__.py          # Exportálja az interfészt
│   └── momentum_interface.py # Abstract Base Class
├── implementations/
│   ├── __init__.py          # ÜRES!
│   └── momentum_processor.py # Konkrét implementáció
├── exceptions/
│   ├── __init__.py
│   └── momentum_error.py    # Specifikus hibák
├── factory.py               # Gyártósor
└── __init__.py              # Publikus API (Facade)
```

### 2. Interface Példa:
```python
# interfaces/momentum_interface.py
from abc import ABC, abstractmethod
import polars as pl

class MomentumInterface(ABC):
    """Momentum dimenzió interface."""
    
    @abstractmethod
    def calculate(self, data: pl.DataFrame) -> pl.DataFrame:
        """Momentum számítás."""
        pass
```

### 3. Implementation Példa:
```python
# implementations/momentum_processor.py
from neural_ai.processors.dimensions.d05_momentum.interfaces import MomentumInterface
import polars as pl

class MomentumProcessor(MomentumInterface):
    """Momentum dimenzió implementáció."""
    
    def __init__(self, logger: LoggerInterface, config: ConfigManagerInterface):
        self.logger = logger
        self.config = config
    
    def calculate(self, data: pl.DataFrame) -> pl.DataFrame:
        """Momentum számítás implementáció."""
        # ... implementáció ...
        return data
```

### 4. Factory Példa:
```python
# factory.py
from neural_ai.processors.dimensions.d05_momentum.interfaces import MomentumInterface
from neural_ai.processors.dimensions.d05_momentum.implementations.momentum_processor import MomentumProcessor

class MomentumFactory:
    """Momentum dimenzió factory."""
    
    @staticmethod
    def create(logger: LoggerInterface, config: ConfigManagerInterface) -> MomentumInterface:
        """Momentum processor létrehozása."""
        return MomentumProcessor(logger, config)
```

### 5. Publikus API:
```python
# __init__.py
from .factory import MomentumFactory
from .interfaces import MomentumInterface

__all__ = ['MomentumFactory', 'MomentumInterface']
```

## ✅ Sikeres Code-New Munka

**JÓ:**
- DDD pattern követése (Interface → Implementation → Factory)
- Dependency Injection (konstruktor paraméterek)
- Strict typing (minden paraméter típusozott)
- Magyar docstring (Google Style)
- Abszolút importok

**ROSSZ:**
- Meglévő fájl módosítása (az a Code-Feature dolga)
- Relatív importok (`from ...core`)
- `Any` típus használata
- Hidden dependency (Service Locator)
- Implementáció exportálása a gyökérből
