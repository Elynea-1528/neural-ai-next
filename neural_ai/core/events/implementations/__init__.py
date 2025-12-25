"""Implementációk az events modulhoz.

Ez a csomag tartalmazza az EventBus különböző implementációit.
"""

from neural_ai.core.events.implementations.zeromq_bus import EventBus, EventBusConfig

__all__ = [
    "EventBus",
    "EventBusConfig",
]
