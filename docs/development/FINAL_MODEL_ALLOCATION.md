# 🎯 VÉGLEGES Model Allokáció (Teljes Áttekintés)

**Verzió:** 5.0 FINAL | **Dátum:** 2026-02-12

**Egységes API Key:** `Narzie2012rohaN` (minden mód ugyanazt használja)

---

## 📊 Teljes Beállítási Táblázat (25 Mód)

| # | Mód | Model | API | Reasoning | Effort | Temp | Max Tokens | Context | Indoklás |
|:--|:----|:------|:----|:----------|:-------|:-----|:-----------|:--------|:---------|
| 1 | architect | claude-opus-4-6-thinking | Kiro | ✅ | xhigh | 0.7 | 8000 | 200k | Komplex architektúra, magas kreativitás |
| 2 | planner | kiro-claude-sonnet-4-5-agentic | Kiro | ✅ | high | 0.7 | 8000 | 200k | Roadmap, multi-step reasoning |
| 3 | orchestrator | kiro-claude-sonnet-4-5-agentic | Kiro | ✅ | high | 0.5 | 8000 | 200k | Koordináció, agentic reasoning |
| 4 | code-new | kiro-deepseek-3-2 | Kiro | ✅ | high | 0.3 | 8000 | 200k | Új modul, egyszerű implementáció |
| 5 | code-refactor | claude-opus-4-6-thinking | Kiro | ✅ | xhigh | 0.3 | 8000 | 200k | Komplex refaktorálás |
| 6 | code-feature | kiro-deepseek-3-2 | Kiro | ✅ | high | 0.3 | 8000 | 200k | Feature, egyszerű implementáció |
| 7 | code-fix | gemini-3-pro-high | Kiro | ✅ | high | 0.2 | 8000 | 1M | Bugfix, determinisztikus |
| 8 | code-optimize | claude-opus-4-6-thinking | Kiro | ✅ | xhigh | 0.3 | 8000 | 200k | Teljesítmény optimalizálás |
| 9 | code-style | gemini-3-flash | Kiro | ❌ | - | 0.1 | 4000 | 1M | Formázás, mechanikus |
| 10 | docs-api | gemini-3-pro-high | Kiro | ✅ | high | 0.5 | 8000 | 1M | API dokumentáció |
| 11 | docs-guide | kiro-claude-sonnet-4-5 | Kiro | ✅ | high | 0.6 | 8000 | 200k | Tutorial, kreativitás |
| 12 | docs-arch | claude-opus-4-6-thinking | Kiro | ✅ | xhigh | 0.6 | 8000 | 200k | Architektúra dokumentáció |
| 13 | docs-comment | gemini-3-flash | Kiro | ❌ | - | 0.4 | 4000 | 1M | Inline kommentek, mechanikus |
| 14 | test-unit | gemini-3-pro-high | Kiro | ✅ | high | 0.3 | 8000 | 1M | Unit tesztek |
| 15 | test-integration | kiro-claude-sonnet-4-5 | Kiro | ✅ | high | 0.3 | 8000 | 200k | Integrációs tesztek |
| 16 | test-property | claude-opus-4-6-thinking | Kiro | ✅ | xhigh | 0.3 | 8000 | 200k | Property-based testing |
| 17 | test-e2e | kiro-claude-sonnet-4-5 | Kiro | ✅ | high | 0.3 | 8000 | 200k | E2E tesztek |
| 18 | debug-simple | gemini-3-pro-high | Kiro | ✅ | high | 0.2 | 8000 | 1M | Egyszerű debug |
| 19 | debug-complex | claude-opus-4-6-thinking | Kiro | ✅ | xhigh | 0.3 | 8000 | 200k | Komplex debug |
| 20 | debug-performance | claude-opus-4-6-thinking | Kiro | ✅ | xhigh | 0.3 | 8000 | 200k | Teljesítmény debug |
| 21 | qa | gemini-3-flash | Kiro | ❌ | - | 0.2 | 4000 | 1M | Linter, mechanikus |
| 22 | review | kiro-claude-sonnet-4-5 | Kiro | ✅ | high | 0.5 | 8000 | 200k | Code review |
| 23 | search | gemini-3-pro-high | Kiro | ✅ | high | 0.3 | 8000 | 1M | Codebase keresés |
| 24 | commit | gemini-3-flash | Kiro | ❌ | - | 0.2 | 4000 | 1M | Commit üzenet, mechanikus |
| 25 | reader | gemini-3-flash | Kiro | ❌ | - | 0.3 | 4000 | 1M | Fájl olvasás, mechanikus |

