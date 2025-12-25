# MT5 Expert Advisor Fájlok Tesztelése

## Áttekintés

Ez a dokumentum a [`tests/experts/test_mt5_files.py`](../../../tests/experts/test_mt5_files.py) tesztmodul dokumentációja. A modul a Neural AI Next projekt MT5 Expert Advisor fájljainak ellenőrzéséért felelős.

## Cél

A tesztmodul célja, hogy ellenőrizze a következő MT5 fájlok helyességét:
- [`neural_ai/experts/mt5/src/Neural_AI_Next.mq5`](../../../neural_ai/experts/mt5/src/Neural_AI_Next.mq5)
- [`neural_ai/experts/mt5/src/Neural_AI_Next_Multi.mq5`](../../../neural_ai/experts/mt5/src/Neural_AI_Next_Multi.mq5)

## Tesztelt Funkciók

### Alapvető Fájl Ellenőrzések

1. **Létezés ellenőrzése** - A fájloknak létezniük kell a megadott elérési úton
2. **Fájl típus ellenőrzése** - A célobjektumoknak valóban fájloknak kell lenniük
3. **Olvashatóság ellenőrzése** - A fájloknak olvashatónak kell lenniük
4. **Nem üresség ellenőrzése** - A fájloknak tartalmazniuk kell tartalmat

### Kritikus Stringek Ellenőrzése

A tesztek ellenőrzik a következő kritikus stringek jelenlétét:

#### Mindkét Fájlban
- `FastAPI_Server` - A FastAPI szerver címének konfigurálásához
- `http://localhost:8000` - Alapértelmezett szervercím
- `WebRequest` - HTTP kérésekhez használt MQL5 függvény
- `OnInit` - Expert inicializálási függvény
- `OnTick` - Tick eseménykezelő függvény
- `OnTimer` - Időzítő eseménykezelő függvény

#### Neural_AI_Next.mq5 Specifikus
- `input string FastAPI_Server = "http://localhost:8000"` - Szerver cím input
- `input int Update_Interval = 60` - Frissítési intervallum
- `input bool Enable_HTTP_Logs = true` - HTTP logolás engedélyezése
- `bool TestConnection()` - Kapcsolat tesztelő függvény
- `void CollectAndSendTickData()` - Tick adatok gyűjtése és küldése
- `void CollectAndSendOHLCVData()` - OHLCV adatok gyűjtése és küldése

#### Neural_AI_Next_Multi.mq5 Specifikus
- `input string Instruments = "EURUSD,GBPUSD,USDJPY,XAUUSD"` - Figyelt instrumentumok
- `input string Timeframes = "M1,M5,M15,H1,H4,D1"` - Figyelt időkeretek
- `input bool Enable_Historical_Collection = true` - Történelmi adatgyűjtés engedélyezése
- `input int Historical_Batch_Size = 99000` - Történelmi adatok kötegmérete
- `void ParseInstruments()` - Instrumentumok feldolgozása
- `void ParseTimeframes()` - Időkeretek feldolgozása
- `void CheckForHistoricalRequests()` - Történelmi kérések ellenőrzése
- `bool CollectAndSendHistoricalBatch()` - Történelmi adatok kötegelt küldése
- `int StringToTimeframe(string tf)` - Időkeret sztring konvertálása
- `string TimeframeToString(int tf)` - Időkeret szám konvertálása sztringgé

## Tesztesetek

### Neural_AI_Next.mq5 Tesztesetek

1. `test_single_file_exists` - Létezés ellenőrzése
2. `test_single_file_is_file` - Fájl típus ellenőrzése
3. `test_single_file_is_readable` - Olvashatóság ellenőrzése
4. `test_single_file_not_empty` - Nem üresség ellenőrzése
5. `test_single_file_contains_critical_strings` - Kritikus stringek ellenőrzése
6. `test_single_file_has_fastapi_server_input` - FastAPI szerver input ellenőrzése
7. `test_single_file_has_update_interval` - Frissítési intervallum ellenőrzése
8. `test_single_file_has_http_logs_option` - HTTP logolás opció ellenőrzése
9. `test_single_file_has_test_connection_function` - Kapcsolat teszt függvény ellenőrzése
10. `test_single_file_has_collect_tick_function` - Tick gyűjtő függvény ellenőrzése
11. `test_single_file_has_collect_ohlcv_function` - OHLCV gyűjtő függvény ellenőrzése

