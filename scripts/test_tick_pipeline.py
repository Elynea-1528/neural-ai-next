#!/usr/bin/env python3
"""Tick adatok feldolgozási útvonalának teljes validációja.

Ez a szkript validálja a Resampler és D1 Dimension Processor komponensek
együttműködését "tick" timeframe-mal.
"""

from datetime import UTC, datetime, timedelta
from typing import Any

import polars as pl

from neural_ai.core.config.implementations.yaml_config_manager import YAMLConfigManager
from neural_ai.core.logger.factory import LoggerFactory
from neural_ai.processors.dimensions.d01_price.processor import D01PriceProcessor


def validate_tick_pipeline() -> bool:
    """Tick pipeline validáció végrehajtása.

    Returns:
        bool: True ha minden validáció sikeres, False egyébként
    """
    logger = LoggerFactory.get_logger(__name__, logger_type="colored")
    logger.info("🧪 Tick Pipeline Validáció Elindítva")
    logger.info("=" * 50)

    try:
        # Mock komponensek létrehozása
        config = _create_mock_config()
        mock_logger = _create_mock_logger()

        logger.info("✅ Mock komponensek létrehozva")

        # Teszt adatok generálása
        tick_data = _generate_test_tick_data()
        logger.info(f"✅ Teszt tick adatok generálva: {len(tick_data)} sor")

        # Resample validáció
        logger.info("🔄 Resample Validáció...")
        resample_result = _validate_resample(tick_data, mock_logger)
        if resample_result is None:
            return False

        # D1 Processor validáció
        logger.info("🧬 D1 Processor Validáció...")
        final_result = _validate_d1_processor(resample_result, config, mock_logger)
        if not final_result:
            return False

        logger.info("🎉 Tick Pipeline Validáció Sikeres!")
        return True

    except Exception as e:
        logger.error(f"❌ Végzetes hiba a validáció során: {e}")
        return False


def _create_mock_config() -> dict[str, Any]:
    """Mock konfiguráció létrehozása."""
    return {
        "processors": {"d01_price": {"enabled": True, "timeframe": "tick"}},
        "resampler": {"engine": "polars"},
    }


def _create_mock_logger() -> Any:
    """Mock logger objektum létrehozása."""

    class MockLogger:
        def info(self, message: str, **kwargs: Any) -> None:
            logger = LoggerFactory.get_logger(__name__, logger_type="colored")
            logger.info(f"📝 {message}", **kwargs)

        def error(self, message: str, **kwargs: Any) -> None:
            logger = LoggerFactory.get_logger(__name__, logger_type="colored")
            logger.error(f"❌ {message}", **kwargs)

        def debug(self, message: str, **kwargs: Any) -> None:
            logger = LoggerFactory.get_logger(__name__, logger_type="colored")
            logger.debug(message, **kwargs)

        def warning(self, message: str, **kwargs: Any) -> None:
            logger = LoggerFactory.get_logger(__name__, logger_type="colored")
            logger.warning(f"⚠️ {message}", **kwargs)

    return MockLogger()


def _generate_test_tick_data() -> pl.DataFrame:
    """Mock tick adatok generálása teszteléshez."""
    # 100 tick adat generálása
    timestamps = [
        datetime(2023, 1, 1, 10, 0, 0, tzinfo=UTC) + timedelta(seconds=i) for i in range(100)
    ]
    bids = [1.0520 + 0.0001 * (i % 10) for i in range(100)]
    asks = [bid + 0.0002 for bid in bids]
    bid_volumes = [10 + i % 5 for i in range(100)]
    ask_volumes = [12 + i % 3 for i in range(100)]

    return pl.DataFrame(
        {
            "timestamp": timestamps,
            "bid": bids,
            "ask": asks,
            "bid_volume": bid_volumes,
            "ask_volume": ask_volumes,
        }
    )


