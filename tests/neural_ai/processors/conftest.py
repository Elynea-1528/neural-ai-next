"""Pytest fixtures a processors tesztekhez."""

from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock

import polars as pl
import pytest


@pytest.fixture(scope="function")
def sample_tick_df() -> pl.DataFrame:
    """Minta Tick DataFrame teszteléshez.

    Returns:
        Polars DataFrame 1000 tick adattal (bid, ask, bid_volume, ask_volume).
    """
    dates = [datetime(2024, 1, 1) + timedelta(seconds=i) for i in range(1000)]
    return pl.DataFrame({
        "timestamp": dates,
        "bid": [1.1000 + i * 0.00001 for i in range(1000)],
        "ask": [1.1002 + i * 0.00001 for i in range(1000)],
        "bid_volume": [10 + i for i in range(1000)],
        "ask_volume": [12 + i for i in range(1000)],
    })


@pytest.fixture(scope="function")
def sample_ohlcv_df() -> pl.DataFrame:
    """Minta OHLCV DataFrame teszteléshez.

    Returns:
        Polars DataFrame 100 OHLCV gyertyával.
    """
    dates = [datetime(2024, 1, 1) + timedelta(minutes=i) for i in range(100)]
    return pl.DataFrame({
        "timestamp": dates,
        "open": [1.1000 + i * 0.0001 for i in range(100)],
        "high": [1.1010 + i * 0.0001 for i in range(100)],
        "low": [1.0990 + i * 0.0001 for i in range(100)],
        "close": [1.1005 + i * 0.0001 for i in range(100)],
        "volume": [1000 + i * 10 for i in range(100)],
    })


@pytest.fixture(scope="function")
def empty_tick_df() -> pl.DataFrame:
    """Üres Tick DataFrame teszteléshez.

    Returns:
        Üres Polars DataFrame a megfelelő sémával.
    """
    return pl.DataFrame({
        "timestamp": [],
        "bid": [],
        "ask": [],
        "bid_volume": [],
        "ask_volume": [],
    })


@pytest.fixture(scope="function")
def mock_logger() -> MagicMock:
    """Mock logger teszteléshez.

    Returns:
        MagicMock logger objektum.
    """
    logger = MagicMock()
    logger.info = MagicMock()
    logger.warning = MagicMock()
    logger.error = MagicMock()
    logger.debug = MagicMock()
    return logger


@pytest.fixture(scope="function")
def mock_storage(sample_tick_df: pl.DataFrame) -> MagicMock:
    """Mock storage teszteléshez.

    Args:
        sample_tick_df: Minta tick DataFrame fixture.

    Returns:
        MagicMock storage objektum read_tick_data metódussal.
    """
    storage = MagicMock()
    # Async mock a read_tick_data metódushoz
    storage.read_tick_data = AsyncMock(return_value=sample_tick_df)
    return storage


@pytest.fixture(scope="function")
def mock_storage_empty() -> MagicMock:
    """Mock storage üres adattal teszteléshez.

    Returns:
        MagicMock storage objektum üres DataFrame-mel.
    """
    storage = MagicMock()
    empty_df = pl.DataFrame({
        "timestamp": [],
        "bid": [],
        "ask": [],
        "bid_volume": [],
        "ask_volume": [],
    })
    storage.read_tick_data = AsyncMock(return_value=empty_df)
    return storage


@pytest.fixture(scope="function")
def mock_storage_no_method() -> MagicMock:
    """Mock storage read_tick_data metódus nélkül.

    Returns:
        MagicMock storage objektum read_tick_data nélkül.
    """
    storage = MagicMock()
    # Töröljük a read_tick_data attribútumot
    del storage.read_tick_data
    return storage


@pytest.fixture(scope="function")
def mock_config() -> MagicMock:
    """Mock config teszteléshez.

    Returns:
        MagicMock config objektum.
    """
    config = MagicMock()
    config.get = MagicMock(return_value={"window": 10, "threshold": 2.0})
    return config
