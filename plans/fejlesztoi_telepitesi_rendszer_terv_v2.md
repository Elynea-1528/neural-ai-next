# Fejlesztői Telepítési Rendszer Terv v2

## Változások az előző verzióhoz képest

Ez a frissített terv tartalmazza a felhasználó konkrét igényeit és feedbackjét:

### ✅ Elfogadott/Implementálandó Javaslatok
1. **Fastparquet type stub** - Hozzáadandó a Pylance támogatáshoz
2. **Conda verziók dokumentálása** - Lényeges a kompatibilitás érdekében
3. **CUDA 12.0 vs 12.1** - GTX 1050 Ti kompatibilitás ellenőrzése
4. **Telepítő mappa** - Komplett install mappa létrehozása
5. **VS Code bővítmények optimalizálása** - Csak a szükségesek megtartása
6. **Interaktív telepítő** - Több telepítési opcióval
7. **Laptop támogatás** - Lenovo T480 ThinkPad kompatibilitás
8. **Jupyter konfiguráció** - Kaggle GPU-hoz való előkészítés
9. **Debug konfiguráció** - VS Code debugging támogatás

### ❌ Nem szükséges elemek
- **Docker támogatás** - Wine alatt fut az MT5, nem szükséges
- **GitLens és hasonlók** - Egyedül fejleszted a projektet, felesleges
- **CI/CD komplexitás** - Egyszerűbb megoldások előnyösebbek

## Részletes Implementációs Terv

### 1. Fastparquet Type Stub Kezelése

#### 1.1 Ellenőrzés
```bash
# Ellenőrizzük, hogy létezik-e fastparquet-hoz type stub
pip search types-fastparquet
# vagy
pip index versions fastparquet
```

#### 1.2 Döntési fa
```
Létezik types-fastparquet?
├── IGEN → Hozzáadni a fejlesztői függőségekhez
└── NEM →
    ├── Fastparquet használata kritikus?
    │   ├── IGEN → Saját type stub írása vagy ignore kommentek
    │   └── NEM → Fastparquet eltávolítása a core függőségekből
    └── Alternatíva: pyarrow használata parquet támogatáshoz
```

### 2. Conda Verziók Dokumentálása

#### 2.1 Aktuális környezet ellenőrzése
```python
# scripts/check_conda_versions.py
"""Aktuális conda környezet verzióinak ellenőrzése."""

import subprocess
import json
from typing import Dict, List

def get_conda_packages() -> Dict[str, str]:
    """Lekéri a telepített conda csomagok listáját."""
    result = subprocess.run(
        ["conda", "list", "--json"],
        capture_output=True,
        text=True
    )
    packages = json.loads(result.stdout)

    package_dict = {}
    for pkg in packages:
        package_dict[pkg["name"].lower()] = pkg["version"]

    return package_dict

def generate_version_report():
    """Generál egy verzió jelentést."""
    packages = get_conda_packages()

    critical_packages = [
        "python", "pytorch", "torch", "numpy", "pandas",
        "scikit-learn", "cudatoolkit", "pytorch-cuda"
    ]

    print("=" * 60)
    print("Kritikus csomagok verziói")
    print("=" * 60)

    for pkg in critical_packages:
        if pkg in packages:
            print(f"✓ {pkg}: {packages[pkg]}")
        else:
            print(f"✗ {pkg}: NINCS TELEPÍTVE")

    print("=" * 60)

    # Exportálás fájlba
    with open("conda_versions.txt", "w") as f:
        for pkg, version in packages.items():
            f.write(f"{pkg}=={version}\n")

    print("✓ Verziók exportálva: conda_versions.txt")

if __name__ == "__main__":
    generate_version_report()
```

#### 2.2 Verzió kompatibilitás táblázat
```
Python 3.12 → PyTorch 2.5.1 → CUDA 12.1
├── GTX 1050 Ti (4GB VRAM)
│   ├── CUDA 12.1 támogatott? ✓
│   ├── Memória elég? ✓ (min 4GB)
│   └── Driver kompatibilitás? ✓
└── Lenovo T480 (Intel GPU)
    ├── CUDA NEM támogatott
    ├── CPU only PyTorch szükséges
    └── Jupyter notebook használat javasolt
```