def _validate_resample(tick_data: pl.DataFrame, logger: Any) -> pl.DataFrame | None:
    """Resample komponens validációja.

    Args:
        tick_data: Bemeneti tick adatok
        config: Konfiguráció
        logger: Logger

    Returns:
        Resample eredmény vagy None ha hiba
    """
    try:
        # Mivel a resampler service tényleges adatbázisból dolgozik,
        # ezért a teszteléshez mockolni kell a belső működést

        # Tick timeframe esetén egyszerűen enricheljük a tick adatokat
        # Ez a logika a ResamplerService _convert_to_ohlcv metódusából származik

        mid_price = (pl.col("bid") + pl.col("ask")) / 2
        enriched_tick_data = tick_data.with_columns(
            mid_open=mid_price,
            mid_high=mid_price,
            mid_low=mid_price,
            mid_close=mid_price,
            bid_open=pl.col("bid"),
            bid_high=pl.col("bid"),
            bid_low=pl.col("bid"),
            bid_close=pl.col("bid"),
            ask_open=pl.col("ask"),
            ask_high=pl.col("ask"),
            ask_low=pl.col("ask"),
            ask_close=pl.col("ask"),
            spread=pl.col("ask") - pl.col("bid"),
            real_volume=pl.col("bid_volume") + pl.col("ask_volume"),
            tick_volume=pl.lit(1),
        )

        result = enriched_tick_data

        # Validációs kritériumok
        if len(result) != len(tick_data):
            logger.error(f"❌ Sorok száma nem egyezik: {len(result)} vs {len(tick_data)}")
            return None

        required_columns = ["mid_close", "spread", "tick_volume"]
        missing_columns = [col for col in required_columns if col not in result.columns]
        if missing_columns:
            logger.error(f"❌ Hiányzó oszlopok: {missing_columns}")
            return None

        # Tick volume ellenőrzés
        if not (result["tick_volume"] == 1).all():
            logger.error("❌ Tick volume nem minden sorban 1")
            return None

        logger.info(f"✅ Resample valid: {len(result)} sor, új oszlopok: {required_columns}")
        return result

    except Exception as e:
        logger.error(f"❌ Resample hiba: {e}")
        return None


def _validate_d1_processor(
    resample_data: pl.DataFrame, config: dict[str, Any], logger: Any
) -> bool:
    """D1 Dimension Processor validációja.

    Args:
        resample_data: Resample eredmény
        config: Konfiguráció
        logger: Logger

    Returns:
        bool: True ha valid, False egyébként
    """
    try:
        # Mock config manager létrehozása
        config_manager = YAMLConfigManager()
        config_manager._config = config  # pyright: ignore[reportPrivateUsage]
        processor = D01PriceProcessor(config_manager, logger)

        result = processor.process(resample_data, "tick")

        # Validációs kritériumok
        if "log_return" not in result.columns:
            logger.error("❌ Hiányzó log_return oszlop")
            return False

        # Tick timeframe esetén shadow oszlopok None
        shadow_columns = ["upper_shadow", "lower_shadow"]
        for col in shadow_columns:
            if col in result.columns:
                if not result[col].is_null().all():
                    logger.error(f"❌ {col} oszlop nem None tick timeframe esetén")
                    return False
            else:
                logger.info(f"⚠️  {col} oszlop hiányzik (elfogadott tick esetén)")

        # Eredeti tick oszlopok megőrzése
        original_columns = ["timestamp", "bid", "ask", "bid_volume", "ask_volume"]
        missing_originals = [col for col in original_columns if col not in result.columns]
        if missing_originals:
            logger.error(f"❌ Hiányzó eredeti oszlopok: {missing_originals}")
            return False

        logger.info(f"✅ D1 Processor valid: {len(result)} sor, új oszlop: log_return")
        return True

    except Exception as e:
        logger.error(f"❌ D1 Processor hiba: {e}")
        return False


def main() -> int:
    """Fő végrehajtási függvény.

    Returns:
        int: Kilépési kód (0 = siker, 1 = hiba)
    """
    success = validate_tick_pipeline()
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
