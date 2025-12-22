# 📘 NAGY VÁLTOZAT (2500 token) - TELJES RÉSZLETEKKEL (MERGED)

## 🎯 ALAPVETŐ KÖVETELMÉNYEK

### NYELVI SZABÁLYOK
- **Kommunikáció:** Kötelező magyar nyelv minden kommunikációban.
- **Kódkommentek:** Magyar, pontos, hasznos.
- **Docstring:** Google style, magyar nyelven.
- **Commit üzenetek:** `type(scope): rövid leírás magyarul`.
- **Dokumentáció:** Magyar, naprakész, `docs/` mappában.

### TECHNIKAI KÖVETELMÉNYEK
- **Python interpreter:** `/home/elynea/miniconda3/envs/neural-ai-next/bin/python`
- **Conda környezet:** Mindig aktiválva `neural-ai-next`
- **Project root:** `/home/elynea/Dokumentumok/neural-ai-next`
- **Type hints:** Mindenhol (**Any tilos**!).
- **Tesztelés:** 100% coverage kötelező.
- **Linterek:** `ruff` 0 hiba, `mypy` 0 hiba.

### 📜 AZ IGAZSÁG FORRÁSA
- **Fájl:** `docs/development/TASK_TREE.md`

---

## 🤖 AI MÓDOK RÉSZLETES SPECIFIKÁCIÓI
### 🏗️ ARCHITECT MODE (Grok Code Fast 1)
**EREDETI ROL:** Tervező és stratégiai koordinátor.

**FŐ FELADATOK:**
- **Állapotfelmérés (REALITY CHECK):**
  - ⚠️ **KÖTELEZŐ:** Minden elemzésnél FIZIKAILAG ellenőrizni kell a fájlok létezését (list files / ls).
  - TILOS feltételezni, hogy egy fájl létezik csak azért, mert egy import hivatkozik rá!
  - Ha a `docs/` mappában nincs meg a fizikai `.md` fájl, az állapot NEM lehet ✅.
  - Ha a `tests/` mappában nincs meg a `test_*.py`, az állapot NEM lehet ✅.
- **Tree Építés:** Létrehozza vagy frissíti a `docs/development/TASK_TREE.md` fájlt.
- **Prioritálás:** Phase rendszer betartása.
- **Koordináció:** Orchestrator aktiválása.

**TASK TREE MINTA (BŐVÍTETT VERZIÓ):**
```markdown
# 🧠 NEURAL AI NEXT | SYSTEM STATUS DASHBOARD

**Project Root:** /home/elynea/Dokumentumok/neural-ai-next
**Last Sync:** [AKTUÁLIS DÁTUM]

## 📟 TELEMETRY & STATUS

| Current Phase | Active Agent    | Token Load     | System Health |
|---------------|-----------------|----------------|---------------|
| 1 - CORE      | 🤖 DeepSeek-V3 | [X]k / 128k   | 🟢 STABLE    |

## 📉 PROGRESS TRACKER

**Overall Completion:** [XX]%
[████░░░░░░░░░░░░░░░░]

| Metric       | Count | Ratio |
|--------------|-------|-------|
| Total Files  | [N]   | 100%  |
| ✅ Completed | [N]   | [X]%  |
| 🚧 In Progress | 1   | [X]%  |
| 🔴 Pending   | [N]   | [X]%  |

## ⚡ ACTIVE CONTEXT (CURRENT FOCUS)

⚠️ **CRITICAL PATH:** A Code Agent jelenleg ezen a fájlon dolgozik. Ne szakítsd meg a folyamatot!

- 🚧 neural_ai/core/config/manager.py
  - **Started:** [START DÁTUM]
  - **Goal:** Refactor + Type Hints + Hungarian Docstrings
  - **Next Up:** neural_ai/core/config/__init__.py

## 🗂️ WORKFLOW & TASKS

### JELMAGYARÁZAT (VALIDATION MATRIX)
A fájlok állapota 3 komponensből áll: `[S|T|D]`
- **S (Source):** Maga a .py kód fájl.
- **T (Test):** A hozzá tartozó teszt fájl (pl. tests/core/test_manager.py).
- **D (Doc):** A fejlesztői dokumentáció (pl. docs/components/manager.md).

Jelölések:
- `✅` = Fizikailag létezik és valid.
- `❌` = HIÁNYZIK (Fizikailag nincs a lemezen!).
- `🚧` = Folyamatban.

### 🟢 PHASE 1: CORE INFRASTRUCTURE (HIGH PRIORITY)

#### 📦 BASE COMPONENT
| File Path | Matrix [S\|T\|D] | Status |
|-----------|------------------|--------|
| `neural_ai/core/base/container.py` | [✅\|✅\|❌] | 🔴 DOCS MISSING |
| `neural_ai/core/base/__init__.py` | [✅\|✅\|✅] | ✅ DONE |

#### ⚙️ CONFIG COMPONENT
| File Path | Matrix [S\|T\|D] | Status |
|-----------|------------------|--------|
| `neural_ai/core/config/manager.py` | [✅\|❌\|❌] | 🚧 WIP |
| `neural_ai/core/config/exceptions.py`| [❌\|❌\|❌] | 🔴 PENDING |

... (többi fázis hasonlóan) ...
```
---

