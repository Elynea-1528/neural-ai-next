"""Unit tesztek a main.py modulhoz.

Ez a modul teszteli a CLI belépési pont összes funkcióját:
- Live mód indítása
- Download mód (történeti adatok)
- Dashboard mód (Streamlit)
- Argumentum parsing
- Dátum parsing
- Hibakezelés
"""

import sys
from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, Mock, patch

import pytest

# Mock a main modul importjait
sys.modules["neural_ai.core"] = MagicMock()
sys.modules["neural_ai.core.logger.interfaces.logger_interface"] = MagicMock()
sys.modules["neural_ai.collectors.jforex.interfaces.live_interface"] = MagicMock()
sys.modules["neural_ai.core.base.implementations.component_bundle"] = MagicMock()
sys.modules["neural_ai.core.db.implementations.sqlalchemy_session"] = MagicMock()
sys.modules["neural_ai.core.events.interfaces.event_bus_interface"] = MagicMock()
sys.modules["neural_ai.data.ingestion.market_data_persister"] = MagicMock()

import main  # noqa: E402


class TestParseDateFunction:
    """Tesztek a parse_date() függvényhez."""

    def test_parse_date_valid_format(self) -> None:
        """Helyes dátum formátum parse-olása."""
        # Arrange
        date_str = "2024-03-20"

        # Act
        result = main.parse_date(date_str)

        # Assert
        assert result.year == 2024
        assert result.month == 3
        assert result.day == 20
        assert result.tzinfo == UTC

    def test_parse_date_invalid_format(self) -> None:
        """Érvénytelen dátum formátum ValueError-t dob."""
        # Arrange
        date_str = "invalid-date"

        # Act & Assert
        with pytest.raises(ValueError, match="Érvénytelen dátum formátum"):
            main.parse_date(date_str)

    def test_parse_date_wrong_separator(self) -> None:
        """Rossz elválasztó karakter ValueError-t dob."""
        # Arrange
        date_str = "2024/03/20"

        # Act & Assert
        with pytest.raises(ValueError, match="Érvénytelen dátum formátum"):
            main.parse_date(date_str)


class TestParseArgumentsFunction:
    """Tesztek a parse_arguments() függvényhez."""

    def test_parse_arguments_live_mode(self) -> None:
        """Live mód argumentum parsing."""
        # Arrange
        test_args = ["main.py", "live"]

        # Act
        with patch.object(sys, "argv", test_args):
            args = main.parse_arguments()

        # Assert
        assert args.command == "live"

    def test_parse_arguments_download_mode(self) -> None:
        """Download mód argumentum parsing."""
        # Arrange
        test_args = [
            "main.py",
            "download",
            "--symbol",
            "EURUSD",
            "--start",
            "2024-03-20",
            "--end",
            "2024-03-21",
        ]

        # Act
        with patch.object(sys, "argv", test_args):
            args = main.parse_arguments()

        # Assert
        assert args.command == "download"
        assert args.symbol == "EURUSD"
        assert args.start == "2024-03-20"
        assert args.end == "2024-03-21"

    def test_parse_arguments_dashboard_mode_defaults(self) -> None:
        """Dashboard mód alapértelmezett értékekkel."""
        # Arrange
        test_args = ["main.py", "dashboard"]

        # Act
        with patch.object(sys, "argv", test_args):
            args = main.parse_arguments()

        # Assert
        assert args.command == "dashboard"
        assert args.host == "localhost"
        assert args.port == 8501
        assert args.headless is False

    def test_parse_arguments_dashboard_mode_custom(self) -> None:
        """Dashboard mód egyedi értékekkel."""
        # Arrange
        test_args = [
            "main.py",
            "dashboard",
            "--host",
            "0.0.0.0",
            "--port",
            "9000",
            "--headless",
        ]

        # Act
        with patch.object(sys, "argv", test_args):
            args = main.parse_arguments()

        # Assert
        assert args.command == "dashboard"
        assert args.host == "0.0.0.0"
        assert args.port == 9000
        assert args.headless is True


