#!/usr/bin/env python3
"""Data Warehouse mappa struktúra létrehozása.

Ez a script létrehozza a Data Warehouse mappa struktúrát a pénzügyi adatok
szervezett tárolásához. A struktúra támogatja a több időkeretet, több
instrumentumot és a háromrétegű adatgyűjtési stratégiát.

Struktúra:
    data/
    ├── mt5/
    │   ├── raw/                    # Nyers adatok
    │   │   ├── ticks/             # Tick adatok
    │   │   └── ohlcv/             # OHLCV adatok
    │   ├── processed/              # Feldolgozott adatok
    │   │   ├── validated/         # Validált adatok
    │   │   ├── normalized/        # Normalizált adatok
    │   │   └── features/          # Kinyert feature-ök
    │   └── metadata/              # Metaadatok
    └── warehouse/                 # Data warehouse
        ├── historical/            # Történelmi adatok (25 év)
        ├── update/                # Frissítési adatok (3-12 hónap)
        └── realtime/              # Valós idejű adatok
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from neural_ai.core.logger.implementations.logger_factory import LoggerFactory


class DataWarehouseStructureCreator:
    """Data Warehouse mappa struktúra létrehozó."""

    def __init__(self, base_path: str = "data"):
        """Inicializálás.

        Args:
            base_path: Alap útvonal a data warehouse-hoz
        """
        self.base_path = Path(base_path)
        self.logger = LoggerFactory.get_logger(
            name="DataWarehouseStructureCreator",
            logger_type="colored",
            log_level="INFO",
        )

    def create_structure(self) -> bool:
        """Létrehozza a teljes Data Warehouse struktúrát.

        Returns:
            bool: True ha sikeres, False ha hiba történt
        """
        try:
            self.logger.info("Data Warehouse struktúra létrehozása elkezdve...")

            # 1. MT5 raw adatok struktúra
            self._create_mt5_raw_structure()

            # 2. Feldolgozott adatok struktúra
            self._create_processed_structure()

            # 3. Metaadatok struktúra
            self._create_metadata_structure()

            # 4. Data warehouse struktúra
            self._create_warehouse_structure()

            # 5. Metaadatok inicializálása
            self._initialize_metadata()

            self.logger.info("Data Warehouse struktúra létrehozása befejeződött!")
            return True

        except Exception as e:
            self.logger.error(f"Hiba a struktúra létrehozásakor: {e}")
            return False

    def _create_mt5_raw_structure(self) -> None:
        """Létrehozza a MT5 raw adatok struktúráját."""
        self.logger.info("MT5 raw adatok struktúra létrehozása...")

        # Alap útvonalak
        raw_path = self.base_path / "mt5" / "raw"
        ticks_path = raw_path / "ticks"
        ohlcv_path = raw_path / "ohlcv"

        # DLQ (Dead-Letter-Queue) könyvtár
        dlq_path = raw_path / "dlq"
        dlq_path.mkdir(parents=True, exist_ok=True)
        self.logger.info(f"DLQ könyvtár létrehozva: {dlq_path}")

        # Tick adatok struktúra
        instruments = ["EURUSD", "GBPUSD", "USDJPY", "XAUUSD"]
        for instrument in instruments:
            instrument_path = ticks_path / instrument
            instrument_path.mkdir(parents=True, exist_ok=True)

            # Év/hónap/nap struktúra
            current_year = datetime.now().year
            for year in range(current_year - 1, current_year + 1):
                year_path = instrument_path / str(year)
                year_path.mkdir(exist_ok=True)

                for month in range(1, 13):
                    month_path = year_path / f"{month:02d}"
                    month_path.mkdir(exist_ok=True)

        # OHLCV adatok struktúra
        timeframes = ["M1", "M5", "M15", "H1", "H4", "D1"]
        for instrument in instruments:
            for timeframe in timeframes:
                tf_path = ohlcv_path / instrument / timeframe
                tf_path.mkdir(parents=True, exist_ok=True)

                # Év/hónap struktúra
                for year in range(current_year - 1, current_year + 1):
                    year_path = tf_path / str(year)
                    year_path.mkdir(exist_ok=True)

                    for month in range(1, 13):
                        month_path = year_path / f"{month:02d}"
                        month_path.mkdir(exist_ok=True)

        self.logger.info(f"MT5 raw struktúra létrehozva: {raw_path}")

    def _create_processed_structure(self) -> None:
        """Létrehozza a feldolgozott adatok struktúráját."""
        self.logger.info("Feldolgozott adatok struktúra létrehozása...")

        processed_path = self.base_path / "mt5" / "processed"
        subdirs = ["validated", "normalized", "features"]

        for subdir in subdirs:
            path = processed_path / subdir
            path.mkdir(parents=True, exist_ok=True)

        self.logger.info(f"Feldolgozott adatok struktúra létrehozva: {processed_path}")

    def _create_metadata_structure(self) -> None:
        """Létrehozza a metaadatok struktúráját."""
        self.logger.info("Metaadatok struktúra létrehozása...")

        metadata_path = self.base_path / "mt5" / "metadata"
        metadata_path.mkdir(parents=True, exist_ok=True)

        self.logger.info(f"Metaadatok struktúra létrehozva: {metadata_path}")

    def _create_warehouse_structure(self) -> None:
        """Létrehozza a data warehouse struktúrát."""
        self.logger.info("Data warehouse struktúra létrehozása...")

        warehouse_path = self.base_path / "warehouse"
        subdirs = ["historical", "update", "realtime"]

        for subdir in subdirs:
            path = warehouse_path / subdir
            path.mkdir(parents=True, exist_ok=True)

        self.logger.info(f"Data warehouse struktúra létrehozva: {warehouse_path}")

    def _initialize_metadata(self) -> None:
        """Inicializálja a metaadat fájlokat."""
        self.logger.info("Metaadat fájlok inicializálása...")

        metadata_path = self.base_path / "mt5" / "metadata"

        # Instrumentumok listája
        instruments = {
            "instruments": [
                {
                    "symbol": "EURUSD",
                    "name": "Euro / US Dollar",
                    "type": "forex",
                    "digits": 5,
                    "point": 0.00001,
                },
                {
                    "symbol": "GBPUSD",
                    "name": "British Pound / US Dollar",
                    "type": "forex",
                    "digits": 5,
                    "point": 0.00001,
                },
                {
                    "symbol": "USDJPY",
                    "name": "US Dollar / Japanese Yen",
                    "type": "forex",
                    "digits": 3,
                    "point": 0.001,
                },
                {
                    "symbol": "XAUUSD",
                    "name": "Gold / US Dollar",
                    "type": "commodity",
                    "digits": 2,
                    "point": 0.01,
                },
            ]
        }

        instruments_file = metadata_path / "instruments.json"
        with open(instruments_file, "w") as f:
            json.dump(instruments, f, indent=2)

        # Időkeretek listája
        timeframes = {
            "timeframes": [
                {
                    "code": "M1",
                    "name": "1 Minute",
                    "period": 1,
                    "description": "One minute timeframe",
                },
                {
                    "code": "M5",
                    "name": "5 Minutes",
                    "period": 5,
                    "description": "Five minutes timeframe",
                },
                {
                    "code": "M15",
                    "name": "15 Minutes",
                    "period": 15,
                    "description": "Fifteen minutes timeframe",
                },
                {
                    "code": "H1",
                    "name": "1 Hour",
                    "period": 60,
                    "description": "One hour timeframe",
                },
                {
                    "code": "H4",
                    "name": "4 Hours",
                    "period": 240,
                    "description": "Four hours timeframe",
                },
                {
                    "code": "D1",
                    "name": "Daily",
                    "period": 1440,
                    "description": "Daily timeframe",
                },
            ]
        }

        timeframes_file = metadata_path / "timeframes.json"
        with open(timeframes_file, "w") as f:
            json.dump(timeframes, f, indent=2)

        # Adatminőség jelentés
        data_quality = {
            "last_updated": datetime.now().isoformat(),
            "instruments": {},
            "timeframes": {},
            "overall_quality": {
                "total_records": 0,
                "valid_records": 0,
                "invalid_records": 0,
                "quality_percentage": 100.0,
            },
        }

        data_quality_file = metadata_path / "data_quality.json"
        with open(data_quality_file, "w") as f:
            json.dump(data_quality, f, indent=2)

        self.logger.info("Metaadat fájlok inicializálva")

    def verify_structure(self) -> bool:
        """Ellenőrzi a Data Warehouse struktúrát.

        Returns:
            bool: True ha minden rendben van, False ha hiányzó elemek vannak
        """
        self.logger.info("Data Warehouse struktúra ellenőrzése...")

        required_paths = [
            self.base_path / "mt5" / "raw" / "ticks",
            self.base_path / "mt5" / "raw" / "ohlcv",
            self.base_path / "mt5" / "raw" / "dlq",
            self.base_path / "mt5" / "processed" / "validated",
            self.base_path / "mt5" / "processed" / "normalized",
            self.base_path / "mt5" / "processed" / "features",
            self.base_path / "mt5" / "metadata",
            self.base_path / "warehouse" / "historical",
            self.base_path / "warehouse" / "update",
            self.base_path / "warehouse" / "realtime",
        ]

        missing_paths = []
        for path in required_paths:
            if not path.exists():
                missing_paths.append(str(path))

        if missing_paths:
            self.logger.error(f"Hiányzó útvonalak: {missing_paths}")
            return False

        # Metaadat fájlok ellenőrzése
        metadata_path = self.base_path / "mt5" / "metadata"
        required_files = ["instruments.json", "timeframes.json", "data_quality.json"]

        missing_files = []
        for filename in required_files:
            file_path = metadata_path / filename
            if not file_path.exists():
                missing_files.append(filename)

        if missing_files:
            self.logger.error(f"Hiányzó metaadat fájlok: {missing_files}")
            return False

        self.logger.info("Data Warehouse struktúra ellenőrzése sikeres!")
        return True

    def print_structure(self) -> None:
        """Kiírja a Data Warehouse struktúrát."""
        self.logger.info("Data Warehouse struktúra:")

        def print_tree(path: Path, prefix: str = "", max_depth: int = 4, current_depth: int = 0):
            """Rekurzívan kiírja a mappa struktúrát."""
            if current_depth >= max_depth:
                return

            try:
                items = sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name))
                for i, item in enumerate(items):
                    is_last = i == len(items) - 1
                    current_prefix = "└── " if is_last else "├── "
                    print(f"{prefix}{current_prefix}{item.name}")

                    if item.is_dir():
                        extension = "    " if is_last else "│   "
                        print_tree(item, prefix + extension, max_depth, current_depth + 1)
            except PermissionError:
                pass

        print(f"\n{self.base_path}/")
        print_tree(self.base_path, "", max_depth=4)


def main():
    """Fő függvény."""
    print("=" * 60)
    print("Data Warehouse Structure Creator")
    print("=" * 60)

    creator = DataWarehouseStructureCreator()

    # Létrehozzuk a struktúrát
    if creator.create_structure():
        print("\n✅ Data Warehouse struktúra létrehozva!")
    else:
        print("\n❌ Hiba történt a struktúra létrehozásakor!")
        sys.exit(1)

    # Ellenőrizzük a struktúrát
    if creator.verify_structure():
        print("✅ Data Warehouse struktúra ellenőrzése sikeres!")
    else:
        print("❌ Hiba a struktúra ellenőrzésében!")
        sys.exit(1)

    # Kiírjuk a struktúrát
    print("\n")
    creator.print_structure()

    print("\n" + "=" * 60)
    print("Kész! A Data Warehouse struktúra használatra kész.")
    print("=" * 60)


if __name__ == "__main__":
    main()
