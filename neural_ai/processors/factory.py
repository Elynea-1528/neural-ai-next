"""Processing Factory - Feldolgozási komponensek factory függvényei."""

import importlib
from typing import TYPE_CHECKING, TypedDict, cast

from neural_ai.processors.interfaces.dimension_processor_interface import IDimensionProcessor
from neural_ai.processors.interfaces.time_alignment_interface import ITimeAlignmentService


class TimeframeConfig(TypedDict):
    """Időkeret specifikus konfiguráció."""

    z_score_window: int


class MarketHoursConfig(TypedDict):
    """Piaci órák szűrő konfiguráció."""

    enabled: bool
    weekdays: list[str]
    hours: list[str]
    timezone: str
    log_filtering: bool


class DimensionConfig(TypedDict):
    """Dimenzió processzor konfiguráció."""

    z_score_window: int
    timeframe_configs: dict[str, TimeframeConfig]
    calc_shadows: bool
    market_hours: MarketHoursConfig


class ProcessorConfig(TypedDict):
    """Processor konfigurációk gyűjteménye."""

    d01: DimensionConfig
    d02: DimensionConfig


class TimeAlignmentConfig(TypedDict):
    """Időszinkronizációs szolgáltatás konfiguráció."""

    pass

if TYPE_CHECKING:
    from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
    from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface

# Dimenzió konfigurációk - dinamikus factory loadinghez
DIMENSIONS_CONFIG = {1: "price", 2: "support"}

FACTORY_CLASSES = {1: "D01PriceFactory", 2: "D02SupportFactory"}


def create_time_alignment_service(
    config: "ConfigManagerInterface", logger: "LoggerInterface"
) -> ITimeAlignmentService:
    """TimeAlignmentService factory függvény - dinamikus példányosítással.

    Args:
        config: Konfigurációs menedzser interfész
        logger: A naplózási interfész.

    Returns:
        ITimeAlignmentService: Az időszinkronizációs szolgáltatás példánya
    """
    time_alignment_config = cast(TimeAlignmentConfig, config.get("time_alignment") or {})
    module = importlib.import_module("neural_ai.processors.implementations.time_alignment_service")
    cls = module.TimeAlignmentService
    return cls(logger)


def create_dimension_processor(
    dimension_id: int, config: "ConfigManagerInterface", logger: "LoggerInterface"
) -> IDimensionProcessor:
    """Dimenzió processzor factory függvény - dinamikus factory loadinggal.

    Args:
        dimension_id: A dimenzió azonosítója (1-15)
        config: Konfigurációs menedzser interfész
        logger: Logger interfész

    Returns:
        IDimensionProcessor: A megfelelő dimenzió processor példány

    Raises:
        ValueError: Ha ismeretlen dimenzió ID-t adnak meg
    """
    if dimension_id not in DIMENSIONS_CONFIG:
        raise ValueError(f"Ismeretlen dimenzió ID: {dimension_id}")

    processor_config = cast(ProcessorConfig, config.get("processors") or {})

    name = DIMENSIONS_CONFIG[dimension_id]
    module_name = f"neural_ai.processors.dimensions.d{dimension_id:02d}_{name}.factory"
    module = importlib.import_module(module_name)
    factory_class = getattr(module, FACTORY_CLASSES[dimension_id])
    return factory_class.create(config, logger)
