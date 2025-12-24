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