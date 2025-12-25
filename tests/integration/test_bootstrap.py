#!/usr/bin/env python3
"""Integrációs teszt a main.py szkript indításához.

Ez a tesztmodul ellenőrzi a fő alkalmazás belépési pontjának megfelelő működését.
A teszt mockolja az asyncio.Event().wait() hívást, hogy ne fusson örökké.
"""

import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# Project root hozzáadása a Python path-hoz
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Importáljuk a main modult
import main


class TestMainBootstrap:
    """Tesztosztály a main.py szkript indítási folyamatához."""

    @pytest.mark.asyncio
    async def test_main_function_exists(self) -> None:
        """Teszteli, hogy a main függvény létezik-e."""
        assert hasattr(main, "main")
        assert callable(main.main)

    @pytest.mark.asyncio
    async def test_main_function_is_coroutine(self) -> None:
        """Teszteli, hogy a main függvény async függvény-e."""
        import inspect
        assert inspect.iscoroutinefunction(main.main)

    @pytest.mark.asyncio
    async def test_main_calls_config_loading(self) -> None:
        """Teszteli, hogy a main függvény betölti a konfigurációt."""
        with patch.object(main, "StaticConfig") as mock_config:
            with patch.object(main, "setup_logging") as mock_setup_logging:
                with patch.object(main, "setup_database") as mock_setup_database:
                    with patch.object(main, "setup_event_bus") as mock_setup_event_bus:
                        with patch.object(main, "setup_storage_service") as mock_setup_storage:
                            with patch.object(main, "setup_collectors") as mock_setup_collectors:
                                with patch.object(main, "setup_strategy_engine") as mock_setup_strategy:
                                    with patch.object(main, "start_services") as mock_start_services:
                                        with patch.object(main, "health_check", return_value=True) as mock_health_check:
                                            # Mockoljuk az asyncio.Event().wait()-et, hogy ne várjon örökké
                                            with patch("asyncio.Event") as mock_event:
                                                mock_event_instance = MagicMock()
                                                mock_event.return_value = mock_event_instance
                                                mock_event_instance.wait = AsyncMock()

                                                # Hívjuk meg a main függvényt
                                                await main.main()

                                                # Ellenőrizzük, hogy a konfiguráció betöltésre került-e
                                                mock_config.assert_called_once()

    @pytest.mark.asyncio
    async def test_main_calls_setup_logging(self) -> None:
        """Teszteli, hogy a main függvény meghívja a logging setup-ot."""
        with patch.object(main, "StaticConfig") as mock_config:
            mock_config.return_value = MagicMock(
                app_env="test",
                log_level="INFO",
                db_url="sqlite+aiosqlite:///test.db",
                trading_symbols=["EURUSD"],
                data_base_path="/tmp/test",
                api_host="0.0.0.0",
                api_port=8000
            )
            with patch.object(main, "setup_logging") as mock_setup_logging:
                with patch.object(main, "setup_database") as mock_setup_database:
                    with patch.object(main, "setup_event_bus") as mock_setup_event_bus:
                        with patch.object(main, "setup_storage_service") as mock_setup_storage:
                            with patch.object(main, "setup_collectors") as mock_setup_collectors:
                                with patch.object(main, "setup_strategy_engine") as mock_setup_strategy:
                                    with patch.object(main, "start_services") as mock_start_services:
                                        with patch.object(main, "health_check", return_value=True) as mock_health_check:
                                            with patch("asyncio.Event") as mock_event:
                                                mock_event_instance = MagicMock()
                                                mock_event.return_value = mock_event_instance
                                                mock_event_instance.wait = AsyncMock()

                                                await main.main()

                                                # Ellenőrizzük, hogy a logging setup meghívásra került
                                                mock_setup_logging.assert_called_once()

    @pytest.mark.asyncio
    async def test_main_calls_database_setup(self) -> None:
        """Teszteli, hogy a main függvény meghívja az adatbázis setup-ot."""
        with patch.object(main, "StaticConfig") as mock_config:
            mock_config.return_value = MagicMock(
                app_env="test",
                log_level="INFO",
                db_url="sqlite+aiosqlite:///test.db",
                trading_symbols=["EURUSD"],
                data_base_path="/tmp/test",
                api_host="0.0.0.0",
                api_port=8000
            )
            with patch.object(main, "setup_logging"):
                with patch.object(main, "setup_database") as mock_setup_database:
                    with patch.object(main, "setup_event_bus") as mock_setup_event_bus:
                        with patch.object(main, "setup_storage_service") as mock_setup_storage:
                            with patch.object(main, "setup_collectors") as mock_setup_collectors:
                                with patch.object(main, "setup_strategy_engine") as mock_setup_strategy:
                                    with patch.object(main, "start_services") as mock_start_services:
                                        with patch.object(main, "health_check", return_value=True) as mock_health_check:
                                            with patch("asyncio.Event") as mock_event:
                                                mock_event_instance = MagicMock()
                                                mock_event.return_value = mock_event_instance
                                                mock_event_instance.wait = AsyncMock()

                                                await main.main()

                                                # Ellenőrizzük, hogy az adatbázis setup meghívásra került
                                                mock_setup_database.assert_called_once()

    @pytest.mark.asyncio
    async def test_main_calls_event_bus_setup(self) -> None:
        """Teszteli, hogy a main függvény meghívja az event bus setup-ot."""
        with patch.object(main, "StaticConfig") as mock_config:
            mock_config.return_value = MagicMock(
                app_env="test",
                log_level="INFO",
                db_url="sqlite+aiosqlite:///test.db",
                trading_symbols=["EURUSD"],
                data_base_path="/tmp/test",
                api_host="0.0.0.0",
                api_port=8000
            )
            with patch.object(main, "setup_logging"):
                with patch.object(main, "setup_database"):
                    with patch.object(main, "setup_event_bus") as mock_setup_event_bus:
                        with patch.object(main, "setup_storage_service") as mock_setup_storage:
                            with patch.object(main, "setup_collectors") as mock_setup_collectors:
                                with patch.object(main, "setup_strategy_engine") as mock_setup_strategy:
                                    with patch.object(main, "start_services") as mock_start_services:
                                        with patch.object(main, "health_check", return_value=True) as mock_health_check:
                                            with patch("asyncio.Event") as mock_event:
                                                mock_event_instance = MagicMock()
                                                mock_event.return_value = mock_event_instance
                                                mock_event_instance.wait = AsyncMock()

                                                await main.main()

                                                # Ellenőrizzük, hogy az event bus setup meghívásra került
                                                mock_setup_event_bus.assert_called_once()

    @pytest.mark.asyncio
    async def test_main_calls_storage_service_setup(self) -> None:
        """Teszteli, hogy a main függvény meghívja a storage service setup-ot."""
        with patch.object(main, "StaticConfig") as mock_config:
            mock_config.return_value = MagicMock(
                app_env="test",
                log_level="INFO",
                db_url="sqlite+aiosqlite:///test.db",
                trading_symbols=["EURUSD"],
                data_base_path="/tmp/test",
                api_host="0.0.0.0",
                api_port=8000
            )
            with patch.object(main, "setup_logging"):
                with patch.object(main, "setup_database"):
                    with patch.object(main, "setup_event_bus"):
                        with patch.object(main, "setup_storage_service") as mock_setup_storage:
                            with patch.object(main, "setup_collectors") as mock_setup_collectors:
                                with patch.object(main, "setup_strategy_engine") as mock_setup_strategy:
                                    with patch.object(main, "start_services") as mock_start_services:
                                        with patch.object(main, "health_check", return_value=True) as mock_health_check:
                                            with patch("asyncio.Event") as mock_event:
                                                mock_event_instance = MagicMock()
                                                mock_event.return_value = mock_event_instance
                                                mock_event_instance.wait = AsyncMock()

                                                await main.main()

                                                # Ellenőrizzük, hogy a storage service setup meghívásra került
                                                mock_setup_storage.assert_called_once()

    @pytest.mark.asyncio
    async def test_main_calls_collectors_setup(self) -> None:
        """Teszteli, hogy a main függvény meghívja a collectors setup-ot."""
        with patch.object(main, "StaticConfig") as mock_config:
            mock_config.return_value = MagicMock(
                app_env="test",
                log_level="INFO",
                db_url="sqlite+aiosqlite:///test.db",
                trading_symbols=["EURUSD"],
                data_base_path="/tmp/test",
                api_host="0.0.0.0",
                api_port=8000
            )
            with patch.object(main, "setup_logging"):
                with patch.object(main, "setup_database"):
                    with patch.object(main, "setup_event_bus"):
                        with patch.object(main, "setup_storage_service"):
                            with patch.object(main, "setup_collectors") as mock_setup_collectors:
                                with patch.object(main, "setup_strategy_engine") as mock_setup_strategy:
                                    with patch.object(main, "start_services") as mock_start_services:
                                        with patch.object(main, "health_check", return_value=True) as mock_health_check:
                                            with patch("asyncio.Event") as mock_event:
                                                mock_event_instance = MagicMock()
                                                mock_event.return_value = mock_event_instance
                                                mock_event_instance.wait = AsyncMock()

                                                await main.main()

                                                # Ellenőrizzük, hogy a collectors setup meghívásra került
                                                mock_setup_collectors.assert_called_once()

    @pytest.mark.asyncio
    async def test_main_calls_strategy_engine_setup(self) -> None:
        """Teszteli, hogy a main függvény meghívja a strategy engine setup-ot."""
        with patch.object(main, "StaticConfig") as mock_config:
            mock_config.return_value = MagicMock(
                app_env="test",
                log_level="INFO",
                db_url="sqlite+aiosqlite:///test.db",
                trading_symbols=["EURUSD"],
                data_base_path="/tmp/test",
                api_host="0.0.0.0",
                api_port=8000
            )
            with patch.object(main, "setup_logging"):
                with patch.object(main, "setup_database"):
                    with patch.object(main, "setup_event_bus"):
                        with patch.object(main, "setup_storage_service"):
                            with patch.object(main, "setup_collectors"):
                                with patch.object(main, "setup_strategy_engine") as mock_setup_strategy:
                                    with patch.object(main, "start_services") as mock_start_services:
                                        with patch.object(main, "health_check", return_value=True) as mock_health_check:
                                            with patch("asyncio.Event") as mock_event:
                                                mock_event_instance = MagicMock()
                                                mock_event.return_value = mock_event_instance
                                                mock_event_instance.wait = AsyncMock()

                                                await main.main()

                                                # Ellenőrizzük, hogy a strategy engine setup meghívásra került
                                                mock_setup_strategy.assert_called_once()

    @pytest.mark.asyncio
    async def test_main_calls_start_services(self) -> None:
        """Teszteli, hogy a main függvény meghívja a services indítását."""
        with patch.object(main, "StaticConfig") as mock_config:
            mock_config.return_value = MagicMock(
                app_env="test",
                log_level="INFO",
                db_url="sqlite+aiosqlite:///test.db",
                trading_symbols=["EURUSD"],
                data_base_path="/tmp/test",
                api_host="0.0.0.0",
                api_port=8000
            )
            with patch.object(main, "setup_logging"):
                with patch.object(main, "setup_database"):
                    with patch.object(main, "setup_event_bus"):
                        with patch.object(main, "setup_storage_service"):
                            with patch.object(main, "setup_collectors"):
                                with patch.object(main, "setup_strategy_engine"):
                                    with patch.object(main, "start_services") as mock_start_services:
                                        with patch.object(main, "health_check", return_value=True) as mock_health_check:
                                            with patch("asyncio.Event") as mock_event:
                                                mock_event_instance = MagicMock()
                                                mock_event.return_value = mock_event_instance
                                                mock_event_instance.wait = AsyncMock()

                                                await main.main()

                                                # Ellenőrizzük, hogy a services indítása meghívásra került
                                                mock_start_services.assert_called_once()

    @pytest.mark.asyncio
    async def test_main_calls_health_check(self) -> None:
        """Teszteli, hogy a main függvény meghívja a health check-et."""
        with patch.object(main, "StaticConfig") as mock_config:
            mock_config.return_value = MagicMock(
                app_env="test",
                log_level="INFO",
                db_url="sqlite+aiosqlite:///test.db",
                trading_symbols=["EURUSD"],
                data_base_path="/tmp/test",
                api_host="0.0.0.0",
                api_port=8000
            )
            with patch.object(main, "setup_logging"):
                with patch.object(main, "setup_database"):
                    with patch.object(main, "setup_event_bus"):
                        with patch.object(main, "setup_storage_service"):
                            with patch.object(main, "setup_collectors"):
                                with patch.object(main, "setup_strategy_engine"):
                                    with patch.object(main, "start_services"):
                                        with patch.object(main, "health_check", return_value=True) as mock_health_check:
                                            with patch("asyncio.Event") as mock_event:
                                                mock_event_instance = MagicMock()
                                                mock_event.return_value = mock_event_instance
                                                mock_event_instance.wait = AsyncMock()

                                                await main.main()

                                                # Ellenőrizzük, hogy a health check meghívásra került
                                                mock_health_check.assert_called_once()

    @pytest.mark.asyncio
    async def test_main_waits_with_event(self) -> None:
        """Teszteli, hogy a main függvény az asyncio.Event().wait()-et hívja meg."""
        with patch.object(main, "StaticConfig") as mock_config:
            mock_config.return_value = MagicMock(
                app_env="test",
                log_level="INFO",
                db_url="sqlite+aiosqlite:///test.db",
                trading_symbols=["EURUSD"],
                data_base_path="/tmp/test",
                api_host="0.0.0.0",
                api_port=8000
            )
            with patch.object(main, "setup_logging"):
                with patch.object(main, "setup_database"):
                    with patch.object(main, "setup_event_bus"):
                        with patch.object(main, "setup_storage_service"):
                            with patch.object(main, "setup_collectors"):
                                with patch.object(main, "setup_strategy_engine"):
                                    with patch.object(main, "start_services"):
                                        with patch.object(main, "health_check", return_value=True):
                                            with patch("asyncio.Event") as mock_event:
                                                mock_event_instance = MagicMock()
                                                mock_event.return_value = mock_event_instance
                                                mock_event_instance.wait = AsyncMock()

                                                await main.main()

                                                # Ellenőrizzük, hogy az event wait meghívásra került
                                                mock_event_instance.wait.assert_called_once()

    @pytest.mark.asyncio
    async def test_main_exits_on_health_check_failure(self) -> None:
        """Teszteli, hogy a main függvény kilép, ha a health check sikertelen."""
        with patch.object(main, "StaticConfig") as mock_config:
            mock_config.return_value = MagicMock(
                app_env="test",
                log_level="INFO",
                db_url="sqlite+aiosqlite:///test.db",
                trading_symbols=["EURUSD"],
                data_base_path="/tmp/test",
                api_host="0.0.0.0",
                api_port=8000
            )
            with patch.object(main, "setup_logging"):
                with patch.object(main, "setup_database"):
                    with patch.object(main, "setup_event_bus"):
                        with patch.object(main, "setup_storage_service"):
                            with patch.object(main, "setup_collectors"):
                                with patch.object(main, "setup_strategy_engine"):
                                    with patch.object(main, "start_services"):
                                        with patch.object(main, "health_check", return_value=False):
                                            with patch.object(main, "sys") as mock_sys:
                                                mock_sys.exit = MagicMock()

                                                # A tesztnek el kell érnie a sys.exit(1) hívást
                                                try:
                                                    await main.main()
                                                except SystemExit:
                                                    pass

                                                # Ellenőrizzük, hogy a sys.exit meghívásra került
                                                mock_sys.exit.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_main_handles_keyboard_interrupt(self) -> None:
        """Teszteli, hogy a main függvény kezeli a KeyboardInterrupt-ot."""
        with patch.object(main, "StaticConfig") as mock_config:
            mock_config.return_value = MagicMock(
                app_env="test",
                log_level="INFO",
                db_url="sqlite+aiosqlite:///test.db",
                trading_symbols=["EURUSD"],
                data_base_path="/tmp/test",
                api_host="0.0.0.0",
                api_port=8000
            )
            with patch.object(main, "setup_logging"):
                with patch.object(main, "setup_database"):
                    with patch.object(main, "setup_event_bus"):
                        with patch.object(main, "setup_storage_service"):
                            with patch.object(main, "setup_collectors"):
                                with patch.object(main, "setup_strategy_engine"):
                                    with patch.object(main, "start_services"):
                                        with patch.object(main, "health_check", return_value=True):
                                            with patch("asyncio.Event") as mock_event:
                                                mock_event_instance = MagicMock()
                                                mock_event.return_value = mock_event_instance
                                                # Dobjunk KeyboardInterrupt-ot a wait hívásakor
                                                mock_event_instance.wait = AsyncMock(
                                                    side_effect=KeyboardInterrupt
                                                )

                                                # A tesztnek nem szabad kivételt dobnia
                                                try:
                                                    await main.main()
                                                except KeyboardInterrupt:
                                                    pass  # Ez várható viselkedés

                                                # Ellenőrizzük, hogy a wait meghívásra került
                                                mock_event_instance.wait.assert_called_once()

    @pytest.mark.asyncio
    async def test_main_handles_general_exception(self) -> None:
        """Teszteli, hogy a main függvény kezeli az általános kivételeket."""
        with patch.object(main, "StaticConfig") as mock_config:
            mock_config.return_value = MagicMock(
                app_env="test",
                log_level="INFO",
                db_url="sqlite+aiosqlite:///test.db",
                trading_symbols=["EURUSD"],
                data_base_path="/tmp/test",
                api_host="0.0.0.0",
                api_port=8000
            )
            with patch.object(main, "setup_logging"):
                with patch.object(main, "setup_database") as mock_setup_database:
                    # Dobjunk egy általános kivételt a database setup során
                                                    mock_setup_database.side_effect = Exception("Database error")
                                                    with patch.object(main, "sys") as mock_sys:
                                                        mock_sys.exit = MagicMock()

                                                        # A tesztnek el kell érnie a sys.exit(1) hívást
                                                        try:
                                                            await main.main()
                                                        except SystemExit:
                                                            pass

                                                        # Ellenőrizzük, hogy a sys.exit meghívásra került
                                                        mock_sys.exit.assert_called_once_with(1)


