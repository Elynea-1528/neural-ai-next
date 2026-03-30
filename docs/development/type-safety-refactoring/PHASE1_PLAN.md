# 🔴 FÁZIS 1: KRITIKUS HIBÁK JAVÍTÁSA

**Időkeret**: 1-2 hét
**Prioritás**: P0 🔴 BLOCKER
**Cél**: 19 VULNERABLE fájl → 0 VULNERABLE

---

## 📊 ÁTTEKINTÉS

**Jelenlegi állapot**:
- 🔴 19 VULNERABLE fájl
- 91 failed teszt
- Bootstrap instabilitás

**Végcél**:
- ✅ 0 VULNERABLE fájl
- ✅ 91 teszt pass
- ✅ Stabil bootstrap

---

## 🎯 MILESTONE 1.1: CORE INFRASTRUCTURE STABILIZÁLÁS (1. hét)

### Fájlok és Hibák

#### 1. [`neural_ai/core/__init__.py`](../../../neural_ai/core/__init__.py) - 7 failed teszt

**Hiba típusok**:
- Import error: Circular dependency
- Type error: ComponentBundle típus nem felismert
- AttributeError: _instances attribútum hiányzik

**Javítási stratégia**:
```python
# ❌ ROSSZ
from neural_ai.core.base import ComponentBundle  # type: ignore

# ✅ JÓ
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from neural_ai.core.base import ComponentBundle

# Runtime import
from typing import cast
bundle = cast("ComponentBundle", get_bundle())
```

**Tesztek**:
- `tests/neural_ai/core/test_core_init.py`
- 7 failed teszt javítása

**QA Parancsok**:
```bash
/home/elynea/miniconda3/envs/neural-ai-next/bin/ruff check neural_ai/core/__init__.py
/home/elynea/miniconda3/envs/neural-ai-next/bin/mypy neural_ai/core/__init__.py
/home/elynea/miniconda3/envs/neural-ai-next/bin/pyright neural_ai/core/__init__.py
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/neural_ai/core/test_core_init.py -vv
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest --cov=neural_ai/core/__init__.py --cov-report=term-missing --cov-branch
# CÉL: 100% Stmt / 100% Brch
```

---

#### 2. [`neural_ai/core/config/factory.py`](../../../neural_ai/core/config/factory.py) - 2 failed teszt

**Hiba típusok**:
- Type error: ConfigManagerInterface nem felismert
- Factory return type mismatch

**Javítási stratégia**:
```python
# ❌ ROSSZ
def create_config() -> Any:  # type: ignore
    return YamlConfigManager()

# ✅ JÓ
from typing import cast
from neural_ai.core.config.interfaces import ConfigManagerInterface

def create_config() -> ConfigManagerInterface:
    return cast(ConfigManagerInterface, YamlConfigManager())
```

**Tesztek**:
- `tests/neural_ai/core/config/test_config_factory.py`
- 2 failed teszt javítása

---

#### 3. [`neural_ai/core/config/implementations/__init__.py`](../../../neural_ai/core/config/implementations/__init__.py) - 1 failed teszt

**Hiba típusok**:
- Import error: Implementáció exportálva (TILOS!)

**Javítási stratégia**:
```python
# ❌ ROSSZ (Implementáció exportálva)
from .yaml_config_manager import YamlConfigManager
__all__ = ['YamlConfigManager']

# ✅ JÓ (ÜRES - ne exportálj implementációt!)
__all__: list[str] = []
```

**Tesztek**:
- `tests/neural_ai/core/config/implementations/test_config_implementations_init.py`
- 1 failed teszt javítása

---

#### 4. [`neural_ai/core/events/factory.py`](../../../neural_ai/core/events/factory.py) - 4 failed teszt

**Hiba típusok**:
- Type error: ZeroMQ socket típus nem felismert
- Factory dependency injection hiba

**Javítási stratégia**:
```python
# ❌ ROSSZ
def create_event_bus(config: Any) -> Any:  # type: ignore
    return ZeroMQBus(config)

# ✅ JÓ
from typing import cast
from neural_ai.core.events.interfaces import EventBusInterface

def create_event_bus(config: dict[str, Any]) -> EventBusInterface:
    return cast(EventBusInterface, ZeroMQBus(config))
```