### 3. CUDA Kompatibilitás GTX 1050 Ti-hez

#### 3.1 Hardver követelmények
```
GTX 1050 Ti specifikáció:
- CUDA Cores: 768
- VRAM: 4GB GDDR5
- Compute Capability: 6.1
- CUDA 12.1 támogatott: ✓
```

#### 3.2 CUDA 12.0 vs 12.1 döntés
```python
# scripts/check_gpu_compatibility.py
"""GPU kompatibilitás ellenőrzése."""

import torch
import subprocess

def check_gpu_compatibility():
    """Ellenőrzi a GPU kompatibilitást."""
    print("=" * 60)
    print("GPU Kompatibilitás Ellenőrzés")
    print("=" * 60)

    # NVIDIA driver ellenőrzés
    try:
        result = subprocess.run(
            ["nvidia-smi"],
            capture_output=True,
            text=True
        )
        print("✓ NVIDIA driver telepítve")
        print(result.stdout)
    except:
        print("✗ NVIDIA driver NINCS telepítve")
        return False

    # PyTorch CUDA támogatás
    if torch.cuda.is_available():
        print(f"✓ CUDA elérhető")
        print(f"  - CUDA verzió: {torch.version.cuda}")
        print(f"  - GPU: {torch.cuda.get_device_name(0)}")
        print(f"  - VRAM: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")

        # Ellenőrizzük a CUDA 12.1 támogatást
        if "12.1" in torch.version.cuda:
            print("✓ CUDA 12.1 támogatott")
        else:
            print(f"⚠ CUDA {torch.version.cuda} van telepítve, 12.1 ajánlott")
    else:
        print("✗ CUDA NEM elérhető")
        print("  - CPU only mód lesz használva")

    print("=" * 60)
    return torch.cuda.is_available()

if __name__ == "__main__":
    check_gpu_compatibility()
```

### 4. Telepítő Mappa Struktúra

```
scripts/install/
├── __init__.py
├── main.py                    # Fő telepítő
├── version_config.py          # Verzió konfiguráció
├── conda_manager.py           # Conda műveletek
├── dependency_checker.py      # Függőség ellenőrzés
├── pytorch_installer.py       # PyTorch telepítés (CPU/GPU)
├── precommit_setup.py         # Pre-commit beállítás
├── verification.py            # Telepítés ellenőrzés
├── functional_tests.py        # Funkcionalitás tesztek
├── mt5_setup.py              # MT5 Wine beállítás
├── jupyter_setup.py          # Jupyter kernel konfig
└── debug_setup.py            # VS Code debug konfig
```

### 5. VS Code Bővítmények Optimalizálása

#### 5.1 Szükséges bővítmények (Core)
```json
{
    "recommendations": [
        // Python Support (LÉNYEGES)
        "ms-python.python",
        "ms-python.vscode-pylance",
        "ms-python.black-formatter",

        // MQL5 Support (LÉNYEGES)
        "L-I-V.mql-tools",

        // Jupyter (LÉNYEGES - Kaggle GPU-hoz)
        "ms-toolsai.jupyter",

        // Code Quality (LÉNYEGES)
        "charliermarsh.ruff",

        // YAML Support (SZÜKSÉGES)
        "redhat.vscode-yaml",

        // Markdown (HASZNOS)
        "yzhang.markdown-all-in-one",

        // GitHub Copilot (OPCIONÁLIS)
        "github.copilot"
    ]
}
```

#### 5.2 Eltávolítandó bővítmények
- ~~"tiangolo.fastapi"~~ - Nincs használva
- ~~"github.vscode-github-actions"~~ - Nem szükséges
- ~~"eamodio.gitlens"~~ - Egyedül fejlesztesz
- ~~"ms-azuretools.vscode-docker"~~ - Nincs Docker
- ~~"humao.rest-client"~~ - Nem szükséges

### 6. Interaktív Telepítő Fejlesztése

