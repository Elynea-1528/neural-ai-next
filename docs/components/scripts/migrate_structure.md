# scripts/migrate_structure.py

Adatstruktúra migrációs szkript.

Ez a szkript a tick adatokat migrálja az új mappa szerkezetbe.
Az új szerkezet: data/tick/SYMBOL/YEAR/MONTH/DAY/ fájlok

## Importok

```python
import sys
from pathlib import Path
from typing import Any
from neural_ai.core.base.implementations.component_bundle import CoreComponentFactory
import shutil
import traceback
```

## Konstansok

- **`base_dir`**
: `Path('data/tick')`


- **`symbols_processed`**
: `0`


- **`symbols_migrated`**
: `0`


- **`symbol_name`**
: `symbol_dir.name`


- **`tick_subdir`**
: `symbol_dir / 'tick'`


- **`tick_contents`**
: `list(tick_subdir.iterdir())`


- **`year_name`**
: `item.name`


- **`target_year_dir`**
: `symbol_dir / year_name`


- **`components`**
: `CoreComponentFactory.create_minimal()`


- **`logger`**
: `components.logger`


### `migrate_tick_structure()`

```python
def migrate_tick_structure(logger: Any) -> None
```

Tick adatstruktúra migrálása. Az új szerkezet: data/tick/SYMBOL/YEAR/MONTH/DAY/ fájlok A régi szerkezet: data/tick/SYMBOL/tick/YEAR/... fájlok

**Paraméterek:**

- **`logger`** (`Any`): A logger példány

**Visszatérési érték:**

- Típus: `None`

### `main()`

```python
def main() -> int
```

Fő függvény a szkript futtatásához.

**Visszatérési érték:**

- Típus: `int`
- int: Kilépési kód (0 = siker, 1 = hiba)

---

**Forrásfájl:** [`scripts/migrate_structure.py`](../../scripts/migrate_structure.py)
