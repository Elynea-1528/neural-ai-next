"""Strategy Service tesztek.

Ez a modul tartalmazza a StrategyService osztály tesztjeit,
beleértve az új get_candles metódust.
"""

from datetime import datetime
from unittest.mock import AsyncMock, Mock, patch

import pytest

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
