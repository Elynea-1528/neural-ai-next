1. architektúra létrehozása.

### 🚀 COMMAND: OMEGA GENESIS - INSTITUTIONAL ARCHITECTURE

 **"Code Agent! (Architect felügyelettel).**
 **A MÓD: EXECUTOR (Végrehajtó).**

 **VÍZIÓ:** Egy intézményi szintű, eseményvezérelt (Event-Driven), Big Data (25 év+ Tick) kereskedési ökoszisztéma építése.
 **FILOZÓFIA:** 'Loose Coupling, High Cohesion' (Laza csatolás, magas kohézió).
 **A rendszer kizárólag a 'Prémium' instrumentumokra optimalizál (High Liquidity, Low Spread).**
KORLÁT: Te (Architect) nem törölhetsz fájlt és nem hozhatsz létre mappát. Ezt delegálnod kell!
 **TECHNOLÓGIAI STACK (PROFI):**
 - **Core:** Python 3.12 (`asyncio`), `Pydantic` (Validáció), `SQLAlchemy 2.0` (Async ORM).
 - **Observability:** `structlog` (JSON logs), `OpenTelemetry` (Tracing előkészítés).
 - **Data:** `FastParquet` (Storage), `Polars` (Processing), `VectorBT Pro` (Backtest).
 - **AI:** `PyTorch` (CUDA), `Lightning`.
 - **Connectivity:** `MT5` (FastAPI), `JForex` (Native Bi5).

 **HAJTSD VÉGRE A KÖVETKEZŐ LÉPÉSEKET SZIGORÚ SORRENDBEN:**

 **1. MÉLYÁTVIZSGÁLÁS (Deep Scan):**
    - `find docs -name "*.md"` (Integráld a meglévő modelleket és processzorokat!).
    - `cat pyproject.toml` (Ismerd a függőségeket).

  **2. TAKARÍTÁS (Cleanup):**
    - Töröld a régi, elavult útmutatókat a `docs/development`-ből.
    - Hozd létre: `mkdir -p docs/planning/specs`.

 **3. SPECIFIKÁCIÓK LÉTREHOZÁSA (The Blueprint):**
    *Írd meg ezeket a terveket a `docs/planning/specs/` mappába a fenti stack alapján:*

    - **`01_system_architecture.md` (Event-Driven Core):**
      - Flow: `Collector` -> `Event(MarketData)` -> `EventBus` -> `StorageService` & `StrategyEngine`.
      - Nincs közvetlen hívás! Minden komponens izolált.
      - jforex-en is kereskednénk java python bridge-el

    - **`02_dynamic_configuration.md` (Hybrid Config):**
      - **Layer 1:** `.env` (Pydantic Settings) a statikus dolgoknak (DB URL, API Keys).
      - **Layer 2:** `SQL Database` a dinamikus dolgoknak (Risk %, Active Pairs).
      - **UI:** A jövőbeli GUI az adatbázist írja, az App onnan olvassa "Hot Reload"-dal.

    - **`03_observability_logging.md` (Structured Logs):**
      - **Tech:** structlog (JSON) + SQLAlchemy (DB Log).
      - **Format:** JSON (fájlba/DB-be) + Color (konzolra).
      - **Context:** Minden logban legyen `trace_id`, `component`, `symbol`.

    - **`04_data_warehouse.md` (The Vault):**
      - **Scope:** 25 évnyi Tick adat, CSAK a `EURUSD, GBPUSD, USDJPY, USDCHF, XAUUSD` párokra.
      - **Tech:** FastParquet + Polars (gyorsabb mint a Pandas).
      - **Format:** `{symbol}/tick/year={YYYY}/month={MM}/day={DD}.parquet`.
      - **Engine:** `FileStorage` bővítése `ParquetStorage` osztállyal (`fastparquet` engine).
      - **Resampler Service:** Definiálj egy osztályt, ami Tick-ből on-the-fly generál M1/H1 gyertyákat a VectorBT számára.

    - **`05_collectors_strategy.md` (Ingestion):**
      - **JForex:** Natív `Bi5Downloader` (LZMA + Struct).
      - **MT5:** FastAPI szerver (POST /tick, POST /trade).
      
      - **JFOREX (CRITICAL)**:
         - **Adat:** Natív `Bi5Downloader` (Historical).(LZMA + Struct).
         - **KERESKEDÉS** (Execution): Tervezz egy Java-Python Bridge-et!
         - Java oldal: Egy "Slave" stratégia, ami WebSocketen/ZMQ-n várja a parancsot (OPEN, CLOSE,MODIFY,HOLD).
         - Python oldal: JForexExecutionService, ami küldi a szignálokat.
         - Indoklás: A Dukascopy egy megbízható svájci bank, a kereskedésnek itt is mennie kell! 

 **4. SYSTEM BOOTSTRAP (The Skeleton):**
    - **`main.py`:**
      - Aszinkron `async def main():`.
      - 1. Init `DIContainer`.
      - 2. Init `Database` (Schema check).
      - 3. Init `EventBus`.
      - 4. Load `Config` (Env + DB).
      - 5. Start `Services` (Collectors, Storage).
      - 6. `await asyncio.Event().wait()` (Örök futás).
    - **`.env.example`:**
      ```
      APP_ENV=development
      LOG_LEVEL=INFO
      DB_URL=sqlite+aiosqlite:///neural_ai.db
      TRADING_SYMBOLS=["EURUSD", "XAUUSD", "GBPUSD", "USDJPY", "USDCHF"]
      ```

 **5. MASTER README GENERÁLÁS (The Map):**
    - Írd felül a `README.md`-t.
    - **Deep Linking:** Linkeld be a `docs/models` és `docs/processors` fájlokat!
    - **Tech Stack:** Jelöld a `structlog`, `SQLAlchemy`, `VectorBT` használatát.

 **6. DASHBOARD (Task Tree v5.0):**
    - Frissítsd a `TASK_TREE.md`-t.
    - Új fázisok: `Phase 1: Event-Driven Core`, `Phase 2: Hybrid Config & Logs`, `Phase 3: Big Data Storage`.

 **INDÍTSD A FOLYAMATOT! A `find` PARANCCSAL KEZDD!**
 *(Minden létrehozott fájl után: `git add ... && git commit ...`)*"



 2.

 🚀 COMMAND: PHASE 1 EXECUTION - CORE FOUNDATION