class TestRunLiveMode:
    """Tesztek a run_live_mode() függvényhez."""

    @pytest.mark.asyncio
    async def test_run_live_mode_success(self) -> None:
        """Live mód sikeres indítása és leállítása."""
        # Arrange
        mock_logger = Mock()
        mock_event_bus = AsyncMock()
        mock_database = AsyncMock()
        mock_live_feed = AsyncMock()
        mock_persister = AsyncMock()

        mock_components = Mock()
        mock_components.logger = mock_logger
        mock_components.event_bus = mock_event_bus
        mock_components.database = mock_database
        mock_components.live_feed = mock_live_feed
        mock_components.persister = mock_persister

        # Act
        with (
            patch("main.get_core_components", return_value=mock_components),
            patch("asyncio.Event") as mock_event_class,
        ):
            # Mock az Event().wait() hogy azonnal visszatérjen
            mock_event = Mock()
            mock_event.wait = AsyncMock(side_effect=KeyboardInterrupt)
            mock_event_class.return_value = mock_event

            try:
                await main.run_live_mode()
            except KeyboardInterrupt:
                pass

        # Assert - Szolgáltatások indítása
        mock_event_bus.start.assert_called_once()
        mock_database.initialize.assert_called_once()
        mock_persister.start.assert_called_once()
        mock_live_feed.start.assert_called_once()

        # Assert - Szolgáltatások leállítása (fordított sorrend)
        mock_persister.stop.assert_called_once()
        mock_live_feed.stop.assert_called_once()
        mock_event_bus.stop.assert_called_once()

    @pytest.mark.asyncio
    async def test_run_live_mode_none_components(self) -> None:
        """Live mód None komponensekkel (graceful degradation)."""
        # Arrange
        mock_components = Mock()
        mock_components.logger = None
        mock_components.event_bus = None
        mock_components.database = None
        mock_components.live_feed = None
        mock_components.persister = None

        # Act
        with (
            patch("main.get_core_components", return_value=mock_components),
            patch("asyncio.Event") as mock_event_class,
        ):
            mock_event = Mock()
            mock_event.wait = AsyncMock(side_effect=KeyboardInterrupt)
            mock_event_class.return_value = mock_event

            try:
                await main.run_live_mode()
            except KeyboardInterrupt:
                pass

        # Assert - Nem dob hibát None komponensekkel


class TestRunDownloadMode:
    """Tesztek a run_download_mode() függvényhez."""

    @pytest.mark.asyncio
    async def test_run_download_mode_success(self) -> None:
        """Download mód sikeres futása."""
        # Arrange
        mock_logger = Mock()
        symbol = "EURUSD"
        start_date = datetime(2024, 3, 20, tzinfo=UTC)
        end_date = datetime(2024, 3, 21, tzinfo=UTC)

        # Mock a dinamikus importot a run_download_mode függvényen belül
        mock_download = AsyncMock()

        # Act
        mock_module = MagicMock(download_historical_data=mock_download)
        with patch.dict("sys.modules", {"scripts.download_history": mock_module}):
            await main.run_download_mode(mock_logger, symbol, start_date, end_date)

        # Assert
        mock_download.assert_called_once_with(symbol, start_date, end_date)
        assert mock_logger.info.call_count >= 2  # Banner + üzenetek


class TestRunDashboardMode:
    """Tesztek a run_dashboard_mode() függvényhez."""

    def test_run_dashboard_mode_success(self) -> None:
        """Dashboard mód sikeres indítása."""
        # Arrange
        mock_logger = Mock()
        host = "localhost"
        port = 8501
        headless = False

        # Act
        with patch("subprocess.run") as mock_subprocess:
            main.run_dashboard_mode(mock_logger, host, port, headless)

        # Assert
        mock_subprocess.assert_called_once()
        call_args = mock_subprocess.call_args[0][0]
        assert "/streamlit" in call_args[0]
        assert "run" in call_args
        assert "neural_ai/ui/streamlit_app.py" in call_args
        assert str(port) in call_args

    def test_run_dashboard_mode_headless(self) -> None:
        """Dashboard mód headless flag-gel."""
        # Arrange
        mock_logger = Mock()
        host = "0.0.0.0"
        port = 9000
        headless = True

        # Act
        with patch("subprocess.run") as mock_subprocess:
            main.run_dashboard_mode(mock_logger, host, port, headless)

        # Assert
        call_args = mock_subprocess.call_args[0][0]
        assert "--server.headless" in call_args
        assert "true" in call_args

    def test_run_dashboard_mode_subprocess_error(self) -> None:
        """Dashboard mód subprocess hiba kezelése."""
        # Arrange
        mock_logger = Mock()
        import subprocess

        # Act & Assert
        with (
            patch("subprocess.run", side_effect=subprocess.CalledProcessError(1, "cmd")),
            pytest.raises(SystemExit) as exc_info,
        ):
            main.run_dashboard_mode(mock_logger, "localhost", 8501, False)

        assert exc_info.value.code == 1
        mock_logger.error.assert_called_once()

    def test_run_dashboard_mode_keyboard_interrupt(self) -> None:
        """Dashboard mód KeyboardInterrupt kezelése."""
        # Arrange
        mock_logger = Mock()

        # Act & Assert
        with (
            patch("subprocess.run", side_effect=KeyboardInterrupt),
            pytest.raises(SystemExit) as exc_info,
        ):
            main.run_dashboard_mode(mock_logger, "localhost", 8501, False)

        assert exc_info.value.code == 0


