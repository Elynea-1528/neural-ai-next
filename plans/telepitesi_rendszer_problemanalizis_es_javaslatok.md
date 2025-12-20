# Telepítési Rendszer - Problémaelemzés és Javaslatok

## Áttekintés

Ez a dokumentum részletesen elemzi a Neural AI Next projekt jelenlegi telepítési rendszerét, azonosítja a problémákat, és javaslatokat tesz a fejlesztésre.

## 1. Problémaelemzés

### 1.1 environment.yml vs pyproject.toml vs main.py

#### environment.yml (Conda környezet definíció)
**Előnyök:**
- Teljes környezet definíció egy fájlban
- Conda és pip függőségek együtt
- Verziók pontos megadása
- Könnyen reprodukálható környezet

**Problémák:**
- A `main.py` NEM használja az environment.yml-t
- Manuálisan hozza létre a környezetet parancsokkal
- Duplikáció a pyproject.toml-lel

#### pyproject.toml (Python projekt konfiguráció)
**Előnyök:**
- Modern Python projekt standard
- Függőségek jól definiálva
- Optional dependencies (dev, stb.)
- Build konfiguráció

**Problémák:**
- A `main.py` csak részben használja (`pip install -e .[dev]`)
- Nem használja ki az optional dependencies teljes potenciálját
- Verziók némelyike eltér az environment.yml-től

#### main.py (Interaktív telepítő)
**Problémák:**
1. **Nem használja az environment.yml-t**
   ```python
   # ROSSZ: Manuális parancsok
   run_command("conda create -n neural-ai-next python=3.12 -y")
   run_command("conda install pytorch==2.5.1 ...")

   # JÓ: environment.yml használata
   run_command("conda env create -f environment.yml")
   ```

2. **Conda init nem működik így**
   ```python
   # ROSSZ: Ez nem inicializálja a conda-t
   run_command("conda init")

   # JÓ: Conda init-et manuálisan kell futtatni a telepítés előtt
   # vagy a scriptnek ki kell írnia az utasítást
   ```

3. **Conda activate nem működik scriptből**
   ```python
   # ROSSZ: Ez nem fog működni
   run_command("conda activate neural-ai-next")

   # JÓ: A conda activate csak interaktív shellben működik
   # Scriptből a teljes conda útvonalat kell használni
   # vagy source activate parancsot
   ```

4. **Függőségek duplikálva vannak**
   - environment.yml: PyTorch CUDA 12.1
   - pyproject.toml: torch==2.5.1
   - main.py: újra definiálja a PyTorch telepítést

5. **Telepítési módok inkonzisztensek**
   ```python
   # Minimal: pip install -e .
   # Dev: pip install -e .[dev]
   # Dev+Trader: pip install -e .[dev] + broker script
   # Full: pip install -e .[dev] + jupyter + broker

   # Probléma: A pyproject.toml-ben nincs "trader" optional dependency
   # A broker script mindig külön fut
   ```

### 1.2 Conda Init és Activate Problémák

#### Conda Init
**Helyzet:**
- A `conda init` parancsot a `main.py` futtatja
- Ez NEM fogja inicializálni a felhasználó shelljét
- A conda init-et minden felhasználónak manuálisan kell futtatnia

**Helyes megoldás:**
```python
def check_conda():
    """Ellenőrzi, hogy conda telepítve és inicializálva van-e."""
    if not run_command("conda --version", check=False):
        print("✗ Conda nincs telepítve!")
        print("Kérlek telepítsd a Miniconda-t:")
        print("https://docs.conda.io/en/latest/miniconda.html")
        print("\nUtána futtasd:")
        print("conda init bash  # vagy conda init zsh")
        return False

    # Ellenőrizzük, hogy inicializálva van-e
    if not os.path.exists(os.path.expanduser("~/.bashrc")):
        # Nem létezik a conda init, ki kell írni
        print("⚠️  Conda nincs inicializálva!")
        print("Futtasd: conda init")
        return False

    return True
```

#### Conda Activate
**Probléma:**
```python
# EZ NEM MŰKÖDIK:
run_command("conda activate neural-ai-next")
run_command("pip install ...")
```

