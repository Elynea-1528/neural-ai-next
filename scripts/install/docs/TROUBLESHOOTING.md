# Hibaelhárítási Útmutató

## Áttekintés

Ez a dokumentum a Neural AI Next telepítésével és használatával kapcsolatos gyakori problémák megoldását tartalmazza.

## Telepítési Problémák

### 1. Conda környezet nem aktiválódik

**Probléma:** A `conda activate neural-ai-next` parancs nem működik.

**Megoldás:**
```bash
# Conda inicializálása
conda init bash
source ~/.bashrc

# Környezet aktiválása
conda activate neural-ai-next
```

### 2. CUDA nem elérhető

**Probléma:** A PyTorch nem találja a CUDA-t.

**Megoldás:**
```bash
# NVIDIA driver ellenőrzés
nvidia-smi

# PyTorch újratelepítése CUDA 12.1-gyel
conda install pytorch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1 pytorch-cuda=12.1 -c pytorch -c nvidia -y
```

**Ellenőrzés:**
```python
import torch
print(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"CUDA version: {torch.version.cuda}")
    print(f"GPU: {torch.cuda.get_device_name(0)}")
```

### 3. Import hibák

**Probléma:** A modulok importálása sikertelen.

**Megoldás:**
```bash
# Függőségek újratelepítése
pip install -e . --force-reinstall

# Fejlesztői környezet telepítése
pip install -e .[dev]
```

### 4. Pre-commit hibák

**Probléma:** A pre-commit hookok hibát jeleznek.

**Megoldás:**
```bash
# Pre-commit újratelepítése
pre-commit clean
pre-commit install

# Manuális futtatás
pre-commit run --all-files
```

## Wine és Broker Problémák

### 5. Wine nincs telepítve

**Probléma:** A `wine` parancs nem található.

**Megoldás:**
```bash
# Ubuntu/Debian
sudo apt install wine-stable winbind

# Fedora
sudo dnf install wine

# Arch Linux
sudo pacman -S wine
```

### 6. MT5 telepítő ablak nem jelenik meg

**Probléma:** Az MT5 telepítő nem indul el.

**Megoldás:**
```bash
# Wine prefix törlése
rm -rf ~/.mt5

# Wine prefix újrainicializálása
WINEPREFIX=~/.mt5 winecfg

# Telepítés újrapróbálása
bash scripts/install/scripts/setup_brokers.sh
```

### 7. WebView2 Runtime hiba

**Probléma:** WebView2 Runtime hibaüzenet az MT5 indításakor.

**Megoldás:**
```bash
# WebView2 manuális telepítése
cd ~/Downloads
curl -L https://msedge.sf.dl.delivery.mp.microsoft.com/filestreamingservice/files/f2910a1e-e5a6-4f17-b52d-7faf525d17f8/MicrosoftEdgeWebview2Setup.exe --output webview2.exe
WINEPREFIX=~/.mt5 wine webview2.exe /silent /install
```

### 8. JForex4 telepítő nem indul el

**Probléma:** A JForex4 telepítő nem reagál.

**Megoldás:**
```bash
# JForex4 natív Linux alkalmazás, nem Wine-on fut!
# Ellenőrizd a következőket:

# 1. A telepítő letöltése megtörtént-e
ls -la ~/Downloads/JForex4_installer.sh

# 2. A telepítő futtatható-e
chmod +x ~/Downloads/JForex4_installer.sh

# 3. Telepítő manuális indítása
cd ~/Downloads
./JForex4_installer.sh

# 4. Ha a telepítő nem indul el, ellenőrizd a jogosultságokat
# A JForex4 natív Linux alkalmazás, Java alapú
```

## GPU Problémák

### 9. GPU memória túlcsordulás

**Probléma:** CUDA out of memory hiba.

**Megoldás:**
```python
# Batch méret csökkentése
batch_size = 32  # Változtasd 16-ra vagy 8-ra

# Gradient accumulation használata
accumulation_steps = 4

# Mixed precision training
from torch.cuda.amp import autocast, GradScaler
scaler = GradScaler()
```

