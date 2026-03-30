# scripts/audit_architecture.py

Architecture Audit Script - Pre-audit a teljes projektre.

Ellenőrzi:
- Fájlnév konvenció (redundáns prefix-ek)
- Import típus (relatív vs abszolút)
- Struktúra (The Atomic Unit)
- Mirror Testing
- Export szabályok (__init__.py)

Output: docs/development/ARCHITECTURE_AUDIT.md

## Importok

```python
import ast
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Literal
```

## Konstansok

- **`PROJECT_ROOT`**
: `Path(__file__).resolve().parent.parent`


- **`auditor`**
: `ArchitectureAuditor()`


## Osztály: `FileIssue`

Egy fájl problémája.

## Osztály: `ArchitectureAuditor`

Architecture audit végrehajtó.

### Metódusok

#### `__init__()`

```python
def __init__(self) -> None
```

Inicializálja az auditor-t.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `scan_codebase()`

```python
def scan_codebase(self) -> list[Path]
```

Szkenneli a projektet.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `list[Path]`

#### `check_filename()`

```python
def check_filename(self, file: Path) -> None
```

Ellenőrzi a fájlnév konvenciót.

**Paraméterek:**

- **`self`**
- **`file`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `check_imports()`

```python
def check_imports(self, file: Path) -> None
```

Ellenőrzi az importokat.

**Paraméterek:**

- **`self`**
- **`file`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `check_structure()`

```python
def check_structure(self, file: Path) -> None
```

Ellenőrzi a modul struktúrát.

**Paraméterek:**

- **`self`**
- **`file`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `check_mirror_test()`

```python
def check_mirror_test(self, file: Path) -> None
```

Ellenőrzi a Mirror Testing szabályt.

**Paraméterek:**

- **`self`**
- **`file`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `check_exports()`

```python
def check_exports(self, file: Path) -> None
```

Ellenőrzi az export szabályokat (__init__.py).

**Paraméterek:**

- **`self`**
- **`file`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `run_audit()`

```python
def run_audit(self) -> None
```

Futtatja az audit-ot.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `generate_report()`

```python
def generate_report(self) -> str
```

Generálja a riportot.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `str`

#### `save_report()`

```python
def save_report(self, output_file: Path) -> None
```

Menti a riportot.

**Paraméterek:**

- **`self`**
- **`output_file`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`scripts/audit_architecture.py`](../../scripts/audit_architecture.py)
