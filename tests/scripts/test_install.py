#!/usr/bin/env python3
"""Tesztek a scripts/install.py modulhoz.

Ez a modul unit és integrációs teszteket tartalmaz a telepítő szkript
különböző funkcióinak ellenőrzéséhez.
"""

import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pytest

# A projekt gyökérkönyvtárának meghatározása
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

# Importáljuk a tesztelendő modult
import install as installer  # noqa: E402


class TestColors:
    """Tesztek a Colors osztályhoz."""

    def test_colors_defined(self) -> None:
        """Ellenőrzi, hogy a színek definiálva vannak-e."""
        assert hasattr(installer.Colors, "RED")
        assert hasattr(installer.Colors, "GREEN")
        assert hasattr(installer.Colors, "YELLOW")
        assert hasattr(installer.Colors, "BLUE")
        assert hasattr(installer.Colors, "NC")


class TestHelperFunctions:
    """Tesztek a segédfüggvényekhez."""

    def test_print_banner(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Ellenőrzi a banner kiírását."""
        installer.print_banner()
        captured = capsys.readouterr()
        assert "Neural AI Next" in captured.out
        assert "Unified Zero-Touch Installer" in captured.out

    def test_print_success(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Ellenőrzi a sikeres üzenet kiírását."""
        installer.print_success("Teszt üzenet")
        captured = capsys.readouterr()
        assert "✓" in captured.out
        assert "Teszt üzenet" in captured.out

    def test_print_error(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Ellenőrzi a hibaüzenet kiírását."""
        installer.print_error("Hiba üzenet")
        captured = capsys.readouterr()
        assert "✗" in captured.out
        assert "Hiba üzenet" in captured.out

    def test_print_warning(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Ellenőrzi a figyelmeztető üzenet kiírását."""
        installer.print_warning("Figyelmeztetés")
        captured = capsys.readouterr()
        assert "⚠" in captured.out
        assert "Figyelmeztetés" in captured.out

    def test_print_info(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Ellenőrzi az információs üzenet kiírását."""
        installer.print_info("Információ")
        captured = capsys.readouterr()
        assert "ℹ" in captured.out
        assert "Információ" in captured.out

    def test_command_exists_true(self) -> None:
        """Ellenőrzi, hogy a 'python' parancs létezik-e."""
        assert installer.command_exists("python") is True

    def test_command_exists_false(self) -> None:
        """Ellenőrzi, hogy egy nem létező parancs nem létezik."""
        assert installer.command_exists("nonexistent_command_xyz") is False

    def test_run_command_success(self) -> None:
        """Ellenőrzi a sikeres parancs futtatását."""
        result = installer.run_command("echo 'hello'", check=True)
        assert result.returncode == 0
        assert "hello" in result.stdout

    def test_run_command_failure(self) -> None:
        """Ellenőrzi a sikertelen parancs futtatását."""
        with pytest.raises(subprocess.CalledProcessError):
            installer.run_command("false", check=True)

    def test_run_command_no_check(self) -> None:
        """Ellenőrzi a parancs futtatását check=False esetén."""
        result = installer.run_command("false", check=False)
        assert result.returncode != 0


class TestHardwareDetection:
    """Tesztek a hardver detektáló függvényekhez."""

    @patch("install.command_exists")
    def test_check_conda_true(self, mock_exists: MagicMock) -> None:
        """Ellenőrzi a Conda jelenlétét (pozitív eset)."""
        mock_exists.return_value = True
        assert installer.check_conda() is True

    @patch("install.command_exists")
    def test_check_conda_false(self, mock_exists: MagicMock) -> None:
        """Ellenőrzi a Conda hiányát (negatív eset)."""
        mock_exists.return_value = False
        assert installer.check_conda() is False

    @patch("install.command_exists")
    def test_check_nvidia_gpu_true(self, mock_exists: MagicMock) -> None:
        """Ellenőrzi az NVIDIA GPU jelenlétét (pozitív eset)."""
        mock_exists.return_value = True
        with patch("install.run_command") as mock_run:
            mock_result = Mock()
            mock_result.returncode = 0
            mock_result.stdout = "NVIDIA GeForce RTX 3080"
            mock_run.return_value = mock_result
            assert installer.check_nvidia_gpu() is True

    @patch("install.command_exists")
    def test_check_nvidia_gpu_false_no_nvidia_smi(
        self, mock_exists: MagicMock
    ) -> None:
        """Ellenőrzi az NVIDIA GPU hiányát (nvidia-smi nincs)."""
        mock_exists.return_value = False
        assert installer.check_nvidia_gpu() is False

    @patch("install.command_exists")
    def test_check_nvidia_gpu_false_empty_output(
        self, mock_exists: MagicMock
    ) -> None:
        """Ellenőrzi az NVIDIA GPU hiányát (üres output)."""
        mock_exists.return_value = True
        with patch("install.run_command") as mock_run:
            mock_result = Mock()
            mock_result.returncode = 0
            mock_result.stdout = ""
            mock_run.return_value = mock_result
            assert installer.check_nvidia_gpu() is False

    def test_check_avx2_support_true(self) -> None:
        """Ellenőrzi az AVX2 támogatást (pozitív eset)."""
        with patch("builtins.open", create=True) as mock_open:
            mock_open.return_value.__enter__().read.return_value = "flags: avx2 sse4"
            assert installer.check_avx2_support() is True

    def test_check_avx2_support_false(self) -> None:
        """Ellenőrzi az AVX2 hiányát (negatív eset)."""
        with patch("builtins.open", create=True) as mock_open:
            mock_open.return_value.__enter__().read.return_value = "flags: sse4 mmx"
            assert installer.check_avx2_support() is False

    def test_check_avx2_support_exception(self) -> None:
        """Ellenőrzi az AVX2 ellenőrzést kivétel esetén."""
        with patch("builtins.open", side_effect=Exception("File not found")):
            assert installer.check_avx2_support() is False

    @patch("install.command_exists")
    def test_check_wine_true(self, mock_exists: MagicMock) -> None:
        """Ellenőrzi a Wine jelenlétét (pozitív eset)."""
        mock_exists.return_value = True
        assert installer.check_wine() is True

    @patch("install.command_exists")
    def test_check_wine_false(self, mock_exists: MagicMock) -> None:
        """Ellenőrzi a Wine hiányát (negatív eset)."""
        mock_exists.return_value = False
        assert installer.check_wine() is False

    def test_get_conda_path(self) -> None:
        """Ellenőrzi a Conda elérési útját."""
        path = installer.get_conda_path()
        assert path == "/home/elynea/miniconda3/bin/conda"


class TestEnvironmentSetup:
    """Tesztek a környezet beállító függvényekhez."""

    @patch("install.run_command")
    def test_remove_conda_env_exists(self, mock_run: MagicMock) -> None:
        """Ellenőrzi a létező Conda környezet eltávolítását."""
        mock_result = Mock()
        mock_result.stdout = "neural-ai-next"
        mock_run.return_value = mock_result

        installer.remove_conda_env()
        # A remove parancs meghívásának ellenőrzése
        assert any(
            "conda env remove" in str(call[0][0]) for call in mock_run.call_args_list
        )

    @patch("install.run_command")
    def test_remove_conda_env_not_exists(self, mock_run: MagicMock) -> None:
        """Ellenőrzi a nem létező Conda környezet ellenőrzését."""
        mock_result = Mock()
        mock_result.stdout = ""
        mock_run.return_value = mock_result

        installer.remove_conda_env()
        # Nem hívja meg a remove parancsot

    @patch("install.run_command")
    def test_create_conda_env_with_packages_gpu(
        self, mock_run: MagicMock
    ) -> None:
        """Ellenőrzi a Conda környezet létrehozását GPU-val."""
        installer.create_conda_env_with_packages(gpu_available=True)
        mock_run.assert_called_once()
        call_args = mock_run.call_args[0][0]
        assert "pytorch==2.5.1" in call_args
        assert "pytorch-cuda=12.1" in call_args

    @patch("install.run_command")
    def test_create_conda_env_with_packages_cpu(
        self, mock_run: MagicMock
    ) -> None:
        """Ellenőrzi a Conda környezet létrehozását CPU-val."""
        installer.create_conda_env_with_packages(gpu_available=False)
        mock_run.assert_called_once()
        call_args = mock_run.call_args[0][0]
        assert "pytorch==2.5.1" in call_args
        assert "cpuonly" in call_args

    @patch("install.run_command")
    def test_install_data_libraries_avx2(self, mock_run: MagicMock) -> None:
        """Ellenőrzi az adatkönyvtárak telepítését AVX2 támogatással."""
        installer.install_data_libraries(avx2_supported=True)
        mock_run.assert_called_once()
        call_args = mock_run.call_args[0][0]
        assert "polars" in call_args
        assert "pyarrow" in call_args

    @patch("install.run_command")
    def test_install_data_libraries_no_avx2(self, mock_run: MagicMock) -> None:
        """Ellenőrzi az adatkönyvtárak telepítését AVX2 nélkül."""
        installer.install_data_libraries(avx2_supported=False)
        mock_run.assert_called_once()
        call_args = mock_run.call_args[0][0]
        assert "fastparquet" in call_args

    @patch("install.run_command")
    def test_install_project_packages_default(self, mock_run: MagicMock) -> None:
        """Ellenőrzi a projekt csomagok telepítését alapértelmezettként."""
        installer.install_project_packages(extra_groups=[])
        mock_run.assert_called_once()
        call_args = mock_run.call_args[0][0]
        assert "pip install -e ." in call_args

    @patch("install.run_command")
    def test_install_project_packages_with_groups(
        self, mock_run: MagicMock
    ) -> None:
        """Ellenőrzi a projekt csomagok telepítését csoportokkal."""
        installer.install_project_packages(extra_groups=["dev", "trader"])
        mock_run.assert_called_once()
        call_args = mock_run.call_args[0][0]
        assert "dev" in call_args
        assert "trader" in call_args


class TestBrokerInstallation:
    """Tesztek a bróker telepítő függvényekhez."""

    def test_create_downloads_dir(self, tmp_path: Path) -> None:
        """Ellenőrzi a downloads mappa létrehozását."""
        with patch("install.PROJECT_ROOT", tmp_path):
            downloads_dir = installer.create_downloads_dir()
            assert downloads_dir.exists()
            assert downloads_dir.name == "downloads"

    @patch("install.run_command")
    def test_download_file(self, mock_run: MagicMock, tmp_path: Path) -> None:
        """Ellenőrzi a fájl letöltését."""
        url = "https://example.com/file.txt"
        output_path = tmp_path / "file.txt"
        installer.download_file(url, output_path)
        mock_run.assert_called_once()
        call_args = mock_run.call_args[0][0]
        assert "curl" in call_args
        assert url in call_args

    @patch("subprocess.Popen")
    @patch("install.download_file")
    def test_install_jforex4(
        self, mock_download: MagicMock, mock_popen: MagicMock, tmp_path: Path
    ) -> None:
        """Ellenőrzi a JForex4 telepítését."""
        with patch("install.PROJECT_ROOT", tmp_path):
            downloads_dir = installer.create_downloads_dir()
            # Mock fájl létrehozása a chmod művelethez
            installer_file = downloads_dir / "JForex4_unix_64_JRE_bundled.sh"
            installer_file.touch()
            installer.install_jforex4(downloads_dir)
            mock_download.assert_called_once()
            mock_popen.assert_called_once()

    @patch("subprocess.Popen")
    @patch("install.download_file")
    def test_install_tws(
        self, mock_download: MagicMock, mock_popen: MagicMock, tmp_path: Path
    ) -> None:
        """Ellenőrzi a TWS telepítését."""
        with patch("install.PROJECT_ROOT", tmp_path):
            downloads_dir = installer.create_downloads_dir()
            # Mock fájl létrehozása a chmod művelethez
            installer_file = downloads_dir / "tws-latest-linux-x64.sh"
            installer_file.touch()
            installer.install_tws(downloads_dir)
            mock_download.assert_called_once()
            mock_popen.assert_called_once()

    @patch("install.check_wine")
    @patch("subprocess.Popen")
    @patch("install.download_file")
    def test_install_mt5_dukascopy_with_wine(
        self,
        mock_download: MagicMock,
        mock_popen: MagicMock,
        mock_check_wine: MagicMock,
        tmp_path: Path,
    ) -> None:
        """Ellenőrzi az MT5 telepítését Wine-el."""
        mock_check_wine.return_value = True
        with patch("install.PROJECT_ROOT", tmp_path):
            downloads_dir = installer.create_downloads_dir()
            installer.install_mt5_dukascopy(downloads_dir)
            mock_download.assert_called_once()
            mock_popen.assert_called_once()

    @patch("install.check_wine")
    def test_install_mt5_dukascopy_no_wine(
        self, mock_check_wine: MagicMock, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Ellenőrzi az MT5 telepítését Wine nélkül."""
        mock_check_wine.return_value = False
        with patch("install.PROJECT_ROOT", tmp_path):
            downloads_dir = installer.create_downloads_dir()
            installer.install_mt5_dukascopy(downloads_dir)
            captured = capsys.readouterr()
            assert "Wine nincs telepítve" in captured.out


class TestMainFunctions:
    """Tesztek a fő függvényekhez."""

    @patch("install.check_conda")
    @patch("install.check_nvidia_gpu")
    @patch("install.check_avx2_support")
    def test_run_hardware_detection_success(
        self,
        mock_avx2: MagicMock,
        mock_gpu: MagicMock,
        mock_conda: MagicMock,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Ellenőrzi a sikeres hardver detektálást."""
        mock_conda.return_value = True
        mock_gpu.return_value = True
        mock_avx2.return_value = True

        gpu_available, avx2_supported = installer.run_hardware_detection()

        assert gpu_available is True
        assert avx2_supported is True
        captured = capsys.readouterr()
        assert "Hardver detektálás" in captured.out

    @patch("install.check_conda")
    def test_run_hardware_detection_no_conda(
        self, mock_conda: MagicMock
    ) -> None:
        """Ellenőrzi a hardver detektálást Conda hiányában."""
        mock_conda.return_value = False
        with pytest.raises(SystemExit) as exc_info:
            installer.run_hardware_detection()
        assert exc_info.value.code == 1

    @patch("install.install_project_packages")
    @patch("install.install_data_libraries")
    @patch("install.create_conda_env_with_packages")
    @patch("install.remove_conda_env")
    def test_install_core_environment(
        self,
        mock_remove: MagicMock,
        mock_create: MagicMock,
        mock_install_data: MagicMock,
        mock_install_project: MagicMock,
    ) -> None:
        """Ellenőrzi a core környezet telepítését."""
        installer.install_core_environment(
            gpu_available=True, avx2_supported=True, extra_groups=["dev"]
        )
        mock_remove.assert_called_once()
        # A mock hívás ellenőrzése (nem név szerinti paraméterrel)
        mock_create.assert_called_once()
        assert mock_create.call_args[0][0] is True  # gpu_available
        mock_install_data.assert_called_once()
        assert mock_install_data.call_args[0][0] is True  # avx2_supported
        mock_install_project.assert_called_once()
        assert mock_install_project.call_args[0][0] == ["dev"]  # extra_groups

    @patch("install.install_mt5_dukascopy")
    @patch("install.install_tws")
    @patch("install.install_jforex4")
    @patch("install.create_downloads_dir")
    def test_install_brokers(
        self,
        mock_create_dir: MagicMock,
        mock_jforex: MagicMock,
        mock_tws: MagicMock,
        mock_mt5: MagicMock,
    ) -> None:
        """Ellenőrzi a brókerek telepítését."""
        mock_create_dir.return_value = Path("/tmp/downloads")
        installer.install_brokers()
        mock_jforex.assert_called_once()
        mock_tws.assert_called_once()
        mock_mt5.assert_called_once()


class TestArgumentParsing:
    """Tesztek az argumentum feldolgozáshoz."""

    def test_parse_arguments_default(self) -> None:
        """Ellenőrzi az alapértelmezett argumentumokat."""
        with patch("sys.argv", ["install.py"]):
            args = installer.parse_arguments()
            assert args.only is None
            assert args.no_brokers is False
            assert args.verbose is False

    def test_parse_arguments_only(self) -> None:
        """Ellenőrzi a --only argumentumot."""
        with patch("sys.argv", ["install.py", "--only", "dev,trader"]):
            args = installer.parse_arguments()
            assert args.only == "dev,trader"

    def test_parse_arguments_no_brokers(self) -> None:
        """Ellenőrzi a --no-brokers argumentumot."""
        with patch("sys.argv", ["install.py", "--no-brokers"]):
            args = installer.parse_arguments()
            assert args.no_brokers is True

    def test_parse_arguments_verbose(self) -> None:
        """Ellenőrzi a --verbose argumentumot."""
        with patch("sys.argv", ["install.py", "-v"]):
            args = installer.parse_arguments()
            assert args.verbose is True


class TestCompletionMessage:
    """Tesztek a befejezési üzenethez."""

    def test_print_completion_message_gpu_avx2(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Ellenőrzi a befejezési üzenetet GPU-val és AVX2-vel."""
        installer.print_completion_message(
            gpu_available=True, avx2_supported=True, extra_groups=["dev", "trader"]
        )
        captured = capsys.readouterr()
        assert "TELJES TELEPÍTÉS SIKERES" in captured.out
        assert "NVIDIA GPU" in captured.out
        assert "AVX2" in captured.out
        assert "polars + pyarrow" in captured.out

    def test_print_completion_message_cpu_no_avx2(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Ellenőrzi a befejezési üzenetet CPU-val és AVX2 nélkül."""
        installer.print_completion_message(
            gpu_available=False, avx2_supported=False, extra_groups=[]
        )
        captured = capsys.readouterr()
        assert "CPU mód" in captured.out
        assert "fastparquet" in captured.out


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
