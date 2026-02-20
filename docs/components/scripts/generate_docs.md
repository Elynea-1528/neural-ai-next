# scripts/generate_docs.py

Profi dokumentáció generátor a Neural AI Next projekthez.

Ez a script AST-alapú elemzéssel generál részletes, profi szintű dokumentációt:
- Google Style docstring parsing
- Függvény szignatúrák type hints-tel
- Paraméter és return type dokumentáció
- Import és dependency tracking
- Tükör struktúra: root, scripts, neural_ai mappák

## Importok

```python
import ast
import inspect
import re
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from typing import Any
import shutil
```

## Konstansok

- **`generator`**
: `DocumentationGenerator()`


## Osztály: `Parameter`

Függvény paraméter reprezentáció.

## Osztály: `FunctionInfo`

Függvény információ.

## Osztály: `ClassInfo`

Osztály információ.

## Osztály: `ModuleInfo`

Modul információ.

## Osztály: `GoogleDocstringParser`

Google Style docstring parser.

### Metódusok

#### `parse()`

```python
def parse(docstring: str | None) -> dict[str, Any]
```

Parse Google Style docstring.

**Paraméterek:**

- **`docstring`** (`str | None`): A docstring szöveg.

**Visszatérési érték:**

- Típus: `dict[str, Any]`
- Dict a parsed adatokkal (description, args, returns, raises, examples).

## Osztály: `ASTExtractor(ast.NodeVisitor)`

AST-alapú kód elemző.

### Metódusok

#### `__init__()`

```python
def __init__(self, file_path: Path) -> None
```

Inicializálja az elemzőt.

**Paraméterek:**

- **`self`**
- **`file_path`** (`Path`): A Python fájl elérési útja.

**Visszatérési érték:**

- Típus: `None`

#### `visit_Module()`

```python
def visit_Module(self, node: ast.Module) -> None
```

Modul docstring kinyerése.

**Paraméterek:**

- **`self`**
- **`node`** (`ast.Module`)

**Visszatérési érték:**

- Típus: `None`

#### `visit_Import()`

```python
def visit_Import(self, node: ast.Import) -> None
```

Import statement kinyerése.

**Paraméterek:**

- **`self`**
- **`node`** (`ast.Import`)

**Visszatérési érték:**

- Típus: `None`

#### `visit_ImportFrom()`

```python
def visit_ImportFrom(self, node: ast.ImportFrom) -> None
```

From import statement kinyerése.

**Paraméterek:**

- **`self`**
- **`node`** (`ast.ImportFrom`)

**Visszatérési érték:**

- Típus: `None`

#### `visit_ClassDef()`

```python
def visit_ClassDef(self, node: ast.ClassDef) -> None
```

Osztály definíció kinyerése.

**Paraméterek:**

- **`self`**
- **`node`** (`ast.ClassDef`)

**Visszatérési érték:**

- Típus: `None`

#### `visit_FunctionDef()`

```python
def visit_FunctionDef(self, node: ast.FunctionDef) -> None
```

Függvény definíció kinyerése.

**Paraméterek:**

- **`self`**
- **`node`** (`ast.FunctionDef`)

**Visszatérési érték:**

- Típus: `None`

#### `visit_AsyncFunctionDef()`

```python
def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None
```

Aszinkron függvény definíció kinyerése.

**Paraméterek:**

- **`self`**
- **`node`** (`ast.AsyncFunctionDef`)

**Visszatérési érték:**

- Típus: `None`

#### `visit_Assign()`

```python
def visit_Assign(self, node: ast.Assign) -> None
```

Konstans/változó kinyerése (modul szintű).

**Paraméterek:**

- **`self`**
- **`node`** (`ast.Assign`)

**Visszatérési érték:**

- Típus: `None`

#### `_extract_function()`

```python
def _extract_function(self, node: ast.FunctionDef | ast.AsyncFunctionDef, is_async: bool) -> FunctionInfo
```

Függvény információ kinyerése.

**Paraméterek:**

- **`self`**
- **`node`** (`ast.FunctionDef | ast.AsyncFunctionDef`)
- **`is_async`** (`bool`)

