# 🎯 TYPE SAFETY REFACTORING - ROADMAP

**Projekt**: Neural AI Next - Type Safety Audit & Refactoring
**Időkeret**: 12 hét (3 hónap)
**Prioritás**: 🔴 KRITIKUS
**Verzió**: 1.0
**Létrehozva**: 2026-03-30

---

## 📊 PROJEKT ÁTTEKINTÉS

### Jelenlegi Állapot
- **Fájlok száma**: 367
- **`# type: ignore` használat**: 369 db
- **🔴 VULNERABLE**: 19 fájl (5.2%) - failed tesztek
- **🟡 WARNING**: 31 fájl (8.4%) - alacsony coverage
- **✅ SECURE**: 317 fájl (86.4%)

### Végcél (12. hét vége)
- ✅ **0 VULNERABLE** fájl
- ✅ **0 WARNING** fájl
- ✅ **367 SECURE** fájl
- ✅ **<50 `# type: ignore`** (dokumentált, indokolt)
- ✅ **100% coverage** kritikus modulokban (core, data, processors)
- ✅ **0 QA hiba** (Ruff, Mypy, Pylance)

---

## 🗺️ FÁZISOK ÉS MILESTONE-OK

### **FÁZIS 1: KRITIKUS HIBÁK JAVÍTÁSA (1-2 hét) - P0 🔴**

**Cél**: 19 VULNERABLE fájl stabilizálása, failed tesztek javítása

#### Milestone 1.1: Core Infrastructure Stabilizálás (1. hét)
**Fájlok**: 5 db
- [`neural_ai/core/__init__.py`](../../../neural_ai/core/__init__.py) - 7 failed teszt
- [`neural_ai/core/config/factory.py`](../../../neural_ai/core/config/factory.py) - 2 failed teszt
- [`neural_ai/core/config/implementations/__init__.py`](../../../neural_ai/core/config/implementations/__init__.py) - 1 failed teszt
- [`neural_ai/core/events/factory.py`](../../../neural_ai/core/events/factory.py) - 4 failed teszt
- [`neural_ai/core/logger/implementations/default_logger.py`](../../../neural_ai/core/logger/implementations/default_logger.py) - 8 failed teszt

**Függőség**: Nincs
**Kockázat**: Bootstrap hibák → teljes rendszer instabil
**Deliverable**: 
- 5 fájl ✅ SECURE
- 22 teszt pass
- `# type: ignore` audit és javítás

#### Milestone 1.2: Database & Domain Stabilizálás (2. hét)
**Fájlok**: 4 db
- [`neural_ai/core/db/implementations/sqlalchemy_session.py`](../../../neural_ai/core/db/implementations/sqlalchemy_session.py) - 16 failed teszt
- [`neural_ai/processors/dimensions/d01_price/factory.py`](../../../neural_ai/processors/dimensions/d01_price/factory.py) - 1 failed teszt
- [`neural_ai/processors/dimensions/d02_support/implementations/support_processor.py`](../../../neural_ai/processors/dimensions/d02_support/implementations/support_processor.py) - 16 failed teszt
- [`neural_ai/ui/factory.py`](../../../neural_ai/ui/factory.py) - 2 failed teszt

**Függőség**: Milestone 1.1 (core stabil)
**Kockázat**: Adatbázis hibák → data loss, domain logika törés
**Deliverable**: 
- 4 fájl ✅ SECURE
- 35 teszt pass
- SQLAlchemy async típusok javítása

