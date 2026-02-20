# scripts/data_reset.py

Adat reset szkript a Neural AI Next rendszer számára.

Ez a script végrehajtja az adat reset műveletet, törölve az összes tick adatot és logokat
a tiszta validáció érdekében.

Használat:
    python scripts/data_reset.py

## Importok

```python
import os
import shutil
import sys
from pathlib import Path
```

## Konstansok

- **`directories`**
: `['data/tick', 'logs']`


- **`tick_dir`**
: `'data/tick'`


- **`logs_dir`**
: `'logs'`


- **`item_path`**
: `os.path.join(logs_dir, item)`


- **`tick_success`**
: `remove_tick_data()`


- **`logs_success`**
: `remove_logs()`


### `check_directory_exists()`

```python
def check_directory_exists(path: str) -> bool
```

Ellenőrzi, hogy a megadott könyvtár létezik-e és könyvtár-e.

**Paraméterek:**

- **`path`** (`str`): A könyvtár elérési útja.

**Visszatérési érték:**

- Típus: `bool`
- True ha létezik és könyvtár, különben False.

### `create_directories_if_needed()`

```python
def create_directories_if_needed() -> None
```

Létrehozza a szükséges könyvtárakat, ha nem léteznek.

**Visszatérési érték:**

- Típus: `None`

### `remove_tick_data()`

```python
def remove_tick_data() -> bool
```

Eltávolítja a teljes tick adat könyvtárat.

**Visszatérési érték:**

- Típus: `bool`
- True ha sikeres, False ha hiba történt.

### `remove_logs()`

```python
def remove_logs() -> bool
```

Eltávolítja az összes fájlt és alkönyvtárat a logs könyvtárban.

**Visszatérési érték:**

- Típus: `bool`
- True ha sikeres, False ha hiba történt.

### `main()`

```python
def main() -> None
```

Fő függvény az adat reset végrehajtásához.

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`scripts/data_reset.py`](../../scripts/data_reset.py)
