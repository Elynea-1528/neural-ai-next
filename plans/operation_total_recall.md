# 🎯 Terv: OPERATION TOTAL RECALL

## 📌 Célkitűzés
A rendszer megfigyelhetőségének (Observability) és stabilitásának helyreállítása a DDD refaktor után. A fókusz a "néma" rendszer felélesztésén és a szigorú típusbiztonságon van.

## 🛠️ Kritikus Akciópontok (Minden Modulra)
1.  **LoggerFactory Audit**: Minden fájlban `self._logger = LoggerFactory.get_logger(__name__)` használata.
2.  **Structlog Irtás**: Közvetlen `structlog` importok törlése.
3.  **Trace Dekorátorok**: `@trace` dekorátor elhelyezése minden kritikus üzleti logikát végző metóduson.
4.  **TypedDict Konfiguráció**: `factory.py` fájlokban TypedDict definiálása és szigorú castolás (`cast(TypedDict, raw_cfg)`).
5.  **Static QA**: Ruff és MyPy hibák (piros) teljes körű javítása.

## 🗓️ Ütemezés

### 1. Fázis: Infrastructure Réteg (`neural_ai/core`)
- [ ] `core/utils`: HardwareInfo és Decorators audit.
- [ ] `core/config`: Dynamic és Yaml Config Manager audit.
- [ ] `core/logger`: LoggerFactory és implementációk audit.
- [ ] `core/events`: ZeroMQ busz audit.
- [ ] `core/db`: SQLAlchemy async engine audit.

### 2. Fázis: Persistence Réteg (`neural_ai/data`)
- [ ] `data/storage`: Parquet és File storage audit.
- [ ] `data/ingestion`: MarketDataPersister audit.

### 3. Fázis: Domain Réteg (`neural_ai/processors`)
- [ ] `processors/pipeline`: Teljes pipeline orchestrator audit.
- [ ] `processors/dimensions`: D1-D15 dimenziók auditja.

### 4. Fázis: Input Réteg (`neural_ai/collectors`)
- [ ] `collectors/jforex`: Bi5Downloader és LiveFeed audit.

## 🛡️ Biztonsági Protokoll
- **TESZTEK FUTTATÁSA TILOS!** A rendszer instabil, a `pytest` és `python main.py` parancsok használata felfüggesztve a stabilitás helyreállításáig.
- Kizárólag statikus kódanalízis és manuális kód audit végezhető.

## 📊 Követés
Minden modul auditálása után a `docs/development/TASK_TREE.md` frissítése kötelező.