**Helyes megoldások:**

**1. Megoldás: Conda env parancs használata**
```python
# Minden parancsot a környezet nevével futtatunk
run_command("conda run -n neural-ai-next pip install ...")
```

**2. Megoldás: Teljes útvonal használata**
```python
# Megkeressük a conda környezet bin mappáját
conda_env_path = "~/miniconda3/envs/neural-ai-next/bin"
run_command(f"{conda_env_path}/pip install ...")
```

**3. Megoldás: Source parancs használata**
```python
# Bash script generálása és futtatása
script_content = """
source ~/miniconda3/etc/profile.d/conda.sh
conda activate neural-ai-next
pip install ...
"""
with open("/tmp/install.sh", "w") as f:
    f.write(script_content)
run_command("bash /tmp/install.sh")
```

### 1.3 Függőségkezelési Problémák

#### Verzióeltérések

| Komponens | environment.yml | pyproject.toml | main.py |
| --------- | --------------- | -------------- | ------- |
| Python    | 3.12.*          | >=3.12         | 3.12    |
| PyTorch   | 2.5.1           | 2.5.1          | 2.5.1   |
| NumPy     | 1.24.3          | >=1.24.3,<3.0  | -       |
| Pandas    | 2.0.3           | >=2.0.3,<3.0   | -       |
| Lightning | 2.5.5           | >=2.5.5        | -       |

**Probléma:** Az environment.yml fix verziókat ad meg, a pyproject.toml rugalmasabb. Ez konfliktushoz vezethet.

#### Optional Dependencies Hiánya

A pyproject.toml-ben csak `dev` optional dependency van, de a main.py több módot támogat:
- Minimal: alap függőségek
- Dev: alap + dev
- Dev+Trader: alap + dev + broker script
- Full: alap + dev + jupyter + broker script

**Javaslat:** Bővíteni a pyproject.toml-t:
```toml
[project.optional-dependencies]
dev = [
    "pytest-cov>=4.1.0",
    "isort>=5.13.2",
    # ... stb
]

trader = [
    "MetaTrader5",
    "jforex-api",
    # Broker specifikus függőségek
]

jupyter = [
    "jupyterlab>=4.0.0",
    "notebook",
    "ipykernel",
    "kaggle-api"
]

full = [
    ".[dev]",
    ".[trader]",
    ".[jupyter]"
]
```

### 1.4 Telepítési Módok Konzisztencia Problémái

#### Jelenlegi implementáció
```python
if install_mode == InstallMode.MINIMAL:
    run_command("pip install -e .")
elif install_mode == InstallMode.DEV:
    run_command("pip install -e .[dev]")
elif install_mode == InstallMode.DEV_TRADER:
    run_command("pip install -e .[dev]")
    run_command("bash scripts/install/scripts/setup_brokers.sh")
elif install_mode == InstallMode.FULL:
    run_command("pip install -e .[dev]")
    run_command("conda install -n neural-ai-next jupyterlab notebook -c conda-forge -y")
    run_command("bash scripts/install/scripts/setup_brokers.sh")
```

**Problémák:**
1. A DEV_TRADER és FULL is ugyanazt telepíti + extra lépések
2. A jupyter telepítése conda-val történik, nem pip-pel
3. A broker script mindig külön fut, nem integrálva

**Javaslat:**
```python
# Pyproject.toml bővítése
[project.optional-dependencies]
dev = [...]
trader = ["MetaTrader5", "jforex-api"]
jupyter = ["jupyterlab", "notebook", "ipykernel"]
full = [".[dev]", ".[trader]", ".[jupyter]"]

# Main.py egyszerűsítése
if install_mode == InstallMode.MINIMAL:
    run_command("pip install -e .")
elif install_mode == InstallMode.DEV:
    run_command("pip install -e .[dev]")
elif install_mode == InstallMode.DEV_TRADER:
    run_command("pip install -e .[dev,trader]")
    run_command("bash scripts/install/scripts/setup_brokers.sh")
elif install_mode == InstallMode.FULL:
    run_command("pip install -e .[full]")
    run_command("bash scripts/install/scripts/setup_brokers.sh")
```

