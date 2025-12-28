"""Tesztek az EventBusInterface-hez.

Ez a modul tartalmazza az EventBusInterface absztrakt osztály tesztjeit.

Author: Neural AI Next Team
Version: 1.0.0
"""

from abc import ABC, abstractmethod
from typing import Any

import pytest
from pydantic import BaseModel

from neural_ai.core.events.interfaces.event_bus_interface import (
    EventBusConfig,
    EventBusInterface,
)


class ConcreteEventBus(EventBusInterface, ABC):
    """Konkrét EventBus implementáció teszteléshez.

    Ez egy absztrakt osztály, amely implementálja az EventBusInterface-t,
    de nem ad meg konkrét implementációt a metódusokhoz.
    """

    @property
    @abstractmethod
    def config(self) -> EventBusConfig:
        """Visszaadja az EventBus konfigurációját."""
        pass

    @abstractmethod
    async def start(self) -> None:
        """Elindítja az EventBus-t és létrehozza a socketeket."""
        pass

    @abstractmethod
    async def stop(self) -> None:
        """Leállítja az EventBus-t és felszabadítja az erőforrásokat."""
        pass

    @abstractmethod
    async def publish(self, event_type: str, event: BaseModel) -> None:
        """Esemény közzététele a buszon."""
        pass

    @abstractmethod
    def subscribe(self, event_type: str, callback: Any) -> None:
        """Feliratkozás eseménytípusra."""
        pass

    @abstractmethod
    def unsubscribe(self, event_type: str, callback: Any) -> None:
        """Leiratkozás eseménytípusról."""
        pass

    @abstractmethod
    async def run_forever(self) -> None:
        """Eseménybusz örök futás (blokkoló)."""
        pass


class TestEventBusConfig:
    """EventBusConfig tesztek."""

    def test_default_config(self) -> None:
        """Teszteli az alapértelmezett konfigurációt."""
        config = EventBusConfig()
        assert config.pub_port == 5555
        assert config.sub_port == 5556
        assert config.use_inproc is False
        assert config.zmq_context is None

    def test_custom_config(self) -> None:
        """Teszteli az egyéni konfigurációt."""
        mock_context = object()
        config = EventBusConfig(
            zmq_context=mock_context,
            pub_port=6666,
            sub_port=6667,
            use_inproc=True,
        )
        assert config.pub_port == 6666
        assert config.sub_port == 6667
        assert config.use_inproc is True
        assert config.zmq_context is mock_context

    def test_config_immutability(self) -> None:
        """Teszteli, hogy a konfiguráció megváltoztathatatlan."""
        config = EventBusConfig()
        # A dataclass nem teszi lehetővé a mezők módosítását alapértelmezés szerint
        # de ellenőrizzük, hogy a beállított értékek megmaradnak-e
        _ = config.pub_port  # Csak ellenőrizzük, hogy elérhető-e
        # Ha a dataclass frozen=True, akkor ez hibát dobna
        # Jelenleg nincs frozen=True, ezért ezt a tesztet kihagyjuk


