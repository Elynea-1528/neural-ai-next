#!/usr/bin/env python3
"""Neural AI Next - Fő indító szkript.

Ez a szkript inicializálja a teljes kereskedési ökoszisztémát:
1. DI Container
2. Adatbázis kapcsolat
3. Event Bus
4. Konfiguráció betöltése
5. Szolgáltatások indítása
6. Örök futás
"""

import asyncio
import sys
from pathlib import Path

# Project root hozzáadása a Python path-hoz
sys.path.insert(0, str(Path(__file__).parent))

import structlog
from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# Importok az új architektúra szerint
from neural_ai.core.events.factory import EventBusFactory
from neural_ai.core.storage.factory import StorageFactory
from neural_ai.core.db.factory import DatabaseFactory
from neural_ai.core.logger.factory import LoggerFactory

logger = structlog.get_logger("neural_ai.bootstrap")


class StaticConfig(BaseSettings):
    """Statikus konfiguráció (lásd: docs/planning/specs/02_dynamic_configuration.md)."""

    app_env: str = "development"
    log_level: str = "INFO"
    db_url: str = "sqlite+aiosqlite:///neural_ai.db"
    trading_symbols: list = ["EURUSD", "XAUUSD", "GBPUSD", "USDJPY", "USDCHF"]
    data_base_path: str = "/data/tick"
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    class Config:
        """Pydantic konfiguráció osztály."""

        env_file = ".env"
        env_file_encoding = "utf-8"


def setup_logging(config: StaticConfig) -> None:
    """Logging rendszer konfigurálása structlog-gal.
    
    Args:
        config: A statikus konfiguráció objektum.
    """
    logger.info("logging_setup_started", log_level=config.log_level)
    
    # Structlog konfiguráció
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(config.log_level),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=False,
    )
    
    # Standard logging konfigurálása
    LoggerFactory.configure({
        'default_level': config.log_level,
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        'date_format': '%Y-%m-%d %H:%M:%S',
        'handlers': {
            'console': {
                'enabled': True,
                'level': config.log_level
            }
        }
    })
    
    logger.info("logging_setup_completed")




async def setup_database(config: StaticConfig):
    """Adatbázis kapcsolat és session factory létrehozása a DatabaseFactory használatával."""
    logger.info("database_setup_started", db_url=config.db_url)

    try:
        # Session maker létrehozása a DatabaseFactory segítségével
        async_session_maker = DatabaseFactory.get_session_maker()
        
        logger.info("database_setup_completed")
        return async_session_maker

    except Exception as e:
        logger.error("database_setup_failed", error=str(e))
        raise


async def setup_event_bus(config: StaticConfig):
    """Event Bus inicializálása az EventBusFactory használatával."""
    logger.info("event_bus_setup_started")

    try:
        # EventBus létrehozása és indítása a factory segítségével
        event_bus = await EventBusFactory.create_and_start()
        
        logger.info("event_bus_setup_completed")
        return event_bus

    except Exception as e:
        logger.error("event_bus_setup_failed", error=str(e))
        raise


async def setup_storage_service(config: StaticConfig):
    """Tároló szolgáltatás inicializálása a StorageFactory használatával."""
    logger.info("storage_service_setup_started", path=config.data_base_path)

    try:
        # Storage létrehozása a factory segítségével
        storage = StorageFactory.get_storage(
            storage_type="file",
            base_path=config.data_base_path
        )
        
        logger.info("storage_service_setup_completed")
        return storage

    except Exception as e:
        logger.error("storage_service_setup_failed", error=str(e))
        raise


async def setup_collectors(config: StaticConfig, event_bus):
    """Adatgyűjtők inicializálása."""
    logger.info("collectors_setup_started")

    try:
        # TODO: JForex, MT5, IBKR collectorok (lásd: docs/planning/specs/05_collectors_strategy.md)
        # jforex_collector = Bi5Downloader(symbols=config.trading_symbols)
        # mt5_collector = MT5Collector(event_bus=event_bus)

        logger.info("collectors_setup_completed")
        return []

    except Exception as e:
        logger.error("collectors_setup_failed", error=str(e))
        raise


