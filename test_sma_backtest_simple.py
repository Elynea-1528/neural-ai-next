"""Egyszerű teszt szkript a run_sma_backtest metódus ellenőrzésére."""

import asyncio

import pandas as pd

from neural_ai.ui.services.strategy_service import StrategyService


async def test_run_sma_backtest():
    """Teszteli a run_sma_backtest metódust mock adatokkal."""
    # Mock adatok létrehozása
    df = pd.DataFrame(
        {
            "timestamp": pd.date_range("2024-01-01", periods=100, freq="1min"),
            "open": [1.0 + i * 0.001 for i in range(100)],
            "high": [1.01 + i * 0.001 for i in range(100)],
            "low": [0.99 + i * 0.001 for i in range(100)],
            "close": [1.005 + i * 0.001 for i in range(100)],
            "volume": [1000 for _ in range(100)],
        }
    )
    df.set_index("timestamp", inplace=True)

    # StrategyService példányosítása
    service = StrategyService()

    try:
        # run_sma_backtest meghívása
        result = await service.run_sma_backtest(
            symbol="EURUSD",
            date="2024-01-01",
            timeframe="1m",
            fast_period=5,
            slow_period=10,
            initial_capital=10000.0,
            df=df,
        )

        # Ellenőrzések
        if "error" in result:
            print(f"Teszt sikertelen: {result['error']}")
            return False

        trades = result.get("trades", {})
        if "pnl" not in trades:
            print("Hiba: 'pnl' kulcs hiányzik a trades dict-ből.")
            return False

        if "duration" not in trades:
            print("Hiba: 'duration' kulcs hiányzik a trades dict-ből.")
            return False

        pnl = trades["pnl"]
        duration = trades["duration"]

        if not isinstance(pnl, list):
            print("Hiba: 'pnl' nem lista.")
            return False

        if not isinstance(duration, list):
            print("Hiba: 'duration' nem lista.")
            return False

        if not all(isinstance(d, str) for d in duration):
            print("Hiba: 'duration' elemei nem stringek.")
            return False

        print("Sikerült: 'pnl' és 'duration' jelen van, mindkettő lista, 'duration' string lista.")
        return True

    except Exception as e:
        print(f"Teszt sikertelen kivétel miatt: {str(e)}")
        return False


if __name__ == "__main__":
    success = asyncio.run(test_run_sma_backtest())
    if success:
        print("Teszt sikeres!")
    else:
        print("Teszt sikertelen!")
