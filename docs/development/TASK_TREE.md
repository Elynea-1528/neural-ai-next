# 🌳 NEURAL AI NEXT - TASK TREE v2.0

**Verzió:** 2.0 (DDD Refactor utáni állapot) | **Státusz:** 🟢 AKTÍV FEJLESZTÉS | **Frissítve:** 2026-01-29

---

## ⚠️ FONTOS MEGJEGYZÉS - STATISZTIKÁK MÉRÉSE SZÜKSÉGES

Ez a TASK_TREE architektúra és struktúra alapján készült. A pontos tesztelési lefedettség és teljesítmény metrikák **még nem lettek mérve**.

### 📊 MÉRT METRIKÁK (Utolsó Mérés: 2026-01-29)

**Kódbázis Statisztikák:**
- ✅ **155 Python fájl** `neural_ai/`-ban
- ✅ **103 teszt fájl** `tests/`-ban
- ✅ **1576 összesen teszt** (pytest discovery)

**Tesztelési Eredmények (Modulonkénti):**
- ✅ **core/base**: 97% coverage | 242 passed, 2 failed
- ✅ **core/config**: 99% coverage | 267 passed, 0 failed
- ⚠️ **core/logger**: coverage mérve | 99 passed, 8 failed
- ✅ **core/events+db+system+utils**: mérve | 376 passed, 3 failed, 3 skipped
- ⚠️ **collectors/jforex**: mérve | 54 passed, 4 failed
- 🔴 **data**: részben mérve | 113 passed, 39 failed, 56 errors
- ⏳ **processors**: részben mérve (SIGKILL memória limit)
- ⏳ **ui**: nincs tesztelve (Streamlit komponensek)

**Összesített Teszt Státusz:**
- **~1150+ passed** tesztből ~1576-ból
- **~73% teszt sikerességi arány** (coverage mérés során)
- **Kritikus problémák**:
  - `data/storage/implementations/file_storage.py` - 56 error
  - `core/logger/implementations/default_logger.py` - 8 failed
  - Memory limit issues teljes pytest run során

### 📋 TODO - További Mérések

- [x] **Pytest Coverage Futtatás**: Modulonkénti mérések elvégezve
- [x] **Fájlszámolás**: 155 .py fájl neural_ai/-ban
- [x] **Teszt fájlok száma**: 103 .py fájl tests/-ban
- [ ] **Teljes Coverage HTML Report**: `pytest --cov=neural_ai --cov-report=html` (memória probléma)
- [ ] **Branch Coverage**: `pytest --cov-branch` rétegenkénti mérések
- [ ] **Kódbázis Lines of Code**: `find neural_ai -name "*.py" -exec wc -l {} +`
- [ ] **Komplexitás Mérés**: McCabe complexity per modul
- [ ] **TODO/FIXME Audit**: `grep -r "TODO\|FIXME" neural_ai/`
- [ ] **Type Coverage**: mypy strict mode futtatás

---

## 📊 PROJEKT ÁTTEKINTÉS

### Architektúra Alapinformációk
- **Tervezési Minta:** Domain-Driven Design (DDD)
- **Rétegek Száma:** 5 (Infrastructure → Input → Persistence → Domain → Presentation)
- **Elsődleges Adatformat:** Partitioned Parquet (fastparquet)
- **Kommunikáció:** ZeroMQ Pub/Sub EventBus
- **Type Checking:** Strict (Pylance + Ruff)

---

## 🏛️ RENDSZERARCHITEKTÚRA (DDD 5-RÉTEG)

| # | Réteg | Mappa | Felelősség | Implementált | Tesztek Vannak |
|---|-------|-------|------------|--------------|----------------|
| 1 | **Infrastructure** | `neural_ai/core/` | Config, Logger, Events, DB, System | ✅ Igen | ✅ Igen |
| 2 | **Input** | `neural_ai/collectors/` | JForex, MT5 adatgyűjtés | 🟡 Részleges | ✅ Igen |
| 3 | **Persistence** | `neural_ai/data/` | Storage, Ingestion, Parquet IO | ✅ Igen | ✅ Igen |
| 4 | **Domain** | `neural_ai/processors/` | Dimenziók, Resampler, Pipeline | 🟡 Fejlesztés | ✅ Igen |
| 5 | **Presentation** | `neural_ai/ui/` | Streamlit Dashboard, Services | ✅ Igen | ✅ Igen |

