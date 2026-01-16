"""Data reset szkript teszt modul.

Ez a modul tartalmazza a data_reset.py szkript tesztjeit.
"""

import os
import shutil
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from scripts.data_reset import (
    check_directory_exists,
    create_directories_if_needed,
    main,
    remove_logs,
    remove_tick_data,
)


class TestDataReset:
    """Data reset szkript tesztjei."""

    @pytest.fixture
    def temp_base_dir(self):
        """Ideiglenes alap könyvtár létrehozása a tesztekhez."""
        tmpdir = tempfile.mkdtemp()
        yield Path(tmpdir)
        shutil.rmtree(tmpdir)

    def test_check_directory_exists_true(self, temp_base_dir: Path) -> None:
        """Teszteli a könyvtár létezésének ellenőrzését létező könyvtár esetén."""
        test_dir = temp_base_dir / "existing_dir"
        test_dir.mkdir()

        assert check_directory_exists(str(test_dir)) is True

    def test_check_directory_exists_false_no_dir(self, temp_base_dir: Path) -> None:
        """Teszteli a könyvtár létezésének ellenőrzését nem létező könyvtár esetén."""
        test_dir = temp_base_dir / "nonexistent_dir"

        assert check_directory_exists(str(test_dir)) is False

    def test_check_directory_exists_false_file(self, temp_base_dir: Path) -> None:
        """Teszteli a könyvtár létezésének ellenőrzését fájl esetén."""
        test_file = temp_base_dir / "test_file.txt"
        test_file.write_text("test")

        assert check_directory_exists(str(test_file)) is False

    @patch("scripts.data_reset.shutil.rmtree")
    @patch("scripts.data_reset.check_directory_exists")
    def test_remove_tick_data_exists(
        self, mock_check_dir: MagicMock, mock_rmtree: MagicMock
    ) -> None:
        """Teszteli a tick adatok törlését létező könyvtár esetén."""
        mock_check_dir.return_value = True

        result = remove_tick_data()

        assert result is True
        mock_rmtree.assert_called_once_with("data/tick")

    @patch("scripts.data_reset.check_directory_exists")
    def test_remove_tick_data_not_exists(self, mock_check_dir: MagicMock) -> None:
        """Teszteli a tick adatok törlését nem létező könyvtár esetén."""
        mock_check_dir.return_value = False

        result = remove_tick_data()

        assert result is True  # Nem hiba, ha nem létezik

    @patch("scripts.data_reset.shutil.rmtree")
    @patch("scripts.data_reset.check_directory_exists")
    def test_remove_tick_data_exception(
        self, mock_check_dir: MagicMock, mock_rmtree: MagicMock
    ) -> None:
        """Teszteli a tick adatok törlését kivétel esetén."""
        mock_check_dir.return_value = True
        mock_rmtree.side_effect = Exception("Mocked error")

        result = remove_tick_data()

        assert result is False

    @patch("scripts.data_reset.os.listdir")
    @patch("scripts.data_reset.os.path.isdir")
    @patch("scripts.data_reset.os.path.isfile")
    @patch("scripts.data_reset.os.path.islink")
    @patch("scripts.data_reset.os.remove")
    @patch("scripts.data_reset.shutil.rmtree")
    @patch("scripts.data_reset.check_directory_exists")
    def test_remove_logs_exists_with_files(
        self,
        mock_check_dir: MagicMock,
        mock_rmtree: MagicMock,
        mock_remove: MagicMock,
        mock_islink: MagicMock,
        mock_isfile: MagicMock,
        mock_isdir: MagicMock,
        mock_listdir: MagicMock,
    ) -> None:
        """Teszteli a logok törlését létező könyvtár esetén fájlokkal."""
        mock_check_dir.return_value = True
        mock_listdir.return_value = ["file1.txt", "file2.log", "subdir"]
        mock_isfile.side_effect = [
            True,
            True,
            False,
        ]  # file1.txt, file2.log fájlok, subdir könyvtár
        mock_islink.return_value = False
        mock_isdir.return_value = True

        result = remove_logs()

        assert result is True
        mock_remove.assert_any_call(os.path.join("logs", "file1.txt"))
        mock_remove.assert_any_call(os.path.join("logs", "file2.log"))
        mock_rmtree.assert_called_once_with(os.path.join("logs", "subdir"))

    @patch("scripts.data_reset.check_directory_exists")
    def test_remove_logs_not_exists(self, mock_check_dir: MagicMock) -> None:
        """Teszteli a logok törlését nem létező könyvtár esetén."""
        mock_check_dir.return_value = False

        result = remove_logs()

        assert result is True  # Nem hiba, ha nem létezik

    @patch("scripts.data_reset.os.listdir")
    @patch("scripts.data_reset.check_directory_exists")
    def test_remove_logs_exception(
        self, mock_check_dir: MagicMock, mock_listdir: MagicMock
    ) -> None:
        """Teszteli a logok törlését kivétel esetén."""
        mock_check_dir.return_value = True
        mock_listdir.side_effect = Exception("Mocked error")

        result = remove_logs()

        assert result is False

    @patch("pathlib.Path.mkdir")
    def test_create_directories_if_needed(self, mock_mkdir: MagicMock) -> None:
        """Teszteli a szükséges könyvtárak létrehozását."""
        create_directories_if_needed()

        # Ellenőrizzük, hogy a mkdir hívások megtörténtek exist_ok=True-val
        assert mock_mkdir.call_count == 2
        mock_mkdir.assert_any_call(parents=True, exist_ok=True)

    @patch("scripts.data_reset.remove_logs")
    @patch("scripts.data_reset.remove_tick_data")
    @patch("scripts.data_reset.create_directories_if_needed")
    @patch("builtins.print")
    def test_main_success(
        self,
        mock_print: MagicMock,
        mock_create_dirs: MagicMock,
        mock_remove_tick: MagicMock,
        mock_remove_logs: MagicMock,
    ) -> None:
        """Teszteli a main függvényt sikeres végrehajtás esetén."""
        mock_remove_tick.return_value = True
        mock_remove_logs.return_value = True

        with patch("sys.exit") as mock_exit:
            main()

        mock_create_dirs.assert_called_once()
        mock_remove_tick.assert_called_once()
        mock_remove_logs.assert_called_once()
        mock_exit.assert_not_called()

        # Ellenőrizzük a siker üzenetet
        success_messages = [call.args[0] for call in mock_print.call_args_list]
        assert any("✅ Adat reset sikeres!" in msg for msg in success_messages)

    @patch("scripts.data_reset.remove_logs")
    @patch("scripts.data_reset.remove_tick_data")
    @patch("scripts.data_reset.create_directories_if_needed")
    @patch("builtins.print")
    def test_main_failure_tick_data(
        self,
        mock_print: MagicMock,
        mock_create_dirs: MagicMock,
        mock_remove_tick: MagicMock,
        mock_remove_logs: MagicMock,
    ) -> None:
        """Teszteli a main függvényt tick adatok törlésének sikertelensége esetén."""
        mock_remove_tick.return_value = False
        mock_remove_logs.return_value = True

        with patch("sys.exit") as mock_exit:
            main()

        mock_exit.assert_called_once_with(1)

        # Ellenőrizzük a hiba üzenetet
        error_messages = [call.args[0] for call in mock_print.call_args_list]
        assert any(
            "❌ Adat reset részben vagy teljesen sikertelen." in msg for msg in error_messages
        )

    @patch("scripts.data_reset.remove_logs")
    @patch("scripts.data_reset.remove_tick_data")
    @patch("scripts.data_reset.create_directories_if_needed")
    @patch("builtins.print")
    def test_main_failure_logs(
        self,
        mock_print: MagicMock,
        mock_create_dirs: MagicMock,
        mock_remove_tick: MagicMock,
        mock_remove_logs: MagicMock,
    ) -> None:
        """Teszteli a main függvényt logok törlésének sikertelensége esetén."""
        mock_remove_tick.return_value = True
        mock_remove_logs.return_value = False

        with patch("sys.exit") as mock_exit:
            main()

        mock_exit.assert_called_once_with(1)

    @patch("scripts.data_reset.remove_logs")
    @patch("scripts.data_reset.remove_tick_data")
    @patch("scripts.data_reset.create_directories_if_needed")
    @patch("builtins.print")
    def test_main_failure_both(
        self,
        mock_print: MagicMock,
        mock_create_dirs: MagicMock,
        mock_remove_tick: MagicMock,
        mock_remove_logs: MagicMock,
    ) -> None:
        """Teszteli a main függvényt mindkét törlés sikertelensége esetén."""
        mock_remove_tick.return_value = False
        mock_remove_logs.return_value = False

        with patch("sys.exit") as mock_exit:
            main()

        mock_exit.assert_called_once_with(1)
