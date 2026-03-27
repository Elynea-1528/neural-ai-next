"""Unit tesztek a StrategyService osztályhoz."""

from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from neural_ai.ui.services.strategy_service import StrategyService


class TestStrategyService:
    """Tesztek a StrategyService osztályhoz."""

    def test_initialization(self) -> None:
        """Teszt: StrategyService inicializálása."""
        logger = MagicMock()
        config: dict[str, Any] = {}
        core_components = MagicMock()

        service = StrategyService(logger=logger, config=config, core_components=core_components)

        assert service._logger is logger  # type: ignore
        assert service._config == config  # type: ignore
        assert service._core_components is core_components  # type: ignore
        assert len(service._strategies) == 2  # type: ignore
        assert "moving_avg_cross" in service._strategies  # type: ignore
        assert "rsi_strategy" in service._strategies  # type: ignore

    def test_get_strategies(self) -> None:
        """Teszt: Stratégiák lekérdezése."""
        service = StrategyService(logger=MagicMock(), config={}, core_components=MagicMock())

        strategies = service.get_strategies()

        assert len(strategies) == 2
        assert strategies[0]["id"] == "moving_avg_cross"
        assert strategies[0]["name"] == "Mozgóátlag Kereszt"
        assert strategies[1]["id"] == "rsi_strategy"
        assert strategies[1]["name"] == "RSI Stratégia"

    def test_create_strategy(self) -> None:
        """Teszt: Új stratégia létrehozása."""
        service = StrategyService(logger=MagicMock(), config={}, core_components=MagicMock())
        config = {"param1": "value1"}
        code = "def strategy(): pass"

        strategy_id = service.create_strategy(name="Test Strategy", config=config, code=code)

        assert strategy_id == "strategy_3"
        assert strategy_id in service._strategies  # type: ignore
        assert service._strategies[strategy_id]["name"] == "Test Strategy"  # type: ignore
        assert service._strategies[strategy_id]["config"] == config  # type: ignore
        assert service._strategies[strategy_id]["code"] == code  # type: ignore
        assert service._strategies[strategy_id]["status"] == "active"  # type: ignore

    def test_update_strategy_config(self) -> None:
        """Teszt: Stratégia konfigurációjának módosítása."""
        service = StrategyService(logger=MagicMock(), config={}, core_components=MagicMock())
        strategy_id = service.create_strategy(
            name="Test", config={"old": "value"}, code="old_code"
        )
        new_config = {"new": "value"}

        result = service.update_strategy(strategy_id=strategy_id, config=new_config)

        assert result is True
        assert service._strategies[strategy_id]["config"] == new_config  # type: ignore
        assert "updated_at" in service._strategies[strategy_id]  # type: ignore

    def test_update_strategy_code(self) -> None:
        """Teszt: Stratégia kódjának módosítása."""
        service = StrategyService(logger=MagicMock(), config={}, core_components=MagicMock())
        strategy_id = service.create_strategy(name="Test", config={}, code="old_code")
        new_code = "def new_strategy(): pass"

        result = service.update_strategy(strategy_id=strategy_id, code=new_code)

        assert result is True
        assert service._strategies[strategy_id]["code"] == new_code  # type: ignore

    def test_update_strategy_unknown(self) -> None:
        """Teszt: Ismeretlen stratégia módosítása hibát dob."""
        service = StrategyService(logger=MagicMock(), config={}, core_components=MagicMock())

        with pytest.raises(ValueError, match="Ismeretlen stratégia"):
            service.update_strategy(strategy_id="unknown", config={})

    def test_delete_strategy_success(self) -> None:
        """Teszt: Stratégia sikeres törlése."""
        service = StrategyService(logger=MagicMock(), config={}, core_components=MagicMock())
        strategy_id = service.create_strategy(name="Test", config={}, code="code")

        result = service.delete_strategy(strategy_id=strategy_id)

        assert result is True
        assert strategy_id not in service._strategies  # type: ignore

    def test_delete_strategy_unknown(self) -> None:
        """Teszt: Ismeretlen stratégia törlése hibát dob."""
        service = StrategyService(logger=MagicMock(), config={}, core_components=MagicMock())

        with pytest.raises(ValueError, match="Ismeretlen stratégia"):
            service.delete_strategy(strategy_id="unknown")

    def test_backtest_strategy(self) -> None:
        """Teszt: Stratégia backtestelése."""
        service = StrategyService(logger=MagicMock(), config={}, core_components=MagicMock())
        strategy_id = "moving_avg_cross"

        result = service.backtest_strategy(
            strategy_id=strategy_id,
            start_date="2024-01-01",
            end_date="2024-01-31",
            initial_capital=10000.0,
        )

        assert "backtest_id" in result
        assert result["strategy_id"] == strategy_id
        assert result["status"] == "started"
        assert "message" in result

    def test_get_backtest_status(self) -> None:
        """Teszt: Backtest állapotának lekérdezése."""
        service = StrategyService(logger=MagicMock(), config={}, core_components=MagicMock())
        backtest_result = service.backtest_strategy(
            strategy_id="moving_avg_cross",
            start_date="2024-01-01",
            end_date="2024-01-31",
            initial_capital=10000.0,
        )
        backtest_id = backtest_result["backtest_id"]

        result = service.get_backtest_status(backtest_id=backtest_id)

        assert result["backtest_id"] == backtest_id
        assert result["status"] == "completed"
        assert result["total_return"] == 0.15
        assert result["sharpe_ratio"] == 1.2

    def test_get_backtest_status_unknown(self) -> None:
        """Teszt: Ismeretlen backtest állapotának lekérdezése hibát dob."""
        service = StrategyService(logger=MagicMock(), config={}, core_components=MagicMock())

        with pytest.raises(ValueError, match="Ismeretlen backtest"):
            service.get_backtest_status(backtest_id="unknown")

    def test_optimize_strategy(self) -> None:
        """Teszt: Stratégia optimalizálása."""
        service = StrategyService(logger=MagicMock(), config={}, core_components=MagicMock())
        strategy_id = "moving_avg_cross"
        parameters = {"fast_period": [5, 10, 15], "slow_period": [20, 30, 40]}

        result = service.optimize_strategy(
            strategy_id=strategy_id, parameters=parameters, optimization_method="grid"
        )

        assert "optimization_id" in result
        assert result["strategy_id"] == strategy_id
        assert result["status"] == "started"
        assert "message" in result

    def test_optimize_strategy_unknown(self) -> None:
        """Teszt: Ismeretlen stratégia optimalizálása hibát dob."""
        service = StrategyService(logger=MagicMock(), config={}, core_components=MagicMock())

        with pytest.raises(ValueError, match="Ismeretlen stratégia"):
            service.optimize_strategy(strategy_id="unknown", parameters={})

    @pytest.mark.asyncio
    async def test_get_candles_success(self) -> None:
        """Teszt: Gyertyák lekérdezése sikeresen."""
        service = StrategyService(logger=MagicMock(), config={}, core_components=MagicMock())
        mock_resampler = AsyncMock()
        mock_df = MagicMock()
        mock_resampler.resample.return_value = mock_df

        with patch(
            "neural_ai.processors.resampler_service.factory.ResamplerServiceFactory.get_instance",
            return_value=mock_resampler,
        ):
            result = await service.get_candles(
                symbol="EURUSD", date="2024-03-20", timeframe="1h"
            )

        assert result is mock_df
        mock_resampler.resample.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_candles_error(self) -> None:
        """Teszt: Gyertyák lekérdezése hiba esetén hibát dob."""
        service = StrategyService(logger=MagicMock(), config={}, core_components=MagicMock())
        mock_resampler = AsyncMock()
        mock_resampler.resample.side_effect = Exception("Test error")

        with (
            patch(
                "neural_ai.processors.resampler_service.factory.ResamplerServiceFactory.get_instance",
                return_value=mock_resampler,
            ),
            pytest.raises(Exception, match="Test error"),
        ):
            await service.get_candles(symbol="EURUSD", date="2024-03-20", timeframe="1h")

    @pytest.mark.asyncio
    async def test_analyze_market_structure_with_df(self) -> None:
        """Teszt: Piaci struktúra elemzése megadott DataFrame-mel."""
        service = StrategyService(logger=MagicMock(), config={}, core_components=MagicMock())
        mock_df = MagicMock()
        mock_df.is_empty.return_value = False
        mock_df.empty = False
        mock_config = MagicMock()
        mock_logger = MagicMock()
        mock_processor = MagicMock()
        mock_processed_df = MagicMock()
        mock_processor.process.return_value = mock_processed_df

        service._core_components.get_component = MagicMock(  # type: ignore
            side_effect=lambda x: mock_config if x == "config" else mock_logger
        )

        with patch(
            "neural_ai.processors.factory.create_dimension_processor",
            return_value=mock_processor,
        ):
            result = await service.analyze_market_structure(
                symbol="EURUSD", date="2024-03-20", timeframe="1h", df=mock_df
            )

        assert result is mock_processed_df
        mock_processor.process.assert_called_once_with(mock_df, timeframe="1h")

    @pytest.mark.asyncio
    async def test_analyze_market_structure_without_df(self) -> None:
        """Teszt: Piaci struktúra elemzése DataFrame nélkül (betöltéssel)."""
        service = StrategyService(logger=MagicMock(), config={}, core_components=MagicMock())
        mock_df = MagicMock()
        mock_df.is_empty.return_value = False
        mock_df.empty = False
        mock_config = MagicMock()
        mock_logger = MagicMock()
        mock_processor = MagicMock()
        mock_processed_df = MagicMock()
        mock_processor.process.return_value = mock_processed_df

        service._core_components.get_component = MagicMock(  # type: ignore
            side_effect=lambda x: mock_config if x == "config" else mock_logger
        )

        with (
            patch.object(service, "get_candles", return_value=mock_df),
            patch(
                "neural_ai.processors.factory.create_dimension_processor",
                return_value=mock_processor,
            ),
        ):
            result = await service.analyze_market_structure(
                symbol="EURUSD", date="2024-03-20", timeframe="1h"
            )

        assert result is mock_processed_df

    @pytest.mark.asyncio
    async def test_analyze_market_structure_empty_df(self) -> None:
        """Teszt: Piaci struktúra elemzése üres DataFrame-mel hibát dob."""
        service = StrategyService(logger=MagicMock(), config={}, core_components=MagicMock())
        mock_df = MagicMock()
        mock_df.is_empty.return_value = True

        with pytest.raises(ValueError, match="Nincs elérhető adat"):
            await service.analyze_market_structure(
                symbol="EURUSD", date="2024-03-20", timeframe="1h", df=mock_df
            )

    @pytest.mark.asyncio
    async def test_analyze_market_structure_no_config(self) -> None:
        """Teszt: Piaci struktúra elemzése config nélkül hibát dob."""
        service = StrategyService(logger=MagicMock(), config={}, core_components=MagicMock())
        mock_df = MagicMock()
        mock_df.is_empty.return_value = False
        mock_df.empty = False

        service._core_components.get_component = MagicMock(return_value=None)  # type: ignore

        with pytest.raises(RuntimeError, match="Config vagy Logger komponens nem elérhető"):
            await service.analyze_market_structure(
                symbol="EURUSD", date="2024-03-20", timeframe="1h", df=mock_df
            )