---

## 📂 RÉSZLETES MODULÁLLAPOT (Fájl Szint)

### 🔧 INFRASTRUCTURE LAYER (`neural_ai/core/`)

#### core/base/ - DI Container & Patterns
| Fájl | Létezik | Teszt Van | Megjegyzés |
|------|---------|-----------|-----------|
| `factory.py` | ✅ | ✅ | Bootstrap sorrend kritikus |
| `implementations/di_container.py` | ✅ | ✅ | Singleton pattern |
| `implementations/component_bundle.py` | ✅ | ✅ | CoreComponents wrapper |
| `implementations/lazy_loader.py` | ✅ | ✅ | Circular imports megoldás |
| `implementations/singleton.py` | ✅ | ✅ | Meta osztály |
| `interfaces/container_interface.py` | ✅ | ✅ | ABC |
| `interfaces/component_interface.py` | ✅ | ✅ | ABC |
| `exceptions/base_error.py` | ✅ | ✅ | ComponentNotFoundError |

---

#### core/config/ - Konfiguráció Kezelés
| Fájl | Létezik | Teszt Van | Megjegyzés |
|------|---------|-----------|-----------|
| `factory.py` | ✅ | ✅ | TypedDict cast példa |
| `implementations/yaml_config_manager.py` | ✅ | ✅ | YAML + .env hybrid |
| `implementations/dynamic_config_manager.py` | ✅ | ✅ | SQL runtime config |
| `interfaces/config_interface.py` | ✅ | ✅ | ABC |
| `interfaces/async_config_interface.py` | ✅ | ✅ | Async ABC |
| `interfaces/factory_interface.py` | ✅ | ✅ | Factory ABC |
| `interfaces/types.py` | ✅ | ✅ | TypedDict sémák |
| `exceptions/config_error.py` | ✅ | ✅ | ConfigError |

---

#### core/logger/ - Strukturált Naplózás
| Fájl | Létezik | Teszt Van | Megjegyzés |
|------|---------|-----------|-----------|
| `factory.py` | ✅ | ✅ | Multi-logger factory |
| `implementations/default_logger.py` | ✅ | ✅ | Structlog wrapper |
| `implementations/colored_logger.py` | ✅ | ✅ | Console színezés |
| `implementations/rotating_file_logger.py` | ✅ | ✅ | File rotation |
| `formatters/logger_formatters.py` | ✅ | ✅ | JSON formatters |
| `interfaces/logger_interface.py` | ✅ | ✅ | ABC |
| `interfaces/factory_interface.py` | ✅ | ✅ | Factory ABC |
| `exceptions/logger_error.py` | ✅ | ✅ | LoggerError |

---

#### core/events/ - ZeroMQ EventBus
| Fájl | Létezik | Teszt Van | Megjegyzés |
|------|---------|-----------|-----------|
| `factory.py` | ✅ | ✅ | Lazy load ZMQ |
| `implementations/zeromq_bus.py` | ✅ | ✅ | Pub/Sub + async loop |
| `interfaces/event_bus_interface.py` | ✅ | ✅ | ABC |
| `interfaces/event_models.py` | ✅ | ✅ | Event TypedDict |
| `exceptions/event_error.py` | ✅ | ✅ | EventError |

---

#### core/db/ - SQLAlchemy Async
| Fájl | Létezik | Teszt Van | Megjegyzés |
|------|---------|-----------|-----------|
| `factory.py` | ✅ | ✅ | Async engine |
| `implementations/sqlalchemy_session.py` | ✅ | ✅ | DatabaseManager |
| `implementations/models.py` | ✅ | ✅ | ORM Models |
| `implementations/model_base.py` | ✅ | ✅ | Base class |
| `exceptions/db_error.py` | ✅ | ✅ | DBError |

---

