"""EventBus-specifikus kivételek.

Ez a modul tartalmazza az összes EventBus-műveletekhez kapcsolódó kivételeket.
"""

from neural_ai.core.base.exceptions import NeuralAIException


class EventBusError(NeuralAIException):
    """Általános EventBus hiba."""

    def __init__(self, message: str, details: str | None = None) -> None:
        """Inicializálja az EventBusError kivételt.

        Args:
            message: A hibaüzenet.
            details: Opcionális részletes leírás a hibáról.
        """
        super().__init__(message)
        self.details = details


class PublishError(EventBusError):
    """Esemény közzététel hiba."""

    def __init__(self, message: str, event_type: str | None = None) -> None:
        """Inicializálja a PublishError kivételt.

        Args:
            message: A hibaüzenet.
            event_type: Az esemény típusa, amelynek közzététele sikertelen volt.
        """
        super().__init__(message)
        self.event_type = event_type


class SubscriberError(EventBusError):
    """Feliratkozási hiba."""

    def __init__(self, message: str, subscriber_id: str | None = None) -> None:
        """Inicializálja a SubscriberError kivételt.

        Args:
            message: A hibaüzenet.
            subscriber_id: A feliratkozó azonosítója, ahol a hiba történt.
        """
        super().__init__(message)
        self.subscriber_id = subscriber_id
