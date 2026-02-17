# Mirror Structure Refactor - Specification

**Létrehozva:** 2026-02-17  
**Státusz:** DRAFT  
**Prioritás:** HIGH

## Probléma

A jelenlegi mappaszerkezet NEM követi a Mirror Rule-t következetesen:

### Jelenlegi (HIBÁS):
```
neural_ai/
├── collectors/
├── core/
├── data/
├── processors/
└── ui/

tests/
├── collectors/          ❌ NEM tükör (hiányzik a neural_ai/)
├── core/
├── data/
├── processors/
└── ui/

docs/components/
├── collectors/          ❌ NEM tükör (hiányzik a neural_ai/)
├── core/
├── data/
├── processors/
└── ui/
```

### Cél (HELYES - TELJES TÜKÖR):
```
neural_ai/
├── collectors/
├── core/
├── data/
├── processors/
└── ui/

tests/
└── neural_ai/           ✅ TÜKÖR
    ├── collectors/
    ├── core/
    ├── data/
    ├── processors/
    └── ui/

docs/components/
└── neural_ai/           ✅ TÜKÖR
    ├── collectors/
    ├── core/
    ├── data/
    ├── processors/
    └── ui/
```

## User Stories

### US-1: Tests mappa átnevezése
**Mint** fejlesztő  
**Szeretném**, hogy a `tests/` mappa tükrözze a `neural_ai/` struktúrát  
**Hogy** könnyen megtaláljam a teszteket

**Acceptance Criteria:**
- [ ] `tests/collectors/` → `tests/neural_ai/collectors/`
- [ ] `tests/core/` → `tests/neural_ai/core/`
- [ ] `tests/data/` → `tests/neural_ai/data/`
- [ ] `tests/processors/` → `tests/neural_ai/processors/`
- [ ] `tests/ui/` → `tests/neural_ai/ui/`
- [ ] Minden import frissítve
- [ ] Pytest sikeresen fut

### US-2: Docs mappa átnevezése
**Mint** fejlesztő  
**Szeretném**, hogy a `docs/components/` mappa tükrözze a `neural_ai/` struktúrát  
**Hogy** könnyen megtaláljam a dokumentációt

**Acceptance Criteria:**
- [ ] `docs/components/collectors/` → `docs/components/neural_ai/collectors/`
- [ ] `docs/components/core/` → `docs/components/neural_ai/core/`
- [ ] `docs/components/data/` → `docs/components/neural_ai/data/`
- [ ] `docs/components/processors/` → `docs/components/neural_ai/processors/`
- [ ] `docs/components/ui/` → `docs/components/neural_ai/ui/`
- [ ] Minden link frissítve

### US-3: Mirror Rule frissítése
**Mint** fejlesztő  
**Szeretném**, hogy a Mirror Rule logika helyesen működjön  
**Hogy** a task tree generator helyesen találja meg a teszteket és dokumentációt

**Acceptance Criteria:**
- [ ] `MirrorChecker.get_test_path()` frissítve
- [ ] `MirrorChecker.check_documentation()` frissítve
- [ ] Task tree generator helyesen működik

### US-4: Dokumentáció frissítése
**Mint** fejlesztő  
**Szeretném**, hogy minden dokumentáció tükrözze az új struktúrát  
**Hogy** ne legyen zavaró

**Acceptance Criteria:**
- [ ] `AGENTS.md` frissítve
- [ ] `.clinerules/cline-rules.md` frissítve
- [ ] `docs/development/architecture_standards.md` frissítve
- [ ] Minden `.roo/rules-*/AGENTS.md` frissítve
- [ ] README.md frissítve (ha van benne példa)

## Technikai követelmények

### Fájl átnevezések

#### 1. Tests mappa:
```bash
# Létrehozni
mkdir -p tests/neural_ai

# Átmozgatni (git mv használata a history megőrzéséhez)
git mv tests/collectors tests/neural_ai/collectors
git mv tests/core tests/neural_ai/core
git mv tests/data tests/neural_ai/data
git mv tests/processors tests/neural_ai/processors
git mv tests/ui tests/neural_ai/ui

# Megtartani (nem változik)
# tests/scripts/
# tests/test_*.py (root szintű tesztek)
```

