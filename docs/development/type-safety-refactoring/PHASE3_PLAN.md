# 🟠 FÁZIS 3: DOMAIN & DATA LAYER

**Időkeret**: 6-7. hét (2 hét)
**Prioritás**: P1 🟠 FONTOS
**Cél**: Domain logika és adatkezelés típusbiztonság növelése

---

## 📊 ÁTTEKINTÉS

**Scope**: 45+ fájl (processors + data)
**Jelenlegi**: ~60+ `# type: ignore` használat
**Cél**: <18 `# type: ignore` (dokumentált)

---

## 🎯 MILESTONE 3.1: PROCESSORS (6. hét)

### Fájlok
- [`neural_ai/processors/`](../../../neural_ai/processors/) - 25 fájl

### Fókusz Területek

#### Polars DataFrame Típusok
```python
# ❌ ROSSZ
def process(self, df: Any) -> Any:  # type: ignore
    return df.with_columns(...)

# ✅ JÓ
import polars as pl

def process(self, df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns(...)
```

#### Dimension Processor Típus Annotációk
```python
# ❌ ROSSZ
class D01PriceProcessor:
    def calculate(self, data):  # type: ignore
        ...

# ✅ JÓ
from typing import Protocol
import polars as pl

class ProcessorProtocol(Protocol):
    def calculate(self, data: pl.DataFrame) -> pl.DataFrame: ...

class D01PriceProcessor:
    def calculate(self, data: pl.DataFrame) -> pl.DataFrame:
        ...
```

#### Pipeline Orchestrator
```python
# ❌ ROSSZ
def run_pipeline(processors: list) -> Any:  # type: ignore
    ...

# ✅ JÓ
from typing import Sequence
from neural_ai.processors.interfaces import ProcessorInterface

def run_pipeline(processors: Sequence[ProcessorInterface]) -> pl.DataFrame:
    ...
```

### QA Gate (MINDEN FÁJLNÁL)

```bash
# 1. Linting
/home/elynea/miniconda3/envs/neural-ai-next/bin/ruff check neural_ai/processors/dimensions/d01_price/processor.py

# 2. Type Check (Mypy)
/home/elynea/miniconda3/envs/neural-ai-next/bin/mypy neural_ai/processors/dimensions/d01_price/processor.py

# 3. Type Check (Pyright)
/home/elynea/miniconda3/envs/neural-ai-next/bin/pyright neural_ai/processors/dimensions/d01_price/processor.py

# 4. Tests
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/neural_ai/processors/dimensions/d01_price/test_processor.py -vv

# 5. Coverage (CÉL: 100% Stmt / 100% Brch)
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest \
  --cov=neural_ai/processors/dimensions/d01_price/processor.py \
  --cov-report=term-missing \
  --cov-branch

# 6. HA MINDEN PASS (0 hiba, 100%/100%) → Commit
git add neural_ai/processors/dimensions/d01_price/processor.py tests/neural_ai/processors/dimensions/d01_price/test_processor.py
git commit -m "refactor(type-safety): d01 processor type ignore javítás"

# 7. TASK_TREE frissítés
python scripts/generate.py
git add docs/development/TASK_TREE.md
git commit -m "docs(task-tree): d01 processor státusz frissítés 🟡→✅"
```

### Deliverable
- ✅ 25 fájl auditálva
- ✅ <10 `# type: ignore`
- ✅ **100% Stmt / 100% Brch coverage** minden fájlnál
- ✅ 0 Ruff/Mypy/Pyright hiba
- ✅ Polars Protocol definíció (opcionális)

---

## 🎯 MILESTONE 3.2: DATA STORAGE & INGESTION (7. hét)

### Fájlok
- [`neural_ai/data/storage/`](../../../neural_ai/data/storage/) - 12 fájl
- [`neural_ai/data/ingestion/`](../../../neural_ai/data/ingestion/) - 8 fájl

### Fókusz Területek

#### Parquet I/O Típusok
```python
# ❌ ROSSZ
def read_parquet(path: str) -> Any:  # type: ignore
    return pl.read_parquet(path)

# ✅ JÓ
import polars as pl

def read_parquet(path: str) -> pl.DataFrame:
    return pl.read_parquet(path)
```

#### FastParquet Backend
```python
# ❌ ROSSZ
from fastparquet import ParquetFile
pf = ParquetFile(path)  # type: ignore
df = pf.to_pandas()  # type: ignore

# ✅ JÓ
from typing import cast
import pandas as pd
from fastparquet import ParquetFile

pf = ParquetFile(path)
df = cast(pd.DataFrame, pf.to_pandas())
```

#### MarketDataPersister Buffer
```python
# ❌ ROSSZ
class MarketDataPersister:
    def __init__(self):
        self._buffer = []  # type: ignore

# ✅ JÓ
from typing import Any
import polars as pl

class MarketDataPersister:
    def __init__(self):
        self._buffer: list[dict[str, Any]] = []
    
    def flush(self) -> pl.DataFrame:
        return pl.DataFrame(self._buffer)
```

### QA Gate (MINDEN FÁJLNÁL)

```bash
# 1-3. Linting + Type Check
/home/elynea/miniconda3/envs/neural-ai-next/bin/ruff check neural_ai/data/storage/implementations/parquet_storage.py
/home/elynea/miniconda3/envs/neural-ai-next/bin/mypy neural_ai/data/storage/implementations/parquet_storage.py
/home/elynea/miniconda3/envs/neural-ai-next/bin/pyright neural_ai/data/storage/implementations/parquet_storage.py

# 4-5. Tests + Coverage (100%/100%)
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/neural_ai/data/storage/implementations/test_parquet_storage.py -vv
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest \
  --cov=neural_ai/data/storage/implementations/parquet_storage.py \
  --cov-report=term-missing \
  --cov-branch

# 6-7. Commit + TASK_TREE
git add neural_ai/data/storage/implementations/parquet_storage.py tests/neural_ai/data/storage/implementations/test_parquet_storage.py
git commit -m "refactor(type-safety): parquet storage type ignore javítás"
python scripts/generate.py
git add docs/development/TASK_TREE.md
git commit -m "docs(task-tree): parquet storage státusz frissítés"
```

### Deliverable
- ✅ 20 fájl auditálva
- ✅ <8 `# type: ignore`
- ✅ **100% Stmt / 100% Brch coverage** minden fájlnál
- ✅ 0 Ruff/Mypy/Pyright hiba
- ✅ Parquet stub fájl (opcionális)

---

## 📋 FÁZIS 3 ÖSSZESÍTÉS

### Eredmények

**Előtte**:
- ~60+ `# type: ignore` a domain/data rétegben
- Polars típus problémák
- Parquet I/O típus hiányok

**Utána**:
- ✅ <18 `# type: ignore` (dokumentált)
- ✅ 45+ fájl tiszta
- ✅ **100% Stmt / 100% Brch coverage** minden fájlnál
- ✅ 0 Ruff/Mypy/Pyright hiba
- ✅ Domain & Data layer típusbiztos

### Következő lépés

**Delegálás**: Fázis 4 - Input & Presentation Layer
**Mód**: code-refactor
**Időkeret**: 2 hét

---

**Verzió**: 1.0
**Utolsó frissítés**: 2026-03-30
