# 🎯 TYPE SAFETY REFACTORING - DELEGÁLÁSI PARANCSOK

**Projekt**: Neural AI Next - Type Safety Audit & Refactoring
**Verzió**: 1.0
**Létrehozva**: 2026-03-30

---

## 📋 HASZNÁLATI ÚTMUTATÓ

Ez a dokumentum tartalmazza az **összes delegálási parancsot** a Type Safety Refactoring projekthez. Minden fázishoz és milestone-hoz tartozik egy konkrét parancs, amelyet a megfelelő Roo Code módba kell másolni.

**Workflow**:
1. Cline (Lead Developer) kiválasztja a következő feladatot
2. Kimásolja a megfelelő parancsot ebből a fájlból
3. Átmásolja Roo Code-ba (megfelelő mód)
4. Roo Code végrehajtja
5. Eredmény visszamásolása Cline-nak
6. Cline ellenőrzi és továbblép

---

## 🔴 FÁZIS 1: KRITIKUS HIBÁK JAVÍTÁSA (1-2 hét)

### Milestone 1.1: Core Infrastructure Stabilizálás

**Mód**: `code-fix`

**Parancs**:
```
Code-Fix! Javítsd a Core Infrastructure kritikus hibáit.

FELADAT: 5 fájl, 22 failed teszt javítása

FÁJLOK (prioritási sorrendben):
1. neural_ai/core/__init__.py - 7 failed teszt
2. neural_ai/core/config/factory.py - 2 failed teszt
3. neural_ai/core/config/implementations/__init__.py - 1 failed teszt
4. neural_ai/core/events/factory.py - 4 failed teszt
5. neural_ai/core/logger/implementations/default_logger.py - 8 failed teszt

MINDEN FÁJLNÁL:
1. Reader! Olvasd be a fájlt és a teszt fájlt
2. Elemezd a failed teszteket (mi a hiba, miért bukik)
3. Azonosítsd a # type: ignore használatokat
4. Javítsd a hibákat:
   - typing.cast() használata típus konverzióhoz
   - MagicMock(spec=Interface) mockokhoz
   - Specifikus error code (pl. [assignment], [attr-defined])
5. QA Gate futtatása:
   /home/elynea/miniconda3/envs/neural-ai-next/bin/ruff check neural_ai/core/__init__.py
   /home/elynea/miniconda3/envs/neural-ai-next/bin/mypy neural_ai/core/__init__.py
   /home/elynea/miniconda3/envs/neural-ai-next/bin/pyright neural_ai/core/__init__.py
   /home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/neural_ai/core/test_core_init.py -vv
   /home/elynea/miniconda3/envs/neural-ai-next/bin/pytest --cov=neural_ai/core/__init__.py --cov-branch
6. HA PASS → Atomic commit:
   git add neural_ai/core/__init__.py tests/neural_ai/core/test_core_init.py
   git commit -m "fix(core): __init__ type ignore javítás - bootstrap stabilizálás"
7. TASK_TREE frissítés:
   python scripts/generate.py
   git add docs/development/TASK_TREE.md
   git commit -m "docs(task-tree): core/__init__ státusz frissítés 🔴→✅"
8. KÖVETKEZŐ FÁJL

IDŐKERET: 1 hét
DELIVERABLE: 5 fájl ✅, 22 teszt pass, <5 # type: ignore
```

---

### Milestone 1.2: Database & Domain Stabilizálás

**Mód**: `code-fix`

**Parancs**:
```
Code-Fix! Javítsd a Database & Domain kritikus hibáit.

FELADAT: 4 fájl, 35 failed teszt javítása

FÁJLOK (prioritási sorrendben):
1. neural_ai/core/db/implementations/sqlalchemy_session.py - 16 failed teszt
2. neural_ai/processors/dimensions/d01_price/factory.py - 1 failed teszt
3. neural_ai/processors/dimensions/d02_support/implementations/support_processor.py - 16 failed teszt
4. neural_ai/ui/factory.py - 2 failed teszt

FÓKUSZ:
- SQLAlchemy async típusok → cast(AsyncEngine, ...) használat
- AsyncSession típus annotációk
- Polars DataFrame típus problémák

MINDEN FÁJLNÁL:
1. Reader! Olvasd be a fájlt és a teszt fájlt
2. Elemezd a failed teszteket
3. Javítsd a típus hibákat (cast, Protocol)
4. QA Gate futtatása
5. Atomic commit
6. TASK_TREE frissítés
7. KÖVETKEZŐ FÁJL

FÜGGŐSÉG: Milestone 1.1 befejezve
IDŐKERET: 1 hét
DELIVERABLE: 4 fájl ✅, 35 teszt pass, <8 # type: ignore
```

