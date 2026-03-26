# 🦾 CLINE COMMAND FOR ROO CODE

**MÓD**: **Architect**

**FELADAT**: Teljes Projekt Architecture Audit és Konvergencia Terv

---

## 📋 KONTEXTUS

**Projekt**: Neural AI Next - Forex Trading AI rendszer
**Architecture Standards**: `docs/development/architecture_standards.md` (v4.0)
**Jelenlegi Állapot**: 295 Python fájl, vegyes minőség

**Előzetes Audit** (egyszerű script):
- 🔴 52 kritikus probléma (relatív importok, implementáció exportok)
- 🟡 82 figyelmeztetés (hiányzó mirror tesztek)
- ⚠️ **FIGYELEM**: Az egyszerű script NEM ellenőrizte a DI és DDD elveket!

---

## 🎯 FELADAT

Készíts **részletes Architecture Audit riportot** a teljes projektre, amely:

### 1. **DDD (Domain-Driven Design) Ellenőrzés**

**Réteg Hierarchia** (Architecture Standards 1.1):
```
1. Presentation (ui/)
2. Domain (processors/)
3. Persistence (data/)
4. Input (collectors/)
5. Infrastructure (core/)
```

**Ellenőrizendő:**
- ❌ Alsó réteg hivatkozik-e felső rétegre? (TILOS!)
  - Példa: `core/` NEM hivatkozhat `processors/`-ra
  - Példa: `data/` NEM hivatkozhat `ui/`-ra
- ✅ Függőségi irány helyes? (fentről lefelé)
- ✅ Rétegek tiszták? (nincs kereszthivatkozás)

**Modul Struktúra** (Architecture Standards 2.1 - The Atomic Unit):
```
xyz_module/
├── interfaces/              # ABC osztályok
│   ├── __init__.py          # Exportálja az interfészt
│   └── xyz_interface.py
├── implementations/         # Konkrét kód
│   ├── __init__.py          # ÜRES!
│   └── concrete_xyz.py
├── exceptions/              # Típusos hibák
│   ├── __init__.py
│   └── xyz_error.py
├── factory.py               # EGYETLEN importálási pont
└── __init__.py              # PUBLIKUS API (csak Interface + Factory)
```

**Ellenőrizendő:**
- ✅ Van-e `interfaces/`, `implementations/`, `exceptions/` mappa?
- ✅ Van-e `factory.py`?
- ✅ A `__init__.py` csak Interface + Factory-t exportál?
- ❌ Implementáció exportálva? (TILOS!)

---

### 2. **DI (Dependency Injection) Ellenőrzés**

**Konstruktor Injektálás** (Architecture Standards 5.1):
```python
# ❌ HELYTELEN (Hidden Dependency)
class BadService:
    def __init__(self):
        self.logger = LoggerFactory.get_logger(__name__)  # TILOS!

# ✅ HELYES (Explicit Dependency)
class GoodService:
    def __init__(self, logger: LoggerInterface, config: ConfigManagerInterface):
        self.logger = logger
        self.config = config
```

**Ellenőrizendő:**
- ❌ Service Locator használat? (TILOS!)
- ❌ Hidden dependency? (osztály példányosítja a saját függőségeit)
- ✅ Konstruktor injektálás? (logger, config paraméterek)
- ✅ Factory Pattern használat?

---

### 3. **Import Szabályok** (Architecture Standards 4)

**Abszolút Import** (Architecture Standards 4.1):
```python
# ✅ HELYES
from neural_ai.core.logger.interfaces import LoggerInterface

# ❌ TILOS
from ...core.logger.interfaces import LoggerInterface
```

**TYPE_CHECKING** (Architecture Standards 4.3):
```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from neural_ai.data.storage.interfaces import StorageInterface

class DataProcessor:
    def __init__(self, storage: "StorageInterface"):  # String hint!
        self.storage = storage
```

**Ellenőrizendő:**
- ❌ Relatív importok? (TILOS!)
- ✅ Abszolút importok?
- ✅ TYPE_CHECKING használat körkörös import esetén?

---

### 4. **Type Safety** (Architecture Standards 6)

**Pydantic Konfiguráció** (Architecture Standards 6.1):
```python
# ❌ ELAVULT (TypedDict)
from typing import TypedDict
class OldConfig(TypedDict):
    host: str

# ✅ AKTUÁLIS (Pydantic)
from pydantic import BaseModel, Field
class NewConfig(BaseModel):
    host: str = Field(..., description="Host")
```

