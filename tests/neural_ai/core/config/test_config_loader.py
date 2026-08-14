"""Unit tesztek a ConfigLoader implementációhoz.

Ez a modul tartalmazza a ConfigLoader osztály unit tesztjeit, beleértve:
- Inicializálási teszteket
- SOPS fájl detektálást
- SOPS dekódolási logikát
- Plain YAML fájl betöltést
- Könyvtár betöltést
- Hibakezelést

Arrange-Act-Assert pattern alapján.
"""

import subprocess
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from neural_ai.core.config.exceptions import ConfigLoadError, SOPSDecryptError
from neural_ai.core.config.implementations.config_loader import ConfigLoader


class TestConfigLoaderInit:
    """ConfigLoader inicializálási tesztek."""

    def test_init_without_logger(self) -> None:
        """Teszt: Logger nélküli inicializálás.

        ARRANGE & ACT: ConfigLoader példányosítása alapértelmezett paraméterekkel.
        ASSERT: Logger és SOPS binary alapértelmezett értékek.
        """
        # ARRANGE & ACT
        loader = ConfigLoader()

        # ASSERT
        assert loader._logger is None
        assert loader._sops_binary == "sops"

    def test_init_with_custom_sops_binary(self) -> None:
        """Teszt: Custom SOPS binary útvonal.

        ARRANGE & ACT: ConfigLoader példányosítása custom SOPS binary-vel.
        ASSERT: SOPS binary az átadott érték.
        """
        # ARRANGE & ACT
        loader = ConfigLoader(sops_binary="/usr/local/bin/sops")

        # ASSERT
        assert loader._sops_binary == "/usr/local/bin/sops"


class TestConfigLoaderIsSOPSFile:
    """_is_sops_file() metódus tesztek."""

    def test_is_sops_file_yaml_sops(self) -> None:
        """Teszt: .yaml.sops fájl detektálása.

        ARRANGE: ConfigLoader példány.
        ACT & ASSERT: .yaml.sops végződés detektálása True.
        """
        # ARRANGE
        loader = ConfigLoader()

        # ACT & ASSERT
        assert loader._is_sops_file("secrets.yaml.sops") is True

    def test_is_sops_file_yml_sops(self) -> None:
        """Teszt: .yml.sops fájl detektálása.

        ARRANGE: ConfigLoader példány.
        ACT & ASSERT: .yml.sops végződés detektálása True.
        """
        # ARRANGE
        loader = ConfigLoader()

        # ACT & ASSERT
        assert loader._is_sops_file("config.yml.sops") is True

    def test_is_not_sops_file_plain_yaml(self) -> None:
        """Teszt: Plain .yaml fájl nem SOPS.

        ARRANGE: ConfigLoader példány.
        ACT & ASSERT: .yaml végződés detektálása False.
        """
        # ARRANGE
        loader = ConfigLoader()

        # ACT & ASSERT
        assert loader._is_sops_file("database.yaml") is False


