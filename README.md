# Neural-AI-Next

## Áttekintés

A Neural-AI-Next egy moduláris, hierarchikus kereskedési rendszer, amely különböző piaci dimenziókat elemez és integrál, hogy komplex kereskedési döntéseket hozzon. A rendszer modern gépi tanulási technikákat alkalmaz a pénzügyi piacok elemzésére.

## Fő jellemzők

- Moduláris, interfész-alapú architektúra
- Hierarchikus modell struktúra
- Több dimenzió együttes elemzése
- Integrált gépi tanulási modellek
- Konfiguráció-vezérelt működés
- Teljeskörű naplózás és monitorozás
- Skálázható és kiterjeszthető kialakítás
- Grafikus felület adatgyűjtés monitorozására
- Integrált log viewer

## Telepítés

### Interaktív Telepítés (Ajánlott)

```bash
# Interaktív telepítő indítása
python scripts/install/main.py --interactive
```

Az interaktív telepítő lehetővé teszi:
- Telepítési mód választását (minimal, dev, dev+mt5, full)
- PyTorch konfigurációt (CPU only, CUDA 12.0, CUDA 12.1)
- Automatikus ellenőrzést

### Gyors Telepítés

**Asztali gép (GTX 1050 Ti):**
```bash
python scripts/install/main.py --mode dev+mt5 --pytorch cuda12.1
```

**Laptop (Lenovo T480):**
```bash
python scripts/install/main.py --mode dev --pytorch cpu
```

### Manuális Telepítés

```bash
# 1. Conda környezet létrehozása
conda create -n neural-ai-next python=3.12 -y
conda activate neural-ai-next

# 2. PyTorch telepítése (válaszd ki a megfelelőt)

# CUDA 12.1 (GTX 1050 Ti-hez)
conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia -y

# VAGY CPU only (laptopokhoz)
conda install pytorch torchvision torchaudio cpuonly -c pytorch -y

# 3. Projekt telepítése
pip install -e .[dev]

# 4. Jupyter kernel konfiguráció
python scripts/install/jupyter_setup.py

# 5. Ellenőrzés
python scripts/check_installation.py
```

## Részletes Telepítési Útmutató

Lásd: [docs/INSTALLATION_GUIDE.md](docs/INSTALLATION_GUIDE.md)

## Projekt struktúra

```
neural-ai-next/
├── neural_ai/              # Fő kódkönyvtár
│   ├── core/              # Core komponensek
│   │   ├── base/          # Alap infrastruktúra
│   │   ├── config/        # Konfigurációkezelés
│   │   ├── logger/        # Naplózás
│   │   └── storage/       # Adattárolás
│   ├── collectors/        # Adatgyűjtők
│   ├── processors/        # Adatfeldolgozók
│   ├── models/            # Modell definíciók
│   └── utils/             # Segédeszközök
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
└── INSTALLATION.md        # Telepítési útmutató
```

## Használat

### Környezet aktiválása

```bash
conda activate neural-ai-next
```

### JupyterLab indítása

```bash
jupyter lab
```

### Tesztek futtatása

```bash
# Összes teszt
pytest

# Tesztlefedettség
pytest --cov=neural_ai

# Adott modul
pytest tests/core/logger/
```

### Grafikus felület használata

A projekt tartalmaz egy teljes grafikus felületet az adatgyűjtés monitorozására és vezérlésére.

#### Fő grafikus felület indítása

```bash
python main.py
```

A grafikus felület a következő funkciókat nyújtja:
- Valós idejű adatgyűjtés indítása/leállítása
- Historikus adatgyűjtés indítása
- Logok megtekintése valós időben
- Fájlstruktúra böngészése
- Adatok állapotának ellenőrzése
- Data warehouse tartalmának megjelenítése

#### Log Viewer indítása

```bash
python scripts/log_viewer.py
```

A Log Viewer lehetővé teszi:
- Logfájlok független megtekintését
- Valós idejű logfrissítést
- Logfájlok törlését és frissítését

## Fejlesztés

A fejlesztéssel kapcsolatos további információk a [docs/](docs/) könyvtárban találhatók.

### Fejlesztési állapot


## Technológiai stack

- **Nyelv**: Python 3.12
- **Gépi tanulás**: PyTorch 2.5.1 + Lightning 2.5.5
- **Adatkezelés**: pandas 2.3.3, numpy 2.3.5
- **Backtesting**: VectorBT
- **Vizualizáció**: matplotlib, seaborn
- **Tesztelés**: pytest
- **Kódminőség**: black, flake8, mypy, ruff, pre-commit
- **CUDA**: 12.1 (GTX 1050 Ti támogatott)
- **Jupyter**: JupyterLab Kaggle kompatibilis

## Projekttel kapcsolatos információk

- **Verzió**: 1.0.0
- **Utolsó frissítés**: 2025-12-17
- **Tesztlefedettség**: 194 teszteset
- **Kódminőség**: Pre-commit hookok aktív (black, flake8, isort, mypy)

## Licenc

Privát projekt, minden jog fenntartva.