#### Milestone 1.3: Test Infrastructure Javítás (2. hét vége)
**Fájlok**: 10 db teszt fájl
- [`tests/neural_ai/core/test_core_init.py`](../../../tests/neural_ai/core/test_core_init.py) - 7 failed
- [`tests/neural_ai/core/config/test_config_factory.py`](../../../tests/neural_ai/core/config/test_config_factory.py) - 2 failed
- [`tests/neural_ai/core/config/implementations/test_config_implementations_init.py`](../../../tests/neural_ai/core/config/implementations/test_config_implementations_init.py) - 1 failed
- [`tests/neural_ai/core/db/implementations/test_sqlalchemy_session.py`](../../../tests/neural_ai/core/db/implementations/test_sqlalchemy_session.py) - 16 failed
- [`tests/neural_ai/core/events/test_events_factory.py`](../../../tests/neural_ai/core/events/test_events_factory.py) - 4 failed
- [`tests/neural_ai/core/logger/implementations/test_default_logger.py`](../../../tests/neural_ai/core/logger/implementations/test_default_logger.py) - 8 failed
- [`tests/neural_ai/processors/dimensions/d01_price/test_d01_factory.py`](../../../tests/neural_ai/processors/dimensions/d01_price/test_d01_factory.py) - 1 failed
- [`tests/neural_ai/processors/dimensions/d02_support/implementations/test_support_processor.py`](../../../tests/neural_ai/processors/dimensions/d02_support/implementations/test_support_processor.py) - 16 failed
- [`tests/neural_ai/ui/test_ui_factory.py`](../../../tests/neural_ai/ui/test_ui_factory.py) - 2 failed
- [`tests/scripts/test_validation_end_to_end.py`](../../../tests/scripts/test_validation_end_to_end.py) - 1 failed

**Függőség**: Milestone 1.1, 1.2
**Kockázat**: Teszt infrastruktúra törött → false positive/negative
**Deliverable**: 
- 10 teszt fájl javítva
- 91 teszt pass
- MagicMock spec használat

**Fázis 1 Eredmény**: 🔴 19 VULNERABLE → ✅ 0 VULNERABLE

---

### **FÁZIS 2: INFRASTRUCTURE LAYER TISZTÍTÁS (3-5. hét) - P1 🟠**

**Cél**: [`neural_ai/core/`](../../../neural_ai/core/) könyvtár `# type: ignore` minimalizálása

#### Milestone 2.1: Core Base & Config (3. hét)
**Fájlok**: 22 db
- [`neural_ai/core/base/`](../../../neural_ai/core/base/) - 12 fájl
- [`neural_ai/core/config/`](../../../neural_ai/core/config/) - 10 fájl

**Fókusz**:
- DI Container típus problémák → `typing.cast()` használat
- Singleton metaclass → stub fájl ([`singleton.pyi`](../../../neural_ai/core/base/implementations/singleton.pyi))
- Pydantic config validáció típusok

**Függőség**: Fázis 1 (stabil tesztek)
**Kockázat**: DI Container törés → bootstrap fail
**Deliverable**: 
- 22 fájl auditálva
- <10 `# type: ignore` összesen
- 1 stub fájl létrehozva

#### Milestone 2.2: Logger & Events (4. hét)
**Fájlok**: 18 db
- [`neural_ai/core/logger/`](../../../neural_ai/core/logger/) - 11 fájl
- [`neural_ai/core/events/`](../../../neural_ai/core/events/) - 7 fájl

**Fókusz**:
- ZeroMQ típus problémák → stub fájl ([`zeromq_bus.pyi`](../../../neural_ai/core/events/implementations/zeromq_bus.pyi))
- Structlog típusok → Protocol használat
- Logger factory típus inferencia

**Függőség**: Milestone 2.1
**Kockázat**: Logging törés → debug nehéz
**Deliverable**: 
- 18 fájl auditálva
- <8 `# type: ignore` összesen
- 1 stub fájl létrehozva

#### Milestone 2.3: DB & System & Utils (5. hét)
**Fájlok**: 32 db
- [`neural_ai/core/db/`](../../../neural_ai/core/db/) - 13 fájl
- [`neural_ai/core/system/`](../../../neural_ai/core/system/) - 9 fájl
- [`neural_ai/core/utils/`](../../../neural_ai/core/utils/) - 10 fájl

**Fókusz**:
- SQLAlchemy async típusok → `cast()` használat
- AsyncEngine, AsyncSession típus annotációk
- HardwareInfo platform specifikus típusok

**Függőség**: Milestone 2.2
**Kockázat**: Adatbázis típus hibák → runtime error
**Deliverable**: 
- 32 fájl auditálva
- <15 `# type: ignore` összesen
- SQLAlchemy stub fájl (opcionális)

**Fázis 2 Eredmény**: 70+ core fájl tiszta, <35 `# type: ignore` összesen

---

### **FÁZIS 3: DOMAIN & DATA LAYER (6-7. hét) - P1 🟠**

**Cél**: Domain logika és adatkezelés típusbiztonság növelése

