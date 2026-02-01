# ResamplerService DI Fix Terv

**Prioritás:** P1 - Kritikus  
**Típus:** Hidden Dependency Anti-Pattern javítás  
**Érintett komponensek:** 4 fájl  
**Becsült időigény:** 30 perc  

---

## 🎯 CÉL

A [`ResamplerService`](../../../neural_ai/processors/resampler_service/implementations/resampler_service.py) osztály **Hidden Dependency** anti-pattern-jének megszüntetése logger DI hozzáadásával.

---

## 📋 PROBLÉMA

### Jelenlegi állapot (ROSSZ):

```python
# neural_ai/processors/resampler_service/implementations/resampler_service.py:33-40
class ResamplerService(ResamplerInterface):
    def __init__(self, storage: "StorageInterface") -> None:
        """ResamplerService inicializálása.
        
        Args:
            storage: A tárolási interfész példány (Dependency Injection)
        """
        self._storage = storage
        self._logger: LoggerInterface = LoggerFactory.get_logger(__name__)  # ❌ HIDDEN!
```

### Problémák:
1. **Hidden Dependency:** Logger nem paraméterként kapott, hanem belül létrehozott
2. **Tesztelhetetlen:** Mock logger nem adható át
3. **Coupling:** ResamplerService függ LoggerFactory-tól
4. **Production korlátozás:** Nem lehet custom logger-t (pl. Sentry) használni

---

## 🔧 MEGOLDÁS

### 1. ResamplerService Implementáció

**Fájl:** `neural_ai/processors/resampler_service/implementations/resampler_service.py`

**Változtatás:**

```python
# RÉGI (33-40. sor):
def __init__(self, storage: "StorageInterface") -> None:
    """ResamplerService inicializálása.
    
    Args:
        storage: A tárolási interfész példány (Dependency Injection)
    """
    self._storage = storage
    self._logger: LoggerInterface = LoggerFactory.get_logger(__name__)

# ÚJ:
def __init__(
    self, 
    storage: "StorageInterface",
    logger: "LoggerInterface"
) -> None:
    """ResamplerService inicializálása.
    
    Args:
        storage: A tárolási interfész példány (Dependency Injection)
        logger: A naplózási interfész (Dependency Injection)
    """
    self._storage = storage
    self._logger = logger
```

**Módosítások:**
- **Hozzáadás:** `logger: "LoggerInterface"` paraméter
- **Eltávolítás:** `from neural_ai.core.logger.factory import LoggerFactory` import (11. sor)
- **Csere:** `LoggerFactory.get_logger(__name__)` → `logger`

---

### 2. ResamplerService Interfész Ellenőrzése

**Fájl:** `neural_ai/processors/resampler_service/interfaces/resampler_interface.py`

**Ellenőrzés szükséges:**
- Az interfész NEM definiál `__init__` szignatúrát (ABC pattern)
- NEM igényel változtatást (implementáció szintű módosítás)

**Akció:** Nincs szükség módosításra ✅

---

### 3. ResamplerServiceFactory Frissítése

**Fájl:** `neural_ai/processors/resampler_service/factory.py`

**Változtatás 1 - create() metódus (21-30. sor):**

```python
# RÉGI:
@staticmethod
def create(storage: "StorageInterface") -> ResamplerInterface:
    """ResamplerService példány létrehozása.
    
    Args:
        storage: A tárolási interfész példány
    
    Returns:
        ResamplerInterface: A létrehozott ResamplerService példány
    """
    return ResamplerService(storage=storage)

# ÚJ:
@staticmethod
def create(
    storage: "StorageInterface",
    logger: "LoggerInterface"
) -> ResamplerInterface:
    """ResamplerService példány létrehozása.
    
    Args:
        storage: A tárolási interfész példány
        logger: A naplózási interfész
    
    Returns:
        ResamplerInterface: A létrehozott ResamplerService példány
    """
    return ResamplerService(storage=storage, logger=logger)
```

**Változtatás 2 - Dead Code Eltávolítása (42-44. sor):**

```python
# RÉGI:
from neural_ai.core.logger.factory import LoggerFactory

LoggerFactory.get_logger(__name__)  # ← TÖRLENDŐ!
container = DIContainer()

# ÚJ:
container = DIContainer()
```

**Változtatás 3 - get_instance() frissítése (56-60. sor):**

```python
# RÉGI:
from neural_ai.data.storage.factory import StorageFactory

storage = StorageFactory.get_storage(storage_type="parquet")
instance = cls.create(storage=storage)
container.register(component_name, instance)
return instance

# ÚJ:
from neural_ai.data.storage.factory import StorageFactory
from neural_ai.core.logger.factory import LoggerFactory

storage = StorageFactory.get_storage(storage_type="parquet")
logger = LoggerFactory.get_logger(__name__)  # ← Bootstrap context
instance = cls.create(storage=storage, logger=logger)
container.register(component_name, instance)
return instance
```

**Megjegyzés:** `get_instance()` egy **bootstrap metódus**, LEHET benne `LoggerFactory.get_logger()`, mert célja komponensek LÉTREHOZÁSA.

