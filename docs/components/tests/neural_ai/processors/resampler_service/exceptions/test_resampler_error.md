# 🧪 Teszt: tests/neural_ai/processors/resampler_service/exceptions/test_resampler_error.py

**Tesztelt modul:** [`neural_ai/processors/resampler_service/exceptions/resampler_error.py`](../../neural_ai/processors/resampler_service/exceptions/resampler_error.py)

Unit tesztek a Resampler Exception osztályokhoz.

## Teszt Osztály: `TestResamplerError`

Tesztek a ResamplerError alap kivételhez.

### ✓ `test_resampler_error_is_neural_ai_exception()`

Ellenőrzi, hogy ResamplerError a NeuralAIException leszármazottja.

### ✓ `test_resampler_error_can_be_raised()`

Ellenőrzi, hogy ResamplerError dobható.

### ✓ `test_resampler_error_with_message()`

Ellenőrzi, hogy ResamplerError üzenettel dobható.

### ✓ `test_resampler_error_with_details()`

Ellenőrzi, hogy ResamplerError részletekkel dobható.

### ✓ `test_resampler_error_with_original_error()`

Ellenőrzi, hogy ResamplerError eredeti hibával dobható.

## Teszt Osztály: `TestDataLoadError`

Tesztek a DataLoadError kivételhez.

### ✓ `test_data_load_error_is_resampler_error()`

Ellenőrzi, hogy DataLoadError a ResamplerError leszármazottja.

### ✓ `test_data_load_error_can_be_raised()`

Ellenőrzi, hogy DataLoadError dobható.

### ✓ `test_data_load_error_with_parameters()`

Ellenőrzi, hogy DataLoadError paraméterekkel dobható.

### ✓ `test_data_load_error_with_original_error()`

Ellenőrzi, hogy DataLoadError eredeti hibával dobható.

## Teszt Osztály: `TestResamplingError`

Tesztek a ResamplingError kivételhez.

### ✓ `test_resampling_error_is_resampler_error()`

Ellenőrzi, hogy ResamplingError a ResamplerError leszármazottja.

### ✓ `test_resampling_error_can_be_raised()`

Ellenőrzi, hogy ResamplingError dobható.

### ✓ `test_resampling_error_with_parameters()`

Ellenőrzi, hogy ResamplingError paraméterekkel dobható.

### ✓ `test_resampling_error_with_original_error()`

Ellenőrzi, hogy ResamplingError eredeti hibával dobható.

## Teszt Osztály: `TestInvalidTimeframeError`

Tesztek az InvalidTimeframeError kivételhez.

### ✓ `test_invalid_timeframe_error_is_resampler_error()`

Ellenőrzi, hogy InvalidTimeframeError a ResamplerError leszármazottja.

### ✓ `test_invalid_timeframe_error_can_be_raised()`

Ellenőrzi, hogy InvalidTimeframeError dobható.

### ✓ `test_invalid_timeframe_error_with_timeframe()`

Ellenőrzi, hogy InvalidTimeframeError időkerettel dobható.

### ✓ `test_invalid_timeframe_error_caught_as_resampler_error()`

Ellenőrzi, hogy InvalidTimeframeError elkapható ResamplerError-ként.

---

**Teszt fájl:** [`tests/neural_ai/processors/resampler_service/exceptions/test_resampler_error.py`](../../tests/neural_ai/processors/resampler_service/exceptions/test_resampler_error.py)

**Tesztelt modul:** [`neural_ai/processors/resampler_service/exceptions/resampler_error.py`](../../neural_ai/processors/resampler_service/exceptions/resampler_error.py)