**Visszatérési érték:**

- Típus: `FunctionInfo`

#### `_get_annotation()`

```python
def _get_annotation(self, annotation: ast.expr | None) -> str | None
```

Type annotation string kinyerése.

**Paraméterek:**

- **`self`**
- **`annotation`** (`ast.expr | None`)

**Visszatérési érték:**

- Típus: `str | None`

#### `_get_name()`

```python
def _get_name(self, node: ast.expr) -> str
```

Node név kinyerése.

**Paraméterek:**

- **`self`**
- **`node`** (`ast.expr`)

**Visszatérési érték:**

- Típus: `str`

#### `_build_signature()`

```python
def _build_signature(self, name: str, parameters: list[Parameter], return_type: str | None, is_async: bool) -> str
```

Függvény szignatúra építése.

**Paraméterek:**

- **`self`**
- **`name`** (`str`)
- **`parameters`** (`list[Parameter]`)
- **`return_type`** (`str | None`)
- **`is_async`** (`bool`)

**Visszatérési érték:**

- Típus: `str`

## Osztály: `MarkdownBuilder`

Profi Markdown dokumentáció építő.

### Metódusok

#### `build()`

```python
def build(module_info: ModuleInfo) -> str
```

Markdown dokumentáció építése.

**Paraméterek:**

- **`module_info`** (`ModuleInfo`): A modul információ.

**Visszatérési érték:**

- Típus: `str`
- A generált Markdown tartalom.

#### `_build_class()`

```python
def _build_class(class_info: ClassInfo) -> str
```

Osztály dokumentáció építése.

**Paraméterek:**

- **`class_info`** (`ClassInfo`)

**Visszatérési érték:**

- Típus: `str`

#### `_build_function()`

```python
def _build_function(func_info: FunctionInfo, indent: bool = False) -> str
```

Függvény dokumentáció építése.

**Paraméterek:**

- **`func_info`** (`FunctionInfo`)
- **`indent`** (`bool`) = `False`

**Visszatérési érték:**

- Típus: `str`

## Osztály: `MirrorManager`

Tükör struktúra kezelő (root, scripts, neural_ai).

### Metódusok

#### `get_doc_path()`

```python
def get_doc_path(source_path: Path) -> Path
```

Dokumentáció útvonal kiszámítása.

**Paraméterek:**

- **`source_path`** (`Path`): A forrásfájl elérési útja.

**Visszatérési érték:**

- Típus: `Path`
- A dokumentáció fájl elérési útja.

## Osztály: `DocumentationGenerator`

Profi dokumentáció generátor.

### Metódusok

#### `__init__()`

```python
def __init__(self, source_dirs: list[str] | None = None, docs_dir: str = 'docs/components') -> None
```

Inicializálja a generátort.

**Paraméterek:**

- **`self`**
- **`source_dirs`** (`list[str] | None`) = `None`: A forráskód mappák listája (default: ["neural_ai", "scripts", "."]).
- **`docs_dir`** (`str`) = `'docs/components'`: A dokumentáció mappa elérési útja.

**Visszatérési érték:**

- Típus: `None`

#### `extract_module_info()`

```python
def extract_module_info(self, file_path: Path) -> ModuleInfo | None
```

Modul információ kinyerése.

**Paraméterek:**

- **`self`**
- **`file_path`** (`Path`): A Python fájl elérési útja.

**Visszatérési érték:**

- Típus: `ModuleInfo | None`
- A kinyert modul információ vagy None hiba esetén.

#### `generate_documentation()`

```python
def generate_documentation(self, file_path: Path) -> None
```

Dokumentáció generálása egy fájlhoz.

**Paraméterek:**

- **`self`**
- **`file_path`** (`Path`): A forrásfájl elérési útja.

**Visszatérési érték:**

- Típus: `None`

#### `generate_all()`

```python
def generate_all(self) -> None
```

Összes dokumentáció generálása.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `main()`

```python
def main() -> None
```

Főprogram.

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`scripts/generate_docs.py`](../../scripts/generate_docs.py)
