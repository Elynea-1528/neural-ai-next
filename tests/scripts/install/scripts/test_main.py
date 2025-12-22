#!/usr/bin/env python3
"""Tesztelési modul a main.py scripthez.

Ez a modul egyszerű dummy teszteket tartalmaz a telepítő scripthez,
mivel a script külső parancsokat futtat, amelyeket nehéz unit tesztelni.
"""

import os

# Importáljuk a tesztelendő modult
import sys
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../../scripts/install/scripts"))

from main import (
    Colors,
    InstallMode,
    PyTorchMode,
    check_conda,
    check_environment,
    print_error,
    print_info,
    print_success,
    print_warning,
    run_command,
    update_environment_yml,
)


class TestInstallMode(unittest.TestCase):
    """Teszt osztály az InstallMode enumhoz."""

    def test_install_mode_values(self):
        """Teszteli az InstallMode értékeit."""
        self.assertEqual(InstallMode.MINIMAL.value, "minimal")
        self.assertEqual(InstallMode.DEV.value, "dev")
        self.assertEqual(InstallMode.DEV_TRADER.value, "dev+trader")
        self.assertEqual(InstallMode.FULL.value, "full")
        self.assertEqual(InstallMode.CHECK_ONLY.value, "check")
        self.assertEqual(InstallMode.TRADER_ONLY.value, "trader")
        self.assertEqual(InstallMode.JUPYTER_ONLY.value, "jupyter")


class TestPyTorchMode(unittest.TestCase):
    """Teszt osztály a PyTorchMode enumhoz."""

    def test_pytorch_mode_values(self):
        """Teszteli a PyTorchMode értékeit."""
        self.assertEqual(PyTorchMode.CPU.value, "cpu")
        self.assertEqual(PyTorchMode.CUDA_12_1.value, "cuda12.1")


class TestColors(unittest.TestCase):
    """Teszt osztály a Colors osztályhoz."""

    def test_colors_constants(self):
        """Teszteli a színkonstansokat."""
        self.assertTrue(hasattr(Colors, "RED"))
        self.assertTrue(hasattr(Colors, "GREEN"))
        self.assertTrue(hasattr(Colors, "YELLOW"))
        self.assertTrue(hasattr(Colors, "BLUE"))
        self.assertTrue(hasattr(Colors, "RESET"))

        # Ellenőrizzük, hogy a színek ANSI kódokat tartalmaznak
        self.assertIn("\033[", Colors.RED)
        self.assertIn("\033[", Colors.GREEN)
        self.assertIn("\033[", Colors.YELLOW)
        self.assertIn("\033[", Colors.BLUE)
        self.assertIn("\033[", Colors.RESET)


class TestPrintFunctions(unittest.TestCase):
    """Teszt osztály a nyomtatási függvényekhez."""

    @patch("builtins.print")
    def test_print_error(self, mock_print):
        """Teszteli a hibaüzenet kiírását."""
        print_error("Teszt hiba")
        mock_print.assert_called_once()
        args = mock_print.call_args[0][0]
        self.assertIn(Colors.RED, args)
        self.assertIn("✗", args)
        self.assertIn("Teszt hiba", args)

    @patch("builtins.print")
    def test_print_success(self, mock_print):
        """Teszteli a sikerüzenet kiírását."""
        print_success("Teszt siker")
        mock_print.assert_called_once()
        args = mock_print.call_args[0][0]
        self.assertIn(Colors.GREEN, args)
        self.assertIn("✓", args)
        self.assertIn("Teszt siker", args)

    @patch("builtins.print")
    def test_print_warning(self, mock_print):
        """Teszteli a figyelmeztető üzenet kiírását."""
        print_warning("Teszt figyelmeztetés")
        mock_print.assert_called_once()
        args = mock_print.call_args[0][0]
        self.assertIn(Colors.YELLOW, args)
        self.assertIn("⚠️", args)
        self.assertIn("Teszt figyelmeztetés", args)

    @patch("builtins.print")
    def test_print_info(self, mock_print):
        """Teszteli az információs üzenet kiírását."""
        print_info("Teszt információ")
        mock_print.assert_called_once()
        args = mock_print.call_args[0][0]
        self.assertIn(Colors.BLUE, args)
        self.assertIn("ℹ️", args)
        self.assertIn("Teszt információ", args)


