#!/usr/bin/env python3
"""Tömeges tick adat letöltő script a Neural AI Next rendszerhez (DIRECT STORAGE MODE).

Ez a script lehetővé teszi a tick adatok tömeges letöltését a JForex adatforrásból
egy megadott dátumtartományban. A letöltött adatok közvetlenül a ParquetStorageService
által kerülnek mentésre, kikerülve az EventBus-t a maximális sebesség érdekében.

Használat:
    python scripts/download_history.py --symbol EURUSD --start 2023-01-01 --end 2023-12-31

Author: Neural AI Next Team
Version: 2.0.0 (Direct Storage Mode)
"""

import argparse
import asyncio
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import TYPE_CHECKING

import polars as pl

# Hozzáadjuk a projekt gyökerét a Python path-hoz
sys.path.insert(0, str(Path(__file__).parent.parent))

from neural_ai.collectors.jforex.exceptions.jforex_error import (
    DataNotAvailableError,
    DecodeError,
    DownloadError,
)
from neural_ai.collectors.jforex.factory import JForexFactory
from neural_ai.core import bootstrap_core

if TYPE_CHECKING:
    from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
    from neural_ai.core.storage.interfaces.storage_interface import StorageInterface


async def download_historical_data(symbol: str, start_date: datetime, end_date: datetime) -> None:
    """Történelmi tick adatok letöltése a megadott tartományban (Direct Storage Mode).

    Args:
        symbol: A pénzpár szimbóluma (pl. 'EURUSD')
        start_date: A letöltés kezdő dátuma
        end_date: A letöltés záró dátuma
    """
    print("🚀 Történelmi adat letöltés indítása (DIRECT STORAGE MODE)...")
    print(f"   Szimbólum: {symbol}")
    print(f"   Dátumtartomány: {start_date.date()} - {end_date.date()}")
    print()

    # Rendszer inicializálása
    print("⏳ Rendszer inicializálása...")
    try:
        # Bootstrap a core komponensekkel
        core = bootstrap_core()
        logger = core.logger
        storage = core.storage

        # Debug: Ellenőrizzük, hogy a storage létezik-e
        print(f"   ✅ Storage: {storage is not None} (type: {type(storage)})")
        if storage is None:
            print("   ❌ Hiba: Storage None!")
            return

        # Biztonsági ellenőrzés: data/tick mappa létezik-e
        data_dir = Path("data/tick")
        data_dir.mkdir(parents=True, exist_ok=True)
        print(f"   ✅ Data directory: {data_dir.absolute()}")

    except Exception as e:
        print(f"❌ Hiba a rendszer inicializálásakor: {e}")
        return

    # Bi5Downloader létrehozása
    try:
        if not core.config:
            raise RuntimeError("Config nincs elérhető")
        if not logger:
            raise RuntimeError("Logger nincs elérhető")

        # Létrehozzuk a downloader-t, de NEM indítjuk el az EventBus-t
        downloader = JForexFactory.create_downloader(
            config=core.config,
            logger=logger,
            event_bus=None,  # Nincs EventBus, Direct Storage mód
            storage=storage,
        )
        logger.info("Bi5Downloader létrehozva (Direct Storage Mode)")
    except Exception as e:
        print(f"❌ Hiba a Bi5Downloader létrehozásakor: {e}")
        return

    # Dátumok generálása
    current_date = start_date
    total_days = (end_date - start_date).days + 1
    successful_downloads = 0
    failed_downloads = 0
    skipped_downloads = 0
    total_ticks = 0

    print(f"📅 Összesen {total_days} nap adatának letöltése...")
    print()

    # Letöltés naponként
    day_count = 0
    while current_date <= end_date:
        day_count += 1

        # Minden napon belül óránkénti letöltés
        current_hour = current_date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_hour = current_date.replace(hour=23, minute=0, second=0, microsecond=0)

        hours_downloaded = 0
        hours_failed = 0
        day_ticks = 0

        while current_hour <= end_hour:
            try:
                print(
                    f"   📥 [{day_count}/{total_days}] Letöltés: "
                    f"{current_hour.strftime('%Y-%m-%d %H:%M')}"
                )

                ticks = await downloader.download_tick_data(symbol, current_hour)

                if ticks:
                    hours_downloaded += 1
                    day_ticks += len(ticks)
                    total_ticks += len(ticks)
                    print(f"      ✅ {len(ticks)} tick letöltve")

                    # DIRECT STORAGE: Az adatokat közvetlenül a storage-ba mentjük
                    await _save_ticks_direct(storage, symbol, ticks, current_hour, logger)

                else:
                    print("      ⚠️  Nincs adat ehhez az órához")
                    skipped_downloads += 1

            except DataNotAvailableError:
                print("      ⚠️  Adat nem elérhető ehhez az órához")
                hours_failed += 1
                skipped_downloads += 1

            except (DownloadError, DecodeError) as e:
                print(f"      ❌ Hiba a letöltéskor: {e}")
                hours_failed += 1
                failed_downloads += 1

            except Exception as e:
                print(f"      ❌ Váratlan hiba: {e}")
                hours_failed += 1
                failed_downloads += 1

            # Következő óra
            current_hour += timedelta(hours=1)

        # Statisztika a napról
        if hours_downloaded > 0:
            successful_downloads += 1
            print(f"   ✅ Nap összesítve: {hours_downloaded} óra, {day_ticks} tick")
        else:
            print("   ⚠️  Nap összesítve: Nincs elérhető adat")

        if hours_failed > 0:
            print(f"   ❌ Nap összesítve: {hours_failed} óra sikertelen")

        print()

        # Következő nap
        current_date += timedelta(days=1)

    # Összesített statisztika
    print("=" * 60)
    print("📊 LETÖLTÉS BEFEJEZVE - ÖSSZESÍTÉS")
    print("=" * 60)
    print(f"✅ Sikeres napok: {successful_downloads}/{total_days}")
    print(f"❌ Sikertelen napok: {failed_downloads}/{total_days}")
    print(f"⚠️  Kihagyott órák: {skipped_downloads}")
    print(f"📈 Összes tick: {total_ticks}")
    print()

    # LEÁLLÍTÁSI SZEKVENCIA (Egyszerűbb, mert nincs EventBus)
    print("⏳ Rendszer leállítása (CLEANUP)...")
    try:
        # 1. Downloader lezárása (hálózat)
        if "downloader" in locals():
            await downloader.close()
            if logger:
                logger.info("Bi5Downloader lezárva")
            print("   ✅ Bi5Downloader lezárva")

        print("✅ Összes erőforrás tisztán lezárva!")

    except Exception as e:
        print(f"⚠️  Hiba a rendszer leállításakor: {e}")


