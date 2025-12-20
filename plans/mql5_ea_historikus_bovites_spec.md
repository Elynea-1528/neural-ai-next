# MQL5 Expert Advisor - Történelmi Adat Bővítmény Specifikáció

**Dátum:** 2025-12-16
**Verzió:** 1.0.0
**Cél EA:** [`Neural_AI_Next_Multi.mq5`](neural_ai/experts/mt5/src/Neural_AI_Next_Multi.mq5:1)

---

## Fordítás állapota

✅ **Teljes dokumentum lefordítva**
✅ **Minden szakasz magyar nyelven**
✅ **Markdown formázás megtartva**
✅ **Kódpéldák angolul maradtak**
⚠️ **Implementáció állapota: Tervezési fázis**

---

## Áttekintés

Ez a dokumentum meghatározza a meglévő MQL5 Expert Advisor történelmi adatgyűjtés támogatásához szükséges módosításait. Az EA a következőkre lesz bővítve:

1. Történelmi adatkérések fogadása a Python FastAPI szervertől
2. Történelmi adatok lekérése az MT5ből konfigurálható kötegekben
3. Történelmi adatok visszaküldése a szervernek
4. Folyamat követés és jelentés hosszú futású műveletekhez

---

## Jelenlegi EA architektúra

### Meglévő funkcionalitás
- ✅ Valós idejű tick adatgyűjtés (OnTick esemény)
- ✅ Periodikus OHLCV adatgyűjtés (OnTimer esemény, 60s intervallum)
- ✅ Több instrumentum támogatás (4 instrumentum)
- ✅ Több időkeret támogatás (6 időkeret)
- ✅ HTTP kommunikáció FastAPI szerverrel

### Jelenlegi adatfolyam
```
OnTick → CollectAndSendTickData → HTTP POST /api/v1/collect/tick
OnTimer → CollectAndSendOHLCVData → HTTP POST /api/v1/collect/ohlcv
```

---

## Javasolt bővítmények

### 1. Új bemeneti paraméterek

Add hozzá ezeket a bemeneti paramétereket az EAhöz:

```mql
// Történelmi adatgyűjtés beállítások
input bool Enable_Historical_Collection = true;    // Történelmi adatgyűjtés engedélyezése
input int Max_Historical_Batch_Days = 365;         // Maximális napok per köteg
input int Historical_Request_Timeout = 300;        // Timeout másodpercben
input bool Log_Historical_Requests = true;         // Történelmi kérések naplózása
```

### 2. Új globális változók

Add hozzá ezeket a globális változókat:

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

### 3. Új funkciók

#### 3.1 Történelmi kérés kezelő

