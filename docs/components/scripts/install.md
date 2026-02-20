# scripts/install.py

Neural AI Next - Unified Zero-Touch Installer.

=============================================

Automatizált telepítő a teljes környezet és brókerek beállításához.
Hardver detektálás, GPU ellenőrzés, AVX2 támogatás és automatikus bróker telepítés.

Használat:
    python scripts/install.py

Követelmények:
    - Conda/Miniconda telepítve kell legyen
    - Internet kapcsolat
    - Sudo jogosultság (csak Wine telepítéséhez)

## Importok

```python
import argparse
import os
import shutil
import subprocess
import sys
import traceback
from pathlib import Path
```

## Konstansok

- **`CONDA_ENV_NAME`**
: `'neural-ai-next'`


- **`PYTHON_VERSION`**
: `'3.12'`


- **`PROJECT_ROOT`**
: `Path(__file__).parent.parent`


- **`_verbose`**
: `False`


- **`BROKER_URLS`**
: `{'jforex4': 'https://dukascopy-eu.cdn.online-trading-solutions.com/installer4/dukascopy-eu/JForex4_unix_64_JRE_bundled.sh', 'tws': 'https://download2.interactivebrokers.com/installers/tws/latest/tws-latest-linux-x64.sh', 'mt5_dukascopy': 'https://download.mql5.com/cdn/web/dukascopy.bank.sa/mt5/dukascopy5setup.exe'}`


- **`result`**
: `subprocess.run(command, shell=shell, check=check, capture_output=True, text=True)`


- **`result`**
: `run_command('nvidia-smi --query-gpu=name --format=csv,noheader', check=False)`


- **`gpu_detected`**
: `bool(result.returncode == 0 and result.stdout and (result.stdout.strip() != ''))`


- **`cpuinfo`**
: `f.read()`


- **`result`**
: `run_command(f'{get_conda_path()} env list | grep {CONDA_ENV_NAME}', check=False)`


- **`python`**
: `f'python={PYTHON_VERSION}'`


- **`base_packages`**
: `'pandas numpy scikit-learn'`


- **`pytorch_packages`**
: `'pytorch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1 pytorch-cuda=12.1'`


- **`channels`**
: `'-c pytorch -c nvidia -c conda-forge'`


- **`pytorch_packages`**
: `'pytorch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1 cpuonly'`


- **`channels`**
: `'-c pytorch -c conda-forge'`


- **`lightning_package`**
: `'lightning=2.5.5'`


- **`all_packages`**
: `f'{python} {pytorch_packages} {lightning_package} {base_packages}'`


- **`groups_str`**
: `','.join(extra_groups)`


- **`downloads_dir`**
: `PROJECT_ROOT / 'downloads'`


- **`installer_path`**
: `downloads_dir / 'JForex4_unix_64_JRE_bundled.sh'`


- **`installer_path`**
: `downloads_dir / 'tws-latest-linux-x64.sh'`


- **`installer_path`**
: `downloads_dir / 'dukascopy5setup.exe'`


- **`wineprefix`**
: `Path.home() / '.mt5'`


- **`env`**
: `os.environ.copy()`


- **`downloads_dir`**
: `create_downloads_dir()`


- **`groups_str`**
: `', '.join(extra_groups)`


- **`parser`**
: `argparse.ArgumentParser(description='Neural AI Next - Unified Zero-Touch Installer', formatter_class=argparse.RawDescriptionHelpFormatter, epilog='\nPéldák:\n  python scripts/install.py                    # Alap telepítés (összes csoport)\n  python scripts/install.py --no-brokers       # Csak környezet, brókerek nélkül\n  python scripts/install.py --only dev         # Csak dev csomagok\n  python scripts/install.py --only dev,trader  # Dev + trader csomagok\n  python scripts/install.py -v                 # Verbose mód\n  python scripts/install.py --only dev -v      # Dev csomagok verbose módban\n        ')`


- **`args`**
: `parse_arguments()`


