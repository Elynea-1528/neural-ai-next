#!/usr/bin/env python3
"""Tick adatok feldolgozási útvonalának teljes validációja.

Ez a szkript validálja a Resampler és D1 Dimension Processor komponensek
együttműködését "tick" timeframe-mal.
"""

import asyncio
from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    import polars as pl


def validate_tick_pipeline() -> bool:
    """Tick pipeline validáció végrehajtása.

    Returns:
        bool: True ha minden validáció sikeres, False egyébként
    """
    print("🧪 Tick Pipeline Validáció Elindítva")
    print("=" * 50)

    try:
        # Mock komponensek létrehozása
        config = _create_mock_config()
        logger = _create_mock_logger()
        storage = _create_mock_storage()

        print("✅ Mock komponensek létrehozva")

        # Teszt adatok generálása
        tick_data = _generate_test_tick_data()
        print(f"✅ Teszt tick adatok generálva: {len(tick_data)} sor")

        # Resample validáció
        print("\n🔄 Resample Validáció...")
        resample_result = _validate_resample(tick_data, config, logger)
        if resample_result is None:
            return False

        # D1 Processor validáció
        print("\n🧬 D1 Processor Validáció...")
        final_result = _validate_d1_processor(resample_result, config, logger)
        if not final_result:
            return False

        print("\n🎉 Tick Pipeline Validáció Sikeres!")
        return True

    except Exception as e:
        print(f"❌ Végzetes hiba a validáció során: {e}")
        return False


def _create_mock_config() -> dict[str, Any]:
    """Mock konfigurációs objektum létrehozása."""
    return {
        "processors": {
            "d01_price": {
                "enabled": True,
                "timeframe": "tick"
            }
        },
        "resampler": {
            "engine": "polars"
        }
    }


def _create_mock_logger() -> Any:
    """Mock logger objektum létrehozása."""
    class MockLogger:
        def info(self, message: str, **kwargs: Any) -> None:
            print(f"📝 {message}")

        def error(self, message: str, **kwargs: Any) -> None:
            print(f"❌ {message}")

        def debug(self, message: str, **kwargs: Any) -> None:
            pass

    return MockLogger()


def _create_mock_storage() -> Any:
    """Mock storage objektum létrehozása."""
    class MockStorage:
        def __init__(self, data: Any):
            self.data = data

        def load_data(self, **kwargs: Any) -> Any:
            return self.data

    return MockStorage(None)


def _generate_test_tick_data() -> "pl.DataFrame":
    """Mock tick adatok generálása teszteléshez."""
    from datetime import datetime, timedelta

    import polars as pl

    # 100 tick adat generálása
    timestamps = [datetime(2023, 1, 1, 10, 0, 0) + timedelta(seconds=i) for i in range(100)]
    bids = [1.0520 + 0.0001 * (i % 10) for i in range(100)]
    asks = [bid + 0.0002 for bid in bids]
    bid_volumes = [10 + i % 5 for i in range(100)]
    ask_volumes = [12 + i % 3 for i in range(100)]

    return pl.DataFrame({
        "timestamp": timestamps,
        "bid": bids,
        "ask": asks,
        "bid_volume": bid_volumes,
        "ask_volume": ask_volumes
    })


def _validate_resample(tick_data: "pl.DataFrame", config: dict[str, Any], logger: Any) -> Optional["pl.DataFrame"]:
    """Resample komponens validációja.

    Args:
        tick_data: Bemeneti tick adatok
        config: Konfiguráció
        logger: Logger

    Returns:
        Resample eredmény vagy None ha hiba
    """
    try:
        from neural_ai.core.processing.resampler_service.factory import ResamplerServiceFactory

        resampler = ResamplerServiceFactory.get_resampler_service(
            config=config,
            logger=logger
        )

        # Tick timeframe - bypass aggregáció
        result = asyncio.run(resampler.resample(tick_data, "tick"))

        # Validációs kritériumok
        if len(result) != len(tick_data):
            print(f"❌ Sorok száma nem egyezik: {len(result)} vs {len(tick_data)}")
            return None

        required_columns = ["mid_close", "spread", "tick_volume"]
        missing_columns = [col for col in required_columns if col not in result.columns]
        if missing_columns:
            print(f"❌ Hiányzó oszlopok: {missing_columns}")
            return None

        # Tick volume ellenőrzés
        if not (result["tick_volume"] == 1).all():
            print("❌ Tick volume nem minden sorban 1")
            return None

        print(f"✅ Resample valid: {len(result)} sor, új oszlopok: {required_columns}")
        return result

    except Exception as e:
        print(f"❌ Resample hiba: {e}")
        return None


def _validate_d1_processor(resample_data: "pl.DataFrame", config: dict[str, Any], logger: Any) -> bool:
    """D1 Dimension Processor validációja.

    Args:
        resample_data: Resample eredmény
        config: Konfiguráció
        logger: Logger

    Returns:
        bool: True ha valid, False egyébként
    """
    try:
        from neural_ai.processors.factory import create_dimension_processor

        processor = create_dimension_processor("d01_price", config, logger)

        result = asyncio.run(processor.process(resample_data))

        # Validációs kritériumok
        if "log_return" not in result.columns:
            print("❌ Hiányzó log_return oszlop")
            return False

        # Tick timeframe esetén shadow oszlopok None
        shadow_columns = ["upper_shadow", "lower_shadow"]
        for col in shadow_columns:
            if col in result.columns:
                if not result[col].is_null().all():
                    print(f"❌ {col} oszlop nem None tick timeframe esetén")
                    return False
            else:
                print(f"⚠️  {col} oszlop hiányzik (elfogadott tick esetén)")

        # Eredeti tick oszlopok megőrzése
        original_columns = ["timestamp", "bid", "ask", "bid_volume", "ask_volume"]
        missing_originals = [col for col in original_columns if col not in result.columns]
        if missing_originals:
            print(f"❌ Hiányzó eredeti oszlopok: {missing_originals}")
            return False

        print(f"✅ D1 Processor valid: {len(result)} sor, új oszlop: log_return")
        return True

    except Exception as e:
        print(f"❌ D1 Processor hiba: {e}")
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