#### Milestone 3.1: Processors (6. hét)
**Fájlok**: 25 db
- [`neural_ai/processors/`](../../../neural_ai/processors/) - teljes könyvtár

**Fókusz**:
- Polars DataFrame típusok → Protocol/cast
- Dimension processzorok típus annotációk
- Pipeline orchestrator típusbiztonság

**Függőség**: Fázis 2 (core stabil)
**Kockázat**: Dimension logika törés → rossz jelek
**Deliverable**: 
- 25 fájl auditálva
- <10 `# type: ignore` összesen
- Polars Protocol definíció (opcionális)

#### Milestone 3.2: Data Storage & Ingestion (7. hét)
**Fájlok**: 20 db
- [`neural_ai/data/storage/`](../../../neural_ai/data/storage/) - 12 fájl
- [`neural_ai/data/ingestion/`](../../../neural_ai/data/ingestion/) - 8 fájl

**Fókusz**:
- Parquet I/O típusok → cast használat
- FastParquet backend típus problémák
- MarketDataPersister buffer típusok

**Függőség**: Milestone 3.1
**Kockázat**: Adatvesztés → corrupt parquet
**Deliverable**: 
- 20 fájl auditálva
- <8 `# type: ignore` összesen
- Parquet stub fájl (opcionális)

**Fázis 3 Eredmény**: 45+ domain/data fájl tiszta, <18 `# type: ignore` összesen

---

### **FÁZIS 4: INPUT & PRESENTATION LAYER (8-9. hét) - P2 🟡**

**Cél**: Adatforrások és UI típusbiztonság javítása

#### Milestone 4.1: Collectors (8. hét)
**Fájlok**: 12 db
- [`neural_ai/collectors/jforex/`](../../../neural_ai/collectors/jforex/) - 8 fájl
- [`neural_ai/collectors/mt5/`](../../../neural_ai/collectors/mt5/) - 4 fájl

**Fókusz**:
- Bi5 decoder típusok → stub fájl
- JForex bridge Java interop típusok
- MT5 API típus problémák

**Függőség**: Fázis 3
**Kockázat**: Adatforrás hibák → rossz tick adat
**Deliverable**: 
- 12 fájl auditálva
- <5 `# type: ignore` összesen
- 1 stub fájl (bi5 decoder)

#### Milestone 4.2: UI Layer (9. hét)
**Fájlok**: 30 db
- [`neural_ai/ui/`](../../../neural_ai/ui/) - teljes könyvtár

**Fókusz**:
- Streamlit típus problémák → dokumentált ignore
- Session state típusok → TypedDict
- Widget típus annotációk

**Függőség**: Milestone 4.1
**Kockázat**: UI crash → felhasználói élmény rossz
**Deliverable**: 
- 30 fájl auditálva
- <15 `# type: ignore` (dokumentált)
- Streamlit stub fájl (opcionális)

**Fázis 4 Eredmény**: 42+ input/ui fájl tiszta, <20 `# type: ignore` összesen

---

### **FÁZIS 5: TEST & SCRIPT TISZTÍTÁS (10. hét) - P2 🟡**

**Cél**: Teszt és script fájlok típusbiztonság javítása

#### Milestone 5.1: Test Files (10. hét eleje)
**Fájlok**: 150+ db
- [`tests/`](../../../tests/) - teljes könyvtár

**Fókusz**:
- MagicMock spec használat
- `patch.object()` helyett context manager
- Fixture típus annotációk

**Függőség**: Fázis 1-4 (stabil kód)
**Kockázat**: Teszt törés → false negative
**Deliverable**: 
- 150+ fájl auditálva
- <30 `# type: ignore` összesen
- Pytest stub fájl (opcionális)

#### Milestone 5.2: Scripts (10. hét vége)
**Fájlok**: 18 db
- [`scripts/`](../../../scripts/) - teljes könyvtár

**Fókusz**:
- Privát metódus hívás dokumentálása
- CLI argument típusok
- Script utility típus annotációk

**Függőség**: Milestone 5.1
**Kockázat**: Script törés → CI/CD fail
**Deliverable**: 
- 18 fájl auditálva
- <10 `# type: ignore` összesen

**Fázis 5 Eredmény**: 168+ teszt/script fájl tiszta, <40 `# type: ignore` összesen

---