**Tesztek**:
- `tests/neural_ai/core/events/test_events_factory.py`
- 4 failed teszt javítása

---

#### 5. [`neural_ai/core/logger/implementations/default_logger.py`](../../../neural_ai/core/logger/implementations/default_logger.py) - 8 failed teszt

**Hiba típusok**:
- Type error: Structlog típusok nem felismertek
- Logger method signature mismatch

**Javítási stratégia**:
```python
# ❌ ROSSZ
def info(self, msg: str, **kwargs: Any) -> None:  # type: ignore
    self._logger.info(msg, **kwargs)

# ✅ JÓ
from typing import Any
def info(self, msg: str, **kwargs: Any) -> None:
    # Structlog extra paraméterek
    self._logger.info(msg, **kwargs)  # type: ignore[call-arg]
```

**Tesztek**:
- `tests/neural_ai/core/logger/implementations/test_default_logger.py`
- 8 failed teszt javítása

---

### Függőségi Gráf

```
1. neural_ai/core/__init__.py (ELSŐ - bootstrap)
   ↓
2. neural_ai/core/config/implementations/__init__.py (exportálás javítás)
   ↓
3. neural_ai/core/config/factory.py (config factory)
   ↓
4. neural_ai/core/logger/implementations/default_logger.py (logger)
   ↓
5. neural_ai/core/events/factory.py (events - utolsó)
```

**Kritikus**: A fenti sorrendben kell javítani!

---

### Deliverable

- ✅ 5 fájl javítva
- ✅ 22 teszt pass
- ✅ <5 `# type: ignore` összesen
- ✅ Bootstrap stabil

---

## 🎯 MILESTONE 1.2: DATABASE & DOMAIN STABILIZÁLÁS (2. hét)

### Fájlok és Hibák

#### 1. [`neural_ai/core/db/implementations/sqlalchemy_session.py`](../../../neural_ai/core/db/implementations/sqlalchemy_session.py) - 16 failed teszt

**Hiba típusok**:
- Type error: AsyncEngine típus nem felismert
- AsyncSession context manager típus hiba
- SQLAlchemy 2.0 async típusok

**Javítási stratégia**:
```python
# ❌ ROSSZ
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine(url)  # type: ignore

# ✅ JÓ
from typing import cast
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

engine = cast(AsyncEngine, create_async_engine(url))
```

**Async Session**:
```python
# ❌ ROSSZ
async with self._session_maker() as session:  # type: ignore
    ...

# ✅ JÓ
from sqlalchemy.ext.asyncio import AsyncSession

async with self._session_maker() as session:
    session = cast(AsyncSession, session)
    ...
```

**Tesztek**:
- `tests/neural_ai/core/db/implementations/test_sqlalchemy_session.py`
- 16 failed teszt javítása

---

#### 2. [`neural_ai/processors/dimensions/d01_price/factory.py`](../../../neural_ai/processors/dimensions/d01_price/factory.py) - 1 failed teszt

**Hiba típusok**:
- Type error: Processor interface típus hiba

**Javítási stratégia**:
```python
# ❌ ROSSZ
def create_price_processor() -> Any:  # type: ignore
    return PriceProcessor()

# ✅ JÓ
from typing import cast
from neural_ai.processors.interfaces import ProcessorInterface

def create_price_processor() -> ProcessorInterface:
    return cast(ProcessorInterface, PriceProcessor())
```

---

#### 3. [`neural_ai/processors/dimensions/d02_support/implementations/support_processor.py`](../../../neural_ai/processors/dimensions/d02_support/implementations/support_processor.py) - 16 failed teszt

**Hiba típusok**:
- Type error: Polars DataFrame típus nem felismert
- Config dict típus hiba

**Javítási stratégia**:
```python
# ❌ ROSSZ
def process(self, df: Any) -> Any:  # type: ignore
    return df.with_columns(...)

# ✅ JÓ
import polars as pl

def process(self, df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns(...)
```

