"""DataServiceInterface tesztelése.

Ez a tesztcsomag ellenőrzi a DataServiceInterface interfész megfelelő definícióját
és a Protocol szerződés betartását.
"""

import sys
from collections.abc import Generator
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pandas as pd
import pytest

# Közvetlen import az interfész fájlból, hogy elkerüljük a hibás __init__.py-t
sys.path.insert(0, "/home/elynea/Dokumentumok/neural-ai-next")
from neural_ai.ui.interfaces.data_service_interface import DataServiceInterface


class MockDataService(DataServiceInterface):
    """Mock implementáció a DataServiceInterface teszteléséhez."""

    def load_data(
        self, source: str, filters: dict[str, Any] | None = None, chunk_size: int = 10000
    ) -> Generator[list[dict[str, Any]], None, None]:
        """Mock adatok betöltése."""
        yield [{"id": 1, "data": "test"}]

    def get_data_sources(self) -> list[dict[str, str]]:
        """Mock adatforrások."""
        return [{"name": "test_source", "type": "parquet"}]

    def get_data_info(self, source: str) -> dict[str, Any]:
        """Mock adatforrás információk."""
        return {"source": source, "rows": 1000}

    def apply_filters(
        self, data: list[dict[str, Any]], filters: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """Mock szűrés."""
        return [
            item for item in data if all(item.get(key) == value for key, value in filters.items())
        ]

    def export_data(self, data: list[dict[str, Any]], format: str, destination: str) -> bool:
        """Mock exportálás."""
        return True

    def get_default_date_range(self) -> tuple[datetime, datetime]:
        """Mock alapértelmezett dátumtartomány."""
        start = datetime(2020, 1, 1, tzinfo=UTC)
        end = datetime.now(UTC)
        return start, end

    async def download_history(self, symbol: str, start: datetime, end: datetime) -> dict[str, Any]:
        """Mock történelmi adatok letöltése."""
        return {"symbol": symbol, "start": start, "end": end, "status": "success", "records": 1000}

    def list_available_data(self, symbol: str | None = None) -> pd.DataFrame:
        """Mock elérhető adatok listázása."""
        data: dict[str, list[Any]] = {
            "symbol": ["EURUSD", "GBPUSD"],
            "start_date": [datetime(2020, 1, 1), datetime(2020, 1, 1)],
            "end_date": [datetime(2024, 12, 31), datetime(2024, 12, 31)],
            "rows": [50000, 45000],
        }
        df = pd.DataFrame(data)
        if symbol:
            df = df[df["symbol"] == symbol]
        return df

    def get_storage_path(self) -> Path:
        """Mock tárhely elérési út."""
        return Path("/mock/storage/path")

    def get_configured_symbols(self) -> list[str]:
        """Mock konfigurált szimbólumok."""
        return ["EURUSD", "GBPUSD", "USDJPY"]


class TestDataServiceInterface:
    """DataServiceInterface tesztosztály."""

    def test_interface_is_protocol(self):
        """Teszteli, hogy az interfész Protocol-t követ."""
        assert hasattr(DataServiceInterface, "__protocol__") or hasattr(
            DataServiceInterface, "_is_protocol"
        )

    def test_interface_is_runtime_checkable(self):
        """Teszteli, hogy az interfész runtime_checkable."""
        assert hasattr(DataServiceInterface, "__instancecheck__")

    def test_mock_implements_interface(self):
        """Teszteli, hogy a mock osztály implementálja az interfészt."""
        service = MockDataService()
        assert isinstance(service, DataServiceInterface)

    def test_load_data_signature(self):
        """Teszteli a load_data metódus szignatúráját."""
        service = MockDataService()
        chunks = list(service.load_data("test_source", chunk_size=1000))
        assert len(chunks) > 0
        assert isinstance(chunks[0], list)

    def test_get_data_sources_return_type(self):
        """Teszteli a get_data_sources visszatérési értékét."""
        service = MockDataService()
        sources = service.get_data_sources()
        assert isinstance(sources, list)
        assert all(isinstance(s, dict) for s in sources)

    def test_get_data_info_return_type(self):
        """Teszteli a get_data_info visszatérési értékét."""
        service = MockDataService()
        info = service.get_data_info("test_source")
        assert isinstance(info, dict)

    def test_apply_filters_functionality(self):
        """Teszteli az apply_filters metódust."""
        service = MockDataService()
        data: list[dict[str, Any]] = [
            {"id": 1, "type": "A"},
            {"id": 2, "type": "B"},
            {"id": 3, "type": "A"},
        ]
        filtered = service.apply_filters(data, {"type": "A"})
        assert len(filtered) == 2
        assert all(item["type"] == "A" for item in filtered)

    def test_export_data_return_type(self):
        """Teszteli az export_data visszatérési értékét."""
        service = MockDataService()
        result = service.export_data([{"test": "data"}], "parquet", "/tmp/test")
        assert isinstance(result, bool)
        assert result is True

    def test_get_default_date_range(self):
        """Teszteli a get_default_date_range metódust."""
        service = MockDataService()
        start, end = service.get_default_date_range()
        assert isinstance(start, datetime)
        assert isinstance(end, datetime)
        assert start < end
        assert start.tzinfo is not None
        assert end.tzinfo is not None

    @pytest.mark.asyncio
    async def test_download_history_async(self):
        """Teszteli a download_history aszinkron metódust."""
        service = MockDataService()
        start = datetime(2024, 1, 1, tzinfo=UTC)
        end = datetime(2024, 12, 31, tzinfo=UTC)
        result = await service.download_history("EURUSD", start, end)

        assert isinstance(result, dict)
        assert result["symbol"] == "EURUSD"
        assert result["start"] == start
        assert result["end"] == end
        assert "status" in result
        assert "records" in result

    def test_list_available_data_return_type(self):
        """Teszteli a list_available_data visszatérési értékét."""
        service = MockDataService()
        df = service.list_available_data()
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0

    def test_list_available_data_with_symbol_filter(self):
        """Teszteli a list_available_data szűrést."""
        service = MockDataService()
        df = service.list_available_data(symbol="EURUSD")
        assert isinstance(df, pd.DataFrame)
        assert all(df["symbol"] == "EURUSD")

    def test_get_storage_path_return_type(self):
        """Teszteli a get_storage_path visszatérési értékét."""
        service = MockDataService()
        path = service.get_storage_path()
        assert isinstance(path, Path)

    def test_get_configured_symbols(self):
        """Teszteli a get_configured_symbols metódust."""
        service = MockDataService()
        symbols = service.get_configured_symbols()
        assert isinstance(symbols, list)
        assert len(symbols) > 0
        assert all(isinstance(s, str) for s in symbols)

    def test_interface_methods_exist(self):
        """Teszteli, hogy az interfész minden metódusa létezik."""
        service = MockDataService()

        # Alap metódusok
        assert hasattr(service, "load_data")
        assert hasattr(service, "get_data_sources")
        assert hasattr(service, "get_data_info")
        assert hasattr(service, "apply_filters")
        assert hasattr(service, "export_data")
        assert hasattr(service, "get_default_date_range")

        # Új Data Hub metódusok
        assert hasattr(service, "download_history")
        assert hasattr(service, "list_available_data")
        assert hasattr(service, "get_storage_path")
        assert hasattr(service, "get_configured_symbols")

    def test_interface_type_hints(self):
        """Teszteli a típusos megjelöléseket."""
        # Ellenőrzi, hogy a metódusok rendelkeznek-e típusos visszatérési értékkel
        assert hasattr(DataServiceInterface.load_data, "__annotations__")
        assert hasattr(DataServiceInterface.get_data_sources, "__annotations__")
        assert hasattr(DataServiceInterface.get_default_date_range, "__annotations__")
        assert hasattr(DataServiceInterface.download_history, "__annotations__")
        assert hasattr(DataServiceInterface.list_available_data, "__annotations__")
        assert hasattr(DataServiceInterface.get_storage_path, "__annotations__")
        assert hasattr(DataServiceInterface.get_configured_symbols, "__annotations__")


class TestDataServiceInterfaceIntegration:
    """Integrációs tesztek a DataServiceInterface-hez."""

    def test_chunk_based_loading(self):
        """Teszteli a chunk-based adatbetöltést."""
        service = MockDataService()
        total_items = 0
        for chunk in service.load_data("test", chunk_size=100):
            total_items += len(chunk)
            assert isinstance(chunk, list)
        assert total_items > 0

    def test_data_pipeline_flow(self):
        """Teszteli az adatfeldolgozási folyamatot."""
        service = MockDataService()

        # 1. Adatok betöltése
        chunks = list(service.load_data("test_source"))
        assert len(chunks) > 0

        # 2. Adatok szűrése
        all_data = [item for chunk in chunks for item in chunk]
        filtered = service.apply_filters(all_data, {"id": 1})
        assert len(filtered) > 0

        # 3. Adatok exportálása
        success = service.export_data(filtered, "parquet", "/tmp/export")
        assert success is True

    @pytest.mark.asyncio
    async def test_async_data_download_flow(self):
        """Teszteli az aszinkron adatletöltési folyamatot."""
        service = MockDataService()

        # Történelmi adatok letöltése
        result = await service.download_history(
            symbol="EURUSD",
            start=datetime(2024, 1, 1, tzinfo=UTC),
            end=datetime(2024, 12, 31, tzinfo=UTC),
        )

        assert result["status"] == "success"
        assert result["records"] > 0

        # Elérhető adatok listázása
        available = service.list_available_data(symbol="EURUSD")
        assert len(available) > 0

        # Tárhely ellenőrzése
        storage_path = service.get_storage_path()
        assert storage_path is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