### **FÁZIS 6: COVERAGE 100% & FINALIZÁLÁS (11-12. hét) - P1 🟠**

**Cél**: Teljes projekt 100% coverage és dokumentáció

#### Milestone 6.1: WARNING Fájlok Coverage Növelés (11. hét)
**Fájlok**: 31 db WARNING fájl

**Prioritási sorrend**:
1. [`neural_ai/ui/services/data_service.py`](../../../neural_ai/ui/services/data_service.py) - 35% → 100%
2. [`neural_ai/ui/pages/03_📥_Data_Hub.py`](../../../neural_ai/ui/pages/03_📥_Data_Hub.py) - 39% → 100%
3. [`neural_ai/ui/pages/05_🪲_Strategy_Lab.py`](../../../neural_ai/ui/pages/05_🪲_Strategy_Lab.py) - 39% → 100%
4. [`neural_ai/ui/services/strategy_service.py`](../../../neural_ai/ui/services/strategy_service.py) - 56% → 100%
5. [`neural_ai/ui/streamlit_app.py`](../../../neural_ai/ui/streamlit_app.py) - 58% → 100%
6. [`neural_ai/ui/core_bridge.py`](../../../neural_ai/ui/core_bridge.py) - 60% → 100%
7. [`neural_ai/core/logger/implementations/rotating_file_logger.py`](../../../neural_ai/core/logger/implementations/rotating_file_logger.py) - 64% → 100%
8. [`neural_ai/core/base/implementations/singleton.py`](../../../neural_ai/core/base/implementations/singleton.py) - 71% → 100%
9. További 23 fájl (73-88% coverage)

**Függőség**: Fázis 1-5
**Kockázat**: Hiányzó edge case tesztek → production bug
**Deliverable**: 
- 31 fájl 100% coverage
- Új tesztek írása
- Skipped tesztek aktiválása

#### Milestone 6.2: Stub Fájlok & Dokumentáció (12. hét eleje)
**Fájlok**: 3 stub fájl + dokumentáció

**Stub fájlok**:
1. [`neural_ai/core/base/implementations/singleton.pyi`](../../../neural_ai/core/base/implementations/singleton.pyi) - Metaclass típusok
2. [`neural_ai/core/base/implementations/di_container.pyi`](../../../neural_ai/core/base/implementations/di_container.pyi) - Dynamic attributes
3. [`neural_ai/core/events/implementations/zeromq_bus.pyi`](../../../neural_ai/core/events/implementations/zeromq_bus.pyi) - ZeroMQ típusok

**Dokumentáció**:
- Minden megmaradt `# type: ignore` dokumentálása
- Type safety best practices guide
- Stub fájl használati útmutató

**Függőség**: Milestone 6.1
**Kockázat**: Dokumentáció hiány → jövőbeli confusion
**Deliverable**: 
- 3 stub fájl létrehozva
- <50 dokumentált `# type: ignore`
- Type safety guide

#### Milestone 6.3: Final QA Gate (12. hét vége)
**Fájlok**: Teljes projekt (367 fájl)

**QA Checklist**:
```bash
# 1. Linting
/home/elynea/miniconda3/envs/neural-ai-next/bin/ruff check .

# 2. Type Check (Mypy)
/home/elynea/miniconda3/envs/neural-ai-next/bin/mypy neural_ai

# 3. Type Check (Pyright)
/home/elynea/miniconda3/envs/neural-ai-next/bin/pyright neural_ai

# 4. Type Check (Pylance) - VS Code
# Automatikus strict mode check

# 5. Tests
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest -vv

# 5. Coverage
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest --cov=neural_ai --cov-report=html --cov-branch

# 6. TASK_TREE frissítés
python scripts/generate.py
```

**Függőség**: Milestone 6.2
**Kockázat**: Regressziós hibák
**Deliverable**: 
- ✅ 0 Ruff hiba
- ✅ 0 Mypy hiba
- ✅ 0 Pylance hiba (strict mode)
- ✅ 100% teszt pass
- ✅ 367 SECURE fájl
- ✅ TASK_TREE finalizálva

**Fázis 6 Eredmény**: 🟡 31 WARNING → ✅ 0 WARNING, projekt production-ready

---

## 📋 PRIORITÁSI MÁTRIX