```mql
//+------------------------------------------------------------------+
//| Történelmi adatkérés kezelése a szervertől                        |
//+------------------------------------------------------------------+
bool HandleHistoricalRequest(const string &json_request) {
    // JSON kérés feldolgozása
    // Várt formátum:
    // {
    //   "job_id": "job_12345",
    //   "symbol": "EURUSD",
    //   "timeframe": "M1",
    //   "start_date": "2000-01-01",
    //   "end_date": "2025-12-31",
    //   "batch_size_days": 365
    // }

    if (Log_Historical_Requests) {
        Print("Történelmi adatkérés fogadva: ", json_request);
    }

    // JSON feldolgozás (egyszerűsítve - élesben használj megfelelő JSON parsert)
    string job_id = ExtractJsonString(json_request, "job_id");
    string symbol = ExtractJsonString(json_request, "symbol");
    string timeframe_str = ExtractJsonString(json_request, "timeframe");
    string start_date_str = ExtractJsonString(json_request, "start_date");
    string end_date_str = ExtractJsonString(json_request, "end_date");
    string batch_size_str = ExtractJsonString(json_request, "batch_size_days");

    // Bemenetek validálása
    if (job_id == "" || symbol == "" || timeframe_str == "" ||
        start_date_str == "" || end_date_str == "") {
        Print("Hiba: Érvénytelen történelmi kérés paraméterek");
        return false;
    }

    // Időkeret sztring konvertálása enumra
    int timeframe = StringToTimeframe(timeframe_str);
    if (timeframe == PERIOD_CURRENT) {
        Print("Hiba: Érvénytelen időkeret: ", timeframe_str);
        return false;
    }

    // Dátumok konvertálása
    datetime start_date = StringToTime(start_date_str);
    datetime end_date = StringToTime(end_date_str);

    if (start_date == 0 || end_date == 0 || start_date >= end_date) {
        Print("Hiba: Érvénytelen dátumtartomány");
        return false;
    }

    // Kötegméret kiszámítása
    int batch_size_days = (int)StringToInteger(batch_size_str);
    if (batch_size_days <= 0) {
        batch_size_days = Max_Historical_Batch_Days;
    }

    // Kérés tárolása
    activeRequest.job_id = job_id;
    activeRequest.symbol = symbol;
    activeRequest.timeframe = timeframe;
    activeRequest.start_date = start_date;
    activeRequest.end_date = end_date;
    activeRequest.batch_size_days = batch_size_days;
    activeRequest.status = "pending";

    // Összes köteg kiszámítása
    int total_days = (int)((end_date - start_date) / 86400);
    totalBatches = (int)MathCeil((double)total_days / batch_size_days);

    if (Log_Historical_Requests) {
        Print("Történelmi kérés validálva:");
        Print("  Job ID: ", job_id);
        Print("  Szimbólum: ", symbol);
        Print("  Időkeret: ", TimeframeToString(timeframe));
        Print("  Dátumtartomány: ", TimeToString(start_date), " to ", TimeToString(end_date));
        Print("  Kötegméret: ", batch_size_days, " nap");
        Print("  Összes köteg: ", totalBatches);
    }

    return true;
}
```

#### 3.2 Történelmi adatgyűjtés

```mql
//+------------------------------------------------------------------+
//| Történelmi adatok gyűjtése és küldése kötegben                    |
//+------------------------------------------------------------------+
bool CollectAndSendHistoricalBatch() {
    if (activeRequest.status != "in_progress" && activeRequest.status != "pending") {
        return false;
    }

    if (activeRequest.status == "pending") {
        activeRequest.status = "in_progress";
        currentJobId = activeRequest.job_id;
        currentJobStartTime = TimeCurrent();
        currentBatchNumber = 0;
    }

    // Köteg dátumtartomány kiszámítása
    datetime batch_start = activeRequest.start_date + (currentBatchNumber * activeRequest.batch_size_days * 86400);
    datetime batch_end = MathMin(batch_start + (activeRequest.batch_size_days * 86400), activeRequest.end_date);

    if (batch_start >= activeRequest.end_date) {
        // Minden köteg befejezve
        activeRequest.status = "completed";
        historicalJobActive = false;

        if (Log_Historical_Requests) {
            Print("Történelmi adatgyűjtés befejezve jobhoz: ", currentJobId);
        }

        return true;
    }

    // Történelmi adatok lekérése
    MqlRates rates[];
    int bars_count = CopyRates(
        activeRequest.symbol,
        (ENUM_TIMEFRAMES)activeRequest.timeframe,
        batch_start,
        batch_end,
        rates
    );

    if (bars_count <= 0) {
        Print("Figyelmeztetés: Nem található adat a(z) ", currentBatchNumber + 1, ". kötethez",
              " (", TimeToString(batch_start), " to ", TimeToString(batch_end), ")");

        // Továbbra is növeljük a kötegszámot és folytatjuk
        currentBatchNumber++;
        return true;
    }

    if (Log_Historical_Requests) {
        Print("Lekérve ", bars_count, " bar a(z) ", currentBatchNumber + 1, ". kötethez",
              " (", TimeToString(batch_start), " to ", TimeToString(batch_end), ")");
    }

    // JSON adatok előkészítése
    string json_data = "{";
    json_data += "\"job_id\":\"" + currentJobId + "\",";
    json_data += "\"batch_number\":" + IntegerToString(currentBatchNumber) + ",";
    json_data += "\"symbol\":\"" + activeRequest.symbol + "\",";
    json_data += "\"timeframe\":" + IntegerToString(activeRequest.timeframe) + ",";
    json_data += "\"date_range\":{";
    json_data += "\"start\":\"" + TimeToString(batch_start, TIME_DATE | TIME_MINUTES | TIME_SECONDS) + "\",";
    json_data += "\"end\":\"" + TimeToString(batch_end, TIME_DATE | TIME_MINUTES | TIME_SECONDS) + "\"";
    json_data += "},";
    json_data += "\"bars\":[";

    // Barok adatok hozzáadása
    for (int i = 0; i < bars_count; i++) {
        if (i > 0) json_data += ",";
        json_data += "{";
        json_data += "\"time\":" + IntegerToString((int)rates[i].time) + ",";
        json_data += "\"open\":" + DoubleToString(rates[i].open, (int)SymbolInfoInteger(activeRequest.symbol, SYMBOL_DIGITS)) + ",";
        json_data += "\"high\":" + DoubleToString(rates[i].high, (int)SymbolInfoInteger(activeRequest.symbol, SYMBOL_DIGITS)) + ",";
        json_data += "\"low\":" + DoubleToString(rates[i].low, (int)SymbolInfoInteger(activeRequest.symbol, SYMBOL_DIGITS)) + ",";
        json_data += "\"close\":" + DoubleToString(rates[i].close, (int)SymbolInfoInteger(activeRequest.symbol, SYMBOL_DIGITS)) + ",";
        json_data += "\"volume\":" + IntegerToString((int)rates[i].tick_volume);
        json_data += "}";
    }

    json_data += "]}";

    // HTTP POST kérés küldése
    string url = FastAPI_Server + "/api/v1/historical/collect";
    string headers = "Content-Type: application/json\r\n";

    char post[];
    char result[];
    string result_headers;
    int response_code;

    StringToCharArray(json_data, post, 0, StringLen(json_data));

    int res = WebRequest("POST", url, headers, Historical_Request_Timeout, post, result, result_headers);

    if (res == 200) {
        string response = CharArrayToString(result);

        if (Log_Historical_Requests) {
            Print("Köteg ", currentBatchNumber + 1, " sikeresen elküldve: ", bars_count, " bar");
        }

        currentBatchNumber++;

        // Folyamat jelentése
        ReportProgress();

        return true;
    } else {
        Print("Hiba a(z) ", currentBatchNumber + 1, ". köteg küldésénél: HTTP ", res);

        if (res > 0) {
            string response = CharArrayToString(result);
            Print("Válasz: ", response);
        }

        return false;
    }
}
```

