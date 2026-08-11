# NEURAL AI NEXT - AGENTS.md v8.2 (PROFI SZINT)

Ez a fájl a Neural AI Next projekt **ALAPTÖRVÉNYE**. Minden AI agentnek (legyen az ember vagy mesterséges intelligencia) kötelező betartania. A szabályoktól való eltérés azonnali `Build Failure`-t vagy Code Review elutasítást von maga után.

**Rendszer filozófia:** "High Performance, Strict Typing, Loose Coupling"

## 📚 SSOT - AZ IGAZSÁG FORRÁSAI (KÖTELEZŐ OLVASMÁNY)

Minden_agentnek (Architect, Orchestrator, Code, QA, stb.) **KÖTELEZŐEN** olvasnia kell ezeket a dokumentumokat mielőbb bármilyen feladatot vállal:

1. `ARCHITECTURE_DECISIONS.md` - **TERMÉK VÍZIÓ, DÖNTÉSEK, ROADMAP, FELHASZNÁLÁSI ÚTMUTATÓ** (ÚJ - MASTER SSOT)
2. `docs/processors/dimensions/overview.md` - Matematikai definíciók (D1-D15)
3. `docs/planning/technical_design/01_processor_architecture.md` - Rendszerterv (Pipeline L0-L4)
4. `docs/models/hierarchical/structure.md` - AI modell bemeneti igények (6 rétegű piramis)
5. `docs/architecture/hierarchical_system/overview.md` - Logikai hierarchia (L1-L6)
6. `docs/development/architecture_standards.md` - Kódolási törvény (v4.0)
7. `docs/development/custom-instructions.md` - Működési protokoll (v8.0)
8. `docs/development/TASK_TREE.md` - Aktuális állapot és Dashboard (v2.0)

**MINDEN AGENS KÖTELEZŐEN OLVASSA EZEKET A DOKUMENTUMOKAT A FELADAT KEZDETE ELŐTT.**

---

## 🇭🇺 NYELVI PROTOKOLL (KÖTELEZŐ)
- **Minden** kommunikáció (Chat, Commit, Docstring, Komment, Answer, Thinking, Task, Task Tree) **MAGYAR**.
- **Kivétel:** Kód kulcsszavak (def, class, import) és angol szakkifejezések (Batch, Thread, Singleton).

## 🎯 RENDSZERDEFINÍCIÓ & VÍZIÓ
- **Adat:** 25 évnyi TICK ADAT (nem OHLCV!).
- **Stack:** Python 3.12, Polars, PyTorch 2.5.1 (CUDA:12.1), Lightning 2.5.5, VectorBT Pro, FastParquet.
- **Forrás:** Dukascopy (Native .bi5 decoding), MT5, IBKR.
- **Architektúra:** Domain-Driven Design (DDD), Eseményvezérelt (ZeroMQ/AsyncIO), Adatbázis-Első.

## 🤔 THINKING BEFORE TOOLS (KRITIKUS!)

**TILOS** tool-t használni átgondolás nélkül!

### Gyors Checklist (MINDEN tool előtt)

Minden tool használat előtt **MENTÁLISAN** futtasd le ezt a checklistet:

```
[ ] Abszolút útvonal? (pl. `/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest`)
[ ] Paraméterek helyesek? (pl. `-n auto` → van pytest-xdist?)
[ ] Working directory? (`/home/elynea/Dokumentumok/neural-ai-next`)
[ ] Timeout elegendő? (Complex: 300s+, Simple: 60s)
[ ] Van dependency? (Tool függőségek telepítve?)
[ ] Projekt szabványok? (rules.md:278-284 betartva?)
```

### Komplex Tool-ok (execute_command, write_to_file, replace_in_file)

**KÖTELEZŐ** explicit reasoning ezekhez:

```python
"""
Reasoning (KOMPLEX TOOL):
1. ✅/❌ Abszolút útvonal: /home/elynea/.../bin/pytest
2. ✅/❌ Paraméterek: -n auto (pytest-xdist van?)
3. ✅/❌ Working directory: /home/elynea/Dokumentumok/neural-ai-next
4. ✅/❌ Timeout: 300s (integration → elég?)
5. ✅/❌ Dependencies: pytest-xdist telepítve?
6. ✅/❌ Szabványok: rules.md:278-284 betartva?
"""
<tool_use name="execute_command">
...
</tool_use>
```

### ❌ TILOS Minták (Anti-Patterns)

```bash
# ❌ ROSSZ: Relatív útvonal, hiányzó paraméterek
pytest tests/ -n auto

# ❌ ROSSZ: conda activate (nem interaktív shell)
conda activate neural-ai-next && pytest

# ✅ JÓ: Teljes, explicit, ellenőrzött
"""
Reasoning:
1. ✅ Abszolút: /home/elynea/.../bin/pytest
2. ✅ -n auto: pytest-xdist van
3. ✅ CWD: neural-ai-next root
4. ✅ Timeout: 300s
5. ✅ Dependency: OK
6. ✅ Szabvány: OK
"""
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/ -n auto -v
```

### 🚨 KRITIKUS SZABÁLY

**Ha 5 másodperc alatt nem tudod validálni → NE HASZNÁLD A TOOL-T!**

Alternatívák:
- **Egyszerű tool** (read_file, list_files) → Csak checklist
- **Komplex tool** (execute_command, write_to_file) → **Reasoning KÖTELEZŐ**
- **Bizonytalan?** → Delegálj (Reader/Search) vagy Kérdezz

## 🤔 THINKING BEFORE TOOLS (KRITIKUS!)

**TILOS** tool-t használni átgondolás nélkül!

### Gyors Checklist (MINDEN tool előtt)

Minden tool használat előtt **MENTÁLISAN** futtasd le ezt a checklistet:

```
[ ] Abszolút útvonal? (pl. `/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest`)
[ ] Paraméterek helyesek? (pl. `-n auto` → van pytest-xdist?)
[ ] Working directory? (`/home/elynea/Dokumentumok/neural-ai-next`)
[ ] Timeout elegendő? (Complex: 300s+, Simple: 60s)
[ ] Van dependency? (Tool függőségek telepítve?)
[ ] Projekt szabványok? (rules.md:278-284 betartva?)
```

### Komplex Tool-ok (execute_command, write_to_file, replace_in_file)

**KÖTELEZŐ** explicit reasoning ezekhez:

```python
"""
Reasoning (KOMPLEX TOOL):
1. ✅/❌ Abszolút útvonal: /home/elynea/.../bin/pytest
2. ✅/❌ Paraméterek: -n auto (pytest-xdist van?)
3. ✅/❌ Working directory: /home/elynea/Dokumentumok/neural-ai-next
4. ✅/❌ Timeout: 300s (integration → elég?)
5. ✅/❌ Dependencies: pytest-xdist telepítve?
6. ✅/❌ Szabványok: rules.md:432 betartva?
"""
<tool_use name="execute_command">
...
</tool_use>
```

### ❌ TILOS Minták (Anti-Patterns)

```bash
# ❌ ROSSZ: Relatív útvonal, hiányzó paraméterek
pytest tests/ -n auto

# ❌ ROSSZ: conda activate (nem interaktív shell)
conda activate neural-ai-next && pytest

# ✅ JÓ: Teljes, explicit, ellenőrzött
"""
Reasoning:
1. ✅ Abszolút: /home/elynea/.../bin/pytest
2. ✅ -n auto: pytest-xdist van
3. ✅ CWD: neural-ai-next root
4. ✅ Timeout: 300s
5. ✅ Dependency: OK
6. ✅ Szabvány: OK
"""
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/ -n auto -v
```

### 🚨 KRITIKUS SZABÁLY

**Ha 5 másodperc alatt nem tudod validálni → NE HASZNÁLD A TOOL-T!**