| Prioritás | Fázis | Időkeret | Fájlok | Kritikusság | Deliverable |
|:----------|:------|:---------|:-------|:------------|:------------|
| **P0** 🔴 | Fázis 1 | 1-2 hét | 19 | BLOCKER | 0 VULNERABLE, 91 teszt pass |
| **P1** 🟠 | Fázis 2 | 3-5 hét | 70+ | FONTOS | Core tiszta, <35 ignore |
| **P1** 🟠 | Fázis 3 | 6-7 hét | 45+ | FONTOS | Domain tiszta, <18 ignore |
| **P1** 🟠 | Fázis 6 | 11-12 hét | 31 | FONTOS | 100% coverage |
| **P2** 🟡 | Fázis 4 | 8-9 hét | 42+ | HASZNOS | Input/UI tiszta, <20 ignore |
| **P2** 🟡 | Fázis 5 | 10 hét | 168+ | HASZNOS | Test/Script tiszta, <40 ignore |

---

## 🔄 VÉGREHAJTÁSI PROTOKOLL

### Fájlonkénti Workflow (MINDEN FÁJLNÁL KÖTELEZŐ)

1. **Olvasás**: Reader mód → fájl beolvasás
2. **Audit**: `# type: ignore` azonosítás és kategorizálás
   - 🔴 Indokolatlan → refaktorálás
   - 🟡 Jobb megoldás → cast/Protocol/stub
   - 🟢 Indokolt → dokumentálás
3. **Javítás**: Megfelelő alternatíva alkalmazása
4. **QA Gate**: Linting, type check, tesztek, coverage
5. **Commit**: Atomic commit (1 fájl = 1 commit)
6. **TASK_TREE**: Frissítés
7. **Következő fájl**: Ismétlés

### Type Safety Alternatívák

#### 1. `typing.cast()` használata
```python
# ❌ ROSSZ
self._logger = resolved_logger  # type: ignore[assignment]

# ✅ JÓ
from typing import cast
self._logger = cast(LoggerInterface, resolved_logger)
```

#### 2. MagicMock spec használata
```python
# ❌ ROSSZ
mock_service = MagicMock()  # type: ignore

# ✅ JÓ
mock_service = MagicMock(spec=StrategyServiceInterface)
```

#### 3. Specifikus error code
```python
# ❌ ROSSZ
result = func()  # type: ignore

# ✅ JÓ
# Mypy nem ismeri fel a Polars DataFrame típust
result = func()  # type: ignore[assignment]
```

#### 4. Protocol használata
```python
# ❌ ROSSZ
def process(obj: Any) -> Any:  # type: ignore

# ✅ JÓ
from typing import Protocol

class Processable(Protocol):
    def process(self) -> None: ...

def process(obj: Processable) -> None:
    obj.process()
```

#### 5. Stub fájl (.pyi)
```python
# singleton.pyi
from typing import TypeVar, Type

T = TypeVar('T')

class SingletonMeta(type):
    _instances: dict[Type[T], T]
    _instance: T
    def __call__(cls: Type[T], *args: Any, **kwargs: Any) -> T: ...
```

### QA Gate Parancsok

```bash
# 1. Linting
/home/elynea/miniconda3/envs/neural-ai-next/bin/ruff check neural_ai/path/to/file.py

# 2. Type Check (Mypy)
/home/elynea/miniconda3/envs/neural-ai-next/bin/mypy neural_ai/path/to/file.py

# 3. Type Check (Pyright)
/home/elynea/miniconda3/envs/neural-ai-next/bin/pyright neural_ai/path/to/file.py

# 4. Tests
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/path/to/test_file.py -vv

# 5. Coverage
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest \
  --cov=neural_ai/path/to/file \
  --cov-report=term-missing \
  --cov-branch

# 6. HA MINDEN PASS → Commit
git add neural_ai/path/to/file.py tests/path/to/test_file.py
git commit -m "refactor(type-safety): [fájlnév] type ignore javítás - [leírás]"

# 7. TASK_TREE frissítés
python scripts/generate.py
git add docs/development/TASK_TREE.md docs/development/TASK_TREE.html
git commit -m "docs(task-tree): [fájlnév] státusz frissítés"
```

### Commit Formátum

