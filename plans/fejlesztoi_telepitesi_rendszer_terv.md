# Fejlesztői Telepítési Rendszer Fejlesztési Terv

## Áttekintés

Ez a dokumentum a Neural AI Next projekt fejlesztői telepítési rendszerének átfogó fejlesztési tervét tartalmazza. A cél egy robusztus, egyszerűen használható és teljes körű fejlesztői környezet biztosítása, amely támogatja a modern Python fejlesztést type checkingkel, code quality eszközökkel és automatikus ellenőrzésekkel.

## Aktuális Állapot Elemzése

### Erősségek
- ✅ Teljes körű `pyproject.toml` konfiguráció
- ✅ Conda `environment.yml` CUDA támogatással
- ✅ Kifogástalan VS Code beállítások
- ✅ Szilárd pre-commit konfiguráció
- ✅ Automatikus telepítő script

### Gyengeségek és Hiányosságok
- ❌ Verzió konfliktusok a konfigurációs fájlok között
- ❌ Hiányoznak a type stub csomagok (types-*)
- ❌ Nincs Ruff code quality eszköz
- ❌ A telepítő script monolitikus (238 sor)
- ❌ Az ellenőrző script statikus, nem dinamikus
- ❌ Nincs funkcionalitás teszt
- ❌ Nincs fejlesztői mód támogatás

## Célok és Prioritások

### 1. Közvetlen Célok (azonnali)
1. **Type stub csomagok hozzáadása** - Pylance támogatás
2. **Ruff integrálása** - Modern code quality eszköz
3. **Verzió konfliktusok feloldása** - Konzisztens függőség kezelés

### 2. Középtávú Célok (1-2 nap)
4. **Telepítő modularizálása** - Jobb karbantarthatóság
5. **Okosabb ellenőrzés** - Dinamikus függőség ellenőrzés
6. **Funkcionalitás tesztek** - Alapvető működés ellenőrzése

### 3. Hosszútávú Célok (jövőbeli)
7. **Telepítési módok** - minimal/full/check-only
8. **CI/CD támogatás** - Non-interactive mód
9. **Dokumentáció fejlesztés** - Részletes telepítési útmutató

## Részletes Implementációs Terv

### 1. Type Stub Csomagok Hozzáadása

#### 1.1 pyproject.toml frissítése
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
```

#### 1.2 environment.yml frissítése
```yaml
dependencies:
  - python=3.12.*
  - pytorch=2.5.1
  - pytorch-cuda=12.1
  - lightning=2.5.5
  - numpy=1.24.3
  - pandas=2.0.3
  - scikit-learn=1.3.0
  - cudatoolkit=12.1
  - pip:
      - -e .
      - vectorbt==0.25.0
      - jupyterlab==4.0.0
      - pytest==7.4.0
      - black==23.7.0
      - flake8==6.1.0
      - mypy==1.5.0
      - ruff==0.1.0
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
      # Type stubs
      - types-pyyaml>=6.0.0
      - types-requests>=2.31.0
      - types-python-dateutil>=2.8.0
      - types-setuptools>=69.0.0
      - types-pytz>=2023.3.0
      - types-six>=1.16.0
```

### 2. Ruff Integráció

#### 2.1 Ruff hozzáadása a fejlesztői eszközökhöz
```toml
# pyproject.toml
[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "C",   # flake8-comprehensions
    "B",   # flake8-bugbear
    "N",   # pep8-naming
]

[tool.ruff.lint.isort]
known-first-party = ["neural_ai"]

[tool.ruff.lint.flake8-quotes]
inline-quotes = "single"
```

#### 2.2 Pre-commit frissítése
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.0
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format
```

#### 2.3 VS Code beállítások frissítése
```json
{
    "python.linting.ruffEnabled": true,
    "python.formatting.provider": "none",
    "python.formatting.blackArgs": [],
    "[python]": {
        "editor.defaultFormatter": "charliermarsh.ruff",
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
            "source.organizeImports": "explicit",
            "source.fixAll": "explicit"
        }
    }
}
```

### 3. Verzió Konfliktusok Feloldása

