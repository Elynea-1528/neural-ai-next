# 🧠 NEURAL AI NEXT | SYSTEM KERNEL v5.0

**Institutionális szintű, eseményvezérelt kereskedési ökoszisztéma**

---

## 📊 PROJEKT STÁTUSZ

**Állapot:** 🔴 FEJLESZTÉS ALATT  
**Verzió:** 5.0.0  
**Utolsó frissítés:** 2025-12-23

### 🎯 CÉL

Nagy teljesítményű, **Big Data (25 év+ Tick adat)** kezelésére alkalmas, **Multi-Platform (MT5, JForex, IBKR)** kereskedési rendszer létrehozása egyetlen központi [`main.py`](main.py:1) által vezérelve.

### 🏗️ ARCHITEKTÚRA

- **Eseményvezérelt (Event-Driven)** rendszer
- **Dependency Injection (DI)** konténer alapú moduláris szerkezet
- **Adatbázis** alapú konfiguráció (SQLite/Postgres)
- **Parquet** formátumú adattárolás
- **Strukturált logolás** (YAML konfigurációval)

### 📁 STRUKTÚRA

```
neural-ai-next/
├── main.py                          # 🎯 EGYETLEN BELÉPÉSI PONT
├── neural_ai/                       # Fő csomag
│   ├── core/                        # Mag komponensek
│   │   ├── base/                    # Alapinterfészek (DI, Factory, Singleton)
│   │   ├── config/                  # Konfiguráció kezelés
│   │   ├── logger/                  # Logoló rendszer
│   │   └── storage/                 # Adattárolás (Parquet)
│   ├── experts/                     # MT5 Expert Advisor-ok
│   └── [collectors|processors]/     # Adatgyűjtők és Feldolgozók
├── docs/                            # Dokumentáció
│   ├── development/                 # Fejlesztői útmutatók
│   │   ├── TASK_TREE.md            # 🎛️ VEZÉRLŐPULT (Dashboard)
│   │   ├── unified_development_guide.md
│   │   └── core_dependencies.md
│   ├── planning/specs/              # Specifikációk
│   └── architecture/                # Architektúra dokumentáció
├── tests/                           # Unit tesztek
├── configs/                         # Konfigurációs fájlok
└── scripts/                         # Segédszkriptek
```

### 🚀 FEJLESZTÉSI FÁZISOK

1.  **🟢 Phase 1: CORE INFRASTRUCTURE** (Foundation)
    - Logging, Config, Database, EventBus, Storage
    - **Állapot:** 85% kész

2.  **🟡 Phase 2: DATA COLLECTORS** (Ingestion)
    - MT5 Server, JForex Bi5 Downloader, IBKR API
    - **Állapot:** 10% kész

3.  **🔴 Phase 3: PROCESSING PIPELINE** (Analytics)
    - Event Processors, ML Modellek
    - **Állapot:** Tervezés alatt

### 📜 FEJLESZTÉSI SZABÁLYOK

- **Nyelv:** Minden kommunikáció **MAGYAR** (kivéve kód kulcsszavak)
- **Típusok:** Szigorú Type Hints (`Any` TILOS)
- **Tesztelés:** 100% coverage (`pytest`)
- **Dokumentáció:** Mirror szerkezet (doksi követi a kódot)
- **Commit:** Atomic (minden fájl után kötelező)

### 🔧 FÜGGŐSÉGEK

- **Python:** 3.10+
- **Core:** `fastapi`, `sqlalchemy`, `pydantic`, `asyncio`
- **Big Data:** `pandas`, `fastparquet`, `pyarrow`
- **Logging:** `structlog`, `colorlog`
- **Testing:** `pytest`, `pytest-asyncio`, `pytest-cov`

### 📖 DOKUMENTÁCIÓ

- **Fejlesztői útmutató:** [`docs/development/unified_development_guide.md`](docs/development/unified_development_guide.md)
- **Vezérlőpult:** [`docs/development/TASK_TREE.md`](docs/development/TASK_TREE.md)
- **Architektúra:** [`docs/architecture/overview.md`](docs/architecture/overview.md)

---

**🎯 KÖVETKEZŐ LÉPÉS:** A CORE INFRASTRUCTURE befejezése és a DATA COLLECTORS implementálása.