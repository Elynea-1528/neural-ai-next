# neural_ai/core/events/interfaces/__init__.py

Interfészek az events modulhoz.

Ez a csomag tartalmazza az EventBus interfészt és az esemény modelleket.

## Importok

```python
from neural_ai.core.events.interfaces.event_bus_interface import EventBusConfig
from neural_ai.core.events.interfaces.event_bus_interface import EventBusInterface
from neural_ai.core.events.interfaces.event_models import EventType
from neural_ai.core.events.interfaces.event_models import MarketDataEvent
from neural_ai.core.events.interfaces.event_models import OrderEvent
from neural_ai.core.events.interfaces.event_models import PositionEvent
from neural_ai.core.events.interfaces.event_models import SignalEvent
from neural_ai.core.events.interfaces.event_models import SystemLogEvent
from neural_ai.core.events.interfaces.event_models import TradeEvent
```

## Konstansok

- **`__all__`**
: `['EventBusInterface', 'EventBusConfig', 'EventType', 'MarketDataEvent', 'TradeEvent', 'SignalEvent', 'SystemLogEvent', 'OrderEvent', 'PositionEvent']`


---

**Forrásfájl:** [`neural_ai/core/events/interfaces/__init__.py`](../../neural_ai/core/events/interfaces/__init__.py)
