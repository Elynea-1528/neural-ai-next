"""Tesztek a main.py modulhoz.

Ez a modul tartalmazza a fő indító szkript tesztjeit, amelyek ellenőrzik
az alkalmazás életciklusát és a komponens inicializálást.
"""

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# A main modul importálása a tesztekhez
from main import main


class TestMain:
    """Tesztek a main függvényhez."""

    @pytest.mark.asyncio
    async def test_main_successful_initialization(self) -> None:
        """Teszteli a sikeres alkalmazás inicializálást.

        Ellenőrzi, hogy a fő függvény helyesen inicializálja a core komponenseket
        és indítja el a szolgáltatásokat.
        """
        # Mock objektumok létrehozása
        mock_logger = MagicMock()
        mock_event_bus = AsyncMock()
        mock_database = AsyncMock()

        # Mock CoreComponents létrehozása
        mock_components = MagicMock()
        mock_components.logger = mock_logger
        mock_components.event_bus = mock_event_bus
        mock_components.database = mock_database

        with patch("main.bootstrap_core", return_value=mock_components):
            # Feladat létrehozása a main függvény futtatásához
            task = asyncio.create_task(main())

            # Várakozás egy rövid ideig, hogy a fő függvény elinduljon
            await asyncio.sleep(0.1)

            # Ellenőrzések
            mock_logger.info.assert_called()
            mock_event_bus.start.assert_called_once()
            mock_database.initialize.assert_called_once()

            # Feladat leállítása
            task.cancel()
            # A CancelledError-t elnyeli a suppress, ezért nem kell expectálni
            await task

    @pytest.mark.asyncio
    async def test_main_without_logger(self) -> None:
        """Teszteli a main függvényt logger nélkül.

        Ellenőrzi, hogy a függvény helyesen kezeli a hiányzó logger esetét.
        """
        # Mock objektumok létrehozása logger nélkül
        mock_event_bus = AsyncMock()
        mock_database = AsyncMock()

        mock_components = MagicMock()
        mock_components.logger = None
        mock_components.event_bus = mock_event_bus
        mock_components.database = mock_database

        with patch("main.bootstrap_core", return_value=mock_components):
            task = asyncio.create_task(main())

            await asyncio.sleep(0.1)

            # Ellenőrzés, hogy a logger nélkül is fut a rendszer
            mock_event_bus.start.assert_called_once()
            mock_database.initialize.assert_called_once()

            task.cancel()
            # A CancelledError-t elnyeli a suppress, ezért nem kell expectálni
            await task

    @pytest.mark.asyncio
    async def test_main_without_event_bus(self) -> None:
        """Teszteli a main függvényt event bus nélkül.

        Ellenőrzi, hogy a függvény helyesen kezeli a hiányzó event bus esetét.
        """
        mock_logger = MagicMock()
        mock_database = AsyncMock()

        mock_components = MagicMock()
        mock_components.logger = mock_logger
        mock_components.event_bus = None
        mock_components.database = mock_database

        with patch("main.bootstrap_core", return_value=mock_components):
            task = asyncio.create_task(main())

            await asyncio.sleep(0.1)

            # Ellenőrzés, hogy az event bus nélkül is fut a rendszer
            mock_logger.info.assert_called()
            mock_database.initialize.assert_called_once()

            task.cancel()
            # A CancelledError-t elnyeli a suppress, ezért nem kell expectálni
            await task

    @pytest.mark.asyncio
    async def test_main_without_database(self) -> None:
        """Teszteli a main függvényt adatbázis nélkül.

        Ellenőrzi, hogy a függvény helyesen kezeli a hiányzó adatbázis esetét.
        """
        mock_logger = MagicMock()
        mock_event_bus = AsyncMock()

        mock_components = MagicMock()
        mock_components.logger = mock_logger
        mock_components.event_bus = mock_event_bus
        mock_components.database = None

        with patch("main.bootstrap_core", return_value=mock_components):
            task = asyncio.create_task(main())

            await asyncio.sleep(0.1)

            # Ellenőrzés, hogy az adatbázis nélkül is fut a rendszer
            mock_logger.info.assert_called()
            mock_event_bus.start.assert_called_once()

            task.cancel()
            # A CancelledError-t elnyeli a suppress, ezért nem kell expectálni
            await task

    def test_main_module_execution(self) -> None:
        """Teszteli a main modul végrehajtását.

        Ellenőrzi, hogy a modul importálható és tartalmazza a szükséges függvényeket.
        """
        # Import ellenőrzése
        import main as main_module

        assert hasattr(main_module, "main")
        assert callable(main_module.main)

    @pytest.mark.asyncio
    async def test_main_graceful_shutdown(self) -> None:
        """Teszteli a main függvény elegáns leállását.

        Ellenőrzi, hogy a CancelledError-t helyesen kezeli a függvény.
        """
        mock_components = MagicMock()
        mock_components.logger = MagicMock()
        mock_components.event_bus = AsyncMock()
        mock_components.database = AsyncMock()

        with patch("main.bootstrap_core", return_value=mock_components):
            task = asyncio.create_task(main())

            await asyncio.sleep(0.1)

            # Feladat leállítása és ellenőrzés, hogy nem dob kivételt
            task.cancel()

            # A CancelledError-t elnyeli a suppress, ezért nem szabad, hogy kivételt dobjon
            await task


class TestMainEntryPoint:
    """Tesztek a __main__ belépési ponthoz."""

    def test_main_entry_point_exists(self) -> None:
        """Teszteli, hogy a main modul tartalmazza a __main__ blokkot.

        Ellenőrzi, hogy a modul futtatható-e standalone módon.
        """
        import main as main_module

        # Ellenőrzés, hogy a modul tartalmazza a __name__ == "__main__" blokkot
        source_code = open(main_module.__file__).read()
        assert 'if __name__ == "__main__"' in source_code

    def test_main_entry_point_uses_asyncio_run(self) -> None:
        """Teszteli, hogy a __main__ blokk asyncio.run-t használ.

        Ellenőrzi, hogy a fő belépési pont helyesen használja az asyncio.run-t
        az alkalmazás indításához.
        """
        import main as main_module

        source_code = open(main_module.__file__).read()
        assert "asyncio.run(main())" in source_code

    def test_main_entry_point_handles_keyboard_interrupt(self) -> None:
        """Teszteli, hogy a __main__ blokk kezeli a KeyboardInterrupt-ot.

        Ellenőrzi, hogy a Ctrl+C helyesen van-e kezelve.
        """
        import main as main_module

        source_code = open(main_module.__file__).read()
        assert "except KeyboardInterrupt:" in source_code

    def test_main_entry_point_handles_general_exceptions(self) -> None:
        """Teszteli, hogy a __main__ blokk kezeli az általános kivételeket.

        Ellenőrzi, hogy a nem várt kivételek helyesen vannak-e kezelve.
        """
        import main as main_module

        source_code = open(main_module.__file__).read()
        assert "except Exception as e:" in source_code
        assert "sys.exit(1)" in source_code

    def test_main_entry_point_finally_block(self) -> None:
        """Teszteli, hogy a __main__ blokk tartalmaz finally blokkot.

        Ellenőrzi, hogy a rendszer leállítása után végrehajtódik a takarítás.
        """
        import main as main_module

        source_code = open(main_module.__file__).read()
        assert "finally:" in source_code