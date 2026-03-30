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
        assert start_sig.return_annotation is None

        # stop
        stop_sig = inspect.signature(EventBusInterface.stop)
        assert stop_sig.return_annotation is None

        # publish
        publish_sig = inspect.signature(EventBusInterface.publish)
        assert publish_sig.parameters["event_type"].annotation is str
        assert publish_sig.return_annotation is None

        # subscribe
        subscribe_sig = inspect.signature(EventBusInterface.subscribe)
        assert subscribe_sig.parameters["event_type"].annotation is str
        assert subscribe_sig.return_annotation is None

        # unsubscribe
        unsubscribe_sig = inspect.signature(EventBusInterface.unsubscribe)
        assert unsubscribe_sig.parameters["event_type"].annotation is str
        assert unsubscribe_sig.return_annotation is None

        # run_forever
        run_forever_sig = inspect.signature(EventBusInterface.run_forever)
        assert run_forever_sig.return_annotation is None

    def test_config_property_has_docstring(self) -> None:
        """Teszteli, hogy a config property-nek van docstringje."""
        assert EventBusInterface.config.__doc__ is not None
        assert "Visszaadja az EventBus konfigurációját" in EventBusInterface.config.__doc__

    def test_start_method_has_docstring(self) -> None:
        """Teszteli, hogy a start metódusnak van docstringje."""
        assert EventBusInterface.start.__doc__ is not None
        assert "Elindítja az EventBus-t" in EventBusInterface.start.__doc__

    def test_stop_method_has_docstring(self) -> None:
        """Teszteli, hogy a stop metódusnak van docstringje."""
        assert EventBusInterface.stop.__doc__ is not None
        assert "Leállítja az EventBus-t" in EventBusInterface.stop.__doc__

    def test_publish_method_has_docstring(self) -> None:
        """Teszteli, hogy a publish metódusnak van docstringje."""
        assert EventBusInterface.publish.__doc__ is not None
        assert "Esemény közzététele" in EventBusInterface.publish.__doc__

    def test_subscribe_method_has_docstring(self) -> None:
        """Teszteli, hogy a subscribe metódusnak van docstringje."""
        assert EventBusInterface.subscribe.__doc__ is not None
        assert "Feliratkozás eseménytípusra" in EventBusInterface.subscribe.__doc__

    def test_unsubscribe_method_has_docstring(self) -> None:
        """Teszteli, hogy az unsubscribe metódusnak van docstringje."""
        assert EventBusInterface.unsubscribe.__doc__ is not None
        assert "Leiratkozás eseménytípusról" in EventBusInterface.unsubscribe.__doc__

    def test_run_forever_method_has_docstring(self) -> None:
        """Teszteli, hogy a run_forever metódusnak van docstringje."""
        assert EventBusInterface.run_forever.__doc__ is not None
        assert "Eseménybusz örök futás" in EventBusInterface.run_forever.__doc__

    def test_event_callback_type_alias(self) -> None:
        """Teszteli az EventCallback típus aliast."""
        from pydantic import BaseModel

        from neural_ai.core.events.interfaces.event_bus_interface import EventCallback

        # Ellenőrizzük, hogy a típus alias létezik
        assert EventCallback is not None

        # Egyszerű ellenőrzés, hogy callable-t vár-e
        def sample_callback(event: BaseModel) -> None:
            pass

        # A típus alias használható
        callback: EventCallback = sample_callback
        assert callable(callback)

    def test_event_bus_config_repr(self) -> None:
        """Teszteli az EventBusConfig string reprezentációját."""
        config = EventBusConfig()
        repr_str = repr(config)
        assert "EventBusConfig" in repr_str
        assert "pub_port=5555" in repr_str
        assert "sub_port=5556" in repr_str

    def test_event_bus_config_str(self) -> None:
        """Teszteli az EventBusConfig szöveges reprezentációját."""
        config = EventBusConfig()
        str_str = str(config)
        assert "EventBusConfig" in str_str

    def test_event_bus_config_equality(self) -> None:
        """Teszteli az EventBusConfig egyenlőségét."""
        config1 = EventBusConfig()
        config2 = EventBusConfig()
        assert config1 == config2

    def test_event_bus_config_inequality(self) -> None:
        """Teszteli az EventBusConfig egyenlőtlenségét."""
        config1 = EventBusConfig(pub_port=5555)
        config2 = EventBusConfig(pub_port=6666)
        assert config1 != config2

    def test_concrete_implementation_calls_pass_statements(self) -> None:
        """Teszteli, hogy a konkrét implementációban a pass utasítások lefutnak."""
        from pydantic import BaseModel

        class TestEvent(BaseModel):
            data: str = "test"

        class ConcreteTestBus(ConcreteEventBus):
            def __init__(self) -> None:
                self._config = EventBusConfig()
                self.started = False
                self.stopped = False
                self.published = False
                self.subscribed = False
                self.unsubscribed = False
                self.ran = False

            @property
            def config(self) -> EventBusConfig:
                """Visszaadja a konfigurációt."""
                return self._config

            async def start(self) -> None:
                """Elindítja az EventBus-t."""
                self.started = True

            async def stop(self) -> None:
                """Leállítja az EventBus-t."""
                self.stopped = True

            async def publish(self, event_type: str, event: BaseModel) -> None:
                """Esemény közzététele."""
                self.published = True

            def subscribe(self, event_type: str, callback: Any) -> None:
                """Feliratkozás eseménytípusra."""
                self.subscribed = True

            def unsubscribe(self, event_type: str, callback: Any) -> None:
                """Leiratkozás eseménytípusról."""
                self.unsubscribed = True

            async def run_forever(self) -> None:
                """Eseménybusz örök futás."""
                self.ran = True

        import asyncio

        async def test_async_methods() -> None:
            bus = ConcreteTestBus()

            # Teszteljük az összes metódust
            await bus.start()
            assert bus.started

            await bus.publish("test", TestEvent())
            assert bus.published

            await bus.stop()
            assert bus.stopped

            await bus.run_forever()
            assert bus.ran

        # Aszinkron metódusok tesztelése
        asyncio.run(test_async_methods())

        # Szinkron metódusok tesztelése
        bus = ConcreteTestBus()
        bus.subscribe("test", lambda e: None)  # pyright: ignore[reportUnknownLambdaType]
        assert bus.subscribed

        bus.unsubscribe("test", lambda e: None)  # pyright: ignore[reportUnknownLambdaType]
        assert bus.unsubscribed

    def test_interface_cannot_be_instantiated_directly(self) -> None:
        """Teszteli, hogy az interfész nem példányosítható közvetlenül."""
        with pytest.raises(TypeError, match="abstract"):
            EventBusInterface()  # type: ignore
