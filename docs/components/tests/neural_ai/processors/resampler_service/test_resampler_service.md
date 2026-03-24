# 🧪 Teszt: tests/neural_ai/processors/resampler_service/test_resampler_service.py

**Tesztelt modul:** [`neural_ai/processors/resampler_service/resampler_service.py`](../../neural_ai/processors/resampler_service/resampler_service.py)

ResamplerService unit tesztek - 100% coverage cél.

## Teszt Osztály: `TestResamplerServiceInitialization`

ResamplerService inicializálás tesztek.

### ✓ `test_init_success()`

Teszt: Sikeres inicializálás függőségekkel.

## Teszt Osztály: `TestResamplerServiceValidateTimeframe`

ResamplerService _validate_timeframe tesztek.

### ✓ `test_validate_timeframe_valid()`

Teszt: Érvényes timeframe-ek validálása.

### ✓ `test_validate_timeframe_invalid()`

Teszt: Érvénytelen timeframe-ek elutasítása.

## Teszt Osztály: `TestResamplerServiceLoadTickData`

ResamplerService _load_tick_data tesztek.

### ✓ `test_load_tick_data_success()`

Teszt: Sikeres tick adat betöltés.

### ✓ `test_load_tick_data_empty()`

Teszt: Üres adat betöltés (warning log).

### ✓ `test_load_tick_data_no_method()`

Teszt: Storage nem támogatja a read_tick_data metódust.

### ✓ `test_load_tick_data_storage_exception()`

Teszt: Storage kivételt dob betöltéskor.

## Teszt Osztály: `TestResamplerServiceConvertToOHLCV`

ResamplerService _convert_to_ohlcv tesztek.

### ✓ `test_convert_to_ohlcv_empty_dataframe()`

Teszt: Üres DataFrame kezelése.

### ✓ `test_convert_to_ohlcv_missing_columns()`

Teszt: Hiányzó oszlopok kezelése.

### ✓ `test_convert_to_ohlcv_tick_timeframe()`

Teszt: Tick timeframe (bypass aggregáció).

### ✓ `test_convert_to_ohlcv_different_timeframes()`

Teszt: Különböző timeframe-ek aggregációja.

### ✓ `test_convert_to_ohlcv_1m_aggregation()`

Teszt: 1m aggregáció részletes ellenőrzés.

## Teszt Osztály: `TestResamplerServiceResample`

ResamplerService resample tesztek (fő metódus).

### ✓ `test_resample_success_polars()`

Teszt: Sikeres resample Polars visszatérési típussal.

### ✓ `test_resample_success_pandas()`

Teszt: Sikeres resample Pandas visszatérési típussal.

### ✓ `test_resample_invalid_timeframe()`

Teszt: Érvénytelen timeframe elutasítása.

### ✓ `test_resample_invalid_return_type()`

Teszt: Érvénytelen return_type elutasítása.

### ✓ `test_resample_data_load_error()`

Teszt: Adat betöltési hiba kezelése.

### ✓ `test_resample_conversion_error()`

Teszt: Konverziós hiba kezelése.

### ✓ `test_resample_default_timeframe()`

Teszt: Alapértelmezett timeframe (1m).

### ✓ `test_resample_all_timeframes()`

Teszt: Minden támogatott timeframe működik.

---

**Teszt fájl:** [`tests/neural_ai/processors/resampler_service/test_resampler_service.py`](../../tests/neural_ai/processors/resampler_service/test_resampler_service.py)

**Tesztelt modul:** [`neural_ai/processors/resampler_service/resampler_service.py`](../../neural_ai/processors/resampler_service/resampler_service.py)