async def _save_ticks_direct(
    storage: "StorageInterface",
    symbol: str,
    ticks: list,
    date: datetime,
    logger: "LoggerInterface | None" = None,
) -> None:
    """Tick adatok közvetlen mentése a storage-ba (Direct Storage Mode).

    Args:
        storage: A storage interfész
        symbol: A pénzpár szimbóluma
        ticks: A tick adatok listája
        date: A dátum
        logger: A logger (opcionális)
    """
    if not ticks:
        return

    try:
        # Tick adatok konvertálása Polars DataFrame-re
        tick_dicts = [
            {
                "timestamp": tick.timestamp,
                "bid": tick.bid,
                "ask": tick.ask,
                "ask_volume": tick.ask_volume if tick.ask_volume is not None else 0.0,
                "bid_volume": tick.bid_volume if tick.bid_volume is not None else 0.0,
                "source": tick.source,
            }
            for tick in ticks
        ]

        df = pl.DataFrame(tick_dicts)

        # Technikai 'volume' oszlop hozzáadása
        df = df.with_columns((pl.col("ask_volume") + pl.col("bid_volume")).alias("volume"))

        # Dátum formázása a fájlnévhez
        date_str = date.strftime("%Y%m%d")
        time_suffix = date.strftime("%H0000")

        # DIRECT STORAGE: Az adatokat közvetlenül a storage.store_tick_data-val mentjük
        await storage.store_tick_data(symbol=symbol, data=df, date=date, unique_id=time_suffix)

        print(f"   ✅ {len(ticks)} tick mentve -> {symbol}_{date_str}_{time_suffix}.parquet")

        if logger:
            logger.debug(
                "Ticks saved directly to storage",
                symbol=symbol,
                date=date.isoformat(),
                count=len(ticks),
            )

    except Exception as e:
        error_msg = f"Hiba a tick adatok mentésekor: {e}"
        print(f"      ❌ {error_msg}")
        if logger:
            logger.error(error_msg, symbol=symbol, date=date.isoformat(), error=str(e))


def parse_arguments() -> tuple[str, datetime, datetime]:
    """Argumentumok feldolgozása.

    Returns:
        A feldolgozott argumentumok: (symbol, start_date, end_date)
    """
    parser = argparse.ArgumentParser(description="Történelmi tick adatok letöltése JForex-ről")

    parser.add_argument(
        "--symbol", type=str, required=True, help="A pénzpár szimbóluma (pl. EURUSD)"
    )

    parser.add_argument(
        "--start", type=str, required=True, help="A letöltés kezdő dátuma (YYYY-MM-DD formátumban)"
    )

    parser.add_argument(
        "--end", type=str, required=True, help="A letöltés záró dátuma (YYYY-MM-DD formátumban)"
    )

    args = parser.parse_args()

    # Dátumok parse-olása
    try:
        start_date = datetime.strptime(args.start, "%Y-%m-%d").replace(tzinfo=UTC)
        end_date = datetime.strptime(args.end, "%Y-%m-%d").replace(
            hour=23, minute=59, second=59, tzinfo=UTC
        )
    except ValueError as e:
        print(f"❌ Érvénytelen dátum formátum: {e}")
        print("   Használd az YYYY-MM-DD formátumot (pl. 2023-01-01)")
        sys.exit(1)

    # Ellenőrzések
    if start_date > end_date:
        print("❌ A kezdő dátum nem lehet későbbi, mint a záró dátum")
        sys.exit(1)

    if start_date > datetime.now(UTC):
        print("❌ A kezdő dátum nem lehet a jövőben")
        sys.exit(1)

    return args.symbol.upper(), start_date, end_date


def main() -> None:
    """Főprogram."""
    print("=" * 60)
    print("🧠 NEURAL AI NEXT - TÖRTÉNELMI ADAT LETÖLTŐ (DIRECT STORAGE MODE)")
    print("=" * 60)
    print()

    # Argumentumok feldolgozása
    symbol, start_date, end_date = parse_arguments()

    # Letöltés indítása
    try:
        asyncio.run(download_historical_data(symbol, start_date, end_date))
    except KeyboardInterrupt:
        print()
        print("⚠️  Letöltés megszakítva a felhasználó által")
        sys.exit(130)
    except Exception as e:
        print(f"❌ Váratlan hiba: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
