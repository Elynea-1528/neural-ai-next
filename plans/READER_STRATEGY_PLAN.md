# 🎯 HIBRID READER STRATÉGIA - KOMPREHENZÍV TERV

**Verzió:** 1.0 | **Státusz:** ✅ IMPLEMENTÁLVA | **Dátum:** 2026-02-04

---

## 📋 ÁTTEKINTÉS

A **Hibrid Reader Stratégia** célja:
1. ✅ **Drága modellek védelme** (Architect, Code, Debug) - nem olvasnak nagy fájlokat
2. ✅ **Olcsó Reader proxy** - beolvassa az EGÉSZ fájlt (Flash modell)
3. ✅ **Intelligens szűrés** - snippet vagy teljes fájl (attól függően, hogy szükséges-e)
4. ✅ **Automatikus módváltás** - minden drága agent → Reader mód
5. ✅ **90%+ token megtakarítás** - nagy fájloknál

---

## 🏛️ 8 AGENT MÓD - FÁJL OLVASÁSI PROTOKOLL

### **1️⃣ ARCHITECT MÓD** 
**Szerepe:** Tervez, elemez, TASK_TREE-t vezet

#### Fájl Olvasási Szabályok:
```markdown
## 📖 Fájl Olvasás Protokoll (KÖTELEZŐ)

**TILOS:** `read_file` közvetlen használata!

**KÖTELEZŐ:** Reader módba váltás MINDEN fájl olvasáshoz:

### Kis Fájlok (≤150 sor):
- Általános információ kell (struktúra, API, lista)
- Üzenet: "Reader! Nézd meg a `file.py`-t. Mi a struktúrája? Milyen osztályok/függvények vannak?"
- Reader válasz: Teljes fájl (de formázva: osztályok listája)

### Nagy Fájlok (>150 sor):
- Specifikus információ kell (metódus, osztály)
- Üzenet: "Reader! Add meg a `ClassName.method_name()` metódus implementációját a `file.py`-ból."
- Reader válasz: 30-100 soros snippet

### Hiba Diagnosztika:
- Üzenet: "Reader! Nézd meg a `file.py:42` sort. Mi lehet az `AttributeError` oka?"
- Reader válasz: ±20 soros snippet a hiba körül

### Dokumentáció Olvasás:
- Üzenet: "Reader! Nézd meg a `docs/development/architecture_standards.md` fájlt. Mi az 5-rétegű DDD modell?"
- Reader válasz: Releváns szekció (szűrt)

**Előny:** Architect kontextusa tiszta marad, csak a szükséges információ érkezik.
```

---

### **2️⃣ ORCHESTRATOR MÓD**
**Szerepe:** Delegál, lebontja a feladatokat

#### Fájl Olvasási Szabályok:
```markdown
## 📖 Fájl Olvasás Protokoll (KÖTELEZŐ)

**TILOS:** `read_file` közvetlen használata!

**KÖTELEZŐ:** Reader módba váltás információgyűjtéshez:

### Projekt Struktúra Megértés:
- Üzenet: "Reader! Nézd meg a `neural_ai/processors/` mappát. Milyen modulok vannak? Mi a felelősségük?"
- Reader válasz: Mappastruktúra + rövid leírás

### Modul API Megismerés:
- Üzenet: "Reader! Nézd meg a `neural_ai/data/storage/__init__.py` fájlt. Mi a publikus API?"
- Reader válasz: Exportált osztályok/függvények listája

### Delegálási Specifikáció Előkészítés:
- Üzenet: "Reader! Nézd meg a `neural_ai/core/config/interfaces/types.py` fájlt. Milyen Pydantic modellek vannak?"
- Reader válasz: Modellek listája + mezők

**Előny:** Orchestrator csak a szükséges információt kapja, nem beszennyeződik a kontextusa.
```

---

### **3️⃣ CODE MÓD**
**Szerepe:** Implementál, kódot ír