- **`_verbose`**
: `args.verbose`


- **`extra_groups`**
: `[g.strip() for g in args.only.split(',')]`


- **`extra_groups`**
: `['dev', 'trader', 'jupyter']`


## Osztály: `Colors`

Színek a konzol kimenethez.

### `print_banner()`

```python
def print_banner() -> None
```

Kiírja a telepítő bannerét.

**Visszatérési érték:**

- Típus: `None`

### `print_success()`

```python
def print_success(message: str) -> None
```

Zöld színnel kiírja a sikeres üzenetet.

**Paraméterek:**

- **`message`** (`str`)

**Visszatérési érték:**

- Típus: `None`

### `print_error()`

```python
def print_error(message: str) -> None
```

Piros színnel kiírja a hibát.

**Paraméterek:**

- **`message`** (`str`)

**Visszatérési érték:**

- Típus: `None`

### `print_warning()`

```python
def print_warning(message: str) -> None
```

Sárga színnel kiírja a figyelmeztetést.

**Paraméterek:**

- **`message`** (`str`)

**Visszatérési érték:**

- Típus: `None`

### `print_info()`

```python
def print_info(message: str) -> None
```

Kék színnel kiírja az információt.

**Paraméterek:**

- **`message`** (`str`)

**Visszatérési érték:**

- Típus: `None`

### `run_command()`

```python
def run_command(command: str, shell: bool = True, check: bool = True) -> 'subprocess.CompletedProcess[str]'
```

Lefuttat egy shell parancsot és visszaadja az eredményt.

**Paraméterek:**

- **`command`** (`str`): A futtatandó parancs
- **`shell`** (`bool`) = `True`: Használjon-e shell-t
- **`check`** (`bool`) = `True`: Dobjon-e kivételt, ha a parancs sikertelen

**Visszatérési érték:**

- Típus: `'subprocess.CompletedProcess[str]'`
- A lefuttatott parancs eredménye

### `command_exists()`

```python
def command_exists(command: str) -> bool
```

Ellenőrzi, hogy egy parancs elérhető-e a rendszeren.

**Paraméterek:**

- **`command`** (`str`): Az ellenőrizendő parancs

**Visszatérési érték:**

- Típus: `bool`
- True, ha a parancs elérhető

### `check_conda()`

```python
def check_conda() -> bool
```

Ellenőrzi, hogy Conda telepítve van-e.

**Visszatérési érték:**

- Típus: `bool`
- True, ha Conda elérhető

### `check_nvidia_gpu()`

```python
def check_nvidia_gpu() -> bool
```

Ellenőrzi, hogy NVIDIA GPU van-e a rendszerben.

**Visszatérési érték:**

- Típus: `bool`
- True, ha NVIDIA GPU található

### `check_avx2_support()`

```python
def check_avx2_support() -> bool
```

Ellenőrzi, hogy a CPU támogatja-e az AVX2 utasításkészletet.

**Visszatérési érték:**

- Típus: `bool`
- True, ha AVX2 támogatott

### `check_wine()`

```python
def check_wine() -> bool
```

Ellenőrzi, hogy Wine telepítve van-e.

**Visszatérési érték:**

- Típus: `bool`
- True, ha Wine elérhető

### `get_conda_path()`

```python
def get_conda_path() -> str
```

Visszaadja a Conda bináris elérési útját.

**Visszatérési érték:**

- Típus: `str`
- A Conda bináris elérési útja

### `remove_conda_env()`

```python
def remove_conda_env() -> None
```

Eltávolítja a neural-ai-next Conda környezetet, ha létezik.

**Visszatérési érték:**

- Típus: `None`

### `create_conda_env_with_packages()`

```python
def create_conda_env_with_packages(gpu_available: bool) -> None
```

Létrehozza a neural-ai-next Conda környezetet az összes csomaggal együtt.

**Paraméterek:**

- **`gpu_available`** (`bool`): True, ha GPU elérhető

