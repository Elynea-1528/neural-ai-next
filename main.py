#!/usr/bin/env python3
"""Neural AI Next - Unified CLI Entry Point.

Ez a modul a rendszer központi belépési pontja, amely egyesíti a live módot,
a történelmi adatok letöltését és a dashboard-t egy egységes CLI felületen keresztül.

Használat:
    python main.py live                    # Live mód indítása
    python main.py download --symbol EURUSD --start 2024-03-20 --end 2024-03-20
    python main.py dashboard               # Dashboard indítása
    python main.py dashboard --host 0.0.0.0 --port 8501 --server.headless True
"""

import argparse
import asyncio
import sys
from contextlib import suppress
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from neural_ai.core import get_core_components
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface

# Körkörös importok elkerüléséhez
if TYPE_CHECKING:
    from neural_ai.collectors.jforex.interfaces.live_interface import ILiveFeed
    from neural_ai.core.base.implementations.component_bundle import CoreComponents
    from neural_ai.core.db.implementations.sqlalchemy_session import DatabaseManager
    from neural_ai.core.events.interfaces.event_bus_interface import EventBusInterface
    from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
    from neural_ai.data.ingestion.market_data_persister import MarketDataPersister


async def run_live_mode() -> None:
    """Live mód indítása - az eredeti main logika.

    Ez a függvény felelős az alkalmazás teljes életciklusáért:
    1. Core komponensek inicializálása
    2. Szolgáltatások indítása (event bus, adatbázis)
    3. Örök futás biztosítása, amíg le nem állítják
    4. Hiba kezelése és naplózása

    Raises:
        SystemExit: Ha kritikus hiba történik az alkalmazás indítása során.
    """
    # Core komponensek inicializálása típusos változóval
    components: CoreComponents = get_core_components()

    # Komponensek lekérése
    logger: LoggerInterface | None = components.logger
    event_bus: EventBusInterface | None = components.event_bus
    database: DatabaseManager | None = components.database
    live_feed: ILiveFeed | None = components.live_feed
    persister: MarketDataPersister | None = components.persister

    try:
        if logger is not None:
            logger.info("Rendszer indítása", extra={"version": "0.5.0"})

        # Szolgáltatások indítása
        if event_bus is not None:
            await event_bus.start()

            # A FOGADÓ CIKLUS INDÍTÁSA - Ez felelős azért, hogy a Persister megkapja az eseményeket!
            asyncio.create_task(event_bus.run_forever())
            if logger is not None:
                logger.info("✅ EventBus Listener Loop elindítva (Background Task)")

        if database is not None:
            await database.initialize()

        # Adatmentő szolgálat indítása (Hogy ne vesszen el az adat!)
        if persister:
            await persister.start()
            if logger:
                logger.info("✅ MarketDataPersister elindítva")

        # Live feed indítása (ha elérhető)
        if live_feed is not None:
            await live_feed.start()
            if logger is not None:
                logger.info("✅ JForex Live Feed elindítva")

        if logger is not None:
            logger.info("Rendszer fut, eseményekre vár")

        # Örök futás (amíg nem jön Ctrl+C)
        # A suppress elnyeli a CancelledError-t leálláskor
        with suppress(asyncio.CancelledError):
            await asyncio.Event().wait()

    finally:
        # Szolgáltatások leállítása fordított sorrendben
        if logger is not None:
            logger.info("Rendszer leállítása...")

        # ELŐSZÖR a Persistert állítjuk le, hogy kiírja a buffert!
        if persister:
            await persister.stop()
            if logger:
                logger.info("✅ MarketDataPersister leállítva (Buffer kiírva)")

        if live_feed is not None:
            await live_feed.stop()
            if logger is not None:
                logger.info("✅ JForex Live Feed leállítva")

        if event_bus is not None:
            await event_bus.stop()
            if logger is not None:
                logger.info("✅ EventBus leállítva")

        if logger is not None:
            logger.info("✅ Rendszer leállítva")


async def run_download_mode(
    logger: LoggerInterface, symbol: str, start_date: datetime, end_date: datetime
) -> None:
    """Történelmi adatok letöltése a megadott tartományban.

    Args:
        logger: Logger példány a naplózáshoz
        symbol: A pénzpár szimbóluma (pl. 'EURUSD')
        start_date: A letöltés kezdő dátuma
        end_date: A letöltés záró dátuma
    """
    # Importáljuk a download_historical_data függvényt a scripts modulból
    from scripts.download_history import download_historical_data

    logger.info("=" * 60)
    logger.info("🧠 NEURAL AI NEXT - TÖRTÉNELMI ADAT LETÖLTŐ (CLI MODE)")
    logger.info("=" * 60)

    await download_historical_data(symbol, start_date, end_date)


