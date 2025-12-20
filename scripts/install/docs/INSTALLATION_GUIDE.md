# Neural AI Next - Telepítési Útmutató

## Áttekintés

Ez a dokumentum részletesen leírja, hogyan telepítsd a Neural AI Next fejlesztői környezetet. A projekt támogatja a CUDA 12.1-et (GTX 1050 Ti-hez) és CPU only módot (laptopokhoz).

## Rendszerkövetelmények

### Minimális követelmények
- **CPU**: 4 mag (ajánlott 8+)
- **RAM**: 8GB (ajánlott 16GB+)
- **GPU**: Opcionális (CUDA 12.1 támogatott)
- **Tárhely**: 10GB szabad hely
- **OS**: Linux (Ubuntu 20.04+)

### Támogatott hardver konfigurációk

#### 1. Asztali gép (GTX 1050 Ti)
```
GPU: NVIDIA GTX 1050 Ti (4GB VRAM)
CUDA: 12.1 támogatott
PyTorch: CUDA 12.1 verzió
```

#### 2. Laptop (Lenovo T480)
```
GPU: Intel UHD Graphics 620 (CPU only)
PyTorch: CPU only verzió
Jupyter: Használat javasolt
```

### Támogatott brókerek

A projekt támogatja a következő brókereket:

#### 1. MetaTrader 5 (MT5)
- **Platform**: MetaTrader 5
- **Brókerek**: XM, Dukascopy
- **Telepítés**: Automatikus Wine-alapú telepítés
- **Konfiguráció**: `../../configs/collectors/mt5/`

#### 2. JForex
- **Platform**: Dukascopy JForex
- **Verzió**: JForex4
- **Telepítés**: Manuális telepítés szükséges
- **Dokumentáció**: `../../../docs/components/collectors/jforex/`

## Telepítési Módok

### 1. Interaktív Telepítés (Ajánlott)

```bash
# Interaktív telepítő indítása
python main.py --interactive
```

Az interaktív telepítő a következőket kérdezi:
1. **Telepítési mód**:
   - Minimal (csak alapok)
   - Fejlesztői környezet
   - Fejlesztői + Trader Engine
   - Teljes telepítés
   - Csak ellenőrzés

2. **PyTorch konfiguráció**:
   - CUDA 12.1 (ajánlott GTX 1050 Ti-hez)
   - CPU only (laptopokhoz)

### 2. Gyors Telepítés (Parancssori)

#### Asztali gép (GTX 1050 Ti)
```bash
python main.py --mode dev+trader --pytorch cuda12.1
```

#### Laptop (T480)
```bash
python main.py --mode dev --pytorch cpu
```

#### Csak ellenőrzés
```bash
python main.py --mode check
```

### 3. Manuális Telepítés

#### 1. Conda környezet létrehozása

**Asztali gép (CUDA 12.1):**
```bash
conda create -n neural-ai-next python=3.12 -y
conda activate neural-ai-next
conda install pytorch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1 pytorch-cuda=12.1 -c pytorch -c nvidia -y
```

**Laptop (CPU only):**
```bash
conda create -n neural-ai-next python=3.12 -y
conda activate neural-ai-next
conda install pytorch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1 cpuonly -c pytorch -y
```

#### 2. Függőségek telepítése

```bash
# Alap telepítés
pip install -e .

# Fejlesztői környezet
pip install -e .[dev]

# Broker támogatással
pip install -e .[dev]
bash scripts/install/scripts/setup_brokers.sh

# Válaszd ki a kívánt brókert:
# 1) MetaTrader 5 (MetaQuotes Demo)
# 2) XM Forex MT5
# 3) Dukascopy MT5
# 4) Dukascopy JForex4
# 5) Összes MT5 bróker (MetaQuotes, XM, Dukascopy)
# 6) Összes JForex bróker (JForex4)
# 7) Minden bróker telepítése
```

#### 3. Pre-commit beállítás

```bash
pre-commit install
```

#### 4. Jupyter kernel konfiguráció

```bash
python jupyter_setup.py
```

## Telepítés Ellenőrzése

### 1. Alapvető ellenőrzés

```bash
python check_installation.py
```

### 2. GPU ellenőrzés

```python
import torch
print(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"CUDA version: {torch.version.cuda}")
    print(f"GPU: {torch.cuda.get_device_name(0)}")
```

### 3. Core komponensek ellenőrzése

```python
from neural_ai.core.base import CoreComponentFactory
from neural_ai.core.config import ConfigManagerFactory
from neural_ai.core.logger import LoggerFactory

print("✓ Core komponensek betöltve")
```

## VS Code Beállítás

### 1. Bővítmények

