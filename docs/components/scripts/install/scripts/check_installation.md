# check_installation.py

## Áttekintés

A `check_installation.py` egy telepítési ellenőrző script, amely ellenőrzi, hogy a Neural AI Next projekthez szükséges összes csomag és eszköz megfelelően telepítve van-e a rendszeren.

## Fájl információ

- **Elérési út:** `scripts/install/scripts/check_installation.py`
- **Típus:** Ellenőrző és validációs script
- **Feladat:** Környezet-ellenőrzés és telepítési állapot jelentés

## Főbb funkciók

### 1. Csomagellenőrzés (`check_package`)

Ellenőrzi egy adott Python csomag telepítését és verzióját.

**Paraméterek:**
- `package_name` (str): A csomag neve (pl. 'numpy')
- `import_name` (str | None): Az importáláshoz használt név (opcionális)
- `min_version` (str | None): A minimális szükséges verzió (opcionális)

**Visszatérési érték:**
- `tuple[bool, str]`: (sikeres-e, üzenet) pár

**Példa:**
```python
ok, message = check_package("torch", "torch", "2.5.0")
if ok:
    print(f"Siker: {message}")
else:
    print(f"Hiba: {message}")
```

### 2. CUDA core becslés (`estimate_cuda_cores`)

Becsüli a GPU CUDA core-ok számát a compute capability és a memória alapján.

**Paraméterek:**
- `major` (int): Major compute capability verzió
- `minor` (int): Minor compute capability verzió
- `total_memory_gb` (float): Teljes GPU memória GB-ban

**Visszatérési érték:**
- `int`: Becsült CUDA core-ok száma

**Támogatott GPU architektúrák:**
- Pascal (6.1): 128 core
- Turing (7.5): 1024 core
- Ampere (8.6): 2560 core
- Ada Lovelace (8.9): 10240 core

### 3. CUDA ellenőrzés (`check_cuda`)

Ellenőrzi a CUDA és cuDNN telepítését, valamint a GPU elérhetőségét.

**Visszatérési érték:**
- `tuple[bool, str]`: (sikeres-e, részletes információ)

**Ellenőrzött elemek:**
- GPU elérhetősége
- CUDA verzió
- cuDNN verzió
- GPU memória
- Compute capability
- CUDA core-ok becsült száma
- Működési teszt (mátrix szorzás)

### 4. Fő funkció (`main`)

Végrehajtja a teljes telepítési ellenőrzést és kiírja az eredményt.

**Ellenőrzött csomagok:**

**Core csomagok:**
- Python 3.12+
- NumPy 1.24.3+
- Pandas 2.0.3+
- PyTorch 2.5.0+
- Lightning 2.5.0+
- VectorBT 0.25.0+
- Scikit-learn 1.3.0+

**Fejlesztői eszközök:**
- Pytest 8.0.0+
- Black 24.1.0+
- Flake8 7.0.0+
- Mypy 1.8.0+
- Pre-commit 3.5.0+
- Ruff 0.1.0+

**Adatkezelő eszközök:**
- Fastparquet 2023.4.0+ (opcionális)

**Jupyter eszközök:**
- JupyterLab 4.0.0+
- Notebook 7.0.0+
- IPython 8.15.0+

**Web framework eszközök:**
- FastAPI 0.104.0+
- Uvicorn 0.24.0+
- WebSockets 12.0+
- HTTPX 0.25.0+
- Pydantic 2.4.0+

## Használat

### Futtatás

```bash
python scripts/install/scripts/check_installation.py
```

### Kimenet

A script részletes jelentést ad ki a következő formátumban:

```
============================================================
Neural AI Next - Telepítési Ellenőrzés
============================================================

Core csomagok:
✓ Python 3.12.12
✓ NumPy 1.24.3
✓ Pandas 2.0.3
✓ PyTorch 2.5.0
✓ Lightning 2.5.0
✓ VectorBT 0.25.0
✓ Scikit-learn 1.3.0
✓ CUDA: NVIDIA GeForce RTX 4090, CUDA verzió: 12.1, cuDNN: 8901,
       Memória: 24.0GB, Compute: 8.9, CUDA Cores: ~10240

Fejlesztői eszközök:
  ✓ Pytest 8.0.0
  ✓ Black 24.1.0
  ...

============================================================
✓ Minden ellenőrzés sikeres!
A környezet készen áll a fejlesztésre!
```

### Kilépési kódok

- `0`: Minden ellenőrzés sikeres
- `1`: Egy vagy több ellenőrzés sikertelen

## Típusok és minőségbiztosítás

### Típusannotációk

A script teljes típusozással rendelkezik:
- Minden függvény rendelkezik visszatérési típussal
- Nincs `Any` típus használat
- A `mypy` ellenőrzés 0 hibát jelez

### Linter konformitás

- `ruff` ellenőrzés: 0 hiba
- `mypy` ellenőrzés: 0 hiba
- A kód megfelel a projekt coding standardjeinek

## Tesztelés

A scripthez tartozik tesztfájl: `tests/scripts/install/scripts/test_check_installation.py`

**Tesztelt funkciók:**
- Csomagellenőrzés Python verzióval
- Nem létező csomag kezelése
- CUDA core becslés különböző GPU-kon

**Teszt futtatása:**
```bash
pytest tests/scripts/install/scripts/test_check_installation.py
```

vagy

```bash
python tests/scripts/install/scripts/test_check_installation.py
```

## Függőségek

- `torch`: PyTorch CUDA funkciókhoz
- `packaging`: Verzió összehasonlításhoz

## Hibakezelés

A script robusztus hibakezeléssel rendelkezik:
- Import hibák kezelése
- CUDA elérhetőség ellenőrzése
- Kivételkezelés a GPU működési tesztnél

## Kapcsolódó dokumentáció

- [Telepítési útmutató](../../../INSTALLATION_GUIDE.md)
- [Fejlesztői dokumentáció](../../../development/implementation_guide.md)
- [TASK_TREE_SCRIPTS](../../../development/TASK_TREE_SCRIPTS.md)

## Verziótörténet

- **1.0.0**: Kezdeti verzió - teljes környezet-ellenőrzés
- **Refaktorálva**: 2025-12-22 - magyar nyelv, típusozás, dokumentáció
