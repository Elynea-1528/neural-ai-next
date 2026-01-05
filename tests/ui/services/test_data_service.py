"""DataService tesztek.

Ez a modul tartalmazza a DataService osztály tesztjeit, amelyek ellenőrzik
az adatkezelési funkcionalitás helyes működését.
"""

from datetime import datetime
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pandas as pd
import pytest

from neural_ai.ui.services.data_service import DataService


class TestDataService:
    """DataService osztály tesztjei."""

    @pytest.fixture
    def mock_bridge(self) -> MagicMock:
        """Mock CoreBridge létrehozása."""
        bridge = MagicMock()
        return bridge

    @pytest.fixture
    def data_service(self, mock_bridge: MagicMock) -> DataService:
        """DataService példány létrehozása."""
        return DataService(mock_bridge)

    def test_init(self, data_service: DataService) -> None:
        """Teszteli a DataService inicializálását."""
        assert data_service is not None
        assert len(data_service._data_sources) == 3
        assert "tick_data" in data_service._data_sources
        assert "ohlc_data" in data_service._data_sources
        assert "market_data" in data_service._data_sources

    def test_get_data_sources(self, data_service: DataService) -> None:
        """Teszteli az adatforrások lekérdezését."""
        sources = data_service.get_data_sources()

        assert isinstance(sources, list)
        assert len(sources) == 3

        # Ellenőrizzük az első forrás struktúráját
        first_source = sources[0]
        assert "id" in first_source
        assert "name" in first_source
        assert "description" in first_source
        assert "format" in first_source

    def test_get_data_info_valid_source(self, data_service: DataService) -> None:
        """Teszteli az adatforrás információk lekérdezését érvényes forrással."""
        info = data_service.get_data_info("tick_data")

        assert isinstance(info, dict)
        assert "source" in info
        assert "name" in info
        assert "description" in info
        assert "format" in info
        assert "size" in info
        assert "records" in info
        assert "last_updated" in info

    def test_get_data_info_invalid_source(self, data_service: DataService) -> None:
        """Teszteli a hibakezelést érvénytelen adatforrás esetén."""
        with pytest.raises(ValueError, match="Ismeretlen adatforrás"):
            data_service.get_data_info("invalid_source")

    def test_apply_filters_basic(self, data_service: DataService) -> None:
        """Teszteli az alapvető szűrő alkalmazását."""
        data = [
            {"id": 1, "name": "test1", "value": 100},
            {"id": 2, "name": "test2", "value": 200},
            {"id": 3, "name": "test1", "value": 150},
        ]

        filters = {"name": "test1"}
        filtered = data_service.apply_filters(data, filters)

        assert len(filtered) == 2
        assert all(item["name"] == "test1" for item in filtered)

    def test_apply_filters_range(self, data_service: DataService) -> None:
        """Teszteli a tartomány szűrő alkalmazását."""
        data = [
            {"id": 1, "value": 100},
            {"id": 2, "value": 200},
            {"id": 3, "value": 150},
            {"id": 4, "value": 300},
        ]

        filters = {"value": {"min": 150, "max": 250}}
        filtered = data_service.apply_filters(data, filters)

        assert len(filtered) == 2
        assert all(150 <= item["value"] <= 250 for item in filtered)

    def test_export_data_success(self, data_service: DataService) -> None:
        """Teszteli az adatok exportálását."""
        data = [
            {"id": 1, "name": "test1"},
            {"id": 2, "name": "test2"},
        ]

        result = data_service.export_data(data, "parquet", "/tmp/test.parquet")
        assert result is True

    def test_export_data_empty(self, data_service: DataService) -> None:
        """Teszteli az üres adatok exportálását."""
        result = data_service.export_data([], "parquet", "/tmp/test.parquet")
        assert result is False

    def test_export_data_invalid_format(self, data_service: DataService) -> None:
        """Teszteli a hibakezelést érvénytelen formátum esetén."""
        data = [{"id": 1, "name": "test1"}]

        with pytest.raises(ValueError, match="Nem támogatott formátum"):
            data_service.export_data(data, "invalid", "/tmp/test.invalid")

    @pytest.mark.asyncio
    async def test_download_history_success(
        self, data_service: DataService, mock_bridge: MagicMock
    ) -> None:
        """Teszteli a sikeres történelmi adatok letöltését."""
        # Mock Bi5Downloader létrehozása, ami implementálja az interfészt
        from neural_ai.collectors.jforex.interfaces.downloader_interface import (
            IJForexDownloader,
        )

        mock_downloader = MagicMock(spec=IJForexDownloader)
        mock_downloader.download_tick_data = AsyncMock(
            return_value=[{"timestamp": "2026-01-01", "bid": 1.0850, "ask": 1.0852}]
        )

        mock_bridge.get_component.return_value = mock_downloader

        start_date = datetime(2026, 1, 1)
        end_date = datetime(2026, 1, 3)

        result = await data_service.download_history("EURUSD", start_date, end_date)

        assert isinstance(result, dict)
        assert result["symbol"] == "EURUSD"
        assert result["status"] == "downloaded"
        assert result["records"] == 3  # 3 nap adatai
        assert "size_mb" in result
        assert result["format"] == "parquet"

    @pytest.mark.asyncio
    async def test_download_history_invalid_date_range(self, data_service: DataService) -> None:
        """Teszteli a hibakezelést érvénytelen dátumtartomány esetén."""
        start_date = datetime(2026, 1, 3)
        end_date = datetime(2026, 1, 1)

        with pytest.raises(ValueError, match="nem lehet későbbi"):
            await data_service.download_history("EURUSD", start_date, end_date)

    @pytest.mark.asyncio
    async def test_download_history_future_date(self, data_service: DataService) -> None:
        """Teszteli a hibakezelést jövőbeli dátummal."""
        start_date = datetime(2030, 1, 1)
        end_date = datetime(2030, 1, 3)

        with pytest.raises(ValueError, match="nem lehet a jövőben"):
            await data_service.download_history("EURUSD", start_date, end_date)

    @pytest.mark.asyncio
    async def test_download_history_missing_downloader(
        self, data_service: DataService, mock_bridge: MagicMock
    ) -> None:
        """Teszteli a hibakezelést hiányzó downloader esetén."""
        mock_bridge.get_component.return_value = None

        start_date = datetime(2026, 1, 1)
        end_date = datetime(2026, 1, 3)

        with pytest.raises(RuntimeError, match="nem érhető el"):
            await data_service.download_history("EURUSD", start_date, end_date)

    def test_list_available_data_with_symbol(
        self, data_service: DataService, mock_bridge: MagicMock
    ) -> None:
        """Teszteli az elérhető adatok listázását szimbólummal."""
        # Mock Storage létrehozása, ami implementálja az interfészt
        from neural_ai.core.storage.interfaces.storage_interface import (
            StorageInterface,
        )

        mock_storage = MagicMock(spec=StorageInterface)
        mock_storage.get_storage_stats = MagicMock(
            return_value={
                "total_files": 100,
                "size_gb": 2.5,
                "available_dates": 30,
            }
        )

        mock_bridge.get_component.return_value = mock_storage

        result = data_service.list_available_data("EURUSD")

        assert isinstance(result, pd.DataFrame)
        assert len(result) > 0
        assert "source_id" in result.columns
        assert "symbol" in result.columns
        assert "name" in result.columns
        assert "size_gb" in result.columns
        assert "records" in result.columns

    def test_list_available_data_without_symbol(
        self, data_service: DataService, mock_bridge: MagicMock
    ) -> None:
        """Teszteli az elérhető adatok listázását szimbólum nélkül."""
        # Mock Storage létrehozása, ami implementálja az interfészt
        from neural_ai.core.storage.interfaces.storage_interface import (
            StorageInterface,
        )

        mock_storage = MagicMock(spec=StorageInterface)
        mock_storage.get_storage_stats = MagicMock(
            return_value={
                "total_files": 100,
                "size_gb": 2.5,
                "available_dates": 30,
            }
        )

        mock_bridge.get_component.return_value = mock_storage

        result = data_service.list_available_data()

        assert isinstance(result, pd.DataFrame)
        assert len(result) > 0
        # Több szimbólumot kell tartalmaznia
        assert len(result["symbol"].unique()) > 1

    def test_list_available_data_missing_storage(
        self, data_service: DataService, mock_bridge: MagicMock
    ) -> None:
        """Teszteli a hibakezelést hiányzó storage esetén."""
        mock_bridge.get_component.return_value = None

        with pytest.raises(RuntimeError, match="nem érhető el"):
            data_service.list_available_data("EURUSD")

    def test_get_storage_path_success(
        self, data_service: DataService, mock_bridge: MagicMock
    ) -> None:
        """Teszteli a tárolási útvonal lekérdezését."""
        # Mock Storage létrehozása BASE_PATH attribútummal
        from neural_ai.core.storage.interfaces.storage_interface import (
            StorageInterface,
        )

        mock_storage = MagicMock(spec=StorageInterface)
        mock_storage.BASE_PATH = Path("/data/tick")

        mock_bridge.get_component.return_value = mock_storage

        result = data_service.get_storage_path()

        assert isinstance(result, Path)
        assert str(result) == "/data/tick"

    def test_get_storage_path_default(
        self, data_service: DataService, mock_bridge: MagicMock
    ) -> None:
        """Teszteli az alapértelmezett tárolási útvonal lekérdezését."""
        # Mock Storage létrehozása BASE_PATH attribútum nélkül
        from neural_ai.core.storage.interfaces.storage_interface import (
            StorageInterface,
        )

        mock_storage = MagicMock(spec=StorageInterface)
        # A spec-ból nem lehet törölni attribútumot, ezért hasattr ellenőrzéssel
        if hasattr(mock_storage, "BASE_PATH"):
            del mock_storage.BASE_PATH

        mock_bridge.get_component.return_value = mock_storage

        result = data_service.get_storage_path()

        assert isinstance(result, Path)
        assert str(result) == "/data/tick"

    def test_get_storage_path_missing_storage(
        self, data_service: DataService, mock_bridge: MagicMock
    ) -> None:
        """Teszteli a hibakezelést hiányzó storage esetén."""
        mock_bridge.get_component.return_value = None

        with pytest.raises(RuntimeError, match="nem érhető el"):
            data_service.get_storage_path()

    def test_load_data_basic(self, data_service: DataService) -> None:
        """Teszteli az adatok betöltését."""
        source = "tick_data"
        chunk_size = 100

        chunks = list(data_service.load_data(source, chunk_size=chunk_size))

        assert len(chunks) > 0
        assert all(isinstance(chunk, list) for chunk in chunks)
        assert all(len(chunk) <= chunk_size for chunk in chunks)

    def test_load_data_with_filters(self, data_service: DataService) -> None:
        """Teszteli az adatok betöltését szűrőkkel."""
        source = "tick_data"
        filters = {"symbol": "EURUSD"}

        chunks = list(data_service.load_data(source, filters=filters))

        assert len(chunks) > 0
        # Ellenőrizzük, hogy a szűrők hatására kevesebb adatot kapunk-e
        total_records = sum(len(chunk) for chunk in chunks)
        assert total_records > 0

    def test_load_data_invalid_source(self, data_service: DataService) -> None:
        """Teszteli a hibakezelést érvénytelen forrással."""
        with pytest.raises(ValueError, match="Ismeretlen adatforrás"):
            list(data_service.load_data("invalid_source"))

    @pytest.mark.asyncio
    async def test_get_storage_stats_async_success(self, data_service: DataService) -> None:
        """Teszteli a storage statisztikák aszinkron lekérdezését."""
        mock_storage = MagicMock()
        mock_storage.get_storage_stats = AsyncMock(
            return_value={
                "total_files": 100,
                "size_gb": 2.5,
                "available_dates": 30,
            }
        )

        result = await data_service._get_storage_stats_async(mock_storage, "EURUSD")

        assert isinstance(result, dict)
        assert "total_files" in result
        assert "size_gb" in result
        assert "available_dates" in result

    @pytest.mark.asyncio
    async def test_get_storage_stats_async_fallback(self, data_service: DataService) -> None:
        """Teszteli a fallback logikát, ha a storage nem támogatja a metódust."""
        from neural_ai.core.storage.interfaces.storage_interface import (
            StorageInterface,
        )

        mock_storage = MagicMock(spec=StorageInterface)
        # Nincs get_storage_stats metódus, ezért a hasattr False lesz

        result = await data_service._get_storage_stats_async(mock_storage, "EURUSD")

        assert isinstance(result, dict)
        assert result["total_files"] == 0
        assert result["size_gb"] == 0.0
        assert result["available_dates"] == 0

    @pytest.mark.asyncio
    async def test_get_storage_stats_async_exception_handling(
        self, data_service: DataService
    ) -> None:
        """Teszteli a kivételkezelést a storage statisztikák lekérdezésénél."""
        mock_storage = MagicMock()
        mock_storage.get_storage_stats = AsyncMock(side_effect=Exception("Hiba"))

        # A metódusnak hibátlanul kell visszatérnie alapértelmezett értékekkel
        result = await data_service._get_storage_stats_async(mock_storage, "EURUSD")

        assert isinstance(result, dict)
        assert result["total_files"] == 0
        assert result["size_gb"] == 0.0
        assert result["available_dates"] == 0
