# Neural AI Next - Telepítési Útmutató

## Áttekintés

A rendszer **egyetlen automatizált telepítővel** telepíthető: [`scripts/install.py`](../scripts/install.py).
A telepítő hardverdetektálást végez, és ennek megfelelően dönt:

| Detektálás | Eredmény |
|---|---|
| NVIDIA GPU (`nvidia-smi`) | CUDA 12.1-es PyTorch VS CPU-only PyTorch |
| AVX2 (`/proc/cpuinfo`) | Polars + PyArrow (gyors) VS fastparquet (fallback) |

## Rendszerkövetelmények

- **CPU**: 4 mag (ajánlott 8+), **AVX2 ajánlott** (a Polars adatfeldolgozóhöz)
- **RAM**: 8GB (ajánlott 16GB+)
- **GPU**: opcionális, CUDA 12.1 támogatott NVIDIA kártyákhoz (pl. GTX 1050 Ti, RTX 3050)
- **Tárhely**: 10GB+ szabad (a conda env CUDA-s PyTorch-csal ~8-12GB)
- **OS**: Linux (Ubuntu 20.04+)

## Előfeltételek

1. **Miniconda** – a telepítő ezt feltételezi, és kilép, ha nincs conda.
   Telepítés: `https://docs.conda.io/en/latest/miniconda.html` (**default útvonalra**, ld. hibaelhárítás)
2. **NVIDIA driver** *(opcionális, de ajánlott NVIDIA GPU-hoz)* – a telepítő `nvidia-smi`-vel érzékeli a GPU-t.
   Ha nincs driver, **CPU-only PyTorch** kerül telepítésre (a 3050 kihasználatlanul marad).
   ```bash
   sudo ubuntu-drivers install          # vagy: sudo apt install nvidia-driver-570 nvidia-utils-570
   nvidia-smi                           # ellenőrzés – csak ezután futtasd a telepítőt!
   ```
   Hibrid (Optimus) laptopokon: `prime-select nvidia` vagy `prime-select on-demand`.
3. **Wine** *(opcionális, csak az MT5 brókerhez)* – a telepítő csak figyelmeztet, nem telepíti:
   ```bash
   sudo apt install wine-stable
   ```

## Telepítés

### 1. Automatikus telepítés (ajánlott)

```bash
# Fejlesztői környezet brókerek nélkül (laptopon fejlesztéshez ez az ajánlott):
python scripts/install.py --no-brokers

# Vagy teljes telepítés (bróker telepítőkkel: JForex4, IBKR TWS, MT5):
python scripts/install.py
```

**Mit csinál a telepítő automatikusan:**
- Hardverdetektálás (NVIDIA GPU, AVX2)
- Régi `neural-ai-next` környezet eltávolítása (ha létezik)
- Conda env létrehozása: **Python 3.12, PyTorch 2.5.1 (+ torchvision 0.20.1, torchaudio 2.5.1, CUDA 12.1 vagy CPU), Lightning 2.5.5, pandas, numpy, scikit-learn**
- Adatkönyvtárak: **polars + pyarrow** (AVX2) vagy **fastparquet** (fallback)
- Projekt függőségek: `pip install -e .[dev,trader,jupyter,ui]`
- Bróker telepítők letöltése és indítása (kivéve `--no-brokers` esetén)

**Hasznos flag-ek:**
```bash
python scripts/install.py --only dev,trader   # csak meghatározott csoportok (dev, trader, jupyter, ui)
python scripts/install.py --no-brokers        # bróker telepítők kihagyása
python scripts/install.py -v                  # részletes (verbose) kimenet
```

### 2. Kézi telepítés

```bash
# 1. Környezet létrehozása
conda create -n neural-ai-next python=3.12 -y
conda activate neural-ai-next

# 2. PyTorch – NVIDIA GPU esetén (CUDA 12.1):
conda install pytorch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1 pytorch-cuda=12.1 -c pytorch -c nvidia -y
# VAGY CPU only (GPU nélkül):
conda install pytorch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1 cpuonly -c pytorch -y

# 3. Kapcsolódó ML csomagok
conda install lightning=2.5.5 pandas numpy scikit-learn -c conda-forge -y

# 4. Adatkönyvtárak (AVX2-es CPU esetén; különben fastparquet):
pip install polars pyarrow

# 5. Projekt függőségek
pip install -e .[dev,trader,jupyter,ui]        # vagy pl. csak: pip install -e .[dev]
```

## Környezet konfigurálása

```bash
conda activate neural-ai-next
cp .env.example .env      # opcionális; a rendszer fő konfigurációja a configs/*.yaml
```

- **`configs/*.yaml`** – a tényleges futási konfiguráció (adatbázis, storage, logging, collectors, processors, events, system)
- **`.env`** – opcionális környezeti változó forrás. **Soha ne kerüljön a repository-ba** – a `.gitignore` (`:60`) védi. Ha hibaüzenet `DB_URL`-t kér, azt itt vagy a `configs/database.yaml`-ban állíthatod be.