def run_dashboard_mode(logger: LoggerInterface, host: str, port: int, headless: bool) -> None:
    """Dashboard indítása Streamlit-en keresztül.

    Args:
        logger: Logger példány a naplózáshoz
        host: A szerver hosztja (pl. 'localhost' vagy '0.0.0.0')
        port: A szerver portja (pl. 8501)
        headless: Ha True, headless módban fut (nincs browser automatikus megnyitása)
    """
    import subprocess

    # Streamlit parancs összeállítása a conda környezet abszolút útvonalával
    streamlit_cmd = [
        "/home/elynea/miniconda3/envs/neural-ai-next/bin/streamlit",
        "run",
        "neural_ai/ui/streamlit_app.py",
        "--server.address",
        host,
        "--server.port",
        str(port),
    ]

    # Headless mód hozzáadása, ha kérték
    if headless:
        streamlit_cmd.extend(["--server.headless", "true"])

    logger.info("=" * 60)
    logger.info("🧠 NEURAL AI NEXT - DASHBOARD")
    logger.info("=" * 60)
    logger.info(f"🌐 Hoszt: {host}")
    logger.info(f"🚪 Port: {port}")
    logger.info(f"👻 Headless: {'Igen' if headless else 'Nem'}")
    logger.info("⏳ Dashboard indítása...")

    try:
        # Streamlit indítása
        subprocess.run(streamlit_cmd, check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Hiba a Streamlit indításakor: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("🛑 Dashboard leállítva.")
        sys.exit(0)


def parse_arguments() -> argparse.Namespace:
    """Argumentumok feldolgozása.

    Returns:
        A feldolgozott argumentumok
    """
    parser = argparse.ArgumentParser(
        description="Neural AI Next - Unified CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Példák:
  %(prog)s live
  %(prog)s download --symbol EURUSD --start 2024-03-20 --end 2024-03-20
  %(prog)s dashboard
  %(prog)s dashboard --host 0.0.0.0 --port 8501 --headless
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Parancsok")

    # Live parancs
    subparsers.add_parser("live", help="Live mód indítása")

    # Download parancs
    download_parser = subparsers.add_parser("download", help="Történelmi adatok letöltése")
    download_parser.add_argument(
        "--symbol", type=str, required=True, help="A pénzpár szimbóluma (pl. EURUSD)"
    )
    download_parser.add_argument(
        "--start", type=str, required=True, help="A letöltés kezdő dátuma (YYYY-MM-DD formátumban)"
    )
    download_parser.add_argument(
        "--end", type=str, required=True, help="A letöltés záró dátuma (YYYY-MM-DD formátumban)"
    )

    # Dashboard parancs
    dashboard_parser = subparsers.add_parser("dashboard", help="Dashboard indítása")
    dashboard_parser.add_argument(
        "--host",
        type=str,
        default="localhost",
        help="A szerver hosztja (alapértelmezett: localhost)",
    )
    dashboard_parser.add_argument(
        "--port", type=int, default=8501, help="A szerver portja (alapértelmezett: 8501)"
    )
    dashboard_parser.add_argument(
        "--headless",
        action="store_true",
        help="Headless mód (nincs browser automatikus megnyitása)",
    )

    return parser.parse_args()


def parse_date(date_str: str) -> datetime:
    """Dátum string parse-olása.

    Args:
        date_str: Dátum string (YYYY-MM-DD formátumban)

    Returns:
        A parse-olt dátum UTC időzónával
    """
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=UTC)
    except ValueError as e:
        raise ValueError(
            f"Érvénytelen dátum formátum: {date_str}. Használd az YYYY-MM-DD formátumot."
        ) from e


def main() -> None:
    """Főprogram."""
    # Core komponensek inicializálása
    components = get_core_components()
    logger = components.logger

    # Logger kötelező a rendszer működéséhez
    assert logger is not None, "Logger is required but not initialized"

    args = parse_arguments()

    if args.command == "live":
        try:
            asyncio.run(run_live_mode())
        except KeyboardInterrupt:
            logger.info("🛑 Rendszer leállítva.")
        except Exception as e:
            logger.error(f"❌ Váratlan hiba: {e}")
            sys.exit(1)

    elif args.command == "download":
        # Dátumok parse-olása
        try:
            start_date = parse_date(args.start)
            end_date = parse_date(args.end).replace(hour=23, minute=59, second=59)
        except ValueError as e:
            logger.error(f"❌ {e}")
            sys.exit(1)

        # Ellenőrzések
        if start_date > end_date:
            logger.error("❌ A kezdő dátum nem lehet későbbi, mint a záró dátum")
            sys.exit(1)

        if start_date > datetime.now(UTC):
            logger.error("❌ A kezdő dátum nem lehet a jövőben")
            sys.exit(1)

        # Letöltés indítása
        try:
            asyncio.run(run_download_mode(logger, args.symbol.upper(), start_date, end_date))
        except KeyboardInterrupt:
            logger.warning("⚠️  Letöltés megszakítva a felhasználó által")
            sys.exit(130)
        except Exception as e:
            logger.error(f"❌ Váratlan hiba: {e}")
            sys.exit(1)

    elif args.command == "dashboard":
        # Dashboard indítása
        try:
            run_dashboard_mode(logger, args.host, args.port, args.headless)
        except KeyboardInterrupt:
            logger.info("🛑 Dashboard leállítva.")
        except Exception as e:
            logger.error(f"❌ Váratlan hiba: {e}")
            sys.exit(1)

    else:
        logger.error(
            "❌ Érvénytelen parancs. Használd 'live', 'download' vagy 'dashboard' parancsot."
        )
        logger.error("   Példa: python main.py live")
        logger.error(
            "   Példa: python main.py download --symbol EURUSD --start 2024-03-20 --end 2024-03-20"
        )
        logger.error("   Példa: python main.py dashboard")
        logger.error("   Példa: python main.py dashboard --host 0.0.0.0 --port 8501 --headless")
        sys.exit(1)


if __name__ == "__main__":
    main()
