# 🏛️ NEURAL AI NEXT - ARCHITECTURE STANDARDS v4.0 (THE ULTIMATE CODEX)

**Verzió:** 4.0 (Post-DDD Refactor) | **Státusz:** ✅ ÉLŐ | **Enforcement:** STRICT (Zéró Tolerancia)

---

## 📜 PREAMBULUM
Ez a dokumentum a Neural AI Next rendszer fejlesztésének **ALAPTÖRVÉNYE**. Minden fejlesztőnek (legyen az ember vagy AI) kötelező betartania. A szabályoktól való eltérés azonnali `Build Failure`-t vagy Code Review elutasítást von maga után.

A rendszer filozófiája: **"High Performance, Strict Typing, Loose Coupling"**.

---

## 📋 TARTALOMJEGYZÉK

1.  [Rendszerarchitektúra és Hierarchia (Global Map)](#1-rendszerarchitektúra-és-hierarchia-global-map)
2.  [Modul Tervezési Minta (The Atomic Unit)](#2-modul-tervezési-minta-the-atomic-unit)
3.  [Bootstrap és Inicializációs Protokoll](#3-bootstrap-és-inicializációs-protokoll)
4.  [Importálási Szabványok (Import Policy)](#4-importálási-szabványok-import-policy)
5.  [Dependency Injection (DI) és Factory Pattern](#5-dependency-injection-di-és-factory-pattern)
6.  [Típusbiztonság és Konfiguráció (Strict Mode)](#6-típusbiztonság-és-konfiguráció-strict-mode)
7.  [Adatfeldolgozás és Processzorok (Polars Engine)](#7-adatfeldolgozás-és-processzorok-polars-engine)
8.  [Megfigyelhetőség (Logging & Telemetry)](#8-megfigyelhetőség-logging--telemetry)
9.  [Minőségbiztosítási Protokoll (QA)](#9-minőségbiztosítási-protokoll-qa)

---

## 1. RENDSZERARCHITEKTÚRA ÉS HIERARCHIA (GLOBAL MAP)

A rendszer **Domain-Driven Design (DDD)** elveket követ, négy fő rétegre osztva. A függőségek iránya szigorúan **fentről lefelé** mutathat. A lenti rétegek soha nem tudhatnak a fenti rétegekről.

### 1.1 Rétegek (Layers)

| Réteg | Mappa | Felelősség | Függőségek |
|:---|:---|:---|:---|
| **1. Presentation** | `neural_ai/ui` | Felhasználói interakció (Streamlit). Csak megjelenít, nem számol. | Processors, Collectors, Core |
| **2. Domain** | `neural_ai/processors` | **AZ AGY.** Tiszta üzleti logika. Dimenziók, Indikátorok, AI előkészítés. | Data, Core |
| **3. Persistence** | `neural_ai/data` | **A RAKTÁR.** Adatok mentése, betöltése, perzisztálása (Parquet, SQL). | Core |
| **4. Input** | `neural_ai/collectors` | **ÉRZÉKSZERVEK.** Külső adatok (JForex, MT5) fogadása és normalizálása. | Core |
| **5. Infrastructure** | `neural_ai/core` | **AZ ALAPOK.** Technikai keretrendszer (Log, Config, EventBus). | *Nincs (Önálló)* |

### 1.2 Mappastruktúra (Canonical Tree)

```text
neural_ai/
├── ui/                  # [Presentation Layer]
│   ├── pages/           # View (Streamlit oldalak)
│   ├── services/        # ViewModel (Közvetítő logika)
│   └── components/      # UI Widgetek (Charts, Cards)
│
├── processors/          # [Domain Layer]
│   ├── pipeline.py      # Pipeline Orchestrator (Karmester)
│   ├── resampler/       # Tick -> OHLCV transzformáció
│   └── dimensions/      # D1-D15 Elemző Logikák
│       ├── d01_price/
│       ├── d02_support/
│       └── d03_trend/
│
├── data/                # [Persistence Layer]
│   ├── storage/         # Parquet IO (Írás/Olvasás)
│   └── ingestion/       # MarketDataPersister (Buffer & Save)
│
├── collectors/          # [Input Layer]
│   ├── jforex/          # Bi5 letöltő és Live Bridge
│   └── mt5/             # MetaTrader csatlakozó
│
└── core/                # [Infrastructure Layer]
    ├── base/            # DI Container, Singleton, Interfaces
    ├── config/          # Konfiguráció kezelés (YAML, .env)
    ├── logger/          # Strukturált naplózás (Structlog)
    ├── events/          # Eseménybusz (ZeroMQ Pub/Sub)
    ├── db/              # Adatbázis (SQLAlchemy Async)
    ├── system/          # HealthMonitor, Telemetry
    └── utils/           # HardwareInfo (AVX2), Decorators
```

---

## 2. MODUL TERVEZÉSI MINTA (THE ATOMIC UNIT)

Minden funkcionális egységnek (pl. `data/storage` vagy `processors/resampler`) követnie kell a **Szétválasztott Implementáció (Separated Interface)** mintát. Ez teszi lehetővé a cserélhetőséget és a tesztelhetőséget.

### 2.1 Belső Mappaszerkezet

```text
xyz_module/
├── interfaces/              # 1. A SZERZŐDÉS (Contract)
│   ├── __init__.py          # Exportálja az interfészt (ABC)
│   └── feature_interface.py # Abstract Base Class
│
├── implementations/         # 2. A MEGVALÓSÍTÁS (Hidden)
│   ├── __init__.py          # ÜRES! Ne exportálj innen semmit!
│   └── concrete_impl.py     # A tényleges kód
│
├── exceptions/              # 3. HIBAKEZELÉS (Typed)
│   ├── __init__.py
│   └── feature_error.py     # Specifikus hibák
│
├── factory.py               # 4. GYÁRTÓSOR (Assembly)
│                            # Az EGYETLEN hely, ami ismeri az implementációt.
│
└── __init__.py              # 5. PUBLIKUS API (Facade)
                             # Csak az Interfészt és a Factory-t exportálja.
```

### 2.2 Exportálási Törvény (`__init__.py`)
**TILOS** implementációt exportálni a modul gyökeréből. A külvilág számára az implementáció láthatatlan kell legyen.

#### ✅ HELYES (Facade):
```python
# neural_ai/data/storage/__init__.py
from .factory import StorageFactory
from .interfaces import StorageInterface

__all__ = ['StorageFactory', 'StorageInterface']
```

---

## 3. BOOTSTRAP ÉS INICIALIZÁCIÓS PROTOKOLL

A rendszer nem véletlenszerűen indul. A `neural_ai.core.bootstrap_core()` függvény felel a komponensek determinisztikus, függőségi sorrendben történő felépítéséért.

**Inicializációs Lánc (Dependency Chain):**

1.  **HardwareInfo (`core.utils`):**
    *   *Függőség:* Nincs.
    *   *Cél:* Detektálja az AVX2/CUDA képességeket az optimalizációhoz.
2.  **ConfigManager (`core.config`):**
    *   *Függőség:* Nincs.
    *   *Cél:* Betölti a `.env` és `yaml` fájlokat.
3.  **Logger (`core.logger`):**
    *   *Függőség:* Config (Log level).
    *   *Cél:* Hibaüzenetek és státusz naplózása.
4.  **EventBus (`core.events`):**
    *   *Függőség:* Config (Portok), Logger.
    *   *Cél:* ZeroMQ socketek megnyitása.
5.  **Storage (`data.storage`):**
    *   *Függőség:* Config, Logger, HardwareInfo.
    *   *Cél:* Backend (Polars/Pandas) kiválasztása hardver alapján.
6.  **Database (`core.db`):**
    *   *Függőség:* Config (Connection String), Logger.
    *   *Cél:* Async Engine létrehozása.
7.  **SystemMonitor (`core.system`):**
    *   *Függőség:* Mindenki más.
    *   *Cél:* Health Check regisztráció.

---

## 4. IMPORTÁLÁSI SZABVÁNYOK (IMPORT POLICY)

A refaktorálhatóság és a `pylance` stabilitása érdekében szigorú import szabályok érvényesek.

### 4.1 Abszolút Import Szabály
A modulokon keresztüli hivatkozásnál **KÖTELEZŐ** az abszolút útvonal használata.

*   ✅ **HELYES:** `from neural_ai.core.logger.interfaces import LoggerInterface`
*   ❌ **TILOS:** `from ...core.logger.interfaces import LoggerInterface`

### 4.2 Relatív Import Kivétel
Relatív import (`.`, `..`) kizárólag **csomagon belül** (intra-package) engedélyezett, például az `__init__.py`-ban, vagy amikor egy implementáció importálja a saját kivételeit.

### 4.3 Type Checking Import (Circular Dependency)
A körkörös hivatkozások elkerülése érdekében (pl. Interface <-> Implementation) használd a `TYPE_CHECKING` blokkot és string-hivatkozást.

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # Ez az import nem fut le runtime-ban, csak a linter látja
    from neural_ai.data.storage.interfaces import StorageInterface

class DataProcessor:
    # Stringként hivatkozunk a típusra
    def __init__(self, storage: "StorageInterface"):
        self.storage = storage
```

---

## 5. DEPENDENCY INJECTION (DI) ÉS FACTORY PATTERN

A kódnak "Service Locator" mentesnek kell lennie. Az osztályok nem "keresik" a függőségeiket, hanem "megkapják" azokat.

### 5.1 Konstruktor Injektálás
Minden függőséget a konstruktorban (`__init__`) kell átadni. Az osztály nem példányosíthatja a saját loggerét vagy configját.

#### ❌ HELYTELEN (Hidden Dependency):
```python
class BadService:
    def __init__(self):
        # A logger a "semmiből" jön -> Tesztelhetetlen!
        self.logger = LoggerFactory.get_logger(__name__)
```

#### ✅ HELYES (Explicit Dependency):
```python
class GoodService:
    def __init__(self, logger: LoggerInterface, config: ConfigManagerInterface):
        self.logger = logger
        self.config = config
```

### 5.2 Factory Pattern Felelőssége
A `factory.py` az **egyetlen** hely, ahol:
1.  A `DIContainer` használata engedélyezett.
2.  A konkrét osztályok (`ConcreteClass`) példányosítása történik.
3.  A `TypedDict` alapú konfiguráció validálása és castolása zajlik.

---

## 6. TÍPUSBIZTONSÁG ÉS KONFIGURÁCIÓ (STRICT MODE)

A rendszer `python.analysis.typeCheckingMode: "strict"` alatt fut. Ez nem javaslat, ez követelmény.

### 6.1 Config TypedDict (KÖTELEZŐ!)
A `config.get()` metódus alapból `Any` típust ad vissza, ami strict módban hiba. Minden konfigurációs objektumhoz definiálni kell egy `TypedDict`-et a Factory-ban.

```python
from typing import TypedDict, cast, NotRequired

# 1. Struktúra definíció
class JForexConfig(TypedDict, total=False):
    base_url: str
    timeout: int
    enabled: bool

# 2. Biztonságos kinyerés a Factory-ban
raw_config = config.get("jforex")
# Castoljuk a nyers dict-et a definiált típusra
typed_cfg = cast(JForexConfig, raw_config if isinstance(raw_config, dict) else {})

# 3. Típusos használat
timeout = typed_cfg.get("timeout", 30)  # Pylance tudja: ez int!
```

### 6.2 Zéró `Any` Tolerancia
Az `Any` használata **TILOS** a saját kódban, kivéve a legszükségesebb boundary layer (pl. JSON parsing) eseteket, de ott is azonnal `cast`-olni kell. Minden függvény paraméterének és visszatérési értékének típusosnak kell lennie.

---

## 7. ADATFELDOLGOZÁS ÉS PROCESSZOROK (POLARS ENGINE)

### 7.1 Polars First Policy
Minden nagy tömegű adatfeldolgozás (Resampler, Dimenziók) **Polars DataFrame** (`pl.DataFrame`) alapú.
*   **Pandas:** Csak a UI rétegben (megjelenítéshez) használható.
*   **Iteráció:** `for row in df` használata **TILOS** a processzorokban. Használj `pl.Expr`-t a vektorizált műveletekhez.

### 7.2 Processzor Hierarchia
*   **Pipeline Orchestrator:** (`pipeline.py`) - Ez hívja meg sorban a processzorokat.
*   **Resampler:** (Tick -> OHLCV). Ez az első lépés.
*   **D1 (Base Data):** Általános indikátorok (Z-Score, Returns).
*   **D2-D15 (Specialized):** Specifikus üzleti logika.

### 7.3 Adatáramlás (The Flow)
1.  Bemenet: `Time Aligned OHLCV DataFrame`.
2.  Feldolgozás: `IDimensionProcessor.process()`.
3.  Kimenet: `Feature DataFrame` (ugyanannyi sorral, mint a bemenet, új oszlopokkal).

---

## 8. LOGOLÁS, HIBAKEZELÉS ÉS MEGFIGYELHETŐSÉG

### 8.1 Nincs Print
A `print()` utasítás használata a `neural_ai/` mappában **TILOS** (kivéve CLI toolok `if __name__ == "__main__"` blokkját). Minden kimenetnek a Loggeren keresztül kell mennie.

### 8.2 Strukturált Logolás
Használd az `extra` paramétert a kontextus átadására. Ne fűzz össze stringeket!

```python
# HELYTELEN:
logger.info(f"Feldolgozva: {count} sor, symbol: {symbol}")

# HELYES (Structured - JSON-ben kereshető lesz):
logger.info("Feldolgozás kész", extra={"rows": count, "symbol": symbol})
```

### 8.3 Hibakezelés (Exception Chaining)
Soha ne nyelj el hibát üres `except`-tel. Használd a `from e` szintaxist az eredeti hiba megőrzésére, hogy a Traceback ne vesszen el.

```python
try:
    ...
except ValueError as e:
    raise ConfigError("Érvénytelen konfiguráció") from e
```

---

## 9. MINŐSÉGBIZTOSÍTÁSI PROTOKOLL (QA)

### 9.1 Teszt Tükrözés (Mirror Testing)
A `tests/` mappa szerkezete bitre pontosan kövesse a `neural_ai/` szerkezetét.
*   Source: `neural_ai/processors/dimensions/d01_price/processor.py`
*   Test: `tests/processors/dimensions/d01_price/test_processor.py`

### 9.2 Quality Gate (A Kapuőr)
Commitolás előtt kötelező ellenőrizni:
1.  **Ruff:** 0 hiba (Linting).
2.  **Pylance:** 0 hiba (Strict Type Checking).
3.  **Tests:** Minden teszt zöld.
4.  **Coverage:** Törekedj a 100%-ra, de a kritikus üzleti logikánál (Processors, Data) ez kötelező.

### 9.3 Atomic Commit
Egy commit = Egy logikai egység (Feat, Fix, Refactor, Docs). Soha ne keverd a formázást a logikai módosítással egy commitban. Az üzenet legyen konvencionális: `feat(processor): add d3 trend logic`.

---

**Ez a szabvány a projekt bibliája. Ha a kód eltér ettől, a kód a hibás. Nincs kivétel.**
```