## 2. Javaslatok

### 2.1 Egységesített Telepítő Rendszer

#### 2.1.1 Új main.py struktúra

```python
#!/usr/bin/env python3
"""
Neural AI Next - Egységesített Telepítő
"""

import argparse
import subprocess
import sys
import os
from pathlib import Path
from enum import Enum
from typing import Any, Dict, Optional

class InstallMode(Enum):
    MINIMAL = "minimal"
    DEV = "dev"
    DEV_TRADER = "dev+trader"
    FULL = "full"
    CHECK_ONLY = "check"

class PyTorchMode(Enum):
    CPU = "cpu"
    CUDA_12_1 = "cuda12.1"

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def print_error(message: str):
    print(f"{Colors.RED}✗ {message}{Colors.RESET}")

def print_success(message: str):
    print(f"{Colors.GREEN}✓ {message}{Colors.RESET}")

def print_warning(message: str):
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.RESET}")

def print_info(message: str):
    print(f"{Colors.BLUE}ℹ️  {message}{Colors.RESET}")

def run_command(command: str, check: bool = True, shell: bool = True) -> bool:
    """Futtat egy shell parancsot."""
    print(f"$ {command}")
    try:
        result = subprocess.run(
            command,
            shell=shell,
            check=check,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print_error(f"Parancs sikertelen: {e}")
        if e.stderr:
            print_error(f"Hiba: {e.stderr}")
        return False

def check_conda() -> bool:
    """Ellenőrzi, hogy conda telepítve van-e."""
    if not run_command("conda --version", check=False):
        print_error("Conda nincs telepítve!")
        print_info("Telepítsd a Miniconda-t:")
        print_info("https://docs.conda.io/en/latest/miniconda.html")
        print_info("\nUtána futtasd:")
        print_info("conda init bash  # vagy conda init zsh")
        return False
    print_success("Conda telepítve van")
    return True

def check_conda_initialized() -> bool:
    """Ellenőrzi, hogy conda inicializálva van-e."""
    # Ellenőrizzük, hogy a conda init megtörtént-e
    bashrc = Path.home() / ".bashrc"
    if bashrc.exists():
        with open(bashrc, 'r') as f:
            content = f.read()
            if "conda initialize" in content:
                print_success("Conda inicializálva van")
                return True

    print_warning("Conda nincs inicializálva!")
    print_info("Futtasd: conda init")
    return False

def check_environment() -> bool:
    """Ellenőrzi, hogy a környezet létezik-e."""
    try:
        result = subprocess.run(
            "conda env list",
            shell=True,
            capture_output=True,
            text=True
        )
        return "neural-ai-next" in result.stdout
    except:
        return False

def create_environment_yml(pytorch_mode: PyTorchMode) -> str:
    """Létrehozza az environment.yml-t a kívánt PyTorch mód szerint."""
    env_content = f"""name: neural-ai-next
channels:
  - pytorch
  - nvidia
  - conda-forge
  - defaults
dependencies:
  - python=3.12.*
  - pytorch=2.5.1
"""

    if pytorch_mode == PyTorchMode.CPU:
        env_content += "  - pytorch-cpu=2.5.1\n"
        env_content += "  - cpuonly\n"
    else:
        env_content += "  - pytorch-cuda=12.1\n"
        env_content += "  - cudatoolkit=12.1\n"

    env_content += """  - lightning=2.5.5
  - numpy=1.24.3
  - pandas=2.0.3
  - scikit-learn=1.3.0
  - pip:
      - -e .
      - vectorbt==0.25.0
      - pytest==7.4.0
      - black==23.7.0
      - flake8==6.1.0
      - mypy==1.5.0
      - pre-commit==3.4.0
      - fastapi==0.104.0
      - uvicorn==0.24.0
      - websockets==12.0
      - httpx==0.25.0
      - pydantic==2.4.0
      - python-multipart==0.0.6
      - pyyaml==6.0
      - packaging==23.1
      - fastparquet==2023.4.0
"""

    env_path = "/tmp/environment_neural_ai.yml"
    with open(env_path, 'w') as f:
        f.write(env_content)

    return env_path

def install_environment(config: Dict[str, Any]) -> bool:
    """Telepíti a környezetet a megadott konfiguráció szerint."""
    install_mode: InstallMode = config['install_mode']
    pytorch_mode: PyTorchMode = config['pytorch_mode']

    print_info("Telepítés megkezdése...")

    # 1. Conda ellenőrzés
    if not check_conda():
        return False

    if not check_conda_initialized():
        print_warning("Folytatás előtt inicializáld a conda-t!")
        return False

    # 2. Környezet ellenőrzése
    if check_environment():
        print_warning("A neural-ai-next környezet már létezik")
        response = input("Szeretnéd törölni és újra létrehozni? [y/N]: ").strip().lower()
        if response == 'y':
            print_info("Környezet törlése...")
            run_command("conda env remove -n neural-ai-next -y", check=False)
        else:
            print_info("Meglévő környezet használata...")
            return True

    # 3. Environment.yml létrehozása és használata
    print_info("Környezet létrehozása environment.yml-ből...")
    env_file = create_environment_yml(pytorch_mode)

    if not run_command(f"conda env create -f {env_file}"):
        print_error("Környezet létrehozása sikertelen!")
        return False

    print_success("Környezet létrehozva")

    # 4. Opcionális függőségek telepítése
    print_info("Opcionális függőségek telepítése...")

    if install_mode == InstallMode.MINIMAL:
        print_info("Minimal mód - nincs extra függőség")
    elif install_mode == InstallMode.DEV:
        if not run_command("conda run -n neural-ai-next pip install -e .[dev]"):
            print_error("Dev függőségek telepítése sikertelen!")
            return False
    elif install_mode == InstallMode.DEV_TRADER:
        if not run_command("conda run -n neural-ai-next pip install -e .[dev,trader]"):
            print_error("Dev+Trader függőségek telepítése sikertelen!")
            return False
        print_info("Broker telepítő indítása...")
        run_command("bash scripts/install/scripts/setup_brokers.sh")
    elif install_mode == InstallMode.FULL:
        if not run_command("conda run -n neural-ai-next pip install -e .[full]"):
            print_error("Full függőségek telepítése sikertelen!")
            return False
        print_info("Broker telepítő indítása...")
        run_command("bash scripts/install/scripts/setup_brokers.sh")

    # 5. Pre-commit beállítás
    if install_mode != InstallMode.MINIMAL:
        print_info("Pre-commit beállítása...")
        run_command("conda run -n neural-ai-next pre-commit install")

    # 6. Ellenőrzés
    print_info("Telepítés ellenőrzése...")
    run_command("conda run -n neural-ai-next python scripts/install/scripts/check_installation.py")

    return True

def interactive_setup() -> Optional[Dict[str, Any]]:
    """Interaktív telepítési menü."""
    print("=" * 60)
    print("Neural AI Next - Egységesített Telepítő")
    print("=" * 60)

    # 1. Telepítési mód választás
    print("\n1. Telepítési mód:")
    print("   [1] Minimal (csak alapok)")
    print("   [2] Fejlesztői környezet")
    print("   [3] Fejlesztői + Trader Engine")
    print("   [4] Teljes telepítés")
    print("   [5] Csak ellenőrzés")

    mode_choice = input("Válassz opciót [1-5] (alapértelmezett: 2): ").strip()
    mode_map = {
        "1": InstallMode.MINIMAL,
        "2": InstallMode.DEV,
        "3": InstallMode.DEV_TRADER,
        "4": InstallMode.FULL,
        "5": InstallMode.CHECK_ONLY
    }
    install_mode = mode_map.get(mode_choice, InstallMode.DEV)

    # 2. PyTorch mód
    print("\n2. PyTorch konfiguráció:")
    print("   [1] CUDA 12.1 (ajánlott GTX 1050 Ti-hez)")
    print("   [2] CPU only (laptopokhoz)")

    pytorch_choice = input("Válassz opciót [1-2] (alapértelmezett: 1): ").strip()
    pytorch_map = {
        "1": PyTorchMode.CUDA_12_1,
        "2": PyTorchMode.CPU
    }
    pytorch_mode = pytorch_map.get(pytorch_choice, PyTorchMode.CUDA_12_1)

    # 3. Megerősítés
    print("\n" + "=" * 60)
    print("Telepítési beállítások:")
    print(f"  - Mód: {install_mode.value}")
    print(f"  - PyTorch: {pytorch_mode.value}")
    print("=" * 60)

    confirm = input("\nFolytatod a telepítést? [y/N]: ").strip().lower()
    if confirm != 'y':
        print_info("Telepítés megszakítva.")
        return None

    return {
        'install_mode': install_mode,
        'pytorch_mode': pytorch_mode
    }

def main():
    """Fő belépési pont."""
    parser = argparse.ArgumentParser(description="Neural AI Next egységesített telepítő")
    parser.add_argument('--interactive', action='store_true', help='Interaktív mód')
    parser.add_argument('--mode', choices=['minimal', 'dev', 'dev+trader', 'full', 'check'])
    parser.add_argument('--pytorch', choices=['cpu', 'cuda12.1'])

    args = parser.parse_args()

    if args.interactive or (args.mode is None and args.pytorch is None):
        # Interaktív mód
        config_result = interactive_setup()
        if config_result is None:
            return
        success = install_environment(config_result)
    else:
        # Parancssori mód
        config: Dict[str, Any] = {
            'install_mode': InstallMode(args.mode or 'dev'),
            'pytorch_mode': PyTorchMode(args.pytorch or 'cuda12.1')
        }
        success = install_environment(config)

    if success:
        print_success("Telepítés sikeres!")
        print_info("\nKövetkező lépések:")
        print_info("1. Környezet aktiválása:")
        print_info("   conda activate neural-ai-next")
        print_info("\n2. Fejlesztés megkezdése:")
        print_info("   code .")
    else:
        print_error("Telepítés sikertelen!")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

### 2.2 Pyproject.toml bővítése

```toml
[project.optional-dependencies]
dev = [
    "pytest-cov>=4.1.0",
    "isort>=5.13.2",
    "pylint>=3.0.3",
    "bandit>=1.7.7",
    "ruff>=0.1.0",
    # Type stubs for Pylance
    "types-pyyaml>=6.0.0",
    "types-requests>=2.31.0",
    "types-python-dateutil>=2.8.0",
    "types-setuptools>=69.0.0",
    "types-pytz>=2023.3.0",
    "types-six>=1.16.0",
]