#### 3.1 Központi verzió konfiguráció létrehozása
```python
# scripts/install/version_config.py
"""Központi verzió konfiguráció a projekt számára."""

PROJECT_VERSION = "1.0.0"
PYTHON_VERSION = "3.12"

# Core dependencies
CORE_DEPENDENCIES = {
    "torch": "2.5.1",
    "lightning": "2.5.5",
    "numpy": "1.24.3",
    "pandas": "2.0.3",
    "scikit-learn": "1.3.0",
    "vectorbt": "0.25.0",
    "jupyterlab": "4.0.0",
    "pytest": "7.4.0",
    "black": "23.7.0",
    "flake8": "6.1.0",
    "mypy": "1.5.0",
    "ruff": "0.1.0",
    "pre-commit": "3.4.0",
    "fastapi": "0.104.0",
    "uvicorn": "0.24.0",
    "websockets": "12.0",
    "httpx": "0.25.0",
    "pydantic": "2.4.0",
    "python-multipart": "0.0.6",
    "pyyaml": "6.0",
    "packaging": "23.1",
    "fastparquet": "2023.4.0",
}

# Type stub dependencies
TYPE_STUBS = {
    "types-pyyaml": "6.0.0",
    "types-requests": "2.31.0",
    "types-python-dateutil": "2.8.0",
    "types-setuptools": "69.0.0",
    "types-pytz": "2023.3.0",
    "types-six": "1.16.0",
}

# Development tools
DEV_DEPENDENCIES = {
    "pytest-cov": "4.1.0",
    "isort": "5.13.2",
    "pylint": "3.0.3",
    "bandit": "1.7.7",
}
```

#### 3.2 Konfigurációs fájlok generálása
```python
# scripts/install/generate_configs.py
"""Automatikus konfiguráció generálás a központi verziókból."""

from version_config import CORE_DEPENDENCIES, TYPE_STUBS, DEV_DEPENDENCIES

def generate_pyproject_dependencies():
    """Generálja a pyproject.toml függőségeket."""
    deps = []
    for package, version in CORE_DEPENDENCIES.items():
        deps.append(f'{package}=={version}')
    return deps

def generate_environment_yml():
    """Generálja az environment.yml tartalmát."""
    # Hasonlóan implementálva
    pass
```

### 4. Telepítő Modularizálása

#### 4.1 Új modul struktúra
```
scripts/install/
├── __init__.py
├── main.py                    # Fő telepítő
├── version_config.py          # Verzió konfiguráció
├── conda_manager.py           # Conda műveletek
├── dependency_checker.py      # Függőség ellenőrzés
├── pytorch_installer.py       # PyTorch specifikus
├── precommit_setup.py         # Pre-commit beállítás
├── verification.py            # Telepítés ellenőrzés
└── functional_tests.py        # Funkcionalitás tesztek
```

#### 4.2 Fő telepítő (main.py)
```python
#!/usr/bin/env python3
"""Neural AI Next - Moduláris telepítő script."""

import argparse
import sys
from pathlib import Path

from conda_manager import CondaManager
from dependency_checker import DependencyChecker
from pytorch_installer import PyTorchInstaller
from precommit_setup import PrecommitSetup
from verification import Verification
from functional_tests import FunctionalTests


class Installer:
    """Fő telepítő osztály."""

    def __init__(self, mode='full', non_interactive=False):
        self.mode = mode
        self.non_interactive = non_interactive
        self.conda = CondaManager()
        self.deps = DependencyChecker()
        self.pytorch = PyTorchInstaller()
        self.precommit = PrecommitSetup()
        self.verify = Verification()
        self.tests = FunctionalTests()

    def run(self):
        """Futtatja a telepítési folyamatot."""
        try:
            self.conda.check_and_create_environment()
            self.pytorch.install()
            self.precommit.setup()
            self.verify.check_installation()
            self.tests.run_basic_tests()
            return True
        except Exception as e:
            print(f"✗ Telepítés sikertelen: {e}")
            return False


def main():
    """Fő belépési pont."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['minimal', 'full', 'check-only'])
    parser.add_argument('--non-interactive', action='store_true')
    args = parser.parse_args()

    installer = Installer(mode=args.mode, non_interactive=args.non_interactive)
    success = installer.run()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
```

### 5. Okosabb Ellenőrző Script

