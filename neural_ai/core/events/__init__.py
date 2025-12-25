"""EventBus modul a Neural AI Next rendszerhez.

Ez a csomag biztosítja az eseményvezérelt architektúra magját,
lehetővé téve a komponensek közötti laza csatolást.

Komponensek:
- interfaces/: Esemény modellek (Pydantic BaseModel-ek) és interfészek
- implementations/: EventBus implementációk (ZeroMQ)
- factory.py: EventBus factory a példányosításhoz
"""

from neural_ai.core.events.factory import EventBusFactory
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
    # Factory
    "EventBusFactory",
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
