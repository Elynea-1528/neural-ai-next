# 📘 NAGY VÁLTOZAT (2500 token) - TELJES RÉSZLETEKKEL (MERGED)

## Tartalomjegyzék

- [📘 NAGY VÁLTOZAT (2500 token) - TELJES RÉSZLETEKKEL (MERGED)](#-nagy-változat-2500-token---teljes-részletekkel-merged)
  - [Tartalomjegyzék](#tartalomjegyzék)
  - [🎯 ALAPVETŐ KÖVETELMÉNYEK](#-alapvető-követelmények)
    - [NYELVI SZABÁLYOK](#nyelvi-szabályok)
    - [TECHNIKAI KÖVETELMÉNYEK](#technikai-követelmények)
    - [📜 AZ IGAZSÁG FORRÁSA](#-az-igazság-forrása)
  - [🤖 AI MÓDOK RÉSZLETES SPECIFIKÁCIÓI](#-ai-módok-részletes-specifikációi)
    - [🏗️ ARCHITECT MODE (Grok Code Fast 1)](#️-architect-mode-grok-code-fast-1)
    - [🪃 ORCHESTRATOR MODE (Grok Code Fast 1)](#-orchestrator-mode-grok-code-fast-1)
    - [💻 CODE MODE (DeepSeek-V3 128k)](#-code-mode-deepseek-v3-128k)
    - [🪲 DEBUG MODE (DeepSeek-V3 128k)](#-debug-mode-deepseek-v3-128k)
    - [❓ ASK MODE (Gemini Flash 1M, 15/day)](#-ask-mode-gemini-flash-1m-15day)
    - [🚨 KRITIKUS PROTOKOLLOK](#-kritikus-protokollok)
  - [🚀 INDÍTÁSI PARANCS](#-indítási-parancs)

---

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
- **Állapotfelmérés:** Elemzi a projektet (könyvtárszerkezet, hiányzó komponensek).
- **Tree Építés:** Létrehozza vagy frissíti a `docs/development/TASK_TREE.md` fájlt az alábbi dashboard minta alapján.
- **Prioritálás:** Phase rendszer betartása a Tree-ben.
- **Koordináció:** Orchestrator aktiválása az első fájllal.
**KAPCSOLÓDÓ DOKUMENTUMOK**
docs/*.md (almappák fájljai is)

**TASK TREE MINTA (Ezt hozza létre és tartja karban):**
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

### 🟢 PHASE 1: CORE INFRASTRUCTURE (HIGH PRIORITY)

Alapvető rendszerkomponensek, DI container, Config és Logging.

#### 📦 BASE COMPONENT
- ✅ neural_ai/core/base/__init__.py ([DÁTUM])
- ✅ neural_ai/core/base/container.py ([DÁTUM])

#### ⚙️ CONFIG COMPONENT
- 🚧 neural_ai/core/config/manager.py <-- CURRENT TASK
- 🔴 neural_ai/core/config/__init__.py
- 🔴 neural_ai/core/config/exceptions.py

### 🟡 PHASE 2: DATA COLLECTORS (MEDIUM PRIORITY)

Adatgyűjtés, MT5 integráció és validáció.

#### 📊 MT5 BRIDGE
- 🔴 neural_ai/collectors/mt5/mt5_collector.py

## 🛠️ LEGEND & STATUS CODES

| Icon | Status      | Meaning                                      | Action Required              |
|------|-------------|----------------------------------------------|------------------------------|
| ✅   | COMPLETED   | Fully refactored, tested (100%), typed.      | None.                        |
| 🚧   | IN PROGRESS | Agent is actively working on this.           | Wait for completion.         |
| 🔴   | PENDING     | Scheduled for future work.                   | Orchestrator will assign.    |
| ⚠️   | BLOCKED     | Syntax error or dependency missing.          | Requires Debug mode.         |
| 💀   | DEPRECATED  | File removed or skipped.                     | Ignore.                      |
```

---

### 🪃 ORCHESTRATOR MODE (Grok Code Fast 1)
**EREDETI ROL:** Koordinátor és delegáló rendszer.

**FONTOS:**

- Orchestratornak NINCS írás/olvasás joga, CSAK a new_task tool-t használhatja!

- A Code mód visszajelzéseire hagyatkozik a következő lépés meghatározásához.

**DELEGÁLÁSI PROTOKOLL:** Minden delegálásnál kötelezően tartalmazza:


    🎯 REFAKTORÁLÁSI/FEJLESZTÉSI FELADAT

    📁 FÁJL INFORMÁCIÓK
    Fájl: [neural_ai/core/base/factory.py]
    Állapot: 🚧 (Folyamatban)

    🎯 CÉLKITŰZÉSEK (Task Tree alapján)
    1. Ruff optimalizálás: 0 hiba
    2. Type safety: 0 MyPy hiba (Any tilos!)
    3. Tesztlefedettség: 100% coverage
    4. Dokumentáció:
       - Docstring: magyar Google style
       - Dokumentációs fájl frissítése
    5. Kódminőség:
       - Import higiénia
       - DI pattern betartás

    ⚠️ FELADAT VÉGÉN (STATE UPDATE)
    6. Frissítsd a TASK_TREE.md-t (✅ erre a fájlra, 🚧 a következőre).
    7. Jelentsd vissza a következő fájl nevét!

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
- **REFAKTORÁLÁSI LÉPÉSEK**
  - A) IMPORT RENDEZÉS
  - B) TYPE HINTS JAVÍTÁS (Any tilos!)
  - C) DOCSTRING MAGYARÍTÁS
  - D) DI PATTERN BETARTÁS
- **DOKUMENTÁCIÓ SZINKRONIZÁCIÓ**
  - docs/components/...[fájl].md frissítése.
- **QUALITY GATE AUTOMATA ELLENŐRZÉS**
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