### Neural_AI_Next_Multi.mq5 Tesztesetek

1. `test_multi_file_exists` - Létezés ellenőrzése
2. `test_multi_file_is_file` - Fájl típus ellenőrzése
3. `test_multi_file_is_readable` - Olvashatóság ellenőrzése
4. `test_multi_file_not_empty` - Nem üresség ellenőrzése
5. `test_multi_file_larger_than_single` - Méret összehasonlítása (több funkcionalitás)
6. `test_multi_file_contains_critical_strings` - Kritikus stringek ellenőrzése
7. `test_multi_file_has_fastapi_server_input` - FastAPI szerver input ellenőrzése
8. `test_multi_file_has_instruments_input` - Instrumentumok input ellenőrzése
9. `test_multi_file_has_timeframes_input` - Időkeretek input ellenőrzése
10. `test_multi_file_has_historical_collection_option` - Történelmi gyűjtés opció ellenőrzése
11. `test_multi_file_has_historical_batch_size` - Kötegméret ellenőrzése
12. `test_multi_file_has_parse_instruments_function` - Instrumentum feldolgozó ellenőrzése
13. `test_multi_file_has_parse_timeframes_function` - Időkeret feldolgozó ellenőrzése
14. `test_multi_file_has_check_historical_requests_function` - Történelmi kérés ellenőrző
15. `test_multi_file_has_collect_historical_batch_function` - Történelmi köteg küldő
16. `test_multi_file_has_string_to_timeframe_function` - Időkeret konverter ellenőrzése
17. `test_multi_file_has_timeframe_to_string_function` - Időkeret sztring konverter

## Futtatás

### Egyedi Futtatás

```bash
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/experts/test_mt5_files.py -v
```

### Linter Ellenőrzés

```bash
/home/elynea/miniconda3/envs/neural-ai-next/bin/ruff check tests/experts/test_mt5_files.py
```

### Teljes Tesztlefedettség

A tesztmodul 28 tesztesetet tartalmaz, amelyek 100%-os lefedettséget biztosítanak a MT5 fájlok kritikus részeire.

## Kimenet Példa

```
============================= test session starts ==============================
platform linux -- Python 3.12.12, pytest-9.0.2, pluggy-1.6.0
cachedir: .pytest_cache
rootdir: /home/elynea/Dokumentumok/neural-ai-next
configfile: pyproject.toml
plugins: anyio-4.12.0, asyncio-1.3.0, cov-7.0.0
collected 28 items

tests/experts/test_mt5_files.py::TestMT5Files::test_multi_file_contains_critical_strings PASSED [  3%]
tests/experts/test_mt5_files.py::TestMT5Files::test_multi_file_exists PASSED [  7%]
...
tests/experts/test_mt5_files.py::TestMT5Files::test_single_file_not_empty PASSED [100%]

============================== 28 passed in 0.09s ==============================
```

## Kapcsolódó Dokumentáció

- [MT5 Expert Advisor README](../../../neural_ai/experts/mt5/README.md)
- [MT5 Tesztelési Útmutató](../../../neural_ai/experts/mt5/TESTING_GUIDE_HU.md)
- [Történelmi Adatgyűjtés Implementáció](../../../neural_ai/experts/mt5/HISTORICAL_EXTENSION_IMPLEMENTATION.md)

## Fejlesztői Jegyzetek

- A tesztek Python 3.12-es verzióval lettek létrehozva
- A tesztek a `unittest` keretrendszert használják
- Minden teszteset tartalmaz magyar nyelvű docstring-et
- A tesztek típusos annotációkat használnak (`-> None`)
- A kód megfelel a PEP 8 szabványoknak (ruff formázó)