---

### Milestone 1.3: Test Infrastructure Javítás

**Mód**: `test-unit`

**Parancs**:
```
Test-Unit! Javítsd a Test Infrastructure hibáit.

FELADAT: 10 teszt fájl, 91 failed teszt javítása

FÁJLOK:
1. tests/neural_ai/core/test_core_init.py - 7 failed
2. tests/neural_ai/core/config/test_config_factory.py - 2 failed
3. tests/neural_ai/core/config/implementations/test_config_implementations_init.py - 1 failed
4. tests/neural_ai/core/db/implementations/test_sqlalchemy_session.py - 16 failed
5. tests/neural_ai/core/events/test_events_factory.py - 4 failed
6. tests/neural_ai/core/logger/implementations/test_default_logger.py - 8 failed
7. tests/neural_ai/processors/dimensions/d01_price/test_d01_factory.py - 1 failed
8. tests/neural_ai/processors/dimensions/d02_support/implementations/test_support_processor.py - 16 failed
9. tests/neural_ai/ui/test_ui_factory.py - 2 failed
10. tests/scripts/test_validation_end_to_end.py - 1 failed

FÓKUSZ:
- MagicMock(spec=Interface) használat
- patch.object() context manager
- Fixture típus annotációk

MINDEN FÁJLNÁL:
1. Reader! Olvasd be a teszt fájlt
2. Elemezd a failed teszteket
3. Javítsd a mock problémákat:
   mock_service = MagicMock(spec=StrategyServiceInterface)
4. QA Gate futtatása
5. Atomic commit
6. TASK_TREE frissítés
7. KÖVETKEZŐ FÁJL

FÜGGŐSÉG: Milestone 1.1, 1.2 befejezve
IDŐKERET: 1 hét vége
DELIVERABLE: 10 fájl ✅, 91 teszt pass
```

---

## 🟠 FÁZIS 2: INFRASTRUCTURE LAYER TISZTÍTÁS (3-5. hét)

### Milestone 2.1: Core Base & Config

**Mód**: `code-refactor`

**Parancs**:
```
Code-Refactor! Tisztítsd meg a Core Base & Config modulokat.

FELADAT: 22 fájl # type: ignore audit és javítás

FÁJLOK:
- neural_ai/core/base/ - 12 fájl
- neural_ai/core/config/ - 10 fájl

FÓKUSZ:
- DI Container típus problémák → typing.cast() használat
- Singleton metaclass → stub fájl (singleton.pyi)
- Pydantic config validáció típusok

MINDEN FÁJLNÁL:
1. Reader! Olvasd be a fájlt
2. Keress minden # type: ignore használatot
3. Kategorizáld:
   🔴 Indokolatlan → refaktorálni kell
   🟡 Indokolt, de van jobb megoldás → cast, Protocol, stub
   🟢 Indokolt és szükséges → dokumentálni kell
4. Javítsd a 🔴 és 🟡 eseteket
5. Dokumentáld a 🟢 eseteket:
   # Mypy nem ismeri fel a metaclass típust
   result = func()  # type: ignore[attr-defined]
6. QA Gate futtatása
7. Atomic commit
8. TASK_TREE frissítés
9. KÖVETKEZŐ FÁJL

STUB FÁJL LÉTREHOZÁSA:
- neural_ai/core/base/implementations/singleton.pyi
- Metaclass típusok definiálása

FÜGGŐSÉG: Fázis 1 befejezve
IDŐKERET: 1 hét
DELIVERABLE: 22 fájl auditálva, <10 # type: ignore, 1 stub fájl
```

---

### Milestone 2.2: Logger & Events

**Mód**: `code-refactor`

