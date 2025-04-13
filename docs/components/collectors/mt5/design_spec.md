# MT5 Collector Komponens

## Áttekintés

Az MT5 Collector komponens felelős a MetaTrader 5 platformról történő adatok gyűjtéséért és rendszerezéséért. A komponens aszinkron működéssel, hatékony kapcsolatkezeléssel és adatstruktúrákkal biztosítja a különböző pénzügyi instrumentumok és időkeretek adatainak megbízható gyűjtését.

## Fő funkciók

- MetaTrader 5 platformhoz való kapcsolódás és hitelesítés
- Valós idejű és történelmi áradatok gyűjtése
- Különböző időkeretek (M1, M5, M15, H1, H4, D1, stb.) támogatása
- Automatikus újrakapcsolódás és hibajavítás
- Adatvalidáció és konzisztencia ellenőrzés
- Hatékony adattárolás a Storage komponensen keresztül
- Többszálú/aszinkron lekérdezések kezelése

## Architekturális felépítés

### Komponens struktúra

MT5Collector
├── MT5Connection       # A kapcsolatot kezeli a MT5 platformmal
│   ├── Authenticator  # Hitelesítés és session kezelés
│   └── ConnectionPool # Kapcsolati pool a párhuzamos kérésekhez
├── DataFetcher        # Adatok lekérdezése
│   ├── HistoryFetcher # Történelmi adatok lekérdezése
│   └── LiveFetcher    # Valós idejű adatok gyűjtése
├── DataProcessor      # Nyers adatok feldolgozása
│   ├── TimeFrameConverter # Időkeret konverziók
│   └── DataValidator      # Adatok validálása
└── DataPersistor      # Adatok tárolása
    └── StorageAdapter      # Interfész a Storage komponenshez

### Működési diagram

  +-------------------+      +-------------------+      +-------------------+
  |                   |      |                   |      |                   |
  | Kapcsolódás MT5   +----->+ Adatok lekérése   +----->+ Adatok validálása |
  |                   |      |                   |      |                   |
  +-------------------+      +-------------------+      +--------+----------+
                                                                |
                                                                v
  +-------------------+      +-------------------+      +-------+-----------+
  |                   |      |                   |      |                   |
  | Kész adatok       |<-----+ Adatok tárolása   |<-----+ Adatok formázása  |
  |                   |      |                   |      |                   |
  +-------------------+      +-------------------+      +-------------------+

## Konfiguráció

Az MT5 Collector a `configs/collectors/mt5.yaml` fájlban konfigurálható. Példa konfiguráció:

```yaml
# MT5 Collector konfiguráció
mt5:
  # Kapcsolódási beállítások
  connection:
    server: "MetaQuotes-Demo"   # Szerver neve
    login: 12345678             # Felhasználói azonosító
    password: "password123"     # Jelszó
    timeout: 60                 # Kapcsolódási időtúllépés (másodperc)
    max_retries: 3              # Újracsatlakozási próbálkozások
    retry_delay: 5              # Újrapróbálkozási késleltetés (másodperc)

  # Adatgyűjtési beállítások
  data:
    use_cache: true             # Cache engedélyezése
    cache_expiry: 3600          # Cache lejárati ideje (másodperc)
    validate_data: true         # Adatok validálása
    chunk_size: 10000           # Adatok lekérése chunk-okban
    max_candles: 50000          # Maximum lekérhető gyertyák száma

  # Időkeret beállítások
  timeframes:
    M1: 1                       # 1 perc
    M5: 5                       # 5 perc
    M15: 15                     # 15 perc
    M30: 30                     # 30 perc
    H1: 60                      # 1 óra
    H4: 240                     # 4 óra
    D1: 1440                    # 1 nap
    W1: 10080                   # 1 hét

```
## API Referencia

### Nyilvános Metódusok

#### async connect() -> bool

Kapcsolódás a MetaTrader 5 platformhoz.
- Visszatérés: True sikeres kapcsolódás esetén, egyébként False
- Kivételek: MT5ConnectionError: Ha a kapcsolódás sikertelen

#### async disconnect() -> bool

Kapcsolat bontása a MetaTrader 5 platformmal.
- Visszatérés: True sikeres kapcsolatbontás esetén, egyébként False

#### is_connected() -> bool

Ellenőrzi a kapcsolat állapotát.
- Visszatérés: True ha kapcsolódva van, egyébként False

#### async download_data(symbol: str, timeframe: str, start_date: Optional[Union[str, datetime]] = None, end_date: Optional[Union[str, datetime]] = None, max_candles: Optional[int] = None) -> pd.DataFrame

Adatok letöltése a megadott szimbólumhoz és időkerethez.

