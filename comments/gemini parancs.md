  

## 🚦 RENDSZER STÁTUSZ JELENTÉS (SITREP)

A rendszer egy "Hard Reset" és refaktorálás után áll. A komponensek állapota vegyes:

### 1. HISTORICAL MODE (Batch) - ✅ KÉSZ
*   **Script:** `scripts/download_history.py` (Direct Storage Mode).
*   **Ingestion:** `Bi5Downloader` (20 bájtos support, helyes időszámítás).
*   **Storage:** `ParquetStorage` (Append-only, `data/tick/SYMBOL` struktúra).

### 2. LIVE MODE (Stream) - ✅ STABIL
*   **Bridge:** Java (`NeuralBridgeStrategy`) + Python (`JForexLiveFeed`).
*   **Pipeline:** EventBus ➔ MarketDataPersister ➔ Storage.

### 3. PROCESSING - 🚧 AKTÍV ZÓNA
*   **Resampler:** ✅ KÉSZ (Mid/Bid OHLC, Spread, Real Volume).
*   **D1 (Price):** ✅ KÉSZ (Z-Score, Log Return, Timeframe Config).
*   **D2 (Support):** ⚠️ **KRITIKUS.** A kód létezik, de a validáció és a config szinkronizáció kérdéses.

---

## ⚡ A TE ELSŐ FELADATOD: "DEEP AUDIT & MASTER PLAN"

Ne írj javító kódot! Először térképezd fel a terepet.

**LÉPÉS 1: HYGIENE (Takarítás)**
Utasíts a `cache` fájlok (`__pycache__`, `.pytest_cache`, `.mypy_cache`, `ruff_cache`) és a `logs/` tartalmának törlésére, hogy tiszta lappal induljunk.

**LÉPÉS 2: DEEP CODE AUDIT (Rétegenként)**
Elemezd a csatolt teljes kódbázist az alábbi sorrendben:
1.  **CORE & COLLECTORS & DATA:** (Az alapok). Stimmelnek az importok? A `pyproject.toml` függőségek? A Config struktúra?
2.  **UI & PROCESSORS:** (A felépítmény). A D1/D2 implementáció megfelel az `overview.md`-nek? A UI (`Strategy Lab`) helyesen hívja a Service-t?

**LÉPÉS 3: MASTER TASK TREE LÉTREHOZÁSA**
A kimeneted egy Markdown táblázat vagy lista legyen, ami **FÁJL SZINTŰ** pontossággal mutatja az állapotot:
*   Melyik fájl felel meg az SSOT-nak? (✅)
*   Hol van eltérés vagy hiba? (❌)
*   Hol hiányzik teszt? (⚠️)

**Indítsd az elemzést! Kezdj a takarítási paranccsal, majd a Core réteg átvilágításával!**