#### 3.3 Folyamat jelentés

```mql
//+------------------------------------------------------------------+
//| Folyamat jelentése a szervernek                                   |
//+------------------------------------------------------------------+
void ReportProgress() {
    if (currentJobId == "") return;

    int progress_percentage = (int)((double)currentBatchNumber / totalBatches * 100);

    string json_data = "{";
    json_data += "\"job_id\":\"" + currentJobId + "\",";
    json_data += "\"status\":\"in_progress\",";
    json_data += "\"progress\":{";
    json_data += "\"completed_batches\":" + IntegerToString(currentBatchNumber) + ",";
    json_data += "\"total_batches\":" + IntegerToString(totalBatches) + ",";
    json_data += "\"percentage\":" + IntegerToString(progress_percentage);
    json_data += "},";
    json_data += "\"current_batch\":{";
    json_data += "\"batch_number\":" + IntegerToString(currentBatchNumber) + ",";
    json_data += "\"date_range\":\"" + TimeToString(activeRequest.start_date) + " to " + TimeToString(activeRequest.end_date) + "\"";
    json_data += "}";
    json_data += "}";

    string url = FastAPI_Server + "/api/v1/historical/progress";
    string headers = "Content-Type: application/json\r\n";

    char post[];
    char result[];
    string result_headers;
    int response_code;

    StringToCharArray(json_data, post, 0, StringLen(json_data));

    int res = WebRequest("POST", url, headers, 10, post, result, result_headers);

    if (res == 200 && Log_Historical_Requests) {
        Print("Folyamat jelentve: ", progress_percentage, "% (", currentBatchNumber, "/", totalBatches, ")");
    }
}
```

#### 3.4 JSON helper funkciók