class TestSetupFunctions:
    """Tesztosztály a setup függvényekhez."""

    def test_setup_logging_exists(self) -> None:
        """Teszteli, hogy a setup_logging függvény létezik-e."""
        assert hasattr(main, "setup_logging")
        assert callable(main.setup_logging)

    def test_setup_database_exists(self) -> None:
        """Teszteli, hogy a setup_database függvény létezik-e."""
        assert hasattr(main, "setup_database")
        assert callable(main.setup_database)

    def test_setup_event_bus_exists(self) -> None:
        """Teszteli, hogy a setup_event_bus függvény létezik-e."""
        assert hasattr(main, "setup_event_bus")
        assert callable(main.setup_event_bus)

    def test_setup_storage_service_exists(self) -> None:
        """Teszteli, hogy a setup_storage_service függvény létezik-e."""
        assert hasattr(main, "setup_storage_service")
        assert callable(main.setup_storage_service)

    def test_setup_collectors_exists(self) -> None:
        """Teszteli, hogy a setup_collectors függvény létezik-e."""
        assert hasattr(main, "setup_collectors")
        assert callable(main.setup_collectors)

    def test_setup_strategy_engine_exists(self) -> None:
        """Teszteli, hogy a setup_strategy_engine függvény létezik-e."""
        assert hasattr(main, "setup_strategy_engine")
        assert callable(main.setup_strategy_engine)

    def test_start_services_exists(self) -> None:
        """Teszteli, hogy a start_services függvény létezik-e."""
        assert hasattr(main, "start_services")
        assert callable(main.start_services)

    def test_health_check_exists(self) -> None:
        """Teszteli, hogy a health_check függvény létezik-e."""
        assert hasattr(main, "health_check")
        assert callable(main.health_check)

    def test_graceful_shutdown_exists(self) -> None:
        """Teszteli, hogy a graceful_shutdown függvény létezik-e."""
        assert hasattr(main, "graceful_shutdown")
        assert callable(main.graceful_shutdown)

    @pytest.mark.asyncio
    async def test_setup_database_is_async(self) -> None:
        """Teszteli, hogy a setup_database async függvény-e."""
        import inspect
        assert inspect.iscoroutinefunction(main.setup_database)

    @pytest.mark.asyncio
    async def test_setup_event_bus_is_async(self) -> None:
        """Teszteli, hogy a setup_event_bus async függvény-e."""
        import inspect
        assert inspect.iscoroutinefunction(main.setup_event_bus)

    @pytest.mark.asyncio
    async def test_setup_storage_service_is_async(self) -> None:
        """Teszteli, hogy a setup_storage_service async függvény-e."""
        import inspect
        assert inspect.iscoroutinefunction(main.setup_storage_service)

    @pytest.mark.asyncio
    async def test_setup_collectors_is_async(self) -> None:
        """Teszteli, hogy a setup_collectors async függvény-e."""
        import inspect
        assert inspect.iscoroutinefunction(main.setup_collectors)

    @pytest.mark.asyncio
    async def test_setup_strategy_engine_is_async(self) -> None:
        """Teszteli, hogy a setup_strategy_engine async függvény-e."""
        import inspect
        assert inspect.iscoroutinefunction(main.setup_strategy_engine)

    @pytest.mark.asyncio
    async def test_start_services_is_async(self) -> None:
        """Teszteli, hogy a start_services async függvény-e."""
        import inspect
        assert inspect.iscoroutinefunction(main.start_services)

    @pytest.mark.asyncio
    async def test_health_check_is_async(self) -> None:
        """Teszteli, hogy a health_check async függvény-e."""
        import inspect
        assert inspect.iscoroutinefunction(main.health_check)


