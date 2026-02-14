# 🏛️ Hierarchikus Agent Rendszer - Neural AI Next

**Verzió:** 3.0 (25 Mód) | **Státusz:** ✅ AKTÍV | **Dátum:** 2026-02-05

---

## 📋 Áttekintés

A Neural AI Next projekt 25 specializált AI ágensrendszert használ. A rendszer célja a felelősségi körök szigorú szétválasztása (Separation of Concerns) és a token költség optimalizálás.

**Roo Code = Végrehajtó Csapat:** A Roo Code agensek a **Lead Developer (Cline)** parancsait hajtják végre. Cline elemzi a feladatot, kiad egy parancsot, a Roo Code agent végrehajtja, majd az eredményt visszaküldi Cline-nak ellenőrzésre.

---

## 🎯 25 Mód Hierarchikus Struktúra

```
┌─────────────────────────────────────────────────────────────────┐
│                    🏗️ TERVEZÉSI RÉTEG (2)                        │
├─────────────────────────────────────────────────────────────────┤
│  1. ARCHITECT    → Rendszertervezés, DDD, TASK_TREE vezetés     │
│  2. PLANNER      → Stratégiai tervezés, roadmap, milestone      │
└────────────────────────┬────────────────────────────────────────┘
                         │ Delegál
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    🎼 KOORDINÁCIÓ (1)                            │
├─────────────────────────────────────────────────────────────────┤
│  3. ORCHESTRATOR → Feladat koordináció, delegálás               │
└────────────────────────┬────────────────────────────────────────┘
                         │ Utasít
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                 💻 IMPLEMENTÁCIÓS RÉTEG (6)                      │
├─────────────────────────────────────────────────────────────────┤
│  4. CODE-NEW       → Új modul létrehozás (0→1)                  │
│  5. CODE-REFACTOR  → Komplex refaktorálás, architektúra változás│
│  6. CODE-FEATURE   → Új funkció hozzáadás meglévő modulhoz      │
│  7. CODE-FIX       → Egyszerű bugfix, typo, import hiba         │
│  8. CODE-OPTIMIZE  → Performance optimalizálás                  │
│  9. CODE-STYLE     → Formatting, import rendezés, style guide   │
└────────────────────────┬────────────────────────────────────────┘
                         │ Dokumentál
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                  📝 DOKUMENTÁCIÓS RÉTEG (4)                      │
├─────────────────────────────────────────────────────────────────┤
│ 10. DOCS-API       → Docstring, API referencia                  │
│ 11. DOCS-GUIDE     → README, tutorial, getting started          │
│ 12. DOCS-ARCH      → Architektúra dokumentáció, design decisions│
│ 13. DOCS-COMMENT   → Inline kommentek, TODO/FIXME/NOTE          │
└────────────────────────┬────────────────────────────────────────┘
                         │ Tesztel
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   🧪 TESZTELÉSI RÉTEG (4)                        │
├─────────────────────────────────────────────────────────────────┤
│ 14. TEST-UNIT        → Unit tesztek, egyszerű funkciók          │
│ 15. TEST-INTEGRATION → Integration tesztek, modulok interakció  │
│ 16. TEST-PROPERTY    → Property-based testing, invariant        │
│ 17. TEST-E2E         → End-to-end tesztek, teljes rendszer flow │
└────────────────────────┬────────────────────────────────────────┘
                         │ Ellenőriz
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                  🔧 KARBANTARTÁSI RÉTEG (3)                      │
├─────────────────────────────────────────────────────────────────┤
│ 18. DEBUG-SIMPLE     → Linter hibák, import problémák           │
│ 19. DEBUG-COMPLEX    → Logic hibák, race condition, memory leak │
│ 20. DEBUG-PERFORMANCE→ Performance bottleneck, profiling        │
└────────────────────────┬────────────────────────────────────────┘
                         │ QA Gate
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   📖 TÁMOGATÓ RÉTEG (5)                          │
├─────────────────────────────────────────────────────────────────┤
│ 21. QA             → Linter futtatás, type check, egyszerű hibák│
│ 22. REVIEW         → Kód review, best practices, javaslatok     │
│ 23. SEARCH         → Codebase keresés, pattern matching         │
│ 24. COMMIT         → Git commit, atomic commit, conventional    │
│ 25. READER         → Fájl olvasás, szűrés, context hygiene      │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Munkafolyamat Példák

### 1. Új Modul Létrehozás:
```
ARCHITECT → ORCHESTRATOR → CODE-NEW → DOCS-API → TEST-UNIT → QA → COMMIT
```

### 2. Komplex Refaktorálás:
```
ARCHITECT → ORCHESTRATOR → CODE-REFACTOR → DOCS-ARCH → TEST-INTEGRATION → DEBUG-COMPLEX → QA → COMMIT
```

### 3. Egyszerű Bugfix:
```
ORCHESTRATOR → CODE-FIX → TEST-UNIT → QA → COMMIT
```

### 4. Performance Optimalizálás:
```
ORCHESTRATOR → CODE-OPTIMIZE → TEST-E2E → DEBUG-PERFORMANCE → QA → COMMIT
```

---

## 📜 Felelősségi Mátrix (25 Mód)

| Mód | Modell | Thinking | Felelősség | Reader Használat |
|:----|:-------|:---------|:-----------|:-----------------|
| **architect** | Opus 4.5 | extrahigh | Rendszertervezés, DDD, TASK_TREE | KÖTELEZŐ |
| **planner** | Opus 4.5 | extrahigh | Stratégiai tervezés, roadmap | KÖTELEZŐ |
| **orchestrator** | Sonnet 4.5 | high | Feladat koordináció, delegálás | KÖTELEZŐ |
| **code-new** | Sonnet 4.5 | high | Új modul létrehozás (0→1) | KÖTELEZŐ |
| **code-refactor** | Opus 4.5 | extrahigh | Komplex refaktorálás | KÖTELEZŐ |
| **code-feature** | Sonnet 4.5 | high | Új funkció hozzáadás | KÖTELEZŐ |
| **code-fix** | Gemini Pro | high | Egyszerű bugfix | KÖTELEZŐ |
| **code-optimize** | Opus 4.5 | extrahigh | Performance optimalizálás | KÖTELEZŐ |
| **code-style** | Gemini Flash | high | Formatting, style guide | Ritkán |
| **docs-api** | Gemini Pro | high | Docstring, API referencia | KÖTELEZŐ |
| **docs-guide** | Sonnet 4.5 | high | Tutorial, getting started | KÖTELEZŐ |
| **docs-arch** | Opus 4.5 | extrahigh | Architektúra dokumentáció | KÖTELEZŐ |
| **docs-comment** | Gemini Flash | high | Inline kommentek | Ritkán |
| **test-unit** | Gemini Pro | high | Unit tesztek | KÖTELEZŐ |
| **test-integration** | Sonnet 4.5 | high | Integration tesztek | KÖTELEZŐ |
| **test-property** | Opus 4.5 | extrahigh | Property-based testing | KÖTELEZŐ |
| **test-e2e** | Sonnet 4.5 | high | End-to-end tesztek | KÖTELEZŐ |
| **debug-simple** | Gemini Pro | high | Linter hibák | KÖTELEZŐ |
| **debug-complex** | Opus 4.5 | extrahigh | Logic hibák | KÖTELEZŐ |
| **debug-performance** | Opus 4.5 | extrahigh | Performance bottleneck | KÖTELEZŐ |
| **qa** | Gemini Flash | high | Linter, type check, egyszerű hibák | Ritkán |
| **review** | Sonnet 4.5 | high | Kód review, best practices | KÖTELEZŐ |
| **search** | Gemini Pro | high | Codebase keresés | NEM (csak search tools) |
| **commit** | Gemini Flash | high | Git commit | Ritkán |
| **reader** | Gemini Flash | high | Fájl olvasás, szűrés | N/A (ő maga a Reader) |

---

## 🛑 Kritikus Szabályok

1. **Specializáció:** Minden mód CSAK a saját felelősségi körét látja el
2. **Delegálás:** Drága modellek (Opus, Sonnet) SOHA nem olvasnak fájlokat közvetlenül
3. **QA Gate:** Soha nincs commit QA és Test futtatása nélkül
4. **Reader Használat:** KÖTELEZŐ minden fájl olvasáshoz (kivéve mechanikus módok)
5. **Atomic Commit:** Egy commit = Egy logikai egység

---

## 💰 Token Economy - Reader Delegálási Lánc

### Alapelv: Hibrid Reader Stratégia

**Cél:** 90%+ token megtakarítás a drága modellek kontextusában.

**Munkafolyamat:**

```
Drága Agent (Architect/Code/Debug)
  │
  ├─ Fájl olvasás szükséges?
  │   │
  │   └─ IGEN → switch_mode → reader
  │       │
  │       └─ Reader (Flash modell)
  │           │
  │           ├─ Beolvassa az EGÉSZ fájlt (olcsó)
  │           │
  │           ├─ Intelligens szűrés:
  │           │   ├─ Specifikus kérés → Snippet (30-100 sor)
  │           │   ├─ Általános kérés → Teljes fájl (formázva)
  │           │   ├─ Hiba kontextus → Snippet (±20 sor)
  │           │   └─ Dokumentáció → Snippet (szekció)
  │           │
  │           └─ Visszaküldi a snippet-et
  │               │
  │               └─ switch_mode → [eredeti mód]
  │                   │
  │                   └─ Drága Agent: Feldolgozza a snippet-et
  │                       (Kontextusa tiszta, csak 50 sor)