trader = [
    "MetaTrader5>=5.0.0",
    "jforex-api>=1.0.0",
    "python-socketio>=5.0.0",
]

jupyter = [
    "jupyterlab>=4.0.0",
    "notebook>=7.0.0",
    "ipykernel>=6.0.0",
    "kaggle-api>=1.0.0",
    "matplotlib>=3.5.0",
    "seaborn>=0.12.0",
]

full = [
    ".[dev]",
    ".[trader]",
    ".[jupyter]",
]
```

### 2.3 Environment.yml frissítése

```yaml
name: neural-ai-next
channels:
  - pytorch
  - nvidia
  - conda-forge
  - defaults
dependencies:
  - python=3.12.*
  - pytorch=2.5.1
  - pytorch-cuda=12.1  # vagy cpuonly
  - lightning=2.5.5
  - numpy=1.24.3
  - pandas=2.0.3
  - scikit-learn=1.3.0
  - cudatoolkit=12.1  # csak CUDA módban
  - pip:
      - -e .
      - vectorbt==0.25.0
      - pytest==7.4.0
      - black==23.7.0
      - flake8==6.1.0
      - mypy==1.5.0
      - pre-commit==3.4.0
      - fastapi==0.104.0
      - uvicorn==0.24.0
      - websockets==12.0
      - httpx==0.25.0
      - pydantic==2.4.0
      - python-multipart==0.0.6
      - pyyaml==6.0
      - packaging==23.1
      - fastparquet==2023.4.0