---

## 🎯 Model Elosztás Összefoglaló

### Claude Opus 4.6 Thinking (7 mód) - KRITIKUS FELADATOK
**Kvóta:** Korlátozott (Antigravity)
**Reasoning:** xhigh
**Temperature:** 0.3-0.7

| Mód | Temp | Feladatkör |
|:----|:-----|:-----------|
| architect | 0.7 | Architektúra tervezés |
| code-refactor | 0.3 | Refaktorálás |
| code-optimize | 0.3 | Optimalizálás |
| docs-arch | 0.6 | Architektúra dokumentáció |
| test-property | 0.3 | Property-based testing |
| debug-complex | 0.3 | Komplex debug |
| debug-performance | 0.3 | Teljesítmény debug |

### Kiro Claude Sonnet 4.5 (6 mód) - KOORDINÁCIÓ & DOKUMENTÁCIÓ
**Kvóta:** Korlátozott (Kiro)
**Reasoning:** high
**Temperature:** 0.3-0.7

| Mód | Model Variant | Temp | Feladatkör |
|:----|:--------------|:-----|:-----------|
| planner | agentic | 0.7 | Roadmap készítés |
| orchestrator | agentic | 0.5 | Koordináció |
| docs-guide | sima | 0.6 | Tutorial írás |
| test-integration | sima | 0.3 | Integrációs tesztek |
| test-e2e | sima | 0.3 | E2E tesztek |
| review | sima | 0.5 | Code review |

### Kiro DeepSeek 3.2 (2 mód) - KÓD ÍRÁS
**Kvóta:** Korlátozott (Kiro)
**Reasoning:** high
**Temperature:** 0.3

| Mód | Model Variant | Feladatkör |
|:----|:--------------|:-----------|
| code-new | sima | Új modul létrehozása |
| code-feature | sima | Feature hozzáadás |

### Gemini 3 Pro High (5 mód) - RUTIN FELADATOK
**Kvóta:** Bőséges
**Reasoning:** high
**Temperature:** 0.2-0.5

| Mód | Temp | Feladatkör |
|:----|:-----|:-----------|
| code-fix | 0.2 | Bugfix |
| docs-api | 0.5 | API dokumentáció |
| test-unit | 0.3 | Unit tesztek |
| debug-simple | 0.2 | Egyszerű debug |
| search | 0.3 | Codebase keresés |

### Gemini 3 Flash (5 mód) - MECHANIKUS FELADATOK
**Kvóta:** Bőséges
**Reasoning:** disabled
**Temperature:** 0.1-0.4

| Mód | Temp | Feladatkör |
|:----|:-----|:-----------|
| code-style | 0.1 | Formázás |
| docs-comment | 0.4 | Inline kommentek |
| qa | 0.2 | Linter futtatás |
| commit | 0.2 | Commit üzenet |
| reader | 0.3 | Fájl olvasás |

---

## 🔑 Kritikus Döntések Magyarázata

### 1. Agentic Suffix (2 mód)
**KELL:**
- **planner:** Roadmap = multi-step reasoning (több fázis tervezése)
- **orchestrator:** Koordináció = több feladat összehangolása

