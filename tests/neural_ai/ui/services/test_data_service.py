"""Unit tesztek a DataService osztályhoz."""

from datetime import datetime
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pandas as pd
import pytest

from neural_ai.core.config.interfaces.types import DataServiceConfig, UIJForexConfig
from neural_ai.ui.services.data_service import DataService


class TestDataService:
    """Tesztek a DataService osztályhoz."""

    def test_initialization_with_config(self) -> None:
        """Teszteli a DataService inicializálását konfigurációval."""
        logger = MagicMock()
        config = DataServiceConfig(jforex=UIJForexConfig(symbols=None, date_range=None))
        core_components = MagicMock()

        service = DataService(logger=logger, config=config, core_components=core_components)

        assert service._logger is logger  # pyright: ignore[reportPrivateUsage]
        assert service._config is config  # pyright: ignore[reportPrivateUsage]
        assert service._core_components is core_components  # pyright: ignore[reportPrivateUsage]

    def test_initialization_without_config(self) -> None:
        """Teszteli a DataService inicializálását konfiguráció nélkül."""
        logger = MagicMock()
        core_components = MagicMock()

        service = DataService(logger=logger, config=None, core_components=core_components)

        assert service._logger is logger  # pyright: ignore[reportPrivateUsage]
        assert service._config is not None  # pyright: ignore[reportPrivateUsage]
        assert service._core_components is core_components  # pyright: ignore[reportPrivateUsage]

    def test_core_components_property(self) -> None:
        """Teszteli a core_components property-t."""
        core_components = MagicMock()
        service = DataService(logger=MagicMock(), config=None, core_components=core_components)

        assert service.core_components is core_components

    def test_data_sources_property(self) -> None:
        """Teszteli a data_sources property-t."""
        service = DataService(logger=MagicMock(), config=None, core_components=MagicMock())

        sources = service.data_sources

        assert isinstance(sources, dict)
        assert "tick_data" in sources
        assert "ohlc_data" in sources
        assert "market_data" in sources

    def test_load_data_with_chunking(self) -> None:
        """Teszteli az adatok betöltését chunking-gal."""
        service = DataService(logger=MagicMock(), config=None, core_components=MagicMock())

        mock_df = pd.DataFrame({"col1": range(100)})

        with patch.object(service, "_generate_mock_data", return_value=mock_df):
            chunks = list(service.load_data(source="tick_data", chunk_size=10))

        assert len(chunks) == 10
        assert all(isinstance(chunk, pd.DataFrame) for chunk in chunks)

    def test_get_data_sources(self) -> None:
        """Teszteli az adatforrások lekérdezését."""
        service = DataService(logger=MagicMock(), config=None, core_components=MagicMock())

        sources = service.get_data_sources()

        assert isinstance(sources, list)
        assert len(sources) > 0
        assert all("id" in source for source in sources)

    def test_get_data_info_success(self) -> None:
        """Teszteli az adatforrás információk lekérdezését."""
        service = DataService(logger=MagicMock(), config=None, core_components=MagicMock())

        info = service.get_data_info(source="tick_data")

        assert info["source"] == "tick_data"
        assert info["name"] == "Tick Adatok"
        assert "records" in info

    def test_get_data_info_invalid_source(self) -> None:
        """Teszteli az adatforrás információk lekérdezését érvénytelen forrással."""
        service = DataService(logger=MagicMock(), config=None, core_components=MagicMock())

        with pytest.raises(ValueError, match="Ismeretlen adatforrás"):
            service.get_data_info(source="invalid_source")

    def test_apply_filters_with_filters(self) -> None:
        """Teszteli a szűrők alkalmazását."""
        service = DataService(logger=MagicMock(), config=None, core_components=MagicMock())

        mock_data: list[dict[str, Any]] = [{"col1": 5, "col2": 15}, {"col1": 3, "col2": 13}]
        filters = {"col1": 5}

        result = service.apply_filters(data=mock_data, filters=filters)

        assert isinstance(result, list)
        assert len(result) <= len(mock_data)

    def test_apply_filters_without_filters(self) -> None:
        """Teszteli a szűrők alkalmazását szűrők nélkül."""
        service = DataService(logger=MagicMock(), config=None, core_components=MagicMock())

        mock_data: list[dict[str, Any]] = [{"col1": i} for i in range(10)]

        result = service.apply_filters(data=mock_data, filters={})

        assert isinstance(result, list)
        assert len(result) == len(mock_data)

    def test_export_data(self) -> None:
        """Teszteli az adatok exportálását."""
        service = DataService(logger=MagicMock(), config=None, core_components=MagicMock())

        mock_data: list[dict[str, Any]] = [{"col1": 1}, {"col1": 2}, {"col1": 3}]

        with patch("pathlib.Path.write_text"):
            result = service.export_data(
                data=mock_data, format="json", destination="/tmp/test.json"
            )
            assert result is True

    def test_get_default_date_range(self) -> None:
        """Teszteli az alapértelmezett dátumtartomány lekérdezését."""
        service = DataService(logger=MagicMock(), config=None, core_components=MagicMock())

        start_date, end_date = service.get_default_date_range()

        assert isinstance(start_date, datetime)
        assert isinstance(end_date, datetime)
        assert start_date < end_date

    def test_list_available_data_with_symbol(self) -> None:
        """Teszteli az elérhető adatok listázását szimbólum szűréssel."""
        service = DataService(logger=MagicMock(), config=None, core_components=MagicMock())

        # Mock storage with proper StorageInterface
        from neural_ai.data.storage.interfaces.storage_interface import StorageInterface

        mock_storage = MagicMock(spec=StorageInterface)
        mock_storage.get_storage_stats = AsyncMock(
            return_value={"total_files": 10, "size_gb": 1.5, "available_dates": 30}
        )

        # Mock core_components.get_component
        service._core_components.get_component = MagicMock(return_value=mock_storage)  # pyright: ignore[reportPrivateUsage]

        result = service.list_available_data(symbol="EURUSD")

        assert isinstance(result, pd.DataFrame)
        assert len(result) > 0

    def test_list_available_data_without_symbol(self) -> None:
        """Teszteli az elérhető adatok listázását szimbólum szűrés nélkül."""
        service = DataService(logger=MagicMock(), config=None, core_components=MagicMock())

        # Mock storage with proper StorageInterface
        from neural_ai.data.storage.interfaces.storage_interface import StorageInterface

        mock_storage = MagicMock(spec=StorageInterface)
        mock_storage.get_storage_stats = AsyncMock(
            return_value={"total_files": 5, "size_gb": 0.8, "available_dates": 15}
        )

        # Mock core_components.get_component
        service._core_components.get_component = MagicMock(return_value=mock_storage)  # pyright: ignore[reportPrivateUsage]

        result = service.list_available_data()

        assert isinstance(result, pd.DataFrame)
        assert len(result) > 0

    def test_get_storage_path(self) -> None:
        """Teszteli a tárolási útvonal lekérdezését."""
        service = DataService(logger=MagicMock(), config=None, core_components=MagicMock())

        # Mock storage with proper StorageInterface
        from neural_ai.data.storage.interfaces.storage_interface import StorageInterface

        mock_storage = MagicMock(spec=StorageInterface)
        mock_storage.BASE_PATH = Path("/data/tick")

        # Mock core_components.get_component
        service._core_components.get_component = MagicMock(return_value=mock_storage)  # pyright: ignore[reportPrivateUsage]

        path = service.get_storage_path()

        assert isinstance(path, Path)
        assert str(path) == "/data/tick"

    def test_get_configured_symbols(self) -> None:
        """Teszteli a konfigurált szimbólumok lekérdezését."""
        logger = MagicMock()
        config = DataServiceConfig(
            jforex=UIJForexConfig(symbols=["EURUSD", "GBPUSD"], date_range=None)
        )
        core_components = MagicMock()

        service = DataService(logger=logger, config=config, core_components=core_components)

        symbols = service.get_configured_symbols()

        assert isinstance(symbols, list)
        assert len(symbols) == 2
        assert "EURUSD" in symbols

    def test_get_configured_symbols_no_config(self) -> None:
        """Teszteli a szimbólumok lekérdezését konfiguráció nélkül."""
        service = DataService(logger=MagicMock(), config=None, core_components=MagicMock())

        symbols = service.get_configured_symbols()

        assert isinstance(symbols, list)
        assert len(symbols) == 1
        assert symbols[0] == "EURUSD"
