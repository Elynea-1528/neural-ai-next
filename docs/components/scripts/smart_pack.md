# scripts/smart_pack.py

Smart Context Packer & Drive Sync.

Ez a szkript összegyűjti a projekt releváns forráskódjait egyetlen
Markdown/Text fájlba a LLM kontextus számára, és automatikusan
szinkronizálja a Google Drive-ra (Linux GVFS támogatással).

## Importok

```python
import argparse
import os
import subprocess
import time
from pathlib import Path
```

## Konstansok

- **`PROJECT_ROOT`**
: `Path(__file__).parent.parent.resolve()`


- **`OUTPUT_FILENAME_TXT`**
: `'neural_ai_full_context.txt'`


- **`OUTPUT_FILE_TXT`**
: `PROJECT_ROOT / OUTPUT_FILENAME_TXT`


- **`OUTPUT_FILENAME_MD`**
: `'neural_ai_full_context.md'`


- **`OUTPUT_FILE_MD`**
: `PROJECT_ROOT / OUTPUT_FILENAME_MD`


- **`DRIVE_SUBFOLDER`**
: `'Google AI Studio'`


- **`INCLUDE_DIRS`**
: `['neural_ai', 'scripts', 'configs', 'docs', 'external']`


- **`INCLUDE_FILES`**
: `['pyproject.toml', 'main.py', 'README.md', '.gitignore', '.vscode/settings.json']`


- **`uid`**
: `os.getuid()`


- **`gvfs_root`**
: `Path(f'/run/user/{uid}/gvfs')`


- **`target`**
: `item / DRIVE_SUBFOLDER`


- **`dest_folder`**
: `find_drive_path()`


- **`dest_file`**
: `dest_folder / source_file.name`


- **`start_t`**
: `time.time()`


- **`cmd`**
: `['cp', str(source_file), str(dest_file)]`


- **`result`**
: `subprocess.run(cmd, capture_output=True, text=True)`


- **`duration`**
: `time.time() - start_t`


- **`rel_path`**
: `path.relative_to(PROJECT_ROOT)`


- **`path`**
: `PROJECT_ROOT / f`


- **`dir_path`**
: `PROJECT_ROOT / d`


- **`unique_files`**
: `sorted(set(all_files))`


- **`count`**
: `0`


- **`timestamp`**
: `time.strftime('%Y-%m-%d %H:%M:%S')`


- **`header_txt`**
: `f'=== NEURAL AI NEXT CONTEXT ({mode.upper()}) ===\n'`


- **`header_md`**
: `f'# NEURAL AI NEXT CONTEXT ({mode.upper()})\n'`


- **`rel`**
: `path.relative_to(PROJECT_ROOT)`


- **`content`**
: `path.read_text(encoding='utf-8', errors='ignore')`


- **`ext`**
: `path.suffix[1:] if path.suffix else 'text'`


- **`ext`**
: `'cpp'`


- **`size_mb_txt`**
: `os.path.getsize(OUTPUT_FILE_TXT) / (1024 * 1024)`


- **`size_mb_md`**
: `os.path.getsize(OUTPUT_FILE_MD) / (1024 * 1024)`


- **`parser`**
: `argparse.ArgumentParser()`


- **`args`**
: `parser.parse_args()`


### `find_drive_path()`

```python
def find_drive_path() -> Path | None
```

Megkeresi az Ubuntu által felcsatolt Google Drive útvonalat.

**Visszatérési érték:**

- Típus: `Path | None`
- Path | None: A célmappa útvonala, vagy None ha nem található.

### `sync_to_drive()`

```python
def sync_to_drive(source_file: Path) -> None
```

Átmásolja a fájlt a Linux 'cp' parancsával (GVFS Workaround).

**Paraméterek:**

- **`source_file`** (`Path`): A forrásfájl útvonala.

**Visszatérési érték:**

- Típus: `None`

### `is_ignored()`

```python
def is_ignored(path: Path) -> bool
```

Eldönti, hogy egy fájl kihagyandó-e.

**Paraméterek:**

- **`path`** (`Path`): A vizsgált fájl útvonala.

**Visszatérési érték:**

- Típus: `bool`
- bool: True ha ki kell hagyni.

### `pack_project()`

```python
def pack_project(mode: str = 'full') -> None
```

Projekt csomagolása.

**Paraméterek:**

- **`mode`** (`str`) = `'full'`: Csomagolási mód (jelenleg csak 'full' támogatott).

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`scripts/smart_pack.py`](../../scripts/smart_pack.py)