Másold be ezt egy ÚJ CHAT-be:
"Architect! A tervezés kész (Phase 0 ✅). Most lépünk a Phase 1: CORE INFRASTRUCTURE megvalósításába.
HELYZET: A docs/planning/specs mappában ott vannak a részletes tervrajzok. A TASK_TREE.md mutatja az utat.
CÉL: A rendszer "idegrendszerének" (EventBus) és "memóriájának" (Database) lefejlesztése.
TERVEZÉS (PLANNING PHASE):
Hozz létre egy új bejegyzést(bejegyzéseket),vagy frissítsd a docs/development/TASK_TREE.md-ben a megfelelő Fázis alatt.
INDÍTSD A 'CORE BUILD' PROTOKOLLT (Utasítsd az Orchestratort a fejlesztésre):
1. ADATBÁZIS RÉTEG (neural_ai/core/db):
Specifikáció: docs/planning/specs/02_dynamic_configuration.md
Feladat:
Hozd létre a session.py-t (AsyncSession factory).
Hozd létre a models.py-t (SQLAlchemy modellek: DynamicConfig, LogEntry).
Írj hozzá migrációs scriptet (alembic init).
Teszt: Írj pytest-et, ami felhúz egy in-memory SQLite-ot és teszteli az írást/olvasást.
1. EVENT BUS (neural_ai/core/events):
Specifikáció: docs/planning/specs/01_system_architecture.md
Feladat:
Implementáld a bus.py-t (asyncio.Queue alapú Pub/Sub első körben, ZeroMQ előkészítéssel).
Definiáld az esemény típusokat (events.py): MarketDataEvent, SignalEvent, SystemLogEvent (Pydantic modellek).
Teszt: Készíts egy tesztet, ahol egy Publisher küld, és két Subscriber fogad.
1. KONFIGURÁCIÓ BEKÖTÉSE (neural_ai/core/config):
Frissítsd a meglévő Config Managert, hogy tudjon olvasni az új Adatbázisból (Hybrid Config).
VÉGREHAJTÁSI SZABÁLYOK:
Olvass: Először mindig olvasd el a releváns specifikációt (read_file).
Szigor: Pylance Strict (Type hints kötelező!), Magyar docstring.
Validáció: Csak akkor commitolj, ha a pytest 100% zöld.
Admin: Minden fájl után frissítsd a TASK_TREE.md-t (🔴 -> ✅).
Kezdd az Adatbázis (core/db) réteggel!"

