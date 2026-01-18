"""Data Service tesztelése.

Ez a modul a DataService osztály tesztjeit tartalmazza.
"""

import unittest
from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock, Mock, patch

import pandas as pd

from neural_ai.ui.services.data_service import DataService


class TestDataService(unittest.TestCase):
    """DataService osztály tesztjei."""

    def setUp(self) -> None:
        """Teszt előkészítése."""
        self.mock_bridge = Mock()
        self.data_service = DataService(self.mock_bridge)

    def test_init(self) -> None:
        """Teszteli a DataService inicializálását."""
        self.assertEqual(self.data_service.bridge, self.mock_bridge)
        self.assertIn("tick_data", self.data_service.data_sources)
        self.assertIn("ohlc_data", self.data_service.data_sources)
        self.assertIn("market_data", self.data_service.data_sources)

    def test_load_data(self) -> None:
        """Teszteli az adatok betöltését."""
        chunks = list(self.data_service.load_data("tick_data", chunk_size=100))
        self.assertGreater(len(chunks), 0)
        self.assertIsInstance(chunks[0], list)

    def test_load_data_invalid_source(self) -> None:
        """Teszteli a hibakezelést érvénytelen adatforrás esetén."""
        with self.assertRaises(ValueError):
            list(self.data_service.load_data("invalid_source"))

    def test_get_data_sources(self) -> None:
        """Teszteli az adatforrások lekérdezését."""
        sources = self.data_service.get_data_sources()
        self.assertIsInstance(sources, list)
        self.assertEqual(len(sources), 3)
        self.assertEqual(sources[0]["id"], "tick_data")

    def test_get_data_info(self) -> None:
        """Teszteli az adatforrás információk lekérdezését."""
        info = self.data_service.get_data_info("tick_data")
        self.assertIsInstance(info, dict)
        self.assertIn("name", info)
        self.assertIn("description", info)
        self.assertIn("format", info)

    def test_get_data_info_invalid_source(self) -> None:
        """Teszteli a hibakezelést érvénytelen adatforrás esetén."""
        with self.assertRaises(ValueError):
            self.data_service.get_data_info("invalid_source")

    def test_apply_filters(self) -> None:
        """Teszteli a szűrők alkalmazását."""
        data = [
            {"symbol": "EURUSD", "price": 1.08},
            {"symbol": "GBPUSD", "price": 1.28},
            {"symbol": "EURUSD", "price": 1.09},
        ]
        filters = {"symbol": "EURUSD"}
        filtered = self.data_service.apply_filters(data, filters)
        self.assertEqual(len(filtered), 2)
        self.assertTrue(all(item["symbol"] == "EURUSD" for item in filtered))

    def test_apply_filters_range(self) -> None:
        """Teszteli a tartomány szűrést."""
        data = [
            {"price": 1.08},
            {"price": 1.15},
            {"price": 1.20},
        ]
        filters = {"price": {"min": 1.10, "max": 1.18}}
        filtered = self.data_service.apply_filters(data, filters)
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["price"], 1.15)

    def test_export_data(self) -> None:
        """Teszteli az adatok exportálását."""
        data = [{"symbol": "EURUSD", "price": 1.08}]
        result = self.data_service.export_data(data, "csv", "/tmp/test.csv")
        self.assertTrue(result)

    def test_export_data_invalid_format(self) -> None:
        """Teszteli a hibakezelést érvénytelen formátum esetén."""
        data = [{"symbol": "EURUSD", "price": 1.08}]
        with self.assertRaises(ValueError):
            self.data_service.export_data(data, "invalid", "/tmp/test.invalid")

    def test_export_data_empty(self) -> None:
        """Teszteli az üres adatok exportálását."""
        result = self.data_service.export_data([], "csv", "/tmp/test.csv")
        self.assertFalse(result)

    @patch("asyncio.run")
    def test_list_available_data(self, mock_run: MagicMock) -> None:
        """Teszteli az elérhető adatok listázását (csak tick_data)."""
        from neural_ai.data.storage.interfaces.storage_interface import StorageInterface

        mock_storage = Mock(spec=StorageInterface)
        mock_storage.get_storage_stats = Mock(
            return_value={
                "total_files": 10,
                "size_gb": 1.5,
                "available_dates": 30,
            }
        )
        self.mock_bridge.get_component.return_value = mock_storage

        mock_run.return_value = {
            "total_files": 10,
            "size_gb": 1.5,
            "available_dates": 30,
        }

        result = self.data_service.list_available_data()
        self.assertIsInstance(result, pd.DataFrame)
        self.assertGreater(len(result), 0)
        # Ellenőrzés: csak tick_data forrás van (nem ohlc_data vagy market_data)
        self.assertTrue(all(row["source_id"] == "tick_data" for row in result.to_dict("records")))
        # Ellenőrzés: rekord becslés 3530 (óránkénti átlag) * 10 fájl = 35300
        self.assertEqual(result["records"].iloc[0], 35300)

    @patch("asyncio.run")
    def test_list_available_data_with_symbol(self, mock_run: MagicMock) -> None:
        """Teszteli az elérhető adatok listázását egyedi szimbólummal."""
        from neural_ai.data.storage.interfaces.storage_interface import StorageInterface

        mock_storage = Mock(spec=StorageInterface)
        mock_storage.get_storage_stats = Mock(
            return_value={
                "total_files": 5,
                "size_gb": 0.75,
                "available_dates": 15,
            }
        )
        self.mock_bridge.get_component.return_value = mock_storage

        mock_run.return_value = {
            "total_files": 5,
            "size_gb": 0.75,
            "available_dates": 15,
        }

        result = self.data_service.list_available_data(symbol="EURUSD")
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 1)
        self.assertEqual(result["symbol"].iloc[0], "EURUSD")
        self.assertEqual(result["records"].iloc[0], 5 * 3530)  # 17650

    @patch("asyncio.run")
    def test_list_available_data_no_files(self, mock_run: MagicMock) -> None:
        """Teszteli az elérhető adatok listázását, ha nincs fájl."""
        from neural_ai.data.storage.interfaces.storage_interface import StorageInterface

        mock_storage = Mock(spec=StorageInterface)
        mock_storage.get_storage_stats = Mock(
            return_value={
                "total_files": 0,
                "size_gb": 0.0,
                "available_dates": 0,
            }
        )
        self.mock_bridge.get_component.return_value = mock_storage

        mock_run.return_value = {
            "total_files": 0,
            "size_gb": 0.0,
            "available_dates": 0,
        }

        result = self.data_service.list_available_data()
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 0)  # Nincs sor, mert nincs fájl

    def test_get_storage_path(self) -> None:
        """Teszteli a tárolási útvonal lekérdezését."""
        from neural_ai.data.storage.interfaces.storage_interface import StorageInterface

        mock_storage = Mock(spec=StorageInterface)
        mock_storage.BASE_PATH = "/data/tick"
        self.mock_bridge.get_component.return_value = mock_storage

        result = self.data_service.get_storage_path()
        self.assertIsNotNone(result)
        self.assertEqual(str(result), "/data/tick")

    def test_get_storage_path_default(self) -> None:
        """Teszteli az alapértelmezett tárolási útvonal lekérdezését."""
        from neural_ai.data.storage.interfaces.storage_interface import StorageInterface

        mock_storage = Mock(spec=StorageInterface)
        del mock_storage.BASE_PATH
        self.mock_bridge.get_component.return_value = mock_storage

        result = self.data_service.get_storage_path()
        self.assertIsNotNone(result)
        self.assertEqual(str(result), "/data/tick")

    def test_get_configured_symbols_with_valid_config(self) -> None:
        """Teszteli a konfigurált szimbólumok lekérdezését érvényes konfiggal."""
        # Mock a konfigurációt
        mock_config = Mock()
        mock_config.get.return_value = ["EURUSD", "GBPUSD", "USDJPY"]

        # Mock a bridge és a core konfigot
        mock_core = Mock()
        mock_core.config = mock_config
        self.mock_bridge.core = mock_core

        symbols = self.data_service.get_configured_symbols()

        self.assertEqual(symbols, ["EURUSD", "GBPUSD", "USDJPY"])
        mock_config.get.assert_called_once_with("collectors", "jforex", "symbols")

    def test_get_configured_symbols_with_empty_config(self) -> None:
        """Teszteli a konfigurált szimbólumok lekérdezését üres konfiggal."""
        # Mock a konfigurációt, ami üres listát ad vissza
        mock_config = Mock()
        mock_config.get.return_value = []

        mock_core = Mock()
        mock_core.config = mock_config
        self.mock_bridge.core = mock_core

        symbols = self.data_service.get_configured_symbols()

        self.assertEqual(symbols, ["EURUSD"])

    def test_get_configured_symbols_with_none_config(self) -> None:
        """Teszteli a konfigurált szimbólumok lekérdezését None konfiggal."""
        # Mock a konfigurációt, ami None-t ad vissza
        mock_config = Mock()
        mock_config.get.return_value = None

        mock_core = Mock()
        mock_core.config = mock_config
        self.mock_bridge.core = mock_core

        symbols = self.data_service.get_configured_symbols()

        self.assertEqual(symbols, ["EURUSD"])

    def test_get_configured_symbols_with_invalid_config_type(self) -> None:
        """Teszteli a konfigurált szimbólumok lekérdezését érvénytelen típusú konfiggal."""
        # Mock a konfigurációt, ami nem listát ad vissza
        mock_config = Mock()
        mock_config.get.return_value = "EURUSD,GBPUSD"  # String instead of list

        mock_core = Mock()
        mock_core.config = mock_config
        self.mock_bridge.core = mock_core

        symbols = self.data_service.get_configured_symbols()

        self.assertEqual(symbols, ["EURUSD"])

    def test_get_configured_symbols_with_no_core_config(self) -> None:
        """Teszteli a konfigurált szimbólumok lekérdezését, ha nincs core konfig."""
        # Mock a bridge-t, ami None core-t ad vissza
        self.mock_bridge.core = None

        symbols = self.data_service.get_configured_symbols()

        self.assertEqual(symbols, ["EURUSD"])

    def test_get_configured_symbols_with_exception(self) -> None:
        """Teszteli a konfigurált szimbólumok lekérdezését kivétel esetén."""
        # Mock a konfigurációt, ami kivételt dob
        mock_config = Mock()
        mock_config.get.side_effect = Exception("Config error")

        mock_core = Mock()
        mock_core.config = mock_config
        self.mock_bridge.core = mock_core

        symbols = self.data_service.get_configured_symbols()

        self.assertEqual(symbols, ["EURUSD"])

    def test_generate_mock_data(self) -> None:
        """Teszteli a mock adatok generálását."""
        data = self.data_service._generate_mock_data("tick_data")
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1000)
        self.assertIn("timestamp", data[0])
        self.assertIn("symbol", data[0])
        self.assertIn("bid", data[0])

    def test_generate_mock_data_with_filters(self) -> None:
        """Teszteli a mock adatok generálását szűrőkkel."""
        filters = {"symbol": "EURUSD"}
        data = self.data_service._generate_mock_data("tick_data", filters)
        self.assertIsInstance(data, list)
        if data:  # Ha van szűrt adat
            self.assertEqual(data[0]["symbol"], "EURUSD")

    @patch("pathlib.Path.exists", return_value=True)
    @patch("pathlib.Path.stat")
    @patch("builtins.print")
    @patch("asyncio.sleep", return_value=None)
    async def test_download_history_with_existing_data_skip(
        self, mock_print: MagicMock, mock_stat: MagicMock, mock_exists: MagicMock
    ) -> None:
        """Teszteli a download_history metódust, amikor az adat már létezik és skip-eli."""
        # Mock stat return value
        mock_stat.return_value.st_size = 2000  # > 1000, tehát skip

        # Mock bridge és komponensek
        mock_downloader = AsyncMock()
        mock_storage = AsyncMock()
        self.mock_bridge.get_component.side_effect = lambda name: {
            "bi5_downloader": mock_downloader,
            "parquet_storage": mock_storage,
        }.get(name)

        # Mock config
        mock_config = Mock()
        mock_core = Mock()
        mock_core.config = mock_config
        self.mock_bridge.core = mock_core

        # Mock get_storage_path
        with patch.object(self.data_service, "get_storage_path", return_value=Mock()):
            start = datetime(2023, 1, 1, tzinfo=UTC)
            end = datetime(2023, 1, 1, tzinfo=UTC)

            result = await self.data_service.download_history("EURUSD", start, end)

            # Ellenőrizzük, hogy skip-elt
            mock_print.assert_called_with("⏭️ SKIPPING 2023-01-01 00:00:00+00:00 - Adat már létezik")
            # downloader.download_tick_data nem hívódott meg
            mock_downloader.download_tick_data.assert_not_called()
            # day_ticks hozzáadva
            self.assertIn("records", result)
            self.assertIn(
                "day_ticks", str(result)
            )  # Bonyolultabb lenne mock-olni, de alapvetően jó

    @patch("pathlib.Path.exists", return_value=False)
    @patch("builtins.print")
    @patch("asyncio.sleep", return_value=None)
    async def test_download_history_with_new_data_download(
        self, mock_print: MagicMock, mock_exists: MagicMock
    ) -> None:
        """Teszteli a download_history metódust, amikor új adat letöltésre kerül."""
        # Mock bridge és komponensek
        mock_downloader = AsyncMock()
        mock_storage = AsyncMock()
        mock_tick = Mock()
        mock_tick.timestamp = datetime.now(UTC)
        mock_tick.bid = 1.0850
        mock_tick.ask = 1.0852
        mock_tick.ask_volume = 100.0
        mock_tick.bid_volume = 50.0
        mock_tick.source = "test"
        mock_downloader.download_tick_data.return_value = [mock_tick]
        self.mock_bridge.get_component.side_effect = lambda name: {
            "bi5_downloader": mock_downloader,
            "parquet_storage": mock_storage,
        }.get(name)

        # Mock config
        mock_config = Mock()
        mock_core = Mock()
        mock_core.config = mock_config
        self.mock_bridge.core = mock_core

        # Mock get_storage_path
        with patch.object(self.data_service, "get_storage_path", return_value=Mock()):
            start = datetime(2023, 1, 1, tzinfo=UTC)
            end = datetime(2023, 1, 1, tzinfo=UTC)

            result = await self.data_service.download_history("EURUSD", start, end)

            # Ellenőrizzük, hogy letöltés történt
            mock_downloader.download_tick_data.assert_called()
            mock_storage.store_tick_data.assert_called()
            self.assertIn("records", result)
            self.assertGreater(result["records"], 0)

            # Ellenőrizzük a tárolt DataFrame oszlopait (csak forrásoszlopok, volume nélkül)
            call_args = mock_storage.store_tick_data.call_args
            df = call_args[1]["data"]  # keyword argument 'data'

            # Csak a 5 forrásoszlop legyen jelen: timestamp, bid, ask, ask_volume, bid_volume
            expected_columns = ["timestamp", "bid", "ask", "ask_volume", "bid_volume"]
            self.assertEqual(list(df.columns), expected_columns)

            # Ellenőrizzük, hogy a 'volume' oszlop NINCS jelen
            self.assertNotIn("volume", df.columns)

            # Ellenőrizzük, hogy a 'source' oszlop NINCS jelen (csak a tick_dicts-ben használt)
            self.assertNotIn("source", df.columns)

            # Ellenőrizzük az adatokat
            self.assertEqual(len(df), 1)
            self.assertEqual(df["bid"].iloc[0], 1.0850)
            self.assertEqual(df["ask"].iloc[0], 1.0852)
            self.assertEqual(df["ask_volume"].iloc[0], 100.0)
            self.assertEqual(df["bid_volume"].iloc[0], 50.0)


if __name__ == "__main__":
    unittest.main()