#### Fájl Olvasási Szabályok:
```markdown
## 📖 Fájl Olvasás Protokoll (KÖTELEZŐ)

**TILOS:** `read_file` közvetlen használata!

**KÖTELEZŐ:** Reader módba váltás MINDEN fájl olvasáshoz:

### Módosítás Előtti Context:
- Üzenet: "Reader! Add meg a `ClassName.method_name()` metódus snippetjét a `file.py`-ból. Kontextus: ±5 sor."
- Reader válasz: 30-50 soros snippet
- Használat: `apply_diff` SEARCH blokkjában

### Új Fájl Írás (Referencia):
- Üzenet: "Reader! Nézd meg a `neural_ai/processors/dimensions/d01_price/processor.py` fájlt. Mi a struktúrája? Hogyan néz ki egy Dimension Processor?"
- Reader válasz: Teljes fájl (template-ként)
- Használat: Új fájl írásához referencia

### Hiba Javítás:
- Üzenet: "Reader! Nézd meg a `file.py:42` sort. Mi lehet az `TypeError` oka? Kontextus: ±10 sor."
- Reader válasz: 20-30 soros snippet
- Használat: `apply_diff` SEARCH blokkjában

### Import Ellenőrzés:
- Üzenet: "Reader! Nézd meg a `neural_ai/core/config/__init__.py` fájlt. Mi a publikus API? Mit exportálnak?"
- Reader válasz: Exportált elemek listája

**Előny:** Code Agent kontextusa tiszta, csak a szükséges kódrészlet érkezik. 90% token megtakarítás!
```

---

### **4️⃣ DEBUG MÓD**
**Szerepe:** Javít, hibákat diagnosztizál

#### Fájl Olvasási Szabályok:
```markdown
## 📖 Fájl Olvasás Protokoll (KÖTELEZŐ)

**TILOS:** `read_file` közvetlen használata!

**KÖTELEZŐ:** Reader módba váltás MINDEN fájl olvasáshoz:

### Hiba Diagnosztika:
- Üzenet: "Reader! Nézd meg a `file.py:42` sort. Traceback: `AttributeError: 'NoneType' object has no attribute 'get'`. Mi lehet az oka? Kontextus: ±15 sor."
- Reader válasz: 30-40 soros snippet a hiba körül
- Használat: Hiba azonosítás

### Típus Hiba Kontextus:
- Üzenet: "Reader! Nézd meg a `file.py:78` sort. Pylance hiba: `Expected 'str', got 'Any'`. Mi a típus probléma? Kontextus: ±10 sor."
- Reader válasz: 20-30 soros snippet
- Használat: Típus hiba javítás

### Linter Hiba Kontextus:
- Üzenet: "Reader! Nézd meg a `file.py:55` sort. Ruff hiba: `F841 local variable assigned but never used`. Mi a probléma? Kontextus: ±5 sor."
- Reader válasz: 10-20 soros snippet
- Használat: Linter hiba javítás

### Referencia Implementáció:
- Üzenet: "Reader! Nézd meg a `neural_ai/processors/dimensions/d01_price/processor.py` fájlt. Hogyan implementálják a `process()` metódust? Add meg a teljes implementációt."
- Reader válasz: Teljes metódus (template-ként)
- Használat: Referencia a javításhoz

**Előny:** Debug Agent csak a szükséges kontextust kapja, gyorsabb diagnosztika.
```

---

### **5️⃣ QA MÓD**
**Szerepe:** Linting, típusellenőrzés

#### Fájl Olvasási Szabályok:
```markdown
## 📖 Fájl Olvasás Protokoll (KÖTELEZŐ)

**TILOS:** `read_file` közvetlen használata!

**KÖTELEZŐ:** Reader módba váltás CSAK ha szükséges:

### Linter Hiba Kontextus:
- Üzenet: "Reader! Nézd meg a `file.py:42` sort. Ruff hiba: `E501 line too long`. Mi a sor? Kontextus: ±2 sor."
- Reader válasz: 5-10 soros snippet
- Használat: Hiba megértés

### Típus Hiba Kontextus:
- Üzenet: "Reader! Nézd meg a `file.py:78` sort. Pylance hiba: `Expected 'str', got 'Any'`. Mi a típus? Kontextus: ±5 sor."
- Reader válasz: 10-15 soros snippet
- Használat: Típus hiba megértés

**Megjegyzés:** QA mód általában NEM olvas fájlokat (csak parancssor kimenetből dolgozik).
```

---

### **6️⃣ TEST MÓD**
**Szerepe:** Tesztek futtatása, hibajavítás

#### Fájl Olvasási Szabályok:
```markdown
## 📖 Fájl Olvasás Protokoll (KÖTELEZŐ)

**TILOS:** `read_file` közvetlen használata!

**KÖTELEZŐ:** Reader módba váltás CSAK ha szükséges:

### Teszt Hiba Kontextus:
- Üzenet: "Reader! Nézz meg a `tests/processors/test_pipeline.py:42` sort. Teszt hiba: `AssertionError: expected 100, got 99`. Mi a teszt? Kontextus: ±10 sor."
- Reader válasz: 20-30 soros snippet (teszt függvény)
- Használat: Teszt hiba megértés

### Forráskód Hiba Kontextus:
- Üzenet: "Reader! Nézz meg a `neural_ai/processors/pipeline.py:145` sort. Teszt bukik erre a sorra. Mi lehet az oka? Kontextus: ±10 sor."
- Reader válasz: 20-30 soros snippet
- Használat: Hiba diagnosztika

**Megjegyzés:** Test mód általában NEM olvas fájlokat (csak pytest kimenetből dolgozik).
```

