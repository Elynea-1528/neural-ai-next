# scripts/bootstrap_integration_test.py

Bootstrap integrációs teszt szkript.

Ez a szkript végrehajtja a neural_ai.core.bootstrap_core() függvényt,
és ellenőrzi a rendszer komponenseinek helyes inicializálását.

## Importok

```python
import sys
import traceback
from pathlib import Path
from neural_ai.core import bootstrap_core
```

## Konstansok

- **`project_root`**
: `Path(__file__).parent.parent`


- **`core`**
: `bootstrap_core()`


- **`exit_code`**
: `main()`


### `main()`

```python
def main() -> int
```

Fő teszt függvény.

**Visszatérési érték:**

- Típus: `int`
- 0 ha sikeres, 1 ha hiba történt

---

**Forrásfájl:** [`scripts/bootstrap_integration_test.py`](../../scripts/bootstrap_integration_test.py)
