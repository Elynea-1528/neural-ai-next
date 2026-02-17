# NEURAL AI NEXT - AGENTS.md v8.0 (PROFI SZINT)

Ez a fájl a Neural AI Next projekt **ALAPTÖRVÉNYE**. Minden AI agentnek (legyen az ember vagy mesterséges intelligencia) kötelező betartania. A szabályoktól való eltérés azonnali `Build Failure`-t vagy Code Review elutasítást von maga után.

**Rendszer filozófia:** "High Performance, Strict Typing, Loose Coupling"

## 🇭🇺 NYELVI PROTOKOLL (KÖTELEZŐ)
- **Minden** kommunikáció (Chat, Commit, Docstring, Komment, Answer, Thinking, Task, Task Tree) **MAGYAR**.
- **Kivétel:** Kód kulcsszavak (def, class, import) és angol szakkifejezések (Batch, Thread, Singleton).

## 🎯 RENDSZERDEFINÍCIÓ & VÍZIÓ
- **Adat:** 25 évnyi TICK ADAT (nem OHLCV!).
- **Stack:** Python 3.12, Polars, PyTorch 2.5.1 (CUDA:12.1), Lightning 2.5.5, VectorBT Pro, FastParquet.
- **Forrás:** Dukascopy (Native .bi5 decoding), MT5, IBKR.
- **Architektúra:** Domain-Driven Design (DDD), Eseményvezérelt (ZeroMQ/AsyncIO), Adatbázis-Első.

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

## 💰 Token Economy (Hibrid Reader Stratégia)

**Cél:** A drága modellek (Architect/Code/Debug) védelme nagy fájlok olvasásától.

**Alapelv:**
- **Drága modellek (Architect, Code, Debug):** SOHA nem olvasnak fájlokat közvetlenül!
- **Search mód (Gemini Pro):** Codebase keresés, metódus/osztály definíció keresése
- **Reader mód (Flash modell):** Beolvassa az EGÉSZ fájlt (olcsó), majd intelligensen szűr
- **Eredmény:** 90%+ token megtakarítás a drága modellek kontextusában

**Döntési Fa (Mikor mit használj):**
```
Kérdés típusa:
  │
  ├─ "Hol van definiálva X?" → SEARCH mód
  ├─ "Mi az X return type-ja?" → SEARCH mód
  ├─ "Hol használják X-et?" → SEARCH mód
  ├─ "Van már Y modul?" → SEARCH mód
  │
  ├─ "Mi az X struktúrája?" → READER mód
  ├─ "Add meg X metódus kódját" → READER mód
  ├─ "Milyen importokat használ X?" → READER mód
  └─ "Hogyan néz ki X modul?" → READER mód
```

**Szabály (Egyszerű):**
1. **Drága agent:** Ha **keresés** kell → `switch_mode → search`
2. **Search:** Megkeresi a definíciót/használati helyeket
3. **Drága agent:** Ha **olvasás** kell → `switch_mode → reader`
4. **Reader:** Beolvassa az EGÉSZ fájlt, intelligensen szűr
5. **Drága agent:** `switch_mode → [eredeti mód]`
6. **Drága agent:** Feldolgozza a snippet-et (tiszta kontextus)

**Token Megtakarítás:**
- Régi: 15,000 token (drágán)
- Új: 1,500 token (drágán) + 15,000 token (olcsón)
- **Megtakarítás: 90%** ✅

### Szűrési Döntési Fa
```
Kérés érkezik
  │
  ├─ Specifikus (metódus/osztály neve)?
  │   └─ IGEN → Snippet (30-100 sor)
  │
  ├─ Általános (struktúra/API)?
  │   └─ IGEN → Teljes fájl (formázva)
  │
  ├─ Hiba kontextus (sor szám)?
  │   └─ IGEN → Snippet (±20 sor)
  │
  └─ Dokumentáció szekció?
      └─ IGEN → Snippet (releváns szekció)
```

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