class TestConfigLoaderDecryptSOPS:
    """_decrypt_sops_file() metódus tesztek."""

    @patch("subprocess.run")
    def test_decrypt_sops_file_success(self, mock_run: Mock) -> None:
        """Teszt: Sikeres SOPS dekódolás.

        ARRANGE: ConfigLoader példány, mock subprocess.run sikeres válasszal.
        ACT: _decrypt_sops_file() hívása.
        ASSERT: Dekódolt YAML tartalom visszaadása.
        """
        # ARRANGE
        loader = ConfigLoader()
        mock_run.return_value = Mock(
            returncode=0,
            stdout="key: decrypted_value\n"
        )

        # ACT
        result = loader._decrypt_sops_file("secrets.yaml.sops")

        # ASSERT
        assert result == "key: decrypted_value\n"
        mock_run.assert_called_once()

    @patch("subprocess.run")
    def test_decrypt_sops_file_command_error(self, mock_run: Mock) -> None:
        """Teszt: SOPS parancs hiba (pl. érvénytelen fájl).

        ARRANGE: ConfigLoader példány, mock subprocess.run hibával.
        ACT & ASSERT: SOPSDecryptError kivétel dobása helyes exit code-dal.
        """
        # ARRANGE
        loader = ConfigLoader()
        mock_run.side_effect = subprocess.CalledProcessError(
            returncode=1,
            cmd=["sops", "-d", "bad.yaml.sops"],
            stderr="Failed to decrypt"
        )

        # ACT & ASSERT
        with pytest.raises(SOPSDecryptError) as exc_info:
            loader._decrypt_sops_file("bad.yaml.sops")

        assert exc_info.value.exit_code == 1
        assert "Failed to decrypt" in str(exc_info.value)

    @patch("subprocess.run")
    def test_decrypt_sops_file_binary_not_found(self, mock_run: Mock) -> None:
        """Teszt: SOPS binary nem található.

        ARRANGE: ConfigLoader példány, mock subprocess.run FileNotFoundError-ral.
        ACT & ASSERT: SOPSDecryptError kivétel dobása.
        """
        # ARRANGE
        loader = ConfigLoader()
        mock_run.side_effect = FileNotFoundError("sops not found")

        # ACT & ASSERT
        with pytest.raises(SOPSDecryptError) as exc_info:
            loader._decrypt_sops_file("secrets.yaml.sops")

        assert "binary nem található" in str(exc_info.value)

    @patch("subprocess.run")
    def test_decrypt_sops_file_timeout(self, mock_run: Mock) -> None:
        """Teszt: SOPS dekódolás timeout.

        ARRANGE: ConfigLoader példány, mock subprocess.run TimeoutExpired-del.
        ACT & ASSERT: SOPSDecryptError kivétel dobása timeout hibaüzenettel.
        """
        # ARRANGE
        loader = ConfigLoader()
        mock_run.side_effect = subprocess.TimeoutExpired(
            cmd=["sops", "-d", "huge.yaml.sops"],
            timeout=30
        )

        # ACT & ASSERT
        with pytest.raises(SOPSDecryptError) as exc_info:
            loader._decrypt_sops_file("huge.yaml.sops")

        assert "timeout" in str(exc_info.value)


class TestConfigLoaderLoadFile:
    """load_file() metódus tesztek."""

    def test_load_file_plain_yaml_success(self, tmp_path: Path) -> None:
        """Teszt: Plain YAML fájl betöltése.

        ARRANGE: ConfigLoader példány, temp fájl plain YAML tartalommal.
        ACT: load_file() hívása.
        ASSERT: Helyes dict struktúra visszaadása.
        """
        # ARRANGE
        loader = ConfigLoader()
        config_file = tmp_path / "test.yaml"
        config_file.write_text("database:\n  host: localhost\n")

        # ACT
        result = loader.load_file(str(config_file))

        # ASSERT
        assert result == {"database": {"host": "localhost"}}

    def test_load_file_empty_yaml(self, tmp_path: Path) -> None:
        """Teszt: Üres YAML fájl → üres dict.

        ARRANGE: ConfigLoader példány, üres temp fájl.
        ACT: load_file() hívása.
        ASSERT: Üres dict visszaadása.
        """
        # ARRANGE
        loader = ConfigLoader()
        config_file = tmp_path / "empty.yaml"
        config_file.write_text("")

        # ACT
        result = loader.load_file(str(config_file))

        # ASSERT
        assert result == {}

    def test_load_file_not_found(self) -> None:
        """Teszt: Nem létező fájl → ConfigLoadError.

        ARRANGE: ConfigLoader példány.
        ACT & ASSERT: ConfigLoadError kivétel dobása nem létező fájl esetén.
        """
        # ARRANGE
        loader = ConfigLoader()

        # ACT & ASSERT
        with pytest.raises(ConfigLoadError) as exc_info:
            loader.load_file("/nonexistent/file.yaml")

        assert "nem található" in str(exc_info.value)

    def test_load_file_invalid_yaml(self, tmp_path: Path) -> None:
        """Teszt: Érvénytelen YAML → ConfigLoadError.

        ARRANGE: ConfigLoader példány, temp fájl érvénytelen YAML-lal.
        ACT & ASSERT: ConfigLoadError kivétel dobása.
        """
        # ARRANGE
        loader = ConfigLoader()
        config_file = tmp_path / "invalid.yaml"
        config_file.write_text("{{invalid yaml}}")

        # ACT & ASSERT
        with pytest.raises(ConfigLoadError):
            loader.load_file(str(config_file))

    @patch.object(ConfigLoader, "_decrypt_sops_file")
    def test_load_file_sops_success(self, mock_decrypt: Mock, tmp_path: Path) -> None:
        """Teszt: SOPS fájl betöltése mockolással.

        ARRANGE: ConfigLoader példány, temp SOPS fájl, mock dekódolás.
        ACT: load_file() hívása.
        ASSERT: Dekódolt tartalom helyes visszaadása.
        """
        # ARRANGE
        loader = ConfigLoader()
        config_file = tmp_path / "secrets.yaml.sops"
        config_file.write_text("")  # SOPS fájl (tartalom nem számít, mock-olt)

        mock_decrypt.return_value = "api_key: secret123\n"

        # ACT
        result = loader.load_file(str(config_file))

        # ASSERT
        assert result == {"api_key": "secret123"}
        mock_decrypt.assert_called_once_with(str(config_file))


