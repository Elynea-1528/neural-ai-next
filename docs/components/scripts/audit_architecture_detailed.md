# scripts/audit_architecture_detailed.py

Részletes Architecture Audit Script.

Ellenőrzi:
1. DDD Réteg Hierarchia (alsó → felső TILOS)
2. Modul Struktúra (interfaces/, implementations/, exceptions/, factory.py)
3. DI Pattern (konstruktor injektálás)
4. Import Szabályok (abszolút kötelező)
5. Type Safety (Pydantic, Any TILOS)
6. Mirror Testing (tests/ struktúra)

## Importok

```python
import ast
from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from pathlib import Path
```

## Konstansok

- **`project_root`**
: `Path(__file__).parent.parent`


- **`auditor`**
: `ArchitectureAuditor(project_root)`


## Osztály: `Issue`

Audit probléma.

## Osztály: `ModuleAudit`

Modul audit eredmény.

## Osztály: `ArchitectureAuditor`

Architecture Audit Engine.

### Metódusok

#### `__init__()`

```python
def __init__(self, project_root: Path)
```

Initialize the architecture auditor.

**Paraméterek:**

- **`self`**
- **`project_root`** (`Path`)

#### `run()`

```python
def run(self) -> None
```

Audit futtatása.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `_audit_module_structure()`

```python
def _audit_module_structure(self) -> None
```

Modul struktúra ellenőrzés (DDD Atomic Unit).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `_audit_file()`

```python
def _audit_file(self, file_path: Path) -> None
```

Egyetlen Python fájl audit.

**Paraméterek:**

- **`self`**
- **`file_path`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `_check_imports()`

```python
def _check_imports(self, tree: ast.AST, rel_path: Path) -> None
```

Import szabályok ellenőrzése.

**Paraméterek:**

- **`self`**
- **`tree`** (`ast.AST`)
- **`rel_path`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `_is_lazy_import()`

```python
def _is_lazy_import(self, node: ast.ImportFrom, tree: ast.AST) -> bool
```

Ellenőrzi, hogy az import lazy import-e (függvényen belül van).

**Paraméterek:**

- **`self`**
- **`node`** (`ast.ImportFrom`)
- **`tree`** (`ast.AST`)

**Visszatérési érték:**

- Típus: `bool`

#### `_is_in_type_checking_block()`

```python
def _is_in_type_checking_block(self, node: ast.ImportFrom, tree: ast.AST) -> bool
```

Ellenőrzi, hogy az import TYPE_CHECKING blokkon belül van-e.

**Paraméterek:**

- **`self`**
- **`node`** (`ast.ImportFrom`)
- **`tree`** (`ast.AST`)

**Visszatérési érték:**

- Típus: `bool`

#### `_check_layer_dependencies()`

```python
def _check_layer_dependencies(self, tree: ast.AST, rel_path: Path) -> None
```

DDD Réteg függőség ellenőrzés (alsó → felső TILOS).

**Paraméterek:**

- **`self`**
- **`tree`** (`ast.AST`)
- **`rel_path`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `_check_di_pattern()`

```python
def _check_di_pattern(self, tree: ast.AST, rel_path: Path) -> None
```

DI Pattern ellenőrzés (konstruktor injektálás).

**Paraméterek:**

- **`self`**
- **`tree`** (`ast.AST`)
- **`rel_path`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `_check_type_safety()`

```python
def _check_type_safety(self, tree: ast.AST, rel_path: Path) -> None
```

Type Safety ellenőrzés (Any TILOS, Pydantic kötelező config-nál).

**Paraméterek:**

- **`self`**
- **`tree`** (`ast.AST`)
- **`rel_path`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `_check_exports()`

```python
def _check_exports(self, tree: ast.AST, rel_path: Path) -> None
```

Export ellenőrzés (__init__.py fájlokban).

**Paraméterek:**

- **`self`**
- **`tree`** (`ast.AST`)
- **`rel_path`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `_audit_mirror_testing()`

```python
def _audit_mirror_testing(self) -> None
```

Mirror Testing ellenőrzés.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `_generate_report()`

```python
def _generate_report(self) -> None
```

Riport generálás.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `_get_layer_from_path()`

```python
def _get_layer_from_path(self, path: str) -> str
```

Réteg meghatározása fájl útvonalból.

**Paraméterek:**

- **`self`**
- **`path`** (`str`)

**Visszatérési érték:**

- Típus: `str`

### `main()`

```python
def main() -> None
```

Főprogram.

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`scripts/audit_architecture_detailed.py`](../../scripts/audit_architecture_detailed.py)
