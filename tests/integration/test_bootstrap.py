#!/usr/bin/env python3
"""Integrációs teszt a main.py szkript indításához.

Ez a tesztmodul ellenőrzi a fő alkalmazás belépési pontjának megfelelő működését
az új CoreComponents struktúra szerint.
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
    """Tesztosztály a main.py szkript indítási folyamatához az új CoreComponents struktúrával."""

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
    async def test_main_calls_bootstrap_core(self) -> None:
        """Teszteli, hogy a main függvény meghívja a bootstrap_core-t."""
        with patch.object(main, "bootstrap_core") as mock_bootstrap:
            # Mockoljuk a CoreComponents objektumot
            mock_components = MagicMock()
            mock_components.event_bus = MagicMock()
            mock_components.event_bus.start = AsyncMock()
            mock_components.database = MagicMock()
            mock_components.database.initialize = AsyncMock()
            mock_bootstrap.return_value = mock_components

            # Mockoljuk az asyncio.Event().wait()-et, hogy ne várjon örökké
            with patch("asyncio.Event") as mock_event:
                mock_event_instance = MagicMock()
                mock_event.return_value = mock_event_instance
                mock_event_instance.wait = AsyncMock()

                # Hívjuk meg a main függvényt
                await main.main()

                # Ellenőrizzük, hogy a bootstrap_core meghívásra került
                mock_bootstrap.assert_called_once()

    @pytest.mark.asyncio
    async def test_main_calls_event_bus_start(self) -> None:
        """Teszteli, hogy a main függvény meghívja az event bus start-ot."""
        with patch.object(main, "bootstrap_core") as mock_bootstrap:
            # Mockoljuk a CoreComponents objektumot
            mock_components = MagicMock()
            mock_components.event_bus = MagicMock()
            mock_components.event_bus.start = AsyncMock()
            mock_components.database = MagicMock()
            mock_components.database.initialize = AsyncMock()
            mock_bootstrap.return_value = mock_components

            # Mockoljuk az asyncio.Event().wait()-et
            with patch("asyncio.Event") as mock_event:
                mock_event_instance = MagicMock()
                mock_event.return_value = mock_event_instance
                mock_event_instance.wait = AsyncMock()

                await main.main()

                # Ellenőrizzük, hogy az event_bus.start meghívásra került
                mock_components.event_bus.start.assert_called_once()

    @pytest.mark.asyncio
    async def test_main_calls_database_initialize(self) -> None:
        """Teszteli, hogy a main függvény meghívja az adatbázis inicializálást."""
        with patch.object(main, "bootstrap_core") as mock_bootstrap:
            # Mockoljuk a CoreComponents objektumot
            mock_components = MagicMock()
            mock_components.event_bus = MagicMock()
            mock_components.event_bus.start = AsyncMock()
            mock_components.database = MagicMock()
            mock_components.database.initialize = AsyncMock()
            mock_bootstrap.return_value = mock_components

            # Mockoljuk az asyncio.Event().wait()-et
            with patch("asyncio.Event") as mock_event:
                mock_event_instance = MagicMock()
                mock_event.return_value = mock_event_instance
                mock_event_instance.wait = AsyncMock()

                await main.main()

                # Ellenőrizzük, hogy a database.initialize meghívásra került
                mock_components.database.initialize.assert_called_once()

    @pytest.mark.asyncio
    async def test_main_waits_with_event(self) -> None:
        """Teszteli, hogy a main függvény az asyncio.Event().wait()-et hívja meg."""
        with patch.object(main, "bootstrap_core") as mock_bootstrap:
            # Mockoljuk a CoreComponents objektumot
            mock_components = MagicMock()
            mock_components.event_bus = MagicMock()
            mock_components.event_bus.start = AsyncMock()
            mock_components.database = MagicMock()
            mock_components.database.initialize = AsyncMock()
            mock_bootstrap.return_value = mock_components

            with patch("asyncio.Event") as mock_event:
                mock_event_instance = MagicMock()
                mock_event.return_value = mock_event_instance
                mock_event_instance.wait = AsyncMock()

                await main.main()

                # Ellenőrizzük, hogy az event wait meghívásra került
                mock_event_instance.wait.assert_called_once()

    @pytest.mark.asyncio
    async def test_main_handles_keyboard_interrupt(self) -> None:
        """Teszteli, hogy a main függvény kezeli a KeyboardInterrupt-ot."""
        with patch.object(main, "bootstrap_core") as mock_bootstrap:
            # Mockoljuk a CoreComponents objektumot
            mock_components = MagicMock()
            mock_components.event_bus = MagicMock()
            mock_components.event_bus.start = AsyncMock()
            mock_components.database = MagicMock()
            mock_components.database.initialize = AsyncMock()
            mock_bootstrap.return_value = mock_components

            with patch("asyncio.Event") as mock_event:
                mock_event_instance = MagicMock()
                mock_event.return_value = mock_event_instance
                # Dobjunk KeyboardInterrupt-ot a wait hívásakor
                mock_event_instance.wait = AsyncMock(side_effect=KeyboardInterrupt)

                # A tesztnek nem szabad kivételt dobnia
                try:
                    await main.main()
                except KeyboardInterrupt:
                    pass  # Ez várható viselkedés

                # Ellenőrizzük, hogy a wait meghívásra került
                mock_event_instance.wait.assert_called_once()

    @pytest.mark.asyncio
    async def test_main_handles_general_exception(self) -> None:
        """Teszteli, hogy a main függvény nem kezeli az általános kivételeket."""
        with patch.object(main, "bootstrap_core") as mock_bootstrap:
            # Dobjunk egy általános kivételt a bootstrap során
            mock_bootstrap.side_effect = Exception("Bootstrap error")
            with patch("asyncio.Event") as mock_event:
                mock_event_instance = MagicMock()
                mock_event.return_value = mock_event_instance
                mock_event_instance.wait = AsyncMock()

                # A main függvénynek tovább kell adnia a kivételt
                with pytest.raises(Exception, match="Bootstrap error"):
                    await main.main()

    @pytest.mark.asyncio
    async def test_main_handles_database_initialization_error(self) -> None:
        """Teszteli, hogy a main függvény nem kezeli az adatbázis inicializálási hibát."""
        with patch.object(main, "bootstrap_core") as mock_bootstrap:
            # Mockoljuk a CoreComponents objektumot
            mock_components = MagicMock()
            mock_components.event_bus = MagicMock()
            mock_components.event_bus.start = AsyncMock()
            mock_components.database = MagicMock()
            # Dobjunk kivételt az adatbázis inicializálásakor
            mock_components.database.initialize = AsyncMock(side_effect=Exception("DB init error"))
            mock_bootstrap.return_value = mock_components

            with patch("asyncio.Event") as mock_event:
                mock_event_instance = MagicMock()
                mock_event.return_value = mock_event_instance
                mock_event_instance.wait = AsyncMock()

                # A main függvénynek tovább kell adnia a kivételt
                with pytest.raises(Exception, match="DB init error"):
                    await main.main()

    @pytest.mark.asyncio
    async def test_main_handles_event_bus_start_error(self) -> None:
        """Teszteli, hogy a main függvény nem kezeli az event bus indítási hibát."""
        with patch.object(main, "bootstrap_core") as mock_bootstrap:
            # Mockoljuk a CoreComponents objektumot
            mock_components = MagicMock()
            mock_components.event_bus = MagicMock()
            # Dobjunk kivételt az event bus indításakor
            mock_components.event_bus.start = AsyncMock(side_effect=Exception("Event bus error"))
            mock_components.database = MagicMock()
            mock_components.database.initialize = AsyncMock()
            mock_bootstrap.return_value = mock_components

            with patch("asyncio.Event") as mock_event:
                mock_event_instance = MagicMock()
                mock_event.return_value = mock_event_instance
                mock_event_instance.wait = AsyncMock()

                # A main függvénynek tovább kell adnia a kivételt
                with pytest.raises(Exception, match="Event bus error"):
                    await main.main()


class TestBootstrapCore:
    """Tesztosztály a bootstrap_core függvényhez."""

    def test_bootstrap_core_function_exists(self) -> None:
        """Teszteli, hogy a bootstrap_core függvény létezik-e."""
        from neural_ai.core import bootstrap_core
        assert callable(bootstrap_core)

    def test_bootstrap_core_returns_core_components(self) -> None:
        """Teszteli, hogy a bootstrap_core visszaadja a CoreComponents objektumot."""
        from neural_ai.core import CoreComponents, bootstrap_core

        # Mockoljuk a factory függvényeket, hogy ne próbáljanak ténylegesen inicializálni
        config_path = "neural_ai.core.config.factory.ConfigManagerFactory.get_manager"
        logger_path = "neural_ai.core.logger.factory.LoggerFactory.get_logger"
        db_path = "neural_ai.core.db.factory.DatabaseFactory.create_manager"
        event_path = "neural_ai.core.events.factory.EventBusFactory.create"
        storage_path = "neural_ai.core.storage.factory.StorageFactory.get_storage"
        hw_path = "neural_ai.core.utils.factory.HardwareFactory.get_hardware_info"

        with patch(config_path) as mock_config, \
             patch(logger_path) as mock_logger, \
             patch(db_path) as mock_db, \
             patch(event_path) as mock_event, \
             patch(storage_path) as mock_storage, \
             patch(hw_path) as mock_hw:
                                # Beállítjuk a mockok visszatérési értékét
                                mock_config.return_value = MagicMock()
                                mock_logger.return_value = MagicMock()
                                mock_db.return_value = MagicMock()
                                mock_event.return_value = MagicMock()
                                mock_storage.return_value = MagicMock()
                                mock_hw.return_value = MagicMock()

                                # Hívjuk meg a bootstrap_core-t
                                components = bootstrap_core()

                                # Ellenőrizzük, hogy CoreComponents objektumot kapunk vissza
                                assert isinstance(components, CoreComponents)

    def test_core_components_has_required_attributes(self) -> None:
        """Teszteli, hogy a CoreComponents rendelkezik a szükséges attribútumokkal."""
        from neural_ai.core import CoreComponents

        # Mock komponensek létrehozása
        mock_config = MagicMock()
        mock_logger = MagicMock()
        mock_storage = MagicMock()
        mock_database = MagicMock()
        mock_event_bus = MagicMock()
        mock_hardware = MagicMock()

        # Létrehozzuk a CoreComponents példányt és beállítjuk a komponenseket
        components = CoreComponents()
        components.set_config(mock_config)
        components.set_logger(mock_logger)
        components.set_storage(mock_storage)
        components.set_database(mock_database)
        components.set_event_bus(mock_event_bus)
        components.set_hardware(mock_hardware)

        # Ellenőrizzük, hogy minden attribútum létezik
        assert hasattr(components, "config")
        assert hasattr(components, "logger")
        assert hasattr(components, "storage")
        assert hasattr(components, "database")
        assert hasattr(components, "event_bus")
        assert hasattr(components, "hardware")

        # Ellenőrizzük, hogy a megfelelő objektumokat tárolja-e
        assert components.config is mock_config
        assert components.logger is mock_logger
        assert components.storage is mock_storage
        assert components.database is mock_database
        assert components.event_bus is mock_event_bus
        assert components.hardware is mock_hardware

        # Ellenőrizzük az új mezőket a feladat szerint
        assert components.database is not None
        assert components.event_bus is not None
        assert components.hardware is not None


class TestCoreModule:
    """Tesztosztály a core modul globális függvényeihez."""

    def test_get_version_exists(self) -> None:
        """Teszteli, hogy a get_version függvény létezik-e."""
        from neural_ai.core import get_version
        assert callable(get_version)

    def test_get_version_returns_string(self) -> None:
        """Teszteli, hogy a get_version stringet ad vissza."""
        from neural_ai.core import get_version
        version = get_version()
        assert isinstance(version, str)

    def test_get_schema_version_exists(self) -> None:
        """Teszteli, hogy a get_schema_version függvény létezik-e."""
        from neural_ai.core import get_schema_version
        assert callable(get_schema_version)

    def test_get_schema_version_returns_string(self) -> None:
        """Teszteli, hogy a get_schema_version stringet ad vissza."""
        from neural_ai.core import get_schema_version
        schema_version = get_schema_version()
        assert isinstance(schema_version, str)
        assert schema_version == "1.0.0"

    def test_get_core_components_exists(self) -> None:
        """Teszteli, hogy a get_core_components függvény létezik-e."""
        from neural_ai.core import get_core_components
        assert callable(get_core_components)

    def test_get_core_components_returns_singleton(self) -> None:
        """Teszteli, hogy a get_core_components szingleton példányt ad vissza."""
        from neural_ai.core import CoreComponents, get_core_components

        # Mockoljuk a bootstrap_core-t, hogy ne próbáljon ténylegesen inicializálni
        with patch("neural_ai.core.bootstrap_core") as mock_bootstrap:
            mock_bootstrap.return_value = MagicMock(spec=CoreComponents)

            # Első hívás
            components1 = get_core_components()

            # Második hívás - ugyanazt a példányt kell visszaadnia
            components2 = get_core_components()

            # Ellenőrizzük, hogy ugyanaz a példány
            assert components1 is components2
            # Ellenőrizzük, hogy a bootstrap_core csak egyszer hívódott meg
            mock_bootstrap.assert_called_once()
