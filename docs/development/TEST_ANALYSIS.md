# 🧪 NEURAL AI NEXT - TESZT ELEMZÉS ÉS JAVÍTÁSI TERV

**Verzió:** 1.0 | **Státusz:** 🔴 KRITIKUS PROBLÉMÁK | **Dátum:** 2026-01-29

---

## 📊 ÖSSZEFOGLALÓ METRIKÁK

### Kódbázis Méret
- **21,292 LOC** production kód (`neural_ai/`)
- **25,254 LOC** teszt kód (`tests/`)
- **155 Python fájl** neural_ai/-ban
- **103 teszt fájl** tests/-ban
- **Test/Code arány:** 1.19:1 (119% teszt coverage LOC-ban)

### Teszt Végrehajtási Eredmények
- **1576 teszt** összesen (pytest discovery)
- **~1150+ passed** (~73%)
- **~56 failed** (~3.5%)
- **~56 errors** (~3.5%)
- **~3 skipped** (<1%)
- **~311 nem futott** (20%, processors/UI részben nem mérve)

### Tech Debt Mutatók
- **2 TODO komment** összesen (D01, D02 processzorok)
- **0 FIXME** komment

---

## 🔴 KRITIKUS PROBLÉMÁK KATEGORIZÁLÁSA

### 1. DATA LAYER - 56 ERROR (🔴 BLOCKER)

**Érintett Modul:** `neural_ai/data/storage/implementations/file_storage.py`

**Probléma Típusa:**
- **56 ERROR** a `test_file_storage.py` tesztekben
- **Összes teszt ERROR státuszú**, nem FAILED (kivétel dobódik inicializáláskor)

**Valószínű Ok:**
```python
# tests/data/storage/implementations/test_file_storage.py
# Setup hibák a file_storage.py inicializálásakor
# Lehet:
# - Missing dependency (logger, config)
# - Initialization order probléma
# - Mock setup hiányzik
```

**Hatás:**
- FileStorage komponens **nem tesztelhető**
- ParquetStorage dependency erre → 33 további failed
- **BLOCKER a data persistence rétegre**

**Prioritás:** 🔴 **P0 - AZONNAL**

---

### 2. DATA STORAGE - 39 FAILED (🔴 KRITIKUS)

**Érintett Modulok:**
- `neural_ai/data/storage/backends/polars_backend.py` - 13 failed
- `neural_ai/data/storage/backends/base.py` - 6 failed
- `neural_ai/data/ingestion/market_data_persister.py` - 8 failed
- `neural_ai/data/storage/implementations/parquet_storage.py` - 27 failed

**Probléma Mintázatok:**

#### a) Polars Backend (13 failed)
```python
# Valószínű okok:
# - write/read metódusok signature változás
# - Polars API breaking change
# - Schema validation hibák
```

**Érintett tesztek:**
- `test_write_basic`, `test_write_with_compression`
- `test_read_basic`, `test_read_with_columns`, `test_read_chunked`
- `test_append_*` metódusok
- `test_validate_data`, `test_get_info`

#### b) Parquet Storage Service (27 failed)
```python
# Cascade failure FileStorage 56 error miatt
# ParquetStorage depends on FileStorage
# → FileStorage fix után újratesztelés szükséges
```

#### c) Market Data Persister (8 failed)
```python
# EventBus mock hibák
# DataFrame conversion failure (pandas/polars)
```

**Prioritás:** 🔴 **P1 - KRITIKUS** (FileStorage fix után)

---

### 3. CORE LOGGER - 8 FAILED (🟡 MAGAS)

**Érintett Modul:** `neural_ai/core/logger/implementations/default_logger.py`

**Probléma:**
- **Összes teszt failed** a `test_default_logger.py`-ban
- Initialization, debug, info, warning, error, critical log tesztek

**Valószínű Ok:**
```python
# Structlog konfiguráció vagy handler setup probléma
# Lehet:
# - Logger factory initialization issue
# - Handler duplicate check fails
# - Structlog processor chain configuration
```

**Hatás:**
- DefaultLogger használhatatlan tesztekben
- Production logger működik (main.py fut)
- **Nem blocker**, de quality gate problem

**Prioritás:** 🟡 **P2 - MAGAS**

---

### 4. CORE EVENTS - 26 FAILED (🟡 MAGAS)

**Érintett Modul:** `neural_ai/core/events/implementations/zeromq_bus.py`

**Probléma:**
- Async mock setup issues
- RuntimeWarning: coroutine never awaited
- Subscribe/publish error handling

**Valószínű Ok:**
```python
# ZeroMQ async context manager mock hibák
# Asyncio event loop setup tesztek során
```

