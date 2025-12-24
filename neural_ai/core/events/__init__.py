"""EventBus modul a Neural AI Next rendszerhez.

Ez a csomag biztosítja az eseményvezérelt architektúra magját,
lehetővé téve a komponensek közötti laza csatolást.

Komponensek:
- events.py: Esemény modellek (Pydantic BaseModel-ek)
- bus.py: EventBus implementáció (ZeroMQ PUB/SUB)
"""

from neural_ai.core.events.bus import EventBus, EventBusConfig
from neural_ai.core.events.events import (
    EventType,
    MarketDataEvent,
    OrderEvent,
    PositionEvent,
    SignalEvent,
    SystemLogEvent,
    TradeEvent,
)

__all__ = [
    # Esemény típusok
    "EventType",
    # Esemény modellek
    "MarketDataEvent",
    "TradeEvent",
    "SignalEvent",
    "SystemLogEvent",
    "OrderEvent",
    "PositionEvent",
    # EventBus
    "EventBus",
    "EventBusConfig",
]