A projekt automatikusan ajánlja a szükséges bővítményeket:
- **LÉNYEGES**: MQL Extension Pack, Python, Pylance, Jupyter, Ruff
- **ADATNÉZŐ**: Rainbow CSV, Parquet Viewer
- **FEJLESZTŐI**: Material Icon Theme, Roo Code

### 2. Debug konfiguráció

A `.vscode/launch.json` tartalmazza a következő debug konfigurációkat:
- **Neural AI Next**: Fő program futtatása
- **MT5 Collector**: Adatgyűjtő futtatása
- **Pytest**: Tesztek futtatása
- **Jupyter**: JupyterLab indítása
- **Installer**: Telepítő futtatása

### 3. Használat

1. Nyisd meg a projektet VS Code-ban
2. Válaszd ki a megfelelő debug konfigurációt
3. Nyomj F5-öt a futtatáshoz

## Jupyter Használat

### 1. JupyterLab indítása

```bash
conda activate neural-ai-next
jupyter lab
```

### 2. Kernel kiválasztása

1. Nyiss egy új notebookot
2. Válaszd ki a "Neural AI Next" kernelt:
   - Kernel → Change Kernel → Neural AI Next

### 3. Kaggle használata

1. Töltsd fel a `kaggle_template.ipynb` fájlt Kaggle-re
2. Add hozzá a projekt forráskódját
3. Használd a GPU-t modell tanításhoz

## Hibaelhárítás

### 1. Conda környezet nem aktiválódik

```bash
# Conda inicializálása
conda init bash
source ~/.bashrc

# Környezet aktiválása
conda activate neural-ai-next
```

### 2. CUDA nem elérhető

```bash
# NVIDIA driver ellenőrzés
nvidia-smi

# PyTorch újratelepítése
conda install pytorch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1 pytorch-cuda=12.1 -c pytorch -c nvidia -y
```

### 3. Import hibák

```bash
# Függőségek újratelepítése
pip install -e . --force-reinstall
```

### 4. Pre-commit hibák

```bash
# Pre-commit újratelepítése
pre-commit clean
pre-commit install
```

## Telepítési Opciók Részletesen

### Minimal
- Csak a core függőségek
- Nincs fejlesztői eszköz
- Alapvető funkcionalitás

### Dev
- Minden fejlesztői eszköz
- Type stub-ok a Pylance-hoz
- Pre-commit hookok
- Tesztelési keretrendszer

### Dev+Trader
- Fejlesztői környezet
- Trader Engine támogatás (MT5, JForex4)
- Adatgyűjtő készenlét
- Broker telepítő hozzáférés

### Full
- Minden funkció
- JupyterLab telepítve
- Kaggle template-ek
- Teljes debug támogatás
- MT5 és JForex4 támogatás
- Összes fejlesztői eszköz
- Adatkezelő eszközök

## Verzió Kompatibilitás

### Ténylegesen tesztelt verziók
```
Python: 3.12.12
PyTorch: 2.5.1
NumPy: 2.3.5
Pandas: 2.3.3
CUDA: 12.1
Lightning: 2.6.0
```

### Konfigurációs fájlok
- [`pyproject.toml`](../pyproject.toml): Függőségek és verziók
- [`environment.yml`](../environment.yml): Conda környezet
- [`.vscode/extensions.json`](../.vscode/extensions.json): VS Code bővítmények
- [`.vscode/launch.json`](../.vscode/launch.json): Debug konfiguráció

## Következő Lépések

1. **Fejlesztés megkezdése**:
   ```bash
   conda activate neural-ai-next
   code .
   ```

2. **Tesztek futtatása**:
   ```bash
   pytest tests -v
   ```

3. **Dokumentáció olvasása**:
    - [Komponens dokumentáció](../../../docs/components/base/README.md)
    - [API dokumentáció](../../../docs/components/base/api.md)
    - [Fejlesztési útmutató](../../../docs/development/unified_development_guide.md)

## További Források

- [PyTorch dokumentáció](https://pytorch.org/docs/stable/index.html)
- [CUDA dokumentáció](https://docs.nvidia.com/cuda/)
- [Jupyter dokumentáció](https://jupyter.org/documentation)
- [Kaggle GPU útmutató](https://www.kaggle.com/docs/gpu)

## Segítség Kérése

Ha problémába ütközne a telepítéssel:

1. Ellenőrizd a [hibaelhárítási szekciót](#hibaelhárítás)
2. Futtasd az ellenőrző scriptet: `python check_installation.py`
3. Nézd meg a [PROJECT_STATUS_REPORT.md](../../../docs/PROJECT_STATUS_REPORT.md) fájlt
4. Kérj segítséget a GitHub issue-k között