# 🧠 Neural AI Next - Intézményi Kereskedelem Ekozisztéma

**Verzió:** 1.0.0 | **Státusz:** 🟢 Foundation Phase (95.1% SECURE) | **Licenc:** MIT

---

## 🎯 Látomás & Küldetés

A **Neural AI Next** egy intézményi szintű, eseményvezérelt kereskedelmi ekozisztéma, amelyet nagyfrekvenciás tick adatfeldolgozásra (25+ év), valós idejű végrehajtásra és AI-alapú stratégia üzembe helyezésre terveztek. **Zéró kompromisszumokkal** épült a megbízhatóság, skálázhatóság és teljesítmény érdekében.

**Filozófia:** *"Laza Csatolás, Magas Kohézió"* - Minden komponens izolált, tesztelhető és cserélhető.

**Fókusz:** Prémium instrumentumok csak (EURUSD, XAUUSD, GBPUSD, USDJPY, USDCHF) - Magas likviditás, alacsony spread.

---

## 🏗️ Rendszerarchitektúra

### Eseményvezérelt Mag

```
┌─────────────────────────────────────────────────────────┐
│                    NEURAL AI NEXT                        │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │  JForex      │  │  MT5         │  │  IBKR        │ │
│  │  Bi5 + Java  │  │  FastAPI     │  │  TWS API     │ │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘ │
│         │                 │                 │          │
│         └─────────────────┼─────────────────┘          │
│                           ▼                            │
│              ┌────────────────────────┐                │
│              │   ESEMÉNY BUSZ (ZeroMQ)│                │
│              └────────────┬───────────┘                │
│                           │                            │
│         ┌─────────────────┼─────────────────┐          │
│         ▼                 ▼                 ▼          │
│  ┌──────────┐    ┌──────────────┐    ┌──────────┐    │
│  │ Parquet  │    │   Stratégia  │    │   AI     │    │
│  │ Tároló   │    │   Motor      │    │  Modellek│    │
│  └──────────┘    └──────────────┘    └──────────┘    │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

**Kulcselvek:**
- **Nincs Direkt Hívás:** A komponensek kizárólag eseményeken keresztül kommunikálnak
- **Adatbázis Először:** Minden állapot SQL adatbázisban perzisztált
- **Aszinkron Mindenhol:** Python 3.12 + `asyncio` a maximális teljesítményért
- **Big Data Kész:** Parquet tároló 25+ év tick adathoz

---

## 📊 Projekt Állapot (2026-08-11)

| Metrika | Érték |
|---------|-------|
| **Összes teszt** | 2395 |
| **SECURE** | 349 (95.1%) |
| **WARNING** | 13 (3.5%) |
| **VULNERABLE** | 5 (1.4%) |
| **Core réteg tesztek** | 1229 teszt gyűjtve |
| **Licenc** | MIT |
| **Python** | 3.12 |
| **PyTorch** | 2.5.1 (CUDA 12.1) |
| **Lightning** | 2.5.5 |

**Haladás:** 95.1% [████████████████████░░░░░░]

---

## 📚 Dokumentáció Szerkezete

### 🗺️ Fő Tervrajz

Minden fejlesztést a **Rendszer Specifikációk** irányítanak a [`docs/planning/specs/`](docs/planning/specs/) mappában:

1. **[Rendszerarchitektúra](docs/planning/specs/01_system_architecture.md)** - Eseményvezérelt Mag Tervezés
2. **[Dinamikus Konfiguráció](docs/planning/specs/02_dynamic_configuration.md)** - Hibrid Konfigurációs Rendszer (.env + SQL)
3. **[Megfigyelhetőség & Naplózás](docs/planning/specs/03_observability_logging.md)** - Strukturált Naplózás `structlog`-gal
4. **[Adatraktár](docs/planning/specs/04_data_warehouse.md)** - Parquet Tároló & Újramintavételezés
5. **[Gyűjtők Stratégia](docs/planning/specs/05_collectors_strategy.md)** - JForex Bi5 + Java Híd + MT5

### 📚 Komponens Dokumentáció

**Automatikusan Generált API Dokumentáció** a forráskódból docstring-ekkel:

- **[Komponensek Áttekintése](docs/components/)** - Teljes API dokumentáció minden core modulhoz
- **Tükörszerkezet:** A dokumentáció pontosan követi a forráskód szerkezetét
- **Forráshivatkozások:** Minden dokumentációs fájl linkel vissza az eredeti forrásfájlra
- **Automatikus Frissítés:** Futtasd a `python scripts/generate_docs.py` parancsot a dokumentáció újragenerálásához

**Core Modulok:**
- [Alaparchitektúra](docs/components/core/base/index.md) - DI Konténer, Factory, Interfészek
- [Konfiguráció](docs/components/core/config/index.md) - Dinamikus & YAML Konfig
- [Naplózás](docs/components/core/logger/index.md) - Strukturált Naplózó Rendszer
- [Tároló](docs/components/core/storage/index.md) - Parquet & Fájl Tároló
- [Adatbázis](docs/components/core/db/index.md) - SQLAlchemy ORM
- [Események](docs/components/core/events/index.md) - ZeroMQ Esemény Busz
- [Rendszer](docs/components/core/system/index.md) - Egészségügyi Monitorozás
- [Segédeszközök](docs/components/core/utils/index.md) - Segédfunkciók

### 🧠 AI Modellek

A rendszer **hierarchikus AI architektúrát** valósít meg több időkeretű elemzéshez:

- **[Hierarchikus Modell Szerkezet](docs/models/hierarchical/structure.md)** - D1, H4, H1, M15, M5, M1 modellek
- **Együttes Tanulás** - Több időkeretből származó előrejelzések kombinálása
- **PyTorch + Lightning** - CUDA-gyorsított tanítás és inferencia

### ⚙️ Adatfeldolgozók

15-dimenziós feature engineering tick adatokhoz:

- **[Dimenzió Feldolgozók Áttekintése](docs/processors/dimensions/overview.md)** - D1-D15 feature extrakció
- **Valós Idejű Feldolgozás** - Futás közbeni feature számítás
- **VectorBT Integráció** - Backtesting és validáció

---

## 🚀 Gyors Indítás

```bash
# 1. Miniconda telepítése (ha még nincs)
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b
source ~/.bashrc