class TestStaticConfig:
    """Tesztosztály a StaticConfig osztályhoz."""

    def test_static_config_exists(self) -> None:
        """Teszteli, hogy a StaticConfig osztály létezik-e."""
        assert hasattr(main, "StaticConfig")
        assert isinstance(main.StaticConfig, type)

    def test_static_config_has_required_attributes(self) -> None:
        """Teszteli, hogy a StaticConfig rendelkezik a szükséges attribútumokkal."""
        config = main.StaticConfig()

        assert hasattr(config, "app_env")
        assert hasattr(config, "log_level")
        assert hasattr(config, "db_url")
        assert hasattr(config, "trading_symbols")
        assert hasattr(config, "data_base_path")
        assert hasattr(config, "api_host")
        assert hasattr(config, "api_port")

    def test_static_config_default_values(self) -> None:
        """Teszteli a StaticConfig alapértelmezett értékeit."""
        config = main.StaticConfig()

        assert config.app_env == "development"
        assert config.log_level == "INFO"
        assert config.db_url == "sqlite+aiosqlite:///neural_ai.db"
        assert isinstance(config.trading_symbols, list)
        assert len(config.trading_symbols) > 0
        assert config.data_base_path == "/data/tick"
        assert config.api_host == "0.0.0.0"
        assert config.api_port == 8000
