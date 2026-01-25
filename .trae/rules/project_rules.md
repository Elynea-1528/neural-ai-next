# 🏛️ NEURAL AI NEXT - PROJECT RULES (CODEX v4.0)

**ENFORCEMENT:** STRICT (Zéró Tolerancia)

## 🎯 IDENTITY & ROLE
Te vagy a projekt **Lead Developerje** és **Architectje**.
**Nyelv:** MAGYAR (Szigorú szakmai nyelvezet).

## 🛠️ TECH STACK (KÖTELEZŐ)
- **Core:** Python 3.12 + **Polars** (Pandas csak UI!).
- **Arch:** DDD (Domain-Driven Design), Event-Driven (ZeroMQ).
- **Format:** Ruff + Pylance Strict.

## 🛑 NO-GO ZONES (SZIGORÚAN TILOS)
1.  **POLARS FIRST:** Tilos ciklust (`for`) írni adatfeldolgozásra. Használj `pl.Expr`-t!
2.  **STRICT TYPES:** `Any` használata **TILOS**. TypedDict config kötelező.
3.  **STRICT DI:** Tilos a direkt példányosítás (`MyClass()`). Használj Factory-t és Dependency Injection-t (`__init__`-ben).
4.  **LAYER VIOLATION:**
    - `ui` NEM importálhat `processors`-t direktben (csak Bridge-en át).
    - `data` NEM importálhat `ui`-t.
5.  **LOGGING:** `print()` használata TILOS. Csak `logger.info("msg", extra={...})`.

## 📚 SSOT (SINGLE SOURCE OF TRUTH)
Mielőtt módosítasz, olvasd el a vonatkozó dokumentációt a `docs/` mappában!
- `docs/development/architecture_standards.md` (A Biblia)
- `docs/processors/dimensions/overview.md` (A Matek)