#### 5.1 Dinamikus ellenőrzés
```python
# scripts/check_installation.py
#!/usr/bin/env python3
"""Okos telepítési ellenőrző script."""

import json
import sys
import toml
from typing import Dict, List, Tuple

import torch
from packaging import version as pkg_version


class InstallationChecker:
    """Telepítés ellenőrző osztály."""

    def __init__(self):
        self.expected_deps = self._load_expected_dependencies()
        self.results = []

    def _load_expected_dependencies(self) -> Dict[str, str]:
        """Betölti a várt függőségeket pyproject.toml-ből."""
        with open("pyproject.toml") as f:
            config = toml.load(f)

        deps = {}
        for dep in config["project"]["dependencies"]:
            parts = dep.split("==")
            if len(parts) == 2:
                deps[parts[0]] = parts[1]
        return deps

    def check_package(self, package_name: str, min_version: str = None) -> Tuple[bool, str]:
        """Ellenőrzi egy csomag telepítését."""
        try:
            module = __import__(package_name.replace("-", "_"))
            version = getattr(module, "__version__", "unknown")

            if min_version and version != "unknown":
                if pkg_version.parse(version) < pkg_version.parse(min_version):
                    return False, f"{package_name} {version} (minimum {min_version})"

            return True, f"{package_name} {version}"
        except ImportError:
            return False, f"{package_name} nincs telepítve"

    def check_cuda(self) -> Tuple[bool, str]:
        """Ellenőrzi a CUDA telepítést."""
        try:
            if not torch.cuda.is_available():
                return False, "CUDA nem elérhető"

            device_name = torch.cuda.get_device_name(0)
            cuda_version = torch.version.cuda
            cudnn_version = torch.backends.cudnn.version()

            # Teszteljük a CUDA működését
            x = torch.randn(100, 100).cuda()
            y = torch.randn(100, 100).cuda()
            z = torch.matmul(x, y)

            return True, f"CUDA: {device_name}, verzió: {cuda_version}, cuDNN: {cudnn_version}"
        except Exception as e:
            return False, f"CUDA ellenőrzés sikertelen: {str(e)}"

    def generate_report(self, format: str = "text") -> str:
        """Generálja a jelentést."""
        if format == "json":
            return json.dumps(self.results, indent=2)

        # Szöveges formázás
        lines = ["=" * 60, "Neural AI Next - Telepítési Ellenőrzés", "=" * 60]
        for status, message in self.results:
            symbol = "✓" if status else "✗"
            lines.append(f"{symbol} {message}")
        lines.append("=" * 60)
        return "\n".join(lines)

    def run_checks(self) -> bool:
        """Futtatja az összes ellenőrzést."""
        # Core dependencies
        for package, expected_version in self.expected_deps.items():
            ok, message = self.check_package(package, expected_version)
            self.results.append((ok, message))

        # CUDA
        cuda_ok, cuda_msg = self.check_cuda()
        self.results.append((cuda_ok, cuda_msg))

        return all(status for status, _ in self.results)


def main():
    """Fő ellenőrzési funkció."""
    checker = InstallationChecker()
    all_ok = checker.run_checks()

    print(checker.generate_report())

    if all_ok:
        print("\n✓ Minden ellenőrzés sikeres!")
        return 0
    else:
        print("\n✗ Néhány ellenőrzés sikertelen!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
```

### 6. Funkcionalitás Tesztek

