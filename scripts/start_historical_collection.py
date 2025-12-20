#!/usr/bin/env python3
"""Historical Data Collection Script.
==================================

Ez a script lehetővé teszi a historikus adatgyűjtés indítását
parancssorból vagy más scriptekből.

Használat:
    python scripts/start_historical_collection.py [options]

Opciók:
    --auto-start          Automatikus indítás (ellenőrzi a hiányzó adatokat)
    --all-instruments     Minden instrumentumra indít
    --symbol SYMBOL       Csak adott szimbólumra indít
    --timeframe TF        Csak adott időkeretre indít
    --start-date DATE     Kezdő dátum (YYYY-MM-DD formátumban)
    --end-date DATE       Végdátum (YYYY-MM-DD formátumban)
    --batch-size DAYS     Kötegenkénti napok száma (alapértelmezett: 365)
    --priority LEVEL      Prioritás (low, normal, high)

Példák:
    # Automatikus indítás (ajánlott)
    python scripts/start_historical_collection.py --auto-start

    # Minden instrumentum indítása
    python scripts/start_historical_collection.py --all-instruments

    # Csak EURUSD M1 adatok
    python scripts/start_historical_collection.py --symbol EURUSD --timeframe M1

    # Egyéni dátumtartomány
    python scripts/start_historical_collection.py --start-date 2020-01-01 --end-date 2025-12-31

Author: Neural AI Team
Date: 2025-12-17
Version: 1.0.0
"""

import argparse
import asyncio
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from neural_ai.collectors.mt5.data_validator import DataValidator
from neural_ai.collectors.mt5.error_handler import ErrorHandler
from neural_ai.collectors.mt5.implementations.historical_data_manager import (
    HistoricalDataManager,
)
from neural_ai.collectors.mt5.implementations.storage.collector_storage import (
    CollectorStorage,
)
from neural_ai.core.logger.implementations.logger_factory import LoggerFactory


def setup_logger():
    """Logger beállítása."""
    return LoggerFactory.get_logger(
        name="HistoricalCollectionScript",
        logger_type="colored",
        log_level="INFO",
    )


def create_manager(logger):
    """HistoricalDataManager létrehozása."""
    # Storage inicializálása
    storage = CollectorStorage(base_path="data", logger=logger)

    # Validator inicializálása
    validator = DataValidator(logger=logger, enable_quality_framework=True)

    # ErrorHandler inicializálása
    error_handler = ErrorHandler(logger=logger)

    # HistoricalDataManager létrehozása
    manager = HistoricalDataManager(
        storage=storage,
        validator=validator,
        error_handler=error_handler,
        logger=logger,
    )

    return manager


async def auto_start_collection(logger):
    """Automatikus historikus adatgyűjtés indítása."""
    logger.info("=" * 60)
    logger.info("Automatikus historikus adatgyűjtés indítása")
    logger.info("=" * 60)

    try:
        manager = create_manager(logger)

        # Auto-start indítása
        result = manager.auto_start_historical_collection()

        if result["status"] == "started":
            logger.info("✅ Historikus adatgyűjtés sikeresen indítva")
            logger.info(f"   Létrehozott job-ok: {result['total_jobs']}")

            # Job-ok részleteinek kiírása
            for i, job in enumerate(result["jobs_created"], 1):
                logger.info(f"   {i}. Job ID: {job['job_id']}")
                logger.info(f"      Becsült időtartam: {job['estimated_duration']}")
                logger.info(f"      Összes köteg: {job['total_batches']}")

            return True

        elif result["status"] == "no_action":
            logger.info("ℹ️  Minden historikus adat megtalálható, nincs szükség indításra")
            return True

        else:
            logger.error(f"❌ Historikus adatgyűjtés indítása sikertelen: {result['message']}")
            return False

    except Exception as e:
        logger.error(f"❌ Hiba történt: {e}")
        import traceback

        traceback.print_exc()
        return False


async def start_all_instruments(
    logger, start_date=None, end_date=None, batch_size=365, priority="normal"
):
    """Historikus adatgyűjtés indítása minden instrumentumra."""
    logger.info("=" * 60)
    logger.info("Historikus adatgyűjtés indítása minden instrumentumra")
    logger.info("=" * 60)

    try:
        manager = create_manager(logger)

        # Minden instrumentum indítása
        result = manager.start_historical_collection_for_all_instruments()

        if result["status"] == "started":
            logger.info("✅ Historikus adatgyűjtés sikeresen indítva")
            logger.info(f"   Létrehozott job-ok: {result['total_jobs']}")
            logger.info(
                f"   Dátumtartomány: {result['date_range']['start']} - {result['date_range']['end']}"
            )

            return True
        else:
            logger.error(f"❌ Historikus adatgyűjtés indítása sikertelen: {result['message']}")
            return False

    except Exception as e:
        logger.error(f"❌ Hiba történt: {e}")
        import traceback

        traceback.print_exc()
        return False