```

### Token Megtakarítás Példa:

**Forgatókönyv:** Code Agent módosít egy 500 soros fájlt

| Módszer | Reader Token | Drága Token | Teljes | Megtakarítás |
|:---|---:|---:|---:|---:|
| **Régi (közvetlen)** | 0 | 15,000 | 15,000 | - |
| **Új (Reader proxy)** | 15,000 (olcsó) | 1,500 | 16,500 | **90%** (drágán) |

**Eredmény:** Ugyanaz a módosítás, de 90% token megtakarítás a drága modell kontextusában! ✅

---

## 📊 Modell Allokáció Összesítés

| Modell | Thinking | Módok (Darab) | Felelősség |
|:-------|:---------|:--------------|:-----------|
| **Opus 4.5** | extrahigh | 7 | Kritikus döntések |
| **Sonnet 4.5** | high | 8 | Implementáció |
| **Gemini Pro** | high | 5 | Rutin feladatok |
| **Gemini Flash** | high | 5 | Mechanikus feladatok |

---

## 📚 Dokumentáció Hivatkozások

- **Fő szabályzat:** `AGENTS.md` (minden agent látja - auto cache)
- **Mód-specifikus szabályok:** `.roo/rules-*/AGENTS.md` (csak az adott mód látja)
- **Konfiguráció:** `.roomodes` (25 mód definíciója)

---

## 🎯 Következő Lépések

1. **Roo Code Konfiguráció:** Manuálisan beállítani a 25 módot a Roo Code UI-ban
2. **Tesztelés:** Minden mód kipróbálása egyszerű feladatokkal
3. **Finomhangolás:** Szükség esetén mód-specifikus AGENTS.md frissítése


---

## 🔄 Cline (Lead Developer) → Roo Code (Execution Team) Workflow

### Szerepkörök:

- **Ember (Te):** Projekt tulajdonos, döntéshozó
- **Cline (Lead Developer):** Elemzi a feladatot, tervez, parancsot generál, ellenőriz
- **Roo Code (Execution Team):** Végrehajtja a parancsokat, visszajelzést ad

### Munkafolyamat:

```
┌─────────────────────────────────────────────────────────────┐
│  1. EMBER → Cline: "Hozz létre D6 Volatility processzort"  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  2. Cline (Lead Dev): Elemzi, tervezi, parancsot generál   │
│     Output: "Architect! Tervezd meg a D6 Volatility..."    │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  3. EMBER: Átmásolja a parancsot Roo Code-ba (Architect)   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  4. Roo Code (Architect): Végrehajtja, tervet készít       │
│     Output: [Terv, struktúra, fájlok listája]              │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  5. EMBER: Átmásolja az eredményt Cline-nak                │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  6. Cline: Ellenőrzi, értékeli, következő lépés            │
│     Output: "Jó terv! Most implementálás..."               │
│     "Orchestrator! Implementáld az Architect tervét..."     │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
                    [Ismétlés]
