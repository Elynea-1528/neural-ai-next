#!/usr/bin/env python3
"""Teszt script a ResamplerService Polars módjának validálására."""

import asyncio
from datetime import datetime

import polars as pl

from neural_ai.core.processing.resampler_service.factory import ResamplerServiceFactory


async def main():
    """Fő teszt függvény."""
    print("🧪 ResamplerService Polars mód tesztelése...")

    # Bootstrap (ha szükséges, de Factory kezeli)
    print("📦 Factory inicializálása...")

    # ResamplerService példány lekérése
    resampler = ResamplerServiceFactory.get_instance()

    # Teszt paraméterek
    symbol = "EURUSD"
    start = datetime(2024, 3, 20, 0, 0, 0)
    end = datetime(2024, 3, 20, 23, 59, 59)
    timeframe = "1m"

    print(f"📊 Adatok lekérése: {symbol} {start.date()} {timeframe} (Polars mód)")

    # Polars mód teszt
    try:
        result = await resampler.resample(
            symbol=symbol, start=start, end=end, timeframe=timeframe, return_type="polars"
        )

        # Validálás
        assert isinstance(result, pl.DataFrame), f"Várt: polars.DataFrame, kapott: {type(result)}"
        print(f"✅ Polars mód működik, típus: {type(result)}")
        print(f"📈 Sorok száma: {len(result)}")
        if len(result) > 0:
            print(f"📋 Oszlopok: {result.columns}")
            print(f"🔍 Első sor: {result.head(1).to_pandas().to_dict('records')[0]}")

    except Exception as e:
        print(f"❌ Hiba a Polars teszt során: {e}")
        return False

    print("🎉 Teszt sikeres!")
    return True


if __name__ == "__main__":
    asyncio.run(main())