#### core/system/ - Health Monitor
| Fájl | Létezik | Teszt Van | Megjegyzés |
|------|---------|-----------|-----------|
| `factory.py` | ✅ | ✅ | HealthMonitor factory |
| `implementations/health_monitor.py` | ✅ | ✅ | System metrics |
| `interfaces/health_interface.py` | ✅ | ✅ | ABC |
| `exceptions/health_error.py` | ✅ | ✅ | HealthError |

---

#### core/utils/ - Hardware & Decorators
| Fájl | Létezik | Teszt Van | Megjegyzés |
|------|---------|-----------|-----------|
| `factory.py` | ✅ | ✅ | HardwareInfo factory |
| `implementations/hardware_info.py` | ✅ | ✅ | AVX2/CUDA detektálás |
| `decorators.py` | ✅ | ✅ | @trace decorator |
| `interfaces/hardware_interface.py` | ✅ | ✅ | ABC |
| `exceptions/util_error.py` | ✅ | ✅ | UtilError |

---

### 📡 INPUT LAYER (`neural_ai/collectors/`)

#### collectors/jforex/ - Dukascopy Bridge
| Fájl | Létezik | Teszt Van | Megjegyzés |
|------|---------|-----------|-----------|
| `factory.py` | ✅ | ✅ | Downloader + LiveFeed factory |
| `implementations/bi5_downloader.py` | ✅ | ✅ | LZMA dekompresszió |
| `implementations/live_feed.py` | ✅ | ✅ | Java Bridge kommunikáció |
| `interfaces/downloader_interface.py` | ✅ | ✅ | ABC |
| `interfaces/live_interface.py` | ✅ | ✅ | ABC |
| `interfaces/tick_data.py` | ✅ | ✅ | TickData dataclass |
| `exceptions/jforex_error.py` | ✅ | ✅ | JForexError |

**⚠️ ISMERT PROBLÉMA**: `live_feed.py` Java Bridge integrációja KRITIKUS feladat!

---

### 💾 PERSISTENCE LAYER (`neural_ai/data/`)

#### data/storage/ - Parquet IO
| Fájl | Létezik | Teszt Van | Megjegyzés |
|------|---------|-----------|-----------|
| `factory.py` | ✅ | ✅ | Backend auto-select |
| `implementations/parquet_storage.py` | ✅ | ✅ | Partitioned Parquet |
| `implementations/file_storage.py` | ✅ | ✅ | Generic file ops |
| `backends/polars_backend.py` | ✅ | ✅ | AVX2 optimized |
| `backends/pandas_backend.py` | ✅ | ✅ | Fallback backend |
| `backends/base.py` | ✅ | ✅ | ABC |
| `interfaces/storage_interface.py` | ✅ | ✅ | ABC |
| `interfaces/factory_interface.py` | ✅ | ✅ | Factory ABC |

---

#### data/ingestion/ - Market Data Persister
| Fájl | Létezik | Teszt Van | Megjegyzés |
|------|---------|-----------|-----------|
| `market_data_persister.py` | ✅ | ✅ | Buffer + EventBus subscriber |

---

### 🧠 DOMAIN LAYER (`neural_ai/processors/`)

#### processors/resampler_service/ - Tick → OHLCV
| Fájl | Létezik | Teszt Van | Megjegyzés |
|------|---------|-----------|-----------|
| `factory.py` | ✅ | ✅ | Resampler factory |
| `implementations/resampler_service.py` | ✅ | ✅ | Polars time_alignment |
| `interfaces/resampler_interface.py` | ✅ | ✅ | ABC |
| `exceptions/resampler_error.py` | ✅ | ✅ | ResamplerError |

---

#### processors/dimensions/ - D1-D15 Processzorok
| Dimenzió | Fájl | Létezik | Teszt Van | Státusz |
|----------|------|---------|-----------|---------|
| **D01 - Price** | `d01_price/processor.py` | ✅ | ✅ | 🟢 Implementált |
| **D02 - Support** | `d02_support/implementations/support_processor.py` | ✅ | ✅ | 🟡 WIP |
| **D03-D15** | - | ❌ | ❌ | 🔴 PENDING |

**D01 Price**:
- Returns, Z-Score, Moving Averages implementálva

**D02 Support/Resistance**:
- Fractal detection implementálva, finomítás folyamatban