**Parancs**:
```
Code-Refactor! Tisztítsd meg a Logger & Events modulokat.

FELADAT: 18 fájl # type: ignore audit és javítás

FÁJLOK:
- neural_ai/core/logger/ - 11 fájl
- neural_ai/core/events/ - 7 fájl

FÓKUSZ:
- ZeroMQ típus problémák → stub fájl (zeromq_bus.pyi)
- Structlog típusok → Protocol használat
- Logger factory típus inferencia

MINDEN FÁJLNÁL:
1. Reader! Olvasd be a fájlt
2. Audit # type: ignore használatok
3. Javítsd a típus problémákat
4. QA Gate futtatása
5. Atomic commit
6. TASK_TREE frissítés
7. KÖVETKEZŐ FÁJL

STUB FÁJL LÉTREHOZÁSA:
- neural_ai/core/events/implementations/zeromq_bus.pyi
- ZeroMQ socket típusok definiálása

FÜGGŐSÉG: Milestone 2.1 befejezve
IDŐKERET: 1 hét
DELIVERABLE: 18 fájl auditálva, <8 # type: ignore, 1 stub fájl
```

---

### Milestone 2.3: DB & System & Utils

**Mód**: `code-refactor`

**Parancs**:
```
Code-Refactor! Tisztítsd meg a DB & System & Utils modulokat.

FELADAT: 32 fájl # type: ignore audit és javítás

FÁJLOK:
- neural_ai/core/db/ - 13 fájl
- neural_ai/core/system/ - 9 fájl
- neural_ai/core/utils/ - 10 fájl

FÓKUSZ:
- SQLAlchemy async típusok → cast() használat
- AsyncEngine, AsyncSession típus annotációk
- HardwareInfo platform specifikus típusok

MINDEN FÁJLNÁL:
1. Reader! Olvasd be a fájlt
2. Audit # type: ignore használatok
3. Javítsd a típus problémákat:
   engine = cast(AsyncEngine, create_async_engine(...))
4. QA Gate futtatása
5. Atomic commit
6. TASK_TREE frissítés
7. KÖVETKEZŐ FÁJL

FÜGGŐSÉG: Milestone 2.2 befejezve
IDŐKERET: 1 hét
DELIVERABLE: 32 fájl auditálva, <15 # type: ignore
```

---

## 🟠 FÁZIS 3: DOMAIN & DATA LAYER (6-7. hét)

### Milestone 3.1: Processors

**Mód**: `code-refactor`

**Parancs**:
```
Code-Refactor! Tisztítsd meg a Processors modulokat.

FELADAT: 25 fájl # type: ignore audit és javítás

FÁJLOK:
- neural_ai/processors/ - teljes könyvtár (25 fájl)

FÓKUSZ:
- Polars DataFrame típusok → Protocol/cast
- Dimension processzorok típus annotációk
- Pipeline orchestrator típusbiztonság

MINDEN FÁJLNÁL:
1. Reader! Olvasd be a fájlt
2. Audit # type: ignore használatok
3. Javítsd a Polars típus problémákat:
   df = cast(pl.DataFrame, result)
4. QA Gate futtatása
5. Atomic commit
6. TASK_TREE frissítés
7. KÖVETKEZŐ FÁJL

FÜGGŐSÉG: Fázis 2 befejezve
IDŐKERET: 1 hét
DELIVERABLE: 25 fájl auditálva, <10 # type: ignore
```

---

### Milestone 3.2: Data Storage & Ingestion

**Mód**: `code-refactor`

**Parancs**:
```
Code-Refactor! Tisztítsd meg a Data Storage & Ingestion modulokat.

FELADAT: 20 fájl # type: ignore audit és javítás

FÁJLOK:
- neural_ai/data/storage/ - 12 fájl
- neural_ai/data/ingestion/ - 8 fájl

FÓKUSZ:
- Parquet I/O típusok → cast használat
- FastParquet backend típus problémák
- MarketDataPersister buffer típusok

MINDEN FÁJLNÁL:
1. Reader! Olvasd be a fájlt
2. Audit # type: ignore használatok
3. Javítsd a Parquet típus problémákat
4. QA Gate futtatása
5. Atomic commit
6. TASK_TREE frissítés
7. KÖVETKEZŐ FÁJL

FÜGGŐSÉG: Milestone 3.1 befejezve
IDŐKERET: 1 hét
DELIVERABLE: 20 fájl auditálva, <8 # type: ignore
```

