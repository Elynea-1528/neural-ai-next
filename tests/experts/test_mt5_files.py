"""MT5 Expert Advisor fájlok ellenőrzésére szolgáló tesztek.

Ez a modul ellenőrzi a Neural_AI_Next.mq5 és Neural_AI_Next_Multi.mq5 fájlok:
- Létezését
- Olvashatóságát
- Kritikus stringek jelenlétét (pl. FastAPI_Server)
"""

import os
import unittest
from pathlib import Path


class TestMT5Files(unittest.TestCase):
    """MT5 Expert Advisor fájlok ellenőrzésére szolgáló tesztosztály."""

    # Fájl elérési utak
    MT5_SRC_DIR = Path("neural_ai/experts/mt5/src")
    SINGLE_FILE = MT5_SRC_DIR / "Neural_AI_Next.mq5"
    MULTI_FILE = MT5_SRC_DIR / "Neural_AI_Next_Multi.mq5"

    # Kritikus stringek, amiknek jelen kell lenniük a fájlokban
    CRITICAL_STRINGS = {
        "FastAPI_Server",
        "http://localhost:8000",
        "WebRequest",
        "OnInit",
        "OnTick",
        "OnTimer",
    }

    # Kritikus stringek specifikusak a Multi fájlnak
    MULTI_CRITICAL_STRINGS = CRITICAL_STRINGS | {
        "Instruments",
        "Timeframes",
        "EURUSD,GBPUSD,USDJPY,XAUUSD",
        "M1,M5,M15,H1,H4,D1",
        "CollectAndSendTickData",
        "CollectAndSendOHLCVData",
    }

    def setUp(self) -> None:
        """Teszt előkészítése."""
        self.single_file_path = self.SINGLE_FILE
        self.multi_file_path = self.MULTI_FILE

    def test_single_file_exists(self) -> None:
        """Teszteli, hogy a Neural_AI_Next.mq5 fájl létezik-e."""
        self.assertTrue(
            self.single_file_path.exists(),
            f"A {self.single_file_path} fájlnak léteznie kell"
        )

    def test_single_file_is_file(self) -> None:
        """Teszteli, hogy a Neural_AI_Next.mq5 valóban fájl-e."""
        self.assertTrue(
            self.single_file_path.is_file(),
            f"A {self.single_file_path} nem fájl"
        )

    def test_single_file_is_readable(self) -> None:
        """Teszteli, hogy a Neural_AI_Next.mq5 olvasható-e."""
        self.assertTrue(
            os.access(self.single_file_path, os.R_OK),
            f"A {self.single_file_path} nem olvasható"
        )

    def test_single_file_not_empty(self) -> None:
        """Teszteli, hogy a Neural_AI_Next.mq5 nem üres."""
        file_size = self.single_file_path.stat().st_size
        self.assertGreater(
            file_size,
            0,
            f"A {self.single_file_path} üres fájl"
        )

    def test_single_file_contains_critical_strings(self) -> None:
        """Teszteli, hogy a Neural_AI_Next.mq5 tartalmazza-e a kritikus stringeket."""
        content = self.single_file_path.read_text(encoding="utf-8")

        missing_strings: set[str] = set()
        for critical_string in self.CRITICAL_STRINGS:
            if critical_string not in content:
                missing_strings.add(critical_string)

        self.assertFalse(
            missing_strings,
            f"A következő kritikus stringek hiányoznak: {missing_strings}"
        )

    def test_single_file_has_fastapi_server_input(self) -> None:
        """Teszteli, hogy a Neural_AI_Next.mq5 tartalmazza-e a FastAPI_Server input paramétert."""
        content = self.single_file_path.read_text(encoding="utf-8")
        self.assertIn(
            'input string FastAPI_Server = "http://localhost:8000"',
            content,
            "Hiányzik a FastAPI_Server input paraméter"
        )

    def test_single_file_has_update_interval(self) -> None:
        """Teszteli, hogy a Neural_AI_Next.mq5 tartalmazza-e az Update_Interval paramétert."""
        content = self.single_file_path.read_text(encoding="utf-8")
        self.assertIn(
            "input int Update_Interval = 60",
            content,
            "Hiányzik az Update_Interval input paraméter"
        )

    def test_single_file_has_http_logs_option(self) -> None:
        """Teszteli, hogy a Neural_AI_Next.mq5 tartalmazza-e a Enable_HTTP_Logs paramétert."""
        content = self.single_file_path.read_text(encoding="utf-8")
        self.assertIn(
            "input bool Enable_HTTP_Logs = true",
            content,
            "Hiányzik az Enable_HTTP_Logs input paraméter"
        )

    def test_single_file_has_test_connection_function(self) -> None:
        """Teszteli, hogy a Neural_AI_Next.mq5 tartalmazza-e a TestConnection függvényt."""
        content = self.single_file_path.read_text(encoding="utf-8")
        self.assertIn(
            "bool TestConnection()",
            content,
            "Hiányzik a TestConnection függvény"
        )

    def test_single_file_has_collect_tick_function(self) -> None:
        """Teszteli, hogy a Neural_AI_Next.mq5 tartalmazza-e a CollectAndSendTickData függvényt."""
        content = self.single_file_path.read_text(encoding="utf-8")
        self.assertIn(
            "void CollectAndSendTickData()",
            content,
            "Hiányzik a CollectAndSendTickData függvény"
        )

    def test_single_file_has_collect_ohlcv_function(self) -> None:
        """Teszteli, hogy a Neural_AI_Next.mq5 tartalmazza-e a CollectAndSendOHLCVData függvényt."""
        content = self.single_file_path.read_text(encoding="utf-8")
        self.assertIn(
            "void CollectAndSendOHLCVData()",
            content,
            "Hiányzik a CollectAndSendOHLCVData függvény"
        )

    def test_multi_file_exists(self) -> None:
        """Teszteli, hogy a Neural_AI_Next_Multi.mq5 fájl létezik-e."""
        self.assertTrue(
            self.multi_file_path.exists(),
            f"A {self.multi_file_path} fájlnak léteznie kell"
        )

    def test_multi_file_is_file(self) -> None:
        """Teszteli, hogy a Neural_AI_Next_Multi.mq5 valóban fájl-e."""
        self.assertTrue(
            self.multi_file_path.is_file(),
            f"A {self.multi_file_path} nem fájl"
        )

    def test_multi_file_is_readable(self) -> None:
        """Teszteli, hogy a Neural_AI_Next_Multi.mq5 olvasható-e."""
        self.assertTrue(
            os.access(self.multi_file_path, os.R_OK),
            f"A {self.multi_file_path} nem olvasható"
        )

    def test_multi_file_not_empty(self) -> None:
        """Teszteli, hogy a Neural_AI_Next_Multi.mq5 nem üres."""
        file_size = self.multi_file_path.stat().st_size
        self.assertGreater(
            file_size,
            0,
            f"A {self.multi_file_path} üres fájl"
        )

    def test_multi_file_larger_than_single(self) -> None:
        """Teszteli, hogy a Multi fájl nagyobb-e mint a Single fájl (több funkcionalitás)."""
        single_size = self.single_file_path.stat().st_size
        multi_size = self.multi_file_path.stat().st_size

        self.assertGreater(
            multi_size,
            single_size,
            "A Multi fájlnak nagyobbnak kell lennie mint a Single fájl"
        )

    def test_multi_file_contains_critical_strings(self) -> None:
        """Teszteli, hogy a Neural_AI_Next_Multi.mq5 tartalmazza-e a kritikus stringeket."""
        content = self.multi_file_path.read_text(encoding="utf-8")

        missing_strings: set[str] = set()
        for critical_string in self.MULTI_CRITICAL_STRINGS:
            if critical_string not in content:
                missing_strings.add(critical_string)

        self.assertFalse(
            missing_strings,
            f"A következő kritikus stringek hiányoznak: {missing_strings}"
        )

    def test_multi_file_has_fastapi_server_input(self) -> None:
        """Teszteli, hogy a Neural_AI_Next_Multi.mq5 tartalmazza-e a FastAPI_Server input paramétert."""  # noqa: E501
        content = self.multi_file_path.read_text(encoding="utf-8")
        self.assertIn(
            'input string FastAPI_Server = "http://localhost:8000"',
            content,
            "Hiányzik a FastAPI_Server input paraméter"
        )

    def test_multi_file_has_instruments_input(self) -> None:
        """Teszteli, hogy a Neural_AI_Next_Multi.mq5 tartalmazza-e az Instruments input paramétert."""  # noqa: E501
        content = self.multi_file_path.read_text(encoding="utf-8")
        self.assertIn(
            'input string Instruments = "EURUSD,GBPUSD,USDJPY,XAUUSD"',
            content,
            "Hiányzik az Instruments input paraméter"
        )

    def test_multi_file_has_timeframes_input(self) -> None:
        """Teszteli, hogy a Neural_AI_Next_Multi.mq5 tartalmazza-e a Timeframes input paramétert."""
        content = self.multi_file_path.read_text(encoding="utf-8")
        self.assertIn(
            'input string Timeframes = "M1,M5,M15,H1,H4,D1"',
            content,
            "Hiányzik a Timeframes input paraméter"
        )

    def test_multi_file_has_historical_collection_option(self) -> None:
        """Teszteli, hogy a Neural_AI_Next_Multi.mq5 tartalmazza-e a történelmi adatgyűjtés opciót."""  # noqa: E501
        content = self.multi_file_path.read_text(encoding="utf-8")
        self.assertIn(
            "input bool Enable_Historical_Collection = true",
            content,
            "Hiányzik az Enable_Historical_Collection input paraméter"
        )

    def test_multi_file_has_historical_batch_size(self) -> None:
        """Teszteli, hogy a Neural_AI_Next_Multi.mq5 tartalmazza-e a Historical_Batch_Size paramétert."""  # noqa: E501
        content = self.multi_file_path.read_text(encoding="utf-8")
        self.assertIn(
            "input int Historical_Batch_Size = 99000",
            content,
            "Hiányzik a Historical_Batch_Size input paraméter"
        )

    def test_multi_file_has_parse_instruments_function(self) -> None:
        """Teszteli, hogy a Neural_AI_Next_Multi.mq5 tartalmazza-e a ParseInstruments függvényt."""
        content = self.multi_file_path.read_text(encoding="utf-8")
        self.assertIn(
            "void ParseInstruments()",
            content,
            "Hiányzik a ParseInstruments függvény"
        )

    def test_multi_file_has_parse_timeframes_function(self) -> None:
        """Teszteli, hogy a Neural_AI_Next_Multi.mq5 tartalmazza-e a ParseTimeframes függvényt."""
        content = self.multi_file_path.read_text(encoding="utf-8")
        self.assertIn(
            "void ParseTimeframes()",
            content,
            "Hiányzik a ParseTimeframes függvény"
        )

    def test_multi_file_has_check_historical_requests_function(self) -> None:
        """Teszteli, hogy a Neural_AI_Next_Multi.mq5 tartalmazza-e a CheckForHistoricalRequests függvényt."""  # noqa: E501
        content = self.multi_file_path.read_text(encoding="utf-8")
        self.assertIn(
            "void CheckForHistoricalRequests()",
            content,
            "Hiányzik a CheckForHistoricalRequests függvény"
        )

    def test_multi_file_has_collect_historical_batch_function(self) -> None:
        """Teszteli, hogy a Neural_AI_Next_Multi.mq5 tartalmazza-e a CollectAndSendHistoricalBatch függvényt."""  # noqa: E501
        content = self.multi_file_path.read_text(encoding="utf-8")
        self.assertIn(
            "bool CollectAndSendHistoricalBatch()",
            content,
            "Hiányzik a CollectAndSendHistoricalBatch függvény"
        )

    def test_multi_file_has_string_to_timeframe_function(self) -> None:
        """Teszteli, hogy a Neural_AI_Next_Multi.mq5 tartalmazza-e a StringToTimeframe függvényt."""
        content = self.multi_file_path.read_text(encoding="utf-8")
        self.assertIn(
            "int StringToTimeframe(string tf)",
            content,
            "Hiányzik a StringToTimeframe függvény"
        )

    def test_multi_file_has_timeframe_to_string_function(self) -> None:
        """Teszteli, hogy a Neural_AI_Next_Multi.mq5 tartalmazza-e a TimeframeToString függvényt."""
        content = self.multi_file_path.read_text(encoding="utf-8")
        self.assertIn(
            "string TimeframeToString(int tf)",
            content,
            "Hiányzik a TimeframeToString függvény"
        )


if __name__ == "__main__":
    unittest.main()