async def start_specific_instrument(
    logger,
    symbol,
    timeframe=None,
    start_date=None,
    end_date=None,
    batch_size=365,
    priority="normal",
):
    """Historikus adatgyűjtés indítása adott instrumentumra."""
    logger.info("=" * 60)
    logger.info(f"Historikus adatgyűjtés indítása: {symbol}")
    if timeframe:
        logger.info(f"Időkeret: {timeframe}")
    logger.info("=" * 60)

    try:
        manager = create_manager(logger)

        # Alapértelmezett dátumtartomány
        if not end_date:
            end_date = datetime.now().isoformat()
        if not start_date:
            start_date = (datetime.now() - timedelta(days=5 * 365)).isoformat()

        if timeframe:
            # Csak egy instrumentum/timeframe kombináció
            result = manager.request_historical_data(
                symbol=symbol,
                timeframe=timeframe,
                start_date=start_date,
                end_date=end_date,
                batch_size=batch_size,
                priority=priority,
            )

            logger.info("✅ Historikus adatgyűjtés sikeresen létrehozva")
            logger.info(f"   Job ID: {result['job_id']}")
            logger.info(f"   Becsült időtartam: {result['estimated_duration']}")
            logger.info(f"   Összes köteg: {result['total_batches']}")

            return True
        else:
            # Minden időkeretre indítása az adott instrumentumnak

            timeframes = list(manager.storage.supported_timeframes.keys())
            jobs_created = []

            for tf in timeframes:
                result = manager.request_historical_data(
                    symbol=symbol,
                    timeframe=tf,
                    start_date=start_date,
                    end_date=end_date,
                    batch_size=batch_size,
                    priority=priority,
                )
                jobs_created.append(result)

            logger.info(
                f"✅ {len(jobs_created)} historikus job létrehozva a(z) {symbol} szimbólumhoz"
            )

            return True

    except Exception as e:
        logger.error(f"❌ Hiba történt: {e}")
        import traceback

        traceback.print_exc()
        return False


def parse_arguments():
    """Argumentumok feldolgozása."""
    parser = argparse.ArgumentParser(
        description="Historical Data Collection Script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    # Műveleti opciók
    parser.add_argument(
        "--auto-start",
        action="store_true",
        help="Automatikus indítás (ellenőrzi a hiányzó adatokat)",
    )
    parser.add_argument(
        "--all-instruments",
        action="store_true",
        help="Historikus adatgyűjtés indítása minden instrumentumra",
    )

    # Szűrő opciók
    parser.add_argument(
        "--symbol",
        type=str,
        help="Csak adott szimbólumra indít (pl. EURUSD)",
    )
    parser.add_argument(
        "--timeframe",
        type=str,
        help="Csak adott időkeretre indít (pl. M1, H1)",
    )

    # Dátum opciók
    parser.add_argument(
        "--start-date",
        type=str,
        help="Kezdő dátum (YYYY-MM-DD formátumban)",
    )
    parser.add_argument(
        "--end-date",
        type=str,
        help="Végdátum (YYYY-MM-DD formátumban)",
    )

    # Egyéb opciók
    parser.add_argument(
        "--batch-size",
        type=int,
        default=365,
        help="Kötegenkénti napok száma (alapértelmezett: 365)",
    )
    parser.add_argument(
        "--priority",
        type=str,
        default="normal",
        choices=["low", "normal", "high"],
        help="Prioritás (alapértelmezett: normal)",
    )

    return parser.parse_args()


async def main():
    """Főprogram."""
    # Logger beállítása
    logger = setup_logger()

    # Argumentumok feldolgozása
    args = parse_arguments()

    try:
        # Művelet végrehajtása
        if args.auto_start:
            success = await auto_start_collection(logger)
        elif args.all_instruments:
            success = await start_all_instruments(
                logger,
                start_date=args.start_date,
                end_date=args.end_date,
                batch_size=args.batch_size,
                priority=args.priority,
            )
        elif args.symbol:
            success = await start_specific_instrument(
                logger,
                symbol=args.symbol,
                timeframe=args.timeframe,
                start_date=args.start_date,
                end_date=args.end_date,
                batch_size=args.batch_size,
                priority=args.priority,
            )
        else:
            logger.error(
                "❌ Nincs megadva művelet! Használd --auto-start, --all-instruments vagy --symbol"
            )
            logger.info("Használd --help a súgó megjelenítéséhez")
            return 1

        if success:
            logger.info("=" * 60)
            logger.info("✅ A művelet sikeresen befejeződött")
            logger.info("=" * 60)
            return 0
        else:
            logger.info("=" * 60)
            logger.error("❌ A művelet sikertelen")
            logger.info("=" * 60)
            return 1

    except KeyboardInterrupt:
        logger.info("\n⚠️  Művelet megszakítva a felhasználó által")
        return 130
    except Exception as e:
        logger.error(f"❌ Váratlan hiba: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
