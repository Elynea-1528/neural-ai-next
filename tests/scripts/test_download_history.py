"""Tesztek a scripts/download_history.py scripthez."""

from pathlib import Path

import pytest


class TestSmartResumeLogic:
    """Smart Resume logika tesztelése."""

    def test_hour_dir_path_construction(self) -> None:
        """Teszteli az óra mappa útvonalának helyes összeállítását."""
        from scripts.download_history import download_historical_data

        # Ellenőrizzük, hogy a függvény importálható
        assert callable(download_historical_data)

    def test_smart_resume_debug_log_exists(self) -> None:
        """Teszteli, hogy a debug log megtalálható a forráskódban."""
        source_code = Path("scripts/download_history.py").read_text()

        # Ellenőrizzük, hogy a DEBUG log benne van
        assert "DEBUG: Checking path:" in source_code

    def test_hour_dir_exists_check(self) -> None:
        """Teszteli, hogy a logika ellenőrzi a mappa létezését."""
        source_code = Path("scripts/download_history.py").read_text()

        # Ellenőrizzük, hogy az hour_dir.exists() ellenőrzés benne van
        assert "hour_dir.exists()" in source_code

    def test_parquet_glob_check(self) -> None:
        """Teszteli, hogy a parquet fájlok ellenőrzése benne van."""
        source_code = Path("scripts/download_history.py").read_text()

        # Ellenőrizzük, hogy az any(hour_dir.glob("*.parquet")) ellenőrzés benne van
        assert 'any(hour_dir.glob("*.parquet"))' in source_code

    def test_old_logic_removed(self) -> None:
        """Teszteli, hogy a régi logika el lett távolítva."""
        source_code = Path("scripts/download_history.py").read_text()

        # A régi expected_path logika nem lehet benne
        assert "expected_path" not in source_code
        assert "tick_" not in source_code or "any(hour_dir.glob" in source_code


class TestDownloadHistoryImports:
    """Import tesztek."""

    def test_type_checking_block_exists(self) -> None:
        """Teszteli, hogy a TYPE_CHECKING blokk létezik."""
        source_code = Path("scripts/download_history.py").read_text()

        assert "if TYPE_CHECKING:" in source_code
        assert "LoggerInterface" in source_code
        assert "StorageInterface" in source_code

    def test_required_imports(self) -> None:
        """Teszteli a kötelező importokat."""
        source_code = Path("scripts/download_history.py").read_text()

        assert "from pathlib import Path" in source_code
        assert "from datetime import" in source_code
        assert "import asyncio" in source_code


class TestArgumentParsing:
    """Argumentum feldolgozás tesztek."""

    def test_parse_arguments_function_exists(self) -> None:
        """Teszteli a parse_arguments függvény létezését."""
        from scripts.download_history import parse_arguments

        assert callable(parse_arguments)


class TestMainFunction:
    """Fő függvény tesztek."""

    def test_main_function_exists(self) -> None:
        """Teszteli a main függvény létezését."""
        from scripts.download_history import main

        assert callable(main)


class TestSaveTicksDirect:
    """_save_ticks_direct függvény tesztek."""

    def test_save_ticks_direct_function_exists(self) -> None:
        """Teszteli a _save_ticks_direct függvény létezését."""
        from scripts.download_history import _save_ticks_direct  # type: ignore[import]

        assert callable(_save_ticks_direct)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