class TestConfigLoaderLoad:
    """load() metódus tesztek (könyvtár betöltés)."""

    def test_load_directory_success(self, tmp_path: Path) -> None:
        """Teszt: Könyvtár betöltése namespace struktúrával.

        ARRANGE: ConfigLoader példány, temp könyvtár több YAML fájllal.
        ACT: load() hívása.
        ASSERT: Namespace-elt dict struktúra visszaadása.
        """
        # ARRANGE
        loader = ConfigLoader()
        config_dir = tmp_path / "configs"
        config_dir.mkdir()

        (config_dir / "database.yaml").write_text("host: localhost\n")
        (config_dir / "logging.yaml").write_text("level: INFO\n")

        # ACT
        result = loader.load(str(config_dir))

        # ASSERT
        assert "database" in result
        assert "logging" in result
        assert result["database"] == {"host": "localhost"}
        assert result["logging"] == {"level": "INFO"}

    def test_load_directory_empty(self, tmp_path: Path) -> None:
        """Teszt: Üres könyvtár → üres dict.

        ARRANGE: ConfigLoader példány, üres temp könyvtár.
        ACT: load() hívása.
        ASSERT: Üres dict visszaadása.
        """
        # ARRANGE
        loader = ConfigLoader()
        config_dir = tmp_path / "empty_configs"
        config_dir.mkdir()

        # ACT
        result = loader.load(str(config_dir))

        # ASSERT
        assert result == {}

    def test_load_directory_not_found(self) -> None:
        """Teszt: Nem létező könyvtár → ConfigLoadError.

        ARRANGE: ConfigLoader példány.
        ACT & ASSERT: ConfigLoadError kivétel dobása nem létező könyvtár esetén.
        """
        # ARRANGE
        loader = ConfigLoader()

        # ACT & ASSERT
        with pytest.raises(ConfigLoadError) as exc_info:
            loader.load("/nonexistent/configs")

        assert "nem található" in str(exc_info.value)

    @patch.object(ConfigLoader, "_decrypt_sops_file")
    def test_load_mixed_plain_and_sops(self, mock_decrypt: Mock, tmp_path: Path) -> None:
        """Teszt: Plain + SOPS fájlok együtt.

        ARRANGE: ConfigLoader példány, temp könyvtár plain + SOPS fájlokkal.
        ACT: load() hívása.
        ASSERT: Mind a plain, mind a SOPS fájlok helyes betöltése.
        """
        # ARRANGE
        loader = ConfigLoader()
        config_dir = tmp_path / "configs"
        config_dir.mkdir()

        (config_dir / "public.yaml").write_text("app_name: MyApp\n")
        (config_dir / "secrets.yaml.sops").write_text("")  # Mock SOPS fájl

        mock_decrypt.return_value = "api_key: secret\n"

        # ACT
        result = loader.load(str(config_dir))

        # ASSERT
        assert "public" in result
        assert "secrets" in result
        assert result["public"] == {"app_name": "MyApp"}
        assert result["secrets"] == {"api_key": "secret"}