---

## 🟡 FÁZIS 4: INPUT & PRESENTATION LAYER (8-9. hét)

### Milestone 4.1: Collectors

**Mód**: `code-refactor`

**Parancs**:
```
Code-Refactor! Tisztítsd meg a Collectors modulokat.

FELADAT: 12 fájl # type: ignore audit és javítás

FÁJLOK:
- neural_ai/collectors/jforex/ - 8 fájl
- neural_ai/collectors/mt5/ - 4 fájl

FÓKUSZ:
- Bi5 decoder típusok → stub fájl
- JForex bridge Java interop típusok
- MT5 API típus problémák

MINDEN FÁJLNÁL:
1. Reader! Olvasd be a fájlt
2. Audit # type: ignore használatok
3. Javítsd a típus problémákat
4. QA Gate futtatása
5. Atomic commit
6. TASK_TREE frissítés
7. KÖVETKEZŐ FÁJL

FÜGGŐSÉG: Fázis 3 befejezve
IDŐKERET: 1 hét
DELIVERABLE: 12 fájl auditálva, <5 # type: ignore
```

---

### Milestone 4.2: UI Layer

**Mód**: `code-refactor`

**Parancs**:
```
Code-Refactor! Tisztítsd meg a UI Layer modulokat.

FELADAT: 30 fájl # type: ignore audit és javítás

FÁJLOK:
- neural_ai/ui/ - teljes könyvtár (30 fájl)

FÓKUSZ:
- Streamlit típus problémák → dokumentált ignore
- Session state típusok → TypedDict
- Widget típus annotációk

MINDEN FÁJLNÁL:
1. Reader! Olvasd be a fájlt
2. Audit # type: ignore használatok
3. Streamlit típus problémák DOKUMENTÁLÁSA (nem javítható):
   # Streamlit session_state nem típusos
   st.session_state.key = value  # type: ignore[attr-defined]
4. QA Gate futtatása
5. Atomic commit
6. TASK_TREE frissítés
7. KÖVETKEZŐ FÁJL

FÜGGŐSÉG: Milestone 4.1 befejezve
IDŐKERET: 1 hét
DELIVERABLE: 30 fájl auditálva, <15 # type: ignore (dokumentált)
```

---

## 🟡 FÁZIS 5: TEST & SCRIPT TISZTÍTÁS (10. hét)

### Milestone 5.1: Test Files

**Mód**: `test-unit`

**Parancs**:
```
Test-Unit! Tisztítsd meg a Test Files modulokat.

FELADAT: 150+ fájl # type: ignore audit és javítás

FÁJLOK:
- tests/ - teljes könyvtár (150+ fájl)

FÓKUSZ:
- MagicMock spec használat
- patch.object() helyett context manager
- Fixture típus annotációk

MINDEN FÁJLNÁL:
1. Reader! Olvasd be a teszt fájlt
2. Audit # type: ignore használatok
3. Javítsd a mock problémákat:
   # ❌ ROSSZ
   mock_service = MagicMock()  # type: ignore
   
   # ✅ JÓ
   mock_service = MagicMock(spec=StrategyServiceInterface)
4. QA Gate futtatása
5. Atomic commit
6. TASK_TREE frissítés
7. KÖVETKEZŐ FÁJL

FÜGGŐSÉG: Fázis 1-4 befejezve
IDŐKERET: 1 hét eleje
DELIVERABLE: 150+ fájl auditálva, <30 # type: ignore
```

---

### Milestone 5.2: Scripts

**Mód**: `code-refactor`