Alternatívák:
- **Egyszerű tool** (read_file, list_files) → Csak checklist
- **Komplex tool** (execute_command, write_to_file) → **Reasoning KÖTELEZŐ**
- **Bizonytalan?** → Delegálj (Reader/Search) vagy Kérdezz

---

## 🏛️ HIERARCHIKUS VÉGREHAJTÁSI PROTOKOLL (KÖTELEZŐ)

### Cline (Lead Developer) → Roo Code (Execution Team) Workflow

**FONTOS:** A Roo Code agensek **végrehajtó csapatként** működnek. A **Lead Developer (Cline)** adja ki a parancsokat, a Roo Code agensek végrehajtják, majd az eredményt visszaküldik ellenőrzésre.

**Workflow:**
```
1. Ember → Cline (Lead Developer): Feladat megadása
2. Cline → Elemzés, tervezés, parancs generálás
3. Cline → Parancs kimenet (pl. "Architect! Tervezd meg...")
4. Ember → Átmásolja a parancsot Roo Code-ba (megfelelő mód)
5. Roo Code Agent → Végrehajtja a feladatot
6. Roo Code Agent → Válasz kimenet
7. Ember → Átmásolja az eredményt Cline-nak
8. Cline → Ellenőrzi, értékeli, továbblép
```

**Parancs → Mód hozzárendelés:**
- "Tervezd meg..." → **Architect**
- "Készíts roadmap-et..." → **Planner**
- "Implementáld..." → **Orchestrator**
- "Hozz létre új modult..." → **Code-New**
- "Refaktoráld..." → **Code-Refactor**
- "Javítsd a bugot..." → **Code-Fix**
- "Írj tesztet..." → **Test-Unit / Test-Integration**
- "Ellenőrizd..." → **QA**
- "Commitold..." → **Commit**

### Hierarchikus Struktúra
```
1. ARCHITECT → Tervez, elemez, TASK_TREE-t vezet (NEM ír kódot!)
2. ORCHESTRATOR → Delegál, lebontja a feladatokat (NEM ír kódot!)
3. CODE → Implementál (Token Economy: Reader snippetek használata)
4. QA/TEST → Ellenőriz (Linter, Pytest)
5. COMMIT → Lezár (Atomic commit)
6. DEBUG → Javít (Csak hibákat, nem új feature-t)
7. READER → Proxy (Olcsó modell, fájl olvasás + szűrés)
```

### Felelősségi Mátrix

| Agent | Tervezés | Kód Írás | Linting | Tesztelés | Commit | Kód Olvasás |
|:------|:--------:|:--------:|:-------:|:---------:|:------:|:-----------:|
| **Architect** | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ (Reader delegálás KÖTELEZŐ) |
| **Orchestrator** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ (Reader delegálás KÖTELEZŐ) |
| **Code** | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ (Reader delegálás KÖTELEZŐ) |
| **QA** | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ (Reader delegálás ritkán) |
| **Test** | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ (Reader delegálás ritkán) |
| **Debug** | ❌ | Javít | ✅ | ✅ | ❌ | ❌ (Reader delegálás KÖTELEZŐ) |
| **Reader** | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ (Kizárólag - Intelligens szűrés) |
| **Commit** | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ (Reader delegálás ritkán) |

### Kritikus Szabályok
1. **Code Agent NEM Commit-ol:** A Code Agent csak megírja a kódot. A Commit Agent véglegesíti.
2. **QA Gate Kötelező:** Soha nincs commit QA és Test futtatása nélkül.
3. **Debug Agent csak javít:** Nem adhat hozzá új funkciót.
4. **Reader Delegálás KÖTELEZŐ:** Drága modellek (Architect, Code, Debug) SOHA nem olvasnak fájlokat közvetlenül!

### 5-Rétegű DDD Architektúra (KÖTELEZŐ TUDÁS)

A rendszer **Domain-Driven Design (DDD)** elveket követ, öt fő rétegre osztva. A függőségek iránya szigorúan **fentről lefelé** mutathat. A lenti rétegek soha nem tudhatnak a fenti rétegekről.