```
refactor(type-safety): [modul/fájl] type ignore javítás

- Eltávolítva: X db # type: ignore
- Helyettesítve: typing.cast() / MagicMock(spec=) / Protocol
- Dokumentálva: Y db indokolt ignore
- Coverage: Z% → 100%
- QA Gate: ✅ 0 hiba
```

---

## 🚨 KOCKÁZATOK ÉS MITIGÁCIÓ

| Kockázat | Valószínűség | Hatás | Mitigáció |
|:---------|:-------------|:------|:----------|
| Bootstrap törés (core hibák) | Magas | Kritikus | Fázis 1 prioritás, atomic commit |
| Regressziós hibák | Közepes | Magas | QA Gate minden commit után |
| Coverage csökkenés | Alacsony | Közepes | Coverage check kötelező |
| Túl sok `# type: ignore` marad | Közepes | Alacsony | Dokumentálási szabvány |
| Időcsúszás (12 hét → 16 hét) | Közepes | Közepes | P0/P1 fókusz, P2 opcionális |
| Stub fájl inkompatibilitás | Alacsony | Közepes | Mypy/Pylance tesztelés |
| Domain logika törés | Alacsony | Kritikus | 100% teszt lefedettség |

---

## 📊 METRIKÁK ÉS KÖVETÉS

### Heti Jelentés (KÖTELEZŐ)

**Formátum**:
```markdown
## Hét X Jelentés (YYYY-MM-DD)

### Fázis: [Fázis név]
### Milestone: [Milestone név]

### Elvégzett munka:
- Fájlok száma: Auditált X / Javított Y / Hátralevő Z
- `# type: ignore`: Előtte A / Utána B / Csökkenés C%
- Coverage: Átlag D% / 100%-os fájlok E db
- QA hibák: Ruff F / Mypy G / Pylance H
- Tesztek: Pass I / Fail J / Skip K

### Problémák:
- [Probléma leírása]

### Következő hét terv:
- [Terv]
```

### Végső Metrikák (12. hét vége)

- ✅ **367/367 fájl** auditálva
- ✅ **<50 `# type: ignore`** (369 → <50, 86% csökkenés)
- ✅ **100% coverage** kritikus modulokban
- ✅ **0 QA hiba** (Ruff, Mypy, Pylance)
- ✅ **0 VULNERABLE, 0 WARNING** fájl
- ✅ **3 stub fájl** létrehozva
- ✅ **Type safety guide** dokumentálva

---

## 🎯 KÖVETKEZŐ LÉPÉSEK

### 1. Fázis 1 Indítása
**Delegálás**: Architect mód
**Feladat**: Milestone 1.1 részletes tervezés
**Fájlok**: [`PHASE1_PLAN.md`](PHASE1_PLAN.md)

### 2. Reader/Search Használat
**Minden fájl audit előtt**: Reader mód → fájl beolvasás
**Kód keresés**: Search mód → `# type: ignore` lokáció

### 3. Dokumentáció Frissítés
**TASK_TREE**: Minden commit után
**Roadmap**: Milestone befejezése után
**Heti jelentés**: Minden hét vége

---

## 📚 KAPCSOLÓDÓ DOKUMENTUMOK

- [`DELEGATION_COMMANDS.md`](DELEGATION_COMMANDS.md) - Delegálási parancsok minden fázishoz
- [`PHASE1_PLAN.md`](PHASE1_PLAN.md) - Fázis 1 részletes terv
- [`PHASE2_PLAN.md`](PHASE2_PLAN.md) - Fázis 2 részletes terv
- [`PHASE3_PLAN.md`](PHASE3_PLAN.md) - Fázis 3 részletes terv
- [`PHASE4_PLAN.md`](PHASE4_PLAN.md) - Fázis 4 részletes terv
- [`PHASE5_PLAN.md`](PHASE5_PLAN.md) - Fázis 5 részletes terv
- [`PHASE6_PLAN.md`](PHASE6_PLAN.md) - Fázis 6 részletes terv
- [`../../TASK_TREE.md`](../../TASK_TREE.md) - Projekt állapot
- [`../../../.roo/rules-planner/AGENTS.md`](../../../.roo/rules-planner/AGENTS.md) - Agent szabályok

---

**Verzió**: 1.0
**Utolsó frissítés**: 2026-03-30
**Következő felülvizsgálat**: Minden milestone befejezése után
