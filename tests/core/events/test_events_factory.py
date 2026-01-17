"""Tesztek az EventBusFactory-hez.

Ez a modul tartalmazza az EventBusFactory tesztjeit.

Author: Neural AI Next Team
Version: 1.0.0
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.events.factory import EventBusFactory
from neural_ai.core.events.interfaces.event_bus_interface import (
    EventBusConfig,
    EventBusInterface,
)
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface


class TestEventBusFactoryCreate:
    """EventBusFactory create metódus tesztek."""

    @patch("neural_ai.core.events.implementations.zeromq_bus.EventBus")
    def test_create_default(self, mock_event_bus_class: MagicMock) -> None:
        """Teszteli az alapértelmezett EventBus létrehozást."""
        mock_event_bus = MagicMock()
        mock_event_bus_class.return_value = mock_event_bus

        result = EventBusFactory.create()

        mock_event_bus_class.assert_called_once_with(None)
        assert result == mock_event_bus

    @patch("neural_ai.core.events.implementations.zeromq_bus.EventBus")
    def test_create_with_config(self, mock_event_bus_class: MagicMock) -> None:
        """Teszteli az EventBus létrehozást konfigurációval."""
        mock_event_bus = MagicMock()
        mock_event_bus_class.return_value = mock_event_bus

        config = EventBusConfig(pub_port=6666, sub_port=6667)
        result = EventBusFactory.create(config)

        mock_event_bus_class.assert_called_once_with(config)
        assert result == mock_event_bus

    def test_create_returns_interface(self) -> None:
        """Teszteli, hogy az EventBusFactory EventBusInterface-t ad vissza."""
        result = EventBusFactory.create()

        assert isinstance(result, EventBusInterface)


class TestEventBusFactoryCreateAndStart:
    """EventBusFactory create_and_start metódus tesztek."""

    @pytest.mark.asyncio
    @patch("neural_ai.core.events.implementations.zeromq_bus.EventBus")
    async def test_create_and_start_default(
        self, mock_event_bus_class: MagicMock
    ) -> None:
        """Teszteli az alapértelmezett EventBus létrehozást és indítását."""
        mock_event_bus = AsyncMock()
        mock_event_bus_class.return_value = mock_event_bus

        result = await EventBusFactory.create_and_start()

        mock_event_bus_class.assert_called_once_with(None)
        mock_event_bus.start.assert_awaited_once()
        assert result == mock_event_bus

    @pytest.mark.asyncio
    @patch("neural_ai.core.events.implementations.zeromq_bus.EventBus")
    async def test_create_and_start_with_config(
        self, mock_event_bus_class: MagicMock
    ) -> None:
        """Teszteli az EventBus létrehozást és indítását konfigurációval."""
        mock_event_bus = AsyncMock()
        mock_event_bus_class.return_value = mock_event_bus

        config = EventBusConfig(pub_port=6666, sub_port=6667)
        result = await EventBusFactory.create_and_start(config)

        mock_event_bus_class.assert_called_once_with(config)
        mock_event_bus.start.assert_awaited_once()
        assert result == mock_event_bus

    @pytest.mark.asyncio
    async def test_create_and_start_returns_interface(self) -> None:
        """Teszteli, hogy a create_and_start EventBusInterface-t ad vissza."""
        result = await EventBusFactory.create_and_start()

        assert isinstance(result, EventBusInterface)


class TestEventBusFactoryCreateFromConfig:
    """EventBusFactory create_from_config metódus tesztek."""

    def test_create_from_config_success(self) -> None:
        """Teszteli a sikeres EventBus létrehozást konfigurációkezelőből."""
        mock_config_manager = MagicMock(spec=ConfigManagerInterface)
        mock_config_manager.get_section.return_value = {
            "pub_port": 7777,
            "sub_port": 7778,
            "use_inproc": True,
        }

        with patch(
            "neural_ai.core.events.implementations.zeromq_bus.EventBus"
        ) as mock_event_bus_class:
            mock_event_bus = MagicMock()
            mock_event_bus_class.return_value = mock_event_bus

            result = EventBusFactory.create_from_config(mock_config_manager)

            mock_config_manager.get_section.assert_called_once_with("events")
            mock_event_bus_class.assert_called_once()
            called_config = mock_event_bus_class.call_args[0][0]
            assert called_config.pub_port == 7777
            assert called_config.sub_port == 7778
            assert called_config.use_inproc is True
            assert result == mock_event_bus

    def test_create_from_config_with_key_error(self) -> None:
        """Teszteli az EventBus létrehozást KeyError esetén."""
        mock_config_manager = MagicMock(spec=ConfigManagerInterface)
        mock_config_manager.get_section.side_effect = KeyError("Section not found")

        with patch(
            "neural_ai.core.events.implementations.zeromq_bus.EventBus"
        ) as mock_event_bus_class:
            mock_event_bus = MagicMock()
            mock_event_bus_class.return_value = mock_event_bus

            _ = EventBusFactory.create_from_config(mock_config_manager)

            mock_config_manager.get_section.assert_called_once_with("events")
            mock_event_bus_class.assert_called_once()
            called_config = mock_event_bus_class.call_args[0][0]
            assert called_config.pub_port == 5555  # Alapértelmezett
            assert called_config.sub_port == 5556  # Alapértelmezett
            assert called_config.use_inproc is False  # Alapértelmezett

    def test_create_from_config_with_value_error(self) -> None:
        """Teszteli az EventBus létrehozást ValueError esetén."""
        mock_config_manager = MagicMock(spec=ConfigManagerInterface)
        mock_config_manager.get_section.side_effect = ValueError("Invalid value")

        with patch(
            "neural_ai.core.events.implementations.zeromq_bus.EventBus"
        ) as mock_event_bus_class:
            mock_event_bus = MagicMock()
            mock_event_bus_class.return_value = mock_event_bus

            _ = EventBusFactory.create_from_config(mock_config_manager)

            mock_config_manager.get_section.assert_called_once_with("events")
            mock_event_bus_class.assert_called_once()
            called_config = mock_event_bus_class.call_args[0][0]
            assert called_config.pub_port == 5555  # Alapértelmezett
            assert called_config.sub_port == 5556  # Alapértelmezett
            assert called_config.use_inproc is False  # Alapértelmezett

    def test_create_from_config_partial_config(self) -> None:
        """Teszteli az EventBus létrehozást részleges konfigurációval."""
        mock_config_manager = MagicMock(spec=ConfigManagerInterface)
        mock_config_manager.get_section.return_value = {
            "pub_port": 8888,
            # sub_port és use_inproc hiányzik
        }

        with patch(
            "neural_ai.core.events.implementations.zeromq_bus.EventBus"
        ) as mock_event_bus_class:
            mock_event_bus = MagicMock()
            mock_event_bus_class.return_value = mock_event_bus

            _ = EventBusFactory.create_from_config(mock_config_manager)

            mock_config_manager.get_section.assert_called_once_with("events")
            mock_event_bus_class.assert_called_once()
            called_config = mock_event_bus_class.call_args[0][0]
            assert called_config.pub_port == 8888  # Beállított érték
            assert called_config.sub_port == 5556  # Alapértelmezett
            assert called_config.use_inproc is False  # Alapértelmezett

    def test_create_from_config_returns_interface(self) -> None:
        """Teszteli, hogy a create_from_config EventBusInterface-t ad vissza."""
        mock_config_manager = MagicMock(spec=ConfigManagerInterface)
        mock_config_manager.get_section.return_value = {}

        result = EventBusFactory.create_from_config(mock_config_manager)

        assert isinstance(result, EventBusInterface)


class TestEventBusFactoryStaticMethods:
    """EventBusFactory statikus metódusok tesztek."""

    def test_factory_methods_are_static(self) -> None:
        """Teszteli, hogy a factory metódusok valóban statikusak."""
        # Ellenőrizzük, hogy a metódusok statikusak-e
        # Ha nem lennének statikusak, akkor self paramétert várnának
        import inspect

        create_sig = inspect.signature(EventBusFactory.create)
        assert "self" not in create_sig.parameters

        create_and_start_sig = inspect.signature(EventBusFactory.create_and_start)
        assert "self" not in create_and_start_sig.parameters

        create_from_config_sig = inspect.signature(EventBusFactory.create_from_config)
        assert "self" not in create_from_config_sig.parameters