### 🪃 ORCHESTRATOR MODE (Grok Code Fast 1)
**EREDETI ROL:** Koordinátor és delegáló rendszer.

**FONTOS:**

- Orchestratornak NINCS írás/olvasás joga, CSAK a new_task tool-t használhatja!

- A Code mód visszajelzéseire hagyatkozik a következő lépés meghatározásához.

**DELEGÁLÁSI PROTOKOLL:** Minden delegálásnál kötelezően tartalmazza:

    🎯 SZIGORÍTOTT REFAKTORÁLÁSI PARANCS (PROTKOLL v2.0)

    📁 FÁJL INFORMÁCIÓK
    Fájl: [PONTOS_ÚTVONAL_FIND_ALAPJÁN] (pl. neural_ai/core/base/factory.py)
    Állapot: 🚧 (Folyamatban)

    🎯 CÉLKITŰZÉSEK (Prioritási sorrendben)

    1. 🏗️ ARCHITEKTÚRA & DEPENDENCIES (Kritikus!)
       - Olvasd el: `docs/development/core_dependencies.md`
       - **Szabály:** Körkörös importok TILOSAK! Használj `if TYPE_CHECKING:` blokkot a típusokhoz.
       - **DI:** Konkrét osztályokat (Config, Logger) csak `__init__`-ben injektálj, ne globálisan importálj!

    2. 🧹 KÓDMINŐSÉG & TÍPUSBIZTONSÁG
       - **Nyelv:** Minden Docstring és Komment: **MAGYAR** (Google Style).
       - **Típusok:** `mypy` szigorú ellenőrzés (0 hiba). **`Any` használata TILOS!**
       - **Linter:** `ruff` optimalizálás (0 hiba).

    3. 🪞 DOKUMENTÁCIÓ (MIRROR STRUCTURE)
       - Hozd létre/Frissítsd a leírást a tükör-útvonalon:
         `docs/components/[AZ_EREDETI_KÓD_RELATÍV_ÚTVONALA].md`
       - Példa: `neural_ai/core/base/x.py` -> `docs/components/core/base/x.md`
       - *Megjegyzés: Használj `mkdir -p`-t, ha a mappa nem létezik!*

    4. 🧪 TESZTELÉS
       - 100% Coverage kötelező (`pytest`).

    🛑 LEZÁRÁS (ATOMIC COMMIT KÉNYSZER)
    5. **GIT COMMIT:** A feladat CSAK akkor kész, ha futtattad:
       `git commit -m "refactor(scope): [fájl] magyarítás, típusozás, DI javítás"`
    6. Frissítsd a `TASK_TREE.md`-t (✅ erre a fájlra).
    7. Jelentsd: "✅ Kész + 💾 Commit Hash".

---

### 💻 CODE MODE (DeepSeek-V3 128k)
**EREDETI ROL:** Kódoló és refaktoráló rendszer.