**D03-D15 (Tervezés alatt)**:
- 🔴 D03 - Trend Analysis (MACD, ADX)
- 🔴 D04 - Volatility (ATR, Bollinger)
- 🔴 D05 - Volume Profile
- 🔴 D06-D15 - Advanced features (specifikáció szükséges)

---

#### processors/implementations/ - Közös Szolgáltatások
| Fájl | Létezik | Teszt Van | Megjegyzés |
|------|---------|-----------|-----------|
| `time_alignment_service.py` | ✅ | ✅ | Cross-timeframe alignment |

---

### 🖥️ PRESENTATION LAYER (`neural_ai/ui/`)

#### ui/ - Streamlit Dashboard
| Fájl | Létezik | Teszt Van | Megjegyzés |
|------|---------|-----------|-----------|
| `app.py` | ✅ | ✅ | Main Streamlit entry |
| `core_bridge.py` | ✅ | ✅ | Core ↔ UI bridge |
| `factory.py` | ✅ | ✅ | UI services factory |

**ui/pages/ - Dashboard Oldalak:**
| Oldal | Fájl | Létezik | Funkció |
|-------|------|---------|---------|
| 🚀 Launchpad | `01_🚀_Launchpad.py` | ✅ | System overview |
| 🛠️ Dev Center | `02_🛠️_Dev_Center.py` | ✅ | Dev tools |
| 📥 Data Hub | `03_📥_Data_Hub.py` | ✅ | Data management |
| 🧠 AI Lab | `04_🧠_AI_Lab.py` | ✅ | Model training |
| 🪲 Strategy Lab | `05_🪲_Strategy_Lab.py` | ✅ | Backtesting |
| ⚡ Live Ops | `06_⚡_Live_Ops.py` | ✅ | Live monitoring |

**ui/services/ - Backend Logic:**
| Service | Fájl | Létezik | Teszt Van |
|---------|------|---------|-----------|
| Dashboard | `dashboard_service.py` | ✅ | ✅ |
| Data | `data_service.py` | ✅ | ✅ |
| Strategy | `strategy_service.py` | ✅ | ✅ |
| AI | `ai_service.py` | ✅ | ❌ |
| Navigation | `navigation_service.py` | ✅ | ❌ |
| Live Ops | `live_ops_service.py` | ✅ | ❌ |

---

## 🎯 GLOBÁLIS PRIORITÁSI MÁTRIX

### 🔴 KRITIKUS (1-3 nap) - BLOCKER
| # | Feladat | Modul | Indoklás | Állapot |
|---|---------|-------|----------|---------|
| 1 | **Java Bridge implementálás** | `collectors/jforex/live_feed.py` | Live mód nem működik nélküle | 🔴 PENDING |
| 2 | **LiveFeed → EventBus → Persister pipeline teszt** | Integration | End-to-end validáció hiányzik | 🔴 PENDING |
| 3 | **Coverage Report Generálás** | Teljes Projekt | Valós metrikák mérése | 🔴 **AZONNAL** |

### 🟡 MAGAS PRIORITÁS (3-7 nap)
| # | Feladat | Modul | Állapot |
|---|---------|-------|---------|
| 4 | D02 Support/Resistance lefedettség javítás | `processors/dimensions/d02_support/` | 🟡 WIP |
| 5 | Resampler multi-timeframe teszt | `processors/resampler_service/` | 🟡 WIP |
| 6 | UI Services hiányzó tesztek | `ui/services/ai_service.py, navigation_service.py, live_ops_service.py` | 🔴 PENDING |

### 🟢 KÖZEPES PRIORITÁS (1-2 hét)
| # | Feladat | Modul | Állapot |
|---|---------|-------|---------|
| 7 | D03-D05 dimenziók implementálás | `processors/dimensions/d03-d05/` | 🔴 PENDING |
| 8 | AI Lab model training UI | `ui/pages/04_🧠_AI_Lab.py` | 🟡 WIP |
| 9 | Storage backend benchmark | `data/storage/backends/` | 🔴 PENDING |
| 10 | Live Ops monitoring dashboard | `ui/pages/06_⚡_Live_Ops.py` | 🟡 WIP |