#### 2. Docs mappa:
```bash
# Létrehozni
mkdir -p docs/components/neural_ai

# Átmozgatni (git mv használata a history megőrzéséhez)
git mv docs/components/collectors docs/components/neural_ai/collectors
git mv docs/components/core docs/components/neural_ai/core
git mv docs/components/data docs/components/neural_ai/data
git mv docs/components/processors docs/components/neural_ai/processors
git mv docs/components/ui docs/components/neural_ai/ui
```

### Kód frissítések

#### 1. scripts/generate_task_tree.py:

**MirrorChecker.get_test_path():**
```python
# ELŐTTE:
# neural_ai/collectors/jforex/factory.py → tests/collectors/jforex/test_factory.py

# UTÁNA:
# neural_ai/collectors/jforex/factory.py → tests/neural_ai/collectors/jforex/test_factory.py
```

**MirrorChecker.check_documentation():**
```python
# ELŐTTE:
# neural_ai/collectors/jforex/factory.py → docs/components/collectors/jforex/factory.md

# UTÁNA:
# neural_ai/collectors/jforex/factory.py → docs/components/neural_ai/collectors/jforex/factory.md
```

#### 2. Import frissítések:
- Pytest automatikusan kezeli (ha a `tests/` mappa a PYTHONPATH-ban van)
- Nincs szükség import frissítésre (a tesztek relatív importokat használnak)

### Dokumentáció frissítések

#### 1. AGENTS.md:
- Mirror Rule példák frissítése:
  ```
  # ELŐTTE:
  neural_ai/core/logger/factory.py → tests/core/logger/test_logger_factory.py
  
  # UTÁNA:
  neural_ai/core/logger/factory.py → tests/neural_ai/core/logger/test_logger_factory.py
  ```
- Mappaszerkezet diagram frissítése

#### 2. .clinerules/cline-rules.md:
- Mirror Rule példák frissítése

#### 3. docs/development/architecture_standards.md:
- Mirror Rule példák frissítése

#### 4. .roo/rules-*/AGENTS.md:
- Mirror Rule példák frissítése (ha van)

## Kockázatok és megoldások

| Kockázat | Valószínűség | Hatás | Megoldás |
|:---------|:-------------|:------|:---------|
| Import törések | Alacsony | Magas | Pytest automatikusan kezeli |
| Git history elvesztése | Alacsony | Közepes | `git mv` használata |
| CI/CD törések | Közepes | Magas | Pytest útvonalak frissítése |
| Dokumentáció linkek törése | Magas | Alacsony | Minden link manuális ellenőrzése |

## Végrehajtási sorrend

1. **Tests mappa átnevezése** (US-1)
   - `git mv` parancsok futtatása
   - Pytest futtatása (ellenőrzés)

2. **Docs mappa átnevezése** (US-2)
   - `git mv` parancsok futtatása
   - Linkek ellenőrzése

3. **Mirror Rule frissítése** (US-3)
   - `scripts/generate_task_tree.py` módosítása
   - Task tree generálás (ellenőrzés)

4. **Dokumentáció frissítése** (US-4)
   - AGENTS.md, cline-rules.md, architecture_standards.md
   - .roo/rules-*/AGENTS.md fájlok

5. **Tesztelés**
   - Pytest futtatása: `pytest tests/`
   - Task tree generálás: `python scripts/generate_task_tree.py`
   - Dokumentáció linkek ellenőrzése

## Sikerkritériumok

- [ ] Minden teszt zöld (`pytest tests/`)
- [ ] Task tree generator helyesen működik
- [ ] Dokumentáció konzisztens (nincs törött link)
- [ ] Git history megőrzött (`git log --follow`)
- [ ] Mirror Rule példák helyesek minden dokumentációban

## Rollback terv

Ha bármi elromlik:
```bash
# Git reset az utolsó commit előtti állapotra
git reset --hard HEAD~1

# Vagy ha már push-oltuk
git revert <commit_hash>
```

## Megjegyzések

- Ez egy NAGY refaktor, érdemes külön branch-en dolgozni
- A `git mv` parancs megőrzi a git history-t
- A pytest automatikusan kezeli az új útvonalakat
- A dokumentáció linkeket manuálisan kell ellenőrizni
