"""MT5 adatvalidátor modul."""

from typing import Any, Dict

import pandas as pd


class DataValidator:
    """MT5 adatvalidáló osztály."""

    def validate(self, data: pd.DataFrame) -> pd.DataFrame:
        """Adatok validálása és tisztítása."""
        # Alap validációk
        if data.empty:
            return data

        # Duplikátumok eltávolítása
        data = data[~data.index.duplicated(keep="first")]

        # Hiányzó értékek kezelése
        data = data.dropna()

        return data

    def check_quality(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Adatminőség ellenőrzése és metrikák számítása."""
        metrics = {
            "gaps": 0,
            "missing_values": int(data.isnull().sum().sum()),
            "duplicates": int(data.index.duplicated().sum()),
            "consistency": 100,  # Alapértelmezett, implementálandó
        }

        # Időbeli hézagok számítása
        if not data.empty and hasattr(data.index, "to_series"):
            if hasattr(data.index, "to_series"):
                time_diff = data.index.to_series().diff().dropna()
                if not time_diff.empty:
                    metrics["gaps"] = int((time_diff > time_diff.mode()[0]).sum())

        return metrics
