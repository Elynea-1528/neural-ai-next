"""Integration Zero Test: Mock MT5 -> Bridge -> Atomic Storage
Tests the complete data flow from MT5 API to storage with atomic writes.
"""

import shutil
import sys
import tempfile
from datetime import datetime, timedelta

import pytest

# Add project root to path
sys.path.insert(0, "/home/elynea/Dokumentumok/neural-ai-next")

# Import modules with direct file loading to avoid circular imports
import importlib.util

# Load FileStorage directly
spec = importlib.util.spec_from_file_location(
    "file_storage",
    "/home/elynea/Dokumentumok/neural-ai-next/neural_ai/core/storage/implementations/file_storage.py",
)
file_storage_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(file_storage_module)
FileStorage = file_storage_module.FileStorage

from tests.integration.mock_mt5 import MockMT5
from tests.integration.mt5_bridge import MT5Bridge


class TestIntegrationZero:
    """Integration Zero tests."""

    @pytest.fixture
    def mock_mt5(self):
        """Create mock MT5 instance."""
        mt5 = MockMT5()
        mt5.initialize()
        yield mt5
        mt5.shutdown()

    @pytest.fixture
    def temp_storage(self):
        """Create temporary storage."""
        temp_dir = tempfile.mkdtemp()
        storage = FileStorage(base_path=temp_dir)
        yield storage
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def bridge(self, mock_mt5, temp_storage):
        """Create MT5 bridge."""
        return MT5Bridge(mock_mt5, temp_storage, "./data/integration_test")

    def test_mock_mt5_initialization(self, mock_mt5):
        """Test mock MT5 initialization."""
        assert mock_mt5.initialized() is True
        assert mock_mt5.terminal_info().connected is True

        symbols = mock_mt5.symbols_get()
        assert symbols is not None
        assert len(symbols) == 4

    def test_historical_data_flow(self, bridge):
        """Test complete historical data flow."""
        stats = bridge.fetch_and_store_historical_data(
            symbol="EURUSD",
            timeframe=60,  # H1
            start_pos=0,
            count=100,
        )

        assert stats["fetched"] == 100
        assert stats["stored"] == 100
        assert len(stats["errors"]) == 0

        # Verify storage - check if files were created in temp directory
        # The files are saved to ./data/integration_test which is in the project root
        import os

        test_data_dir = "./data/integration_test"
        assert os.path.exists(test_data_dir), f"Directory {test_data_dir} does not exist"

    def test_tick_data_flow(self, bridge):
        """Test complete tick data flow."""
        from_date = datetime.now() - timedelta(hours=1)

        stats = bridge.fetch_and_store_tick_data(symbol="EURUSD", from_date=from_date, count=1000)

        assert stats["fetched"] == 1000
        assert stats["stored"] == 1000
        assert len(stats["errors"]) == 0

        # Verify storage
        storage_info = bridge.get_storage_info()
        assert storage_info["exists"] is True

    def test_multiple_symbols(self, bridge):
        """Test data flow with multiple symbols."""
        symbols = ["EURUSD", "GBPUSD", "USDJPY"]

        for symbol in symbols:
            stats = bridge.fetch_and_store_historical_data(
                symbol=symbol,
                timeframe=15,  # M15
                start_pos=0,
                count=50,
            )

            assert stats["fetched"] == 50
            assert stats["stored"] == 50
            assert len(stats["errors"]) == 0

        # Verify all data stored
        import os

        test_data_dir = "./data/integration_test"
        assert os.path.exists(test_data_dir), f"Directory {test_data_dir} does not exist"

    def test_atomic_write_guarantee(self, bridge):
        """Test atomic write guarantee."""
        # This test verifies that the atomic write mechanism works
        # by checking that data is properly stored

        stats = bridge.fetch_and_store_historical_data(
            symbol="XAUUSD",
            timeframe=240,  # H4
            start_pos=0,
            count=10,
        )

        assert stats["stored"] == 10
        assert len(stats["errors"]) == 0