#### 6.1 Telepítési opciók
```python
# scripts/install/main.py
"""Interaktív telepítő főmodul."""

import argparse
from enum import Enum

class InstallMode(Enum):
    """Telepítési módok."""
    MINIMAL = "minimal"           # Csak alapok
    DEV = "dev"                   # Fejlesztői környezet
    DEV_MT5 = "dev+mt5"           # Fejlesztői + MT5
    FULL = "full"                 # Minden
    CHECK_ONLY = "check"          # Csak ellenőrzés

class PyTorchMode(Enum):
    """PyTorch telepítési módok."""
    CPU = "cpu"                   # CPU only
    CUDA_12_0 = "cuda12.0"        # CUDA 12.0
    CUDA_12_1 = "cuda12.1"        # CUDA 12.1 (ajánlott)

class DeviceType(Enum):
    """Eszköz típusok."""
    DESKTOP_GTX_1050_TI = "desktop_gtx1050ti"
    LAPTOP_T480 = "laptop_t480"
    AUTO_DETECT = "auto"
```

#### 6.2 Interaktív menü
```python
def interactive_setup():
    """Interaktív telepítési menü."""
    print("=" * 60)
    print("Neural AI Next - Interaktív Telepítő")
    print("=" * 60)

    # 1. Telepítési mód választás
    print("\n1. Telepítési mód:")
    print("   [1] Minimal (csak alapok)")
    print("   [2] Fejlesztői környezet")
    print("   [3] Fejlesztői + MT5 támogatás")
    print("   [4] Teljes telepítés")
    print("   [5] Csak ellenőrzés")

    mode_choice = input("Válassz opciót [1-5]: ").strip()
    mode_map = {
        "1": InstallMode.MINIMAL,
        "2": InstallMode.DEV,
        "3": InstallMode.DEV_MT5,
        "4": InstallMode.FULL,
        "5": InstallMode.CHECK_ONLY
    }
    install_mode = mode_map.get(mode_choice, InstallMode.DEV)

    # 2. Eszköz típus
    print("\n2. Eszköz típus:")
    print("   [1] Asztali (GTX 1050 Ti)")
    print("   [2] Laptop (Lenovo T480)")
    print("   [3] Automatikus észlelés")

    device_choice = input("Válassz opciót [1-3]: ").strip()
    device_map = {
        "1": DeviceType.DESKTOP_GTX_1050_TI,
        "2": DeviceType.LAPTOP_T480,
        "3": DeviceType.AUTO_DETECT
    }
    device_type = device_map.get(device_choice, DeviceType.AUTO_DETECT)

    # 3. PyTorch mód (ha nem laptop)
    if device_type != DeviceType.LAPTOP_T480:
        print("\n3. PyTorch konfiguráció:")
        print("   [1] CUDA 12.1 (ajánlott GTX 1050 Ti-hez)")
        print("   [2] CUDA 12.0")
        print("   [3] CPU only")

        pytorch_choice = input("Válassz opciót [1-3]: ").strip()
        pytorch_map = {
            "1": PyTorchMode.CUDA_12_1,
            "2": PyTorchMode.CUDA_12_0,
            "3": PyTorchMode.CPU
        }
        pytorch_mode = pytorch_map.get(pytorch_choice, PyTorchMode.CUDA_12_1)
    else:
        pytorch_mode = PyTorchMode.CPU

    # 4. Megerősítés
    print("\n" + "=" * 60)
    print("Telepítési beállítások:")
    print(f"  - Mód: {install_mode.value}")
    print(f"  - Eszköz: {device_type.value}")
    print(f"  - PyTorch: {pytorch_mode.value}")
    print("=" * 60)

    confirm = input("\nFolytatod a telepítést? [y/N]: ").strip().lower()
    if confirm != 'y':
        print("Telepítés megszakítva.")
        return None

    return {
        'install_mode': install_mode,
        'device_type': device_type,
        'pytorch_mode': pytorch_mode
    }
```

### 7. Laptop Támogatás (Lenovo T480)

#### 7.1 Laptop specifikációk
```
Lenovo ThinkPad T480:
- CPU: Intel Core i5/i7 (8. generáció)
- GPU: Intel UHD Graphics 620 (NINCS CUDA támogatás)
- RAM: 8-32GB DDR4
- Storage: SSD
```