**Config típus**:
```python
# ❌ ROSSZ
def __init__(self, config: Any):  # type: ignore
    self.config = config

# ✅ JÓ
from typing import Any

def __init__(self, config: dict[str, Any]):
    self.config = config
```

---

#### 4. [`neural_ai/ui/factory.py`](../../../neural_ai/ui/factory.py) - 2 failed teszt

**Hiba típusok**:
- Type error: CoreBridge típus hiba
- Streamlit session_state típus

**Javítási stratégia**:
```python
# ❌ ROSSZ
def create_ui(bridge: Any) -> Any:  # type: ignore
    return StreamlitApp(bridge)

# ✅ JÓ
from typing import cast
from neural_ai.ui.interfaces import CoreBridgeInterface

def create_ui(bridge: CoreBridgeInterface) -> Any:
    # Streamlit típus problémák dokumentálva
    return StreamlitApp(bridge)  # type: ignore[arg-type]
```

---

### Függőségi Gráf

```
1. neural_ai/core/db/implementations/sqlalchemy_session.py (ELSŐ - adatbázis)
   ↓
2. neural_ai/processors/dimensions/d01_price/factory.py (processor factory)
   ↓
3. neural_ai/processors/dimensions/d02_support/implementations/support_processor.py (processor impl)
   ↓
4. neural_ai/ui/factory.py (UI - utolsó)
```

---

### Deliverable

- ✅ 4 fájl javítva
- ✅ 35 teszt pass
- ✅ <8 `# type: ignore` összesen
- ✅ Database & Domain stabil

---

## 🎯 MILESTONE 1.3: TEST INFRASTRUCTURE JAVÍTÁS (2. hét vége)

### Fájlok és Hibák

**10 teszt fájl javítása** - MagicMock spec használat

#### Általános Javítási Stratégia

```python
# ❌ ROSSZ
mock_service = MagicMock()  # type: ignore
mock_service.method.return_value = "result"

# ✅ JÓ
from neural_ai.core.logger.interfaces import LoggerInterface

mock_service = MagicMock(spec=LoggerInterface)
mock_service.method.return_value = "result"
```

#### Patch használat

```python
# ❌ ROSSZ
storage.backend.read = MagicMock(return_value=df)  # type: ignore[method-assign]

# ✅ JÓ
from unittest.mock import patch

with patch.object(storage.backend, 'read', return_value=df):
    # teszt kód
```

---

### Fájlok listája

1. `tests/neural_ai/core/test_core_init.py` - 7 failed
2. `tests/neural_ai/core/config/test_config_factory.py` - 2 failed
3. `tests/neural_ai/core/config/implementations/test_config_implementations_init.py` - 1 failed
4. `tests/neural_ai/core/db/implementations/test_sqlalchemy_session.py` - 16 failed
5. `tests/neural_ai/core/events/test_events_factory.py` - 4 failed
6. `tests/neural_ai/core/logger/implementations/test_default_logger.py` - 8 failed
7. `tests/neural_ai/processors/dimensions/d01_price/test_d01_factory.py` - 1 failed
8. `tests/neural_ai/processors/dimensions/d02_support/implementations/test_support_processor.py` - 16 failed
9. `tests/neural_ai/ui/test_ui_factory.py` - 2 failed
10. `tests/scripts/test_validation_end_to_end.py` - 1 failed

---

### Deliverable

- ✅ 10 teszt fájl javítva
- ✅ 91 teszt pass
- ✅ MagicMock spec használat
- ✅ Teszt infrastruktúra stabil

---

## 📋 FÁZIS 1 ÖSSZESÍTÉS

### Eredmények

**Előtte**:
- 🔴 19 VULNERABLE fájl
- 91 failed teszt
- Bootstrap instabil

**Utána**:
- ✅ 0 VULNERABLE fájl
- ✅ 91 teszt pass
- ✅ Bootstrap stabil
- ✅ <20 `# type: ignore` összesen

### Következő lépés

**Delegálás**: Fázis 2 - Infrastructure Layer Tisztítás
**Mód**: code-refactor
**Időkeret**: 3 hét

---

**Verzió**: 1.0
**Utolsó frissítés**: 2026-03-30
