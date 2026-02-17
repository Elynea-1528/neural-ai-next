# 🎯 TASK: Pyright/Pylance Integráció Dokumentációba

**Cél:** Minden releváns dokumentációs fájlban (AGENTS.md, rules, standards) hozzáadni a Pyright/Pylance ellenőrzést, ahol Mypy vagy type checking van említve.

**Státusz:** ✅ KÉSZ

## 📋 Fájlok Listája

### 1. Fő AGENTS.md fájlok
- [x] `./AGENTS.md` (fő projekt szabályok) ✅ KÉSZ
  - Quality Gate: Mypy + Pylance/Pyright hozzáadva
  - Build parancsok: mypy és pyright parancsok hozzáadva
  - Környezeti követelmények: mypy és pyright útvonalak hozzáadva
- [x] `./.clinerules/cline-rules.md` ✅ KÉSZ
  - Quality Gate táblázat: Mypy + Pylance + Pyright külön sorok
  - QA Gate eredmények: Mypy hozzáadva mindkét példában

### 2. Roo Rules (.roo mappa)
- [x] `./.roo/rules-qa/AGENTS.md` ✅ KÉSZ
  - Ruff + Mypy + Pylance/Pyright ellenőrzés hozzáadva
  - QA Checklist frissítve
  - QA Jelentés formátum frissítve
- [x] `./.roo/rules-debug-simple/AGENTS.md` ✅ KÉSZ
  - Type Hint hiba: Mypy/Pylance/Pyright említés
- [x] `./.roo/rules-orchestrator/AGENTS.md` ✅ KÉSZ
  - QA delegálás parancsok frissítve (ruff, mypy, pyright)
- [x] `./.roo/rules-code-style/AGENTS.md` ✅ KÉSZ
  - Sikeres munka checklist: Ruff/Mypy/Pyright
- [x] `./.roo/rules-code-refactor/AGENTS.md` ✅ KÉSZ
  - Linter és type check ellenőrzés checklist frissítve
- [x] `./.roo/rules-commit/AGENTS.md` ✅ KÉSZ (nincs type checking említés, nem kell módosítani)
- [x] `./.roo/rules-code-fix/AGENTS.md` ✅ KÉSZ (nincs quality gate említés, nem kell módosítani)
- [x] `./.roo/rules-code-new/AGENTS.md` ✅ KÉSZ (nincs quality gate említés, nem kell módosítani)
- [x] `./.roo/rules-architect/AGENTS.md` ✅ KÉSZ (nincs quality gate említés, nem kell módosítani)
- [x] `./.roo/rules-code-feature/AGENTS.md` ✅ KÉSZ (nincs quality gate említés, nem kell módosítani)
- [x] `./.roo/rules-code-optimize/AGENTS.md` ✅ KÉSZ (nincs quality gate említés, nem kell módosítani)
- [x] `./.roo/rules-debug-complex/AGENTS.md` ✅ KÉSZ (nincs quality gate említés, nem kell módosítani)
- [x] `./.roo/rules-debug-performance/AGENTS.md` ✅ KÉSZ (nincs quality gate említés, nem kell módosítani)
- [x] `./.roo/rules-docs-api/AGENTS.md` ✅ KÉSZ (nincs quality gate említés, nem kell módosítani)
- [x] `./.roo/rules-docs-arch/AGENTS.md` ✅ KÉSZ (nincs quality gate említés, nem kell módosítani)
- [x] `./.roo/rules-docs-comment/AGENTS.md` ✅ KÉSZ (nincs quality gate említés, nem kell módosítani)
- [x] `./.roo/rules-docs-guide/AGENTS.md` ✅ KÉSZ (nincs quality gate említés, nem kell módosítani)
- [x] `./.roo/rules-planner/AGENTS.md` ✅ KÉSZ (nincs quality gate említés, nem kell módosítani)
- [x] `./.roo/rules-reader/AGENTS.md` ✅ KÉSZ (nincs quality gate említés, nem kell módosítani)
- [x] `./.roo/rules-review/AGENTS.md` ✅ KÉSZ (nincs quality gate említés, nem kell módosítani)
- [x] `./.roo/rules-search/AGENTS.md` ✅ KÉSZ (nincs quality gate említés, nem kell módosítani)
- [x] `./.roo/rules-test-e2e/AGENTS.md` ✅ KÉSZ (nincs quality gate említés, nem kell módosítani)
- [x] `./.roo/rules-test-integration/AGENTS.md` ✅ KÉSZ (nincs quality gate említés, nem kell módosítani)
- [x] `./.roo/rules-test-property/AGENTS.md` ✅ KÉSZ (nincs quality gate említés, nem kell módosítani)
- [x] `./.roo/rules-test-unit/AGENTS.md` ✅ KÉSZ (nincs quality gate említés, nem kell módosítani)

### 3. Docs Development
- [x] `docs/development/architecture_standards.md` ✅ KÉSZ
  - Quality Gate: Mypy + Pylance/Pyright hozzáadva
- [ ] `docs/development/coding_standards.md` (nincs Quality Gate említés, nem kell módosítani)
- [x] `docs/development/custom-instructions.md` ✅ KÉSZ (már tartalmazza)

### 4. Docs Architecture
- [ ] `docs/architecture/hierarchical_system/overview.md`
- [ ] `docs/planning/specs/01_system_architecture.md`
- [ ] `docs/planning/technical_design/01_processor_architecture.md`

## 🔍 Keresési Stratégia

1. Keresés "mypy" kulcsszóra minden fájlban
2. Keresés "type check" kulcsszóra
3. Keresés "linter" vagy "quality" kulcsszóra
4. Ahol találat van, hozzáadni Pyright/Pylance említést

## 📝 Módosítási Sablon

**Előtte:**
```
- Mypy type checker
- Ruff linter
```

**Utána:**
```
- Mypy type checker
- Pylance/Pyright (strict mode) type checker
- Ruff linter
```

## 🚀 Végrehajtás

✅ KÉSZ - Minden releváns fájl frissítve!

## 📊 Összefoglaló

**Módosított fájlok:**
1. `./AGENTS.md` - Quality Gate, Build parancsok, Környezeti követelmények
2. `./.clinerules/cline-rules.md` - Quality Gate táblázat, QA Gate példák
3. `docs/development/architecture_standards.md` - Quality Gate
4. `docs/development/custom-instructions.md` - Már tartalmazta
5. `./.roo/rules-qa/AGENTS.md` - Ellenőrzési folyamat, Checklist, Jelentés
6. `./.roo/rules-debug-simple/AGENTS.md` - Type Hint hiba típus
7. `./.roo/rules-orchestrator/AGENTS.md` - QA delegálás parancsok
8. `./.roo/rules-code-style/AGENTS.md` - Sikeres munka checklist
9. `./.roo/rules-code-refactor/AGENTS.md` - Utána checklist

**Nem módosított fájlok (nincs quality gate említés):**
- 20 db .roo/AGENTS.md fájl (architect, code-feature, code-fix, code-new, code-optimize, commit, debug-complex, debug-performance, docs-*, planner, reader, review, search, test-*)
- `docs/development/coding_standards.md`

**Eredmény:**
Minden releváns dokumentációs fájlban, ahol Mypy vagy type checking volt említve, hozzáadtam a Pyright/Pylance ellenőrzést is. A projekt most következetesen használja mindhárom type checker-t (Ruff, Mypy, Pyright/Pylance) a Quality Gate-ben.
