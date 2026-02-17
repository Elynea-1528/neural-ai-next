# 🎯 TASK: Pyright/Pylance Integráció Dokumentációba

**Cél:** Minden releváns dokumentációs fájlban (AGENTS.md, rules, standards) hozzáadni a Pyright/Pylance ellenőrzést, ahol Mypy vagy type checking van említve.

**Státusz:** 🔄 IN PROGRESS

## 📋 Fájlok Listája

### 1. Fő AGENTS.md fájlok
- [x] `./AGENTS.md` (fő projekt szabályok) ✅ KÉSZ
  - Quality Gate: Mypy + Pylance/Pyright hozzáadva
  - Build parancsok: mypy és pyright parancsok hozzáadva
  - Környezeti követelmények: mypy és pyright útvonalak hozzáadva
- [ ] `./.clinerules/cline-rules.md`

### 2. Roo Rules (.roo mappa)
- [ ] `./.roo/rules-architect/AGENTS.md`
- [ ] `./.roo/rules-code-feature/AGENTS.md`
- [ ] `./.roo/rules-code-fix/AGENTS.md`
- [ ] `./.roo/rules-code-new/AGENTS.md`
- [ ] `./.roo/rules-code-optimize/AGENTS.md`
- [ ] `./.roo/rules-code-refactor/AGENTS.md`
- [ ] `./.roo/rules-code-style/AGENTS.md`
- [ ] `./.roo/rules-commit/AGENTS.md`
- [ ] `./.roo/rules-debug-complex/AGENTS.md`
- [ ] `./.roo/rules-debug-performance/AGENTS.md`
- [ ] `./.roo/rules-debug-simple/AGENTS.md`
- [ ] `./.roo/rules-docs-api/AGENTS.md`
- [ ] `./.roo/rules-docs-arch/AGENTS.md`
- [ ] `./.roo/rules-docs-comment/AGENTS.md`
- [ ] `./.roo/rules-docs-guide/AGENTS.md`
- [ ] `./.roo/rules-orchestrator/AGENTS.md`
- [ ] `./.roo/rules-planner/AGENTS.md`
- [ ] `./.roo/rules-qa/AGENTS.md`
- [ ] `./.roo/rules-reader/AGENTS.md`
- [ ] `./.roo/rules-review/AGENTS.md`
- [ ] `./.roo/rules-search/AGENTS.md`
- [ ] `./.roo/rules-test-e2e/AGENTS.md`
- [ ] `./.roo/rules-test-integration/AGENTS.md`
- [ ] `./.roo/rules-test-property/AGENTS.md`
- [ ] `./.roo/rules-test-unit/AGENTS.md`

### 3. Docs Development
- [ ] `docs/development/architecture_standards.md`
- [ ] `docs/development/coding_standards.md`
- [ ] `docs/development/custom-instructions.md`

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

Folyamatban...