- Paraméterek:
    - symbol: Kereskedési szimbólum (pl. "EURUSD")
    - timeframe: Időkeret (pl. "M1", "H1", "D1")
    - start_date: Kezdő dátum (opcionális)
    - end_date: Záró dátum (opcionális)
    - max_candles: Maximum letöltendő gyertyák száma (opcionális)
- Visszatérés: DataFrame az OHLCV adatokkal
- Kivételek:
    - DataFetchError: Ha az adatok letöltése sikertelen
    - ValidationError: Ha a letöltött adatok érvénytelenek

#### async get_available_symbols() -> List[str]

Elérhető szimbólumok listájának lekérése.

- Visszatérés: A szimbólumok listája
- Kivételek: MT5ConnectionError: Ha nincs aktív kapcsolat

#### get_available_timeframes() -> Dict[str, int]

Elérhető időkeretek listájának lekérése.

- Visszatérés: Időkeretek szótára (név -> érték párok)

#### check_data_quality(data: pd.DataFrame) -> Dict[str, Any]

Adatok minőségének ellenőrzése.

- Paraméterek:
    - data: Ellenőrizendő adatok DataFrame-ben
- Visszatérés: Minőségi metrikák szótára
    - gaps: Hiányzó időszakok száma
    - missing_values: Hiányzó értékek száma
    - duplicates: Duplikált időpontok száma
    - consistency: Konzisztencia pontszám (0-100)

## Hibakezelés

Az MT5 Collector a következő kivételosztályokat használja:

- **MT5CollectorError**: Alap kivétel az MT5 Collector komponenshez
- **MT5ConnectionError**: Kapcsolódási hibák
- **DataFetchError**: Adatok lekérésével kapcsolatos hibák
- **ValidationError**: Adat validációs hibák
- **ConfigurationError**: Konfigurációs hibák

Példa hibakezelésre:

```python
try:
    collector = CollectorFactory.get_collector("mt5", config)
    await collector.connect()
    data = await collector.download_data("EURUSD", "H1", start_date="2023-01-01")
except MT5ConnectionError as e:
    logger.error(f"Kapcsolódási hiba: {e}")
except DataFetchError as e:
    logger.error(f"Adatlekérési hiba: {e}")
finally:
    if collector.is_connected():
        await collector.disconnect()
```

## Használati példák

### Alapvető használat

```python
import asyncio
from neural_ai.core.config import ConfigManagerFactory
from neural_ai.collectors import CollectorFactory

async def main():
    # Konfiguráció betöltése
    config = ConfigManagerFactory.get_manager("configs/collectors/mt5.yaml")

    # MT5 Collector létrehozása
    collector = CollectorFactory.get_collector("mt5", config)

    try:
        # Kapcsolódás a platformhoz
        connected = await collector.connect()
        if not connected:
            print("Nem sikerült kapcsolódni az MT5 platformhoz")
            return

        # Adatok letöltése
        data = await collector.download_data(
            symbol="EURUSD",
            timeframe="H1",
            start_date="2023-01-01",
            end_date="2023-01-31"
        )

        print(f"Letöltött adatok: {len(data)} sor")
        print(data.head())

        # Adatok minőségének ellenőrzése
        quality = collector.check_data_quality(data)
        print(f"Adatminőség: {quality}")

    finally:
        # Kapcsolat bontása
        if collector.is_connected():
            await collector.disconnect()

asyncio.run(main())
```

### Több időkeret párhuzamos letöltése

```python
import asyncio
from neural_ai.collectors import CollectorFactory

async def download_multiple_timeframes(symbol, timeframes):
    config = ConfigManagerFactory.get_manager("configs/collectors/mt5.yaml")
    collector = CollectorFactory.get_collector("mt5", config)

    await collector.connect()

    try:
        tasks = []
        for timeframe in timeframes:
            task = asyncio.create_task(
                collector.download_data(symbol, timeframe)
            )
            tasks.append((timeframe, task))

        results = {}
        for timeframe, task in tasks:
            results[timeframe] = await task
            print(f"{symbol} {timeframe}: {len(results[timeframe])} sor")

        return results

    finally:
        await collector.disconnect()

# Használat
timeframes = ["M15", "H1", "H4", "D1"]
data = asyncio.run(download_multiple_timeframes("EURUSD", timeframes))
```

## Teljesítmény optimalizációk

Az MT5 Collector komponens a következő teljesítmény optimalizációkat alkalmazza:

1. **Kapcsolat újrahasználata**: A komponens újrahasználja a meglévő kapcsolatokat több adatlekéréshez
2. **Batch feldolgozás**: Nagy időszakok esetén az adatok kisebb részletekben kerülnek letöltésre
3. **Adat gyorsítótárazás**: A gyakran használt adatok gyorsítótárban tárolódnak
4. **Párhuzamos kérések**: Több szimbólum/időkeret párhuzamos lekérdezése
5. **Optimalizált adatstruktúrák**: A lekért adatok hatékony tárolása és feldolgozása

