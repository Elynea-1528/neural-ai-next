# main.py - Neural AI Next Egységesített Telepítő

## Áttekintés

A `main.py` a Neural AI Next projekt egységesített telepítő scriptje, amely interaktív módon vagy parancssorból végzi el a fejlesztői környezet telepítését. A script kihasználja az `environment.yml` és `pyproject.toml` fájlokat a függőségek kezeléséhez.

## Funkciók

### Telepítési Módok

A script a következő telepítési módokat támogatja:

- **MINIMAL**: Csak az alapvető függőségek telepítése
- **DEV**: Fejlesztői környezet telepítése
- **DEV_TRADER**: Fejlesztői + Trader Engine telepítése
- **FULL**: Teljes környezet telepítése
- **CHECK_ONLY**: Csak ellenőrzés, telepítés nélkül
- **TRADER_ONLY**: Csak Trader Engine telepítése
- **JUPYTER_ONLY**: Csak Jupyter környezet telepítése

### PyTorch Konfigurációk

- **CPU**: CPU-only telepítés (laptopokhoz)
- **CUDA_12_1**: CUDA 12.1 támogatással (ajánlott GTX 1050 Ti-hez)

## Használat

### Interaktív Mód

```bash
python scripts/install/scripts/main.py --interactive
```

### Parancssori Mód

```bash
# Fejlesztői környezet telepítése CUDA 12.1-gyel
python scripts/install/scripts/main.py --mode dev --pytorch cuda12.1

# Teljes telepítés CPU-val
python scripts/install/scripts/main.py --mode full --pytorch cpu

# Csak ellenőrzés
python scripts/install/scripts/main.py --mode check
```

### Részletes Kimenet

A `--verbose` vagy `-vvv` kapcsolóval részletes kimenetet kaphatunk:

```bash
python scripts/install/scripts/main.py --mode dev --verbose
```

## Főbb Komponensek

### `InstallMode` Enum

A telepítési módokat definiáló enumeráció.

### `PyTorchMode` Enum

A PyTorch konfigurációkat definiáló enumeráció.

### `Colors` Osztály

Színes kimeneteket biztosító ANSI színkódokat tartalmaz.

### `run_command()` Függvény

Shell parancsok végrehajtásáért felelős.

**Paraméterek:**
- `command`: A végrehajtandó parancs
- `check`: Ha True, kivételt dob hibakód esetén
- `shell`: Ha True, shell-en keresztül hajtja végre
- `verbose`: Ha True, részletes kimenetet jelenít meg

**Visszatérési érték:** True ha sikeres, False ha sikertelen

### `check_conda()` Függvény

Ellenőrzi, hogy a conda telepítve van-e.

### `check_conda_initialized()` Függvény

Ellenőrzi, hogy a conda inicializálva van-e.

### `check_environment()` Függvény

Ellenőrzi, hogy a `neural-ai-next` környezet létezik-e.

### `update_environment_yml()` Függvény

Frissíti a projekt `environment.yml` fájlját a kiválasztott PyTorch mód szerint.

**Paraméterek:**
- `pytorch_mode`: A PyTorch telepítési mód

**Visszatérési érték:** Az environment.yml fájl elérési útja

### `install_environment()` Függvény

Telepíti a környezetet a megadott konfiguráció szerint.

**Paraméterek:**
- `config`: Telepítési konfiguráció
- `verbose`: Ha True, részletes kimenetet jelenít meg

**Visszatérési érték:** True ha sikeres, False ha sikertelen

### `interactive_setup()` Függvény

Interaktív telepítési menüt jelenít meg.

**Visszatérési érték:** Telepítési konfiguráció, vagy None ha a felhasználó megszakítja

### `main()` Függvény

A script fő belépési pontja, kezeli a parancssori argumentumokat.

## Telepítési Folyamat

1. **Conda ellenőrzés**: Ellenőrzi, hogy conda telepítve van-e
2. **Conda inicializálás**: Ellenőrzi, hogy conda inicializálva van-e
3. **Környezet ellenőrzés**: Ellenőrzi, hogy a `neural-ai-next` környezet létezik-e
4. **Environment.yml használata**: Létrehozza a környezetet az `environment.yml` alapján
5. **Opcionális függőségek**: Telepíti a kiválasztott módnak megfelelő függőségeket
6. **Pre-commit beállítás**: Beállítja a pre-commit hookokat (ha szükséges)
7. **Ellenőrzés**: Lefuttatja az ellenőrző scriptet

## Hibakezelés

A script robusztus hibakezelést valósít meg:

- Minden parancs végrehajtás ellenőrzése
- Részletes hibaüzenetek színes kimeneten
- Felhasználói visszajelzés a hibákról
- Javaslatok a hibák javítására

## Függőségek

A script a következő külső eszközöket használja:

- **conda**: Környezetkezelés
- **pip**: Python csomagok telepítése
- **pre-commit**: Git pre-commit hookok

## DI Pattern Alkalmazása

A script a Dependency Injection (DI) pattern-t használja a `verbose_mode` kezeléséhez:

- A globális változókat eltávolítottuk
- A `verbose` paramétert a függvények között adjuk át
- Ez tesztelhetőséget és modularitást biztosít

## Példa Kimenet

```
============================================================
Neural AI Next - Egységesített Telepítő
============================================================

1. Telepítési mód:
   [1] Minimal (csak alapok)
   [2] Fejlesztői környezet
   [3] Fejlesztői + Trader Engine
   [4] Teljes telepítés
   [5] Csak Trader Engine
   [6] Csak Jupyter környezet
   [7] Csak ellenőrzés

Válassz opciót [1-7] (alapértelmezett: 2): 2

2. PyTorch konfiguráció:
   [1] CUDA 12.1 (ajánlott GTX 1050 Ti-hez)
   [2] CPU only (laptopokhoz)

Válassz opciót [1-2] (alapértelmezett: 1): 1

============================================================
Telepítési beállítások:
  - Mód: dev
  - PyTorch: cuda12.1
============================================================

Folytatod a telepítést? [y/N]: y
```

## Kapcsolódó Fájlok

- [`environment.yml`](../../../../environment.yml): A projekt függőségeit tartalmazó fájl
- [`pyproject.toml`](../../../../pyproject.toml): A projekt konfigurációja
- [`check_installation.py`](check_installation.md): Telepítés ellenőrző script
- [`jupyter_setup.py`](jupyter_setup.md): Jupyter környezet beállító script
- [`setup_brokers.sh`](setup_brokers.sh): Broker telepítő script

## Jegyzetek

- A script csak Linux környezetben tesztelt
- A CUDA 12.1 támogatás csak kompatibilis GPU-kkal működik
- A telepítés hosszú ideig tarthat, függően a kiválasztott módtól
- A `--verbose` kapcsoló hasznos lehet hibakereséshez
