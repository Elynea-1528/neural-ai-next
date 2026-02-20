# scripts/deploy_jforex.py

JForex Auto-Deploy Script.

Automatically builds the JForex bridge and deploys it to the JForex Strategies folder.
Provides an MT5-like seamless installation experience.

Author: Neural AI Team
Version: 1.0.0

## Importok

```python
import os
import shutil
import subprocess
import sys
from pathlib import Path
import traceback
```

## Konstansok

- **`possible_paths`**
: `[Path.home() / 'JForex4' / 'Strategies', Path.home() / 'Documents' / 'JForex4' / 'Strategies', Path.home() / 'JForex4', Path.home() / 'Documents' / 'JForex4', Path.home() / 'JForex' / 'Strategies', Path.home() / 'Documents' / 'JForex' / 'Strategies', Path.home() / 'JForex', Path.home() / 'Documents' / 'JForex']`


- **`strategies_path`**
: `path / 'Strategies'`


- **`user_input`**
: `input('\n📁 Kérem adja meg a JForex mappa teljes útvonalát: ').strip()`


- **`jforex_path`**
: `Path(user_input)`


- **`original_cwd`**
: `os.getcwd()`


- **`result`**
: `subprocess.run(['gradle', 'build'], capture_output=True, text=True, timeout=300)`


- **`java_source`**
: `bridge_path / 'src' / 'main' / 'java' / 'com' / 'neuralai' / 'bridge' / 'NeuralBridgeStrategy.java'`


- **`destination_file`**
: `jforex_path / 'NeuralBridgeStrategy.java'`


- **`libs_dir`**
: `bridge_path / 'build' / 'libs'`


- **`jforex_libs`**
: `jforex_path / 'files'`


- **`jar_files`**
: `list(libs_dir.glob('*.jar'))`


- **`destination_jar`**
: `jforex_libs / jar_file.name`


- **`libs_dir`**
: `jforex_path / 'files'`


- **`jar_files`**
: `list(libs_dir.glob('*.jar'))`


- **`jforex_path`**
: `find_jforex_folder()`


- **`bridge_path`**
: `Path(__file__).parent.parent / 'external' / 'jforex-bridge'`


### `find_jforex_folder()`

```python
def find_jforex_folder() -> Path
```

Megkeresi a JForex telepítési mappát.

**Visszatérési érték:**

- Típus: `Path`
- Path: A JForex Strategies mappa útvonala

**Kivételek:**

- **`FileNotFoundError`**: Ha nem található JForex mappa

### `run_gradle_build()`

```python
def run_gradle_build(bridge_path: Path) -> bool
```

Lefuttatja a Gradle buildet a JForex bridge mappában.

**Paraméterek:**

- **`bridge_path`** (`Path`): A jforex-bridge mappa útvonala

**Visszatérési érték:**

- Típus: `bool`
- bool: True ha a build sikeres, False egyébként

### `deploy_files()`

```python
def deploy_files(bridge_path: Path, jforex_path: Path) -> bool
```

Bemásolja a szükséges fájlokat a JForex mappába.

**Paraméterek:**

- **`bridge_path`** (`Path`): A jforex-bridge mappa útvonala
- **`jforex_path`** (`Path`): A JForex Strategies mappa útvonala

**Visszatérési érték:**

- Típus: `bool`
- bool: True ha a telepítés sikeres, False egyébként

### `print_summary()`

```python
def print_summary(jforex_path: Path)
```

Kiírja a telepítés utáni összefoglalót.

**Paraméterek:**

- **`jforex_path`** (`Path`): A JForex Strategies mappa útvonala

### `main()`

```python
def main()
```

Fő végrehajtási függvény.

---

**Forrásfájl:** [`scripts/deploy_jforex.py`](../../scripts/deploy_jforex.py)
