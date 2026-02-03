# 🏛️ NEURAL AI NEXT - PROJECT RULES (CODEX v4.0)

## 🏗️ ARCHITEKTÚRÁLIS RÉTEGEK (DDD)
- UI (Presentation) -> Processors (Domain) -> Data (Persistence) -> Collectors (Input) -> Core (Infra).
- Szigorú irány: Hivatkozás csak fentről lefelé engedélyezett.

## 🐍 TECHNIKAI SZIGORÍTÁS
- **POLARS FIRST:** Adatfeldolgozásnál (`processors`, `data`, `collectors`) TILOS a Pandas és a `for` ciklus. Kizárólag `pl.Expr` és vektorizált műveletek.
- **STRICT DI:** Tilos a direkt példányosítás. Minden függőséget Factory-n keresztül, konstruktorban kell átvenni.
- **TYPE SAFETY:** `Any` használata TILOS. Pydantic modellek használata kötelező a konfigurációnál.
- **STORAGE:** Tilos CSV/JSON tárolás. Kizárólag particionált Parquet.
- **LOGGING:** `print()` TILOS. Kizárólag strukturált `structlog`.

## 📜 SSOT DOKUMENTUMOK
Minden döntés alapja:
1. `docs/development/architecture_standards.md`
2. `docs/processors/dimensions/overview.md`
3. `docs/models/overview.md`
4. `docs/planning/technical_design/01_processor_architecture.md`