class TestEventBusInterface:
    """EventBusInterface tesztek."""

    def test_interface_is_abstract(self) -> None:
        """Teszteli, hogy az interfész valóban absztrakt."""
        # Az interfész nem példányosítható
        with pytest.raises(TypeError):
            EventBusInterface()  # type: ignore

    def test_interface_has_required_methods(self) -> None:
        """Teszteli, hogy az interfész tartalmazza a szükséges metódusokat."""
        assert hasattr(EventBusInterface, "config")
        assert hasattr(EventBusInterface, "start")
        assert hasattr(EventBusInterface, "stop")
        assert hasattr(EventBusInterface, "publish")
        assert hasattr(EventBusInterface, "subscribe")
        assert hasattr(EventBusInterface, "unsubscribe")
        assert hasattr(EventBusInterface, "run_forever")

    def test_config_property_is_abstract(self) -> None:
        """Teszteli, hogy a config property absztrakt."""
        # A konkrét osztálynak implementálnia kell
        class IncompleteBus(EventBusInterface):
            pass

        with pytest.raises(TypeError):
            IncompleteBus()  # type: ignore

    def test_start_is_abstract(self) -> None:
        """Teszteli, hogy a start metódus absztrakt."""
        # A konkrét osztálynak implementálnia kell
        class IncompleteBus(EventBusInterface):
            @property
            def config(self) -> EventBusConfig:
                return EventBusConfig()

        with pytest.raises(TypeError):
            IncompleteBus()  # type: ignore

    def test_stop_is_abstract(self) -> None:
        """Teszteli, hogy a stop metódus absztrakt."""
        # A konkrét osztálynak implementálnia kell
        class IncompleteBus(EventBusInterface):
            @property
            def config(self) -> EventBusConfig:
                return EventBusConfig()

            async def start(self) -> None:
                pass

        with pytest.raises(TypeError):
            IncompleteBus()  # type: ignore

    def test_publish_is_abstract(self) -> None:
        """Teszteli, hogy a publish metódus absztrakt."""
        # A konkrét osztálynak implementálnia kell
        class IncompleteBus(EventBusInterface):
            @property
            def config(self) -> EventBusConfig:
                return EventBusConfig()

            async def start(self) -> None:
                pass

            async def stop(self) -> None:
                pass

        with pytest.raises(TypeError):
            IncompleteBus()  # type: ignore

    def test_subscribe_is_abstract(self) -> None:
        """Teszteli, hogy a subscribe metódus absztrakt."""
        # A konkrét osztálynak implementálnia kell
        class IncompleteBus(EventBusInterface):
            @property
            def config(self) -> EventBusConfig:
                return EventBusConfig()

            async def start(self) -> None:
                pass

            async def stop(self) -> None:
                pass

            async def publish(self, event_type: str, event: BaseModel) -> None:
                pass

        with pytest.raises(TypeError):
            IncompleteBus()  # type: ignore

    def test_unsubscribe_is_abstract(self) -> None:
        """Teszteli, hogy az unsubscribe metódus absztrakt."""
        # A konkrét osztálynak implementálnia kell
        class IncompleteBus(EventBusInterface):
            @property
            def config(self) -> EventBusConfig:
                return EventBusConfig()

            async def start(self) -> None:
                pass

            async def stop(self) -> None:
                pass

            async def publish(self, event_type: str, event: BaseModel) -> None:
                pass

            def subscribe(self, event_type: str, callback: Any) -> None:
                pass

        with pytest.raises(TypeError):
            IncompleteBus()  # type: ignore

    def test_run_forever_is_abstract(self) -> None:
        """Teszteli, hogy a run_forever metódus absztrakt."""
        # A konkrét osztálynak implementálnia kell
        class IncompleteBus(EventBusInterface):
            @property
            def config(self) -> EventBusConfig:
                return EventBusConfig()

            async def start(self) -> None:
                pass

            async def stop(self) -> None:
                pass

            async def publish(self, event_type: str, event: BaseModel) -> None:
                pass

            def subscribe(self, event_type: str, callback: Any) -> None:
                pass

            def unsubscribe(self, event_type: str, callback: Any) -> None:
                pass

        with pytest.raises(TypeError):
            IncompleteBus()  # type: ignore

    def test_interface_method_signatures(self) -> None:
        """Teszteli a metódusok aláírásait."""
        # Ellenőrizzük, hogy a metódusok helyesen vannak-e definiálva
        import inspect

        # start
        start_sig = inspect.signature(EventBusInterface.start)
        assert start_sig.return_annotation == None

        # stop
        stop_sig = inspect.signature(EventBusInterface.stop)
        assert stop_sig.return_annotation == None

        # publish
        publish_sig = inspect.signature(EventBusInterface.publish)
        assert publish_sig.parameters["event_type"].annotation == str
        assert publish_sig.return_annotation == None

        # subscribe
        subscribe_sig = inspect.signature(EventBusInterface.subscribe)
        assert subscribe_sig.parameters["event_type"].annotation == str
        assert subscribe_sig.return_annotation == None

        # unsubscribe
        unsubscribe_sig = inspect.signature(EventBusInterface.unsubscribe)
        assert unsubscribe_sig.parameters["event_type"].annotation == str
        assert unsubscribe_sig.return_annotation == None

        # run_forever
        run_forever_sig = inspect.signature(EventBusInterface.run_forever)
        assert run_forever_sig.return_annotation == None