**NEM KELL:**
- **code-new:** Új modul = egyszerű implementáció (egy feladat)
- **code-feature:** Feature = egyszerű implementáció (nem koordináció)

### 2. Reasoning Effort
**xhigh (7 mód):** Komplex architektúra döntések, multi-layer problémák
**high (13 mód):** Normál döntéshozatal, reasoning szükséges
**disabled (5 mód):** Mechanikus feladatok, nincs döntés

### 3. Temperature
**0.1-0.2 (5 mód):** Maximális determinizmus (bugfix, mechanikus)
**0.3 (12 mód):** Alacsony kreativitás (kód írás, tesztek)
**0.4-0.5 (4 mód):** Közepes kreativitás (koordináció, review)
**0.6-0.7 (4 mód):** Magas kreativitás (tervezés, dokumentáció)

---

## 📊 Kvóta Optimalizálás

### Korlátozott Kvóta (15 mód):
- **Antigravity Opus (7):** Kritikus döntések
- **Kiro Sonnet (6):** Koordináció, dokumentáció
- **Kiro DeepSeek (2):** Kód írás

### Bőséges Kvóta (10 mód):
- **Gemini Pro (5):** Rutin feladatok
- **Gemini Flash (5):** Mechanikus feladatok

**Stratégia:** Drága modellek csak kritikus feladatokra, rutin feladatok Gemini-re

---

## ✅ Ellenőrzési Checklist

### Model Allokáció:
- [x] Opus: 7 mód (kritikus döntések)
- [x] Sonnet: 6 mód (koordináció, dokumentáció)
- [x] DeepSeek: 2 mód (kód írás)
- [x] Gemini Pro: 5 mód (rutin feladatok)
- [x] Gemini Flash: 5 mód (mechanikus feladatok)

### Reasoning Beállítások:
- [x] xhigh: 7 mód (Opus)
- [x] high: 13 mód (Sonnet, DeepSeek, Gemini Pro)
- [x] disabled: 5 mód (Gemini Flash)

### Temperature Beállítások:
- [x] 0.1-0.2: 5 mód (mechanikus, bugfix)
- [x] 0.3: 12 mód (kód írás, tesztek)
- [x] 0.4-0.5: 4 mód (koordináció, review)
- [x] 0.6-0.7: 4 mód (tervezés, dokumentáció)

### Agentic Suffix:
- [x] Planner: agentic (multi-step reasoning)
- [x] Orchestrator: agentic (koordináció)
- [x] Code-New: sima (egyszerű implementáció)
- [x] Code-Feature: sima (egyszerű implementáció)

---

## 🚀 Következő Lépések

1. **Script Futtatása:**
   ```bash
   python update_roo_models.py
   ```
   - Automatikusan frissíti a model ID-kat
   - Automatikusan frissíti az API key-t: `Narzie2012rohaN`
   - Automatikusan frissíti a reasoning beállításokat

2. **Roo Code UI Ellenőrzés:**
   - Nyisd meg a Roo Code UI-t
   - Ellenőrizd a frissített beállításokat

3. **Tesztelés:**
   - Minden mód kipróbálása egyszerű feladatokkal
   - Reasoning és temperature ellenőrzése

4. **Monitoring:**
   - Kvóta használat figyelése
   - Model teljesítmény értékelése

---

## 📝 Megjegyzések

- **Egységes API Key:** `Narzie2012rohaN` (minden mód ugyanazt használja)
- **DeepSeek Specifikációk:** Context 200k, Max Tokens 8000 (ellenőrizve)
- **Gemini Model Név:** `gemini-3-pro-high` (a "high" a reasoning effort level része)
- **Kiro API:** `http://127.0.0.1:8310/v1` (minden model)
- **Reasoning vs Temperature:** Független paraméterek (reasoning = mélység, temperature = kreativitás)

---

**Státusz:** ✅ VÉGLEGES | **Ellenőrizve:** 2026-02-12 | **Verzió:** 5.0 FINAL
