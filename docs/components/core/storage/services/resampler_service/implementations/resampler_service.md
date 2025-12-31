# core/storage/services/resampler_service/implementations/resampler_service.py

ResamplerService implementáció - Tick adatokból OHLCV gyertyák létrehozása.

## Osztályok

### `ResamplerService`

ResamplerService implementáció, amely tick adatokból hoz létre OHLCV gyertyákat.

    Ez a szolgáltatás felelős a tick adatok átalakításáért OHLCV (Open, High, Low, Close, Volume)
    gyertyákká a megadott időkeretben. A hatékonyság érdekében Polars-t használ.


## Függvények

### `__init__`

ResamplerService inicializálása.

        Args:
            storage: A tárolási interfész példány (Dependency Injection)

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
            InvalidTimeframeError: Ha az időkeret érvénytelen
            DataLoadError: Ha hiba történik az adatok betöltése során
            ResamplingError: Ha hiba történik az átalakítás során

### `_validate_timeframe`

Időkeret validálása.

        Args:
            timeframe: Az időkeret string

        Raises:
            InvalidTimeframeError: Ha az időkeret érvénytelen

### `_load_tick_data`

Tick adatok betöltése a tárolóból.

        Args:
            symbol: A kereskedési szimbólum
            start: A kezdő időpont
            end: A záró időpont

        Returns:
            Polars DataFrame a tick adatokkal

        Raises:
            DataLoadError: Ha hiba történik a betöltés során

### `_convert_to_ohlcv`

Tick adatok átalakítása OHLCV gyertyákká.

        Args:
            tick_data: Polars DataFrame tick adatokkal
            timeframe: Az időkeret

        Returns:
            Pandas DataFrame OHLCV gyertyákkal


---

**Forrásfájl:** [`core/storage/services/resampler_service/implementations/resampler_service.py`](../../../neural_ai/core/storage/services/resampler_service/implementations/resampler_service.py)
