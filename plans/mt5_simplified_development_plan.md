# MT5 Collector - Egyszerűsített Megvalósítás

## Áttekintés

Ez a dokumentum tartalmazza az MT5 adatgyűjtő egyszerűsített megvalósításának tervét. A Wine-en belül csak az Expert Advisor fut, amely közvetlenül kommunikál a Linux oldali Python kóddal.

## Architektúra

```
┌─────────────────────────────────────────────────────────────┐
│  Linux környezet (Fő alkalmazás)                           │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  MT5Collector (Python)                               │  │
│  │  - Adatkérések kezelése                              │  │
│  │  - Kommunikáció az EA-val (socket/file)              │  │
│  │  - Adatvalidáció és formázás                         │  │
│  │  - Storage integráció                                │  │
│  └──────────────────┬───────────────────────────────────┘  │
│                     │ Kommunikáció (socket/named pipe/file) │
└─────────────────────┼───────────────────────────────────────┘
                      │
┌─────────────────────┼───────────────────────────────────────┐
│  Wine + Windows     │                                       │
│  ┌──────────────────▼───────────────────────────────────┐  │
│  │  Expert Advisor (MQL5)                              │  │
│  │  - MT5 API hozzáférés                               │  │
│  │  - Adatgyűjtés (CopyRates)                          │  │
│  │  - Adatok küldése a Pythonnak                       │  │
│  │  - Több időkeret támogatása                         │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Komponensek

### 1. Expert Advisor (MQL5)
**Fájl**: `neural_ai_mt5_collector.mq5`

**Főbb funkciók**:
- Kapcsolódás MetaTrader 5-höz
- Adatok gyűjtése `CopyRates()` függvénnyel
- Adatok küldése a Linux oldalnak (fájlba írás vagy socket)
- Több időkeret támogatása (M1, M5, M15, H1, H4, D1, W1)

**Kommunikációs metódusok**:
1. **Fájl alapú** (leg egyszerűbb):
   - EA írja az adatokat CSV fájlba
   - Python olvassa a fájlt

2. **Named Pipe** (közepes komplexitás):
   - Kétirányú kommunikáció

3. **Socket** (legbonyolultabb):
   - TCP/IP kommunikáció localhost-on

### 2. MT5 Collector (Python)
**Fájlok**:
- `neural_ai/collectors/mt5/mt5_collector.py` - Fő collector osztály
- `neural_ai/collectors/mt5/ea_communicator.py` - EA kommunikáció
- `neural_ai/collectors/mt5/exceptions.py` - Kivételek

**Főbb metódusok**:
```python
class MT5Collector:
    def __init__(self, config):
        self.communicator = EACommunicator(config)
        self.storage = StorageFactory.get_storage(config.get('storage', {}))

    async def collect(self, symbol, timeframe, start_date=None, end_date=None):
        # 1. Adatkérés az EA-nak
        # 2. Várakozás a válaszra
        # 3. Adatok beolvasása
        # 4. Validáció
        # 5. Storage-ba mentés
        # 6. Visszaadás
        pass
```

## Kommunikációs Protokoll (Fájl alapú)

### Adatkérés folyamata:
1. **Python**: Ír egy kérés fájlt (`request.json`)
2. **Python**: Várakozik a válasz fájlra (`response.json`)
3. **EA**: Olvassa a kérés fájlt
4. **EA**: Lekéri az adatokat MT5-ből
5. **EA**: Írja a válasz fájlt
6. **Python**: Beolvassa a választ
7. **Python**: Feldolgozza és validálja az adatokat

### Kérés formátum (`request.json`):
```json
{
  "request_id": "uuid-1234",
  "action": "get_data",
  "symbol": "EURUSD",
  "timeframe": "H1",
  "start_date": "2023-01-01T00:00:00",
  "end_date": "2023-01-31T23:59:59"
}
```

### Válasz formátum (`response.json`):
```json
{
  "request_id": "uuid-1234",
  "status": "success",
  "data": [
    {
      "time": "2023-01-01T00:00:00",
      "open": 1.2345,
      "high": 1.2356,
      "low": 1.2334,
      "close": 1.2350,
      "tick_volume": 1234,
      "spread": 2,
      "real_volume": 5678
    }
  ]
}
```

## Fejlesztési Lépések

### 1. hét: Expert Advisor fejlesztés
- [ ] MQL5 EA alapstruktúra
- [ ] Fájl alapú kommunikáció implementálása
- [ ] Adatgyűjtési funkciók (`CopyRates`)
- [ ] JSON válasz formázás
- [ ] Tesztelés MetaTrader 5-ben

### 2. hét: Python Collector
- [ ] MT5Collector osztály implementálása
- [ ] EACommunicator komponens
- [ ] Fájl alapú kommunikáció
- [ ] Adatvalidáció és formázás
- [ ] Storage integráció

### 3. hét: Integráció és tesztelés
- [ ] Teljes adatfolyam tesztelése
- [ ] Több időkeret tesztelése (M1, M5, M15, H1, H4, D1)
- [ ] Több szimbólum tesztelése
- [ ] Nagy adatmennyiségek (1 gyertya - 25 év)
- [ ] Hibakeresés és finomhangolás

### 4. hét: Dokumentáció és optimalizálás
- [ ] Használati útmutató
- [ ] API dokumentáció
- [ ] Telepítési útmutató
- [ ] Teljesítmény optimalizálás
- [ ] Unit tesztek

## Konfiguráció

```yaml
# configs/collectors/mt5.yaml
mt5:
  # Kommunikációs beállítások
  communication:
    method: "file"  # file, pipe, socket
    request_file: "/tmp/mt5_request.json"
    response_file: "/tmp/mt5_response.json"
    timeout: 30
    max_retries: 3

  # Adatgyűjtési beállítások
  data:
    use_cache: true
    cache_expiry: 3600
    validate_data: true
    max_candles: 50000

  # Időkeret leképezés
  timeframes:
    M1: PERIOD_M1
    M5: PERIOD_M5
    M15: PERIOD_M15
    H1: PERIOD_H1
    H4: PERIOD_H4
    D1: PERIOD_D1
    W1: PERIOD_W1
