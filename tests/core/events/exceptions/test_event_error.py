"""EventBus kivételek tesztek."""
from neural_ai.core.base.exceptions import NeuralAIException
from neural_ai.core.events.exceptions.event_error import (
    EventBusError,
    PublishError,
    SubscriberError,
)


class TestEventBusError:
    """EventBusError osztály tesztei."""

    def test_event_bus_error_creation(self) -> None:
        """EventBusError létrehozásának tesztelése."""
        error = EventBusError("Hibaüzenet")
        assert str(error) == "Hibaüzenet"
        assert error.details is None

    def test_event_bus_error_with_details(self) -> None:
        """EventBusError létrehozása részletekkel."""
        error = EventBusError("Hibaüzenet", details="Részletes leírás")
        assert str(error) == "Hibaüzenet"
        assert error.details == "Részletes leírás"

    def test_event_bus_error_is_neural_ai_exception(self) -> None:
        """EventBusError NeuralAIException-ből származik."""
        error = EventBusError("Hibaüzenet")
        assert isinstance(error, NeuralAIException)


class TestPublishError:
    """PublishError osztály tesztei."""

    def test_publish_error_creation(self) -> None:
        """PublishError létrehozásának tesztelése."""
        error = PublishError("Közzététel hiba")
        assert str(error) == "Közzététel hiba"
        assert error.event_type is None

    def test_publish_error_with_event_type(self) -> None:
        """PublishError létrehozása event type-nal."""
        error = PublishError("Közzététel hiba", event_type="market_data")
        assert str(error) == "Közzététel hiba"
        assert error.event_type == "market_data"

    def test_publish_error_inheritance(self) -> None:
        """PublishError EventBusError-ből származik."""
        error = PublishError("Közzététel hiba")
        assert isinstance(error, EventBusError)


class TestSubscriberError:
    """SubscriberError osztály tesztei."""

    def test_subscriber_error_creation(self) -> None:
        """SubscriberError létrehozásának tesztelése (47-48. sorok)."""
        error = SubscriberError("Feliratkozás hiba")
        assert str(error) == "Feliratkozás hiba"
        assert error.subscriber_id is None

    def test_subscriber_error_with_subscriber_id(self) -> None:
        """SubscriberError létrehozása subscriber ID-vel (47-48. sorok)."""
        error = SubscriberError("Feliratkozás hiba", subscriber_id="sub_12345")
        assert str(error) == "Feliratkozás hiba"
        assert error.subscriber_id == "sub_12345"

    def test_subscriber_error_inheritance(self) -> None:
        """SubscriberError EventBusError-ből származik."""
        error = SubscriberError("Feliratkozás hiba")
        assert isinstance(error, EventBusError)
