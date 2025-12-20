# 🪃 Orchestrator Mód - Neural AI Next

## Alapelvek

Az Orchestrator módban a következő alapelvekre kell koncentrálni:

1. **Tervezés** - Minden komplex feladatot bonts le részfeladatokra
2. **Koordináció** - Koordináld a különböző módok közötti munkát
3. **Dokumentáció** - Dokumentáld a folyamatot és a döntéseket
4. **Minőségbiztosítás** - Ellenőrizd a részfeladatok elvégzését

## Komplex feladatok lebontása

### 1. Feladat elemzése

Amikor komplex feladatot kapsz, kövesd ezt a folyamatot:

```markdown
## Feladat elemzése

### Fő cél
[A feladat fő céljának leírása]

### Részfeladatok
1. [Első részfeladat]
2. [Második részfeladat]
3. [Harmadik részfeladat]

### Függőségek
- [ ] 2. részfeladat megköveteli az 1. befejezését
- [ ] 3. részfeladat párhuzamosan futhat az 1.-el

### Szükséges módok
- Architect: [mikor és miért]
- Code: [mikor és miért]
- Debug: [mikor és miért]
- Ask: [mikor és miért]
```

### 2. Terv létrehozása

Hozz létre egy részletes tervet:

```markdown
## Implementációs terv

### 1. Fázis: Tervezés (Architect mód)
- [ ] Rendszerarchitektúra tervezése
- [ ] Komponens struktúra meghatározása
- [ ] Adatfolyamok leírása
- [ ] Tesztelési stratégia kidolgozása

### 2. Fázis: Implementáció (Code mód)
- [ ] Alap komponensek létrehozása
- [ ] Interfészek implementálása
- [ ] Fő logika megírása
- [ ] Integrációs tesztek írása

### 3. Fázis: Tesztelés (Debug mód)
- [ ] Egységtesztek futtatása
- [ ] Hibák javítása
- [ ] Teljesítmény optimalizálás
- [ ] Biztonsági ellenőrzés

### 4. Fázis: Dokumentáció (Ask/Architect mód)
- [ ] API dokumentáció frissítése
- [ ] Használati útmutató írása
- [ ] Változásnapló frissítése
- [ ] Példák gyűjtése
```

## Projektspecifikus koordináció

### 1. Új komponens fejlesztése

Amikor új komponenst kell fejleszteni:

#### 1.1 Architect mód - Tervezés

```markdown
## Új komponens tervezése

### Cél
[A komponens céljának leírása]

### Architektúra
- Base komponensek: `neural_ai.core.base.CoreComponentFactory`
- Interfész: `neural_ai.[komponens].interfaces.*`
- Implementáció: `neural_ai.[komponens].implementations.*`
- **Fontos:** Használd a CoreComponentFactory-t a komponensek létrehozásához

### Függőségek
- Config komponens: konfigurációkezelés
- Logger komponens: naplózás
- Storage komponens: adattárolás

### Tesztelési stratégia
- Egységtesztek minden metódushoz
- Integrációs tesztek
- Teljesítménytesztek
```

#### 1.2 Code mód - Implementáció

```python
# neural_ai/[komponens]/__init__.py
"""Új komponens csomag."""

from .implementations.my_component import MyComponent

__all__ = ['MyComponent']

# neural_ai/[komponens]/interfaces/my_component_interface.py
from abc import ABC, abstractmethod

class MyComponentInterface(ABC):
    """Komponens interfész."""
    
    @abstractmethod
    def process(self, data):
        """Adatok feldolgozása."""
        pass

# neural_ai/[komponens]/implementations/my_component.py
from neural_ai.core.base import CoreComponentFactory, CoreComponents
from .my_component_interface import MyComponentInterface

class MyComponent(MyComponentInterface):
    """Komponens implementáció."""
    
    def __init__(self, config: Dict[str, Any]):
        # Komponensek létrehozása a Factory-vel
        self.components: CoreComponents = CoreComponentFactory.create_components(
            config_path=config.get('config_path'),
            log_path=config.get('log_path'),
            storage_path=config.get('storage_path')
        )
        self.config = config
        
    def process(self, data):
        """Adatok feldolgozása."""
        self.components.logger.info("Feldolgozás megkezdése")
        # Implementáció
        return processed_data
```

#### 1.3 Debug mód - Tesztelés

```python
# tests/[komponens]/test_my_component.py
import unittest
from neural_ai.[komponens].implementations.my_component import MyComponent

class TestMyComponent(unittest.TestCase):
    """MyComponent tesztosztály."""
    
    def setUp(self):
        """Teszt előkészítés."""
        self.component = MyComponent(config={})
        
    def test_process(self):
        """Feldolgozás tesztelése."""
        data = {"test": "data"}
        result = self.component.process(data)
        self.assertIsNotNone(result)
```

### 2. MT5 Integráció fejlesztése

Komplex feladat: MT5 adatgyűjtő fejlesztése

#### 2.1 Terv (Architect mód)

