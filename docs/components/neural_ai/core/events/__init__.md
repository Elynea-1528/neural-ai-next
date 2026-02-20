# neural_ai/core/events/__init__.py

EventBus modul a Neural AI Next rendszerhez.

Ez a csomag biztosítja az eseményvezérelt architektúra magját,
lehetővé téve a komponensek közötti laza csatolást.

Komponensek:
- interfaces/: Esemény modellek (Pydantic BaseModel-ek) és interfészek
- implementations/: EventBus implementációk (ZeroMQ)
- factory.py: EventBus factory a példányosításhoz

## Importok

```python
from neural_ai.core.events.factory import EventBusFactory
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
: `['EventBusFactory', 'EventType', 'MarketDataEvent', 'TradeEvent', 'SignalEvent', 'SystemLogEvent', 'OrderEvent', 'PositionEvent']`


---

**Forrásfájl:** [`neural_ai/core/events/__init__.py`](../../neural_ai/core/events/__init__.py)
