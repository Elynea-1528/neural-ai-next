"""Tesztek az EventBusFactory-hez.

Ez a modul tartalmazza az EventBusFactory tesztjeit.

Author: Neural AI Next Team
Version: 1.0.0
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from neural_ai.core.events.factory import EventBusFactory
from neural_ai.core.events.interfaces.event_bus_interface import (
    EventBusConfig,
    EventBusInterface,
)


class TestEventBusFactoryCreate:
    """EventBusFactory create metódus tesztek."""

    @patch("neural_ai.core.events.implementations.zeromq_bus.EventBus")
    def test_create_default(self, mock_event_bus_class: MagicMock) -> None:
        """Teszteli az alapértelmezett EventBus létrehozást."""
        mock_event_bus = MagicMock()
        mock_event_bus_class.return_value = mock_event_bus

        mock_logger = MagicMock()
        factory = EventBusFactory(mock_logger)
        result = factory.create()

        mock_event_bus_class.assert_called_once_with(None, mock_logger)
        assert result == mock_event_bus

    @patch("neural_ai.core.events.implementations.zeromq_bus.EventBus")
    def test_create_with_config(self, mock_event_bus_class: MagicMock) -> None:
        """Teszteli az EventBus létrehozást konfigurációval."""
        mock_event_bus = MagicMock()
        mock_event_bus_class.return_value = mock_event_bus

        config = EventBusConfig(pub_port=6666, sub_port=6667)
        mock_logger = MagicMock()
        factory = EventBusFactory(mock_logger)
        result = factory.create(config)

        mock_event_bus_class.assert_called_once_with(config, mock_logger)
        assert result == mock_event_bus

    def test_create_returns_interface(self) -> None:
        """Teszteli, hogy az EventBusFactory EventBusInterface-t ad vissza."""
        mock_logger = MagicMock()
        factory = EventBusFactory(mock_logger)
        result = factory.create()

        assert isinstance(result, EventBusInterface)


class TestEventBusFactoryCreateAndStart:
    """EventBusFactory create_and_start metódus tesztek."""

    @pytest.mark.asyncio
    @patch("neural_ai.core.events.implementations.zeromq_bus.EventBus")
    async def test_create_and_start_default(self, mock_event_bus_class: MagicMock) -> None:
        """Teszteli az alapértelmezett EventBus létrehozást és indítását."""
        mock_event_bus = AsyncMock()
        mock_event_bus_class.return_value = mock_event_bus

        mock_logger = MagicMock()
        factory = EventBusFactory(mock_logger)
        result = await factory.create_and_start()

        mock_event_bus_class.assert_called_once_with(None, mock_logger)
        mock_event_bus.start.assert_awaited_once()
        assert result == mock_event_bus

    @pytest.mark.asyncio
    @patch("neural_ai.core.events.implementations.zeromq_bus.EventBus")
    async def test_create_and_start_with_config(self, mock_event_bus_class: MagicMock) -> None:
        """Teszteli az EventBus létrehozást és indítását konfigurációval."""
        mock_event_bus = AsyncMock()
        mock_event_bus_class.return_value = mock_event_bus

        config = EventBusConfig(pub_port=6666, sub_port=6667)
        mock_logger = MagicMock()
        factory = EventBusFactory(mock_logger)
        result = await factory.create_and_start(config)

        mock_event_bus_class.assert_called_once_with(config, mock_logger)
        mock_event_bus.start.assert_awaited_once()
        assert result == mock_event_bus

    @pytest.mark.asyncio
    async def test_create_and_start_returns_interface(self) -> None:
        """Teszteli, hogy a create_and_start EventBusInterface-t ad vissza."""
        mock_logger = MagicMock()
        factory = EventBusFactory(mock_logger)
        result = await factory.create_and_start()

        assert isinstance(result, EventBusInterface)


class TestEventBusFactoryGetEventBus:
    """EventBusFactory get_event_bus statikus metódus tesztek."""

    @patch("neural_ai.core.events.implementations.zeromq_bus.EventBus")
    def test_get_event_bus_creates_with_logger(self, mock_event_bus_class: MagicMock) -> None:
        """Teszteli a get_event_bus statikus metódust."""
        mock_event_bus = MagicMock()
        mock_event_bus_class.return_value = mock_event_bus
        mock_logger = MagicMock()

        result = EventBusFactory.get_event_bus(mock_logger)

        mock_event_bus_class.assert_called_once_with(logger=mock_logger)
        assert result == mock_event_bus

    def test_get_event_bus_returns_interface(self) -> None:
        """Teszteli, hogy a get_event_bus EventBusInterface-t ad vissza."""
        mock_logger = MagicMock()
        result = EventBusFactory.get_event_bus(mock_logger)

        assert isinstance(result, EventBusInterface)


class TestEventBusFactoryStaticMethods:
    """EventBusFactory példány metódusok tesztek."""

    def test_factory_methods_are_instance_methods(self) -> None:
        """Teszteli, hogy a factory metódusok példány metódusok."""
        # Ellenőrizzük, hogy a metódusok példány metódusok-e
        # self paramétert kell várniuk (unbound signature)
        import inspect

        create_sig = inspect.signature(EventBusFactory.create)
        assert "self" in create_sig.parameters

        create_and_start_sig = inspect.signature(EventBusFactory.create_and_start)
        assert "self" in create_and_start_sig.parameters
