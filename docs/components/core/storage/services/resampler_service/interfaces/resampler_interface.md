# core/storage/services/resampler_service/interfaces/resampler_interface.py

ResamplerService Interface - Tick adatokból OHLCV gyertyák létrehozásáért felelős.

## Osztályok

### `ResamplerInterface`

ResamplerService interfész, amely definiálja a tick adatok OHLCV gyertyákká alakítását.


## Függvények

### `resample`

Tick adatok átalakítása OHLCV gyertyákká a megadott időkeretben.

        Args:
            symbol: A kereskedési szimbólum (pl. 'EURUSD')
            start: A kezdő időpont
            end: A záró időpont
            timeframe: Az időkeret (alapértelmezett: '1m' - 1 perc)

        Returns:
            DataFrame: OHLCV gyertyákat tartalmazó DataFrame

        Raises:
            ResamplerError: Ha hiba történik az átalakítás során


---

**Forrásfájl:** [`core/storage/services/resampler_service/interfaces/resampler_interface.py`](../../../neural_ai/core/storage/services/resampler_service/interfaces/resampler_interface.py)
