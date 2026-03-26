# 🔄 Cline (Lead Developer) → Roo Code (Execution Team) Workflow

**Verzió:** 1.0 | **Dátum:** 2026-02-05

---

## 🎯 Szerepkörök

| Szereplő | Szerepkör | Felelősség |
|:---------|:----------|:-----------|
| **Ember (Te)** | Projekt Tulajdonos | Döntéshozás, irányítás, jóváhagyás |
| **Cline** | Lead Developer | Elemzés, tervezés, parancs generálás, ellenőrzés |
| **Roo Code** | Execution Team | Végrehajtás, implementáció, tesztelés |

---

## 📋 Munkafolyamat (Lépésről Lépésre)

### 1. Feladat Megadása
```
Te → Cline: "Hozz létre D6 Volatility dimenzió processzort"
```

### 2. Cline Elemzi és Parancsot Generál
```
Cline → Válasz:
"Rendben! Először tervezés kell.

PARANCS ROO CODE-NAK (Architect mód):
Architect! Tervezd meg a D6 Volatility dimenzió processzort.
Követelmények:
- Polars DataFrame
- DDD pattern (Interface → Implementation → Factory)
- Volatility számítás (ATR, Bollinger Bands)
- Magyar docstring
"
```

### 3. Átmásolod a Parancsot Roo Code-ba
```
1. Nyisd meg a Roo Code chat ablakot
2. Válts "Architect" módra (dropdown a tetején)
3. Másold be a parancsot
4. Enter
```

### 4. Roo Code (Architect) Végrehajtja
```
Roo Code (Architect) → Válasz:
"Rendben! D6 Volatility dimenzió processzor terv:

Struktúra:
neural_ai/processors/dimensions/d06_volatility/
├── interfaces/
│   └── volatility_interface.py
├── implementations/
│   └── volatility_processor.py
├── exceptions/
│   └── volatility_error.py
├── factory.py
└── __init__.py

Volatility számítás:
- ATR (Average True Range)
- Bollinger Bands Width
- Standard Deviation

Implementáció részletek:
[...]
"
```

### 5. Átmásolod az Eredményt Cline-nak
```
1. Másold ki a Roo Code válaszát
2. Illeszd be Cline chat ablakába
3. Enter
```

### 6. Cline Ellenőrzi és Következő Lépés
```
Cline → Válasz:
"Kiváló terv! A struktúra megfelelő, a DDD pattern követve van.

Most implementálás következik.

PARANCS ROO CODE-NAK (Orchestrator mód):
Orchestrator! Implementáld az Architect tervét.
Feladatok:
1. Code-New: Hozd létre a fájlokat
2. Test-Unit: Írj unit teszteket
3. QA: Ellenőrizd a kódot
4. Commit: Commitold a változásokat
"
```

### 7. Ismételd a Folyamatot
```
Roo Code (Orchestrator) → Végrehajtás
→ Eredmény visszamásolása Cline-nak
→ Cline ellenőrzi
→ Következő parancs
→ ...
```

---

## 🎯 Parancs → Mód Gyors Referencia

| Cline Parancs Kulcsszó | Roo Code Mód | Mikor Használd |
|:------------------------|:-------------|:---------------|
| **"Tervezd meg..."** | Architect | Új modul/feature tervezés |
| **"Készíts roadmap..."** | Planner | Projekt tervezés, milestone |
| **"Implementáld..."** | Orchestrator | Komplex feladat végrehajtás |
| **"Hozz létre új..."** | Code-New | Új fájl/modul létrehozás |
| **"Refaktoráld..."** | Code-Refactor | Kód átstrukturálás |
| **"Adj hozzá funkciót..."** | Code-Feature | Meglévő modulhoz új funkció |
| **"Javítsd a bugot..."** | Code-Fix | Egyszerű hiba javítás |
| **"Optimalizáld..."** | Code-Optimize | Performance javítás |
| **"Formázd..."** | Code-Style | Kód formázás |
| **"Írj docstring-et..."** | Docs-API | API dokumentáció |
| **"Írj tutorial-t..."** | Docs-Guide | Felhasználói dokumentáció |
| **"Dokumentáld az architektúrát..."** | Docs-Arch | Rendszer dokumentáció |
| **"Írj unit tesztet..."** | Test-Unit | Egyszerű funkció teszt |
| **"Írj integration tesztet..."** | Test-Integration | Modulok közötti teszt |
| **"Írj property tesztet..."** | Test-Property | Invariant tesztelés |
| **"Írj E2E tesztet..."** | Test-E2E | Teljes rendszer teszt |
| **"Debug-old..."** | Debug-Simple | Linter hiba javítás |
| **"Debug-old komplex..."** | Debug-Complex | Logic hiba javítás |
| **"Profilozd..."** | Debug-Performance | Performance debug |
| **"Ellenőrizd..."** | QA | Linter + Type check |
| **"Review-old..."** | Review | Kód review |
| **"Keress..."** | Search | Codebase keresés |
| **"Commitold..."** | Commit | Git commit |

---

## 💡 Tippek

### 1. Cline Mindig Megmondja a Módot
```
PARANCS ROO CODE-NAK (Architect mód):
                      ^^^^^^^^^ Itt van!
```

### 2. Ha Nem Egyértelmű
- Tervezés → **Architect**
- Implementálás → **Orchestrator**
- Egyszerű feladat → **Code-New / Code-Fix**

### 3. Több Lépéses Feladat
```
Cline → "Architect! Tervezd meg..."
→ Roo Code (Architect) → Terv
→ Cline → "Orchestrator! Implementáld..."
→ Roo Code (Orchestrator) → Implementáció
→ Cline → "QA! Ellenőrizd..."
→ Roo Code (QA) → Ellenőrzés
→ Cline → "Commit! Commitold..."
→ Roo Code (Commit) → Commit
```

---

## ✅ Előnyök

1. **Cline (Lead Dev):**
   - Stratégiai döntések
   - Tervezés
   - Ellenőrzés
   - Minőségbiztosítás

2. **Roo Code (Execution):**
   - Végrehajtás
   - Implementáció
   - Tesztelés
   - Dokumentálás

3. **Te (Projekt Tulajdonos):**
   - Döntéshozás
   - Irányítás
   - Jóváhagyás
   - Kontroll

**Eredmény:** Hatékony, ellenőrzött, minőségi fejlesztés! 🚀

---

## 🎯 Példa Session

```
1. Te → Cline: "Hozz létre D6 Volatility processzort"

2. Cline → "PARANCS: Architect! Tervezd meg..."

3. Te → Roo Code (Architect mód): [parancs]

4. Roo Code → [Terv]

5. Te → Cline: [terv]

6. Cline → "Jó! PARANCS: Orchestrator! Implementáld..."

7. Te → Roo Code (Orchestrator mód): [parancs]

8. Roo Code → [Implementáció]

9. Te → Cline: [implementáció]

10. Cline → "Tökéletes! PARANCS: QA! Ellenőrizd..."

11. Te → Roo Code (QA mód): [parancs]

12. Roo Code → [0 hiba, minden zöld]

13. Te → Cline: [eredmény]

14. Cline → "Kiváló! PARANCS: Commit! Commitold..."

15. Te → Roo Code (Commit mód): [parancs]

16. Roo Code → [Commit kész]

17. Te → Cline: [commit]

18. Cline → "D6 Volatility processzor kész! ✅"
```

**Kész!** 🎉