## Telepítés ellenőrzése

```bash
conda activate neural-ai-next

# PyTorch / CUDA ellenőrzés
python -c "import torch; print(f'PyTorch: {torch.__version__}, CUDA: {torch.cuda.is_available()}')"

# Adatfeldolgozás ellenőrzés
python -c "import polars as pl; print(f'Polars: {pl.__version__}')"

# Tesztek futtatása
pytest tests -v
```

## VS Code beállítás

A `.vscode/settings.json` tartalmazza a projekt fejlesztői beállításait (Pylance strict mode, Ruff formatter, pytest konfiguráció).

**FIGYELEM:** a `settings.json` **hardcode-olt abszolút útvonalat** használ az interpreterhez és a pytest-hez:
```jsonc
"python.defaultInterpreterPath": "/home/elynea/miniconda3/envs/neural-ai-next/bin/python",
"python.testing.pytestPath": "/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest",
```
Ha a gépeden a felhasználónév vagy a miniconda útvonala eltér, ezeket igazítani kell.

**Ajánlott bővítmények:** Python, Pylance, Ruff, Rainbow CSV, Parquet Viewer, Material Icon Theme, Roo Code.

## Jupyter használat (opcionális)

```bash
conda activate neural-ai-next
jupyter lab
```

## Gyors indítás

```bash
conda activate neural-ai-next
python main.py live                    # Live mód
python main.py dashboard               # Dashboard
python main.py download --symbol EURUSD --start 2024-03-20 --end 2024-03-20   # Adatletöltés
```

## Hibaelhárítás

### 1. "Conda nincs telepítve!" – a telepítő kilép
Telepítsd a Miniconda-t, és ellenőrizd, hogy a `conda` parancs elérhető: `which conda`.
**Fontos:** a telepítő a conda-t a `/home/<user>/miniconda3` (**default**) útvonalon keresi
([`scripts/install.py`](../scripts/install.py) – `get_conda_path()`). Más útvonalra telepített conda
esetén a függvényt vagy a telepítést igazítani kell.

### 2. Conda környezet nem aktiválódik
```bash
conda init bash
source ~/.bashrc
conda activate neural-ai-next
```

### 3. CUDA nem elérhető / GPU detektálva, de torch nem látja
```bash
# Driver ellenőrzés
nvidia-smi

# PyTorch újratelepítése CUDA 12.1-gyel
conda install pytorch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1 pytorch-cuda=12.1 -c pytorch -c nvidia -y
```
Ha a `nvidia-smi` nem listázza a GPU-t a telepítéskor, a telepítő CPU-only PyTorch-ot tett fel –
telepítsd a drivert, és futtasd újra a telepítőt (a régi env-et az maga eltávolítja).

### 4. Import hibák
```bash
pip install -e . --force-reinstall
```

### 5. MT5 bróker nem indul
A telepítő Wine-t igényel az MT5-höz: `sudo apt install wine-stable`, majd a futtatás a `~/.mt5`
wine prefixben történik. JForex4 és IBKR TWS nem igényelnek Wine-t.

## Verzió kompatibilitás

### Telepített verziók (SSOT: `scripts/install.py`)
```
Python: 3.12
PyTorch: 2.5.1
TorchVision: 0.20.1
TorchAudio: 2.5.1
Lightning: 2.5.5
CUDA: 12.1 (GPU-s build)
Pandas / NumPy / scikit-learn: conda által feloldott verziók
Polars / PyArrow: pip (AVX2 esetén) / fastparquet (fallback)
```

### GPU kompatibilitás
- **CUDA 12.1**: kompatibilis a GTX 1050 Ti-vel (Pascal) és az RTX 3050-nel (Ampere) is.
- **RTX 50xx (Blackwell)** esetén minimum **CUDA 12.8** szükséges – a jövőbeli hardvercserekor
  az install.py `pytorch-cuda` verzióját és a PyTorch buildet frissíteni kell.

### Konfigurációs fájlok
- [`pyproject.toml`](../pyproject.toml): pip függőségek és fejlesztői eszközök (QA Gate)
- [`configs/*.yaml`](../configs/): futási konfiguráció
- [`.vscode/settings.json`](../.vscode/settings.json): VS Code beállítások

## Dokumentáció

- [`README.md`](../README.md): projekt áttekintés és gyors indítás
- [`scripts/install.py`](../scripts/install.py): a telepítő forrása
- [`docs/components/scripts/install.md`](components/scripts/install.md): telepítő komponens dokumentáció
- [`AGENTS.md`](../AGENTS.md): fejlesztési szabályok (nyelv, tükörszerkezet, QA Gate) – **jelenleg a [`.clinerules/rules.md`](../.clinerules/rules.md) a hatályos szabályai**