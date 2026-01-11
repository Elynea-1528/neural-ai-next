"""Strategy Service tesztek.

Ez a modul tartalmazza a StrategyService osztály tesztjeit,
beleértve az új get_candles metódust.
"""

import sys
from datetime import datetime
from unittest.mock import AsyncMock, Mock, patch

import pytest

# Mock vectorbt to avoid import issues in tests
sys.modules["vectorbt"] = Mock()

from neural_ai.ui.services.strategy_service import StrategyService


class TestStrategyService:
    """Strategy Service tesztek."""

    @pytest.fixture
    def mock_bridge(self) -> Mock:
        """Mock CoreBridgeInterface."""
        return Mock()

    @pytest.fixture
    def strategy_service(self, mock_bridge: Mock) -> StrategyService:
        """StrategyService példány létrehozása mock bridge-szel."""
        return StrategyService(bridge=mock_bridge)

    def test_init(self, strategy_service: StrategyService, mock_bridge: Mock) -> None:
        """StrategyService inicializáció tesztelése."""
        assert strategy_service._bridge == mock_bridge
        assert "moving_avg_cross" in strategy_service._strategies
        assert "rsi_strategy" in strategy_service._strategies

    def test_get_strategies(self, strategy_service: StrategyService) -> None:
        """Stratégiák lekérdezésének tesztelése."""
        strategies = strategy_service.get_strategies()
        assert len(strategies) == 2
        assert strategies[0]["id"] == "moving_avg_cross"
        assert strategies[1]["id"] == "rsi_strategy"

    def test_create_strategy(self, strategy_service: StrategyService) -> None:
        """Új stratégia létrehozásának tesztelése."""
        strategy_id = strategy_service.create_strategy(
            name="Test Strategy", config={"param1": "value1"}, code="print('hello')"
        )
        assert strategy_id == "strategy_3"
        assert strategy_id in strategy_service._strategies

    def test_update_strategy(self, strategy_service: StrategyService) -> None:
        """Stratégia módosításának tesztelése."""
        result = strategy_service.update_strategy(
            strategy_id="moving_avg_cross", config={"param1": "new_value"}
        )
        assert result is True
        assert strategy_service._strategies["moving_avg_cross"]["config"]["param1"] == "new_value"

    def test_update_strategy_not_found(self, strategy_service: StrategyService) -> None:
        """Ismeretlen stratégia módosításának tesztelése."""
        with pytest.raises(ValueError, match="Ismeretlen stratégia"):
            strategy_service.update_strategy(strategy_id="unknown")

    def test_delete_strategy(self, strategy_service: StrategyService) -> None:
        """Stratégia törlésének tesztelése."""
        result = strategy_service.delete_strategy(strategy_id="moving_avg_cross")
        assert result is True
        assert "moving_avg_cross" not in strategy_service._strategies

    def test_delete_strategy_not_found(self, strategy_service: StrategyService) -> None:
        """Ismeretlen stratégia törlésének tesztelése."""
        with pytest.raises(ValueError, match="Ismeretlen stratégia"):
            strategy_service.delete_strategy(strategy_id="unknown")

    def test_backtest_strategy(self, strategy_service: StrategyService) -> None:
        """Backtest indításának tesztelése."""
        result = strategy_service.backtest_strategy(
            strategy_id="moving_avg_cross",
            start_date="2024-01-01",
            end_date="2024-01-31",
            initial_capital=10000.0,
        )
        assert result["status"] == "started"
        assert "backtest_" in result["backtest_id"]

    def test_backtest_strategy_not_found(self, strategy_service: StrategyService) -> None:
        """Ismeretlen stratégia backtestelésének tesztelése."""
        with pytest.raises(ValueError, match="Ismeretlen stratégia"):
            strategy_service.backtest_strategy(
                strategy_id="unknown",
                start_date="2024-01-01",
                end_date="2024-01-31",
                initial_capital=10000.0,
            )

    def test_get_backtest_status(self, strategy_service: StrategyService) -> None:
        """Backtest állapot lekérdezésének tesztelése."""
        # Először indítsunk egy backtestet
        strategy_service.backtest_strategy(
            strategy_id="moving_avg_cross",
            start_date="2024-01-01",
            end_date="2024-01-31",
            initial_capital=10000.0,
        )
        backtest_id = "backtest_moving_avg_cross_0"

        status = strategy_service.get_backtest_status(backtest_id=backtest_id)
        assert status["backtest_id"] == backtest_id
        assert status["status"] == "completed"
        assert status["progress"] == 1.0

    def test_get_backtest_status_not_found(self, strategy_service: StrategyService) -> None:
        """Ismeretlen backtest állapot lekérdezésének tesztelése."""
        with pytest.raises(ValueError, match="Ismeretlen backtest"):
            strategy_service.get_backtest_status(backtest_id="unknown")

    def test_optimize_strategy(self, strategy_service: StrategyService) -> None:
        """Optimalizálás indításának tesztelése."""
        result = strategy_service.optimize_strategy(
            strategy_id="moving_avg_cross",
            parameters={"period": [10, 20, 30]},
            optimization_method="grid",
        )
        assert result["status"] == "started"
        assert "optimization_" in result["optimization_id"]

    def test_optimize_strategy_not_found(self, strategy_service: StrategyService) -> None:
        """Ismeretlen stratégia optimalizálásának tesztelése."""
        with pytest.raises(ValueError, match="Ismeretlen stratégia"):
            strategy_service.optimize_strategy(
                strategy_id="unknown",
                parameters={"period": [10, 20, 30]},
                optimization_method="grid",
            )

    @pytest.mark.asyncio
    async def test_get_candles(self, strategy_service: StrategyService) -> None:
        """OHLCV gyertyák lekérdezésének tesztelése."""
        # Mock ResamplerService és DataFrame
        mock_candles = Mock()
        mock_candles.empty = False

        mock_resampler = Mock()
        mock_resampler.resample = AsyncMock(return_value=mock_candles)

        with patch(
            "neural_ai.core.processing.resampler_service.factory.ResamplerServiceFactory.get_instance",
            return_value=mock_resampler,
        ):
            result = await strategy_service.get_candles(
                symbol="EURUSD", date="2024-03-20", timeframe="1m"
            )

            # Ellenőrizzük, hogy a resample metódust hívták-e a helyes paraméterekkel
            mock_resampler.resample.assert_called_once()
            call_args = mock_resampler.resample.call_args

            assert call_args.kwargs["symbol"] == "EURUSD"
            assert call_args.kwargs["timeframe"] == "1m"
            assert isinstance(call_args.kwargs["start"], datetime)
            assert isinstance(call_args.kwargs["end"], datetime)

            assert result == mock_candles

    @pytest.mark.asyncio
    async def test_get_candles_date_format(self, strategy_service: StrategyService) -> None:
        """Dátum formátum konverzió tesztelése."""
        mock_candles = Mock()
        mock_candles.empty = False

        mock_resampler = Mock()
        mock_resampler.resample = AsyncMock(return_value=mock_candles)

        with patch(
            "neural_ai.core.processing.resampler_service.factory.ResamplerServiceFactory.get_instance",
            return_value=mock_resampler,
        ):
            await strategy_service.get_candles(symbol="EURUSD", date="2024-03-20", timeframe="5m")

            call_args = mock_resampler.resample.call_args
            # Ellenőrizzük, hogy a dátum megfelelően lett konvertálva
            assert call_args.kwargs["start"] == datetime(2024, 3, 20, 0, 0, 0)
            assert call_args.kwargs["end"] == datetime(2024, 3, 20, 23, 59, 59)

    @pytest.mark.asyncio
    async def test_get_candles_different_timeframes(
        self, strategy_service: StrategyService
    ) -> None:
        """Különböző időkeretek tesztelése."""
        mock_candles = Mock()
        mock_candles.empty = False

        mock_resampler = Mock()
        mock_resampler.resample = AsyncMock(return_value=mock_candles)

        timeframes = ["1m", "5m", "15m", "1h", "4h", "1d"]

        with patch(
            "neural_ai.core.processing.resampler_service.factory.ResamplerServiceFactory.get_instance",
            return_value=mock_resampler,
        ):
            for timeframe in timeframes:
                await strategy_service.get_candles(
                    symbol="EURUSD", date="2024-03-20", timeframe=timeframe
                )
                assert mock_resampler.resample.call_args.kwargs["timeframe"] == timeframe

    @pytest.mark.asyncio
    async def test_run_sma_backtest_success_with_trades(
        self, strategy_service: StrategyService
    ) -> None:
        """SMA backtest sikerességének tesztelése trades adatokkal."""
        from unittest.mock import MagicMock

        import pandas as pd

        # Mock DataFrame OHLC adatokkal
        df = pd.DataFrame(
            {
                "open": [1.05, 1.06, 1.07],
                "high": [1.06, 1.07, 1.08],
                "low": [1.04, 1.05, 1.06],
                "close": [1.055, 1.065, 1.075],
                "timestamp": pd.to_datetime(
                    ["2024-01-01 10:00:00", "2024-01-01 10:01:00", "2024-01-01 10:02:00"]
                ),
            }
        )
        df.index = df["timestamp"]

        # Mock vectorbt Portfolio
        mock_pf = MagicMock()
        mock_pf.stats.return_value.to_dict.return_value = {
            "total_return": 0.05,
            "sharpe_ratio": 1.2,
        }
        mock_pf.value.return_value = [10000, 10500, 11000]

        # Mock trades.records_readable as MagicMock to avoid pandas issues
        mock_trades_df = MagicMock()
        mock_trades_df.__len__ = Mock(return_value=2)
        mock_trades_df.__getitem__ = Mock(
            side_effect=lambda key: {
                "PnL": MagicMock(
                    fillna=Mock(return_value=Mock(tolist=Mock(return_value=[50.0, 100.0])))
                ),
                "Duration": MagicMock(
                    astype=Mock(
                        return_value=Mock(
                            tolist=Mock(return_value=["0 days 00:05:00", "0 days 00:10:00"])
                        )
                    )
                ),
                "Entry Timestamp": MagicMock(
                    astype=Mock(
                        return_value=Mock(
                            tolist=Mock(return_value=["2024-01-01 10:00:00", "2024-01-01 10:01:00"])
                        )
                    )
                ),
                "Exit Timestamp": MagicMock(
                    astype=Mock(
                        return_value=Mock(
                            tolist=Mock(return_value=["2024-01-01 10:05:00", "2024-01-01 10:11:00"])
                        )
                    )
                ),
            }[key]
        )
        mock_trades_df.columns = ["PnL", "Duration", "Entry Timestamp", "Exit Timestamp"]
        mock_pf.trades.records_readable = mock_trades_df

        # Mock signals
        mock_entries = MagicMock()
        mock_entries.values = [True, False, True]
        mock_exits = MagicMock()
        mock_exits.values = [False, True, False]

        with (
            patch("vectorbt.Portfolio.from_signals", return_value=mock_pf),
            patch("vectorbt.MA.run") as mock_ma_run,
        ):
            # Mock MA.run visszatérési értékek
            mock_fast_ma = MagicMock()
            mock_slow_ma = MagicMock()
            mock_fast_ma.ma_crossed_above.return_value = mock_entries
            mock_fast_ma.ma_crossed_below.return_value = mock_exits
            mock_ma_run.side_effect = [mock_fast_ma, mock_slow_ma]

            result = await strategy_service.run_sma_backtest(
                symbol="EURUSD",
                date="2024-01-01",
                timeframe="1m",
                fast_period=5,
                slow_period=10,
                initial_capital=10000.0,
                df=df,
            )

            # Ellenőrizzük az eredmény szerkezetét
            assert "stats" in result
            assert "equity" in result
            assert "trades" in result
            assert "signals" in result
            assert "parameters" in result

            # Ellenőrizzük a trades adatokat
            trades_data = result["trades"]
            assert trades_data["count"] == 2
            assert trades_data["pnl"] == [50.0, 100.0]
            assert trades_data["duration"] == ["0 days 00:05:00", "0 days 00:10:00"]
            assert trades_data["entry_time"] == [
                "2024-01-01 10:00:00",
                "2024-01-01 10:01:00",
            ]
            assert trades_data["exit_time"] == [
                "2024-01-01 10:05:00",
                "2024-01-01 10:11:00",
            ]

            # Ellenőrizzük a signals-t
            assert result["signals"]["entries"] == [1, 0, 1]
            assert result["signals"]["exits"] == [0, 1, 0]

            # Ellenőrizzük a parameters-t
            params = result["parameters"]
            assert params["symbol"] == "EURUSD"
            assert params["fast_period"] == 5
            assert params["slow_period"] == 10

    @pytest.mark.asyncio
    async def test_run_sma_backtest_no_trades(self, strategy_service: StrategyService) -> None:
        """SMA backtest tesztelése trades nélkül."""
        from unittest.mock import MagicMock

        import pandas as pd

        # Mock DataFrame OHLC adatokkal
        df = pd.DataFrame(
            {
                "open": [1.05, 1.06, 1.07],
                "high": [1.06, 1.07, 1.08],
                "low": [1.04, 1.05, 1.06],
                "close": [1.055, 1.065, 1.075],
                "timestamp": pd.to_datetime(
                    ["2024-01-01 10:00:00", "2024-01-01 10:01:00", "2024-01-01 10:02:00"]
                ),
            }
        )
        df.index = df["timestamp"]

        # Mock vectorbt Portfolio
        mock_pf = MagicMock()
        mock_pf.stats.return_value.to_dict.return_value = {"total_return": 0.0, "sharpe_ratio": 0.0}
        mock_pf.value.return_value = [10000, 10000, 10000]

        # Üres trades DataFrame
        mock_trades_df = pd.DataFrame()
        mock_pf.trades.records_readable = mock_trades_df

        # Mock signals
        mock_entries = MagicMock()
        mock_entries.values = [False, False, False]
        mock_exits = MagicMock()
        mock_exits.values = [False, False, False]

        with (
            patch("vectorbt.Portfolio.from_signals", return_value=mock_pf),
            patch("vectorbt.MA.run") as mock_ma_run,
        ):
            # Mock MA.run visszatérési értékek
            mock_fast_ma = MagicMock()
            mock_slow_ma = MagicMock()
            mock_fast_ma.ma_crossed_above.return_value = mock_entries
            mock_fast_ma.ma_crossed_below.return_value = mock_exits
            mock_ma_run.side_effect = [mock_fast_ma, mock_slow_ma]

            result = await strategy_service.run_sma_backtest(
                symbol="EURUSD",
                date="2024-01-01",
                timeframe="1m",
                fast_period=5,
                slow_period=10,
                initial_capital=10000.0,
                df=df,
            )

            # Ellenőrizzük az eredményt
            trades_data = result["trades"]
            assert trades_data["count"] == 0
            assert trades_data["pnl"] == []
            assert trades_data["duration"] == []
            assert trades_data["entry_time"] == []
            assert trades_data["exit_time"] == []

    @pytest.mark.asyncio
    async def test_run_sma_backtest_missing_pnl_column(
        self, strategy_service: StrategyService
    ) -> None:
        """SMA backtest tesztelése hiányzó PnL oszloppal."""
        from unittest.mock import MagicMock

        import pandas as pd

        # Mock DataFrame OHLC adatokkal
        df = pd.DataFrame(
            {
                "open": [1.05, 1.06, 1.07],
                "high": [1.06, 1.07, 1.08],
                "low": [1.04, 1.05, 1.06],
                "close": [1.055, 1.065, 1.075],
                "timestamp": pd.to_datetime(
                    ["2024-01-01 10:00:00", "2024-01-01 10:01:00", "2024-01-01 10:02:00"]
                ),
            }
        )
        df.index = df["timestamp"]

        # Mock vectorbt Portfolio
        mock_pf = MagicMock()
        mock_pf.stats.return_value.to_dict.return_value = {
            "total_return": 0.02,
            "sharpe_ratio": 0.8,
        }
        mock_pf.value.return_value = [10000, 10200]

        # Trades DataFrame PnL nélkül
        mock_trades_df = pd.DataFrame(
            {
                "Duration": pd.to_timedelta(["00:05:00"]),
                "Entry Timestamp": pd.to_datetime(["2024-01-01 10:00:00"]),
                "Exit Timestamp": pd.to_datetime(["2024-01-01 10:05:00"]),
            }
        )
        mock_pf.trades.records_readable = mock_trades_df

        # Mock signals
        mock_entries = MagicMock()
        mock_entries.values = [True, False]
        mock_exits = MagicMock()
        mock_exits.values = [False, True]

        with (
            patch("vectorbt.Portfolio.from_signals", return_value=mock_pf),
            patch("vectorbt.MA.run") as mock_ma_run,
        ):
            # Mock MA.run visszatérési értékek
            mock_fast_ma = MagicMock()
            mock_slow_ma = MagicMock()
            mock_fast_ma.ma_crossed_above.return_value = mock_entries
            mock_fast_ma.ma_crossed_below.return_value = mock_exits
            mock_ma_run.side_effect = [mock_fast_ma, mock_slow_ma]

            result = await strategy_service.run_sma_backtest(
                symbol="EURUSD",
                date="2024-01-01",
                timeframe="1m",
                fast_period=5,
                slow_period=10,
                initial_capital=10000.0,
                df=df,
            )

            # Ellenőrizzük a trades adatokat
            trades_data = result["trades"]
            assert trades_data["count"] == 1
            assert trades_data["pnl"] == []  # Hiányzó PnL miatt üres lista
            assert trades_data["duration"] == ["0 days 00:05:00"]
            assert trades_data["entry_time"] == ["2024-01-01 10:00:00"]
            assert trades_data["exit_time"] == ["2024-01-01 10:05:00"]
