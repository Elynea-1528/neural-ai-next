# 🧠 Neural AI Next - Intézményi Kereskedelem Ekozisztéma

**Verzió:** 1.0.0 | **Státusz:** 🟡 Architektúra Fázis | **Licenc:** Tulajdonosi

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

### 🛠️ Fejlesztési Irányelvek

- **[Egységes Fejlesztési Útmutató](docs/development/unified_development_guide.md)** - Pylance Strict, Magyar Docstring-ek
- **[Core Függőségek](docs/development/core_dependencies.md)** - DI Konténer, Factory Pattern, NullObject
- **[Feladatfa Vezérlőpult](docs/development/TASK_TREE.md)** - Valós idejű projekt státusz és telemetria
- **[Architektúra Szabványok](docs/development/architecture_standards.md)** - Modulszerkezet & elnevezési konvenciók

### 📖 Dokumentáció Generálás

A rendszer tartalmaz egy **automatikus dokumentáció generátort**, amely kinyeri a docstring-eket a forráskódból:

```bash
# Generál/frissít minden komponens dokumentációt
python scripts/generate_docs.py
```

**Funkciók:**
- ✅ Kinyeri a modul, osztály és függvény docstring-eket AST használatával
- ✅ Létrehozza a tükördokumentáció szerkezetét a `docs/components/` mappában
- ✅ Generál indexfájlokat minden könyvtárhoz
- ✅ Visszahivatkozik a forrásfájlokra a könnyű navigációért
- ✅ Támogatja a magyar docstring-eket (a projekt szabványai szerint)

---

## 🚀 Gyors Indítás

### Előfeltételek

- **Python:** 3.12+
- **Conda:** Miniconda3
- **CUDA:** 12.1 (GPU gyorsításhoz)
- **Java:** 11+ (JForex Hídhoz)

### Telepítés

**🚀 EGYSÉGES ZÉRÓ-BEÁLLÍTÁSÚ TELEPÍTŐ (AJÁNLOTT)**

Futtasd az egységes telepítőt, amely automatikusan észleli a hardvert, telepíti a függőségeket és beállítja a brókereket:

```bash
# 1. Klónozd a repository-t
git clone https://github.com/your-org/neural-ai-next.git
cd neural-ai-next

# 2. Futtasd az egységes telepítőt (mindent automatikusan!)
python scripts/install.py

# 3. Aktiváld a környezetet
conda activate neural-ai-next

# 4. Konfiguráld a környezetet (ha szükséges)
cp .env.example .env
# Szerkeszd az .env fájlt a beállításaiddal

# 5. Indítsd a rendszert
python main.py
```

**Mit csinál a telepítő automatikusan:**
- ✅ Észleli az NVIDIA GPU-t és telepíti a CUDA-kompatibilis PyTorch-ot
- ✅ Ellenőrzi az AVX2 támogatást és telepíti az optimális adatkönyvtárakat (Polars/PyArrow vagy fastparquet)
- ✅ Létrehozza a Conda környezetet Python 3.12-vel
- ✅ Telepíti az összes függőséget (dev + trader + jupyter)
- ✅ Letölti és elindítja a bróker telepítőket (JForex4, TWS, MT5)
- ✅ Beállítja a Wine prefix-et MT5-höz

**Kézi Telepítés (Örökölt)**

Ha preferálod a kézi telepítést:

```bash
# 1. Környezet létrehozása
conda create -n neural-ai-next python=3.12 -y
conda activate neural-ai-next

# 2. PyTorch telepítése (GPU vagy CPU)
conda install -y pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia  # GPU
# VAGY
conda install -y pytorch torchvision torchaudio cpuonly -c pytorch  # CPU

# 3. Projekt függőségek telepítése
pip install -e .[dev,trader,jupyter]

# 4. Környezet konfigurálása
cp .env.example .env
# Szerkeszd az .env fájlt a beállításaiddal

# 5. Rendszer indítása
python main.py
```

### Konfiguráció

Szerkeszd az [`.env`](.env.example) fájlt a következők konfigurálásához:

- **Adatbázis:** SQLite (fejlesztés) vagy PostgreSQL (éles)
- **Brókerek:** JForex, MT5, IBKR hitelesítő adatok
- **Szimbólumok:** Kereskedési instrumentum lista
- **Naplózás:** Log szint és kimeneti formátum
- **API:** FastAPI szerver beállítások

---

## 🧪 Tesztelés

```bash
# Futtasd az összes tesztet
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest

# Futtasd coverage-zel
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest --cov=neural_ai --cov-report=html

# Futtasd specifikus tesztet
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/core/test_event_bus.py -v
```

---

