# MQL5 Expert Advisor - Történelmi Adatgyűjtés Bővítmény Implementáció

**Dátum:** 2025-12-16
**Verzió:** 1.0.0
**Fájl:** [`Neural_AI_Next_Multi.mq5`](src/Neural_AI_Next_Multi.mq5:1)
**Állapot:** ✅ Implementálva és lefordítva

---

## Áttekintés

Sikeresen implementáltuk a történelmi adatgyűjtési funkciókat a meglévő MQL5 Expert Advisor-ba. A bővítmény lehetővé teszi a Python backend számára, hogy történelmi adatokat kérjen az MT5 szerverről, amelyeket az EA kötegekben gyűjt és továbbít vissza.

---

## Implementált Funkcionalitások

### 1. Új Bemeneti Paraméterek

A következő bemeneti paraméterek lettek hozzáadva az EA-hoz:

```mql
// Történelmi adatgyűjtés beállítások
input bool Enable_Historical_Collection = true;    // Történelmi adatgyűjtés engedélyezése
input int Max_Historical_Batch_Days = 365;         // Maximális napok per köteg
input int Historical_Request_Timeout = 300;        // Timeout másodpercben
input bool Log_Historical_Requests = true;         // Történelmi kérések naplózása
```

### 2. Globális Változók és Struktúrák

```mql
// Történelmi adatgyűjtés
bool historicalJobActive = false;
string currentJobId = "";
datetime currentJobStartTime;
int currentBatchNumber = 0;
int totalBatches = 0;

// Történelmi kérés követés
struct HistoricalRequest {
    string job_id;
    string symbol;
    int timeframe;
    datetime start_date;
    datetime end_date;
    int batch_size_days;
    string status;  // "pending", "in_progress", "completed", "failed"
};

HistoricalRequest activeRequest;
```

### 3. JSON Feldolgozó Helper Funkciók

- **`ExtractJsonString()`** - Sztring értékek kinyerése JSON-ből
- **`ExtractJsonInteger()`** - Egész szám értékek kinyerése JSON-ből
- **`StringToTime()`** - Dátum sztring konvertálása (YYYY-MM-DD formátum)

### 4. Történelmi Adatgyűjtési Funkciók

#### `HandleHistoricalRequest()`
- Fogadja és validálja a történelmi adatkéréseket
- Feldolgozza a JSON kéréseket
- Beállítja a kérés paramétereit

#### `CollectAndSendHistoricalBatch()`
- Lekéri a történelmi adatokat az MT5 szerverről
- Kötegekben küldi az adatokat a Python backendnek
- Használja a `CopyRates()` függvényt az adatlekéréshez
- Kezeli a sikertelen lekéréseket

#### `ReportProgress()`
- Jelenti a folyamat állapotát a szervernek
- Küldi a haladási százalékot és köteg információkat

#### `CheckForHistoricalRequests()`
- Periodikusan ellenőrzi az új történelmi kéréseket
- Polling mechanizmus a szerverrel való kommunikációhoz

#### `HandleHistoricalError()`
- Hibák kezelése és jelentése
- Állapot visszaállítása hiba esetén

#### `GetOptimalBatchSize()`
- Optimális kötegméret meghatározása az időkeret alapján
- Nagyfrekvenciás időkeretekhez kisebb kötegek

---

## Módosított Funkciók

### `OnInit()`
- Hozzáadva történelmi adatgyűjtés konfigurációjának kiírása
- Magyar nyelvű üzenetek

### `OnTimer()`
- Hozzáadva történelmi kérések ellenőrzése (10 percenként)
- Hozzáadva történelmi adatgyűjtés feldolgozása

---

## API Kommunikáció

### Végpontok

1. **Történelmi kérés fogadása**
   - `GET /api/v1/historical/poll` - Új kérések lekérdezése

2. **Adatküldés**
   - `POST /api/v1/historical/collect` - Történelmi adatok küldése

3. **Folyamat jelentés**
   - `POST /api/v1/historical/progress` - Haladás jelentése

4. **Hibajelentés**
   - `POST /api/v1/historical/error` - Hibák jelentése

### JSON Formátumok

#### Kérés fogadása (szervertől)
```json
{
  "job_id": "job_20251216_001",
  "symbol": "EURUSD",
  "timeframe": "M1",
  "start_date": "2000-01-01",
  "end_date": "2025-12-31",
  "batch_size_days": 365
}
```

#### Adatküldés (szervernek)
```json
{
  "job_id": "job_20251216_001",
  "batch_number": 1,
  "symbol": "EURUSD",
  "timeframe": 1,
  "date_range": {
    "start": "2000-01-01 00:00:00",
    "end": "2000-12-31 23:59:59"
  },
  "bars": [
    {
      "time": 946684800,
      "open": 1.01000,
      "high": 1.01200,
      "low": 1.00900,
      "close": 1.01150,
      "volume": 1000
    }
  ]
}
```

#### Folyamat jelentés
```json
{
  "job_id": "job_20251216_001",
  "status": "in_progress",
  "progress": {
    "completed_batches": 10,
    "total_batches": 26,
    "percentage": 38
  },
  "current_batch": {
    "batch_number": 11,
    "date_range": "2010-01-01 to 2010-12-31"
  }
}
```