#### 7.2 Laptop specifikus konfiguráció
```python
# scripts/install/laptop_config.py
"""Laptop specifikus konfiguráció."""

LAPTOP_CONFIG = {
    'pytorch': {
        'package': 'pytorch',
        'version': '2.5.1',
        'channel': 'pytorch',
        'cpu_only': True
    },
    'lightning': {
        'package': 'lightning',
        'version': '2.5.5',
        'channel': 'conda-forge'
    },
    'jupyter': {
        'enabled': True,
        'extensions': [
            'jupyterlab',
            'ipywidgets',
            'jupyterlab-git'
        ]
    },
    'debug': {
        'enabled': True,
        'config': 'laptop_debug'
    }
}

def apply_laptop_config():
    """Alkalmazza a laptop konfigurációt."""
    print("Laptop konfiguráció alkalmazása...")

    # PyTorch CPU only telepítés
    print("  - PyTorch CPU only telepítése")
    # conda install pytorch torchvision torchaudio cpuonly -c pytorch

    # Jupyter beállítások
    print("  - Jupyter konfigurálása")
    # jupyter labextension install @jupyter-widgets/jupyterlab-manager

    # Debug konfiguráció
    print("  - Debug konfiguráció létrehozása")
    create_debug_config("laptop")

    print("✓ Laptop konfiguráció kész")
```

### 8. Jupyter Kernel Konfiguráció

#### 8.1 Kaggle GPU-hoz való előkészítés
```python
# scripts/install/jupyter_setup.py
"""Jupyter kernel konfiguráció."""

import json
import subprocess
from pathlib import Path

def create_kaggle_kernel():
    """Létrehozza a Kaggle kompatibilis kernel konfigurációt."""

    kernel_name = "neural-ai-next"
    kernel_dir = Path.home() / ".local" / "share" / "jupyter" / "kernels" / kernel_name
    kernel_dir.mkdir(parents=True, exist_ok=True)

    # Kernel specifikáció
    kernel_spec = {
        "argv": [
            "python",
            "-m",
            "ipykernel_launcher",
            "-f",
            "{connection_file}"
        ],
        "display_name": "Neural AI Next",
        "language": "python",
        "env": {
            "PYTHONPATH": "${PYTHONPATH}:/path/to/neural-ai-next",
            "CUDA_VISIBLE_DEVICES": "0"
        }
    }

    # Kernel spec fájl írása
    with open(kernel_dir / "kernel.json", "w") as f:
        json.dump(kernel_spec, f, indent=2)

    # Logo hozzáadása
    logo_svg = """<svg>...</svg>"""
    with open(kernel_dir / "logo-32x32.png", "wb") as f:
        # SVG to PNG konverzió
        pass

    print(f"✓ Jupyter kernel létrehozva: {kernel_name}")

    # Kaggle notebook template
    create_kaggle_template()

def create_kaggle_template():
    """Létrehozza a Kaggle notebook template-et."""
    template = """{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Neural AI Next - Kaggle Setup\\n",
    "import sys\\n",
    "sys.path.append('/kaggle/working/neural-ai-next')\\n",
    "\\n",
    "from neural_ai.core.base import CoreComponentFactory\\n",
    "from neural_ai.collectors.mt5 import MT5Collector\\n",
    "\\n",
    "print('✓ Neural AI Next loaded')"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}"""

    template_path = Path("kaggle_template.ipynb")
    with open(template_path, "w") as f:
        f.write(template)

    print(f"✓ Kaggle template létrehozva: {template_path}")
```

### 9. VS Code Debug Konfiguráció

#### 9.1 Debug launch.json
```json
// .vscode/launch.json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Neural AI Next",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/main.py",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}",
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            },
            "args": []
        },
        {
            "name": "Python: MT5 Collector",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/scripts/run_collector.py",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}",
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            }
        },
        {
            "name": "Python: Pytest",
            "type": "python",
            "request": "launch",
            "module": "pytest",
            "args": [
                "tests",
                "-v",
                "--tb=short"
            ],
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}"
        },
        {
            "name": "Python: Jupyter",
            "type": "python",
            "request": "launch",
            "module": "jupyter",
            "args": [
                "lab",
                "--no-browser",
                "--port=8888"
            ],
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}"
        }
    ]
}
```