**Visszatérési érték:**

- Típus: `None`

### `install_data_libraries()`

```python
def install_data_libraries(avx2_supported: bool) -> None
```

Telepíti az adatkezelő könyvtárakat (Polars/PyArrow vagy fastparquet).

**Paraméterek:**

- **`avx2_supported`** (`bool`): True, ha AVX2 támogatott

**Visszatérési érték:**

- Típus: `None`

### `install_project_packages()`

```python
def install_project_packages(extra_groups: list[str]) -> None
```

Telepíti a projekt csomagjait a megadott opcionális függőséggel.

**Paraméterek:**

- **`extra_groups`** (`list[str]`): Az opcionális függőségi csoportok listája (pl: ['dev', 'trader'])

**Visszatérési érték:**

- Típus: `None`

### `create_downloads_dir()`

```python
def create_downloads_dir() -> Path
```

Létrehozza a downloads mappát, ha nem létezik.

**Visszatérési érték:**

- Típus: `Path`
- A downloads mappa Path objektuma

### `download_file()`

```python
def download_file(url: str, output_path: Path) -> None
```

Letölt egy fájlt a megadott URL-ről.

**Paraméterek:**

- **`url`** (`str`): A letöltendő fájl URL-je
- **`output_path`** (`Path`): A cél fájl elérési útja

**Visszatérési érték:**

- Típus: `None`

### `install_jforex4()`

```python
def install_jforex4(downloads_dir: Path) -> None
```

Telepíti a JForex4-et háttérfolyamatként.

**Paraméterek:**

- **`downloads_dir`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

### `install_tws()`

```python
def install_tws(downloads_dir: Path) -> None
```

Telepíti az IBKR TWS-t háttérfolyamatként.

**Paraméterek:**

- **`downloads_dir`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

### `install_mt5_dukascopy()`

```python
def install_mt5_dukascopy(downloads_dir: Path) -> None
```

Telepíti a MetaTrader 5-öt (Dukascopy) Wine-on keresztül.

**Paraméterek:**

- **`downloads_dir`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

### `run_hardware_detection()`

```python
def run_hardware_detection() -> tuple[bool, bool]
```

Lefuttatja a hardver detektálást.

**Visszatérési érték:**

- Típus: `tuple[bool, bool]`
- Tuple: (gpu_available, avx2_supported)

### `install_core_environment()`

```python
def install_core_environment(gpu_available: bool, avx2_supported: bool, extra_groups: list[str]) -> None
```

Telepíti a core környezetet az új módszerrel (egyetlen conda create parancs).

**Paraméterek:**

- **`gpu_available`** (`bool`): True, ha GPU elérhető
- **`avx2_supported`** (`bool`): True, ha AVX2 támogatott
- **`extra_groups`** (`list[str]`): Az opcionális függőségi csoportok listája

**Visszatérési érték:**

- Típus: `None`

### `install_brokers()`

```python
def install_brokers() -> None
```

Telepíti az összes brókert automatikusan.

**Visszatérési érték:**

- Típus: `None`

### `print_completion_message()`

```python
def print_completion_message(gpu_available: bool, avx2_supported: bool, extra_groups: list[str]) -> None
```

Kiírja a telepítés befejezési üzenetét a telepített verziókkal.

**Paraméterek:**

- **`gpu_available`** (`bool`): True, ha GPU elérhető
- **`avx2_supported`** (`bool`): True, ha AVX2 támogatott
- **`extra_groups`** (`list[str]`): A telepített csomagcsoportok listája

**Visszatérési érték:**

- Típus: `None`

### `parse_arguments()`

```python
def parse_arguments() -> argparse.Namespace
```

Feldolgozza a parancssori argumentumokat.

**Visszatérési érték:**

- Típus: `argparse.Namespace`
- A feldolgozott argumentumok névtere

### `main()`

```python
def main() -> None
```

A fő telepítési folyamat.

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`scripts/install.py`](../../scripts/install.py)
