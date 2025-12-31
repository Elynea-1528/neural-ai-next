# core/storage/services/resampler_service/exceptions/resampler_error.py

ResamplerService kivételek.

## Osztályok

### `ResamplerError`

Alapértelmezett hiba a ResamplerService-hez.

### `DataLoadError`

Hiba adatok betöltése során.

### `ResamplingError`

Hiba az adatok átalakítása (resampling) során.

### `InvalidTimeframeError`

Hiba érvénytelen időkeret esetén.


## Függvények

### `__init__`

InvalidTimeframeError inicializálása.

        Args:
            timeframe: Az érvénytelen időkeret


---

**Forrásfájl:** [`core/storage/services/resampler_service/exceptions/resampler_error.py`](../../../neural_ai/core/storage/services/resampler_service/exceptions/resampler_error.py)
