# 🧠 NEURAL AI NEXT | SYSTEM TELEMETRY & STATUS TEMPLATE

**Last Sync:** `[ISO 8601 DÁTUM]` | **System Health:** `[🟢 STABLE / 🟡 WARNING / 🔴 CRITICAL]` | **Active Agent:** `[Architect/Code/Debug/Orchestrator/Ask]`

---

## 📊 GLOBAL PROGRESS

**Overall Completion:** `[XX%]` `[████████████░░░░░░░░]`
**Token Usage (Session):** `[~XXXX tokens (Becsült)]`
**Test Coverage (Avg):** `[Stmt: XX% | Brch: XX%]`

---

## 🗂️ DEVELOPMENT PHASES

### `[🟢/🟡/🔴]` PHASE `[X]`: `[PHASE NAME]`

**Description:** `[Rövid leírás a fázis céljáról és scope-járól]`
**Progress:** `[XX%]` `[████████████░░░░░░░░]` | **Priority:** `[CRITICAL/HIGH/MEDIUM/LOW]`
**Complexity:** `[⭐-⭐⭐⭐⭐⭐]` | **Token Budget:** `[~XXXX tokens]`

#### Granular Matrix

| File Path | Matrix `[S|T|D]` | Stmt% | Brch% | Complexity | Token Est. | Dependencies | Status |
|-----------|:----------------:|:-----:|:-----:|:----------:|:----------:|:-------------|:------:|
| `[relatív/útvonal.py]` | `[✅/❌\|✅/❌\|✅/❌]` | `[XX%]` | `[XX%]` | `[⭐-⭐⭐⭐⭐⭐]` | `[XXXX]` | `[dep1, dep2]` | `[✅/🟢/🟡/🔴]` |
| `[relatív/útvonal.py]` | `[✅/❌\|✅/❌\|✅/❌]` | `[XX%]` | `[XX%]` | `[⭐-⭐⭐⭐⭐⭐]` | `[XXXX]` | `[dep1, dep2]` | `[✅/🟢/🟡/🔴]` |

**Matrix Jelmagyarázat:**
- **S** = Source Code (Forrás kód elkészült)
- **T** = Test Coverage (Tesztek elkészültek és átmennek)
- **D** = Documentation (Dokumentáció elkészült)

**Statusz Jelmagyarázat:**
- **✅ PERFECT** = 100% Stmt / 100% Brch Coverage + Type Checked + Dokumentálva
- **🟢 DONE** = Implementálva, de Coverage < 100% vagy hiányos dokumentáció
- **🟡 WIP** = Fejlesztés alatt, tesztek részben jók vagy hiányosak
- **🔴 PENDING** = Nincs kész, vagy a tesztek buknak

---

### `[🟢/🟡/🔴]` PHASE `[X+1]`: `[PHASE NAME]`

**Description:** `[Rövid leírás a fázis céljáról és scope-járól]`
**Progress:** `[XX%]` `[████████████░░░░░░░░]` | **Priority:** `[CRITICAL/HIGH/MEDIUM/LOW]`
**Complexity:** `[⭐-⭐⭐⭐⭐⭐]` | **Token Budget:** `[~XXXX tokens]`

#### Granular Matrix

| File Path | Matrix `[S|T|D]` | Stmt% | Brch% | Complexity | Token Est. | Dependencies | Status |
|-----------|:----------------:|:-----:|:-----:|:----------:|:----------:|:-------------|:------:|
| `[relatív/útvonal.py]` | `[✅/❌\|✅/❌\|✅/❌]` | `[XX%]` | `[XX%]` | `[⭐-⭐⭐⭐⭐⭐]` | `[XXXX]` | `[dep1, dep2]` | `[✅/🟢/🟡/🔴]` |

---

## ⚡ ACTIVE CONTEXT

- 🎯 **Current Focus:** `[aktuális fájl/komponens]`
- 🛑 **Blocker:** `[Akadály vagy függőség]`
- 📈 **Next Steps:** `[Következő lépések rövid leírása]`

---

## 📝 NOTES & BLOCKERS

### Blokkolók
1. `[Blokkoló probléma leírása és hatása]`
2. `[Másik blokkoló]`

### Függőségek
- `[Fázis/Modul]` vár `[Másik Fázis/Modul]`-ra

### Döntések
- `[Dátum]`: `[Fontos döntés vagy változtatás leírása]`

---

## 🔧 TECHNICAL DEBT

| Issue | Severity | Affected Files | Notes |
|-------|:--------:|:---------------|:------|
| `[Issue leírás]` | `[🔴/🟡/🟢]` | `[fájlok]` | `[Megjegyzés]` |

---

## 📊 QUALITY METRICS

| Metric | Target | Current | Status |
|--------|:------:|:-------:|:------:|
| Code Coverage (Stmt) | 100% | `[XX%]` | `[✅/🟡/🔴]` |
| Code Coverage (Branch) | 100% | `[XX%]` | `[✅/🟡/🔴]` |
| Type Safety | Strict | `[Strict/Partial]` | `[✅/🟡/🔴]` |
| Linter Errors | 0 | `[X]` | `[✅/🟡/🔴]` |
| Documentation | 100% | `[XX%]` | `[✅/🟡/🔴]` |

---

## 🚀 RECENT COMMITS

```
[Commit hash] - feat(scope): [commit message]
[Commit hash] - fix(scope): [commit message]
[Commit hash] - docs(scope): [commit message]
```

---

**Template Version:** 1.0
**Last Updated:** `[ISO 8601 DÁTUM]`