#### 6.1 Alapvető funkcionalitás ellenőrzés
```python
# scripts/install/functional_tests.py
"""Funkcionalitás tesztek a telepítés ellenőrzéséhez."""

import sys
from typing import Callable, Tuple


class FunctionalTests:
    """Funkcionalitás tesztek osztálya."""

    def test_pytorch_operations(self) -> Tuple[bool, str]:
        """PyTorch alapműveletek tesztelése."""
        try:
            import torch

            # Tensor létrehozás
            x = torch.randn(3, 3)
            y = torch.randn(3, 3)

            # Alapműveletek
            z = torch.matmul(x, y)
            w = torch.sum(z)

            # CUDA teszt (ha elérhető)
            if torch.cuda.is_available():
                x_cuda = x.cuda()
                y_cuda = y.cuda()
                z_cuda = torch.matmul(x_cuda, y_cuda)

            return True, "PyTorch műveletek sikeresek"
        except Exception as e:
            return False, f"PyTorch teszt sikertelen: {e}"

    def test_numpy_operations(self) -> Tuple[bool, str]:
        """NumPy alapműveletek tesztelése."""
        try:
            import numpy as np

            # Tömb létrehozás
            arr = np.random.randn(100, 100)

            # Alapműveletek
            mean = np.mean(arr)
            std = np.std(arr)
            result = arr @ arr.T  # Mátrix szorzás

            return True, "NumPy műveletek sikeresek"
        except Exception as e:
            return False, f"NumPy teszt sikertelen: {e}"

    def test_pandas_operations(self) -> Tuple[bool, str]:
        """Pandas adatkezelés tesztelése."""
        try:
            import pandas as pd
            import numpy as np

            # DataFrame létrehozás
            df = pd.DataFrame({
                'A': np.random.randn(100),
                'B': np.random.randn(100),
                'C': np.random.randn(100)
            })

            # Alapműveletek
            mean = df.mean()
            std = df.std()
            corr = df.corr()

            return True, "Pandas műveletek sikeresek"
        except Exception as e:
            return False, f"Pandas teszt sikertelen: {e}"

    def test_core_components(self) -> Tuple[bool, str]:
        """Core komponensek tesztelése."""
        try:
            from neural_ai.core.base import CoreComponentFactory
            from neural_ai.core.config import ConfigManagerFactory
            from neural_ai.core.logger import LoggerFactory
            from neural_ai.core.storage import StorageFactory

            # Komponensek létrehozása
            config = ConfigManagerFactory.get_manager("yaml")
            logger = LoggerFactory.get_logger("default")
            storage = StorageFactory.get_storage("file")

            return True, "Core komponensek sikeresen betöltve"
        except Exception as e:
            return False, f"Core komponensek teszt sikertelen: {e}"

    def run_basic_tests(self) -> bool:
        """Futtatja az alapvető funkcionalitás teszteket."""
        tests = [
            ("PyTorch műveletek", self.test_pytorch_operations),
            ("NumPy műveletek", self.test_numpy_operations),
            ("Pandas adatkezelés", self.test_pandas_operations),
            ("Core komponensek", self.test_core_components),
        ]

        print("\n🔧 Funkcionalitás tesztek futtatása...")
        all_passed = True

        for name, test_func in tests:
            try:
                passed, message = test_func()
                status = "✓" if passed else "✗"
                print(f"{status} {name}: {message}")
                if not passed:
                    all_passed = False
            except Exception as e:
                print(f"✗ {name}: Váratlan hiba: {e}")
                all_passed = False

        return all_passed
```

### 7. Telepítési Módok

#### 7.1 Módok definiálása
```python
# scripts/install/modes.py
"""Telepítési módok definíciója."""

from typing import List, Dict

INSTALL_MODES = {
    'minimal': {
        'description': 'Minimális telepítés (csak core + alap eszközök)',
        'packages': ['core', 'testing'],
        'skip_optional': True,
    },
    'full': {
        'description': 'Teljes telepítés (minden funkcióval)',
        'packages': ['core', 'testing', 'dev', 'types'],
        'skip_optional': False,
    },
    'check-only': {
        'description': 'Csak ellenőrzés (nem telepít)',
        'packages': [],
        'skip_optional': True,
    }
}
```

### 8. CI/CD Támogatás

#### 8.1 Non-interactive mód
```python
# scripts/install/ci_cd.py
"""CI/CD támogatás."""

class CICDInstaller:
    """CI/CD környezetekhez telepítő."""

    def __init__(self):
        self.auto_yes = True
        self.verbose = False

    def install_ci_cd(self):
        """CI/CD környezet telepítése."""
        # Conda environment létrehozás
        self.run_command("conda env create -f environment.yml -y")

        # Telepítés aktiválása
        self.run_command("conda activate neural-ai-next")

        # Pre-commit telepítés (opcionális)
        self.run_command("pre-commit install")

        # Alapvető ellenőrzés
        self.run_command("python scripts/check_installation.py")

    def run_command(self, command: str):
        """Futtat egy parancsot."""
        import subprocess
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"CI/CD parancs sikertelen: {command}")
```

## Implementációs Lépések

### Fázis 1: Azonnali Javítások (1-2 óra)
1. ✅ Type stub csomagok hozzáadása `pyproject.toml` és `environment.yml`
2. ✅ Ruff hozzáadása minden konfigurációba
3. ✅ Verzió konfliktusok javítása `check_installation.py`-ban
4. ✅ VS Code beállítások frissítése Ruff támogatással

### Fázis 2: Strukturális Fejlesztés (fél nap)
5. ✅ Központi verzió konfiguráció létrehozása
6. ✅ Telepítő modularizálása (5-6 kisebb fájl)
7. ✅ Okosabb ellenőrző script implementálása
8. ✅ Funkcionalitás tesztek hozzáadása