## Biztonsági szempontok

1. **Hitelesítési adatok védelme**: A kapcsolódási adatok biztonságos tárolása
   - Jelszavak soha nem kerülnek naplózásra
   - Jelszavak soha nem kerülnek plain text formában tárolásra

2. **Hibaellenőrzés**: Minden bemeneti adat ellenőrzése
   - Szimbólumok létezésének ellenőrzése
   - Időkeretek validálása
   - Dátum paraméterek formátumának ellenőrzése

3. **Korlátozások**: Időbeli és erőforrásbeli korlátozások a túlzott használat elkerülésére
   - Maximum lekérendő adatmennyiség limitálása
   - Rate limiting a túl gyakori kérések elkerülésére
   - Timeout beállítások a végtelen várakozások elkerülésére

4. **Hibakezelés**: Robusztus hibakezelés az adatvesztés megelőzésére
   - Automatikus újrapróbálkozás ideiglenes hibák esetén
   - Graceful shutdown kapcsolatvesztés esetén

## Fejlesztési útmutató

### Új funkciók hozzáadása

Az MT5 Collector bővítéséhez:

1. Az `MT5Collector` osztály bővítése a szükséges metódusokkal:


2. Egység tesztek írása az új funkciókhoz:

3. Dokumentáció frissítése:
   - API referencia kibővítése
   - Használati példák hozzáadása
   - Belső dokumentáció frissítése

## Teljesítménymérés

Az MT5 Collector teljesítménye mérhető a következő metrikákkal:

1. **Letöltési sebesség**: másodperc/1000 gyertya
2. **Sikeres/sikertelen kapcsolódások aránya**
3. **Adatminőség konzisztencia pontszáma**
4. **Memória- és CPU-használat** nagy adatmennyiségek esetén

## Diagnosztika és hibaelhárítás

### Gyakori problémák és megoldásaik

#### Kapcsolódási hibák:

- **Ellenőrizze a szervernevet és hitelesítési adatokat**
  - Győződjön meg róla, hogy a szerver neve és a belépési adatok helyesek
  - Ellenőrizze, hogy a fiók aktív és nem zárolt

- **Ellenőrizze az internet kapcsolatot**
  - Tesztelje a kapcsolatot a szerverhez más eszközökkel
  - Ellenőrizze a tűzfal és proxy beállításokat

- **Növelje a timeout értéket sűrűbb hálózati forgalom esetén**
  - A config fájlban növelje meg a `timeout` értéket
  - Próbálja meg növelni a `max_retries` értékét

#### Adatletöltési hibák:

- **Ellenőrizze a szimbólum nevét és elérhetőségét**
  - Használja a `get_available_symbols()` metódust az elérhető szimbólumok listázásához
  - Ellenőrizze, hogy a kereskedési idő megfelelő-e a kért szimbólumhoz

- **Csökkentse a lekérendő adatmennyiséget**
  - Használjon szűkebb időintervallumot
  - Állítsa be a `max_candles` paramétert

- **Használjon kisebb chunk-okat a letöltéshez**
  - Nagy időszakok esetén használja a fent bemutatott chunk-olási módszert

#### Adatminőségi problémák:

- **Ellenőrizze az időzóna beállításait**
  - Győződjön meg róla, hogy az időzóna beállítások konzisztensek

- **Használja a `check_data_quality` metódust a problémák azonosítására**
  - Az eredmények alapján szűrje vagy tisztítsa az adatokat

- **Szűrje ki a duplikált vagy hiányos adatokat**
  - Alkalmazza a pandas eszközeit a duplikált sorok eltávolítására:
    ```python
    data = data.drop_duplicates(subset=['time'])
    ```

## Tesztelés

Az MT5 Collector komponens tesztelhető a következő módokon:

### Unit tesztek

A komponens funkcióinak izolált tesztelése:

### Integrációs tesztek

A Storage komponenssel együtt történő működés tesztelése:


### Szimulált környezet

Mock MT5 API válaszok használata a valós platformtól független teszteléshez:


### Teljesítménytesztek

Nagy mennyiségű adat letöltésének tesztelése:


## Kapcsolódó komponensek

Az MT5 Collector komponens a következő komponensekkel működik együtt:

- **Storage**: Az MT5 Collector által gyűjtött adatok tárolása
  - Az adatok a Storage komponensbe kerülnek mentésre cache és perzisztencia céljából

- **Processors**: Az adatok feldolgozása és elemzése
  - A letöltött nyers adatok a különböző processzorok inputjai lesznek

- **Config Manager**: A komponens konfigurációjának kezelése
  - A komponens működési paramétereit a Config Manager szolgáltatja

- **Logger**: A komponens működésének naplózása
  - Minden művelet és hiba naplózásra kerül a Logger komponensen keresztül