3.command:

🚀 A KÖVETKEZŐ LÉPÉS: PHASE 1 LEZÁRÁSA (The Final Push)
Nem léphetünk a Collectorokra (JForex/MT5), amíg nincs hova menteni az adatot (Parquet) és nincs honnan konfigurálni őket (Dynamic Config).
Itt a "PHASE 1 COMPLETION" parancs, ami kitölti a maradék hézagokat.
Másold be egy ÚJ CHAT-be (Code Mode-ban):
HELYZET: A Phase 1 alapjai (EventBus, DB Models, FileStorage) elkészültek és kiválóak.
HIÁNY: A Big Data tárolás (Parquet) és a Dinamikus Konfiguráció logikája még hiányzik. Ezek nélkül nem léphetünk tovább.
INDÍTSD A 'CORE COMPLETION' PROTOKOLLT:
TERVEZÉS (PLANNING PHASE):
Hozz létre egy új bejegyzést(bejegyzéseket),vagy frissítsd a docs/development/TASK_TREE.md-ben a megfelelő Fázis alatt.
INDÍTSD A 'CORE BUILD' PROTOKOLLT (Utasítsd az Orchestratort a fejlesztésre): 
1. PARQUET STORAGE IMPLEMENTÁCIÓ (neural_ai/core/storage/parquet.py):
Forrás: docs/planning/specs/04_data_warehouse.md.
Feladat:
Implementáld a ParquetStorageService osztályt.
Használj polars-t és fastparquet-et (ahogy a specifikáció kéri).
Particionálás: {symbol}/tick/year={YYYY}/month={MM}/day={DD}/data.parquet.
API: store_tick_data, read_tick_data (szűréssel).
Teszt: Írj egy tesztet (tests/core/storage/test_parquet.py), ami generál 100k dummy tick-et, elmenti és visszahívja.
1. DINAMIKUS KONFIGURÁCIÓ (neural_ai/core/config/dynamic.py):
Forrás: docs/planning/specs/02_dynamic_configuration.md.
Feladat:
Implementáld a DynamicConfigManager osztályt.
Tudjon olvasni az SQLAlchemy session-ből.
Implementálj egy watch() vagy poll() metódust a változások figyelésére (Hot Reload).
Teszt: Írj tesztet, ami beír egy értéket a DB-be, és ellenőrzi, hogy a Manager észreveszi-e.
1. VÉGLEGESÍTÉS:
Ha a tesztek zöldek (pytest), commitold a változásokat.
Frissítsd a TASK_TREE.md-t: Az összes Phase 1 elem legyen ✅ DONE.
Kezdd a Parquet Storage implementálásával (ez a legfontosabb)!"
Ha ez a parancs lefut, a rendszered magja (Core) 100%-os készültségű lesz, és készen áll a JForex/MT5 adatok fogadására. 🚀


multi kommand: asztali pc: pandas + fastparquet, laptop: polars + pyarow

