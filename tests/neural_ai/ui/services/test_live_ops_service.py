"""Unit tesztek a LiveOpsService osztályhoz."""

from typing import Any
from unittest.mock import MagicMock

import pytest

from neural_ai.ui.services.live_ops_service import LiveOpsService


class TestLiveOpsService:
    """Tesztek a LiveOpsService osztályhoz."""

    def test_initialization(self) -> None:
        """Teszt: LiveOpsService inicializálása."""
        logger = MagicMock()
        config: dict[str, Any] = {}
        core_components = MagicMock()

        service = LiveOpsService(logger=logger, config=config, core_components=core_components)

        assert service._logger is logger  # type: ignore
        assert service._config == config  # type: ignore
        assert service._core_components is core_components  # type: ignore
        assert service._positions == {}  # type: ignore
        assert service._orders == {}  # type: ignore
        assert service._market_subscribers == {}  # type: ignore

    def test_get_active_positions_empty(self) -> None:
        """Teszt: Aktív pozíciók lekérdezése üres állapotban."""
        service = LiveOpsService(logger=MagicMock(), config={}, core_components=MagicMock())

        positions = service.get_active_positions()

        assert positions == []

    def test_get_active_positions_with_active(self) -> None:
        """Teszt: Aktív pozíciók lekérdezése aktív pozíciókkal."""
        service = LiveOpsService(logger=MagicMock(), config={}, core_components=MagicMock())
        service._positions = {  # type: ignore
            "pos1": {
                "symbol": "EURUSD",
                "type": "BUY",
                "volume": 1.0,
                "entry_price": 1.0850,
                "current_price": 1.0860,
                "profit": 100.0,
                "status": "active",
            },
            "pos2": {
                "symbol": "GBPUSD",
                "type": "SELL",
                "volume": 0.5,
                "entry_price": 1.2500,
                "status": "closed",
            },
        }

        positions = service.get_active_positions()

        assert len(positions) == 1
        assert positions[0]["id"] == "pos1"
        assert positions[0]["symbol"] == "EURUSD"
        assert positions[0]["type"] == "BUY"
        assert positions[0]["volume"] == 1.0
        assert positions[0]["entry_price"] == 1.0850
        assert positions[0]["current_price"] == 1.0860
        assert positions[0]["profit"] == 100.0
        assert positions[0]["status"] == "active"

    def test_get_account_status(self) -> None:
        """Teszt: Fiók állapotának lekérdezése."""
        service = LiveOpsService(logger=MagicMock(), config={}, core_components=MagicMock())

        status = service.get_account_status()

        assert "balance" in status
        assert "equity" in status
        assert "margin" in status
        assert "free_margin" in status
        assert "margin_level" in status
        assert "used_margin" in status
        assert "leverage" in status
        assert "currency" in status
        assert status["balance"] == 100000.0
        assert status["equity"] == 102500.0
        assert status["currency"] == "USD"

    def test_place_order_basic(self) -> None:
        """Teszt: Alapvető rendelés leadása."""
        service = LiveOpsService(logger=MagicMock(), config={}, core_components=MagicMock())

        order_id = service.place_order(symbol="EURUSD", order_type="BUY", volume=1.0)

        assert order_id == "order_1"
        assert order_id in service._orders  # type: ignore
        assert service._orders[order_id]["symbol"] == "EURUSD"  # type: ignore
        assert service._orders[order_id]["type"] == "BUY"  # type: ignore
        assert service._orders[order_id]["volume"] == 1.0  # type: ignore
        assert service._orders[order_id]["status"] == "pending"  # type: ignore

    def test_place_order_with_sl_tp(self) -> None:
        """Teszt: Rendelés leadása SL/TP szintekkel."""
        service = LiveOpsService(logger=MagicMock(), config={}, core_components=MagicMock())

        order_id = service.place_order(
            symbol="EURUSD",
            order_type="BUY",
            volume=1.0,
            price=1.0850,
            stop_loss=1.0800,
            take_profit=1.0900,
        )

        assert order_id == "order_1"
        assert service._orders[order_id]["price"] == 1.0850  # type: ignore
        assert service._orders[order_id]["stop_loss"] == 1.0800  # type: ignore
        assert service._orders[order_id]["take_profit"] == 1.0900  # type: ignore

    def test_modify_order_success(self) -> None:
        """Teszt: Rendelés sikeres módosítása."""
        service = LiveOpsService(logger=MagicMock(), config={}, core_components=MagicMock())
        order_id = service.place_order(symbol="EURUSD", order_type="BUY", volume=1.0, price=1.0850)

        result = service.modify_order(order_id=order_id, price=1.0860, stop_loss=1.0810)

        assert result is True
        assert service._orders[order_id]["price"] == 1.0860  # type: ignore
        assert service._orders[order_id]["stop_loss"] == 1.0810  # type: ignore
        assert "modified_at" in service._orders[order_id]  # type: ignore

    def test_modify_order_unknown(self) -> None:
        """Teszt: Ismeretlen rendelés módosítása hibát dob."""
        service = LiveOpsService(logger=MagicMock(), config={}, core_components=MagicMock())

        with pytest.raises(ValueError, match="Ismeretlen rendelés"):
            service.modify_order(order_id="unknown_order", price=1.0860)

    def test_cancel_order_success(self) -> None:
        """Teszt: Rendelés sikeres visszavonása."""
        service = LiveOpsService(logger=MagicMock(), config={}, core_components=MagicMock())
        order_id = service.place_order(symbol="EURUSD", order_type="BUY", volume=1.0)

        result = service.cancel_order(order_id=order_id)

        assert result is True
        assert service._orders[order_id]["status"] == "cancelled"  # type: ignore
        assert "cancelled_at" in service._orders[order_id]  # type: ignore

    def test_cancel_order_unknown(self) -> None:
        """Teszt: Ismeretlen rendelés visszavonása hibát dob."""
        service = LiveOpsService(logger=MagicMock(), config={}, core_components=MagicMock())

        with pytest.raises(ValueError, match="Ismeretlen rendelés"):
            service.cancel_order(order_id="unknown_order")

    def test_close_position_success(self) -> None:
        """Teszt: Pozíció sikeres lezárása."""
        service = LiveOpsService(logger=MagicMock(), config={}, core_components=MagicMock())
        service._positions = {  # type: ignore
            "pos1": {
                "symbol": "EURUSD",
                "type": "BUY",
                "volume": 1.0,
                "entry_price": 1.0850,
                "status": "active",
            }
        }

        result = service.close_position(position_id="pos1")

        assert result is True
        assert service._positions["pos1"]["status"] == "closed"  # type: ignore
        assert "closed_at" in service._positions["pos1"]  # type: ignore

    def test_close_position_unknown(self) -> None:
        """Teszt: Ismeretlen pozíció lezárása hibát dob."""
        service = LiveOpsService(logger=MagicMock(), config={}, core_components=MagicMock())

        with pytest.raises(ValueError, match="Ismeretlen pozíció"):
            service.close_position(position_id="unknown_position")

    def test_get_market_data(self) -> None:
        """Teszt: Piaci adatok lekérdezése."""
        service = LiveOpsService(logger=MagicMock(), config={}, core_components=MagicMock())

        market_data = service.get_market_data(symbol="EURUSD")

        assert market_data["symbol"] == "EURUSD"
        assert "bid" in market_data
        assert "ask" in market_data
        assert "spread" in market_data
        assert "high" in market_data
        assert "low" in market_data
        assert "volume" in market_data
        assert "timestamp" in market_data

    def test_subscribe_to_market_updates(self) -> None:
        """Teszt: Feliratkozás piaci frissítésekre."""
        service = LiveOpsService(logger=MagicMock(), config={}, core_components=MagicMock())
        callback = MagicMock()

        service.subscribe_to_market_updates(symbol="EURUSD", callback=callback)

        assert "EURUSD" in service._market_subscribers  # type: ignore
        assert callback in service._market_subscribers["EURUSD"]  # type: ignore

    def test_subscribe_to_market_updates_multiple(self) -> None:
        """Teszt: Több callback feliratkozása ugyanarra a szimbólumra."""
        service = LiveOpsService(logger=MagicMock(), config={}, core_components=MagicMock())
        callback1 = MagicMock()
        callback2 = MagicMock()

        service.subscribe_to_market_updates(symbol="EURUSD", callback=callback1)
        service.subscribe_to_market_updates(symbol="EURUSD", callback=callback2)

        assert len(service._market_subscribers["EURUSD"]) == 2  # type: ignore
        assert callback1 in service._market_subscribers["EURUSD"]  # type: ignore
        assert callback2 in service._market_subscribers["EURUSD"]  # type: ignore

    def test_get_performance_summary(self) -> None:
        """Teszt: Teljesítmény összegzés lekérdezése."""
        service = LiveOpsService(logger=MagicMock(), config={}, core_components=MagicMock())

        performance = service.get_performance_summary()

        assert "total_trades" in performance
        assert "winning_trades" in performance
        assert "losing_trades" in performance
        assert "win_rate" in performance
        assert "total_profit" in performance
        assert "total_loss" in performance
        assert "net_profit" in performance
        assert "max_drawdown" in performance
        assert "average_win" in performance
        assert "average_loss" in performance
        assert "profit_factor" in performance
        assert performance["total_trades"] == 150
        assert performance["win_rate"] == 0.613
        assert performance["net_profit"] == 5300.0