class TestRunCommand(unittest.TestCase):
    """Teszt osztály a run_command függvényhez."""

    @patch("subprocess.run")
    def test_run_command_success(self, mock_run):
        """Teszteli a sikeres parancs végrehajtást."""
        mock_run.return_value = MagicMock(returncode=0)
        result = run_command("echo test", verbose=False)
        self.assertTrue(result)
        mock_run.assert_called_once()

    @patch("subprocess.run")
    def test_run_command_failure(self, mock_run):
        """Teszteli a sikertelen parancs végrehajtást."""
        mock_run.return_value = MagicMock(returncode=1)
        result = run_command("false", check=False, verbose=False)
        self.assertFalse(result)

    @patch("subprocess.Popen")
    def test_run_command_verbose(self, mock_popen):
        """Teszteli a verbose módú parancs végrehajtást."""
        mock_process = MagicMock()
        mock_process.wait.return_value = None
        mock_process.returncode = 0
        mock_popen.return_value = mock_process

        result = run_command("echo test", verbose=True)
        self.assertTrue(result)
        mock_popen.assert_called_once()


class TestCheckConda(unittest.TestCase):
    """Teszt osztály a check_conda függvényhez."""

    @patch("main.run_command")
    def test_check_conda_installed(self, mock_run):
        """Teszteli a conda telepítettségének ellenőrzését (telepítve van)."""
        mock_run.return_value = True
        result = check_conda()
        self.assertTrue(result)

    @patch("main.run_command")
    def test_check_conda_not_installed(self, mock_run):
        """Teszteli a conda telepítettségének ellenőrzését (nincs telepítve)."""
        mock_run.return_value = False
        result = check_conda()
        self.assertFalse(result)


class TestCheckEnvironment(unittest.TestCase):
    """Teszt osztály a check_environment függvényhez."""

    @patch("subprocess.run")
    def test_check_environment_exists(self, mock_run):
        """Teszteli a környezet létezését (létezik)."""
        mock_result = MagicMock()
        mock_result.stdout = "neural-ai-next"
        mock_run.return_value = mock_result

        result = check_environment()
        self.assertTrue(result)

    @patch("subprocess.run")
    def test_check_environment_not_exists(self, mock_run):
        """Teszteli a környezet létezését (nem létezik)."""
        mock_result = MagicMock()
        mock_result.stdout = "other-env"
        mock_run.return_value = mock_result

        result = check_environment()
        self.assertFalse(result)


class TestUpdateEnvironmentYml(unittest.TestCase):
    """Teszt osztály az update_environment_yml függvényhez."""

    @patch("builtins.open", create=True)
    def test_update_environment_yml_cpu(self, mock_open):
        """Teszteli az environment.yml frissítését CPU módban."""
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file

        result = update_environment_yml(PyTorchMode.CPU)

        self.assertIsInstance(result, str)
        self.assertTrue(result.endswith("environment.yml"))
        mock_open.assert_called_once()

    @patch("builtins.open", create=True)
    def test_update_environment_yml_cuda(self, mock_open):
        """Teszteli az environment.yml frissítését CUDA módban."""
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file

        result = update_environment_yml(PyTorchMode.CUDA_12_1)

        self.assertIsInstance(result, str)
        self.assertTrue(result.endswith("environment.yml"))
        mock_open.assert_called_once()


class TestIntegration(unittest.TestCase):
    """Integrációs tesztek."""

    def test_install_mode_enum_completeness(self):
        """Ellenőrzi, hogy az InstallMode enum tartalmazza az összes szükséges módot."""
        expected_modes = ["minimal", "dev", "dev+trader", "full", "check", "trader", "jupyter"]
        actual_modes = [mode.value for mode in InstallMode]
        self.assertEqual(sorted(actual_modes), sorted(expected_modes))

    def test_pytorch_mode_enum_completeness(self):
        """Ellenőrzi, hogy a PyTorchMode enum tartalmazza az összes szükséges módot."""
        expected_modes = ["cpu", "cuda12.1"]
        actual_modes = [mode.value for mode in PyTorchMode]
        self.assertEqual(sorted(actual_modes), sorted(expected_modes))


def run_tests():
    """Futtatja az összes tesztet."""
    # Teszt loader létrehozása
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Összes teszt osztály hozzáadása
    suite.addTests(loader.loadTestsFromTestCase(TestInstallMode))
    suite.addTests(loader.loadTestsFromTestCase(TestPyTorchMode))
    suite.addTests(loader.loadTestsFromTestCase(TestColors))
    suite.addTests(loader.loadTestsFromTestCase(TestPrintFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestRunCommand))
    suite.addTests(loader.loadTestsFromTestCase(TestCheckConda))
    suite.addTests(loader.loadTestsFromTestCase(TestCheckEnvironment))
    suite.addTests(loader.loadTestsFromTestCase(TestUpdateEnvironmentYml))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))

    # Teszt futtató létrehozása
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