# 2. NVIDIA driver ellenőrzése (GPU esetén)
nvidia-smi

# 3. Repository klónozása és telepítés
git clone https://github.com/your-org/neural-ai-next.git
cd neural-ai-next
python scripts/install.py --no-brokers

# 4. Környezet aktiválása
conda activate neural-ai-next

# 4. Adatok letöltése
python main.py download --symbol EURUSD --start 2024-01-01 --end 2024-01-31

# 5. Fejlesztői dashboard indítása
python main.py dashboard
```

---

## 🏗️ Fejlesztési Útmutató

### Projekt Szerkezet

```
neural-ai-next/
├── .github/workflows/ci.yml          # Ruff, Mypy, Pyright, PyTest
├── .github/workflows/deploy.yml      # Deploy staging/prod
├── .github/CODEOWNERS                # Review requirements per layer
├── .sops.yaml                        # SOPS rules
├── docs/                             # SSOT + Generated docs
├── neural_ai/                        # Source (DDD layers)
├── tests/                            # Mirror structure
├── scripts/                          # Install, deploy, generate
├── deploy/                           # Systemd, scripts, configs
├── configs/                          # YAML + SOPS
├── data/                             # .gitignore
├── models/                           # .gitignore
├── .env.example                      # Template only
├── pyproject.toml                    # Deps + tools
├── README.md                         # This file
├── LICENSE                           # MIT
└── CHANGELOG.md
```

### Branch Strategy

```
main (protected) ←── release/vX.Y.Z ←── develop ←── feature/*
                        │
                        └── hotfix/* (main-ből)
```

### Collaboration Rules

1. **Code Owners** – review requirements per layer
2. **Conventional Commits** – `feat(processor): add d3 trend logic`
3. **Atomic Commits** – 1 logikai változás = 1 commit
4. **QA Gate** – PR nem merge-elhető ha nem zöld: Ruff + Mypy + Pyright + PyTest
5. **Documentation** – Mirror docs kötelező (`docs/components/...`)

---

## ⚠️ Kritikus Szabályok (NO-GO ZÓNA)

### 1. 🇭🇺 Nyelvi Protokoll
- **MINDEN** kommunikáció (Chat, Commit, Docstring, Kommentek) **MAGYARUL**
- Kivétel: Kód kulcsszavak (def, class, import) és technikai kifejezések

### 2. 🪞 Tükörszerkezet & Atomic Commit
- A dokumentációnak tükröznie kell a kód szerkezetét
- **Minden fájlváltoztatás azonnali `git commit`-ot igényel**
- Nincs commit = ❌ SIKERTELEN

### 3. 🐍 Technikai Szigorúság
- **JForex:** TILOS CSV! Csak natív .bi5 (LZMA) feldolgozás
- **Tároló:** TILOS CSV/JSON! Csak particionált Parquet
- **Típusok:** TILOS `Any`! Szigorú típushints szükséges
- **Importok:** `if TYPE_CHECKING:` körkörös függőségekhez

### 4. 🧠 Memóriakezelés
- **NINCS TÖMÖRÍTÉS!** Soha ne tömörítsd a kontextust kifejezett felhasználói utasítás nélkül
- Használd ki a teljes 128k/200k token ablakot

### 5. 🔍 Kontextus Tudatosság
- **TILOS** fájlokat generálni a kapcsolódó dokumentáció elolvasása nélkül!
- A README-nek linkelnie kell a `docs/models` és `docs/processors` fájlokat

---

## 📞 Támogatás & Kapcsolat

- **Architektúra Kérdések:** Lásd [Rendszer Specifikációk](docs/planning/specs/)
- **AI Modell Kérdések:** Lásd [Hierarchikus Szerkezet](docs/models/hierarchical/structure.md)
- **Feldolgozó Kérdések:** Lásd [Dimenzió Áttekintés](docs/processors/dimensions/overview.md)
- **Fejlesztési Kérdések:** Lásd [Architektúra Szabványok](docs/development/architecture_standards.md) és [Custom Instructions](docs/development/custom-instructions.md)

---

## 📄 Licenc

**MIT License** - Neural AI Next v1.0.0

© 2026 Neural AI Next. Minden jog fenntartva.

---

## 🏆 Köszönetnyilvánítás

Intézményi szintű mérnöki gyakorlatokkal építve:
- Eseményvezérelt Architektúra
- Függőség Injektálás
- Factory Pattern
- Strategy Pattern
- Repository Pattern
- NullObject Pattern
- Lusta Betöltés
- Singleton (ahol megfelelő)

**Stack:** Python 3.12 | PyTorch 2.5.1 | Lightning 2.5.5 | VectorBT Pro | FastParquet | SQLAlchemy 2.0 | FastAPI | ZeroMQ

---

**Státusz:** 🟢 Foundation Phase (95.1% SECURE) | **Utoljára Frissítve:** 2026-08-11 | **Verzió:** 1.0.0