## 📊 Technológiai Stack

### Core Keretrendszer
- **Python 3.12** - Modern async/await szintaxis
- **Pydantic** - Adatvalidáció és beállításkezelés
- **SQLAlchemy 2.0** - Async ORM típusbiztonsággal
- **FastAPI** - Nagy teljesítményű API szerver

### Adatfeldolgozás
- **Polars** - Villámgyors DataFrame műveletek
- **FastParquet** - Hatékony oszlopos tároló
- **VectorBT Pro** - Backtesting és portfólió elemzés

### AI/ML
- **PyTorch 2.5.1** - Deep learning keretrendszer
- **Lightning 2.5.5** - Tanítási orchestration
- **CUDA 12.1** - GPU gyorsítás

### Megfigyelhetőség
- **structlog** - Strukturált JSON naplózás
- **OpenTelemetry** - Elosztott nyomkövetés (tervezett)
- **Prometheus** - Metrikagyűjtés (tervezett)

### Üzenetküldés
- **ZeroMQ** - Nagy teljesítményű esemény busz
- **WebSockets** - Valós idejű kommunikáció
- **Redis** - Gyorsítótár és pub/sub

### Brókerek
- **JForex** - Dukascopy (Bi5 + Java Híd)
- **MT5** - MetaTrader 5 (FastAPI integráció)
- **IBKR** - Interactive Brokers (TWS API)

---

## 🏗️ Projekt Szerkezet

### 📚 Core Komponensek Dokumentációja

A teljes rendszer dokumentációja a forráskódból automatikusan generálva. Minden komponenshez tartozik részletes API dokumentáció a [`docs/components/`](docs/components/) mappában.

#### 🏛️ Alaparchitektúra
- **[Alap Komponensek Áttekintése](docs/components/core/base/index.md)** - DI Konténer, Factory, Interfészek
  - [`factory.py`](docs/components/core/base/factory.md) - Abstract Factory Pattern
  - [`implementations/`](docs/components/core/base/implementations/index.md) - DI Konténer, Komponens Csomag, Singleton, Lusta Betöltő
  - [`interfaces/`](docs/components/core/base/interfaces/index.md) - Komponens & Konténer Interfészek
  - [`exceptions/`](docs/components/core/base/exceptions/index.md) - Alap Hiba Osztályok

#### ⚙️ Konfigurációs Rendszer
- **[Konfiguráció Áttekintése](docs/components/core/config/index.md)** - Dinamikus & YAML Konfig Manager
  - [`factory.py`](docs/components/core/config/factory.md) - Konfigurációs Factory
  - [`implementations/`](docs/components/core/config/implementations/index.md) - Dinamikus & YAML Konfig Manager
  - [`interfaces/`](docs/components/core/config/interfaces/index.md) - Konfig, Async Konfig & Factory Interfészek
  - [`exceptions/`](docs/components/core/config/exceptions/index.md) - Konfigurációs Hibák

#### 📝 Naplózó Keretrendszer
- **[Naplózás Áttekintése](docs/components/core/logger/index.md)** - Strukturált Naplózó Rendszer
  - [`factory.py`](docs/components/core/logger/factory.md) - Naplózó Factory
  - [`implementations/`](docs/components/core/logger/implementations/index.md) - Színes, Alapértelmezett & Forgó Fájl Naplózók
  - [`interfaces/`](docs/components/core/logger/interfaces/index.md) - Naplózó & Factory Interfészek
  - [`formatters/`](docs/components/core/logger/formatters/index.md) - Napló Formázók
  - [`exceptions/`](docs/components/core/logger/exceptions/index.md) - Naplózási Hibák

#### 💾 Tároló Rendszer
- **[Tároló Áttekintése](docs/components/core/storage/index.md)** - Parquet & Fájl Tároló
  - [`factory.py`](docs/components/core/storage/factory.md) - Tároló Factory
  - [`implementations/`](docs/components/core/storage/implementations/index.md) - Fájl & Parquet Tároló
  - [`interfaces/`](docs/components/core/storage/interfaces/index.md) - Tároló & Factory Interfészek
  - [`backends/`](docs/components/core/storage/backends/index.md) - Polars, Pandas & Alap Backend-ek
  - [`exceptions/`](docs/components/core/storage/exceptions/index.md) - Tárolási Hibák

#### 🗄️ Adatbázis Réteg
- **[Adatbázis Áttekintése](docs/components/core/db/index.md)** - SQLAlchemy ORM & Modellek
  - [`factory.py`](docs/components/core/db/factory.md) - Adatbázis Factory
  - [`implementations/`](docs/components/core/db/implementations/index.md) - Modellek, Modell Alap & SQLAlchemy Session
  - [`exceptions/`](docs/components/core/db/exceptions/index.md) - Adatbázis Hibák