```mql
//+------------------------------------------------------------------+
//| Sztring érték kinyerése JSONből                                   |
//+------------------------------------------------------------------+
string ExtractJsonString(const string &json, const string &key) {
    string search_pattern = "\"" + key + "\":\"";
    int start_pos = StringFind(json, search_pattern);

    if (start_pos == -1) return "";

    start_pos += StringLen(search_pattern);
    int end_pos = StringFind(json, "\"", start_pos);

    if (end_pos == -1) return "";

    return StringSubstr(json, start_pos, end_pos - start_pos);
}

//+------------------------------------------------------------------+
//| Egész szám érték kinyerése JSONből                                |
//+------------------------------------------------------------------+
long ExtractJsonInteger(const string &json, const string &key) {
    string search_pattern = "\"" + key + "\":";
    int start_pos = StringFind(json, search_pattern);

    if (start_pos == -1) return 0;

    start_pos += StringLen(search_pattern);

    // Szám végének megtalálása (vessző, zárójel, vagy kapcsos zárójel)
    int end_pos = start_pos;
    while (end_pos < StringLen(json)) {
        string ch = StringSubstr(json, end_pos, 1);
        if (ch == "," || ch == "}" || ch == "]") break;
        end_pos++;
    }

    string value_str = StringSubstr(json, start_pos, end_pos - start_pos);
    StringTrimLeft(value_str);
    StringTrimRight(value_str);

    return StringToInteger(value_str);
}
```

### 4. Módosított OnInit funkció

```mql
//+------------------------------------------------------------------+
//| Expert inicializálási funkció                                     |
//+------------------------------------------------------------------+
int OnInit() {
    //--- Instrumentumok feldolgozása
    ParseInstruments();

    //--- Időkeretek feldolgozása
    ParseTimeframes();

    //--- időzítő létrehozása
    EventSetTimer(Update_Interval);

    //--- Kapcsolat tesztelése FastAPI szerverrel
    if (TestConnection()) {
        isConnected = true;
        Print("✓ Csatlakozva a FastAPI szerverhez: ", FastAPI_Server);
        Print("✓ Figyelés ", totalInstruments, " instrumentum");
        Print("✓ Figyelés ", totalTimeframes, " időkeret");

        if (Enable_Historical_Collection) {
            Print("✓ Történelmi adatgyűjtés: ENGEDÉLYEZVE");
            Print("✓ Max kötegméret: ", Max_Historical_Batch_Days, " nap");
        } else {
            Print("⚠ Történelmi adatgyűjtés: LETILTVA");
        }
    } else {
        Print("⚠ Figyelmeztetés: Nem sikerült csatlakozni a FastAPI szerverhez");
        Print("  Szerver: ", FastAPI_Server);
        Print("  Az EA folytatja de az adatgyűjtés sikertelen lehet");
    }

    //---
    return (INIT_SUCCEEDED);
}
```

### 5. Új időzítő kezelő

Add hozzá az OnTimer funkcióhoz:

```mql
//+------------------------------------------------------------------+
//| Időzítő funkció                                                   |
//+------------------------------------------------------------------+
void OnTimer() {
    //--- OHLCV adatok gyűjtése és küldése minden instrumentumra és időkeretre
    CollectAndSendOHLCVData();

    //--- Történelmi adatgyűjtés feldolgozása ha aktív
    if (Enable_Historical_Collection && historicalJobActive) {
        CollectAndSendHistoricalBatch();
    }
}
```

### 6. Új HTTP kérés kezelő

Add hozzá egy mechanizmust a szervertől érkező kérések fogadására. Ez implementálható:

**A opció: Polling (Ajánlott)**
- Az EA periodikusan ellenőrzi az új kéréseket a szervertől
- Egyszerű implementáció, meglévő infrastruktúrával működik

**B opció: WebSocket (Haladó)**
- Kétirányú kommunikáció
- Valós idejű kérés kezelés
- Bonyolultabb implementáció

**Polling implementáció:**

