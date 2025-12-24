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