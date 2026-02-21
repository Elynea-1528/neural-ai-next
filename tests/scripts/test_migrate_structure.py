"""Migrate structure szkript teszt modul.

Ez a modul tartalmazza a migrate_structure.py szkript tesztjeit.
"""

import shutil
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from scripts.migrate_structure import main, migrate_tick_structure


class TestMigrateStructure:
    """Migrate structure szkript tesztjei."""

    @pytest.fixture
    def temp_base_dir(self):
        """Ideiglenes alap könyvtár létrehozása a tesztekhez."""
        tmpdir = tempfile.mkdtemp()
        yield Path(tmpdir)
        shutil.rmtree(tmpdir)

    @patch("scripts.migrate_structure.CoreComponentFactory.create_minimal")
    def test_migrate_tick_structure_no_base_dir(self, mock_create_minimal: MagicMock) -> None:
        """Teszteli a migrációt nem létező alapkönyvtár esetén."""
        mock_logger = MagicMock()
        mock_components = MagicMock()
        mock_components.logger = mock_logger
        mock_create_minimal.return_value = mock_components

        with patch("pathlib.Path.exists", return_value=False):
            migrate_tick_structure(mock_logger)

        mock_logger.error.assert_called_once_with("Az alapkönyvtár nem létezik: data/tick")

    @patch("scripts.migrate_structure.CoreComponentFactory.create_minimal")
    def test_migrate_tick_structure_no_symbol_dirs(self, mock_create_minimal: MagicMock) -> None:
        """Teszteli a migrációt szimbólum könyvtárak nélkül."""
        mock_logger = MagicMock()
        mock_components = MagicMock()
        mock_components.logger = mock_logger
        mock_create_minimal.return_value = mock_components

        with (
            patch("pathlib.Path.exists", return_value=True),
            patch("pathlib.Path.iterdir", return_value=[]),
        ):
            migrate_tick_structure(mock_logger)

        mock_logger.warning.assert_called_once_with(
            "Nem található szimbólum mappa a tick könyvtárban"
        )

    @patch("scripts.migrate_structure.CoreComponentFactory.create_minimal")
    def test_migrate_tick_structure_no_tick_dir(self, mock_create_minimal: MagicMock) -> None:
        """Teszteli a migrációt tick könyvtár nélküli szimbólum esetén."""
        mock_logger = MagicMock()
        mock_components = MagicMock()
        mock_components.logger = mock_logger
        mock_create_minimal.return_value = mock_components

        # Mock a szimbólum könyvtárat
        mock_symbol_dir = MagicMock()
        mock_symbol_dir.name = "EURUSD"
        mock_symbol_dir.is_dir.return_value = True

        # Mock hogy nem létezik tick almappa
        mock_symbol_dir.__truediv__.return_value.exists.return_value = False

        with (
            patch("pathlib.Path.exists", return_value=True),
            patch("pathlib.Path.iterdir", return_value=[mock_symbol_dir]),
        ):
            migrate_tick_structure(mock_logger)

        mock_logger.debug.assert_called_once_with("Nincs tick almappa a szimbólumnál: EURUSD")

    @patch("scripts.migrate_structure.CoreComponentFactory.create_minimal")
    def test_migrate_tick_structure_empty_tick_dir(self, mock_create_minimal: MagicMock) -> None:
        """Teszteli a migrációt üres tick könyvtár esetén."""
        mock_logger = MagicMock()
        mock_components = MagicMock()
        mock_components.logger = mock_logger
        mock_create_minimal.return_value = mock_components

        # Mock a szimbólum könyvtárat
        mock_symbol_dir = MagicMock()
        mock_symbol_dir.name = "EURUSD"
        mock_symbol_dir.is_dir.return_value = True

        # Mock tick almappa ami létezik és üres
        mock_tick_dir = MagicMock()
        mock_tick_dir.exists.return_value = True
        mock_tick_dir.is_dir.return_value = True
        mock_tick_dir.iterdir.return_value = []
        mock_tick_dir.rmdir.return_value = None

        mock_symbol_dir.__truediv__.side_effect = lambda path: {"tick": mock_tick_dir}.get(
            path, MagicMock()
        )

        with (
            patch("pathlib.Path.exists", return_value=True),
            patch("pathlib.Path.iterdir", return_value=[mock_symbol_dir]),
        ):
            migrate_tick_structure(mock_logger)

        mock_logger.info.assert_any_call("Üres tick mappa törlésre kerül: " + str(mock_tick_dir))
        mock_logger.info.assert_any_call("Sikeresen törölve: " + str(mock_tick_dir))
        mock_logger.info.assert_any_call(
            "Migráció befejezve. Feldolgozott: 1, Migrált: 1"
        )

    @patch("scripts.migrate_structure.CoreComponentFactory.create_minimal")
    @patch("shutil.move")
    def test_migrate_tick_structure_with_content(
        self, mock_move: MagicMock, mock_create_minimal: MagicMock
    ) -> None:
        """Teszteli a migrációt tick könyvtár tartalommal."""
        mock_logger = MagicMock()
        mock_components = MagicMock()
        mock_components.logger = mock_logger
        mock_create_minimal.return_value = mock_components

        # Mock a szimbólum könyvtárat
        mock_symbol_dir = MagicMock()
        mock_symbol_dir.name = "EURUSD"
        mock_symbol_dir.is_dir.return_value = True

        # Mock tick almappa tartalommal
        mock_tick_dir = MagicMock()
        mock_tick_dir.exists.return_value = True
        mock_tick_dir.is_dir.return_value = True
        mock_subdir = MagicMock()
        mock_subdir.name = "2023"
        mock_tick_dir.iterdir.return_value = [mock_subdir]
        mock_tick_dir.rmdir.return_value = None

        # Mock target könyvtár ami nem létezik
        mock_target_dir = MagicMock()
        mock_target_dir.exists.return_value = False

        mock_symbol_dir.__truediv__.side_effect = lambda path: {
            "tick": mock_tick_dir,
            "2023": mock_target_dir,
        }.get(path, MagicMock())

        with (
            patch("pathlib.Path.exists", return_value=True),
            patch("pathlib.Path.iterdir", return_value=[mock_symbol_dir]),
        ):
            migrate_tick_structure(mock_logger)

        mock_move.assert_called_once()
        mock_logger.info.assert_any_call(
            "Tartalom áthelyezése: " + str(mock_tick_dir) + " -> " + str(mock_symbol_dir)
        )
        mock_logger.info.assert_any_call(
            "Áthelyezve: " + str(mock_subdir) + " -> " + str(mock_target_dir)
        )
        mock_logger.info.assert_any_call("Tick mappa törölve: " + str(mock_tick_dir))

    @patch("scripts.migrate_structure.CoreComponentFactory.create_minimal")
    def test_migrate_tick_structure_tick_not_dir(self, mock_create_minimal: MagicMock) -> None:
        """Teszteli a migrációt amikor a tick 'útvonal' nem mappa."""
        mock_logger = MagicMock()
        mock_components = MagicMock()
        mock_components.logger = mock_logger
        mock_create_minimal.return_value = mock_components

        # Mock a szimbólum könyvtárat
        mock_symbol_dir = MagicMock()
        mock_symbol_dir.name = "EURUSD"
        mock_symbol_dir.is_dir.return_value = True

        # Mock tick almappa ami létezik de nem dir
        mock_tick_dir = MagicMock()
        mock_tick_dir.exists.return_value = True
        mock_tick_dir.is_dir.return_value = False

        mock_symbol_dir.__truediv__.return_value = mock_tick_dir

        with (
            patch("pathlib.Path.exists", return_value=True),
            patch("pathlib.Path.iterdir", return_value=[mock_symbol_dir]),
        ):
            migrate_tick_structure(mock_logger)

        mock_logger.warning.assert_called_once_with(f"A tick 'útvonal' nem mappa: {mock_tick_dir}")

    @patch("scripts.migrate_structure.CoreComponentFactory.create_minimal")
    def test_migrate_tick_structure_rmdir_exception_empty(
        self, mock_create_minimal: MagicMock
    ) -> None:
        """Teszteli a migrációt OSError esetén üres tick mappa törlésekor."""
        mock_logger = MagicMock()
        mock_components = MagicMock()
        mock_components.logger = mock_logger
        mock_create_minimal.return_value = mock_components

        # Mock a szimbólum könyvtárat
        mock_symbol_dir = MagicMock()
        mock_symbol_dir.name = "EURUSD"
        mock_symbol_dir.is_dir.return_value = True

        # Mock tick almappa ami létezik és üres, de rmdir hibázik
        mock_tick_dir = MagicMock()
        mock_tick_dir.exists.return_value = True
        mock_tick_dir.is_dir.return_value = True
        mock_tick_dir.iterdir.return_value = []
        mock_tick_dir.rmdir.side_effect = OSError("Permission denied")

        mock_symbol_dir.__truediv__.return_value = mock_tick_dir

        with (
            patch("pathlib.Path.exists", return_value=True),
            patch("pathlib.Path.iterdir", return_value=[mock_symbol_dir]),
        ):
            migrate_tick_structure(mock_logger)

        mock_logger.error.assert_called_once_with(
            f"Hiba a tick mappa törlésekor {mock_tick_dir}: Permission denied"
        )

    @patch("scripts.migrate_structure.CoreComponentFactory.create_minimal")
    def test_migrate_tick_structure_target_exists(self, mock_create_minimal: MagicMock) -> None:
        """Teszteli a migrációt amikor a célmappa már létezik."""
        mock_logger = MagicMock()
        mock_components = MagicMock()
        mock_components.logger = mock_logger
        mock_create_minimal.return_value = mock_components

        # Mock a szimbólum könyvtárat
        mock_symbol_dir = MagicMock()
        mock_symbol_dir.name = "EURUSD"
        mock_symbol_dir.is_dir.return_value = True

        # Mock tick almappa tartalommal
        mock_tick_dir = MagicMock()
        mock_tick_dir.exists.return_value = True
        mock_tick_dir.is_dir.return_value = True
        mock_subdir = MagicMock()
        mock_subdir.name = "2023"
        mock_tick_dir.iterdir.return_value = [mock_subdir]

        # Mock target könyvtár ami már létezik
        mock_target_dir = MagicMock()
        mock_target_dir.exists.return_value = True

        mock_symbol_dir.__truediv__.side_effect = lambda path: {
            "tick": mock_tick_dir,
            "2023": mock_target_dir,
        }.get(path, MagicMock())

        with (
            patch("pathlib.Path.exists", return_value=True),
            patch("pathlib.Path.iterdir", return_value=[mock_symbol_dir]),
        ):
            migrate_tick_structure(mock_logger)

        mock_logger.warning.assert_called_once_with(
            f"A célmappa már létezik, átugrás: {mock_target_dir}"
        )

    @patch("scripts.migrate_structure.CoreComponentFactory.create_minimal")
    @patch("shutil.move")
    def test_migrate_tick_structure_move_exception(
        self, mock_move: MagicMock, mock_create_minimal: MagicMock
    ) -> None:
        """Teszteli a migrációt OSError esetén az áthelyezéskor."""
        mock_logger = MagicMock()
        mock_components = MagicMock()
        mock_components.logger = mock_logger
        mock_create_minimal.return_value = mock_components

        mock_move.side_effect = OSError("Permission denied")

        # Mock a szimbólum könyvtárat
        mock_symbol_dir = MagicMock()
        mock_symbol_dir.name = "EURUSD"
        mock_symbol_dir.is_dir.return_value = True

        # Mock tick almappa tartalommal
        mock_tick_dir = MagicMock()
        mock_tick_dir.exists.return_value = True
        mock_tick_dir.is_dir.return_value = True
        mock_subdir = MagicMock()
        mock_subdir.name = "2023"
        mock_tick_dir.iterdir.return_value = [mock_subdir]

        # Mock target könyvtár ami nem létezik
        mock_target_dir = MagicMock()
        mock_target_dir.exists.return_value = False

        mock_symbol_dir.__truediv__.side_effect = lambda path: {
            "tick": mock_tick_dir,
            "2023": mock_target_dir,
        }.get(path, MagicMock())

        with (
            patch("pathlib.Path.exists", return_value=True),
            patch("pathlib.Path.iterdir", return_value=[mock_symbol_dir]),
        ):
            migrate_tick_structure(mock_logger)

        mock_logger.error.assert_called_once_with(
            f"Hiba az áthelyezéskor {mock_subdir} -> {mock_target_dir}: Permission denied"
        )

    @patch("scripts.migrate_structure.CoreComponentFactory.create_minimal")
    def test_migrate_tick_structure_rmdir_exception_after_move(
        self, mock_create_minimal: MagicMock
    ) -> None:
        """Teszteli a migrációt OSError esetén tick mappa törlésekor tartalom áthelyezése után."""
        mock_logger = MagicMock()
        mock_components = MagicMock()
        mock_components.logger = mock_logger
        mock_create_minimal.return_value = mock_components

        # Mock a szimbólum könyvtárat
        mock_symbol_dir = MagicMock()
        mock_symbol_dir.name = "EURUSD"
        mock_symbol_dir.is_dir.return_value = True

        # Mock tick almappa tartalommal
        mock_tick_dir = MagicMock()
        mock_tick_dir.exists.return_value = True
        mock_tick_dir.is_dir.return_value = True
        mock_subdir = MagicMock()
        mock_subdir.name = "2023"
        mock_tick_dir.iterdir.return_value = [mock_subdir]
        mock_tick_dir.rmdir.side_effect = OSError("Permission denied")

        # Mock target könyvtár ami nem létezik
        mock_target_dir = MagicMock()
        mock_target_dir.exists.return_value = False

        mock_symbol_dir.__truediv__.side_effect = lambda path: {
            "tick": mock_tick_dir,
            "2023": mock_target_dir,
        }.get(path, MagicMock())

        with (
            patch("pathlib.Path.exists", return_value=True),
            patch("pathlib.Path.iterdir", return_value=[mock_symbol_dir]),
            patch("shutil.move") as mock_move,
        ):
            migrate_tick_structure(mock_logger)

        mock_move.assert_called_once()
        mock_logger.error.assert_called_once_with(
            f"Hiba a tick mappa törlésekor {mock_tick_dir}: Permission denied"
        )

    @patch("scripts.migrate_structure.CoreComponentFactory.create_minimal")
    def test_main_success(self, mock_create_minimal: MagicMock) -> None:
        """Teszteli a main függvényt sikeres végrehajtás esetén."""
        mock_logger = MagicMock()
        mock_components = MagicMock()
        mock_components.logger = mock_logger
        mock_create_minimal.return_value = mock_components

        with patch("scripts.migrate_structure.migrate_tick_structure") as mock_migrate:
            result = main()

        mock_migrate.assert_called_once_with(mock_logger)
        assert result == 0

    @patch("scripts.migrate_structure.CoreComponentFactory.create_minimal")
    def test_main_logger_none(self, mock_create_minimal: MagicMock) -> None:
        """Teszteli a main függvényt None logger esetén."""
        mock_components = MagicMock()
        mock_components.logger = None
        mock_create_minimal.return_value = mock_components

        with patch("builtins.print") as mock_print:
            result = main()

        mock_print.assert_called_once_with("Hiba: Logger komponens nem inicializálódott")
        assert result == 1

    @patch("scripts.migrate_structure.CoreComponentFactory.create_minimal")
    def test_main_exception(self, mock_create_minimal: MagicMock) -> None:
        """Teszteli a main függvényt kivétel esetén."""
        mock_components = MagicMock()
        mock_components.logger = MagicMock()
        mock_create_minimal.side_effect = Exception("Test error")

        with patch("builtins.print") as mock_print, patch("traceback.print_exc") as mock_traceback:
            result = main()

        mock_print.assert_called_once_with("Váratlan hiba: Test error")
        mock_traceback.assert_called_once()
        assert result == 1