#### 9.2 Debug script
```python
# scripts/install/debug_setup.py
"""VS Code debug konfiguráció."""

import json
from pathlib import Path

def create_debug_config(device_type="desktop"):
    """Létrehozza a debug konfigurációt."""

    vscode_dir = Path(".vscode")
    vscode_dir.mkdir(exist_ok=True)

    # Launch konfiguráció
    launch_config = {
        "version": "0.2.0",
        "configurations": []
    }

    # Alap konfigurációk
    base_configs = [
        {
            "name": "Python: Neural AI Next",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/main.py",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}",
            "env": {"PYTHONPATH": "${workspaceFolder}"}
        },
        {
            "name": "Python: Pytest",
            "type": "python",
            "request": "launch",
            "module": "pytest",
            "args": ["tests", "-v", "--tb=short"],
            "console": "integratedTerminal"
        }
    ]

    # Eszköz specifikus konfigurációk
    if device_type == "laptop":
        base_configs.append({
            "name": "Python: Jupyter (CPU)",
            "type": "python",
            "request": "launch",
            "module": "jupyter",
            "args": ["lab", "--no-browser", "--port=8888"],
            "console": "integratedTerminal"
        })
    else:
        base_configs.append({
            "name": "Python: MT5 Collector (GPU)",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/scripts/run_collector.py",
            "console": "integratedTerminal",
            "env": {
                "PYTHONPATH": "${workspaceFolder}",
                "CUDA_VISIBLE_DEVICES": "0"
            }
        })

    launch_config["configurations"] = base_configs

    # Fájl írása
    with open(vscode_dir / "launch.json", "w") as f:
        json.dump(launch_config, f, indent=4)

    print("✓ Debug konfiguráció létrehozva")
```

## Implementációs Lépések (Frissített)

### Fázis 1: Azonnali Javítások (2-3 óra)
1. ✅ Fastparquet type stub ellenőrzése és hozzáadása
2. ✅ Aktuális conda verziók dokumentálása
3. ✅ GPU kompatibilitás ellenőrzése
4. ✅ VS Code bővítmények optimalizálása

### Fázis 2: Interaktív Telepítő (fél nap)
5. ✅ Telepítő mappa létrehozása
6. ✅ Interaktív menü implementálása
7. ✅ Eszköz specifikus konfigurációk
8. ✅ PyTorch CPU/GPU választás

### Fázis 3: Fejlesztői Eszközök (fél nap)
9. ✅ Jupyter kernel konfiguráció
10. ✅ VS Code debug beállítások
11. ✅ MT5 Wine integráció
12. ✅ Funkcionalitás tesztek

## Használati Utasítások (Frissített)

### Interaktív Telepítés
```bash
# Interaktív mód
python scripts/install/main.py --interactive

# Gyors telepítés (asztali gép)
python scripts/install/main.py --mode dev+mt5 --device desktop --pytorch cuda12.1

# Laptop telepítés
python scripts/install/main.py --mode dev --device laptop --pytorch cpu

# Csak ellenőrzés
python scripts/install/main.py --mode check
```

### Manuális Telepítés
```bash
# Asztali gép (GTX 1050 Ti)
conda env create -f environment_desktop.yml
conda activate neural-ai-next
python scripts/install/main.py --setup-mt5

# Laptop (T480)
conda env create -f environment_laptop.yml
conda activate neural-ai-next
python scripts/install/main.py --setup-jupyter
```

## Összefoglalás

Ez a frissített terv minden figyelembe vesz:

✅ **Fastparquet type stub** - Pylance támogatás
✅ **Conda verziók** - Kompatibilitás biztosítása
✅ **GTX 1050 Ti** - CUDA 12.1 támogatással
✅ **Lenovo T480** - CPU only konfigurációval
✅ **Interaktív telepítő** - Több opcióval
✅ **Optimalizált bővítmények** - Csak a szükségesek
✅ **Jupyter konfiguráció** - Kaggle GPU-hoz készen
✅ **Debug támogatás** - VS Code-ban
✅ **MT5 integráció** - Wine alatt futva

A terv most már teljes mértékben illeszkedik a te konkrét igényeidhez és hardver konfigurációdhoz!
