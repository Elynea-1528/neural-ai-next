"""Unit tesztek a StrategyServiceInterface interfészhez."""

from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest

from neural_ai.ui.interfaces.strategy_service_interface import StrategyServiceInterface


class TestStrategyServiceInterface:
    """Tesztek a StrategyServiceInterface interfészhez."""

    def test_interface_is_runtime_checkable(self) -> None:
        """Teszteli, hogy az interfész runtime checkable."""
        mock_service = MagicMock(spec=StrategyServiceInterface)
        assert isinstance(mock_service, StrategyServiceInterface)

    def test_get_strategies_signature(self) -> None:
        """Teszteli a get_strategies metódus szignatúráját."""
        mock_service = MagicMock(spec=StrategyServiceInterface)
        strategies: list[dict[str, Any]] = [
            {"id": "strat1", "name": "SMA Cross"},
            {"id": "strat2", "name": "RSI Strategy"},
        ]
        mock_service.get_strategies.return_value = strategies
        result = mock_service.get_strategies()
        assert result == strategies
        assert len(result) == 2
        mock_service.get_strategies.assert_called_once()

    def test_create_strategy_signature(self) -> None:
        """Teszteli a create_strategy metódus szignatúráját."""
        mock_service = MagicMock(spec=StrategyServiceInterface)
        config: dict[str, Any] = {"param1": 10, "param2": 20}
        code = "def strategy(): pass"
        mock_service.create_strategy.return_value = "strat123"
        result = mock_service.create_strategy("My Strategy", config, code)
        assert result == "strat123"
        mock_service.create_strategy.assert_called_once_with("My Strategy", config, code)

    def test_update_strategy_with_both_params(self) -> None:
        """Teszteli az update_strategy metódust mindkét paraméterrel."""
        mock_service = MagicMock(spec=StrategyServiceInterface)
        config: dict[str, Any] = {"param1": 15}
        code = "def updated_strategy(): pass"
        mock_service.update_strategy.return_value = True
        result = mock_service.update_strategy("strat123", config, code)
        assert result is True
        mock_service.update_strategy.assert_called_once_with("strat123", config, code)

    def test_update_strategy_with_config_only(self) -> None:
        """Teszteli az update_strategy metódust csak config paraméterrel."""
        mock_service = MagicMock(spec=StrategyServiceInterface)
        config: dict[str, Any] = {"param1": 15}
        mock_service.update_strategy.return_value = True
        result = mock_service.update_strategy("strat123", config=config)
        assert result is True
        mock_service.update_strategy.assert_called_once_with("strat123", config=config)

    def test_delete_strategy_signature(self) -> None:
        """Teszteli a delete_strategy metódus szignatúráját."""
        mock_service = MagicMock(spec=StrategyServiceInterface)
        mock_service.delete_strategy.return_value = True
        result = mock_service.delete_strategy("strat123")
        assert result is True
        mock_service.delete_strategy.assert_called_once_with("strat123")

    def test_backtest_strategy_signature(self) -> None:
        """Teszteli a backtest_strategy metódus szignatúráját."""
        mock_service = MagicMock(spec=StrategyServiceInterface)
        backtest_result: dict[str, Any] = {
            "backtest_id": "bt123",
            "total_return": 0.15,
            "sharpe_ratio": 1.5,
        }
        mock_service.backtest_strategy.return_value = backtest_result
        result = mock_service.backtest_strategy("strat123", "2024-01-01", "2024-12-31", 10000.0)
        assert result == backtest_result
        mock_service.backtest_strategy.assert_called_once_with(
            "strat123", "2024-01-01", "2024-12-31", 10000.0
        )

    def test_get_backtest_status_signature(self) -> None:
        """Teszteli a get_backtest_status metódus szignatúráját."""
        mock_service = MagicMock(spec=StrategyServiceInterface)
        status: dict[str, Any] = {"backtest_id": "bt123", "status": "completed", "progress": 1.0}
        mock_service.get_backtest_status.return_value = status
        result = mock_service.get_backtest_status("bt123")
        assert result == status
        mock_service.get_backtest_status.assert_called_once_with("bt123")

    def test_optimize_strategy_with_default_method(self) -> None:
        """Teszteli az optimize_strategy metódust alapértelmezett módszerrel."""
        mock_service = MagicMock(spec=StrategyServiceInterface)
        parameters: dict[str, list[Any]] = {"fast_period": [5, 10, 15], "slow_period": [20, 30, 40]}
        optimization_result: dict[str, Any] = {
            "best_params": {"fast_period": 10, "slow_period": 30}
        }
        mock_service.optimize_strategy.return_value = optimization_result
        result = mock_service.optimize_strategy("strat123", parameters)
        assert result == optimization_result
        mock_service.optimize_strategy.assert_called_once_with("strat123", parameters)

    def test_optimize_strategy_with_custom_method(self) -> None:
        """Teszteli az optimize_strategy metódust egyedi módszerrel."""
        mock_service = MagicMock(spec=StrategyServiceInterface)
        parameters: dict[str, list[Any]] = {"param1": [1, 2, 3]}
        optimization_result: dict[str, Any] = {"best_params": {"param1": 2}}
        mock_service.optimize_strategy.return_value = optimization_result
        result = mock_service.optimize_strategy("strat123", parameters, "bayesian")
        assert result == optimization_result
        mock_service.optimize_strategy.assert_called_once_with("strat123", parameters, "bayesian")

    @pytest.mark.asyncio
    async def test_get_candles_signature(self) -> None:
        """Teszteli a get_candles async metódus szignatúráját."""
        mock_service = MagicMock(spec=StrategyServiceInterface)
        mock_df = MagicMock()
        mock_service.get_candles = AsyncMock(return_value=mock_df)
        result = await mock_service.get_candles("EURUSD", "2024-03-20", "1h")
        assert result is mock_df
        mock_service.get_candles.assert_called_once_with("EURUSD", "2024-03-20", "1h")

    @pytest.mark.asyncio
    async def test_run_sma_backtest_with_all_params(self) -> None:
        """Teszteli a run_sma_backtest async metódust minden paraméterrel."""
        mock_service = MagicMock(spec=StrategyServiceInterface)
        mock_df = MagicMock()
        backtest_result: dict[str, Any] = {"total_return": 0.12, "trades": 50}
        mock_service.run_sma_backtest = AsyncMock(return_value=backtest_result)
        result = await mock_service.run_sma_backtest(
            "EURUSD", "2024-03-20", "1h", 10, 20, 10000.0, mock_df
        )
        assert result == backtest_result
        mock_service.run_sma_backtest.assert_called_once_with(
            "EURUSD", "2024-03-20", "1h", 10, 20, 10000.0, mock_df
        )

    @pytest.mark.asyncio
    async def test_run_sma_backtest_minimal_params(self) -> None:
        """Teszteli a run_sma_backtest async metódust minimális paraméterekkel."""
        mock_service = MagicMock(spec=StrategyServiceInterface)
        backtest_result: dict[str, Any] = {"total_return": 0.08}
        mock_service.run_sma_backtest = AsyncMock(return_value=backtest_result)
        result = await mock_service.run_sma_backtest("GBPUSD", "2024-03-20", "4h", 5, 15)
        assert result == backtest_result
        mock_service.run_sma_backtest.assert_called_once_with(
            "GBPUSD", "2024-03-20", "4h", 5, 15
        )

    @pytest.mark.asyncio
    async def test_analyze_market_structure_with_df(self) -> None:
        """Teszteli az analyze_market_structure async metódust DataFrame-mel."""
        mock_service = MagicMock(spec=StrategyServiceInterface)
        mock_df = MagicMock()
        mock_result_df = MagicMock()
        mock_service.analyze_market_structure = AsyncMock(return_value=mock_result_df)
        result = await mock_service.analyze_market_structure("EURUSD", "2024-03-20", "1h", mock_df)
        assert result is mock_result_df
        mock_service.analyze_market_structure.assert_called_once_with(
            "EURUSD", "2024-03-20", "1h", mock_df
        )

    @pytest.mark.asyncio
    async def test_analyze_market_structure_without_df(self) -> None:
        """Teszteli az analyze_market_structure async metódust DataFrame nélkül."""
        mock_service = MagicMock(spec=StrategyServiceInterface)
        mock_result_df = MagicMock()
        mock_service.analyze_market_structure = AsyncMock(return_value=mock_result_df)
        result = await mock_service.analyze_market_structure("EURUSD", "2024-03-20", "1h")
        assert result is mock_result_df
        mock_service.analyze_market_structure.assert_called_once_with(
            "EURUSD", "2024-03-20", "1h"
        )

    def test_interface_has_all_required_methods(self) -> None:
        """Teszteli, hogy az interfész tartalmazza az összes szükséges metódust."""
        required_methods = [
            "get_strategies",
            "create_strategy",
            "update_strategy",
            "delete_strategy",
            "backtest_strategy",
            "get_backtest_status",
            "optimize_strategy",
            "get_candles",
            "run_sma_backtest",
            "analyze_market_structure",
        ]
        for method in required_methods:
            assert hasattr(StrategyServiceInterface, method)

    def test_mock_implements_interface(self) -> None:
        """Teszteli, hogy a mock objektum implementálja az interfészt."""
        mock_service = MagicMock(spec=StrategyServiceInterface)
        assert hasattr(mock_service, "get_strategies")
        assert hasattr(mock_service, "create_strategy")
        assert hasattr(mock_service, "update_strategy")
        assert hasattr(mock_service, "delete_strategy")
        assert hasattr(mock_service, "backtest_strategy")
        assert hasattr(mock_service, "get_backtest_status")
        assert hasattr(mock_service, "optimize_strategy")
        assert hasattr(mock_service, "get_candles")
        assert hasattr(mock_service, "run_sma_backtest")
        assert hasattr(mock_service, "analyze_market_structure")