| Réteg | Mappa | Felelősség | Függőségek |
|:---|:---|:---|:---|
| **1. Presentation** | `neural_ai/ui` | Felhasználói interakció (Streamlit). Csak megjelenít, nem számol. | Processors, Collectors, Core |
| **2. Domain** | `neural_ai/processors` | **AZ AGY.** Tiszta üzleti logika. Dimenziók, Indikátorok, AI előkészítés. | Data, Core |
| **3. Persistence** | `neural_ai/data` | **A RAKTÁR.** Adatok mentése, betöltése, perzisztálása (Parquet, SQL). | Core |
| **4. Input** | `neural_ai/collectors` | **ÉRZÉKSZERVEK.** Külső adatok (JForex, MT5) fogadása és normalizálása. | Core |
| **5. Infrastructure** | `neural_ai/core` | **AZ ALAPOK.** Technikai keretrendszer (Log, Config, EventBus). | *Nincs (Önálló)* |

### Mappastruktúra (Canonical Tree)
```
neural_ai/
├── ui/                  # [Presentation Layer]
│   ├── pages/           # View (Streamlit oldalak)
│   ├── services/        # ViewModel (Közvetítő logika)
│   └── components/      # UI Widgetek (Charts, Cards)
├── processors/          # [Domain Layer]
│   ├── pipeline.py      # Pipeline Orchestrator (Karmester)
│   ├── resampler/       # Tick -> OHLCV transzformáció
│   └── dimensions/      # D1-D15 Elemző Logikák
├── data/                # [Persistence Layer]
│   ├── storage/         # Parquet IO (Írás/Olvasás)
│   └── ingestion/       # MarketDataPersister (Buffer & Save)
├── collectors/          # [Input Layer]
│   ├── jforex/          # Bi5 letöltő és Live Bridge
│   └── mt5/             # MetaTrader csatlakozó
└── core/                # [Infrastructure Layer]
    ├── base/            # DI Container, Singleton, Interfaces
    ├── config/          # Konfiguráció kezelés (YAML, .env)
    ├── logger/          # Strukturált naplózás (Structlog)
    ├── events/          # Eseménybusz (ZeroMQ Pub/Sub)
    ├── db/              # Adatbázis (SQLAlchemy Async)
    ├── system/          # HealthMonitor, Telemetry
    └── utils/           # HardwareInfo (AVX2), Decorators
```

### Modul Tervezési Minta (The Atomic Unit)
```
xyz_module/
├── interfaces/              # 1. A SZERZŐDÉS (Contract)
│   ├── __init__.py          # Exportálja az interfészt (ABC)
│   └── feature_interface.py # Abstract Base Class
├── implementations/         # 2. A MEGVALÓSÍTÁS (Hidden)
│   ├── __init__.py          # ÜRES! Ne exportálj innen semmit!
│   └── concrete_impl.py     # A tényleges kód
├── exceptions/              # 3. HIBAKEZELÉS (Typed)
│   ├── __init__.py
│   └── feature_error.py     # Specifikus hibák
├── factory.py               # 4. GYÁRTÓSOR (Assembly)
└── __init__.py              # 5. PUBLIKUS API (Facade)
```

### Exportálási Törvény
**TILOS** implementációt exportálni a modul gyökeréből!

```python
# ✅ HELYES (Facade):
# neural_ai/data/storage/__init__.py
from .factory import StorageFactory
from .interfaces import StorageInterface
__all__ = ['StorageFactory', 'StorageInterface']
```

### Bootstrap és Inicializációs Protokoll
**Inicializációs Lánc (Dependency Chain):**
1. **HardwareInfo** (`core.utils`) - AVX2/CUDA detektálás
2. **ConfigManager** (`core.config`) - `.env` és `yaml` betöltés
3. **Logger** (`core.logger`) - Hibaüzenetek és státusz naplózása
4. **EventBus** (`core.events`) - ZeroMQ socketek megnyitása
5. **Storage** (`data.storage`) - Backend kiválasztása hardver alapján
6. **Database** (`core.db`) - Async Engine létrehozása
7. **SystemMonitor** (`core.system`) - Health Check regisztráció