### 🔵 ALACSONY PRIORITÁS (>2 hét)
| # | Feladat | Modul | Állapot |
|---|---------|-------|---------|
| 11 | D06-D15 dimenziók specifikáció | `docs/planning/` | 🔴 PENDING |
| 12 | MT5 collector implementálás | `neural_ai/collectors/mt5/` | 🔴 PENDING |
| 13 | Dokumentáció auto-generálás CI/CD | `scripts/generate_docs.py` | 🔴 PENDING |

---

## 📈 TELJESÍTMÉNY METRIKÁK MÉRÉSE SZÜKSÉGES!

### ⚠️ TODO - Pytest Coverage Futtatás

Futtasd az alábbi parancsot a pontos coverage adatokért:

```bash
# Teljes coverage report HTML kimenettel
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest \
  --cov=neural_ai \
  --cov-report=html \
  --cov-report=term-missing \
  --cov-branch

# Rétegenkénti coverage
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest \
  --cov=neural_ai/core \
  --cov=neural_ai/collectors \
  --cov=neural_ai/data \
  --cov=neural_ai/processors \
  --cov=neural_ai/ui \
  --cov-report=term
```

### Kódbázis Statisztikák (Pontos Mérés Szükséges)
```bash
# Python fájlok száma
find neural_ai -name "*.py" | wc -l

# Teszt fájlok száma
find tests -name "*.py" | wc -l

# Teljes kód sorok
find neural_ai -name "*.py" -exec wc -l {} + | tail -1
```

### Rendszerállapot (Faktikus)
- ✅ **Build:** PASS (Ruff + Pylance strict mode)
- ✅ **Core Components:** MŰKÖDIK (Config, Logger, Events, DB, Storage)
- 🟡 **Data Pipeline:** RÉSZLEGES (Downloader OK, LiveFeed WIP)
- 🟡 **Processors:** RÉSZLEGES (D01 OK, D02 WIP, D03+ PENDING)
- ✅ **UI Dashboard:** MŰKÖDIK (Streamlit multipage)

---

## 🚀 KÖVETKEZŐ MILESTONE: "LIVE FEED ACTIVATION"

**Cél:** Működő live kereskedési mód (`python main.py live`)

**Kritikus Út:**
1. ✅ JForex bi5_downloader (KÉSZ)
2. 🔴 JForex live_feed + Java Bridge (BLOCKER!)
3. 🔴 LiveFeed → EventBus → Persister pipeline (INTEGRATION)
4. ✅ Resampler Tick → OHLCV (KÉSZ)
5. 🟡 D01-D02 processzorok (RÉSZLEGES)
6. 🟡 UI Live Ops Dashboard (WIP)

**Becsült idő:** TBD (Java Bridge függő)

**Sikerkritérium:**
- `python main.py live` elindul hiba nélkül
- JForex live tick adat érkezik EventBus-on
- MarketDataPersister Parquet-be menti a tickeket
- Resampler 1m OHLCV generál
- D01 processzor indikátorokat számol
- UI Live Ops Dashboard real-time mutatja az adatot

---

## 📝 COMMIT TÖRTÉNET & VÁLTOZÁSKÖVETÉS

**Követendő konvenció:**
```
feat(scope): [Magyar üzenet]
fix(scope): [Magyar üzenet]
refactor(scope): [Magyar üzenet]
docs(scope): [Magyar üzenet]
test(scope): [Magyar üzenet]
```

**Atomic Commit Szabály**: Minden fájlváltozás azonnali `git commit`-ot igényel!

---

## 🔗 KAPCSOLÓDÓ DOKUMENTÁCIÓ

- **Architektúra Szabványok:** [`docs/development/architecture_standards.md`](./architecture_standards.md)
- **AI Agent Utasítások:** [`docs/development/custom-instructions.md`](./custom-instructions.md)
- **Rendszer Specifikációk:** `docs/planning/specs/`
- **Modul Dokumentációk:** `docs/components/`
- **Agent Szabályok:** `.roo/rules-*/AGENTS.md`

---

**EMLÉKEZTETŐ:** Ez a TASK_TREE a projekt SSOT (Single Source of Truth) dokumentuma a struktúra tekintetében. **Valós coverage és teljesítmény adatokat pytest futtatás után kell hozzáadni!** 🌳
