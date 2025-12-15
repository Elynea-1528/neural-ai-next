# MT5 Collector - Wine + FastAPI + Expert Advisor Megoldás

## Áttekintés

Ez a dokumentum tartalmazza az MT5 adatgyűjtő alternatív megvalósításának tervét, amely Wine környezetben futó MetaTrader 5-höz kapcsolódik FastAPI-n keresztül egy Expert Advisor segítségével.

## Architektúra

```
┌─────────────────────────────────────────────────────────────┐
│  Linux környezet (Fő alkalmazás)                           │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  MT5Collector (Python)                               │  │
│  │  - Adatkérések kezelése                              │  │
│  │  - FastAPI kliens                                    │  │
│  │  - Adatvalidáció                                     │  │
│  │  - Storage integráció                                │  │
│  └──────────────────┬───────────────────────────────────┘  │
│                     │ FastAPI REST hívások                  │
└─────────────────────┼───────────────────────────────────────┘
                      │
┌─────────────────────┼───────────────────────────────────────┐
│  Wine + Windows     │                                       │
│  ┌──────────────────▼───────────────────────────────────┐  │
│  │  FastAPI Szerver (Python + MT5 pip csomag)          │  │
│  │  - /api/symbols                                      │  │
│  │  - /api/data/{symbol}/{timeframe}                   │  │
│  │  - /api/status                                       │  │
│  └──────────────────┬───────────────────────────────────┘  │
│                     │                                       │
│  ┌──────────────────▼───────────────────────────────────┐  │
│  │  Expert Advisor (MQL5)                              │  │
│  │  - MT5 API hozzáférés                               │  │
│  │  - Adatgyűjtés                                      │  │
│  │  - Kommunikáció a FastAPI szerverrel               │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Komponensek

### 1. Expert Advisor (MQL5)
**Fájl**: `mt5_data_provider.mq5`

**Főbb funkciók**:
- Kapcsolódás MetaTrader 5-höz
- Adatok gyűjtése CopyRates() függvénnyel
- Kommunikáció Python szerverrel (named pipes vagy socket)
- Több időkeret támogatása (M1, M5, M15, H1, H4, D1, W1)

**API végpontok (MQL5 oldalon)**:
```mql
// EA funkciók
bool GetSymbols(string &symbols[]);
bool GetHistoricalData(string symbol, ENUM_TIMEFRAMES timeframe, datetime start, datetime end, MqlRates &rates[]);
```

### 2. FastAPI Szerver (Wine-en belül)
**Fájlok**:
- `mt5_bridge/server.py` - FastAPI alkalmazás
- `mt5_bridge/mt5_client.py` - MT5 EA kommunikáció
- `mt5_bridge/models.py` - Adatmodellek

**API végpontok**:
```python
# GET /api/symbols - Elérhető szimbólumok
@app.get("/api/symbols")
async def get_symbols():
    pass

# GET /api/data/{symbol}/{timeframe} - Adatok letöltése
@app.get("/api/data/{symbol}/{timeframe}")
async def get_data(symbol: str, timeframe: str, start_date: str = None, end_date: str = None):
    pass

# GET /api/status - Szerver állapot
@app.get("/api/status")
async def get_status():
    pass
```

### 3. MT5 Collector (Linux oldal)
**Fájlok**:
- `neural_ai/collectors/mt5/mt5_collector.py` - Fő collector osztály
- `neural_ai/collectors/mt5/fastapi_client.py` - FastAPI kliens
- `neural_ai/collectors/mt5/exceptions.py` - Kivételek

**Főbb metódusok**:
```python
class MT5Collector:
    def __init__(self, config):
        self.api_client = FastAPIClient(config['server_url'])
        self.storage = StorageFactory.get_storage(config.get('storage', {}))
    
    async def collect(self, symbol, timeframe, start_date=None, end_date=None):
        # 1. Ellenőrzi a cache-t
        # 2. Lekéri az adatokat a FastAPI-tól
        # 3. Validálja az adatokat
        # 4. Elmenti a storage-ba
        # 5. Visszaadja az adatokat
        pass
    
    async def get_available_symbols(self):
        pass
    
    async def get_available_timeframes(self):
        pass