**Hatás:**
- EventBus core funkcionalitás működik
- Edge case error handling nem tesztelt
- Live mode critical path érintett lehet

**Prioritás:** 🟡 **P2 - MAGAS**

---

### 5. CORE SYSTEM - 3 FAILED (🟢 KÖZEPES)

**Érintett Modul:** `neural_ai/core/system/factory.py`

**Probléma:**
- Health check integration tesztek
- Async coroutine mock warnings

**Prioritás:** 🟢 **P3 - KÖZEPES**

---

### 6. COLLECTORS JFOREX - 4 FAILED (🟢 KÖZEPES)

**Érintett Modul:** `neural_ai/collectors/jforex/factory.py`

**Probléma:**
- LiveFeed factory visszatérési típus ellenőrzés
- Config exception handling tesztek

**Prioritás:** 🟢 **P3 - KÖZEPES**

---

### 7. CORE BASE - 2 FAILED (🟢 ALACSONY)

**Érintett Modul:** `neural_ai/core/base/factory.py`

**Probléma:**
- `test_create_minimal_with_config_file` - Storage base_directory hiányzik
- Config validation tesztek

**Prioritás:** 🟢 **P4 - ALACSONY**

---

## 🎯 JAVÍTÁSI TERV - PRIORITÁS SZERINT

### 🔴 FÁZIS 1: BLOCKER FIX (1-2 nap)

#### 1.1 FileStorage 56 ERROR javítás
**Feladat:** `tests/data/storage/implementations/test_file_storage.py` ERROR státusz megszüntetése

**Lépések:**
1. Investigate `test_file_storage.py` setup methods
2. Identify missing dependency injection (logger, config, hardware)
3. Add proper mocks/fixtures
4. Ensure FileStorage can be instantiated in tests
5. Re-run `pytest tests/data/storage/implementations/test_file_storage.py -v`

**Sikerkritérium:** 0 ERROR, max 10 FAILED megengedett

**Felelős:** Code mode
**Becsült idő:** 4-6 óra

---

#### 1.2 Parquet Storage Cascade Fix
**Feladat:** FileStorage fix után ParquetStorage tesztek javítása

**Lépések:**
1. Re-run `pytest tests/data/storage/implementations/test_parquet_storage.py -v`
2. Fix remaining failures (várható: 5-10 failed)
3. Ensure write/read/append cycle works

**Sikerkritérium:** <5 FAILED

**Felelős:** Code mode
**Becsült idő:** 2-3 óra

---

### 🟡 FÁZIS 2: KRITIKUS FIX (2-3 nap)

#### 2.1 Polars Backend Fixes
**Feladat:** `test_polars_backend.py` 13 failed javítása

**Lépések:**
1. Check Polars API version compatibility
2. Update write/read method signatures
3. Fix schema validation logic
4. Re-run `pytest tests/data/storage/backends/test_polars_backend.py -v`

**Sikerkritérium:** 0 FAILED

**Becsült idő:** 3-4 óra

---

#### 2.2 DefaultLogger Initialization Fix
**Feladat:** `test_default_logger.py` 8 failed javítása

**Lépések:**
1. Debug structlog configuration
2. Fix logger factory initialization
3. Ensure no duplicate handlers
4. Re-run `pytest tests/core/logger/implementations/test_default_logger.py -v`

**Sikerkritérium:** 0 FAILED

**Becsült idő:** 2-3 óra

---

#### 2.3 Market Data Persister Fixes
**Feladat:** `test_market_data_persister.py` 8 failed javítása

**Lépések:**
1. Fix EventBus mock setup
2. Fix DataFrame conversion (pandas/polars)
3. Ensure buffer flush works
4. Re-run `pytest tests/data/ingestion/test_market_data_persister.py -v`

**Sikerkritérium:** 0 FAILED

**Becsült idő:** 2-3 óra

---

### 🟢 FÁZIS 3: KÖZEPES PRIORITÁS (3-5 nap)

#### 3.1 ZeroMQ EventBus Async Fixes
**Feladat:** `test_zeromq_bus.py` 26 failed javítása

**Lépések:**
1. Fix async mock setup (coroutine warnings)
2. Ensure proper asyncio event loop in tests
3. Fix subscribe/publish error handling tests

**Sikerkritérium:** <3 FAILED

**Becsült idő:** 4-6 óra

---

#### 3.2 JForex Factory & System Health
**Feladat:** 4 JForex + 3 System factory failures

**Sikerkritérium:** 0 FAILED

**Becsült idő:** 2-3 óra

---