```mql
//+------------------------------------------------------------------+
//| Történelmi adatkérések ellenőrzése                                |
//+------------------------------------------------------------------+
void CheckForHistoricalRequests() {
    if (!Enable_Historical_Collection) return;

    string url = FastAPI_Server + "/api/v1/historical/poll";
    string headers;
    char post[];
    char result[];
    string result_headers;
    int response_code;

    int res = WebRequest("GET", url, headers, 10, post, result, result_headers);

    if (res == 200) {
        string response = CharArrayToString(result);

        if (response != "" && response != "{}") {
            // Új kérés fogadva
            if (HandleHistoricalRequest(response)) {
                historicalJobActive = true;
                Print("Új történelmi adat job indult: ", activeRequest.job_id);
            }
        }
    }
}
```

Add hozzá az OnTimerhez:

```mql
void OnTimer() {
    //--- OHLCV adatok gyűjtése és küldése
    CollectAndSendOHLCVData();

    //--- Történelmi kérések ellenőrzése (minden 10 másodpercben)
    static int request_check_counter = 0;
    request_check_counter++;
    if (request_check_counter >= 10) {  // 10 * 60s = 10 perc
        CheckForHistoricalRequests();
        request_check_counter = 0;
    }

    //--- Történelmi adatgyűjtés feldolgozása ha aktív
    if (Enable_Historical_Collection && historicalJobActive) {
        CollectAndSendHistoricalBatch();
    }
}
```

---

## Hibakezelés

### Hiba forgatókönyvek

1. **Kapcsolat vesztés**
   - Újrapróbálkozási logika exponenciális backoffel
   - Folytatás az utolsó sikeres kötegtől

2. **Érvénytelen adatok**
   - Problematikus barok kihagyása
   - Figyelmeztetések naplózása
   - Folytatás a következő köteggel

3. **MT5 API hibák**
   - Rátelimítés kezelése
   - Újrapróbálkozás kisebb kötegekkel
   - Hibák jelentése a szervernek

### Hiba helyreállítás

```mql
//+------------------------------------------------------------------+
//| Történelmi gyűjtési hiba kezelése                                 |
//+------------------------------------------------------------------+
void HandleHistoricalError(const string &error_message) {
    Print("Történelmi gyűjtési hiba: ", error_message);

    // Hiba jelentése a szervernek
    string json_data = "{";
    json_data += "\"job_id\":\"" + currentJobId + "\",";
    json_data += "\"status\":\"error\",";
    json_data += "\"error\":\"" + error_message + "\",";
    json_data += "\"batch_number\":" + IntegerToString(currentBatchNumber);
    json_data += "}";

    string url = FastAPI_Server + "/api/v1/historical/error";
    string headers = "Content-Type: application/json\r\n";

    char post[];
    char result[];
    string result_headers;
    int response_code;

    StringToCharArray(json_data, post, 0, StringLen(json_data));

    WebRequest("POST", url, headers, 10, post, result, result_headers);

    // Állapot visszaállítása
    historicalJobActive = false;
    currentJobId = "";
    activeRequest.status = "failed";
}
```

---

## Teljesítmény optimalizálás

### Kötegméret hangolás

- **Alapértelmezett:** 365 nap per köteg
- **Beállítás alapján:**
  - Időkeret (M1 kisebb kötegeket igényel mint D1)
  - Elérhető memória
  - Hálózati sebesség
  - MT5 API korlátok

### Memória menedzsment

```mql
//+------------------------------------------------------------------+
//| Optimális kötegméret az időkeret alapján                          |
//+------------------------------------------------------------------+
int GetOptimalBatchSize(int timeframe) {
    int base_batch_days = Max_Historical_Batch_Days;

    // Beállítás nagyfrekvenciás időkeretekhez
    if (timeframe <= PERIOD_M1) {
        return MathMin(base_batch_days, 30);  // 1 hónap max M1hez
    } else if (timeframe <= PERIOD_M5) {
        return MathMin(base_batch_days, 90);  // 3 hónap max M5höz
    } else if (timeframe <= PERIOD_M15) {
        return MathMin(base_batch_days, 180); // 6 hónap max M15höz
    } else {
        return base_batch_days;  // Teljes köteg magasabb időkeretekhez
    }
}
```

---

## Tesztelési stratégia

### Egység tesztek

1. **JSON feldolgozás**
   - Teszteld az ExtractJsonString különböző bemenetekkel
   - Teszteld az ExtractJsonInteger különböző bemenetekkel