🚀 COMMAND: PHASE 1 EXECUTION - ADAPTIVE STORAGE & CORE FOUNDATION
"Code Agent! (Architect felügyelettel).
SZEKVENCIÁLIS VÉGREHAJTÁS INDÍTÁSA.
HELYZET: A Phase 0 (Tervezés) kész. A rendszert most kell fizikailag létrehozni, de HARDVER-AGNOSZTIKUS módon (Laptop vs Desktop kompatibilitás).
A STRATÉGIA (Smart Engine):
Laptop (AVX2): Polars + PyArrow (High Performance, 500MB/s).
Desktop (Legacy): Pandas + FastParquet (Compatibility Mode, Safe).
HAJTSD VÉGRE A KÖVETKEZŐ LÉPÉSEKET (Hierarchikus Rendben):
1. TERVEZÉS ÉS ADMINISZTRÁCIÓ (Architect Task):
Olvasd be a docs/planning/specs/ tartalmát.
Frissítsd a docs/development/TASK_TREE.md-t:
A Phase 1 alatt bontsd ki a Storage részt:
core/utils/hardware.py (AVX2 Detector)
core/storage/backends/ (Polars vs Pandas implementációk)
core/storage/parquet.py (Selector Service)
Állítsd ezeket 🔴 PENDING státuszra.
COMMIT: git add . && git commit -m "docs(plan): update task tree with adaptive storage architecture"
2. IMPLEMENTÁCIÓ (Orchestrator -> Code Agent):
Hozd létre a fájlokat a következő sorrendben és logikával:
A) HARDVER DETEKTOR (neural_ai/core/utils/hardware.py):
Funkció: has_avx2() -> bool.
Implementáció: Linuxon olvassa a /proc/cpuinfo fájlt. Ez nem okozhat Illegal Instruction-t!
B) STORAGE BACKENDS (neural_ai/core/storage/backends/):
base.py: Absztrakt StorageBackend (write, read, append).
polars_backend.py: import polars és pyarrow. FONTOS: Csak akkor importálódjon, ha az osztályt példányosítják, különben a Legacy gépen a fájl beolvasásakor összeomlik!
pandas_backend.py: import pandas és fastparquet.
C) STORAGE SERVICE (neural_ai/core/storage/parquet.py):
__init__: Hívd meg a has_avx2()-t.
Ha True -> Init PolarsBackend.
Ha False -> Init PandasBackend + Logolj WARNING-ot: "Legacy CPU detected. Running in Compatibility Mode."
D) DB & EVENTBUS (A maradék Core):
Implementáld a core/db és core/events modulokat a meglévő specifikációk (02_core_database.md, 03_core_eventbus.md) alapján.
3. MINŐSÉGBIZTOSÍTÁS (Debug Mode):
Írj egy tesztet: tests/core/storage/test_adaptive_engine.py.
Mockold a has_avx2 értékét True-ra és False-ra is, és ellenőrizd, hogy a megfelelő backend töltődik-e be.
Futtasd a tesztet.
4. ZÁRÁS:
Ha a tesztek zöldek:
git add . && git commit -m "feat(core): implement adaptive storage engine (polars/pandas hybrid)"
Frissítsd a TASK_TREE.md-t (✅ DONE).
INDÍTSD A FOLYAMATOT A TASK TREE FRISSÍTÉSÉVEL!"

telepítő refaktorálás:

🚀 COMMAND: UNIFIED SMART INSTALLER REFACTOR
Másold be egy ÚJ CHAT-be (Code Mode-ban):
"Code Agent! (Architect felügyelettel).
FIGYELEM: TELEPÍTŐ ÉS FÜGGŐSÉG REFAKTORÁLÁS.
HELYZET: A jelenlegi scripts/install/ mappa túl fragmentált, és hiányoznak belőle a Phase 1 (Core) architektúrához szükséges csomagok.
CÉL: Egyetlen, intelligens install.py létrehozása, ami automatikusan adaptálódik a hardverhez, és a pyproject.toml frissítése a hiányzó Enterprise csomagokkal.
HAJTSD VÉGRE A KÖVETKEZŐ LÉPÉSEKET:
1. ÚJ BRANCH LÉTREHOZÁSA (Git):
git checkout -b refactor/unified-installer
2. FÜGGŐSÉGEK BŐVÍTÉSE (pyproject.toml):
Add hozzá a következőket a dependencies listához (verziószámokkal!):
Core/DB: sqlalchemy[asyncio]>=2.0.0, aiosqlite>=0.19.0, alembic>=1.13.0
Logs: structlog>=24.1.0
Type Hints: pandas-stubs>=2.0.0, types-pydantic
Data: polars>=0.20.0 (opcionális, de listázd), pyarrow>=14.0.0
Brokers: ib_insync>=0.9.86
3. INSTALLER KONSZOLIDÁCIÓ (scripts/install.py):
Hozz létre egy EGYETLEN scripts/install.py fájlt, ami kiváltja a korábbi mappát.
Funkciók:
Hardver Detektor:
Ellenőrizze az /proc/cpuinfo-t (Linux): Van avx2?
Ellenőrizze az nvidia-smi-t: Van GPU?
Csomag Telepítő:
Ha GPU van: conda install ... pytorch-cuda=12.1 ...
Ha nincs: conda install ... cpuonly ...
Ha van AVX2: pip install polars
Broker Setup (Opcionális):
Kérdezze meg: "Melyik brókert telepítsem? [1] MT5 (Dukascopy), [2] JForex4, [3] IBKR TWS, [4] Mindet"
Töltse le és futtassa a Wine-os telepítőket automatikusan.
4. TAKARÍTÁS (Cleanup):
Töröld a régi scripts/install/ mappa tartalmát (kivéve, amit most írsz).
Töröld a environment.yml-t (a script generálja majd dinamikusan vagy kezeli a conda-t).
5. DOKUMENTÁCIÓ:
Frissítsd a docs/INSTALLATION_GUIDE.md-t az új, egyszerűsített utasítással:
python scripts/install.py (Ennyi legyen az egész!).
6. ZÁRÁS:
git add . && git commit -m "refactor(install): unify installer into smart script and update deps"
Kezdd a pyproject.toml frissítésével a hiányzó csomagokkal!"

