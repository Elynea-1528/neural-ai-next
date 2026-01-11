# core/processing/resampler_service/implementations/resampler_service.py

ResamplerService implementáció - Tick adatokból OHLCV gyertyák létrehozása.

Ez a modul a ResamplerService osztályt tartalmazza, amely tick adatokból hoz létre OHLCV gyertyákat különböző időkeretekben.

## Osztályok

### `ResamplerService`

ResamplerService implementáció, amely tick adatokból hoz létre OHLCV gyertyákat.

    Ez az osztály a ResamplerInterface-t implementálja, és felelős a tick adatok
    átalakításáért OHLCV gyertyákká. Támogatja a hagyományos időkereteket (1m, 5m, stb.)
    és a "tick" timeframe-ot, amely esetben bypass aggregációt végez és enrich minden tick-et.

    Attributes:
        _storage: A tárolási interfész példány (Dependency Injection)
        _logger: A logger interfész példány


## Függvények

### `__init__`

ResamplerService inicializálása.

        Args:
            storage: A tárolási interfész példány (Dependency Injection)

        Példa:
            >>> storage = StorageFactory.get_storage()
            >>> resampler = ResamplerService(storage)

### `resample`

Tick adatok átalakítása OHLCV gyertyákká a megadott időkeretben.

        Ez az aszinkron metódus betölti a tick adatokat a tárolóból, átalakítja
        őket OHLCV formátumba, majd visszaadja a kívánt típusban (Pandas vagy Polars).

        Args:
            symbol: A kereskedési szimbólum (pl. 'EURUSD')
            start: A kezdő időpont
            end: A záró időpont
            timeframe: Az időkeret (alapértelmezett: '1m' - 1 perc, vagy 'tick' bypass)
            return_type: A visszaadott DataFrame típusa ('pandas' vagy 'polars')

        Returns:
            DataFrame: OHLCV gyertyákat tartalmazó DataFrame (Pandas vagy Polars)

        Raises:
            InvalidTimeframeError: Ha az időkeret érvénytelen
            DataLoadError: Ha hiba történik az adatok betöltése során
            ResamplingError: Ha hiba történik az átalakítás során

        Példa:
            >>> df = await resampler.resample("EURUSD", start, end, timeframe="tick")

### `_validate_timeframe`

Időkeret validálása.

        Args:
            timeframe: Az időkeret string

        Raises:
            InvalidTimeframeError: Ha az időkeret érvénytelen

        Példa:
            >>> resampler._validate_timeframe("1m")

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

Tick adatok átalakítása kiterjesztett OHLCV gyertyákká.

        Ha timeframe "tick", akkor bypass aggregációt és enrich minden tick-et
        új oszlopokkal (mid_close, spread, tick_volume=1, stb.).

        Args:
            tick_data: Polars DataFrame tick adatokkal
            timeframe: Az időkeret

        Returns:
            Polars DataFrame kiterjesztett gyertyákkal (Bid/Mid OHLC, Spread, Real/Tick Volume)


---

**Forrásfájl:** [`core/processing/resampler_service/implementations/resampler_service.py`](../../../../neural_ai/core/processing/resampler_service/implementations/resampler_service.py)