### 10. GPU nem használható Jupyter-ben

**Probléma:** Jupyter notebook nem használja a GPU-t.

**Megoldás:**
```bash
# Jupyter kernel újraindítása
# Kernel -> Restart Kernel

# GPU ellenőrzése notebookban
import torch
print(f"CUDA available: {torch.cuda.is_available()}")
```

## Adatgyűjtési Problémák

### 11. MT5 kapcsolati hiba

**Probléma:** Nem sikerül csatlakozni az MT5-höz.

**Megoldás:**
```bash
# Ellenőrizd a következőket:
# 1. MT5 fut-e
# 2. Demo fiók létrehozva van-e
# 3. A szerver neve helyes-e
# 4. A login és password be van-e állítva

# Kapcsolati információk ellenőrzése
export WINEPREFIX=~/.mt5
wine ~/.mt5/drive_c/Program\ Files/MetaTrader\ 5/terminal.exe
```

### 12. Historikus adatok letöltése sikertelen

**Probléma:** Az adatgyűjtés megszakad vagy hibát jelez.

**Megoldás:**
```python
# Konfiguráció ellenőrzése
# configs/collectors/mt5/settings.yaml

# Kapcsolati beállítások
connection:
  timeout: 60  # Növeld meg az időtúllépést
  retry_attempts: 5  # Növeld meg a próbálkozások számát
  retry_delay: 10  # Növeld meg a várakozási időt
```

## VS Code Problémák

### 13. Debug konfiguráció nem működik

**Probléma:** A VS Code debugger nem indul el.

**Megoldás:**
```bash
# Conda környezet aktiválása VS Code-ban
# Nyomd meg: Ctrl+Shift+P
# Írd be: Python: Select Interpreter
# Válaszd ki: ~/miniconda3/envs/neural-ai-next/bin/python
```

### 14. Pylance hibák

**Probléma:** Pylance import hibákat jelez.

**Megoldás:**
```json
// .vscode/settings.json
{
    "python.analysis.extraPaths": [
        "./neural_ai",
        "./neural_ai/core",
        "./neural_ai/collectors"
    ]
}
```

## Jupyter Problémák

### 15. Kernel nem található

**Probléma:** A "Neural AI Next" kernel nem jelenik meg.

**Megoldás:**
```bash
# Kernel újratelepítése
python scripts/install/scripts/jupyter_setup.py

# JupyterLab újraindítása
jupyter lab
```

### 16. Kaggle template nem működik

**Probléma:** A Kaggle template hibát jelez.

**Megoldás:**
```python
# Ellenőrizd a következőket:
# 1. Internetkapcsolat
# 2. Kaggle API kulcs beállítva van-e
# 3. A dataset elérhető-e

# Kaggle API kulcs beállítása
import os
os.environ['KAGGLE_USERNAME'] = 'your_username'
os.environ['KAGGLE_KEY'] = 'your_key'
```

## További Segítség

Ha a probléma nem szerepel a listában:

1. Futtasd az ellenőrző scriptet: `python scripts/install/scripts/check_installation.py`
2. Nézd meg a [PROJECT_STATUS_REPORT.md](../../../docs/PROJECT_STATUS_REPORT.md) fájlt
3. Kérj segítséget a GitHub issue-k között
4. Ellenőrizd a [telepítési útmutatót](INSTALLATION_GUIDE.md)

## Hasznos Parancsok

```bash
# Környezet ellenőrzése
conda info --envs

# Telepített csomagok listázása
conda list

# PyTorch verzió ellenőrzése
python -c "import torch; print(torch.__version__)"

# CUDA elérhetőség ellenőrzése
python -c "import torch; print(torch.cuda.is_available())"

# Wine verzió ellenőrzése
wine --version

# Wine prefix információk
WINEPREFIX=~/.mt5 winecfg