```

### 2.4 Telepítési Útmutató Frissítése

#### Conda Init Utasítás

```markdown
## Előkészületek

### 1. Conda telepítés

Ha még nincs conda telepítve:

```bash
# Töltsd le és telepítsd a Miniconda-t
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh

# Kövesd a telepítő utasításait
# Fogadd el a licenszt
# Válaszd az alapértelmezett telepítési útvonalat
```

### 2. Conda inicializálás

**FONTOS:** A conda inicializálása szükséges a környezet aktiválásához!

```bash
# Inicializáld a conda-t a shell-edben
conda init bash  # ha bash-t használsz
conda init zsh   # ha zsh-t használsz

# Indítsd újra a terminált vagy töltsd be a konfigurációt
source ~/.bashrc  # vagy source ~/.zshrc
```

### 3. Conda ellenőrzés

```bash
conda --version
# Eredmény: conda 24.x.x vagy hasonló
```

## Telepítés

Most már készen állsz a Neural AI Next telepítésére!
```

## 3. Összefoglalás

### 3.1 Főbb változtatások

1. **Egységesített telepítő:** A main.py most már az environment.yml-t használja
2. **Helyes conda kezelés:** Conda init és activate problémák megoldva
3. **Bővített pyproject.toml:** Új optional dependencies (trader, jupyter, full)
4. **Konzisztens verziók:** Minden konfigurációban ugyanazok a verziók
5. **Jobb hibakezelés:** Színes kimenet, részletes hibajelentés

### 3.2 Előnyök

- **Reprodukálható:** Az environment.yml garantálja a reprodukálhatóságot
- **Rugalmas:** A pyproject.toml optional dependencies rugalmasságot ad
- **Hibamentes:** A conda run paranccsal nincs activate probléma
- **Átlátható:** Színes kimenet, részletes információk
- **Karbantartható:** Könnyű bővíteni új függőségekkel

### 3.3 Használat

```bash
# Interaktív telepítés
python scripts/install/scripts/main.py --interactive

