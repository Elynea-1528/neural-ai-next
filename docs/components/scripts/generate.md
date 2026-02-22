# scripts/generate.py

TASK_TREE v5.0 Simplified Auditor - Hibrid Kódminőség Ellenőrző.

Egyszerűsített verzió: egyetlen TASK_TREE.md/html generálás (összes réteg).

Funkciók:
- AST: Config típus, Logger DI, Mirror Test ellenőrzés
- Pytest: Teszt eredmények (Pass/Fail/Warn)
- Coverage: Utasítás és elágazás lefedettség
- Ruff: Linter hibák száma
- Mypy: Típus hibák száma
- Pyright: Pylance hibák száma

## Importok

```python
import ast
import html
import json
import os
import subprocess
from dataclasses import dataclass
from datetime import UTC
from datetime import datetime
from pathlib import Path
from typing import Any
# ... és még 1 import
```

## Konstansok

- **`PROJECT_ROOT`**
: `Path(__file__).resolve().parent.parent`


- **`CONDA_ENV_BIN`**
: `Path('/home/elynea/miniconda3/envs/neural-ai-next/bin')`


- **`PYTEST_BIN`**
: `CONDA_ENV_BIN / 'pytest'`


- **`COVERAGE_BIN`**
: `CONDA_ENV_BIN / 'coverage'`


- **`RUFF_BIN`**
: `CONDA_ENV_BIN / 'ruff'`


- **`MYPY_BIN`**
: `CONDA_ENV_BIN / 'mypy'`


- **`REPORT_DIR`**
: `PROJECT_ROOT / 'reports'`


- **`COVERAGE_FILE`**
: `REPORT_DIR / 'coverage.json'`


- **`RUFF_FILE`**
: `REPORT_DIR / 'ruff.json'`


- **`MYPY_FILE`**
: `REPORT_DIR / 'mypy.json'`


- **`OUTPUT_MD`**
: `PROJECT_ROOT / 'docs' / 'development' / 'TASK_TREE.md'`


- **`OUTPUT_HTML`**
: `PROJECT_ROOT / 'docs' / 'development' / 'TASK_TREE.html'`


- **`generator`**
: `TaskTreeGenerator()`


## Osztály: `FileAnalysis`

Egyetlen fájl analízis eredménye.

## Osztály: `ASTAnalyzer`

AST-alapú Python fájl elemző.

### Metódusok

#### `__init__()`

```python
def __init__(self, file_path: Path) -> None
```

Inicializálja az analizátort.

**Paraméterek:**

- **`self`**
- **`file_path`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `parse()`

```python
def parse(self) -> bool
```

Beolvassa és parse-olja a fájlt.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `bool`

#### `check_config_type()`

```python
def check_config_type(self) -> Literal['✅ OK', '🔴 TYPED_DICT', '⚪ N/A']
```

Ellenőrzi a config típusát (Pydantic vs TypedDict).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `Literal['✅ OK', '🔴 TYPED_DICT', '⚪ N/A']`

#### `check_logger_injection()`

```python
def check_logger_injection(self) -> Literal['✅ OK', '⚠️ UNUSED', '🔴 MISSING', '⚪ N/A']
```

Ellenőrzi a logger dependency injection-t.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `Literal['✅ OK', '⚠️ UNUSED', '🔴 MISSING', '⚪ N/A']`

#### `count_tests()`

```python
def count_tests(self) -> int
```

Megszámolja a test_ prefixű függvényeket.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `int`

## Osztály: `MirrorChecker`

Mirror Rule ellenőrző (neural_ai/x.py ↔ tests/x/test_x.py).

### Metódusok

#### `check_documentation()`

```python
def check_documentation(source_path: Path) -> bool
```

Ellenőrzi, hogy van-e dokumentáció a fájlhoz a docs/ mappában. Példák: - main.py -> docs/components/main.md - scripts/generate.py -> docs/components/scripts/generate.md - neural_ai/core/config/factory.py -> docs/components/neural_ai/core/config/factory.md

**Paraméterek:**

- **`source_path`** (`Path`)

**Visszatérési érték:**

- Típus: `bool`

#### `get_test_path()`

```python
def get_test_path(source_path: Path) -> Path
```

Kiszámítja a mirror test fájl útvonalát. Ha a test_X.py nem létezik, megpróbálja a test_X_integration.py-t is. Ha implementations/interfaces/exceptions mappában van, a szülő mappában is keres.

**Paraméterek:**

- **`source_path`** (`Path`)

**Visszatérési érték:**

- Típus: `Path`

#### `check_mirror()`

```python
def check_mirror(source_path: Path) -> tuple[bool, Path]
```

Ellenőrzi, hogy létezik-e a mirror teszt fájl.

**Paraméterek:**

- **`source_path`** (`Path`)

**Visszatérési érték:**

- Típus: `tuple[bool, Path]`

## Osztály: `StatusCalculator`

Státusz kalkulátor logika.

### Metódusok

