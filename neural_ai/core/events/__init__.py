"""EventBus modul a Neural AI Next rendszerhez.

Ez a csomag biztosítja az eseményvezérelt architektúra magját,
lehetővé téve a komponensek közötti laza csatolást.

Komponensek:
- interfaces/: Esemény modellek (Pydantic BaseModel-ek) és interfészek
- implementations/: EventBus implementációk (ZeroMQ)
- factory.py: EventBus factory a példányosításhoz

DDD Szabály:
    Csak Interface + Factory + Exceptions + Event Models exportáltak.
    Az implementációk (EventBus) NEM exportáltak - a Factory hozza létre őket.
"""

from neural_ai.core.events.exceptions import (
    EventBusError,
    PublishError,
    SubscriberError,
)
from neural_ai.core.events.factory import EventBusFactory
from neural_ai.core.events.interfaces import EventBusInterface
from neural_ai.core.events.interfaces.event_models import (
    EventType,
    MarketDataEvent,
    OrderEvent,
    PositionEvent,
    SignalEvent,
    SystemLogEvent,
    TradeEvent,
)

__all__ = [
    # Interface
    "EventBusInterface",
    # Factory
    "EventBusFactory",
    # Exceptions
    "EventBusError",
    "PublishError",
    "SubscriberError",
    # Esemény típusok
    "EventType",
    # Esemény modellek
    "MarketDataEvent",
    "TradeEvent",
    "SignalEvent",
    "SystemLogEvent",
    "OrderEvent",
    "PositionEvent",
]