### Dependency Injection (DI) és Factory Pattern
- **Konstruktor Injektálás:** Minden függőséget a `__init__`-ben adj át
- **Service Locator TILOS:** Az osztályok nem "keresik" a függőségeiket
- **Factory Pattern:** A `factory.py` az EGYETLEN hely, ahol konkrét osztályok példányosítása történik

**Példa:**
```python
# ❌ HELYTELEN (Hidden Dependency)
class BadService:
    def __init__(self):
        self.logger = LoggerFactory.get_logger(__name__)

# ✅ HELYES (Explicit Dependency)
class GoodService:
    def __init__(self, logger: LoggerInterface, config: ConfigManagerInterface):
        self.logger = logger
        self.config = config
```

## 📚 TECHNIKAI SZABVÁNYOK (KÖTELEZŐ BETARTÁS)

### 1. Típusrendszer és Konfiguráció (Pydantic Strict Mode)
- **Pydantic Kötelező:** Konfigurációs objektumok validálására (`config.get()` eredménye) MINDIG Pydantic modellt (`BaseModel`) használj.
- **TypedDict ELAVULT:** A Pydantic helyettesíti minden konfigurációs egységnél.
- **Strict Typing:** `Any` típus használata TILOS. Minden függvény paramétert és visszatérési értéket típus hinttel kell ellátni.
- **Zéró Any Tolerancia:** Az `Any` használata TILOS a saját kódban, kivéve a legszükségesebb boundary layer eseteket.

### 2. Adatkezelés (Polars First Policy)
- **Polars (`pl.DataFrame`):** KÖTELEZŐ a `neural_ai/processors/` és `neural_ai/data/` rétegekben.
- **Pandas:** KIZÁRÓLAG a `neural_ai/ui/` rétegben engedélyezett (Streamlit kompatibilitás miatt).
- **Iteráció TILOS:** `for row in df` használata szigorúan tilos. Használj vektorizált `pl.Expr` műveleteket.

### 3. Logolás (Strukturált) és Hibakezelés
- **Formátum:** `logger.info("Üzenet", extra={"kulcs": "érték"})`
- **TILOS:** f-stringek log üzenetekben (`logger.info(f"Érték: {val}")` ❌).
- **TILOS:** `print()` utasítás használata (kivéve CLI belépési pontok `if __name__ == "__main__"` blokkjában).
- **Exception Chaining:** Soha ne nyelj el hibát üres `except`-tel. Használd a `from e` szintaxist:
```python
try:
    ...
except ValueError as e:
    raise ConfigError("Érvénytelen konfiguráció") from e
```

### 4. Import Szabályok (Import Policy)
- **Abszolút Import:** `from neural_ai.core.logger.interfaces import LoggerInterface` ✅
- **Relatív Import TILOS:** `from ...core.logger.interfaces import LoggerInterface` ❌
- **Körkörös Import:** Használd az `if TYPE_CHECKING:` blokkot és string annotációkat (`storage: "StorageInterface"`).
- **Implementáció Rejtése:** Konkrét osztályokat (`ConcreteClass`) SOHA ne importálj a modulon kívül. Csak `Interface` és `Factory` publikus.
- **Factory Pattern:** Az `implementations/` mappa tartalmát CSAK a `factory.py` importálhatja.

### 5. Fájlformátumok (Teljesítmény Optimalizálás)
- **JForex:** KIZÁRÓLAG `.bi5` (LZMA tömörített bináris). CSV/JSON használata TILOS a `neural_ai/collectors/jforex/` modulban.
- **Storage:** KIZÁRÓLAG particionált Parquet (`fastparquet`). CSV/JSON használata TILOS a `neural_ai/data/storage/` modulban.

