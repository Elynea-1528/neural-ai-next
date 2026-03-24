# 🧪 Teszt: tests/neural_ai/data/ingestion/test_market_data_persister.py

**Tesztelt modul:** [`neural_ai/data/ingestion/market_data_persister.py`](../../neural_ai/data/ingestion/market_data_persister.py)

Tesztek a MarketDataPersister szolgáltatáshoz.

Ez a modul tartalmazza a MarketDataPersister osztály átfogó tesztjeit,
amelyek ellenőrzik a market data eventek bufferezését és mentését.

## Teszt Osztály: `MockMarketDataEvent`

Mock market data event a teszteléshez.

## Teszt Osztály: `TestMarketDataPersisterInit`

Tesztek a MarketDataPersister inicializálásához.

### ✓ `test_init_with_default_values()`

Teszteli az alapértelmezett értékekkel történő inicializálást.

### ✓ `test_init_with_custom_buffer_size()`

Teszteli az egyéni buffer mérettel történő inicializálást.

## Teszt Osztály: `TestMarketDataPersisterStartStop`

Tesztek a MarketDataPersister indításához és leállításához.

### ✓ `test_start_success()`

Teszteli a sikeres indítást.

### ✓ `test_start_when_already_running()`

Teszteli az indítást, ha már fut a szolgáltatás.

### ✓ `test_stop_success()`

Teszteli a sikeres leállítást.

### ✓ `test_stop_when_not_running()`

Teszteli a leállítást, ha nem fut a szolgáltatás.

## Teszt Osztály: `TestMarketDataPersisterOnMarketData`

Tesztek az on_market_data eseménykezelőhöz.

### ✓ `test_on_market_data_single_event()`

Teszteli egyetlen event fogadását.

### ✓ `test_on_market_data_batch_events()`

Teszteli batch eventek fogadását.

### ✓ `test_on_market_data_unknown_format()`

Teszteli ismeretlen formátumú event kezelését.

### ✓ `test_on_market_data_triggers_flush_at_limit()`

Teszteli, hogy a buffer kiürül, ha eléri a méretkorlátot.

## Teszt Osztály: `TestMarketDataPersisterPeriodicFlush`

Tesztek a periodikus flush taskhoz.

### ✓ `test_periodic_flush_triggers_on_new_hour()`

Teszteli, hogy az új óra kezdetekor lefut-e a flush.

### ✓ `test_periodic_flush_handles_exception()`

Teszteli a kivétel kezelését a periodikus flush során.

## Teszt Osztály: `TestMarketDataPersisterFlush`

Tesztek a buffer kiürítéshez.

### ✓ `test_flush_all_buffers_with_data()`

Teszteli az összes buffer kiürítését adatokkal.

### ✓ `test_flush_all_buffers_empty()`

Teszteli az üres buffer kiürítését.

### ✓ `test_flush_symbol_buffer_success()`

Teszteli egy szimbólum bufferének sikeres kiürítését.

### ✓ `test_flush_symbol_buffer_empty()`

Teszteli az üres szimbólum buffer kiürítését.

### ✓ `test_flush_symbol_buffer_handles_exception()`

Teszteli a kivétel kezelését a szimbólum buffer kiürítésekor.

## Teszt Osztály: `TestMarketDataPersisterSave`

Tesztek az adatok tárolóba mentéséhez.

### ✓ `test_save_events_to_storage_with_parquet_service()`

Teszteli az eventek mentését ParquetStorageService használatával.

### ✓ `test_save_events_to_storage_fallback()`

Teszteli az eventek mentését fallback metódussal.

### ✓ `test_save_events_to_storage_empty()`

Teszteli az üres event lista mentését.

### ✓ `test_save_events_to_storage_handles_exception()`

Teszteli a kivétel kezelését az eventek mentésekor.

## Teszt Osztály: `TestMarketDataPersisterConvertToDataFrame`

Tesztek a DataFrame konverzióhoz.

### ✓ `test_convert_events_to_dataframe_with_pandas()`

Teszteli az eventek DataFrame-é konvertálását pandas használatával.

### ✓ `test_convert_events_to_dataframe_with_polars()`

Teszteli az eventek DataFrame-é konvertálását polars használatával.

### ✓ `test_convert_events_to_dataframe_no_library()`

Teszteli a kivételt, ha egyik library sincs telepítve.

## Teszt Osztály: `TestMarketDataPersisterIntegration`

Integrációs tesztek a MarketDataPersister-hez.

### ✓ `test_full_workflow()`

Teszteli a teljes munkafolyamatot.

---

**Teszt fájl:** [`tests/neural_ai/data/ingestion/test_market_data_persister.py`](../../tests/neural_ai/data/ingestion/test_market_data_persister.py)

**Tesztelt modul:** [`neural_ai/data/ingestion/market_data_persister.py`](../../neural_ai/data/ingestion/market_data_persister.py)
