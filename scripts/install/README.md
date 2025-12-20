# Neural AI Next - Egységesített Telepítő Rendszer

## Áttekintés

Ez a mappa tartalmazza a Neural AI Next fejlesztői környezet telepítéséhez szükséges összes scriptet és dokumentációt. Az új egységesített telepítő kihasználja az `environment.yml` és `pyproject.toml` fájlokat a reprodukálható környezet létrehozásához.

## Struktúra

```
scripts/install/
├── docs/                    # Dokumentációk
│   ├── INSTALLATION_GUIDE.md
│   ├── BROKER_SETUP.md
│   └── TROUBLESHOOTING.md
├── scripts/                 # Telepítő scriptek
│   ├── main.py              # Egységesített telepítő
│   ├── setup_brokers.sh
│   ├── setup_wine_mt5.sh
│   ├── compile_mql.sh
│   ├── check_installation.py
│   └── jupyter_setup.py
└── README.md                # Ez a fájl
```

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

## Gyors Telepítés

### 1. Interaktív Telepítés (Ajánlott)

```bash
python scripts/install/scripts/main.py --interactive
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

### 2. Asztali gép (GTX 1050 Ti - CUDA 12.1)

```bash
python scripts/install/scripts/main.py --mode dev+trader --pytorch cuda12.1
```

### 3. Laptop (T480 - CPU only)

```bash
python scripts/install/scripts/main.py --mode dev --pytorch cpu
```

### 4. Teljes telepítés (Minden funkció)

```bash
python scripts/install/scripts/main.py --mode full --pytorch cuda12.1
```

## Telepítési Opciók

### Minimal
- Csak a core függőségek (pyproject.toml alap)
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

## Telepítési Folyamat

### 1. Környezet létrehozása

A telepítő az `environment.yml` fájlt használja a conda környezet létrehozásához:

```yaml
# environment.yml
name: neural-ai-next
dependencies:
  # Conda csomagok (PyTorch, CUDA, NumPy, Pandas, scikit-learn)
  - python=3.12.*
  - pytorch=2.5.1
  - torchvision=0.20.1
  - torchaudio=2.5.1
  - pytorch-cuda=12.1
  - lightning=2.5.5
  - cudatoolkit=12.1
  - numpy>=1.24.3,<3.0
  - pandas>=2.0.3,<3.0
  - scikit-learn>=1.3.0
  
  # Pip csomagok (pyproject.toml-ból)
  - pip:
      - -e .  # Betölti a pyproject.toml-t
```

### 2. Opcionális függőségek

A telepítő ezután telepíti az opcionális függőségeket a pyproject.toml alapján:

```bash
# Minimal: pip install -e .
# Dev: pip install -e .[dev]
# Dev+Trader: pip install -e .[dev,trader]
# Full: pip install -e .[full]
```

### 3. Broker telepítés

Ha szükséges, a telepítő elindítja a broker telepítőt:

```bash
bash scripts/install/scripts/setup_brokers.sh
```

## Broker Telepítés

### Broker Választási Opciók

1. MetaTrader 5 (MetaQuotes Demo)
2. XM Forex MT5
3. Dukascopy MT5
4. Dukascopy JForex4
5. **Összes MT5 bróker (MetaQuotes, XM, Dukascopy)**
6. **Összes JForex bróker (JForex4)**
7. **Minden bróker telepítése**

### Broker Telepítés Indítása

```bash
bash scripts/install/scripts/setup_brokers.sh
```

### Konfiguráció

A konfigurációs fájlok a `configs/collectors/` mappában találhatók:

- **MT5 konfigurációk**: `configs/collectors/mt5/`
  - `broker_metaquotes.yaml`
  - `broker_xm.yaml`
  - `broker_dukascopy.yaml`

- **JForex konfiguráció**: `configs/collectors/jforex/`
  - `jforex_config.yaml`

A konfigurációs fájlokat manuálisan kell létrehozni a saját beállításaid szerint.

## Telepítés Ellenőrzése

### Alapvető ellenőrzés

```bash
python scripts/install/scripts/check_installation.py
```

### GPU ellenőrzés

```python
import torch
print(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"CUDA version: {torch.version.cuda}")
    print(f"GPU: {torch.cuda.get_device_name(0)}")
    print(f"Memory: {torch.cuda.get_device_properties(0).total_memory / (1024**3):.1f}GB")