**Parancs**:
```
Code-Refactor! Tisztítsd meg a Scripts modulokat.

FELADAT: 18 fájl # type: ignore audit és javítás

FÁJLOK:
- scripts/ - teljes könyvtár (18 fájl)

FÓKUSZ:
- Privát metódus hívás dokumentálása
- CLI argument típusok
- Script utility típus annotációk

MINDEN FÁJLNÁL:
1. Reader! Olvasd be a script fájlt
2. Audit # type: ignore használatok
3. Dokumentáld a privát metódus hívásokat:
   # Teszt célból privát metódus hívása
   obj._private_method()  # type: ignore[attr-defined]
4. QA Gate futtatása
5. Atomic commit
6. TASK_TREE frissítés
7. KÖVETKEZŐ FÁJL

FÜGGŐSÉG: Milestone 5.1 befejezve
IDŐKERET: 1 hét vége
DELIVERABLE: 18 fájl auditálva, <10 # type: ignore
```

---

## 🟠 FÁZIS 6: COVERAGE 100% & FINALIZÁLÁS (11-12. hét)

### Milestone 6.1: WARNING Fájlok Coverage Növelés

**Mód**: `test-unit`

**Parancs**:
```
Test-Unit! Növeld a WARNING fájlok coverage-ét 100%-ra.

FELADAT: 31 fájl coverage növelése

PRIORITÁSI SORREND:
1. neural_ai/ui/services/data_service.py - 35% → 100%
2. neural_ai/ui/pages/03_📥_Data_Hub.py - 39% → 100%
3. neural_ai/ui/pages/05_🪲_Strategy_Lab.py - 39% → 100%
4. neural_ai/ui/services/strategy_service.py - 56% → 100%
5. neural_ai/ui/streamlit_app.py - 58% → 100%
6. neural_ai/ui/core_bridge.py - 60% → 100%
7. neural_ai/core/logger/implementations/rotating_file_logger.py - 64% → 100%
8. neural_ai/core/base/implementations/singleton.py - 71% → 100%
9. További 23 fájl (73-88% coverage)

MINDEN FÁJLNÁL:
1. Reader! Olvasd be a fájlt
2. Elemezd a coverage report-ot:
   /home/elynea/miniconda3/envs/neural-ai-next/bin/pytest --cov=neural_ai/ui/services/data_service.py --cov-report=term-missing --cov-branch
3. Azonosítsd a hiányzó teszteket (uncovered lines)
4. Írj új teszteket az uncovered részekhez
5. Aktiváld a skipped teszteket
6. QA Gate futtatása (100% coverage ellenőrzés)
7. Atomic commit
8. TASK_TREE frissítés
9. KÖVETKEZŐ FÁJL

FÜGGŐSÉG: Fázis 1-5 befejezve
IDŐKERET: 1 hét
DELIVERABLE: 31 fájl 100% coverage
```

---

### Milestone 6.2: Stub Fájlok & Dokumentáció

**Mód**: `docs-api`

**Parancs**:
```
Docs-API! Hozz létre stub fájlokat és dokumentáld a megmaradt # type: ignore használatokat.

FELADAT: 3 stub fájl + dokumentáció

STUB FÁJLOK:
1. neural_ai/core/base/implementations/singleton.pyi
   - Metaclass típusok definiálása
   - SingletonMeta típus annotációk

2. neural_ai/core/base/implementations/di_container.pyi
   - Dynamic attributes típusok
   - Container típus annotációk

3. neural_ai/core/events/implementations/zeromq_bus.pyi
   - ZeroMQ socket típusok
   - Pub/Sub típus annotációk

MINDEN STUB FÁJLNÁL:
1. Reader! Olvasd be az eredeti .py fájlt
2. Hozz létre .pyi stub fájlt
3. Definiáld a típusokat:
   from typing import TypeVar, Type
   T = TypeVar('T')
   class SingletonMeta(type):
       _instances: dict[Type[T], T]
       def __call__(cls: Type[T], *args: Any, **kwargs: Any) -> T: ...
4. QA Gate futtatása (Mypy ellenőrzés)
5. Atomic commit
6. KÖVETKEZŐ STUB FÁJL

DOKUMENTÁCIÓ:
- Minden megmaradt # type: ignore dokumentálása
- Type safety best practices guide írása
- Stub fájl használati útmutató

FÜGGŐSÉG: Milestone 6.1 befejezve
IDŐKERET: 1 hét eleje
DELIVERABLE: 3 stub fájl, <50 dokumentált # type: ignore, Type safety guide
```

---

### Milestone 6.3: Final QA Gate

**Mód**: `qa`