### 6. Dokumentáció (Mirror Structure)
- **Nyelv:** MINDEN docstring, komment és commit üzenet **MAGYAR** (Google Style).
- **Mirror Dokumentáció:** Minden `neural_ai/X/Y.py` fájlhoz léteznie kell egy `docs/components/neural_ai/X/Y.md` fájlnak.

### 7. Tesztelés (Quality Gate)
- **Útvonalak:** Abszolút útvonalakat használj: `/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest`.
- **Lefedettség:** Domain réteg (Processors, Data) 100% teszt lefedettséget igényel.
- **Teszt Tükrözés:** A `tests/` mappa szerkezete bitre pontosan kövesse a projeckt szerkezetét.
- **Teszt Struktúra:** Arrange-Act-Assert pattern, leíró nevek, minimális mockolás.

#### Teszt Fájl Elnevezési Konvenció

**KRITIKUS:** A pytest collection errorok elkerülése érdekében minden teszt fájlnak **egyedi névvel** kell rendelkeznie a teljes projektben.

**Elnevezési minta:**
```
test_<modul>_<almodul>_<komponens>.py
```

**Példák:**
```
neural_ai/core/base/__init__.py
→ tests/neural_ai/core/base/test_base_init.py

neural_ai/core/base/factory.py
→ tests/neural_ai/core/base/test_base_factory.py

neural_ai/core/config/__init__.py
→ tests/neural_ai/core/config/test_config_init.py

neural_ai/core/config/factory.py
→ tests/neural_ai/core/config/test_config_factory.py
```

**TILOS:**
```
# ❌ HELYTELEN (Duplikált nevek - pytest collection error!)
tests/neural_ai/core/base/test_init.py
tests/neural_ai/core/config/test_init.py  # Ugyanaz a név!

# ❌ HELYTELEN (Duplikált nevek - pytest collection error!)
tests/neural_ai/core/base/test_factory.py
tests/neural_ai/core/config/test_factory.py  # Ugyanaz a név!
```

**Pytest Collection Error:**
Ha több teszt fájl ugyanazzal a névvel létezik különböző mappákban, a pytest az alábbi hibát dobja:
```
import file mismatch:
imported module 'test_init' has this __file__ attribute:
  /path/to/tests/neural_ai/core/base/test_init.py
which is not the same as the test file we want to collect:
  /path/to/tests/neural_ai/core/config/test_init.py
```

**Megoldás:** Használd a fenti elnevezési mintát, amely a modul hierarchiát is tartalmazza a fájlnévben.

### 8. Quality Gate (A Kapuőr)
Commitolás előtt kötelező ellenőrizni:
- **Ruff:** 0 hiba (Linting)
- **Mypy:** 0 hiba (Type Checking)
- **Pylance/Pyright:** 0 hiba (Strict Type Checking - VS Code)
- **Tests:** Minden teszt zöld
- **Coverage:** Domain réteg 100% lefedettség

### 9. Atomic Commit
- Egy commit = Egy logikai egység (Feat, Fix, Refactor, Docs)
- Üzenet formátum: `típus(scope): [Magyar üzenet]`
- Példa: `feat(processor): add d3 trend logic`

### 10. Környezeti Követelmények
- `conda activate` használata TILOS (nem interaktív shell).
- **KÖTELEZŐ** abszolút útvonalak a parancsokhoz:
  - Python: `/home/elynea/miniconda3/envs/neural-ai-next/bin/python`
  - Ruff: `/home/elynea/miniconda3/envs/neural-ai-next/bin/ruff`
  - Mypy: `/home/elynea/miniconda3/envs/neural-ai-next/bin/mypy`
  - Pyright: `/home/elynea/miniconda3/envs/neural-ai-next/bin/pyright`
  - Pytest: `/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest`

## 💰 Token Economy & Módváltási Mátrix

**Cél:** A drága modellek (Architect/Code/Debug) védelme nagy fájlok olvasásától.