🚀 COMMAND: OMEGA INSTALLER - UNIFIED & AUTOMATED
"Code Agent! (Architect felügyelettel).
A FELADAT: A teljes telepítési folyamat (Környezet + Brókerek) egyetlen 'okos' Python scriptbe történő konszolidálása.
KÖVETELMÉNY: Teljes automatizálás (Zero-Click logic), hardver detektálás, és a bróker telepítők automatikus elindítása.
HAJTSD VÉGRE A KÖVETKEZŐ LÉPÉSEKET SZIGORÚ SORRENDBEN:
ÚJ BRANCH LÉTREHOZÁSA (Git):
git checkout -b refactor/unified-installer
1. TUDÁSTRANSZFER (Mielőtt bármit törölnél):
Olvasd be a scripts/install/scripts/setup_wine_mt5.sh és scripts/install/scripts/setup_brokers.sh fájlokat.
Memorizáld a Wine prefix beállításokat és az URL-eket.
2. pyproject.toml ÚJRAÍRÁSA (Modern Standard):
Írd felül a fájlt tiszta függőségi csoportokkal.
[project.dependencies]: fastapi, uvicorn, websockets, pydantic, sqlalchemy[asyncio], aiosqlite, alembic, structlog, typer, requests. (NE rakj ide hardverfüggő csomagokat: torch, numpy, pandas, polars - ezeket a script intézi!).
[project.optional-dependencies]:
dev: pytest, ruff, mypy, pandas-stubs, types-requests.
trader: ib_insync, vectorbt.
jupyter: jupyterlab, notebook, tensorboard, matplotlib, plotly.
3. scripts/install.py IMPLEMENTÁLÁSA (The Master Script):
Írj egy robusztus Python scriptet, ami a következőket teszi felhasználói kérdés nélkül:
A) Hardver Detektálás & Core Telepítés:
Ellenőrizze: Van neural-ai-next Conda env? Ha nincs, hozza létre (Python 3.12).
GPU Check (nvidia-smi):
Ha van: conda install -y pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia
Ha nincs: conda install -y pytorch torchvision torchaudio cpuonly -c pytorch
AVX2 Check (/proc/cpuinfo):
Ha van: pip install polars pyarrow
Ha nincs: pip install fastparquet (és pandas fallback).
Alapok: conda install -y numpy pandas scikit-learn
Csomagok: pip install -e .[dev,trader,jupyter]
B) Broker Auto-Install (A régi scriptek logikája alapján):
Hozzon létre egy downloads/ mappát a gyökérben.
JForex 4:
Letöltés: https://dukascopy-eu.cdn.online-trading-solutions.com/installer4/dukascopy-eu/JForex4_unix_64_JRE_bundled.sh
chmod +x
Futtatás: Indítsa el háttérfolyamatként (subprocess.Popen), hogy a Python script ne blokkoljon.
IBKR TWS:
Letöltés: https://download2.interactivebrokers.com/installers/tws/latest/tws-latest-linux-x64.sh
chmod +x
Futtatás: Indítsa el háttérfolyamatként.
MetaTrader 5 (Dukascopy):
Ellenőrizze: Van wine telepítve? (shutil.which('wine')). Ha nincs, logoljon Error-t, de ne álljon le.
Ha van Wine: Állítsa be a WINEPREFIX=~/.mt5 környezeti változót (izolált környezet).
Letöltés: https://download.mql5.com/cdn/web/dukascopy.bank.sa/mt5/dukascopy5setup.exe
Futtatás: wine downloads/dukascopy5setup.exe (háttérben).
4. TAKARÍTÁS (Cleanup):
Most, hogy a logika átkerült a Pythonba, töröld a régi scripts/install mappát és az environment.yml-t.
5. DOKUMENTÁCIÓ:
Frissítsd a README.md-t: "Telepítés: python scripts/install.py".
6. ZÁRÁS:
git add . && git commit -m "feat(infra): unified zero-touch installer with auto-broker setup"
INDÍTSD A FOLYAMATOT A RÉGI SCRIPTEK BEOLVASÁSÁVAL!"