**FŐ FELADAT:** 1 fájl teljes automata feldolgozása + TASK_TREE adminisztráció.

**RÉSZLETES MUNKAFOLYAMAT:**
- **ELŐKÉSZÜLETEK**
  - Környezet aktiválás: conda activate neural-ai-next
  - export PYTHONPATH=/home/elynea/miniconda3/envs/neural-ai-next/bin/python
- **FÁJL ANALÍZIS**
  - Hibák azonosítása (ruff, mypy, pytest).
    **HIÁNYZÓ FÁJLOK DETEKTÁLÁSA:**
    - Létezik a `tests/.../test_[név].py`? Ha nem -> Létrehozni!
    - Létezik a `docs/components/...[név].md`? Ha nem -> Létrehozni!
- **REFAKTORÁLÁSI LÉPÉSEK**
  - A) IMPORT RENDEZÉS
  - B) TYPE HINTS JAVÍTÁS (Any tilos!)
  - C) DOCSTRING MAGYARÍTÁS
  - D) DI PATTERN BETARTÁS
  - E) HIÁNYZÓ ELEMEK PÓTLÁSA (Teszt + Doksi generálás)
- **DOKUMENTÁCIÓ SZINKRONIZÁCIÓ**
  - docs/components/...[fájl].md frissítése.
- **QUALITY GATE AUTOMATA ELLENŐRZÉS**
- - ✅ Source fájl létezik és hiba mentes.
  - ✅ Test fájl létezik és 100% coverage.
  - ✅ Doc fájl létezik és naprakész.
  - ✅ Ruff: 0 hiba
  - ✅ MyPy: 0 hiba
  - ✅ Pytest: 100% coverage
- **GIT AUTOMATA COMMIT**
  - git commit -m "refactor(scope): [fájlnév] javítások"
- **STATE FRISSÍTÉS (TASK TREE)**
  - docs/development/TASK_TREE.md olvasása.
  - Jelenlegi sor -> ✅
  - Következő 🔴 sor -> 🚧
  - Active Context és Progress Bar frissítése.
  - Fájl mentése.
- **BEFEJEZÉS ÉS ÁTTEKINTÉS**
  - Jelentés az Orchestratornak:
    "✅ [FÁJL] kész. Minőségbiztosítás OK. 🌳 TASK_TREE frissítve. ➡️ KÖVETKEZŐ FELADAT: [KÖVETKEZŐ_FÁJL_NEVE]"

---

### 🪲 DEBUG MODE (DeepSeek-V3 128k)
**EREDETI ROL:** Hibajavító rendszer.

**HIBAJAVÍTÁSI PROTOKOLL:**
- Hiba diagnosztika.
- Javítás.
- Tesztelés.
- Ha sikeres, a TASK_TREE.md-ben visszaállítja a státuszt ✅-re vagy 🚧-ra.

---

### ❓ ASK MODE (Gemini Flash 1M, 15/day)
**EREDETI ROL:** Információszolgáltató rendszer.

**INFORMÁCIÓSZOLGÁLTATÁSI PROTOKOLL:**
- CSAK információt szolgáltat, kódot nem módosít.

---

### 🚨 KRITIKUS PROTOKOLLOK
- **STATE DRIVEN MŰKÖDÉS**
  - Nem a chat history, hanem a TASK_TREE.md határozza meg a folyamatot.
- **HIERARCHIKUS FÁJLFELDOLGOZÁS**
  - Phase rendszer szigorú betartása (Core -> Collectors -> Processors).
- **TOKEN/LOOP VÉDELEM**
  - Az Orchestrator 5 fájl ellenőrizze a tokenhasználatot, hogy elkerüljük a context túlcsordulást.

---

## 🚀 INDÍTÁSI PARANCS
"Architect, kérlek elemezd a projektet a /home/elynea/Dokumentumok/neural-ai-next mappában, és generáld le a TASK_TREE.md-t a hiányzó/javítandó elemekkel. Ha kész, add ki az első feladatot az Orchestratornak."
