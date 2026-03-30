# 🟡 FÁZIS 4: INPUT & PRESENTATION LAYER

**Időkeret**: 8-9. hét (2 hét)
**Prioritás**: P2 🟡 HASZNOS
**Cél**: Adatforrások és UI típusbiztonság javítása

---

## 📊 ÁTTEKINTÉS

**Scope**: 42+ fájl (collectors + ui)
**Jelenlegi**: ~50+ `# type: ignore` használat
**Cél**: <20 `# type: ignore` (dokumentált)

---

## 🎯 MILESTONE 4.1: COLLECTORS (8. hét)

### Fájlok
- [`neural_ai/collectors/jforex/`](../../../neural_ai/collectors/jforex/) - 8 fájl
- [`neural_ai/collectors/mt5/`](../../../neural_ai/collectors/mt5/) - 4 fájl

### Fókusz Területek

#### Bi5 Decoder Típusok
**Stub fájl szükséges**: `neural_ai/collectors/jforex/implementations/bi5_decoder.pyi`

```python
# bi5_decoder.pyi
from typing import Any
import polars as pl

class Bi5Decoder:
    def decode(self, data: bytes) -> pl.DataFrame: ...
    def _parse_header(self, data: bytes) -> dict[str, Any]: ...
```

#### JForex Bridge Java Interop
```python
# ❌ ROSSZ
from py4j.java_gateway import JavaGateway
gateway = JavaGateway()  # type: ignore
strategy = gateway.entry_point.getStrategy()  # type: ignore

# ✅ JÓ
from typing import Any, cast
from py4j.java_gateway import JavaGateway, JavaObject

gateway = JavaGateway()
strategy = cast(JavaObject, gateway.entry_point.getStrategy())
```

#### MT5 API Típusok
```python
# ❌ ROSSZ
import MetaTrader5 as mt5
ticks = mt5.copy_ticks_range(...)  # type: ignore

# ✅ JÓ
import MetaTrader5 as mt5
import numpy as np
from typing import Any

ticks: np.ndarray[Any, Any] = mt5.copy_ticks_range(...)
```

### QA Gate (MINDEN FÁJLNÁL)

```bash
# 1-3. Linting + Type Check
/home/elynea/miniconda3/envs/neural-ai-next/bin/ruff check neural_ai/collectors/jforex/implementations/bi5_downloader.py
/home/elynea/miniconda3/envs/neural-ai-next/bin/mypy neural_ai/collectors/jforex/implementations/bi5_downloader.py
/home/elynea/miniconda3/envs/neural-ai-next/bin/pyright neural_ai/collectors/jforex/implementations/bi5_downloader.py

# 4-5. Tests + Coverage (CÉL: 100%/100%)
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/neural_ai/collectors/jforex/test_bi5_downloader.py -vv
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest \
  --cov=neural_ai/collectors/jforex/implementations/bi5_downloader.py \
  --cov-report=term-missing \
  --cov-branch

# 6-7. Commit + TASK_TREE
git add neural_ai/collectors/jforex/implementations/bi5_downloader.py tests/neural_ai/collectors/jforex/test_bi5_downloader.py
git commit -m "refactor(type-safety): bi5 downloader type ignore javítás"
python scripts/generate.py
git add docs/development/TASK_TREE.md
git commit -m "docs(task-tree): bi5 downloader státusz frissítés"
```

### Deliverable
- ✅ 12 fájl auditálva
- ✅ <5 `# type: ignore`
- ✅ **100% Stmt / 100% Brch coverage** minden fájlnál
- ✅ 0 Ruff/Mypy/Pyright hiba
- ✅ 1 stub fájl (bi5_decoder.pyi)

---

## 🎯 MILESTONE 4.2: UI LAYER (9. hét)

### Fájlok
- [`neural_ai/ui/`](../../../neural_ai/ui/) - 30 fájl

### Fókusz Területek

#### Streamlit Típus Problémák (DOKUMENTÁLT IGNORE)
```python
# ❌ ROSSZ
import streamlit as st
st.session_state.key = value  # type: ignore

# ✅ JÓ (Dokumentált)
import streamlit as st

# Streamlit session_state nem típusos - third-party library limitation
st.session_state.key = value  # type: ignore[attr-defined]
```

#### Session State TypedDict
```python
# ❌ ROSSZ
def get_state() -> Any:  # type: ignore
    return st.session_state

# ✅ JÓ
from typing import TypedDict, Any

class SessionState(TypedDict, total=False):
    user_id: str
    data: Any
    config: dict[str, Any]

def get_state() -> SessionState:
    return st.session_state  # type: ignore[return-value]  # Streamlit limitation
```

#### Widget Típus Annotációk
```python
# ❌ ROSSZ
class BaseWidget:
    def render(self):  # type: ignore
        ...

# ✅ JÓ
from typing import Protocol

class WidgetProtocol(Protocol):
    def render(self) -> None: ...

class BaseWidget:
    def render(self) -> None:
        ...
```

### QA Gate (MINDEN FÁJLNÁL)

```bash
# 1-3. Linting + Type Check
/home/elynea/miniconda3/envs/neural-ai-next/bin/ruff check neural_ai/ui/services/data_service.py
/home/elynea/miniconda3/envs/neural-ai-next/bin/mypy neural_ai/ui/services/data_service.py
/home/elynea/miniconda3/envs/neural-ai-next/bin/pyright neural_ai/ui/services/data_service.py

# 4-5. Tests + Coverage (CÉL: 100%/100%)
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/neural_ai/ui/services/test_data_service.py -vv
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest \
  --cov=neural_ai/ui/services/data_service.py \
  --cov-report=term-missing \
  --cov-branch

# 6-7. Commit + TASK_TREE
git add neural_ai/ui/services/data_service.py tests/neural_ai/ui/services/test_data_service.py
git commit -m "refactor(type-safety): data service type ignore javítás"
python scripts/generate.py
git add docs/development/TASK_TREE.md
git commit -m "docs(task-tree): data service státusz frissítés"
```

### Deliverable
- ✅ 30 fájl auditálva
- ✅ <15 `# type: ignore` (dokumentált - Streamlit limitációk)
- ✅ **100% Stmt / 100% Brch coverage** minden fájlnál
- ✅ 0 Ruff/Mypy/Pyright hiba
- ✅ Streamlit stub fájl (opcionális)

---

## 📋 FÁZIS 4 ÖSSZESÍTÉS

### Eredmények

**Előtte**:
- ~50+ `# type: ignore` az input/ui rétegben
- Bi5 decoder típus hiányok
- Streamlit típus problémák

**Utána**:
- ✅ <20 `# type: ignore` (dokumentált)
- ✅ 42+ fájl tiszta
- ✅ **100% Stmt / 100% Brch coverage** minden fájlnál
- ✅ 0 Ruff/Mypy/Pyright hiba
- ✅ Input & UI layer típusbiztos

### Következő lépés

**Delegálás**: Fázis 5 - Test & Script Tisztítás
**Mód**: test-unit, code-refactor
**Időkeret**: 1 hét

---

**Verzió**: 1.0
**Utolsó frissítés**: 2026-03-30
