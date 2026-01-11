# 🏗️ Neural AI Next - Architecture Standards

## 📋 Tartalomjegyzék

1. [Modularitás és Mappaszerkezet](#1-modularitás-és-mappaszerkezet)
2. [Core Architektúra](#2-core-architektúra)
3. [Dependency Injection (DI) Szabályok](#3-dependency-injection-di-szabályok)
4. [Típuskezelés (Type Hints)](#4-típuskezelés-type-hints)
5. [Linter Szigorú Alkalmazása](#5-linter-szigorú-alkalmazása)
6. [Tesztelés Követelmények](#6-tesztelés-követelmények)
7. [Dokumentáció Mirror Structure](#7-dokumentáció-mirror-structure)
8. [Atomic Commit Protokoll](#8-atomic-commit-protokoll)

---

## 1. Modularitás és Mappaszerkezet

### 1.1 Alapelvek

Minden modul (`neural_ai/core/xyz`) **SZIGORÚAN** kövesse ezt a szerkezetet:

```
neural_ai/core/xyz/
├── __init__.py              # ⚠️ CSAK Factory-t és Interface-t exportál!
├── factory.py               # Az EGYETLEN belépési pont
├── interfaces/              # Abstract Base Classes (ABC)
│   ├── __init__.py
│   └── xyz_interface.py
├── implementations/         # Konkrét implementációk
│   ├── __init__.py
│   └── concrete_impl.py
├── exceptions/              # Saját hibák
│   ├── __init__.py
│   └── xyz_error.py
└── backends/                # Opcionális: backend-specifikus kód
    ├── __init__.py
    └── backend_impl.py
```

### 1.2 `__init__.py` Explicit Export Szabálya

**⚠️ KRITIKUS SZABÁLY:** Minden `__init__.py` fájl kizárólag a **Factory-t** és a **publikus Interface-t** exportálhatja. Tilos bármilyen implementációt, konstanst vagy belső osztályt direktben exportálni.

#### ✅ HELYES PÉLDA:

```python
# neural_ai/core/logger/__init__.py
from neural_ai.core.logger.factory import LoggerFactory
from neural_ai.core.logger.interfaces import ILogger, ILoggerFactory

__all__ = ['LoggerFactory', 'ILogger', 'ILoggerFactory']
```

#### ❌ TILOS PÉLDA:

```python
# ❌ TILOS: Implementáció exportálása
from neural_ai.core.logger.implementations import ColoredLogger

__all__ = ['ColoredLogger']  # TILOS!
```

```python
# ❌ TILOS: Konstans exportálása
from neural_ai.core.logger.constants import LOG_LEVELS

__all__ = ['LOG_LEVELS']  # TILOS!
```

**Indoklás:** Az `__init__.py` célja a **publikus API** definiálása. A felhasználónak nem szabad tudnia a belső implementációkról. A Factory pattern biztosítja a lazacsatolást, ezért csak az interfészek és a factory legyenek láthatóak.

---

## 2. Core Architektúra

### 2.1 Core Gyökér Bootstrap Központ

A `neural_ai/core` mappa a rendszer **bootstrap központja**, ahol minden modul a saját Factory-jén keresztül inicializálódik, és a DI container biztosítja a függőségeket.

#### Architektúra Diagram:

```
┌─────────────────────────────────────────────────────────────┐
│                    neural_ai/core/__init__.py               │
│                  (Bootstrap Entry Point)                     │
└───────────────────────┬─────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
┌───────────────┐ ┌───────────────┐ ┌───────────────┐
│   Config      │ │    Logger     │ │      DB       │
│   Factory     │ │   Factory     │ │   Factory     │
└───────┬───────┘ └───────┬───────┘ └───────┬───────┘
        │                 │                 │
        ▼                 ▼                 ▼
┌───────────────┐ ┌───────────────┐ ┌───────────────┐
│ DI Container  │ │ DI Container  │ │ DI Container  │
│ (injects      │ │ (injects      │ │ (injects      │
│  dependencies)│ │  dependencies)│ │  dependencies)│
└───────────────┘ └───────────────┘ └───────────────┘
```

#### Bootstrap Folyamat:

1. **Application Start:** A `main.py` meghívja a `neural_ai.core.__init__.py`-t.
2. **Factory Initialization:** Minden modul Factory-je létrehozza a DI containert.
3. **Dependency Registration:** A DI container regisztrálja az összes szükséges függőséget (Config, Logger, DB session, stb.).
4. **Dependency Injection:** A Factory-k konstruktor injection-nel átadják a függőségeket az implementációknak.
5. **Service Locator:** A core modul elérhetővé teszi a Factory-ket a teljes rendszer számára.

#### Példa Bootstrap Kód:

```python
# neural_ai/core/__init__.py
from neural_ai.core.base import DIContainer
from neural_ai.core.config import ConfigFactory
from neural_ai.core.logger import LoggerFactory
from neural_ai.core.db import DatabaseFactory

# Globális DI Container (Singleton)
_container = DIContainer()

# Függőségek regisztrálása
_container.register(IConfig, ConfigFactory.create())
_container.register(ILogger, LoggerFactory.create())
_container.register(IDatabase, DatabaseFactory.create())

# Publikus API
def get_config() -> IConfig:
    return _container.resolve(IConfig)

def get_logger() -> ILogger:
    return _container.resolve(ILogger)

def get_database() -> IDatabase:
    return _container.resolve(IDatabase)
```

---

## 3. Dependency Injection (DI) Szabályok

### 3.1 Szigorú Constructor Injection

**Minden osztály** kötelezően kapja meg a függőségeit **konstruktor paramétereken** keresztül. Tilos a direkt példányosítás vagy a globális importok.

#### ✅ HELYES PÉLDA:

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from neural_ai.core.logger.interfaces import ILogger
    from neural_ai.core.config.interfaces import IConfig

class MyService:
    def __init__(self, logger: ILogger, config: IConfig):
        self._logger = logger
        self._config = config
    
    def do_something(self):
        self._logger.info("Service működik")
```

#### ❌ TILOS PÉLDAK:

```python
# ❌ TILOS: Globális import és direkt használat
from neural_ai.core.logger import LoggerFactory

class MyService:
    def __init__(self):
        self._logger = LoggerFactory.create()  # TILOS!
```

```python
# ❌ TILOS: Direkt példányosítás
from neural_ai.core.logger.implementations import ColoredLogger

class MyService:
    def __init__(self):
        self._logger = ColoredLogger()  # TILOS!
```

### 3.2 Factory Pattern Kötelező Használata

Minden modulnak **kizárólag** a saját Factory-jén keresztül szabad példányokat létrehoznia.

#### Példa Factory:

```python
# neural_ai/core/logger/factory.py
from neural_ai.core.logger.interfaces import ILogger, ILoggerFactory
from neural_ai.core.logger.implementations import ColoredLogger, DefaultLogger
from neural_ai.core.base import DIContainer

class LoggerFactory(ILoggerFactory):
    @staticmethod
    def create(logger_type: str = "default") -> ILogger:
        container = DIContainer.get_instance()
        config = container.resolve(IConfig)
        
        if logger_type == "colored":
            return ColoredLogger(config)
        else:
            return DefaultLogger(config)
```

### 3.3 DI Container Használata

A DI Container felelős a függőségek életciklusáért és injektálásáért.

#### DI Container Implementáció:

```python
# neural_ai/core/base/implementations/di_container.py
from typing import Dict, Type, Any

class DIContainer:
    _instance = None
    _registry: Dict[Type, Any] = {}
    
    @staticmethod
    def get_instance():
        if DIContainer._instance is None:
            DIContainer._instance = DIContainer()
        return DIContainer._instance
    
    def register(self, interface: Type, implementation: Any):
        self._registry[interface] = implementation
    
    def resolve(self, interface: Type) -> Any:
        if interface not in self._registry:
            raise ValueError(f"Nincs regisztrálva implementáció: {interface}")
        return self._registry[interface]
```

---

## 4. Típuskezelés (Type Hints)

### 4.1 Strict Type Hints Kötelező

**Minden függvénynek és metódusnak** legyen pontos típusannotációja. Az `Any` típus használata **SZIGORÚAN TILOS**.

#### ✅ HELYES PÉLDA:

```python
from typing import List, Dict, Optional, Union

def process_data(
    data: List[Dict[str, Union[str, int]]],
    config: Optional[IConfig] = None
) -> Dict[str, int]:
    result = {}
    # ... feldolgozás
    return result
```

#### ❌ TILOS PÉLDA:

```python
from typing import Any

def process_data(data: Any, config: Any = None) -> Any:  # TILOS!
    pass
```

### 4.2 Helyes Használat: `Optional`, `List`, `Dict`, `cast`

#### `Optional` használata:

```python
from typing import Optional

def find_user(user_id: int) -> Optional[User]:
    if user_id in database:
        return database[user_id]
    return None  # ✅ Valid
```

#### `cast` használata típuskonverzióhoz:

```python
from typing import cast

def parse_response(response: Dict[str, Any]) -> UserData:
    # Típuskonverzió, ha biztosak vagyunk a formátumban
    return cast(UserData, response)
```

### 4.3 `TYPE_CHECKING` Blokk Körkörös Importokhoz

Ha körkörös import probléma merül fel, használj `TYPE_CHECKING` blokkot.

#### Példa:

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from neural_ai.core.logger.interfaces import ILogger
    from neural_ai.core.config.interfaces import IConfig

class MyService:
    def __init__(self, logger: ILogger, config: IConfig):
        self._logger = logger
        self._config = config
```

**Indoklás:** A `TYPE_CHECKING` blokkban lévő importok csak a típusellenőrzéskor futnak le, így elkerülve a körkörös import problémákat.

---

## 5. Linter Szigorú Alkalmazása

### 5.1 Ruff Használata

A projekt **kizárólag** a [Ruff](https://github.com/astral-sh/ruff) lintert használja a kódminőség biztosításához.

### 5.2 Ruff Konfiguráció

A Ruff konfiguráció a `pyproject.toml`-ban található:

```toml
[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "C",   # flake8-comprehensions
    "B",   # flake8-bugbear
    "N",   # pep8-naming
    "UP",  # pyupgrade
]
ignore = []

[tool.ruff.lint.isort]
known-first-party = ["neural_ai"]
```

### 5.3 0 Hiba Követelmény

**Minden commit előtt** a Ruff-nak **0 hibát** kell mutatnia. A fejlesztés során futtasd a lintelést gyakran.

### 5.4 Futtatási Parancsok Abszolút Útvonalakkal

**⚠️ KÖTELEZŐ:** A parancsokat mindig abszolút útvonalakkal futtasd!

#### Lintelés:

```bash
/home/elynea/miniconda3/envs/neural-ai-next/bin/ruff check .
```

#### Automatikus javítás:

```bash
/home/elynea/miniconda3/envs/neural-ai-next/bin/ruff check . --fix
```

#### Formázás:

```bash
/home/elynea/miniconda3/envs/neural-ai-next/bin/ruff format .
```

---

## 6. Tesztelés Követelmények

### 6.1 Pytest Használata

A projekt a [pytest](https://docs.pytest.org/) keretrendszert használja tesztelésre.

### 6.2 100% Coverage Követelmény

**Minden új kódnak** el kell érnie a **100% Statement (S) és 100% Branch (B) coverage-t**.

#### Coverage Metrika:

```
Coverage: [Stmt: 100% | Brch: 100%]
```

### 6.3 Tesztfájl Struktúra

A tesztfájlok a `tests/` mappában helyezkednek el, és **tükrözik a forráskód szerkezetét**:

```
tests/
├── core/
│   ├── base/
│   │   ├── test_factory.py
│   │   └── test_container.py
│   ├── config/
│   │   ├── test_config_interface.py
│   │   └── implementations/
│   │       └── test_yaml_config_manager.py
│   └── db/
│       └── test_session.py
└── integration/
    └── test_end_to_end.py
```

### 6.4 Commit Előtti Kötelező Ellenőrzés

**Minden commit előtt** kötelező a tesztek futtatása és a sikeres lefutásuk.

#### Teszt Futtatása:

```bash
# Teljes tesztcsomag
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest

# Egy adott tesztfájl
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/core/base/test_factory.py

# Coverage report-pal
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest --cov=neural_ai --cov-report=term-missing
```

#### Tesztelési Protokoll:

1. **Írd meg a kódot.**
2. **Írd meg a teszteket.**
3. **Futtasd a teszteket:** `pytest -v`
4. **Ellenőrizd a coverage-t:** `pytest --cov=neural_ai --cov-report=term-missing`
5. **Ha minden teszt sikeres ÉS 100% coverage:** Mehet a commit.
6. **Ha a teszt bukik:** Javítsd a kódot vagy a tesztet, majd ismételd a folyamatot.

---

## 7. Dokumentáció Mirror Structure

### 7.1 `docs/components/` Mappastruktúra

A dokumentációnak **tükrönie kell** a forráskód mappaszerkezetét.

#### Példa Mirror Structure:

```
Forráskód:                          Dokumentáció:
neural_ai/                          docs/components/
├── core/                           ├── neural_ai/
│   ├── __init__.py                 │   ├── core/
│   ├── base/                       │   │   ├── __init__.md
│   │   ├── factory.py              │   │   ├── factory.md
│   │   └── interfaces/             │   │   └── interfaces/
│   │       └── component.py        │   │       └── component.md
│   ├── config/                     │   ├── config/
│   │   ├── factory.py              │   │   ├── factory.md
│   │   └── implementations/        │   │   └── implementations/
│   │       └── yaml_manager.py     │   │       └── yaml_manager.md
│   └── db/                         │   └── db/
│       └── session.py              │       └── session.md
└── experts/                        └── experts/
    └── mt5/                            └── mt5/
        └── expert.mq5                      └── expert.md
```

### 7.2 Kötelező Mirror Szabály

**Minden forráskód fájlnak** meg kell jelennie a dokumentációban a megfelelő helyen. A dokumentáció célja a kód funkcionalitásának, architektúrájának és használatának részletes leírása.

### 7.3 Dokumentáció Frissítés

**Minden kódmódosítás után** kötelező a megfelelő dokumentáció frissítése.

#### Dokumentációs Sablon:

```markdown
# [Fájlnév] - [Rövid leírás]

## 🎯 Cél és Feladat

[Mi a fájl célja és fő feladata?]

## 🏗️ Architektúra

[Osztálydiagram vagy architektúrai leírás]

## 🔧 Használat

### Példa Kód

```python
from neural_ai.core.config import ConfigFactory

config = ConfigFactory.create()
value = config.get("database.host")
```

## 📝 API Referencia

[Függvények és osztályok listája]

## 🐛 Hibakezelés

[Gyakori hibák és megoldásaik]
```

---

## 8. Atomic Commit Protokoll

### 8.1 Git Commit Szabályok

**Minden egyes funkcionalitás vagy javítás** külön commitban kell legyen. Tilos több változást egy commitba csomagolni.

### 8.2 Commit Üzenet Formátum

A commit üzeneteknek kötelezően követniük kell az alábbi formátumot:

```
<type>(<scope>): <subject>

<body>
```

#### Típusok (Type):

- `feat`: Új funkció
- `fix`: Hibajavítás
- `refactor`: Kód refaktorálás (nincs funkcionalitás változás)
- `docs`: Dokumentáció változás
- `test`: Tesztek hozzáadása vagy javítása
- `chore`: Build folyamat vagy segédeszközök változása
- `style`: Formázás (nincs kód változás)
- `perf`: Teljesítmény javítás

#### Scope:

A módosított modul neve (pl. `config`, `logger`, `db`, `storage`).

#### Példák:

```
feat(config): YAML config manager implementáció

- YAML fájl betöltés és validálás
- Environment változók felülírásának támogatása
- Tesztek 100% coverage-ral
```

```
fix(debug): EventBus memory leak javítás

- ZeroMQ socketek helyes lezárása
- AsyncIO taskok cancellálása
- Tesztek frissítve
```

```
docs(standards): architecture standards bővítése DI, típusok, linter, tesztelés, docs, commit protokoll

- Új szakaszok hozzáadva a DI, típuskezelés, linter, tesztelés, dokumentáció és commit protokollhoz
- Példakódok illusztrálva
- Formázás ellenőrizve
```

### 8.3 Tranzakcionális Mentés Csak Sikeres Tesztek Után

**⚠️ KRITIKUS SZABÁLY:** Commitot **CSAK** akkor szabad létrehozni, ha minden teszt sikeresen lefutott.

#### Commit Folyamat:

1. **Kód írása és módosítása.**
2. **Tesztelés:** `pytest -v`
3. **Coverage ellenőrzés:** `pytest --cov=neural_ai --cov-report=term-missing`
4. **Lintelés:** `ruff check .`
5. **Ha minden sikeres:**
   ```bash
   git add <módosított fájlok>
   git commit -m "<type>(<scope>): <subject>"
   git push
   ```
6. **Ha valami hibás:** Javítsd ki, majd ismételd a folyamatot.

### 8.4 Atomic Commit Előnyei

- **Könnyű visszavonás:** Ha egy commit hibás, egyszerűen visszavonható.
- **Tiszta történet:** A git history könnyen követhető és érthető.
- **Jobb code review:** A review-k fókuszáltabbak lehetnek.
- **Kisebb kockázat:** A kis, izolált változtatások kevésbé vezetnek váratlan hibákhoz.

---

## 📚 Összefoglalás

Ez a dokumentum a Neural AI Next projekt architektúra szabványait definiálja. Minden fejlesztőnek kötelező betartania ezeket a szabályokat a kódminőség, a karbantarthatóság és a csapatmunka érdekében.

**Kulcsszabályok emlékeztető:**

1. ✅ **Modularitás:** Minden modul követi az `interfaces/`, `implementations/`, `exceptions/`, `factory.py` szerkezetet.
2. ✅ **DI Pattern:** Szigorú constructor injection, Factory használata, tiltott globális importok.
3. ✅ **Típusok:** Strict type hints, `Any` tilos, `TYPE_CHECKING` blokk körkörös importokhoz.
4. ✅ **Linter:** Ruff 0 hiba, abszolút útvonalak használata.
5. ✅ **Tesztelés:** 100% Stmt és Branch coverage, commit előtt kötelező ellenőrzés.
6. ✅ **Dokumentáció:** Mirror structure a `docs/components/`-ban.
7. ✅ **Commit:** Atomic commit, formális üzenet, csak sikeres tesztek után.

Adat Elnevezés:
bid_open, bid_close... -> Kereskedéshez / Chart.
mid_open, mid_close... -> AI Tanításhoz / Elemzéshez.
open, close -> TILOS a backendben (túl kétértelmű). Csak a UI rétegben engedélyezett (display only).

**Utolsó frissítés:** 2025-12-25