# Gyors telepítés
python scripts/install/scripts/main.py --mode dev+trader --pytorch cuda12.1

# Minimal telepítés
python scripts/install/scripts/main.py --mode minimal --pytorch cpu
```

## 4. Következő Lépések

1. **Pyproject.toml frissítése:** Add hozzá az új optional dependencies-t
2. **Main.py implementálása:** Implementáld az új egységesített telepítőt
3. **Dokumentáció frissítése:** Frissítsd a telepítési útmutatókat
4. **Tesztelés:** Teszteld minden telepítési módot
5. **Migráció:** Migráld az esetleges meglévő környezeteket

## 5. Alternatívák

Ha a fenti megoldás túl komplex, egyszerűbb alternatíva:

### 5.1 Egyszerűbb megoldás

```python
def install_environment(config):
    """Egyszerűsített telepítő."""
    pytorch_mode = config['pytorch_mode']

    # 1. Conda környezet létrehozása
    if pytorch_mode == PyTorchMode.CPU:
        run_command("conda create -n neural-ai-next python=3.12 pytorch=2.5.1 cpuonly -c pytorch -y")
    else:
        run_command("conda create -n neural-ai-next python=3.12 pytorch=2.5.1 pytorch-cuda=12.1 -c pytorch -c nvidia -y")

    # 2. Függőségek telepítése
    run_command("conda run -n neural-ai-next pip install -e .")

    # 3. Opcionális függőségek
    install_mode = config['install_mode']
    if install_mode in [InstallMode.DEV, InstallMode.DEV_TRADER, InstallMode.FULL]:
        run_command("conda run -n neural-ai-next pip install -e .[dev]")

    # 4. Broker telepítés
    if install_mode in [InstallMode.DEV_TRADER, InstallMode.FULL]:
        run_command("bash scripts/install/scripts/setup_brokers.sh")
```

Ez a megoldás egyszerűbb, de kevésbé reprodukálható, mert nem használja az environment.yml-t.