```

## Fejlesztési Lépések

### 1. hét: Expert Advisor fejlesztés
- [ ] MQL5 EA alapstruktúra
- [ ] Adatgyűjtési funkciók implementálása
- [ ] Kommunikációs réteg (named pipes/socket)
- [ ] Tesztelés MetaTrader 5-ben

### 2. hét: FastAPI Szerver
- [ ] FastAPI alkalmazás létrehozása
- [ ] MT5 Python csomag integráció
- [ ] EA kommunikáció implementálása
- [ ] API végpontok tesztelése
- [ ] Wine környezetben való futtatás

### 3. hét: Python Collector
- [ ] MT5Collector osztály implementálása
- [ ] FastAPI kliens komponens
- [ ] Adatvalidáció és formázás
- [ ] Storage integráció
- [ ] Hibakezelés

### 4. hét: Integráció és tesztelés
- [ ] Teljes adatfolyam tesztelése
- [ ] Több időkeret és szimbólum tesztelése
- [ ] Teljesítmény optimalizálás
- [ ] Hibakeresés és finomhangolás
- [ ] Dokumentáció

## Konfiguráció

```yaml
# configs/collectors/mt5.yaml
mt5:
  # FastAPI szerver beállítások
  server:
    url: "http://localhost:8000"
    timeout: 30
    max_retries: 3
  
  # Adatgyűjtési beállítások
  data:
    use_cache: true
    cache_expiry: 3600
    validate_data: true
    chunk_size: 10000
    max_candles: 50000
  
  # Időkeret leképezés
  timeframes:
    M1: 1
    M5: 5
    M15: 15
    H1: 60
    H4: 240
    D1: 1440
    W1: 10080
```

## Kommunikációs Protokoll

### Adatkérés folyamata:
1. **Linux**: MT5Collector hívja a FastAPI-t
2. **Wine**: FastAPI szerver fogadja a kérést
3. **Wine**: Szerver kommunikál az EA-val (named pipes/socket)
4. **Wine**: EA lekéri az adatokat MT5-ből
5. **Wine**: EA visszaküldi az adatokat a szervernek
6. **Wine**: Szerver formázza és válaszol
7. **Linux**: MT5Collector fogadja és feldolgozza

### Adatformátum (JSON):
```json
{
  "symbol": "EURUSD",
  "timeframe": "H1",
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

## Előnyök

1. **Kompatibilitás**: Linux-en is működik az MT5 adatgyűjtés
2. **Egyszerűség**: A collector csak HTTP kéréseket küld
3. **Rugalmasság**: A Wine oldalon bármilyen Python könyvtár használható
4. **Megbízhatóság**: Az EA külön processként fut
5. **Skálázhatóság**: Több collector is csatlakozhat ugyanahhoz a szerverhez

## Kihívások és Megoldások

### Kihívás: Kommunikáció Wine és Linux között
**Megoldás**: FastAPI HTTP szerver, localhost-on fut

### Kihívás: EA és Python kommunikáció
**Megoldás**: Named pipes vagy socket kommunikáció

### Kihívás: Teljesítmény
**Megoldás**: Batch adatkérések, gyorsítótárazás

### Kihívás: Hibakezelés
**Megoldás**: Időtúllépések, újrapróbálkozások, részletes naplózás

## Tesztelési Stratégia

### Unit tesztek
- MT5Collector tesztelése mock FastAPI-val
- FastAPI szerver tesztelése mock EA-val
- Adatvalidáció és formázás tesztelése

### Integration tesztek
- Teljes adatfolyam tesztelése
- Több időkeret és szimbólum
- Nagy adatmennyiségek (25 év adat)

### Teljesítménytesztek
- Adatletöltési sebesség
- Memóriahasználat
- Párhuzamos kérések kezelése

## Sikerességi Kritériumok

- [x] EA sikeresen kommunikál a FastAPI szerverrel
- [x] FastAPI szerver képes adatokat gyűjteni MT5-ből
- [x] MT5Collector képes adatokat letölteni a FastAPI-ról
- [x] Adatok helyesen vannak validálva és formázva
- [x] Storage komponensbe történik mentés
- [x] 1 gyertya és 25 év adat is működik
- [x] Több időkeret és szimbólum támogatása
- [x] 90%+ tesztlefedettség

## Következő Lépések

1. **Terv jóváhagyása** - Elfogadjuk ezt a megközelítést?
2. **Környezet beállítása** - Wine + MT5 + Python telepítése
3. **EA fejlesztés** - MQL5 kód írása
4. **FastAPI szerver** - Python szerver implementálása
5. **MT5Collector** - Linux oldali collector fejlesztése
6. **Integráció** - Összekapcsolás és tesztelés
7. **Dokumentáció** - Használati útmutató és API dokumentáció

---

**Dokumentum verzió**: 1.0  
**Utolsó frissítés**: 2025-12-15  
**Felelős**: Architect Mode