class TestMainFunction:
    """Tesztek a main() függvényhez."""

    def test_main_live_mode(self) -> None:
        """Main függvény live móddal."""
        # Arrange
        test_args = ["main.py", "live"]
        mock_logger = Mock()
        mock_components = Mock()
        mock_components.logger = mock_logger

        # Act
        with (
            patch.object(sys, "argv", test_args),
            patch("main.get_core_components", return_value=mock_components),
            patch("asyncio.run") as mock_asyncio_run,
        ):
            main.main()

        # Assert
        mock_asyncio_run.assert_called_once()

    def test_main_live_mode_keyboard_interrupt(self) -> None:
        """Main függvény live mód KeyboardInterrupt kezelése."""
        # Arrange
        test_args = ["main.py", "live"]
        mock_logger = Mock()
        mock_components = Mock()
        mock_components.logger = mock_logger

        # Act
        with (
            patch.object(sys, "argv", test_args),
            patch("main.get_core_components", return_value=mock_components),
            patch("asyncio.run", side_effect=KeyboardInterrupt),
        ):
            main.main()

        # Assert
        mock_logger.info.assert_called_with("🛑 Rendszer leállítva.")

    def test_main_live_mode_exception(self) -> None:
        """Main függvény live mód exception kezelése."""
        # Arrange
        test_args = ["main.py", "live"]
        mock_logger = Mock()
        mock_components = Mock()
        mock_components.logger = mock_logger

        # Act & Assert
        with (
            patch.object(sys, "argv", test_args),
            patch("main.get_core_components", return_value=mock_components),
            patch("asyncio.run", side_effect=RuntimeError("Test error")),
            pytest.raises(SystemExit) as exc_info,
        ):
            main.main()

        assert exc_info.value.code == 1
        mock_logger.error.assert_called_once()

    def test_main_download_mode_success(self) -> None:
        """Main függvény download móddal."""
        # Arrange
        test_args = [
            "main.py",
            "download",
            "--symbol",
            "EURUSD",
            "--start",
            "2024-03-20",
            "--end",
            "2024-03-21",
        ]
        mock_logger = Mock()
        mock_components = Mock()
        mock_components.logger = mock_logger

        # Act
        with (
            patch.object(sys, "argv", test_args),
            patch("main.get_core_components", return_value=mock_components),
            patch("asyncio.run") as mock_asyncio_run,
        ):
            main.main()

        # Assert
        mock_asyncio_run.assert_called_once()

    def test_main_download_mode_invalid_date_format(self) -> None:
        """Main függvény download mód érvénytelen dátum formátummal."""
        # Arrange
        test_args = [
            "main.py",
            "download",
            "--symbol",
            "EURUSD",
            "--start",
            "invalid",
            "--end",
            "2024-03-21",
        ]
        mock_logger = Mock()
        mock_components = Mock()
        mock_components.logger = mock_logger

        # Act & Assert
        with (
            patch.object(sys, "argv", test_args),
            patch("main.get_core_components", return_value=mock_components),
            pytest.raises(SystemExit) as exc_info,
        ):
            main.main()

        assert exc_info.value.code == 1
        mock_logger.error.assert_called_once()

    def test_main_download_mode_start_after_end(self) -> None:
        """Main függvény download mód kezdő dátum > záró dátum."""
        # Arrange
        test_args = [
            "main.py",
            "download",
            "--symbol",
            "EURUSD",
            "--start",
            "2024-03-25",
            "--end",
            "2024-03-20",
        ]
        mock_logger = Mock()
        mock_components = Mock()
        mock_components.logger = mock_logger

        # Act & Assert
        with (
            patch.object(sys, "argv", test_args),
            patch("main.get_core_components", return_value=mock_components),
            pytest.raises(SystemExit) as exc_info,
        ):
            main.main()

        assert exc_info.value.code == 1
        assert any("későbbi" in str(call) for call in mock_logger.error.call_args_list)

    def test_main_download_mode_future_date(self) -> None:
        """Main függvény download mód jövőbeli dátummal."""
        # Arrange
        future_date = (datetime.now(UTC).replace(day=1) + timedelta(days=400)).strftime(
            "%Y-%m-%d"
        )
        test_args = [
            "main.py",
            "download",
            "--symbol",
            "EURUSD",
            "--start",
            future_date,
            "--end",
            future_date,
        ]
        mock_logger = Mock()
        mock_components = Mock()
        mock_components.logger = mock_logger

        # Act & Assert
        with (
            patch.object(sys, "argv", test_args),
            patch("main.get_core_components", return_value=mock_components),
            pytest.raises(SystemExit) as exc_info,
        ):
            main.main()

        assert exc_info.value.code == 1
        assert any("jövőben" in str(call) for call in mock_logger.error.call_args_list)

    def test_main_download_mode_keyboard_interrupt(self) -> None:
        """Main függvény download mód KeyboardInterrupt kezelése."""
        # Arrange
        test_args = [
            "main.py",
            "download",
            "--symbol",
            "EURUSD",
            "--start",
            "2024-03-20",
            "--end",
            "2024-03-21",
        ]
        mock_logger = Mock()
        mock_components = Mock()
        mock_components.logger = mock_logger

        # Act & Assert
        with (
            patch.object(sys, "argv", test_args),
            patch("main.get_core_components", return_value=mock_components),
            patch("asyncio.run", side_effect=KeyboardInterrupt),
            pytest.raises(SystemExit) as exc_info,
        ):
            main.main()

        assert exc_info.value.code == 130
        mock_logger.warning.assert_called_once()

    def test_main_download_mode_exception(self) -> None:
        """Main függvény download mód exception kezelése."""
        # Arrange
        test_args = [
            "main.py",
            "download",
            "--symbol",
            "EURUSD",
            "--start",
            "2024-03-20",
            "--end",
            "2024-03-21",
        ]
        mock_logger = Mock()
        mock_components = Mock()
        mock_components.logger = mock_logger

        # Act & Assert
        with (
            patch.object(sys, "argv", test_args),
            patch("main.get_core_components", return_value=mock_components),
            patch("asyncio.run", side_effect=RuntimeError("Test error")),
            pytest.raises(SystemExit) as exc_info,
        ):
            main.main()

        assert exc_info.value.code == 1
        mock_logger.error.assert_called_once()

    def test_main_dashboard_mode(self) -> None:
        """Main függvény dashboard móddal."""
        # Arrange
        test_args = ["main.py", "dashboard"]
        mock_logger = Mock()
        mock_components = Mock()
        mock_components.logger = mock_logger

        # Act
        with (
            patch.object(sys, "argv", test_args),
            patch("main.get_core_components", return_value=mock_components),
            patch("main.run_dashboard_mode") as mock_dashboard,
        ):
            main.main()

        # Assert
        mock_dashboard.assert_called_once_with(mock_logger, "localhost", 8501, False)

    def test_main_dashboard_mode_keyboard_interrupt(self) -> None:
        """Main függvény dashboard mód KeyboardInterrupt kezelése."""
        # Arrange
        test_args = ["main.py", "dashboard"]
        mock_logger = Mock()
        mock_components = Mock()
        mock_components.logger = mock_logger

        # Act
        with (
            patch.object(sys, "argv", test_args),
            patch("main.get_core_components", return_value=mock_components),
            patch("main.run_dashboard_mode", side_effect=KeyboardInterrupt),
        ):
            main.main()

        # Assert
        mock_logger.info.assert_called_with("🛑 Dashboard leállítva.")

    def test_main_dashboard_mode_exception(self) -> None:
        """Main függvény dashboard mód exception kezelése."""
        # Arrange
        test_args = ["main.py", "dashboard"]
        mock_logger = Mock()
        mock_components = Mock()
        mock_components.logger = mock_logger

        # Act & Assert
        with (
            patch.object(sys, "argv", test_args),
            patch("main.get_core_components", return_value=mock_components),
            patch("main.run_dashboard_mode", side_effect=RuntimeError("Test error")),
            pytest.raises(SystemExit) as exc_info,
        ):
            main.main()

        assert exc_info.value.code == 1
        mock_logger.error.assert_called_once()

    def test_main_invalid_command(self) -> None:
        """Main függvény érvénytelen paranccsal."""
        # Arrange
        test_args = ["main.py", "invalid"]
        mock_logger = Mock()
        mock_components = Mock()
        mock_components.logger = mock_logger

        # Act & Assert
        with (
            patch.object(sys, "argv", test_args),
            patch("main.get_core_components", return_value=mock_components),
            pytest.raises(SystemExit) as exc_info,
        ):
            main.main()

        # argparse érvénytelen parancs esetén exit code 2-t ad vissza
        assert exc_info.value.code == 2

    def test_main_no_command(self) -> None:
        """Main függvény parancs nélkül."""
        # Arrange
        test_args = ["main.py"]
        mock_logger = Mock()
        mock_components = Mock()
        mock_components.logger = mock_logger

        # Act & Assert
        with (
            patch.object(sys, "argv", test_args),
            patch("main.get_core_components", return_value=mock_components),
            pytest.raises(SystemExit) as exc_info,
        ):
            main.main()

        assert exc_info.value.code == 1

    def test_main_logger_assertion(self) -> None:
        """Main függvény logger None esetén assertion error."""
        # Arrange
        test_args = ["main.py", "live"]
        mock_components = Mock()
        mock_components.logger = None

        # Act & Assert
        with (
            patch.object(sys, "argv", test_args),
            patch("main.get_core_components", return_value=mock_components),
            pytest.raises(AssertionError, match="Logger is required"),
        ):
            main.main()