**Ellenőrizendő:**
- ❌ TypedDict használat config célra? (ELAVULT!)
- ✅ Pydantic BaseModel használat?
- ❌ Any típus használat? (TILOS!)
- ✅ Szigorú type hints?

---

### 5. **Mirror Testing** (Architecture Standards 9.1)

**Mirror Rule**:
```
neural_ai/X/Y/module.py → tests/neural_ai/X/Y/test_module.py
```

**Ellenőrizendő:**
- ❌ Hiányzó teszt fájlok?
- ❌ Rossz nevű teszt fájlok? (nem követi a Mirror Rule-t)
- ❌ Rossz helyen lévő teszt fájlok?

---

## 📊 RIPORT FORMÁTUM

Készíts egy **részletes MD fájlt**: `docs/development/ARCHITECTURE_AUDIT_DETAILED.md`

**Struktúra:**

```markdown
# 🔍 ARCHITECTURE AUDIT REPORT (DETAILED)

**Generálva:** [Dátum]
**Elemző**: Roo Code Architect
**Szkennelt fájlok:** [Szám]

## 📊 Executive Summary

- 🔴 **Kritikus problémák:** [Szám]
  - DDD megsértések: [Szám]
  - DI hiányok: [Szám]
  - Import hibák: [Szám]
  - Type Safety: [Szám]
- 🟡 **Figyelmeztetések:** [Szám]
  - Mirror Testing: [Szám]
  - Struktúra: [Szám]

## 🔴 Kritikus Problémák (Rétegek szerint)

### 1. Infrastructure Layer (core/)

#### core/base Modul
- **Státusz**: 🔴 CRITICAL
- **DDD Problémák**:
  - [Konkrét probléma + fájl + sor]
- **DI Problémák**:
  - [Konkrét probléma + fájl + sor]
- **Import Problémák**:
  - [Konkrét probléma + fájl + sor]
- **Type Safety**:
  - [Konkrét probléma + fájl + sor]
- **Javaslatok**:
  1. [Konkrét javítási lépés]
  2. [Konkrét javítási lépés]

#### core/config Modul
...

### 2. Input Layer (collectors/)
...

### 3. Persistence Layer (data/)
...

### 4. Domain Layer (processors/)
...

### 5. Presentation Layer (ui/)
...

## 🟡 Figyelmeztetések
...

## 📋 Prioritizált Javítási Terv

### Fázis 1: Kritikus (1-3 nap)
1. core/base DI javítás
2. core/config import javítás
...

### Fázis 2: Magas (3-7 nap)
...

### Fázis 3: Közepes (1-2 hét)
...

## 📈 Metrikák

| Réteg | Fájlok | Kritikus | Figyelmeztetés | Megfelelőség |
|:------|:-------|:---------|:---------------|:-------------|
| core/ | [Szám] | [Szám] | [Szám] | [%] |
| collectors/ | [Szám] | [Szám] | [Szám] | [%] |
| data/ | [Szám] | [Szám] | [Szám] | [%] |
| processors/ | [Szám] | [Szám] | [Szám] | [%] |
| ui/ | [Szám] | [Szám] | [Szám] | [%] |
```

---

## 🎯 ELVÁRÁSOK

1. **Részletesség**: Minden problémához konkrét fájl + sor + kódpélda
2. **Prioritizálás**: Kritikus → Magas → Közepes
3. **Réteg-alapú**: Infrastructure → Input → Persistence → Domain → Presentation
4. **Javaslatok**: Konkrét javítási lépések kódpéldákkal
5. **Metrikák**: Rétegenkénti statisztika

---

## 📄 OUTPUT

**Fájl**: `docs/development/ARCHITECTURE_AUDIT_DETAILED.md`

**Formátum**: Markdown (emberi olvasható)

**Tartalom**:
- Executive Summary
- Kritikus problémák (rétegek szerint)
- Figyelmeztetések
- Prioritizált javítási terv
- Metrikák

---

## 💡 TIPPEK

1. **AST Elemzés**: Használj AST-alapú elemzést az import és DI ellenőrzéshez
2. **Kontextus**: Vedd figyelembe a modul kontextusát (réteg, függőségek)
3. **Példák**: Adj konkrét kódpéldákat a problémákhoz és megoldásokhoz
4. **Prioritás**: A kritikus problémák (DDD, DI) előrébb valók, mint a figyelmeztetések

---

**PRIORITÁS**: 🔴 KRITIKUS (Teljes projekt minőség)