#### `calculate()`

```python
def calculate(analysis: FileAnalysis) -> Literal['✅ SECURE', '🟡 WARNING', '🔴 VULNERABLE']
```

Kiszámítja az overall státuszt. ✅ SECURE: Minden tökéletes (0 hiba, 0 warning, tesztek OK, dokumentáció OK) 🟡 WARNING: Van javítanivaló, de nem kritikus 🔴 VULNERABLE: Kritikus problémák (teszt hiány, TypedDict, Logger DI hiány, failed tesztek)

**Paraméterek:**

- **`analysis`** (`FileAnalysis`)

**Visszatérési érték:**

- Típus: `Literal['✅ SECURE', '🟡 WARNING', '🔴 VULNERABLE']`

#### `generate_notes()`

```python
def generate_notes(analysis: FileAnalysis) -> str
```

Generál részletes teendő megjegyzéseket.

**Paraméterek:**

- **`analysis`** (`FileAnalysis`)

**Visszatérési érték:**

- Típus: `str`

## Osztály: `GeneratorBase`

Közös bázis osztály a Markdown és HTML generátorokhoz.

### Metódusok

#### `__init__()`

```python
def __init__(self, analyses: list[FileAnalysis]) -> None
```

Inicializálja a generátort.

**Paraméterek:**

- **`self`**
- **`analyses`** (`list[FileAnalysis]`): Fájl analízisek listája

**Visszatérési érték:**

- Típus: `None`

#### `_group_by_layer()`

```python
def _group_by_layer(self) -> dict[str, list[FileAnalysis]]
```

Csoportosítja a fájlokat réteg szerint.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `dict[str, list[FileAnalysis]]`

#### `calculate_statistics()`

```python
def calculate_statistics(self) -> dict[str, int]
```

Statisztikákat számol az összes fájlhoz.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `dict[str, int]`

## Osztály: `MarkdownGenerator(GeneratorBase)`

TASK_TREE.md generátor.

### Metódusok

#### `_create_table()`

```python
def _create_table(self, layer: str, files: list[FileAnalysis]) -> str
```

Létrehoz egy Markdown táblázatot egy réteghez.

**Paraméterek:**

- **`self`**
- **`layer`** (`str`)
- **`files`** (`list[FileAnalysis]`)

**Visszatérési érték:**

- Típus: `str`

#### `generate()`

```python
def generate(self) -> str
```

Generálja a teljes Markdown tartalmat.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `str`

## Osztály: `HTMLGenerator(GeneratorBase)`

HTML Dashboard generátor.

### Metódusok

#### `calculate_statistics()`

```python
def calculate_statistics(self) -> dict[str, int]
```

Statisztikákat számol az összes fájlhoz (HTML specifikus).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `dict[str, int]`

#### `generate()`

```python
def generate(self) -> str
```

Generálja a teljes HTML tartalmat.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `str`

#### `_create_html_table()`

```python
def _create_html_table(self, layer: str, files: list[FileAnalysis]) -> str
```

Létrehoz egy HTML táblázatot egy réteghez.

**Paraméterek:**

- **`self`**
- **`layer`** (`str`)
- **`files`** (`list[FileAnalysis]`)

**Visszatérési érték:**

- Típus: `str`

## Osztály: `TaskTreeGenerator`

Fő orchestrator osztály.

### Metódusok

#### `__init__()`

```python
def __init__(self, source_dir: str = 'neural_ai', output_file: str = 'docs/development/TASK_TREE.md') -> None
```

Inicializálja a generátort.

**Paraméterek:**

- **`self`**
- **`source_dir`** (`str`) = `'neural_ai'`
- **`output_file`** (`str`) = `'docs/development/TASK_TREE.md'`

**Visszatérési érték:**

- Típus: `None`

#### `run_dynamic_tools()`

```python
def run_dynamic_tools(self) -> None
```

Futtatja a dinamikus ellenőrző eszközöket.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `get_dynamic_metrics()`

```python
def get_dynamic_metrics(self, file_path: Path) -> dict[str, Any]
```

Visszaadja a dinamikus metrikákat egy fájlhoz.

**Paraméterek:**

- **`self`**
- **`file_path`** (`Path`)

**Visszatérési érték:**

- Típus: `dict[str, Any]`

#### `scan_codebase()`

```python
def scan_codebase(self) -> list[Path]
```

Rekurzívan bejárja a neural_ai/, tests/, scripts/ mappákat + projekt gyökér fájlok.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `list[Path]`

#### `analyze_file()`

```python
def analyze_file(self, file_path: Path) -> FileAnalysis
```

Elemez egy fájlt.

**Paraméterek:**

- **`self`**
- **`file_path`** (`Path`)

**Visszatérési érték:**

- Típus: `FileAnalysis`

#### `generate()`

```python
def generate(self) -> None
```

Generálja a TASK_TREE.md és TASK_TREE.html fájlokat.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`scripts/generate.py`](../../scripts/generate.py)