```

## Jupyter Használat

### JupyterLab indítása

```bash
conda activate neural-ai-next
jupyter lab
```

### Kernel kiválasztása

1. Nyiss egy új notebookot
2. Válaszd ki a "Neural AI Next" kernelt:
   - Kernel → Change Kernel → Neural AI Next

## VS Code Beállítás

### Bővítmények

A projekt automatikusan ajánlja a szükséges bővítményeket:
- **LÉNYEGES**: MQL Extension Pack, Python, Pylance, Jupyter, Ruff
- **ADATNÉZŐ**: Rainbow CSV, Parquet Viewer
- **FEJLESZTŐI**: Material Icon Theme, Roo Code

### Debug konfiguráció

A `.vscode/launch.json` tartalmazza a következő debug konfigurációkat:
- **Neural AI Next**: Fő program futtatása
- **MT5 Collector**: Adatgyűjtő futtatása
- **Pytest**: Tesztek futtatása
- **Jupyter**: JupyterLab indítása
- **Installer**: Telepítő futtatása

## Támogatott Hardver Konfigurációk

### 1. Asztali gép (GTX 1050 Ti)
```
GPU: NVIDIA GTX 1050 Ti (4GB VRAM)
CUDA: 12.1 támogatott
PyTorch: CUDA 12.1 verzió
```

### 2. Laptop (Lenovo T480)
```
GPU: Intel UHD Graphics 620 (CPU only)
PyTorch: CPU only verzió
Jupyter: Használat javasolt
```

## Támogatott Brókerek

### MetaTrader 5 (MT5)
- **Platform**: MetaTrader 5
- **Brókerek**: MetaQuotes, XM, Dukascopy
- **Telepítés**: Automatikus Wine-alapú telepítés
- **Konfiguráció**: `configs/collectors/mt5/`

### JForex
- **Platform**: Dukascopy JForex
- **Verzió**: JForex4
- **Telepítés**: Automatikus natív Linux telepítés
- **Java**: Bundled JRE (nem szükséges külön Java SDK)
- **Konfiguráció**: `configs/collectors/jforex/`

## Verzió Kompatibilitás

### Ténylegesen tesztelt verziók
```
Python: 3.12.*
PyTorch: 2.5.1
Torchvision: 0.20.1
Torchaudio: 2.5.1
NumPy: 1.24.3+
Pandas: 2.0.3+
CUDA: 12.1
Lightning: 2.5.5
```

## Hibaelhárítás

### Conda init probléma

```bash
# Ellenőrizd, hogy conda inicializálva van-e
cat ~/.bashrc | grep "conda initialize"

# Ha nincs, inicializáld
conda init bash
source ~/.bashrc

# Ha van, de nem működik
export PATH="~/miniconda3/bin:$PATH"
source ~/.bashrc
```

### CUDA nem elérhető

```bash
# NVIDIA driver ellenőrzés
nvidia-smi

# PyTorch újratelepítése
conda install pytorch=2.5.1 torchvision=0.20.1 torchaudio=2.5.1 pytorch-cuda=12.1 -c pytorch -c nvidia -y
```

### Import hibák

```bash
# Függőségek újratelepítése
pip install -e . --force-reinstall
```

### Pre-commit hibák

```bash
# Pre-commit újratelepítése
pre-commit clean
pre-commit install
```

Ha problémába ütközne a telepítéssel:

1. Ellenőrizd a [hibaelhárítási szekciót](docs/TROUBLESHOOTING.md)
2. Futtasd az ellenőrző scriptet: `python scripts/install/scripts/check_installation.py`
3. Nézd meg a [PROJECT_STATUS_REPORT.md](../../docs/PROJECT_STATUS_REPORT.md) fájlt
4. Kérj segítséget a GitHub issue-k között

## Hasznos Linkek

- [PyTorch dokumentáció](https://pytorch.org/docs/stable/index.html)
- [CUDA dokumentáció](https://docs.nvidia.com/cuda/)
- [Jupyter dokumentáció](https://jupyter.org/documentation)
- [Kaggle GPU útmutató](https://www.kaggle.com/docs/gpu)
- [MT5 Collector Dokumentáció](../../docs/components/collectors/mt5/README.md)

## Fejlesztés

### Scriptek fejlesztése

A scriptek fejlesztéséhez kövesd az alábbi lépéseket:

1. Aktiváld a fejlesztői környezetet:
   ```bash
   conda activate neural-ai-next
   ```

2. Futtasd a scripteket teszteléshez:
   ```bash
   python scripts/install/scripts/main.py --mode check
   bash scripts/install/scripts/setup_brokers.sh
   python scripts/install/scripts/check_installation.py
   ```

3. Ellenőrizd a kódminőséget:
   ```bash
   pre-commit run --all-files
   ```

### Új funkciók hozzáadása

1. Hozz létre egy új branchet:
   ```bash
   git checkout -b feature/installer-new-feature
   ```

2. Implementáld az új funkciót

3. Írj teszteket az új funkcióhoz

4. Frissítsd a dokumentációt

5. Commit-old a változtatásokat:
   ```bash
   git add .
   git commit -m "feat(installer): új funkció hozzáadása"
   ```

6. Push-old a változtatásokat:
   ```bash
   git push origin feature/installer-new-feature
   ```

## Licensz

Ez a projekt a Neural AI Next projekt része. További információkért lásd a fő [README.md](../../README.md) fájlt.