**Parancs**:
```
QA! Futtasd a Final QA Gate-et a teljes projekten.

FELADAT: Teljes projekt QA ellenőrzés (367 fájl)

QA CHECKLIST:
1. Linting (Ruff):
   /home/elynea/miniconda3/envs/neural-ai-next/bin/ruff check .

2. Type Check (Mypy):
   /home/elynea/miniconda3/envs/neural-ai-next/bin/mypy neural_ai

3. Type Check (Pylance):
   # Automatikus VS Code-ban (strict mode)

4. Tests:
   /home/elynea/miniconda3/envs/neural-ai-next/bin/pytest -vv

5. Coverage:
   /home/elynea/miniconda3/envs/neural-ai-next/bin/pytest --cov=neural_ai --cov-report=html --cov-branch

6. TASK_TREE frissítés:
   python scripts/generate.py
   git add docs/development/TASK_TREE.md docs/development/TASK_TREE.html
   git commit -m "docs(task-tree): Final QA Gate - projekt finalizálás"

ELVÁRT EREDMÉNYEK:
- ✅ 0 Ruff hiba
- ✅ 0 Mypy hiba
- ✅ 0 Pylance hiba (strict mode)
- ✅ 100% teszt pass
- ✅ 367 SECURE fájl
- ✅ <50 # type: ignore (dokumentált)

HA MINDEN PASS:
- Review! Delegálás code review-ra
- Commit! Delegálás final commit-ra

HA VAN HIBA:
- Debug-Complex! Delegálás hibakeresésre

FÜGGŐSÉG: Milestone 6.2 befejezve
IDŐKERET: 1 hét vége
DELIVERABLE: Projekt production-ready, 0 VULNERABLE, 0 WARNING
```

---

## 📊 HETI JELENTÉS SABLON

**Mód**: `docs-guide`

**Parancs**:
```
Docs-Guide! Készíts heti jelentést a Type Safety Refactoring projektről.

SABLON:
## Hét X Jelentés (YYYY-MM-DD)

### Fázis: [Fázis név]
### Milestone: [Milestone név]

### Elvégzett munka:
- Fájlok száma: Auditált X / Javított Y / Hátralevő Z
- # type: ignore: Előtte A / Utána B / Csökkenés C%
- Coverage: Átlag D% / 100%-os fájlok E db
- QA hibák: Ruff F / Mypy G / Pylance H
- Tesztek: Pass I / Fail J / Skip K

### Problémák:
- [Probléma leírása]

### Következő hét terv:
- [Terv]

MENTÉS:
- docs/development/type-safety-refactoring/weekly-reports/week-X.md
```

---

## 🎯 GYORS REFERENCIA

| Fázis | Milestone | Mód | Fájlok | Időkeret |
|:------|:----------|:----|:-------|:---------|
| 1 | 1.1 Core Infrastructure | code-fix | 5 | 1 hét |
| 1 | 1.2 Database & Domain | code-fix | 4 | 1 hét |
| 1 | 1.3 Test Infrastructure | test-unit | 10 | 1 hét vége |
| 2 | 2.1 Core Base & Config | code-refactor | 22 | 1 hét |
| 2 | 2.2 Logger & Events | code-refactor | 18 | 1 hét |
| 2 | 2.3 DB & System & Utils | code-refactor | 32 | 1 hét |
| 3 | 3.1 Processors | code-refactor | 25 | 1 hét |
| 3 | 3.2 Data Storage & Ingestion | code-refactor | 20 | 1 hét |
| 4 | 4.1 Collectors | code-refactor | 12 | 1 hét |
| 4 | 4.2 UI Layer | code-refactor | 30 | 1 hét |
| 5 | 5.1 Test Files | test-unit | 150+ | 1 hét eleje |
| 5 | 5.2 Scripts | code-refactor | 18 | 1 hét vége |
| 6 | 6.1 WARNING Coverage | test-unit | 31 | 1 hét |
| 6 | 6.2 Stub & Docs | docs-api | 3 | 1 hét eleje |
| 6 | 6.3 Final QA Gate | qa | 367 | 1 hét vége |

---

**Verzió**: 1.0
**Utolsó frissítés**: 2026-03-30
**Következő felülvizsgálat**: Minden milestone befejezése után