2. **Dátum számítások**
   - Teszteld a köteg dátumtartomány számításokat
   - Teszteld a perem eseteket (szökőév, hónap határok)

3. **Adat lekérés**
   - Teszteld a CopyRates különböző dátumtartományokkal
   - Teszteld a hibakezelést érvénytelen paraméterekkel

### Integrációs tesztek

1. **End-to-End teszt**
   - Kérj 1 hónap EURUSD M1 adatot
   - Ellenőrizd minden köteg sikeresen elküldve
   - Ellenőrizd az adatminőséget és teljességet

2. **Hiba helyreállítási teszt**
   - Szimuláld a kapcsolat vesztést
   - Ellenőrizd a folytatási képességet
   - Ellenőrizd a hibajelentést

3. **Teljesítmény teszt**
   - Kérj 1 év adatot
   - Mérj gyűjtési időt
   - Monitorozd a memória használatot

---

## Telepítési ellenőrzőlista

- [ ] EA forráskód frissítése új funkciókkal
- [ ] Új bemeneti paraméterek hozzáadása
- [ ] JSON feldolgozás tesztelése minta kérésekkel
- [ ] Történelmi adatlekérés tesztelése kis kötegekkel
- [ ] Hibakezelés és helyreállítás tesztelése
- [ ] Folyamat jelentés tesztelése
- [ ] Kötegek optimalizálása különböző időkeretekhez
- [ ] EA dokumentáció frissítése
- [ ] Teszt környezetbe telepítés
- [ ] Teljes integrációs teszt futtatása
- [ ] Termelésbe telepítés

---

## Konfigurációs példák

### 1. példa: Szabványos konfiguráció

```mql
// Történelmi adatgyűjtés beállítások
input bool Enable_Historical_Collection = true;
input int Max_Historical_Batch_Days = 365;
input int Historical_Request_Timeout = 300;
input bool Log_Historical_Requests = true;
```

### 2. példa: Nagyfrekvenciás konfiguráció

```mql
// Történelmi adatgyűjtés beállítások (M1hez optimalizálva)
input bool Enable_Historical_Collection = true;
input int Max_Historical_Batch_Days = 30;  // Kisebb kötegek M1hez
input int Historical_Request_Timeout = 600; // Hosszabb timeout
input bool Log_Historical_Requests = true;
```

### 3. példa: Konzervatív konfiguráció

```mql
// Történelmi adatgyűjtés beállítások (korlátozott erőforrások)
input bool Enable_Historical_Collection = true;
input int Max_Historical_Batch_Days = 90;  // Kis kötegek
input int Historical_Request_Timeout = 180; // Rövidebb timeout
input bool Log_Historical_Requests = false; // Naplózás csökkentése
```

---

## API kommunikációs példák

### Példa kérés a szervertől

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

### Példa folyamat jelentés az EAtól

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

### Példa adatköteg az EAtól

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
    // ... több bar
  ]
}
```

---

## Hibaelhárítási útmutató

### Gyakori problémák

1. **"Nem található adat" figyelmeztetések**
   - Ellenőrizd a dátumtartomány érvényességét
   - Ellenőrizd a szimbólum elérhetőségét MT5ben
   - Ellenőrizd az adatok létezését MT5 történeti központban

2. **Kapcsolat timeoutok**
   - Növeld a Historical_Request_Timeoutot
   - Csökkentsd a Max_Historical_Batch_Daysot
   - Ellenőrizd a hálózati kapcsolatot

3. **Memória problémák**
   - Csökkentsd a kötegméretet
   - Zárd be a többi chart/terminált
   - Indítsd újra az MT5öt periodikusan

4. **JSON feldolgozási hibák**
   - Ellenőrizd a JSON formátumot a szervertől
   - Ellenőrizd a speciális karaktereket az adatokban
   - Engedélyezd a részletes naplózást

---

## Verzió történet

- **v1.0.0** (2025-12-16): Kezdeti specifikáció

---

**Dokumentum verzió:** 1.0.0
**Utolsó frissítés:** 2025-12-16
**Szerző:** Roo (AI Architect)
**Állapot:** Kész implementációra