---

### **7️⃣ COMMIT MÓD**
**Szerepe:** Atomikus commitok, release management

#### Fájl Olvasási Szabályok:
```markdown
## 📖 Fájl Olvasás Protokoll (KÖTELEZŐ)

**TILOS:** `read_file` közvetlen használata!

**KÖTELEZŐ:** Reader módba váltás CSAK ha szükséges:

### Commit Üzenet Kontextus:
- Üzenet: "Reader! Nézz meg a `git diff --cached` kimenetét. Mi a módosítás? Rövid összefoglalás."
- Reader válasz: Módosított fájlok listája + rövid leírás
- Használat: Commit üzenet írás

**Megjegyzés:** Commit mód általában NEM olvas fájlokat (csak `git diff` kimenetből dolgozik).
```

---

### **8️⃣ READER MÓD**
**Szerepe:** Proxy, fájl olvasás, szűrés

#### Fájl Olvasási Szabályok:
```markdown
## 📖 Fájl Olvasás Protokoll (KÖTELEZŐ)

**KÖTELEZŐ:** MINDIG beolvasod az EGÉSZ fájlt!

### Szűrési Logika:

#### 1. SPECIFIKUS KÉRÉS (Metódus/Osztály neve):
```
Kérés: "Add meg a `execute_pipeline()` metódust a `pipeline.py`-ból."

Végrehajtás:
1. Beolvasod az EGÉSZ fájlt (500 sor)
2. Keresed a `def execute_pipeline` sort
3. Vágod ki a metódust (±5 sor kontextus)
4. Visszaküldsz: 30-100 soros snippet

Válasz formátum:
# Fájl: neural_ai/processors/pipeline.py (sor 145-178)
def execute_pipeline(self, data: pl.DataFrame) -> pl.DataFrame:
    """Pipeline végrehajtása."""
    # ... metódus törzs ...
    return result
```

#### 2. ÁLTALÁNOS KÉRÉS (Struktúra, API, lista):
```
Kérés: "Mi a fájl struktúrája? Milyen osztályok/függvények vannak?"

Végrehajtás:
1. Beolvasod az EGÉSZ fájlt (500 sor)
2. Azonosítod az összes osztályt/függvényt
3. Visszaküldsz: Teljes fájl (de formázva: osztályok listája)

Válasz formátum:
# Fájl: neural_ai/processors/pipeline.py

## Osztályok:
- PipelineOrchestrator (sor 15-250)
  - __init__(self, ...) (sor 15-25)
  - execute_pipeline(self, ...) (sor 145-178)
  - _validate_input(self, ...) (sor 220-250)

## Függvények:
- create_pipeline(...) (sor 260-280)
```

#### 3. HIBA KONTEXTUS (Sor szám + hiba):
```
Kérés: "Nézd meg a `file.py:42` sort. Mi lehet az `AttributeError` oka? Kontextus: ±20 sor."

Végrehajtás:
1. Beolvasod az EGÉSZ fájlt (500 sor)
2. Keresed a 42. sort
3. Vágod ki: 22-62 sorok (42 ± 20)
4. Visszaküldsz: 40 soros snippet

Válasz formátum:
# Fájl: neural_ai/processors/pipeline.py (sor 22-62)
# HIBA KÖRNYÉKE: AttributeError a 42. sorban

def execute_pipeline(self, data: pl.DataFrame) -> pl.DataFrame:
    # ... sorok 22-41 ...
    result = self.config.get('key')  # ← 42. sor (HIBA ITT)
    # ... sorok 43-62 ...
```

#### 4. DOKUMENTÁCIÓ SZEKCIÓ (Fájl + szekció):
```
Kérés: "Nézd meg a `docs/development/architecture_standards.md` fájlt. Mi az 5-rétegű DDD modell?"

Végrehajtás:
1. Beolvasod az EGÉSZ fájlt (2000 sor)
2. Keresed a "5-rétegű" vagy "DDD" szekciót
3. Vágod ki a releváns szekciót (±5 sor kontextus)
4. Visszaküldsz: 50-100 soros snippet

