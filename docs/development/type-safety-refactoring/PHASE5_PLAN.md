# 🟡 FÁZIS 5: TEST & SCRIPT TISZTÍTÁS

**Időkeret**: 10. hét (1 hét)
**Prioritás**: P2 🟡 HASZNOS
**Cél**: Teszt és script fájlok típusbiztonság javítása

---

## 📊 ÁTTEKINTÉS

**Scope**: 168+ fájl (tests + scripts)
**Jelenlegi**: ~80+ `# type: ignore` használat
**Cél**: <40 `# type: ignore` (dokumentált)

---

## 🎯 MILESTONE 5.1: TEST FILES (10. hét eleje)

### Fájlok
- [`tests/`](../../../tests/) - 150+ fájl

### Fókusz Területek

#### MagicMock Spec Használat
```python
# ❌ ROSSZ
from unittest.mock import MagicMock

mock_service = MagicMock()  # type: ignore
mock_service.method.return_value = "result"

# ✅ JÓ
from unittest.mock import MagicMock
from neural_ai.core.logger.interfaces import LoggerInterface

mock_service = MagicMock(spec=LoggerInterface)
mock_service.method.return_value = "result"
# Nincs type: ignore!
```

#### Patch Context Manager
```python
# ❌ ROSSZ
storage.backend.read = MagicMock(return_value=df)  # type: ignore[method-assign]

# ✅ JÓ
from unittest.mock import patch

with patch.object(storage.backend, 'read', return_value=df):
    # teszt kód
    result = storage.load_data()
# Nincs type: ignore!
```

#### Fixture Típus Annotációk
```python
# ❌ ROSSZ
@pytest.fixture
def mock_config():  # type: ignore
    return {"key": "value"}

# ✅ JÓ
from typing import Any
import pytest

@pytest.fixture
def mock_config() -> dict[str, Any]:
    return {"key": "value"}
```

#### Parametrize Típusok
```python
# ❌ ROSSZ
@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
])  # type: ignore
def test_double(input, expected):
    ...

# ✅ JÓ
import pytest

@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
])
def test_double(input: int, expected: int) -> None:
    assert double(input) == expected
```

### QA Gate (MINDEN TESZT FÁJLNÁL)

```bash
# 1-3. Linting + Type Check
/home/elynea/miniconda3/envs/neural-ai-next/bin/ruff check tests/neural_ai/core/base/test_di_container.py
/home/elynea/miniconda3/envs/neural-ai-next/bin/mypy tests/neural_ai/core/base/test_di_container.py
/home/elynea/miniconda3/envs/neural-ai-next/bin/pyright tests/neural_ai/core/base/test_di_container.py

# 4. Tests (önmagát teszteli)
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/neural_ai/core/base/test_di_container.py -vv

# 5. Coverage (a tesztelt fájl coverage-e)
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest \
  --cov=neural_ai/core/base/implementations/di_container.py \
  --cov-report=term-missing \
  --cov-branch
# CÉL: 100% Stmt / 100% Brch

# 6-7. Commit + TASK_TREE
git add tests/neural_ai/core/base/test_di_container.py
git commit -m "refactor(type-safety): di_container test type ignore javítás"
python scripts/generate.py
git add docs/development/TASK_TREE.md
git commit -m "docs(task-tree): di_container test státusz frissítés"
```

### Deliverable
- ✅ 150+ teszt fájl auditálva
- ✅ <30 `# type: ignore`
- ✅ **100% Stmt / 100% Brch coverage** a tesztelt fájloknál
- ✅ 0 Ruff/Mypy/Pyright hiba
- ✅ MagicMock spec használat mindenhol

---

## 🎯 MILESTONE 5.2: SCRIPTS (10. hét vége)

### Fájlok
- [`scripts/`](../../../scripts/) - 18 fájl

### Fókusz Területek

#### Privát Metódus Hívás Dokumentálása
```python
# ❌ ROSSZ
obj._private_method()  # type: ignore

# ✅ JÓ
# Teszt célból privát metódus hívása - szándékos
obj._private_method()  # type: ignore[attr-defined]
```

#### CLI Argument Típusok
```python
# ❌ ROSSZ
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file")
    args = parser.parse_args()  # type: ignore
    process(args.file)  # type: ignore

# ✅ JÓ
import argparse
from typing import Any

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, required=True)
    args = parser.parse_args()
    file_path: str = args.file
    process(file_path)
```

#### Script Utility Típusok
```python
# ❌ ROSSZ
def load_config(path):  # type: ignore
    with open(path) as f:
        return yaml.safe_load(f)  # type: ignore

# ✅ JÓ
from typing import Any
import yaml

def load_config(path: str) -> dict[str, Any]:
    with open(path) as f:
        return yaml.safe_load(f)
```

### QA Gate (MINDEN SCRIPT FÁJLNÁL)

```bash
# 1-3. Linting + Type Check
/home/elynea/miniconda3/envs/neural-ai-next/bin/ruff check scripts/generate.py
/home/elynea/miniconda3/envs/neural-ai-next/bin/mypy scripts/generate.py
/home/elynea/miniconda3/envs/neural-ai-next/bin/pyright scripts/generate.py

# 4-5. Tests + Coverage
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/scripts/test_generate.py -vv
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest \
  --cov=scripts/generate.py \
  --cov-report=term-missing \
  --cov-branch
# CÉL: 100% Stmt / 100% Brch

# 6-7. Commit + TASK_TREE
git add scripts/generate.py tests/scripts/test_generate.py
git commit -m "refactor(type-safety): generate script type ignore javítás"
python scripts/generate.py
git add docs/development/TASK_TREE.md
git commit -m "docs(task-tree): generate script státusz frissítés"
```

### Deliverable
- ✅ 18 script fájl auditálva
- ✅ <10 `# type: ignore`
- ✅ **100% Stmt / 100% Brch coverage** minden scriptnél
- ✅ 0 Ruff/Mypy/Pyright hiba
- ✅ CLI argumentumok típusosak

---

## 📋 FÁZIS 5 ÖSSZESÍTÉS

### Eredmények

**Előtte**:
- ~80+ `# type: ignore` a test/script rétegben
- MagicMock típus problémák
- Fixture típus hiányok

**Utána**:
- ✅ <40 `# type: ignore` (dokumentált)
- ✅ 168+ fájl tiszta
- ✅ **100% Stmt / 100% Brch coverage** minden fájlnál
- ✅ 0 Ruff/Mypy/Pyright hiba
- ✅ Test & Script layer típusbiztos

### Következő lépés

**Delegálás**: Fázis 6 - Coverage 100% & Finalizálás
**Mód**: test-unit, docs-api, qa
**Időkeret**: 2 hét

---

**Verzió**: 1.0
**Utolsó frissítés**: 2026-03-30
