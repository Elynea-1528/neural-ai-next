#!/usr/bin/env python3
"""Tömeges tick adat letöltő script a Neural AI Next rendszerhez.

Ez a script lehetővé teszi a tick adatok tömeges letöltését a JForex adatforrásból
egy megadott dátumtartományban. A letöltött adatok automatikusan elmentésre kerülnek
a Parquet tárolóba a MarketDataPersister által.

Használat:
    python scripts/download_history.py --symbol EURUSD --start 2023-01-01 --end 2023-12-31

Author: Neural AI Next Team
Version: 1.0.0
"""

import argparse
import asyncio
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path

# Hozzáadjuk a projekt gyökerét a Python path-hoz
sys.path.insert(0, str(Path(__file__).parent.parent))

from neural_ai.collectors.jforex.exceptions.jforex_error import (
    DataNotAvailableError,
    DecodeError,
    DownloadError,
)
from neural_ai.collectors.jforex.factory import JForexFactory
from neural_ai.core import bootstrap_core


async def download_historical_data(symbol: str, start_date: datetime, end_date: datetime) -> None:
    """Történelmi tick adatok letöltése a megadott tartományban.

    Args:
        symbol: A pénzpár szimbóluma (pl. 'EURUSD')
        start_date: A letöltés kezdő dátuma
        end_date: A letöltés záró dátuma
    """
    print("🚀 Történelmi adat letöltés indítása...")
    print(f"   Szimbólum: {symbol}")
    print(f"   Dátumtartomány: {start_date.date()} - {end_date.date()}")
    print()

    # Rendszer inicializálása
    print("⏳ Rendszer inicializálása...")
    try:
        # Bootstrap a core komponensekkel
        core = bootstrap_core()
        logger = core.logger
        event_bus = core.event_bus
        market_data_persister = core.persister  # A bootstrap már tartalmazza!

        # Biztonsági ellenőrzés: data/tick mappa létezik-e
        data_dir = Path("data/tick")
        data_dir.mkdir(parents=True, exist_ok=True)
        print(f"   ✅ Data directory: {data_dir.absolute()}")

        # EventBus indítása (ELŐSZÖR!)
        if event_bus:
            await event_bus.start()
            if logger:
                logger.info("EventBus elindítva")

            # FONTOS: EventBus event loop indítása külön task-ban!
            asyncio.create_task(event_bus.run_forever())
            if logger:
                logger.info("EventBus event loop elindítva")

        # FONTOS: MarketDataPersister explicit indítása (A DOWNLOADER ELŐTT!)
        if market_data_persister:
            await market_data_persister.start()
            if logger:
                logger.info("MarketDataPersister elindítva")
        else:
            print("⚠️  Figyelmeztetés: MarketDataPersister nem érhető el!")

    except Exception as e:
        print(f"❌ Hiba a rendszer inicializálásakor: {e}")
        return

    # Bi5Downloader létrehozása
    try:
        if not core.config:
            raise RuntimeError("Config nincs elérhető")
        if not logger:
            raise RuntimeError("Logger nincs elérhető")
        if not event_bus:
            raise RuntimeError("EventBus nincs elérhető")

        downloader = JForexFactory.create_downloader(
            config=core.config,
            logger=logger,
            event_bus=event_bus,
            storage=core.storage,  # <--- EZT A SORT SZÚRD BE!
        )
        logger.info("Bi5Downloader létrehozva")
    except Exception as e:
        print(f"❌ Hiba a Bi5Downloader létrehozásakor: {e}")
        if event_bus:
            await event_bus.stop()
        return

    # Dátumok generálása
    current_date = start_date
    total_days = (end_date - start_date).days + 1
    successful_downloads = 0
    failed_downloads = 0
    skipped_downloads = 0

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

        while current_hour <= end_hour:
            try:
                print(
                    f"   📥 [{day_count}/{total_days}] Letöltés: "
                    f"{current_hour.strftime('%Y-%m-%d %H:%M')}"
                )

                ticks = await downloader.download_tick_data(symbol, current_hour)

                if ticks:
                    hours_downloaded += 1
                    print(f"      ✅ {len(ticks)} tick letöltve")
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
            print(f"   ✅ Nap összesítve: {hours_downloaded} óra sikeresen letöltve")
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
    print()

    # KRITIKUS LÉPÉS: FLUSH ÉS STOP (EZ HIÁNYZOTT!)
    print("⏳ Adatok véglegesítése (FORCE FLUSH)...")
    try:
        # 1. MarketDataPersister leállítása (ez kiüríti a buffert)
        if market_data_persister:
            await market_data_persister.stop()
            if logger:
                logger.info("MarketDataPersister leállítva, buffer kiürítve")
            print("   ✅ MarketDataPersister buffer kiürítve")

        # 2. EventBus leállítása
        if event_bus:
            await event_bus.stop()
            if logger:
                logger.info("EventBus leállítva")
            print("   ✅ EventBus leállítva")

        print("✅ Összes adat kiírva a lemezre!")

    except Exception as e:
        print(f"⚠️  Hiba a rendszer leállításakor: {e}")


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
    print("🧠 NEURAL AI NEXT - TÖRTÉNELMI ADAT LETÖLTŐ")
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