#### 📡 Esemény Rendszer
- **[Esemény Rendszer Áttekintése](docs/components/core/events/index.md)** - ZeroMQ Esemény Busz
  - [`factory.py`](docs/components/core/events/factory.md) - Esemény Busz Factory
  - [`implementations/`](docs/components/core/events/implementations/index.md) - ZeroMQ Esemény Busz
  - [`interfaces/`](docs/components/core/events/interfaces/index.md) - Esemény Busz Interfész & Esemény Modellek
  - [`exceptions/`](docs/components/core/events/exceptions/index.md) - Esemény Hibák

#### 🖥️ Rendszer Monitorozás
- **[Rendszer Áttekintése](docs/components/core/system/index.md)** - Egészségügyi Monitorozás
  - [`factory.py`](docs/components/core/system/factory.md) - Rendszer Factory
  - [`implementations/`](docs/components/core/system/implementations/index.md) - Egészségügyi Monitor
  - [`interfaces/`](docs/components/core/system/interfaces/index.md) - Egészségügyi Interfész

#### 🛠️ Segédeszközök
- **[Segédeszközök Áttekintése](docs/components/core/utils/index.md)** - Segédfunkciók & Hardver Info
  - [`factory.py`](docs/components/core/utils/factory.md) - Segédeszközök Factory
  - [`decorators.py`](docs/components/core/utils/decorators.md) - Segédeszköz Dekorátorok
  - [`implementations/`](docs/components/core/utils/implementations/index.md) - Hardver Info
  - [`interfaces/`](docs/components/core/utils/interfaces/index.md) - Hardver Interfész
  - [`exceptions/`](docs/components/core/utils/exceptions/index.md) - Segédeszköz Hibák

---

## 📈 Fejlesztési Fázisok

### Fázis 1: Core Infrastruktúra (85% Kész)
- ✅ DI Konténer
- ✅ Konfigurációs Rendszer
- ✅ Naplózó Keretrendszer
- ✅ Alap Interfészek
- 🚧 Esemény Busz
- 🔴 Adatbázis Réteg
- 🔴 Parquet Tároló

### Fázis 2: Adatgyűjtők (10% Kész)
- 🔴 JForex Bi5 Letöltő
- 🔴 MT5 FastAPI Szerver
- 🔴 Java-Python Híd
- 🔴 IBKR TWS Integráció

### Fázis 3: AI/ML Folyamat (0% Kész)
- 🔴 Hierarchikus Modellek
- 🔴 Feature Feldolgozók
- 🔴 Tanítási Folyamat
- 🔴 Inferencia Motor

### Fázis 4: Stratégia Motor (0% Kész)
- 🔴 Backtesting Keretrendszer
- 🔴 Kockázatkezelés
- 🔴 Végrehajtási Motor
- 🔴 Teljesítmény Monitorozás

**Összesített Haladás:** 35% [███████░░░░░░░░░░░░░]

---

## 🤝 Közreműködés

Ez egy tulajdonosi intézményi kereskedelmi rendszer. Minden közreműködéshez szükséges:

1. **Architektúra Felülvizsgálat** - Minden változtatásnak a specifikációkhoz kell igazodnia
2. **100% Tesztlefedettség** - Nincs kód merge teszt nélkül
3. **Dokumentáció** - Tükördokumentáció minden komponenshez
4. **Kód Felülvizsgálat** - Szenior architekt jóváhagyása szükséges

### Fejlesztési Munkafolyamat

```bash
# 1. Hozz létre feature branch-et
git checkout -b feature/your-feature

# 2. Implementáld a változtatásokat (kövesd a specifikációkat)
# 3. Írj teszteket
# 4. Frissítsd a dokumentációt (tükörszerkezet)
# 5. Futtasd a lintet
/home/elynea/miniconda3/envs/neural-ai-next/bin/ruff check

# 6. Futtasd a teszteket
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest

# 7. Commit (atomic commit-ok kötelezőek)
git add .
git commit -m "feat(scope): leírás"

# 8. Push és PR létrehozása
git push origin feature/your-feature
```

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
- **Fejlesztési Kérdések:** Lásd [Fejlesztési Útmutató](docs/development/unified_development_guide.md)

---

## 📄 Licenc

**Tulajdonosi & Bizalmas** - Neural AI Next v1.0.0

© 2025 Neural AI Next. Minden jog fenntartva.

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

**Státusz:** 🟡 Architektúra Fázis | **Utoljára Frissítve:** 2025-12-24 | **Verzió:** 1.0.0