**Alapelv:**
- **Drága modellek (Architect, Code, Debug):** SOHA nem olvasnak fájlokat közvetlenül!
- **Search mód (Qwen3 Coder):** Codebase keresés, metódus/osztály definíció keresése
- **Reader mód (Haiku 4.5):** Beolvassa az EGÉSZ fájlt (olcsó), majd intelligensen szűr
- **Eredmény:** 90%+ token megtakarítás a drága modellek kontextusában

**Token Megtakarítás:**
- Régi: 15,000 token (drágán)
- Új: 1,500 token (drágán) + 15,000 token (olcsón)
- **Megtakarítás: 90%** ✅

### 📊 Teljes Módváltási Táblázat

| Mód | Sikeres → | Hiba → | Olvasás → | Speciális → |
|:----|:----------|:-------|:----------|:------------|
| **Architect** | Planner, Orchestrator | - | Reader, Search | - |
| **Planner** | Architect | - | Reader, Search | - |
| **Orchestrator** | Code-*, Debug-*, Test-*, Docs-*, QA, Review, Commit | - | Reader, Search | - |
| **Code-New** | Test-Unit | Debug-Simple, Debug-Complex | Reader, Search | Docs-API |
| **Code-Feature** | Test-Unit | Debug-Simple, Debug-Complex | Reader, Search | Docs-API |
| **Code-Refactor** | Test-Integration | Debug-Complex | Reader, Search | Docs-Arch |
| **Code-Fix** | Test-Unit | Debug-Complex | Reader, Search | - |
| **Code-Optimize** | Test-E2E | Debug-Performance | Reader, Search | Docs-Comment |
| **Code-Style** | QA | - | Reader, Search | - |
| **Debug-Simple** | Test-Unit | Debug-Complex | Reader, Search | Code-Fix |
| **Debug-Complex** | Test-Integration | - | Reader, Search | Code-Refactor |
| **Debug-Performance** | Test-E2E | - | Reader, Search | Code-Optimize |
| **Test-Unit** | QA | Debug-Simple | Reader, Search | Code-Fix |
| **Test-Integration** | QA | Debug-Complex | Reader, Search | Code-Refactor |
| **Test-Property** | QA | Debug-Complex | Reader, Search | Docs-API |
| **Test-E2E** | QA | Debug-Performance, Debug-Complex | Reader, Search | Docs-Guide |
| **Docs-API** | Review | - | Reader, Search | Code-New, Code-Feature |
| **Docs-Guide** | Review | - | Reader, Search | Test-E2E |
| **Docs-Arch** | Review | - | Reader, Search | Code-Refactor |
| **Docs-Comment** | Review | - | Reader, Search | Code-* |
| **QA** | Commit | Debug-Simple, Debug-Complex, Code-Style | Reader, Search | - |
| **Review** | Commit | Code-Refactor | Reader, Search | Docs-* |
| **Commit** | KÉSZ | - | Reader, Search | - |
| **Reader** | Válaszol | - | - | - |
| **Search** | Válaszol | - | - | - |

**Alapszabály:** Minden mód (kivéve Reader/Search) SOHA nem olvas közvetlenül → Mindig Reader/Search

### 🔄 Mikor melyik módra válts?

**Olvasási Igény:**
```
"Hol van X?" / "Milyen modulok vannak?" → search
"Mi az X struktúrája?" / "Add meg X kódját" → reader
```

**Tervezési Igény:**
```
Nagy projekt (>1 hónap) → planner
Közepes/Kis projekt → orchestrator
```

**Implementációs Igény:**
```
Új modul (0→1) → code-new
Új funkció → code-feature
Refaktorálás → code-refactor
Optimalizálás → code-optimize
Formatting → code-style
```

**Hibakezelési Igény:**
```
Egyszerű (linter, import) → debug-simple
Komplex (logic, race) → debug-complex
Performance → debug-performance
```

**Tesztelési Igény:**
```
Unit → test-unit
Integration → test-integration
Property → test-property
E2E → test-e2e
```

