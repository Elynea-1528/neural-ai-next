"""Tesztek a DataService osztályhoz."""

from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING, Any
from unittest.mock import AsyncMock, MagicMock

import polars as pl
import pytest

from neural_ai.ui.services.data_service import DataService

if TYPE_CHECKING:
    pass


class TestDataService:
    """DataService osztály tesztjei."""

    @pytest.fixture
    def mock_bridge(self) -> MagicMock:
        """Mock CoreBridge létrehozása."""
        bridge: MagicMock = MagicMock()
        return bridge

    @pytest.fixture
    def data_service(self, mock_bridge: MagicMock) -> DataService:
        """DataService példány létrehozása."""
        return DataService(mock_bridge)

    def test_init(self, mock_bridge: MagicMock) -> None:
        """Teszteli a DataService inicializálását."""
        service: DataService = DataService(mock_bridge)
        assert service._bridge == mock_bridge  # type: ignore
        assert "tick_data" in service._data_sources  # type: ignore
        assert "ohlc_data" in service._data_sources  # type: ignore
        assert "market_data" in service._data_sources  # type: ignore

    def test_get_data_sources(self, data_service: DataService) -> None:
        """Teszteli az adatforrások lekérdezését."""
        sources: list[dict[str, Any]] = data_service.get_data_sources()
        assert len(sources) == 3
        assert sources[0]["id"] == "tick_data"
        assert sources[0]["name"] == "Tick Adatok"

    def test_get_data_info_valid_source(self, data_service: DataService) -> None:
        """Teszteli az adatforrás információk lekérdezését érvényes forrással."""
        info: dict[str, Any] = data_service.get_data_info("tick_data")
        assert info["source"] == "tick_data"
        assert info["name"] == "Tick Adatok"
        assert info["format"] == "parquet"

    def test_get_data_info_invalid_source(self, data_service: DataService) -> None:
        """Teszteli a hibakezelést érvénytelen adatforrás esetén."""
        with pytest.raises(ValueError, match="Ismeretlen adatforrás"):
            data_service.get_data_info("invalid_source")

    def test_apply_filters_exact_match(self, data_service: DataService) -> None:
        """Teszteli a szűrést pontos egyezéssel."""
        data: list[dict[str, Any]] = [
            {"id": 1, "name": "test1", "value": 100},
            {"id": 2, "name": "test2", "value": 200},
        ]
        filters: dict[str, Any] = {"name": "test1"}
        filtered: list[dict[str, Any]] = data_service.apply_filters(data, filters)
        assert len(filtered) == 1
        assert filtered[0]["id"] == 1

    def test_apply_filters_range(self, data_service: DataService) -> None:
        """Teszteli a szűrést tartomány alapján."""
        data: list[dict[str, Any]] = [
            {"id": 1, "name": "test1", "value": 100},
            {"id": 2, "name": "test2", "value": 200},
            {"id": 3, "name": "test3", "value": 300},
        ]
        filters: dict[str, Any] = {"value": {"min": 150, "max": 250}}
        filtered: list[dict[str, Any]] = data_service.apply_filters(data, filters)
        assert len(filtered) == 1
        assert filtered[0]["id"] == 2

    def test_export_data_success(self, data_service: DataService) -> None:
        """Teszteli az adatok exportálását."""
        data: list[dict[str, Any]] = [{"id": 1, "value": 100}]
        success: bool = data_service.export_data(data, "parquet", "/tmp/test.parquet")
        assert success is True

    def test_export_data_empty(self, data_service: DataService) -> None:
        """Teszteli az exportálást üres adatokkal."""
        success: bool = data_service.export_data([], "parquet", "/tmp/test.parquet")
        assert success is False

    def test_export_data_invalid_format(self, data_service: DataService) -> None:
        """Teszteli a hibakezelést érvénytelen formátum esetén."""
        data: list[dict[str, Any]] = [{"id": 1, "value": 100}]
        with pytest.raises(ValueError, match="Nem támogatott formátum"):
            data_service.export_data(data, "xml", "/tmp/test.xml")

    @pytest.mark.asyncio
    async def test_download_history_success_and_save(self, mock_bridge: MagicMock) -> None:
        """Teszteli a sikeres történelmi adatletöltést és mentést."""
        # Importáljuk az interfészt a típusellenőrzéshez
        from neural_ai.collectors.jforex.interfaces.downloader_interface import IJForexDownloader
        from neural_ai.core.storage.interfaces.storage_interface import StorageInterface

        # Mock komponensek létrehozása az interfész specifikációval
        mock_downloader: AsyncMock = AsyncMock(spec=IJForexDownloader)
        mock_storage: AsyncMock = AsyncMock(spec=StorageInterface)

        # Mock tick adatok
        mock_tick_1: MagicMock = MagicMock()
        mock_tick_1.timestamp = datetime.now(UTC)
        mock_tick_1.bid = 1.0850
        mock_tick_1.ask = 1.0852
        mock_tick_1.ask_volume = 1.5
        mock_tick_1.bid_volume = 2.5
        mock_tick_1.source = "jforex"

        mock_tick_2: MagicMock = MagicMock()
        mock_tick_2.timestamp = datetime.now(UTC)
        mock_tick_2.bid = 1.0851
        mock_tick_2.ask = 1.0853
        mock_tick_2.ask_volume = 2.0
        mock_tick_2.bid_volume = 3.0
        mock_tick_2.source = "jforex"

        mock_tick_data: list[MagicMock] = [mock_tick_1, mock_tick_2]

        # Mock metódusok visszatérési értékeinek beállítása
        mock_downloader.download_tick_data.return_value = mock_tick_data
        mock_storage.store_tick_data = AsyncMock()  # type: ignore
        mock_bridge.get_component.side_effect = lambda name: {  # type: ignore
            "bi5_downloader": mock_downloader,
            "parquet_storage": mock_storage,
        }.get(name)

        # DataService példányosítása és teszt futtatása
        service: DataService = DataService(mock_bridge)
        start_date: datetime = datetime.now(UTC) - timedelta(days=1)
        end_date: datetime = datetime.now(UTC)

        result: dict[str, Any] = await service.download_history("EURUSD", start_date, end_date)

        # Ellenőrzések
        assert result["symbol"] == "EURUSD"
        assert result["status"] == "downloaded"
        assert result["records"] == 4  # 2 nap * 2 tick adat
        assert result["format"] == "parquet"
        assert result["successful_dates"] == 2  # start és end nap is sikeres
        assert result["failed_dates"] == 0
        assert result["total_days"] == 2  # start és end nap is beleszámít

        # Ellenőrizzük, hogy a download_tick_data meghívásra került
        mock_downloader.download_tick_data.assert_awaited()

        # Ellenőrizzük, hogy a store_tick_data meghívásra került a helyes paraméterekkel
        mock_storage.store_tick_data.assert_awaited()
        # Az utolsó hívás paramétereit ellenőrizzük
        call_args = mock_storage.store_tick_data.await_args
        assert call_args.kwargs["symbol"] == "EURUSD"
        assert call_args.kwargs["unique_id"] is not None
        # Ellenőrizzük, hogy a data argumentum egy Polars DataFrame
        assert isinstance(call_args.kwargs["data"], pl.DataFrame)
        df: pl.DataFrame = call_args.kwargs["data"]
        assert "timestamp" in df.columns
        assert "bid" in df.columns
        assert "ask" in df.columns
        assert "ask_volume" in df.columns
        assert "bid_volume" in df.columns
        assert "source" in df.columns
        assert "volume" in df.columns  # A technikai volume oszlop
        assert len(df) == 2  # Két tick adatunk van

    @pytest.mark.asyncio
    async def test_download_history_invalid_date_range(self, data_service: DataService) -> None:
        """Teszteli a hibakezelést érvénytelen dátumtartomány esetén."""
        start_date: datetime = datetime.now(UTC)
        end_date: datetime = datetime.now(UTC) - timedelta(days=1)

        with pytest.raises(ValueError, match="nem lehet későbbi"):
            await data_service.download_history("EURUSD", start_date, end_date)

    @pytest.mark.asyncio
    async def test_download_history_future_start_date(self, data_service: DataService) -> None:
        """Teszteli a hibakezelést jövőbeli kezdődátum esetén."""
        start_date: datetime = datetime.now(UTC) + timedelta(days=1)
        end_date: datetime = datetime.now(UTC) + timedelta(days=2)

        with pytest.raises(ValueError, match="nem lehet a jövőben"):
            await data_service.download_history("EURUSD", start_date, end_date)

    @pytest.mark.asyncio
    async def test_download_history_downloader_not_available(self, mock_bridge: MagicMock) -> None:
        """Teszteli a hibakezelést, ha a letöltő komponens nem érhető el."""
        mock_bridge.get_component.return_value = None
        service: DataService = DataService(mock_bridge)

        with pytest.raises(RuntimeError, match="Bi5Downloader komponens nem érhető el"):
            await service.download_history(
                "EURUSD", datetime.now(UTC) - timedelta(days=1), datetime.now(UTC)
            )

    @pytest.mark.asyncio
    async def test_download_history_storage_not_available(self, mock_bridge: MagicMock) -> None:
        """Teszteli a hibakezelést, ha a tároló komponens nem érhető el."""
        from neural_ai.collectors.jforex.interfaces.downloader_interface import IJForexDownloader

        mock_downloader: AsyncMock = AsyncMock(spec=IJForexDownloader)
        mock_downloader.download_tick_data.return_value = []
        mock_bridge.get_component.side_effect = lambda name: {  # type: ignore
            "bi5_downloader": mock_downloader,
            "parquet_storage": None,
        }.get(name)
        service: DataService = DataService(mock_bridge)

        with pytest.raises(RuntimeError, match="ParquetStorage komponens nem érhető el"):
            await service.download_history(
                "EURUSD", datetime.now(UTC) - timedelta(days=1), datetime.now(UTC)
            )

    @pytest.mark.asyncio
    async def test_download_history_no_data_for_date(self, mock_bridge: MagicMock) -> None:
        """Teszteli a viselkedést, ha egy adott dátumra nincs adat."""
        from neural_ai.collectors.jforex.interfaces.downloader_interface import IJForexDownloader
        from neural_ai.core.storage.interfaces.storage_interface import StorageInterface

        mock_downloader: AsyncMock = AsyncMock(spec=IJForexDownloader)
        mock_storage: AsyncMock = AsyncMock(spec=StorageInterface)
        mock_storage.store_tick_data = AsyncMock()  # type: ignore
        mock_downloader.download_tick_data.return_value = []  # Nincs adat
        mock_bridge.get_component.side_effect = lambda name: {  # type: ignore
            "bi5_downloader": mock_downloader,
            "parquet_storage": mock_storage,
        }.get(name)

        service: DataService = DataService(mock_bridge)
        start_date: datetime = datetime.now(UTC) - timedelta(days=1)
        end_date: datetime = datetime.now(UTC)

        result: dict[str, Any] = await service.download_history("EURUSD", start_date, end_date)

        # Ellenőrizzük, hogy a letöltés "failed" státuszú lett,
        # mert minden dátumra üres adatok jöttek
        assert result["status"] == "failed"
        assert result["failed_dates"] == 2
        assert result["successful_dates"] == 0
        # Ellenőrizzük, hogy a storage mentést nem hívták meg, mert nincs adat
        mock_storage.store_tick_data.assert_not_awaited()

    def test_load_data(self, data_service: DataService) -> None:
        """Teszteli az adatok betöltését chunk-okban."""
        chunks: list[list[dict[str, Any]]] = list(
            data_service.load_data("tick_data", chunk_size=100)
        )
        assert len(chunks) > 0
        assert all(isinstance(chunk, list) for chunk in chunks)

    def test_load_data_invalid_source(self, data_service: DataService) -> None:
        """Teszteli a hibakezelést érvénytelen forrás esetén az adatbetöltésnél."""
        with pytest.raises(ValueError, match="Ismeretlen adatforrás"):
            list(data_service.load_data("invalid_source"))