```

### Parancs → Mód Hozzárendelés:

| Cline Parancs Típusa | Roo Code Mód | Példa |
|:---------------------|:-------------|:------|
| "Tervezd meg..." | **Architect** | "Architect! Tervezd meg a D6 Volatility processzort" |
| "Készíts roadmap-et..." | **Planner** | "Planner! Készíts roadmap-et a Q1 fejlesztésekhez" |
| "Implementáld..." | **Orchestrator** | "Orchestrator! Implementáld az Architect tervét" |
| "Hozz létre új modult..." | **Code-New** | "Code-New! Hozz létre D6 Volatility modult" |
| "Refaktoráld..." | **Code-Refactor** | "Code-Refactor! Refaktoráld a pipeline.py-t" |
| "Javítsd a bugot..." | **Code-Fix** | "Code-Fix! Javítsd az AttributeError-t" |
| "Optimalizáld..." | **Code-Optimize** | "Code-Optimize! Gyorsítsd a resampler-t" |
| "Írj unit tesztet..." | **Test-Unit** | "Test-Unit! Írj tesztet a calculate() metódushoz" |
| "Írj integration tesztet..." | **Test-Integration** | "Test-Integration! Teszteld a pipeline flow-t" |
| "Ellenőrizd a kódot..." | **QA** | "QA! Futtasd a linter-t és javítsd a hibákat" |
| "Commitold..." | **Commit** | "Commit! Commitold a D6 Volatility modult" |

### Előnyök:

1. **Cline (Lead Dev)** → Stratégiai döntések, tervezés, ellenőrzés
2. **Roo Code (Execution)** → Végrehajtás, implementáció, tesztelés
3. **Ember (Te)** → Döntéshozás, irányítás, jóváhagyás

**Eredmény:** Hatékony, ellenőrzött, minőségi fejlesztés! 🚀

