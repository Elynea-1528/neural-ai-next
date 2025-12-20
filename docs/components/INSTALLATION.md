# Neural AI Next - Telepítési Útmutató

Ez a dokumentum tartalmazza a Neural AI Next projekt teljes környezetének beállítási útmutatóját.

## Gyors Telepítés

```bash
# 1. Miniconda telepítése (ha nincs)
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
source ~/.bashrc

# 2. Automatikus telepítés
python install_environment.py

# 3. Telepítés ellenőrzése
python scripts/check_installation.py
```

## Rendszerkövetelmények

- **Operációs rendszer**: Linux (Ubuntu 20.04+ / Debian / Fedora)
- **GPU**: NVIDIA GPU CUDA 12.2 támogatással (1050 Ti vagy jobb)
- **Memória**: Minimum 8GB RAM (16GB ajánlott)
- **Tárhely**: Minimum 10GB szabad hely
- **NVIDIA Driver**: Minimum 535.x (CUDA 12.2 támogatáshoz)

## Részletes Telepítési Lépések

### 1. NVIDIA Driver Ellenőrzés

```bash
nvidia-smi
```

Ellenőrizd, hogy a CUDA Version legalább 12.2-t mutat.

### 2. Miniconda Telepítés

```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
# Kövesd a képernyőn megjelenő utasításokat
source ~/.bashrc
```

### 3. Automatikus Telepítés

Futtasd a telepítő scriptet:

```bash
python install_environment.py
```

Ez a script:
- Létrehozza a conda környezetet
- Telepíti az összes függőséget
- Beállítja a PyTorch-ot CUDA támogatással
- Konfigurálja a pre-commit hookokat
- Ellenőrzi a telepítést

### 3. Projekt telepítése development módban

Telepítsd a projektet development módban, hogy a Python package-ként legyen kezelve:

```bash
pip install -e .
```

Ez a lépés lehetővé teszi, hogy bármelyik modult importálni lehessen a projektben anélkül, hogy manuálisan kellene a sys.path-et manipulálni.

### 4. Manuális Telepítés (ha szükséges)

```bash
# Környezet létrehozása
conda env create -f environment.yml
conda activate neural-ai-next

# PyTorch telepítése
pip install torch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1 --index-url https://download.pytorch.org/whl/cu121

# Pre-commit beállítása
pre-commit install
```

## Telepítés Ellenőrzése

```bash
python scripts/check_installation.py
```

Várható kimenet:
```
============================================================
Neural AI Next - Telepítési Ellenőrzés
============================================================
✓ Python 3.12.0
✓ NumPy 1.26.3
✓ Pandas 2.2.0
✓ PyTorch 2.5.1
✓ Lightning 2.5.5
✓ VectorBT 0.25.6
✓ Scikit-learn 1.4.0
✓ Matplotlib 3.8.2
✓ CUDA elérhető: NVIDIA GeForce GTX 1050 Ti
✓ CUDA verzió: 12.1
✓ cuDNN verzió: 8902
============================================================
✓ Minden ellenőrzés sikeres!
```

## Environment Fájl

A `environment.yml` fájl tartalmazza az összes szükséges függőséget:

```yaml
name: neural-ai-next
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.12
  - pip=24.0
  - numpy=1.26.3
  - pandas=2.2.0
  - matplotlib=3.8.2
  - seaborn=0.13.1
  - scikit-learn=1.4.0
  - jupyterlab=4.1.0
  - ipykernel=6.29.0
  - lightning=2.5.5
  - pytest=8.0.0
  - pytest-cov=4.1.0
  - black=24.1.1
  - isort=5.13.2
  - flake8=7.0.0
  - mypy=1.8.0
  - pre-commit=3.5.0
  - pylint=3.0.3
  - bandit=1.7.7
  - pip:
    - torch==2.5.1
    - torchvision==0.20.1
    - torchaudio==2.5.1
    - vectorbt==0.25.6
```

## Pre-commit Konfiguráció

A `.pre-commit-config.yaml` fájl tartalmazza a kódminőség-ellenőrző hookokat.

## VSCode Beállítások

A `.vscode/settings.json` fájl tartalmazza a VSCode specifikus beállításokat.

## Használat

### Környezet Aktiválása

```bash
conda activate neural-ai-next
```

### JupyterLab Indítása

```bash
jupyter lab
```

### Tesztek Futtatása

```bash
# Összes teszt
pytest

# Tesztlefedettség
pytest --cov=neural_ai
```

### Grafikus felület használata

A projekt tartalmaz egy teljes grafikus felületet az adatgyűjtés monitorozására és vezérlésére.

#### Fő grafikus felület indítása

```bash
python main.py
```

A grafikus felület a következő funkciókat nyújtja:
- **Control Panel**: Adatgyűjtés indítása/leállítása
  - Start Collector: Valós idejű adatgyűjtés indítása
  - Stop Collector: Adatgyűjtés leállítása
  - Start Historical: 25 éves historikus adatgyűjtés indítása

- **Status Panel**: Rendszerállapot megjelenítése
  - Collector status: Fut-e az adatgyűjtő
  - Historical status: Historikus gyűjtés állapota

- **Data Structure**: Fájlstruktúra böngészése
  - Hierarchikus fa szerkezet
  - Fájlméret és módosítási dátum megjelenítése

- **Log Viewer**: Valós idejű logmegjelenítés
  - Automatikus frissítés 2 másodpercenként
  - Utolsó 100 sor megjelenítése

- **Data Information**: Adatok állapotának ellenőrzése
  - Tick-ek és OHLCV fájlok számának megjelenítése
  - Data warehouse tartalmának ellenőrzése

- **Menüsáv**: Gyors hozzáférés a funkciókhoz
  - File → Open Data Folder: Adatmappa megnyitása
  - Tools → View Logs: Logfájlok megtekintése
  - Tools → Check Data Status: Adatok állapotának ellenőrzése
  - Help → About: Rendszerinformációk

#### Log Viewer indítása

```bash
python scripts/log_viewer.py
```

A Log Viewer lehetővé teszi:
- Logfájlok független megtekintését
- Valós idejű logfrissítést (1 másodpercenként)
- Logfájlok törlését és frissítését
- Logfájl megnyitását külső szerkesztőben

## Hibaelhárítás

### CUDA nem elérhető

```bash
nvidia-smi
python -c "import torch; print(torch.cuda.is_available())"
```

### Conda környezet problémák

```bash
conda env remove -n neural-ai-next -y
python install_environment.py
```

### Pre-commit hibák

```bash
pre-commit clean
pre-commit install
```

## Projekt Szerkezet

```
neural-ai-next/
├── neural_ai/              # Fő kódkönyvtár
├── tests/                 # Tesztek
├── docs/                  # Dokumentáció
├── configs/               # Konfigurációs fájlok
├── data/                  # Adatok
├── logs/                  # Logfájlok
├── notebooks/             # Jupyter notebookok
├── scripts/               # Segédszkriptek
├── main.py                # Grafikus felület
├── environment.yml        # Conda környezet
├── install_environment.py # Automatikus telepítő
└── INSTALLATION.md        # Ez a dokumentum
```

## Következő Lépések

- [ ] MT5 Collector fejlesztése
- [ ] Dimension Processors implementálása
- [ ] Backtesting keretrendszer integráció
- [ ] Modellek fejlesztése

---

**Dokumentum verzió**: 1.1
**Utolsó frissítés**: 2025-12-17
