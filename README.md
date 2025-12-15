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

## Részletes Telepítési Útmutató

Lásd: [INSTALLATION.md](INSTALLATION.md)

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

## Fejlesztés

A fejlesztéssel kapcsolatos további információk a [docs/](docs/) könyvtárban találhatók.

### Fejlesztési állapot

- ✅ Core infrastruktúra (Logger, Config, Storage, Base)
- ✅ Dokumentációs standardok és template-ek
- 🚧 MT5 Collector fejlesztése
- 🚧 Dimension Processors implementálása

### Következő lépések

1. MT5 Collector fejlesztése (Wine + Expert Advisor alapú)
2. Dimension Processors implementálása (15 piaci dimenzió)
3. Backtesting keretrendszer integráció
4. Modellek fejlesztése

## Technológiai stack

- **Nyelv**: Python 3.12
- **Gépi tanulás**: PyTorch 2.5.1 + Lightning 2.5.5
- **Adatkezelés**: pandas, numpy
- **Backtesting**: VectorBT
- **Vizualizáció**: matplotlib, seaborn
- **Tesztelés**: pytest
- **Kódminőség**: black, flake8, mypy, pre-commit

## Licenc
mtatrader 5: account:   5043658843
            password:   @rOpEe4a

Privát projekt, minden jog fenntartva.