---

## Kompatibilitás

### Meglévő Funkcionalitások
✅ **Megtartva** - Valós idejű tick adatgyűjtés
✅ **Megtartva** - Periodikus OHLCV adatgyűjtés
✅ **Megtartva** - Több instrumentum támogatás
✅ **Megtartva** - Több időkeret támogatás
✅ **Megtartva** - HTTP kommunikáció

### Új Funkcionalitások
✅ **Hozzáadva** - Történelmi adatkérés kezelése
✅ **Hozzáadva** - Történelmi adatok gyűjtése kötegekben
✅ **Hozzáadva** - Progress jelentés
✅ **Hozzáadva** - Hibakezelés és helyreállítás
✅ **Hozzáadva** - Konfigurálható kötegméret

---

## Fordítási Eredmény

```
==========================================
MQL5 Compilation Script for Linux
==========================================
✓ Wine found
✓ Wine prefix found: /home/elynea/.mt5
✓ MetaEditor found

Compiling: neural_ai/experts/mt5/src/Neural_AI_Next_Multi.mq5
  ✓ Compilation successful
  ✓ Output file created: Neural_AI_Next_Multi.ex5
  ✓ Copied to: neural_ai/experts/mt5/compiled/
==========================================
✓ Compilation and copy successful
==========================================
```

**Fájlok helye:**
- Forráskód: [`src/Neural_AI_Next_Multi.mq5`](src/Neural_AI_Next_Multi.mq5:1)
- Fordított EA: [`compiled/Neural_AI_Next_Multi.ex5`](compiled/Neural_AI_Next_Multi.ex5:1)

---

## Használati Utasítás

### 1. EA Telepítése

1. Nyisd meg az MT5-öt
2. Navigátor → Expert Advisors
3. Keress rá a "Neural_AI_Next_Multi" EA-ra
4. Húzd a chartra

### 2. Konfiguráció

**Alapvető beállítások:**
- `FastAPI_Server`: `http://localhost:8000`
- `Update_Interval`: `60` (másodperc)
- `Enable_Historical_Collection`: `true`

**Történelmi adatgyűjtés:**
- `Max_Historical_Batch_Days`: `365` (nap per köteg)
- `Historical_Request_Timeout`: `300` (másodperc)
- `Log_Historical_Requests`: `true`

### 3. Tesztelés

1. Indítsd el az EA-t egy charton
2. Ellenőrizd a naplóban a kapcsolódási státuszt
3. Küldj egy történelmi adatkérést a Python backendről
4. Figyeld a folyamatot a naplókban

---

## Hibakeresés

### Gyakori Hibák

1. **Kapcsolódási hiba**
   - Ellenőrizd a FastAPI szerver állapotát
   - Ellenőrizd a hálózati kapcsolatot

2. **Adatlekérési hiba**
   - Ellenőrizd az MT5 történelmi adatbázisát
   - Ellenőrizd a dátumtartomány érvényességét

3. **Timeout hiba**
   - Növeld a `Historical_Request_Timeout` értékét
   - Csökkentsd a `Max_Historical_Batch_Days` értékét

### Naplózás

Engedélyezd a részletes naplózást:
- `Enable_HTTP_Logs = true`
- `Log_Historical_Requests = true`

---

## Teljesítmény Optimalizálás

### Kötegméret beállítások

**Nagyfrekvenciás időkeretek (M1, M5):**
```mql
Max_Historical_Batch_Days = 30;  // 1 hónap
```

**Közepes időkeretek (M15, H1):**
```mql
Max_Historical_Batch_Days = 90;  // 3 hónap
```

**Alacsony frekvenciás időkeretek (H4, D1):**
```mql
Max_Historical_Batch_Days = 365; // 1 év
```

---

## Biztonsági Megfontolások

1. **Timeout beállítások** - Állíts be megfelelő timeout értékeket
2. **Hibakezelés** - Minden hiba le van kezelve és jelentve van
3. **Memória menedzsment** - Kötegekben történő adatgyűjtés
4. **Kapcsolat ellenőrzés** - Periodikus kapcsolat tesztelés

---

## Jövőbeli Fejlesztések

1. **WebSocket támogatás** - Valós idejű kérés kezelés
2. **Több job egyidejű kezelése** - Párhuzamos adatgyűjtés
3. **Automatikus újrapróbálkozás** - Exponenciális backoff
4. **Adattömörítés** - Nagyobb adatmennyiségek hatékonyabb küldése

---

## Dokumentáció Hivatkozások

- [Tervezési Specifikáció](../../../plans/mql5_ea_historikus_bovites_spec.md:1)
- [API Dokumentáció](../../../docs/components/collectors/mt5/api.md:1)
- [MQL5 Fordítási Útmutató](../../../docs/MQL5_COMPILATION_GUIDE.md:1)

---

## Verzió Történet

- **v1.0.0** (2025-12-16): Kezdeti implementáció
  - Történelmi adatkérés kezelés
  - Köteges adatgyűjtés
  - Progress jelentés
  - Hibakezelés

---

**Implementálta:** Roo (AI Architect)
**Utolsó frissítés:** 2025-12-16
**Állapot:** ✅ Kész és tesztelésre kész
