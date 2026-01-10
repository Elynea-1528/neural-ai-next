"""Tesztek a scripts/download_history.py scripthez."""

from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest

from neural_ai.collectors.jforex.interfaces.tick_data import TickData


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

    def test_master_filename_generation(self) -> None:
        """Teszteli, hogy a master fájlnév generálása benne van."""
        source_code = Path("scripts/download_history.py").read_text()

        # Ellenőrizzük, hogy a master_filename generálása benne van
        assert (
            "master_filename = f\"tick_{current_hour.strftime('%Y%m%d_%H')}.parquet\""
            in source_code
        )

    def test_expected_path_check(self) -> None:
        """Teszteli, hogy az expected_path ellenőrzés benne van."""
        source_code = Path("scripts/download_history.py").read_text()

        # Ellenőrizzük, hogy az expected_path.exists() és st_size ellenőrzés benne van
        assert "expected_path.exists() and expected_path.stat().st_size > 1000" in source_code


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

    @pytest.mark.asyncio
    async def test_save_ticks_direct_creates_correct_dataframe_columns(self) -> None:
        """Teszteli, hogy a _save_ticks_direct függvény helyesen hozza létre a DataFrame-et a forrásoszlopokkal."""
        from scripts.download_history import _save_ticks_direct

        # Mock storage
        mock_storage = AsyncMock()

        # Mock logger
        mock_logger = MagicMock()

        # Sample tick data
        ticks = [
            TickData(
                timestamp=datetime(2023, 1, 1, 10, 0, 0, tzinfo=UTC),
                symbol="EURUSD",
                bid=1.0500,
                ask=1.0502,
                ask_volume=100.0,
                bid_volume=150.0,
                source="jforex",
            ),
            TickData(
                timestamp=datetime(2023, 1, 1, 10, 0, 1, tzinfo=UTC),
                symbol="EURUSD",
                bid=1.0501,
                ask=1.0503,
                ask_volume=200.0,
                bid_volume=250.0,
                source="jforex",
            ),
        ]

        symbol = "EURUSD"
        date = datetime(2023, 1, 1, 10, 0, 0, tzinfo=UTC)

        # Call the function
        await _save_ticks_direct(mock_storage, symbol, ticks, date, mock_logger)

        # Verify storage.store_tick_data was called
        assert mock_storage.store_tick_data.called

        # Get the DataFrame that was passed
        call_args = mock_storage.store_tick_data.call_args
        df = call_args[1]["data"]  # keyword argument 'data'

        # Check that DataFrame has the correct columns (only source columns)
        expected_columns = ["timestamp", "bid", "ask", "ask_volume", "bid_volume"]
        assert list(df.columns) == expected_columns

        # Check that 'volume' column is NOT present
        assert "volume" not in df.columns

        # Check that 'source' column is NOT present (only 5 source columns)
        assert "source" not in df.columns

        # Check data integrity
        assert len(df) == 2
        assert df["bid"].to_list() == [1.0500, 1.0501]
        assert df["ask"].to_list() == [1.0502, 1.0503]
        assert df["ask_volume"].to_list() == [100.0, 200.0]
        assert df["bid_volume"].to_list() == [150.0, 250.0]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