Válasz formátum:
# Fájl: docs/development/architecture_standards.md (sor 45-120)

## 1. RENDSZERARCHITEKTÚRA ÉS HIERARCHIA (GLOBAL MAP)

A rendszer **Domain-Driven Design (DDD)** elveket követ, négy fő rétegre osztva...
```

### Szűrési Döntési Fa:

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

**Token Megtakarítás:**
- Reader (Flash): 500 sor = ~15,000 token (olcsó)
- Drága modell (Sonnet): 50 sor = ~1,500 token (helyett 15,000)
- **Megtakarítás: 90%** ✅
```

---

## 📊 MÓDVÁLTÁSI MÁTRIX

| Mód | Fájl Olvasás | Reader Delegálás | Szűrés | Kontextus Méret |
|:---|:---:|:---:|:---:|:---:|
| **Architect** | ❌ | ✅ KÖTELEZŐ | ✅ Igen | Snippet |
| **Orchestrator** | ❌ | ✅ KÖTELEZŐ | ✅ Igen | Snippet |
| **Code** | ❌ | ✅ KÖTELEZŐ | ✅ Igen | Snippet |
| **Debug** | ❌ | ✅ KÖTELEZŐ | ✅ Igen | Snippet |
| **QA** | ❌ | ⚠️ Ritkán | ✅ Igen | Snippet |
| **Test** | ❌ | ⚠️ Ritkán | ✅ Igen | Snippet |
| **Commit** | ❌ | ⚠️ Ritkán | ✅ Igen | Snippet |
| **Reader** | ✅ KÖTELEZŐ | N/A | ✅ Intelligens | Teljes/Snippet |

---

## 🔄 MUNKAFOLYAMAT DIAGRAM

```
Architect Mód
  │
  ├─ "Nézd meg a pipeline.py-t"
  │   │
  │   └─ switch_mode → reader
  │       │
  │       └─ Reader: Beolvassa az EGÉSZ fájlt (500 sor)
  │           │
  │           ├─ Specifikus kérés? → Snippet (50 sor)
  │           └─ Általános kérés? → Teljes fájl (formázva)
  │               │
  │               └─ switch_mode → architect
  │                   │
  │                   └─ Architect: Feldolgozza a snippet-et
  │                       (Kontextusa tiszta, csak 50 sor)
```

---

## 📝 IMPLEMENTÁCIÓS LÉPÉSEK

### 1. AGENTS.md Frissítés
- [x] Token Economy szekció: Hibrid Reader stratégia
- [x] Küszöbértékek: 150 sor
- [x] Módváltási szabályok

### 2. .roo/rules-architect/AGENTS.md Frissítés
- [x] Fájl Olvasás Protokoll hozzáadása
- [x] Reader delegálási sablonok
- [x] Konkrét példák

### 3. .roo/rules-orchestrator/AGENTS.md Frissítés
- [x] Fájl Olvasás Protokoll hozzáadása
- [x] Reader delegálási sablonok
- [x] Konkrét példák

### 4. .roo/rules-code/AGENTS.md Frissítés
- [x] Fájl Olvasás Protokoll hozzáadása
- [x] Reader delegálási sablonok
- [x] Konkrét példák

### 5. .roo/rules-debug/AGENTS.md Frissítés
- [x] Fájl Olvasás Protokoll hozzáadása
- [x] Reader delegálási sablonok
- [x] Konkrét példák

### 6. .roo/rules-qa/AGENTS.md Frissítés
- [x] Fájl Olvasás Protokoll hozzáadása
- [x] Reader delegálási sablonok (ritkán)

### 7. .roo/rules-test/AGENTS.md Frissítés
- [x] Fájl Olvasás Protokoll hozzáadása
- [x] Reader delegálási sablonok (ritkán)

### 8. .roo/rules-commit/AGENTS.md Frissítés
- [x] Fájl Olvasás Protokoll hozzáadása
- [x] Reader delegálási sablonok (ritkán)

### 9. .roo/rules-reader/AGENTS.md Frissítés
- [x] Szűrési logika részletezése
- [x] Szűrési döntési fa
- [x] Válasz formátumok
- [x] Token megtakarítás mérőszámok

### 10. hierarchical_agent_system.md Frissítés
- [x] Felelősségi mátrix: Kód Olvasás oszlop
- [x] Reader delegálási lánc diagram
- [x] Token Economy szekció

---

## 💡 ELŐNYÖK