### Fázis 3: Haladó Funkciók (1-2 nap)
9. ✅ Telepítési módok implementálása
10. ✅ CI/CD támogatás hozzáadása
11. ✅ Automatikus konfiguráció generálás
12. ✅ Dokumentáció frissítése

## Telepítési Útmutató Vázlat

### Fejlesztői Telepítés

#### 1. Automatikus Telepítés (Ajánlott)
```bash
# Teljes fejlesztői környezet
python scripts/install/main.py --mode full

# Csak ellenőrzés
python scripts/install/main.py --mode check-only

# Minimal (csak alapok)
python scripts/install/main.py --mode minimal
```

#### 2. Manuális Telepítés
```bash
# Környezet létrehozása
conda env create -f environment.yml
conda activate neural-ai-next

# Fejlesztői csomagok telepítése
pip install -e ".[dev]"

# Pre-commit beállítás
pre-commit install

# Ellenőrzés
python scripts/check_installation.py
```

#### 3. CI/CD Telepítés
```bash
# GitHub Actions / GitLab CI stb.
python scripts/install/ci_cd.py
```

## Tesztelési Stratégia

### Unit Tesztek
- Minden modulhoz külön teszt fájl
- Mock objektumok használata külső függőségekhez
- 100% coverage cél

### Integrációs Tesztek
- Teljes telepítési folyamat tesztelése
- Különböző környezetekben (Ubuntu, Windows, macOS)
- CUDA és non-CUDA verziók

### Funkcionális Tesztek
- PyTorch műveletek ellenőrzése
- NumPy/Pandas adatkezelés
- Core komponensek működése

## Dokumentáció Terv

### Telepítési Útmutató
- `docs/INSTALLATION_GUIDE.md` - Részletes telepítési útmutató
- `docs/DEVELOPER_SETUP.md` - Fejlesztői környezet beállítása
- `docs/TROUBLESHOOTING.md` - Hibaelhárítási útmutató

### API Dokumentáció
- `docs/install/` - Telepítő rendszer API dokumentációja
- Automatikus generálás Sphinx-szal

## Kockázatok és Megoldások

### Kockázatok
1. **Verzió konfliktusok** - Megoldás: Központi verzió kezelés
2. **CUDA kompatibilitás** - Megoldás: Több CUDA verzió támogatása
3. **Platform függőség** - Megoldás: Platform specifikus ellenőrzések
4. **Hálózati problémák** - Megoldás: Retry mechanizmusok

### Backup Terv
- Manuális telepítési útmutató mindig elérhető
- Egyszerűsített telepítő alternatíva
- Docker image készítése tartaléknak

## Siker Mutatók

### Technikai Mutatók
- ✅ Telepítés sikertelenség < 5%
- ✅ Függőségi konfliktusok száma = 0
- ✅ CI/CD build idő < 10 perc
- ✅ Funkcionalitás tesztek átmennek

### Felhasználói Mutatók
- ✅ Telepítési idő < 15 perc
- ✅ Dokumentáció minőség > 4/5
- ✅ Hibaelhárítási idő < 30 perc

## Következő Lépések

1. **Véglegesítsd a tervet** - Ellenőrizd, hogy minden szükséges elem benne van-e
2. **Implementálás** - Válaszd ki a prioritásos fejlesztéseket
3. **Tesztelés** - Futtass átfogó teszteket
4. **Dokumentáció** - Frissítsd a felhasználói dokumentációt
5. **Közzététel** - Osszd meg a csapattal

## Összefoglalás

Ez a terv egy átfogó fejlesztői telepítési rendszert határoz meg, amely:

- ✅ **Type stub támogatással** rendelkezik a Pylance-hoz
- ✅ **Ruff integrációval** modern code quality ellenőrzésre
- ✅ **Moduláris szerkezetű** a könnyű karbantarthatóság érdekében
- ✅ **Okos ellenőrzéssel** dinamikus függőség kezelésre
- ✅ **Funkcionalitás tesztekkel** a telepítés ellenőrzésére
- ✅ **Több telepítési módot** támogat a különböző igényekre
- ✅ **CI/CD kompatibilis** a folyamatos integrációhoz

A terv végrehajtásával egy professzionális, robusztus és felhasználóbarát fejlesztői telepítési rendszert kapunk, amely jelentősen javítja a fejlesztői élményt és csökkenti a telepítési problémák esélyét.