---

### 4. Tesztek Frissítése

**Fájl:** `tests/processors/resampler_service/test_resampler_service.py`

**Ellenőrzés:** Vannak-e tesztek?

```bash
ls -la tests/processors/resampler_service/
```

**Ha IGEN tesztek:**

Minden tesztet frissíteni kell mock logger-rel:

```python
# RÉGI (példa):
def test_resample_basic():
    mock_storage = MagicMock()
    service = ResamplerService(storage=mock_storage)  # ❌ Nincs logger
    ...

# ÚJ:
def test_resample_basic():
    mock_storage = MagicMock()
    mock_logger = MagicMock()  # ← Mock logger
    service = ResamplerService(storage=mock_storage, logger=mock_logger)
    
    # Logger hívások ellenőrzése:
    mock_logger.debug.assert_called()
    ...
```

**Ha NINCS teszt:**
- Később létrehozni (M4 Milestone)
- Most csak az implementációt javítani

---

## 📝 VÁLTOZTATÁSOK ÖSSZEFOGLALÁSA

| Fájl | Változás | Sor |
|------|----------|-----|
| `resampler_service.py` | `logger` paraméter hozzáadása | 33-40 |
| `resampler_service.py` | `LoggerFactory` import törlése | 11 |
| `resampler_service.py` | `logger` használata (nem factory) | 40 |
| `factory.py` | `create()` - `logger` paraméter | 21-30 |
| `factory.py` | Dead code törlése (L44) | 42-44 |
| `factory.py` | `get_instance()` - logger átadás | 56-60 |
| `test_*.py` | Mock logger hozzáadása (ha létezik) | Minden teszt |

---

## ✅ ELLENŐRZÉSI LISTA

### Kód Változtatások
- [ ] `resampler_service.py` - Logger DI hozzáadva
- [ ] `resampler_service.py` - LoggerFactory import törölve
- [ ] `factory.py` - `create()` logger paraméter
- [ ] `factory.py` - Dead code törölve (L44)
- [ ] `factory.py` - `get_instance()` logger átadás

### Interfész
- [ ] `resampler_interface.py` ellenőrizve (nincs módosítás)

### Tesztek
- [ ] Teszt fájlok keresése
- [ ] Mock logger hozzáadása tesztekhez
- [ ] Tesztek futtatása
- [ ] Ellenőrzés: 0 FAILED

### Dokumentáció
- [ ] `DI_DDD_AUDIT.md` frissítése (RESOLVED státusz)
- [ ] Commit üzenetek előkészítése

---

## 🚀 VÉGREHAJTÁSI SORREND

1. **Interfész ellenőrzés** (nincs változtatás)
2. **ResamplerService implementáció** javítása
3. **ResamplerServiceFactory** javítása
4. **Tesztek** keresése és frissítése
5. **Tesztek futtatása**
6. **Atomic commitok**
7. **Dokumentáció frissítés**

---

## 🎯 SIKERKRITÉRIUMOK

- ✅ ResamplerService logger-t paraméterként kapja
- ✅ LoggerFactory import eltávolítva implementációból
- ✅ Factory átadja a loggert
- ✅ Dead code törölve
- ✅ Tesztek (ha vannak) mock logger-rel működnek
- ✅ 0 FAILED teszt
- ✅ DI_DDD_AUDIT.md frissítve (RESOLVED)

---

## 📦 COMMIT TERV (Atomic Commits)

### Commit 1: ResamplerService DI fix
```
fix(resampler): Logger Dependency Injection hozzáadása

- Hidden Dependency anti-pattern megszüntetése
- Logger paraméter hozzáadása __init__-hez
- LoggerFactory import eltávolítása
- Érintett: neural_ai/processors/resampler_service/implementations/resampler_service.py

DI/DDD Audit: P1 kritikus probléma javítva
```

### Commit 2: ResamplerServiceFactory fix
```
fix(resampler): Factory logger DI és dead code cleanup

- create() metódus logger paraméter hozzáadása
- get_instance() logger átadás
- Dead code eltávolítása (L44: LoggerFactory.get_logger hívás)
- Érintett: neural_ai/processors/resampler_service/factory.py

DI/DDD Audit: P1 kritikus probléma javítva
```

### Commit 3: Tesztek frissítése (ha van)
```
test(resampler): Mock logger hozzáadása tesztekhez

- Minden teszt mock logger-rel frissítve
- Logger hívások ellenőrzése
- Érintett: tests/processors/resampler_service/test_*.py

DI/DDD Audit: P1 kritikus probléma javítva
```

### Commit 4: Dokumentáció
```
docs: DI_DDD_AUDIT.md frissítése - ResamplerService RESOLVED

- ResamplerService státusz: RESOLVED ✅
- Dead code státusz: RESOLVED ✅
- Commit referenciák hozzáadása

DI/DDD Audit: P1 kritikus probléma dokumentálva
```

---

**Következő lépés:** Code módba váltás és implementálás kezdése
