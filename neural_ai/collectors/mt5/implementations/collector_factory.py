"""MT5 Collector Factory.

Ez a modul tartalmazza az MT5 Collector komponens factory osztályát,
amely felelős a collector példányok létrehozásáért.

Author: Neural AI Team
Date: 2025-12-16
Version: 1.0.0
"""

from typing import Any

from neural_ai.collectors.mt5.error_handler import ConfigurationError
from neural_ai.collectors.mt5.interfaces.collector_interface import CollectorInterface


class CollectorFactory:
    """MT5 Collector Factory osztály.

    Felelős a különböző típusú collectorok létrehozásáért
    és konfigurálásáért.
    """

    _collectors = {}

    @classmethod
    def register_collector(cls, collector_type: str, collector_class):
        """Collector regisztrálása.

        Args:
            collector_type: Collector típusa
            collector_class: Collector osztály
        """
        cls._collectors[collector_type] = collector_class

    @classmethod
    def get_collector(cls, collector_type: str, config: dict[str, Any]) -> CollectorInterface:
        """Collector példány létrehozása.

        Args:
            collector_type: Collector típusa
            config: Konfiguráció

        Returns:
            CollectorInterface: Collector példány

        Raises:
            ConfigurationError: Ismeretlen collector típus esetén
        """
        if collector_type not in cls._collectors:
            raise ConfigurationError(f"Ismeretlen collector típus: {collector_type}")

        collector_class = cls._collectors[collector_type]
        return collector_class(config)

    @classmethod
    def get_available_collectors(cls) -> list:
        """Elérhető collector típusok lekérése.

        Returns:
            Collector típusok listája
        """
        return list(cls._collectors.keys())


# Alapértelmezett collector regisztrálása
from neural_ai.collectors.mt5.implementations.mt5_collector import MT5Collector

CollectorFactory.register_collector("mt5", MT5Collector)