✅ **Drága modellek védelme:** Architect, Code, Debug soha nem olvasnak nagy fájlokat
✅ **Olcsó Reader proxy:** Flash modell beolvassa az EGÉSZET
✅ **Intelligens szűrés:** Snippet vagy teljes fájl (attól függően, hogy szükséges-e)
✅ **90%+ token megtakarítás:** Nagy fájloknál
✅ **Automatikus módváltás:** Minden drága agent → Reader mód
✅ **Egyszerű szabály:** "Drága agent = Reader mód"
✅ **Roo Code adoption:** Könnyű implementálható

---

## ⚠️ KOCKÁZATOK & MEGOLDÁSOK

| Kockázat | Megoldás |
|:---|:---|
| Roo Code nem vált át Reader módba | Explicit utasítás minden agent szabályban |
| Reader túl sok szűrési logikát igényel | Szűrési döntési fa + konkrét példák |
| Drága modell mégis nagy kontextust kap | Strict szabály: "TILOS read_file" |
| Snippet nem elég a módosításhoz | Reader ±5 sor kontextus + teljes metódus |

---

## 📊 TOKEN MEGTAKARÍTÁS KALKULÁCIÓ

### Forgatókönyv: Code Agent módosít egy 500 soros fájlt

**Régi módszer (közvetlen olvasás):**
- Code Agent: `read_file` → 500 sor = ~15,000 token
- Drága modell kontextusa: 15,000 token
- **Teljes: 15,000 token**

**Új módszer (Reader proxy):**
- Code Agent: `switch_mode → reader`
- Reader: Beolvassa az EGÉSZET (500 sor) = ~15,000 token (olcsó)
- Reader: Szűr → 50 soros snippet = ~1,500 token
- Code Agent: `switch_mode → code`
- Code Agent: Feldolgozza a 50 soros snippet-et = ~1,500 token (drága)
- **Teljes: ~17,000 token (de csak 1,500 a drágán!)**

**Megtakarítás: 90% a drága modell kontextusában** ✅

---

## 🎬 KÖVETKEZŐ LÉPÉSEK

1. ✅ Terv jóváhagyása
2. ✅ AGENTS.md frissítés
3. ✅ Összes .roo/rules-*/AGENTS.md frissítés
4. ✅ hierarchical_agent_system.md frissítés
5. ⏳ **Tesztelés: Roo Code módváltások**
   - Architect mód: Próbálj fájlt olvasni → Ellenőrizd, hogy Reader módba vált-e
   - Code mód: Próbálj módosítani egy nagy fájlt → Ellenőrizd a Reader delegálást
   - Debug mód: Próbálj hibát javítani → Ellenőrizd a snippet kérést
6. ⏳ **Monitoring: Token megtakarítás mérése**
   - Naplózd a Reader delegálások számát
   - Mérd a snippet méreteket vs teljes fájl méreteket
   - Számold ki a tényleges token megtakarítást
7. ⏳ **Finomhangolás:**
   - Ha a snippet-ek túl kicsik → Növeld a kontextust (±5 → ±10 sor)
   - Ha a snippet-ek túl nagyok → Csökkentsd a kontextust
   - Ha a Reader túl gyakran ad vissza teljes fájlt → Pontosítsd a kéréseket

---

## 📊 IMPLEMENTÁCIÓ STÁTUSZ

| Komponens | Státusz | Megjegyzés |
|:---|:---:|:---|
| AGENTS.md | ✅ | Hibrid Reader stratégia hozzáadva |
| .roo/rules-architect/AGENTS.md | ✅ | Fájl Olvasás Protokoll + példák |
| .roo/rules-orchestrator/AGENTS.md | ✅ | Fájl Olvasás Protokoll + példák |
| .roo/rules-code/AGENTS.md | ✅ | Fájl Olvasás Protokoll + példák |
| .roo/rules-debug/AGENTS.md | ✅ | Fájl Olvasás Protokoll + példák |
| .roo/rules-qa/AGENTS.md | ✅ | Fájl Olvasás Protokoll (ritkán) |
| .roo/rules-test/AGENTS.md | ✅ | Fájl Olvasás Protokoll (ritkán) |
| .roo/rules-commit/AGENTS.md | ✅ | Fájl Olvasás Protokoll (ritkán) |
| .roo/rules-reader/AGENTS.md | ✅ | Teljes újraírás: szűrési logika + döntési fa |
| hierarchical_agent_system.md | ✅ | Felelősségi mátrix + Token Economy szekció |

---

**Az implementáció sikeres! A Hibrid Reader Stratégia élesben van. Következő lépés: tesztelés és monitoring.** 🚀
