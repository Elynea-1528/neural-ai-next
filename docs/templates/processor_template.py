"""
Processzor template a Neural-AI-Next projekthez.

Ez a fájl egy adatfeldolgozási komponens sablont tartalmaz, amelyet
a különböző dimenzió-specifikus processzorok létrehozásához lehet használni.
"""

from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd

from neural_ai.core.logger import LoggerFactory
from neural_ai.processors.interfaces import ProcessorInterface


class DimensionProcessor(ProcessorInterface):
    """
    Dimenzió-specifikus adatfeldolgozó.

    Ez a komponens egy piaci dimenziót elemez és feature-öket számít ki.

    Attributes:
        config: Processzor konfiguráció
        name: A dimenzió neve
        window: Feldolgozási ablakméret
        logger: Logger példány
    """

    def __init__(self, config: Dict[str, Any], logger=None):
        """
        Inicializálja a processzort.

        Args:
            config: Processzor konfigurációja
            logger: Logger példány vagy None (ekkor alapértelmezett logger jön létre)
        """
        self.config = config
        self.logger = logger or LoggerFactory.get_logger(__name__)

        # Konfigurációs paraméterek beolvasása
        self.name = config.get("name", "dimension_processor")
        self.window = config.get("window", 20)
        self.normalize = config.get("normalize", True)

        # Feature definíciók
        self._feature_definitions = self._init_feature_definitions()

        self.logger.info(f"{self.__class__.__name__} initialized with window={self.window}")

    def _init_feature_definitions(self) -> Dict[str, Dict[str, Any]]:
        """
        Feature definíciók inicializálása.

        Returns:
            A processzor által generált feature-ök definíciói
        """
        return {
            "feature1": {
                "function": self._calculate_feature1,
                "params": {"window": self.window},
                "description": "Az első feature leírása",
            },
            "feature2": {
                "function": self._calculate_feature2,
                "params": {"window": self.window // 2, "alpha": 0.5},
                "description": "A második feature leírása",
            },
        }

    def process(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Adatok feldolgozása és feature-ök kiszámítása.

        Args:
            data: OHLCV adatok pandas DataFrame-ben

        Returns:
            Az eredeti adatok kiegészítve a kiszámított feature-ökkel

        Raises:
            ProcessorError: Feldolgozási hiba esetén
        """
        try:
            self.logger.debug(f"Processing data with shape {data.shape}")

            # Adatok validálása
            self._validate_input(data)

            # Feature-ök kiszámítása
            result = data.copy()

            for feature_name, feature_def in self._feature_definitions.items():
                self.logger.debug(f"Calculating feature: {feature_name}")
                result[feature_name] = feature_def["function"](data, **feature_def["params"])

            # Normalizálás, ha szükséges
            if self.normalize:
                result = self._normalize_features(result)

            self.logger.info(
                f"Successfully processed data, added {len(self._feature_definitions)} features"
            )
            return result

        except Exception as e:
            self.logger.error(f"Error processing data: {str(e)}")
            raise ProcessorError(f"Processing failed: {str(e)}") from e

    def _validate_input(self, data: pd.DataFrame) -> None:
        """
        Bemeneti adatok validálása.

        Args:
            data: Ellenőrizendő adatok

        Raises:
            ValueError: Ha az adatok nem megfelelőek
        """
        required_columns = ["open", "high", "low", "close", "volume"]
        missing_columns = [col for col in required_columns if col not in data.columns]

        if missing_columns:
            raise ValueError(f"Input data missing required columns: {missing_columns}")

        if len(data) < self.window:
            raise ValueError(
                f"Input data too short (got {len(data)} rows, need at least {self.window})"
            )

    def _normalize_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Feature-ök normalizálása.

        Args:
            data: Normalizálandó adatok

        Returns:
            Normalizált adatok
        """
        # Csak a számolt feature-öket normalizáljuk, az eredeti OHLCV oszlopokat nem
        feature_columns = list(self._feature_definitions.keys())

        for feature in feature_columns:
            if feature in data.columns:
                # Min-max normalizálás 0-1 tartományba
                min_val = data[feature].min()
                max_val = data[feature].max()
                if max_val > min_val:  # Elkerüljük a nullával való osztást
                    data[feature] = (data[feature] - min_val) / (max_val - min_val)

        return data

    def _calculate_feature1(self, data: pd.DataFrame, window: int) -> pd.Series:
        """
        Első feature számítása.

        Args:
            data: Forrás adatok
            window: Ablakméret

        Returns:
            Az első feature értékei
        """
        # Például: mozgóátlag a záróárakra
        return data["close"].rolling(window=window).mean()

    def _calculate_feature2(self, data: pd.DataFrame, window: int, alpha: float) -> pd.Series:
        """
        Második feature számítása.

        Args:
            data: Forrás adatok
            window: Ablakméret
            alpha: További paraméter

        Returns:
            A második feature értékei
        """
        # Például: exponenciális mozgóátlag
        return data["close"].ewm(span=window, alpha=alpha).mean()

    def get_feature_definitions(self) -> Dict[str, Dict[str, Any]]:
        """
        Feature definíciók lekérése.

        Returns:
            A processzor által generált feature-ök definíciói
        """
        return self._feature_definitions


class ProcessorError(Exception):
    """A processzor specifikus kivétele."""

    pass
