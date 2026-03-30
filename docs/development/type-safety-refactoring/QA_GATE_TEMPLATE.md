# QA GATE SABLON

**MINDEN FÁJLNÁL KÖTELEZŐ FUTTATNI!**

---

## 📋 PARANCSOK

```bash
# 1. Linting (Ruff)
/home/elynea/miniconda3/envs/neural-ai-next/bin/ruff check neural_ai/path/to/file.py

# 2. Type Check (Mypy)
/home/elynea/miniconda3/envs/neural-ai-next/bin/mypy neural_ai/path/to/file.py

# 3. Type Check (Pyright)
/home/elynea/miniconda3/envs/neural-ai-next/bin/pyright neural_ai/path/to/file.py

# 4. Tests
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/path/to/test_file.py -vv

# 5. Coverage (CÉL: 100% Stmt / 100% Brch)
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest \
  --cov=neural_ai/path/to/file \
  --cov-report=term-missing \
  --cov-branch
```

---

## ✅ ELVÁRT EREDMÉNYEK

- ✅ **Ruff**: 0 hiba
- ✅ **Mypy**: 0 hiba  
- ✅ **Pyright**: 0 hiba (strict mode)
- ✅ **Pytest**: X/X passed (0 failed)
- ✅ **Coverage**: **100% Stmt / 100% Brch** (KÖTELEZŐ!)

---

## 🔄 COMMIT WORKFLOW

```bash
# HA MINDEN PASS (0 hiba, 100%/100% coverage) → Commit
git add neural_ai/path/to/file.py tests/path/to/test_file.py
git commit -m "refactor(type-safety): [fájlnév] type ignore javítás - [leírás]"

# TASK_TREE frissítés
python scripts/generate.py
git add docs/development/TASK_TREE.md docs/development/TASK_TREE.html
git commit -m "docs(task-tree): [fájlnév] státusz frissítés"
```

---

## 🚨 HA VALAMELYIK BUKIK

| Hiba típus | Delegálás |
|:-----------|:----------|
| **Ruff hiba** | Code-Style módba |
| **Mypy/Pyright hiba** | Type ignore javítás folytatása |
| **Teszt fail** | Debug-Simple vagy Debug-Complex módba |
| **Coverage <100%** | Test-Unit módba (új tesztek írása) |

---

## 📊 COVERAGE KÖVETELMÉNYEK

**Kritikus modulok** (core, data, processors):
- **Statement Coverage**: 100% (minden sor lefedve)
- **Branch Coverage**: 100% (minden if/else ág lefedve)

**Nem kritikus modulok** (ui, collectors, scripts):
- **Statement Coverage**: minimum 80%
- **Branch Coverage**: minimum 70%

**FIGYELEM**: A TASK_TREE csak akkor frissül 🔴→✅-re, ha 100%/100% coverage!

---

**Verzió**: 1.0
**Utolsó frissítés**: 2026-03-30