**Dokumentációs Igény:**
```
API (docstring) → docs-api
Guide (README) → docs-guide
Arch (ADR) → docs-arch
Comment (inline) → docs-comment
```

**Minőségbiztosítási Igény:**
```
Linter/Type check → qa
Code review → review
Commit → commit
```

### 🎯 Delegálási Sablon

```
switch_mode: [target]
Üzenet: "[Mód]! [Parancs] [Részletek]"
```

### 🚨 Kritikus Módváltási Szabályok

1. **Architect/Planner/Orchestrator SOHA NEM OLVAS fájlokat** (groups: [command] vagy [read, command])
2. **Code-*/Debug-* MINDIG Reader/Search-t használ** (groups: [read, edit, command])
3. **Reader/Search SOHA NEM DELEGÁL** (csak válaszol)
4. **QA CSAK egyszerű hibákat javít** (komplex → Debug-*)
5. **Commit MINDIG utolsó lépés** (QA után)

## 🌳 TASK TREE PROTOKOLL (Granular Dashboard)
- **SSOT Template:** A projekt állapotát kizárólag a `docs/development/TASK_TREE.md` alapján vezetheted.
- **Granularitás:** Fájl szintű követés kötelező!
- **Metrika:** `[Stmt: XX% | Brch: XX%]` (Statement és Branch coverage).
- **Színkód:**
  - `🔴 CRITICAL/PENDING`: 0-49% Coverage, törött, tesztek nélkül.
  - `🟡 WIP`: 50-79% Coverage, vázlat, alacsony lefedettség.
  - `🟢 STABLE`: 80-99% Coverage, funkcionális, jó lefedettség.
  - `✅ PERFECT`: 100% Stmt / 100% Brch Coverage + Type Checked.

## 🛑 KRITIKUS SZABÁLYOK (NO-GO ZÓNA)

### 1. Memory Management (Token Védelem)
- **TILOS A TÖMÖRÍTÉS (NO CONDENSING):** Szigorúan tilos a kontextus automatikus tömörítése vagy a chat history törlése a felhasználó kifejezett utasítása nélkül! A részletek elvesztése kritikus hiba.

### 2. Context Awareness (Memorizálás)
- **TILOS** úgy generálni fájlt, hogy nem olvastad el a kapcsolódó meglévő dokumentációt!
- Ha a README.md-t írod, BE KELL LINKELNED a `docs/models` és `docs/processors` fájlokat. Nem lehet "általános" szöveg.

### 3. Mirror Structure & Atomic Commit
- **Mirror Rule:** A dokumentációnak mappaszinten követnie KELL a kódot.
  - Kód: `neural_ai/core/logger/factory.py` ➔ Dokumentáció: `docs/components/neural_ai/core/logger/factory.md`
- **Atomic Commit:** Minden egyes fájl javítása/létrehozása után `git commit` KÖTELEZŐ.
  - **Ha nincs commit, a feladat ❌ FAILED.**

---

## Build/Test/Lint Parancsok

```bash
# Tesztek futtatása abszolút útvonallal (conda activate nem működik nem-interaktív shell-ben)
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest

# Egyetlen teszt fájl futtatása
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/path/to/test_file.py -v

# Linter futtatása
/home/elynea/miniconda3/envs/neural-ai-next/bin/ruff check .

# Type checking (Mypy)
/home/elynea/miniconda3/envs/neural-ai-next/bin/mypy neural_ai

# Type checking (Pyright - CLI verzió a Pylance-hez)
/home/elynea/miniconda3/envs/neural-ai-next/bin/pyright

# Alkalmazás módok futtatása
python main.py live                    # Élő kereskedési mód
python main.py download --symbol EURUSD --start 2024-03-20 --end 2024-03-20
python main.py dashboard               # Streamlit UI
```

---

**Ez a szabvány a projekt bibliája. Ha a kód eltér ettől, a kód a hibás. Nincs kivétel.**