async def setup_strategy_engine(config: StaticConfig, event_bus, db_session):
    """Stratégia motor inicializálása."""
    logger.info("strategy_engine_setup_started")

    try:
        # TODO: Strategy Engine implementáció
        # strategy_engine = StrategyEngine(
        #     event_bus=event_bus,
        #     db_session=db_session
        # )

        logger.info("strategy_engine_setup_completed")
        return None

    except Exception as e:
        logger.error("strategy_engine_setup_failed", error=str(e))
        raise


async def start_services(services: list):
    """Szolgáltatások indítása."""
    logger.info("services_startup_started", count=len(services))

    try:
        for service in services:
            # TODO: Minden szolgáltatás start() metódussal rendelkezik
            # await service.start()
            logger.debug("service_started", service=type(service).__name__)

        logger.info("services_startup_completed")

    except Exception as e:
        logger.error("services_startup_failed", error=str(e))
        raise


async def health_check() -> bool:
    """Health check a rendszer állapotáról."""
    try:
        # TODO: Komponensek állapotának ellenőrzése
        logger.debug("health_check_passed")
        return True

    except Exception as e:
        logger.error("health_check_failed", error=str(e))
        return False


async def graceful_shutdown(signum, frame):
    """Elegáns leállítás."""
    logger.info("shutdown_initiated", signal=signum)

    try:
        # TODO: Minden szolgáltatás stop() metódussal rendelkezik
        # await asyncio.gather(*[s.stop() for s in services])

        logger.info("shutdown_completed")
        sys.exit(0)

    except Exception as e:
        logger.error("shutdown_failed", error=str(e))
        sys.exit(1)


async def main():
    """Fő alkalmazás belépési pont."""
    logger.info("application_starting", version="1.0.0")

    try:
        # 1. Konfiguráció betöltése
        logger.info("loading_configuration")
        config = StaticConfig()
        logger.info("configuration_loaded", app_env=config.app_env)
        
        # 2. Logging rendszer konfigurálása
        setup_logging(config)

        # 3. DI Container inicializálása
        logger.info("initializing_di_container")
        # container = DIContainer()
        # container.register_singleton(StaticConfig, config)

        # 4. Adatbázis kapcsolat
        db_session_maker = await setup_database(config)
        # container.register_singleton(sessionmaker, db_session_maker)

        # 5. Event Bus
        event_bus = await setup_event_bus(config)
        # container.register_singleton(EventBus, event_bus)

        # 6. Tároló szolgáltatás
        storage_service = await setup_storage_service(config)
        # container.register_singleton(ParquetStorageService, storage_service)

        # 7. Adatgyűjtők
        collectors = await setup_collectors(config, event_bus)

        # 8. Stratégia motor
        strategy_engine = await setup_strategy_engine(config, event_bus, db_session_maker)

        # 9. Összes szolgáltatás összegyűjtése
        all_services = collectors + [strategy_engine] if strategy_engine else collectors

        # 10. Szolgáltatások indítása
        await start_services(all_services)

        # 11. Health check
        if not await health_check():
            logger.error("health_check_failed_on_startup")
            sys.exit(1)

        # 12. Alkalmazás sikeresen elindult
        logger.info(
            "application_started",
            app_env=config.app_env,
            symbols=config.trading_symbols,
            api_url=f"http://{config.api_host}:{config.api_port}",
        )

        # 13. Örök futás (vagy amíg nem kapunk kill signal-t)
        await asyncio.Event().wait()

    except KeyboardInterrupt:
        logger.info("keyboard_interrupt_received")

    except Exception as e:
        logger.error("application_startup_failed", error=str(e), exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    """Entry point."""

    # Signal kezelés (elegáns leállításhoz)
    import signal

    signal.signal(signal.SIGTERM, lambda s, f: asyncio.create_task(graceful_shutdown(s, f)))
    signal.signal(signal.SIGINT, lambda s, f: asyncio.create_task(graceful_shutdown(s, f)))

    # Fő alkalmazás indítása
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("application_stopped_by_user")
    except Exception as e:
        logger.error("application_crashed", error=str(e), exc_info=True)
        sys.exit(1)
