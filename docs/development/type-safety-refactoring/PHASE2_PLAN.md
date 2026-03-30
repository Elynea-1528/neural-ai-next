# 🟠 FÁZIS 2: INFRASTRUCTURE LAYER TISZTÍTÁS

**Időkeret**: 3-5. hét (3 hét)
**Prioritás**: P1 🟠 FONTOS
**Cél**: [`neural_ai/core/`](../../../neural_ai/core/) könyvtár `# type: ignore` minimalizálása

---

## 📊 ÁTTEKINTÉS

**Scope**: 70+ fájl a core infrastructure rétegben
**Jelenlegi**: ~100+ `# type: ignore` használat
**Cél**: <35 `# type: ignore` (dokumentált)

---

## 🎯 MILESTONE 2.1: CORE BASE & CONFIG (3. hét)

### Fájlok
- [`neural_ai/core/base/`](../../../neural_ai/core/base/) - 12 fájl
- [`neural_ai/core/config/`](../../../neural_ai/core/config/) - 10 fájl

### Fókusz Területek

#### DI Container Típus Problémák
```python
# ❌ ROSSZ
container.register("service", service)  # type: ignore

# ✅ JÓ
from typing import cast
container.register("service", cast(ServiceInterface, service))
```

#### Singleton Metaclass
**Stub fájl szükséges**: [`neural_ai/core/base/implementations/singleton.pyi`](../../../neural_ai/core/base/implementations/singleton.pyi)

```python
# singleton.pyi
from typing import TypeVar, Type, Any

T = TypeVar('T')

class SingletonMeta(type):
    _instances: dict[Type[T], T]
    _instance: T
    def __call__(cls: Type[T], *args: Any, **kwargs: Any) -> T: ...
```

#### Pydantic Config Validáció
```python
# ❌ ROSSZ
config = self.config.get("key")  # type: ignore

# ✅ JÓ
from pydantic import BaseModel

class ConfigModel(BaseModel):
    key: str

config = ConfigModel(**self.config.get("section"))
```

### Deliverable
- ✅ 22 fájl auditálva
- ✅ <10 `# type: ignore`
- ✅ 1 stub fájl ([`singleton.pyi`](../../../neural_ai/core/base/implementations/singleton.pyi))

---

## 🎯 MILESTONE 2.2: LOGGER & EVENTS (4. hét)

### Fájlok
- [`neural_ai/core/logger/`](../../../neural_ai/core/logger/) - 11 fájl
- [`neural_ai/core/events/`](../../../neural_ai/core/events/) - 7 fájl

### Fókusz Területek

#### ZeroMQ Típus Problémák
**Stub fájl szükséges**: [`neural_ai/core/events/implementations/zeromq_bus.pyi`](../../../neural_ai/core/events/implementations/zeromq_bus.pyi)

```python
# zeromq_bus.pyi
from typing import Any
import zmq

class ZeroMQBus:
    _context: zmq.Context[Any]
    _pub_socket: zmq.Socket[Any]
    _sub_socket: zmq.Socket[Any]
    
    def publish(self, topic: str, data: dict[str, Any]) -> None: ...
    def subscribe(self, topic: str) -> None: ...
```

#### Structlog Típusok
```python
# ❌ ROSSZ
logger.info("msg", extra=data)  # type: ignore

# ✅ JÓ
from typing import Any
logger.info("msg", **data)  # type: ignore[call-arg]  # Structlog extra params
```

### Deliverable
- ✅ 18 fájl auditálva
- ✅ <8 `# type: ignore`
- ✅ 1 stub fájl ([`zeromq_bus.pyi`](../../../neural_ai/core/events/implementations/zeromq_bus.pyi))

---

## 🎯 MILESTONE 2.3: DB & SYSTEM & UTILS (5. hét)

### Fájlok
- [`neural_ai/core/db/`](../../../neural_ai/core/db/) - 13 fájl
- [`neural_ai/core/system/`](../../../neural_ai/core/system/) - 9 fájl
- [`neural_ai/core/utils/`](../../../neural_ai/core/utils/) - 10 fájl

### Fókusz Területek

#### SQLAlchemy Async Típusok
```python
# ❌ ROSSZ
from sqlalchemy.ext.asyncio import create_async_engine
engine = create_async_engine(url)  # type: ignore

# ✅ JÓ
from typing import cast
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

engine = cast(AsyncEngine, create_async_engine(url))
```

#### AsyncSession Context Manager
```python
# ❌ ROSSZ
async with self._session_maker() as session:  # type: ignore
    result = await session.execute(query)

# ✅ JÓ
from sqlalchemy.ext.asyncio import AsyncSession

async with self._session_maker() as session:
    session = cast(AsyncSession, session)
    result = await session.execute(query)
```

#### HardwareInfo Platform Típusok
```python
# ❌ ROSSZ
import platform
cpu_info = platform.processor()  # type: ignore

# ✅ JÓ
import platform
cpu_info: str = platform.processor()  # Platform specifikus típus
```

### Deliverable
- ✅ 32 fájl auditálva
- ✅ <15 `# type: ignore`

---

## 📋 FÁZIS 2 ÖSSZESÍTÉS

### Eredmények

**Előtte**:
- ~100+ `# type: ignore` a core rétegben
- Stub fájlok hiánya
- Típus inferencia problémák

**Utána**:
- ✅ <35 `# type: ignore` (dokumentált)
- ✅ 2 stub fájl létrehozva
- ✅ 70+ fájl tiszta
- ✅ Core infrastructure típusbiztos

### Következő lépés

**Delegálás**: Fázis 3 - Domain & Data Layer
**Mód**: code-refactor
**Időkeret**: 2 hét

---

**Verzió**: 1.0
**Utolsó frissítés**: 2026-03-30