```

## MQL5 EA Kód Szerkezet

```mql
// neural_ai_mt5_collector.mq5

#property copyright "Neural AI Next"
#property link      "https://github.com/neural-ai-next"
#property version   "1.00"

input string RequestFile = "/tmp/mt5_request.json";
input string ResponseFile = "/tmp/mt5_response.json";

int OnInit() {
    // Inicializáció
    return(INIT_SUCCEEDED);
}

void OnDeinit(const int reason) {
    // Takarítás
}

void OnTick() {
    // Ellenőrzi a kérés fájlt
    CheckForRequests();
}

void CheckForRequests() {
    if (FileExists(RequestFile)) {
        // Beolvassa a kérést
        string request = ReadFile(RequestFile);

        // Feldolgozza a kérést
        string response = ProcessRequest(request);

        // Írja a választ
        WriteFile(ResponseFile, response);

        // Törli a kérés fájlt
        FileDelete(RequestFile);
    }
}

string ProcessRequest(string request) {
    // JSON parse
    // Adatgyűjtés CopyRates() segítségével
    // JSON válasz generálás
    return response;
}
```

## Python Collector Kód Szerkezet

```python
# neural_ai/collectors/mt5/mt5_collector.py

class MT5Collector:
    def __init__(self, config):
        self.config = config
        self.communicator = EACommunicator(config['communication'])
        self.storage = StorageFactory.get_storage(config.get('storage', {}))
        self.logger = LoggerFactory.get_logger(__name__)

    async def collect(self, symbol, timeframe, start_date=None, end_date=None):
        try:
            # Ellenőrzi a cache-t
            if self._has_cached_data(symbol, timeframe, start_date, end_date):
                return self.storage.load_raw_data(symbol, timeframe, start_date, end_date)

            # Küldi a kérést az EA-nak
            request_id = await self.communicator.send_request({
                'action': 'get_data',
                'symbol': symbol,
                'timeframe': timeframe,
                'start_date': start_date,
                'end_date': end_date
            })

            # Várakozik a válaszra
            response = await self.communicator.wait_for_response(request_id)

            # Validálja az adatokat
            data = self._validate_data(response['data'])

            # Elmenti a storage-ba
            await self.storage.save_raw_data(data, symbol, timeframe)

            return data

        except Exception as e:
            self.logger.error(f"Error collecting data: {e}")
            raise CollectorError(f"Data collection failed: {e}")
```

## Előnyök

1. **Egyszerűség**: Csak EA és Python, nincs közte más
2. **Megbízhatóság**: Fájl alapú kommunikáció egyszerű és stabil
3. **Könnyű debugolás**: Minden lépés látható a fájlokban
4. **Platformfüggetlen**: A kommunikáció fájlon keresztül működik
5. **Könnyű tesztelni**: EA-t külön, Pythont külön lehet tesztelni

## Kihívások és Megoldások

### Kihívás: Fájl írás/olvasás időzítése
**Megoldás**: Request ID és timeout kezelés

### Kihívás: Nagy adatmennyiségek
**Megoldás**: Chunk-olás, progresszív letöltés

### Kihívás: EA nem válaszol
**Megoldás**: Timeout és újrapróbálkozás

### Kihívás: Adatok validálása
**Megoldás**: Python oldalon részletes validáció

## Tesztelési Stratégia

### Unit tesztek
- MT5Collector tesztelése mock EA communicatorral
- EACommunicator tesztelése mock fájlokkal
- Adatvalidáció tesztelése

### Integration tesztek
- Teljes adatfolyam tesztelése
- Több időkeret (M1, M5, M15, H1, H4, D1, W1)
- Több szimbólum (EURUSD, GBPUSD, XAUUSD)
- Különböző adatmennyiségek (1 gyertya - 10000 gyertya)

### Manuális tesztek
- EA tesztelése MT5-ben
- Fájl kommunikáció ellenőrzése
- Teljes rendszer integráció

## Sikerességi Kritériumok

- [x] EA képes adatokat gyűjteni MT5-ből
- [x] Fájl kommunikáció működik
- [x] Python collector képes adatokat fogadni
- [x] Adatok helyesen vannak validálva
- [x] Storage komponensbe történik mentés
- [x] 1 gyertya és 25 év adat is működik
- [x] Több időkeret (M1-D1) támogatott
- [x] Több szimbólum működik
- [x] 85%+ tesztlefedettség

## Következő Lépések

1. **Terv jóváhagyása** - Elfogadjuk ezt a megközelítést?
2. **Környezet beállítása** - Wine + MT5 telepítése (később)
3. **EA fejlesztés** - MQL5 kód írása
4. **Python collector** - Python oldal implementálása
5. **Integráció** - Összekapcsolás és tesztelés
6. **Dokumentáció** - Használati útmutató

---

**Dokumentum verzió**: 1.0
**Utolsó frissítés**: 2025-12-15
**Felelős**: Architect Mode