### 🔵 FÁZIS 4: ALACSONY PRIORITÁS (1 hét)

#### 4.1 Core Base Factory Config
**Feladat:** 2 config validation failures

**Sikerkritérium:** 0 FAILED

**Becsült idő:** 1-2 óra

---

## 📈 COVERAGE HIÁNYOSSÁGOK

### Nem Tesztelt Modulok

#### UI Réteg (0% coverage)
- `neural_ai/ui/services/ai_service.py` - ❌ Nincs teszt
- `neural_ai/ui/services/navigation_service.py` - ❌ Nincs teszt
- `neural_ai/ui/services/live_ops_service.py` - ❌ Nincs teszt
- `neural_ai/ui/pages/*.py` - ❌ Streamlit komponensek (manuális teszt)

**Indoklás:** Streamlit UI manuális/integrációs teszt igényel

**Javaslat:** 
- Playwright/Selenium end-to-end tesztek később
- UI services unit tesztek **KÖTELEZŐ** (P2 prioritás)

---

#### Processors Réteg (részben mérve)
- `neural_ai/processors/dimensions/d03-d15/` - ❌ Még nem implementált
- `neural_ai/processors/test_time_alignment_service.py` - 7 failed (SIGKILL miatt nem teljes)

**Javaslat:**
- Time alignment service tesztek külön futtatása memória limit nélkül
- D03-D05 implementálás előtt teszt specifikáció

---

## 🚀 MILESTONE ROADMAP

### M1: FileStorage Blocker Fix (1-2 nap)
- [x] 56 ERROR → 0 ERROR
- [ ] FileStorage unit tesztek működnek
- [ ] ParquetStorage cascade fix

**Exit Criteria:** `pytest tests/data/storage/ -v` <10 FAILED

---

### M2: Data Layer Stability (3-5 nap)
- [ ] Polars backend 0 FAILED
- [ ] Market Data Persister 0 FAILED
- [ ] DefaultLogger 0 FAILED

**Exit Criteria:** `pytest tests/data/ tests/core/logger/ -v` 0 FAILED

---

### M3: EventBus & Factory Cleanup (5-7 nap)
- [ ] ZeroMQ async tesztek <3 FAILED
- [ ] JForex factory 0 FAILED
- [ ] System health 0 FAILED

**Exit Criteria:** `pytest tests/core/events/ tests/collectors/ -v` <5 FAILED

---

### M4: 100% Core Coverage (7-10 nap)
- [ ] Minden core modul 0 FAILED
- [ ] UI services unit tesztek hozzáadása
- [ ] Time alignment service teljes teszt

**Exit Criteria:** `pytest tests/core/ -v` 0 FAILED, >95% coverage

---

## 📋 ACTION ITEMS

### Azonnali (P0)
- [ ] **FileStorage ERROR debug**: Test setup investigation
- [ ] **Mock dependency injection**: Logger, Config, Hardware
- [ ] **Re-run isolated**: `pytest tests/data/storage/implementations/test_file_storage.py::TestFileStorage::test_init_default_path -vv`

### 1-3 nap (P1)
- [ ] **Polars API audit**: Version compatibility check
- [ ] **ParquetStorage cascade fix**: After FileStorage resolved
- [ ] **Market Data Persister**: EventBus mock fix

### 3-7 nap (P2)
- [ ] **DefaultLogger structlog**: Configuration debug
- [ ] **ZeroMQ async**: Coroutine mock setup
- [ ] **UI services tests**: ai_service, navigation_service, live_ops_service

### 7-14 nap (P3-P4)
- [ ] **Time alignment service**: Full test run (avoid SIGKILL)
- [ ] **JForex factory**: Interface return type fixes
- [ ] **Core base config**: Validation edge cases

---

## 🔗 KAPCSOLÓDÓ DOKUMENTÁCIÓ

- **TASK_TREE:** [`docs/development/TASK_TREE.md`](./TASK_TREE.md) - Projekt struktúra
- **Architecture Standards:** [`docs/development/architecture_standards.md`](./architecture_standards.md)
- **Custom Instructions:** [`docs/development/custom-instructions.md`](./custom-instructions.md)

---

## 📝 CHANGELOG

### 2026-01-29 - Első kiadás
- Teszt eredmények összesítése (1576 teszt, 73% passed)
- Problémák kategorizálása 7 fő területre
- Prioritás szerinti javítási terv (P0-P4)
- 4 fázis milestone roadmap
- Action items konkrét lépésekkel

---

**KÖVETKEZŐ LÉPÉS:** FileStorage 56 ERROR debug → Code módra váltás szükséges