```markdown
## MT5 Adatgyűjtő Fejlesztési Terv

### 1. Expert Advisor (MQL5)
- [ ] EA alapstruktúra létrehozása
- [ ] Kommunikációs interfész implementálása
- [ ] Adatgyűjtési logika megírása
- [ ] Biztonsági mechanizmusok

### 2. Python Collector
- [ ] Collector komponens tervezése
- [ ] Socket kommunikáció implementálása
- [ ] Adatvalidáció és minőségbiztosítás
- [ ] Tárolási integráció

### 3. Adatfeldolgozás
- [ ] Dimension Processor implementálása
- [ ] Training dataset generálás
- [ ] Adatminőség ellenőrzés

### 4. Tesztelés
- [ ] Unit tesztek
- [ ] Integrációs tesztek
- [ ] Teljesítménytesztek
- [ ] Stressz tesztelés
```

#### 2.2 Implementáció koordinációja

```python
# 1. Architect módban tervezd meg a struktúrát
# 2. Code módban implementáld a komponenseket
# 3. Debug módban teszteld a működést
# 4. Ask módban dokumentáld a folyamatot
```

## Munkafolyamat koordináció

### 1. Feladat delegálás

Amikor feladatot delegálsz más módoknak:

```markdown
## Feladat delegálása

### Architect mód feladata
- [ ] Rendszerarchitektúra tervezése
- [ ] Komponens struktúra meghatározása
- [ ] Adatfolyamok leírása

### Code mód feladatai
- [ ] Alap komponensek implementálása
- [ ] Interfészek létrehozása
- [ ] Fő logika megírása

### Debug mód feladatai
- [ ] Hibakeresés és tesztelés
- [ ] Teljesítmény optimalizálás
- [ ] Biztonsági ellenőrzés
```

### 2. Folyamat nyomon követése

Használj TODO listát a folyamat nyomon követéséhez:

```markdown
## MT5 Integráció - Folyamat nyomon követése

### Tervezés (Architect)
- [x] Rendszerarchitektúra tervezése
- [x] Komponens struktúra meghatározása
- [ ] Adatfolyamok leírása

### Implementáció (Code)
- [x] Collector komponens létrehozása
- [ ] Socket kommunikáció implementálása
- [ ] Adatvalidáció implementálása

### Tesztelés (Debug)
- [ ] Unit tesztek írása
- [ ] Integrációs tesztek
- [ ] Teljesítménytesztek

### Dokumentáció (Ask)
- [ ] API dokumentáció
- [ ] Használati útmutató
- [ ] Változásnapló
```

## Minőségbiztosítás

### 1. Code Review folyamat

```markdown
## Code Review Checklist

### Kódminőség
- [ ] Típusannotációk helyesek
- [ ] Docstring-ek teljesek
- [ ] Hibakezelés implementálva
- [ ] Naplózás megfelelő

### Architektúra
- [ ] Base komponensek használata (CoreComponentFactory)
- [ ] Interfész implementálva
- [ ] Komponensek CoreComponents-ből elérve
- [ ] Függőségek ellenőrzve

### Tesztelés
- [ ] Unit tesztek léteznek
- [ ] Integrációs tesztek
- [ ] Tesztlefedettség >80%

### Dokumentáció
- [ ] API dokumentáció friss
- [ ] Példakódok működnek
- [ ] Változásnapló frissítve
```

### 2. Integrációs ellenőrzés

```python
# integration_test.py
"""Integrációs teszt a komponensek közötti működéshez."""

from neural_ai.core.base import CoreComponentFactory, CoreComponents

def test_integration():
    """Integrációs teszt."""
    # 1. Komponensek létrehozása a Factory-vel
    components: CoreComponents = CoreComponentFactory.create_minimal()
    
    # 2. Komponensek ellenőrzése
    assert components.has_logger(), "Logger komponens hiányzik"
    assert components.has_storage(), "Storage komponens hiányzik"
    
    # 3. Komponens létrehozása
    class TestComponent:
        def __init__(self, components: CoreComponents):
            self.components = components
            
        def process(self, data):
            self.components.logger.info("Feldolgozás")
            return data
    
    # 4. Teszt futtatása
    component = TestComponent(components)
    result = component.process({"test": "data"})
    
    assert result is not None
    print("Integrációs teszt sikeres")
```

## Hasznos linkek

- [Egységes Fejlesztési Útmutató](../../docs/development/unified_development_guide.md)
- [Komponens Fejlesztési Útmutató](../../docs/development/component_development_guide.md)
- [Code Review Útmutató](../../docs/development/code_review_guide.md)
- [Rendszer Architektúra](../../docs/architecture/overview.md)
- [Hierarchikus Rendszer](../../docs/architecture/hierarchical_system/overview.md)

## Koordinációs sablon

```markdown
# [Feladat neve] - Koordinációs terv

## Áttekintés
[A feladat rövid leírása]

## Részfeladatok
1. [Feladat 1] - [Szükséges mód]
2. [Feladat 2] - [Szükséges mód]
3. [Feladat 3] - [Szükséges mód]

## Idővonal
- [ ] 1. fázis: [dátum]
- [ ] 2. fázis: [dátum]
- [ ] 3. fázis: [dátum]

## Ellenőrzőpontok
- [ ] Ellenőrzőpont 1
- [ ] Ellenőrzőpont 2
- [ ] Ellenőrzőpont 3

## Kockázatok
- [Kockázat 1] - [Enyhítés]
- [Kockázat 2] - [Enyhítés]
```
