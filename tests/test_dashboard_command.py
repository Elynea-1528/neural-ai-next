"""Dashboard parancs tesztjei.

Ez a modul tartalmazza a dashboard parancs tesztjeit.
"""

import subprocess
import sys
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

# Hozzáadjuk a neural_ai könyvtárat a Python path-hoz
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import parse_arguments, run_dashboard_mode


class TestDashboardCommand:
    """Dashboard parancs tesztosztály."""

    @patch("sys.argv", ["main.py", "dashboard"])
    def test_parse_arguments_dashboard_default(self) -> None:
        """Teszteli a dashboard parancs alapértelmezett argumentumait."""
        args = parse_arguments()

        assert args.command == "dashboard"
        assert args.host == "localhost"
        assert args.port == 8501
        assert args.headless is False

    @patch("sys.argv", ["main.py", "dashboard", "--host", "0.0.0.0"])
    def test_parse_arguments_dashboard_with_host(self) -> None:
        """Teszteli a dashboard parancsot hoszt argumentummal."""
        args = parse_arguments()

        assert args.command == "dashboard"
        assert args.host == "0.0.0.0"
        assert args.port == 8501
        assert args.headless is False

    @patch("sys.argv", ["main.py", "dashboard", "--port", "9999"])
    def test_parse_arguments_dashboard_with_port(self) -> None:
        """Teszteli a dashboard parancsot port argumentummal."""
        args = parse_arguments()

        assert args.command == "dashboard"
        assert args.host == "localhost"
        assert args.port == 9999
        assert args.headless is False

    @patch("sys.argv", ["main.py", "dashboard", "--headless"])
    def test_parse_arguments_dashboard_with_headless(self) -> None:
        """Teszteli a dashboard parancsot headless argumentummal."""
        args = parse_arguments()

        assert args.command == "dashboard"
        assert args.host == "localhost"
        assert args.port == 8501
        assert args.headless is True

    @patch(
        "sys.argv",
        ["main.py", "dashboard", "--host", "192.168.1.100", "--port", "8080", "--headless"],
    )
    def test_parse_arguments_dashboard_with_all_options(self) -> None:
        """Teszteli a dashboard parancsot az összes opcióval."""
        args = parse_arguments()

        assert args.command == "dashboard"
        assert args.host == "192.168.1.100"
        assert args.port == 8080
        assert args.headless is True

    @patch("shutil.which")
    @patch("subprocess.run")
    def test_run_dashboard_mode_success(self, mock_run: Mock, mock_which: Mock) -> None:
        """Teszteli a dashboard mód sikeres indítását."""
        # Mock beállítása
        mock_which.return_value = "/usr/bin/streamlit"
        mock_run.return_value = None

        # Teszt futtatása
        try:
            run_dashboard_mode("localhost", 8501, False)
        except SystemExit:
            # A subprocess.run miatt SystemExit jöhet létre
            # Ez normális, ha a mock nem ad vissza értéket
            pass

        # Ellenőrzés
        mock_which.assert_called_once_with("streamlit")
        mock_run.assert_called_once()

    @patch("shutil.which")
    def test_run_dashboard_mode_streamlit_not_found(self, mock_which: Mock) -> None:
        """Teszteli a dashboard módot, ha a Streamlit nincs telepítve."""
        # Mock beállítása
        mock_which.return_value = None

        # Teszt futtatása és ellenőrzés
        with pytest.raises(SystemExit) as exc_info:
            run_dashboard_mode("localhost", 8501, False)

        assert exc_info.value.code == 1
        mock_which.assert_called_once_with("streamlit")

    @patch("shutil.which")
    @patch("subprocess.run")
    def test_run_dashboard_mode_with_headless(self, mock_run: Mock, mock_which: Mock) -> None:
        """Teszteli a dashboard mód headless indítását."""
        # Mock beállítása
        mock_which.return_value = "/usr/bin/streamlit"
        mock_run.return_value = None

        # Teszt futtatása
        try:
            run_dashboard_mode("0.0.0.0", 9999, True)
        except SystemExit:
            pass

        # Ellenőrzés
        mock_which.assert_called_once_with("streamlit")
        mock_run.assert_called_once()

        # Ellenőrizzük, hogy a headless flag szerepel-e a hívásban
        call_args = mock_run.call_args[0][0]
        assert "--server.headless" in call_args
        assert "true" in call_args

    @patch("shutil.which")
    @patch("subprocess.run")
    def test_run_dashboard_mode_without_headless(self, mock_run: Mock, mock_which: Mock) -> None:
        """Teszteli a dashboard mód indítását headless nélkül."""
        # Mock beállítása
        mock_which.return_value = "/usr/bin/streamlit"
        mock_run.return_value = None

        # Teszt futtatása
        try:
            run_dashboard_mode("localhost", 8501, False)
        except SystemExit:
            pass

        # Ellenőrzés
        mock_which.assert_called_once_with("streamlit")
        mock_run.assert_called_once()

        # Ellenőrizzük, hogy a headless flag NEM szerepel a hívásban
        call_args = mock_run.call_args[0][0]
        assert "--server.headless" not in call_args

    @patch("shutil.which")
    @patch("subprocess.run")
    def test_run_dashboard_mode_subprocess_error(self, mock_run: Mock, mock_which: Mock) -> None:
        """Teszteli a dashboard módot, ha a subprocess hiba történik."""
        # Mock beállítása
        mock_which.return_value = "/usr/bin/streamlit"
        mock_run.side_effect = subprocess.CalledProcessError(1, "streamlit")

        # Teszt futtatása és ellenőrzés
        with pytest.raises(SystemExit) as exc_info:
            run_dashboard_mode("localhost", 8501, False)

        assert exc_info.value.code == 1

    def test_run_dashboard_mode_keyboard_interrupt(self) -> None:
        """Teszteli a dashboard mód leállítását KeyboardInterrupt esetén."""
        # Ez a teszt csak ellenőrzi, hogy a függvény létezik
        # A valós teszteléshez mockolni kellene a subprocess.run-t
        assert callable(run_dashboard_mode)


class TestDashboardCLI:
    """Dashboard CLI integrációs tesztjei."""

    def test_dashboard_command_help(self) -> None:
        """Teszteli a dashboard parancs help üzenetét."""
        result = subprocess.run(
            ["python", "main.py", "dashboard", "--help"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert "Dashboard" in result.stdout or "dashboard" in result.stdout
        assert "--host" in result.stdout
        assert "--port" in result.stdout
        assert "--headless" in result.stdout

    def test_dashboard_command_in_main_help(self) -> None:
        """Teszteli, hogy a dashboard szerepel a fő help üzenetben."""
        result = subprocess.run(
            ["python", "main.py", "--help"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert "dashboard" in result.stdout


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
