# 🏛️ NEURAL AI NEXT - PROJECT RULES (CODEX v4.0)

## 🏗️ ARCHITEKTÚRÁLIS RÉTEGEK (DDD)
- UI (Presentation) -> Processors (Domain) -> Data (Persistence) -> Collectors (Input) -> Core (Infra).
- Szigorú irány: Hivatkozás csak fentről lefelé engedélyezett.

## 🐍 TECHNIKAI SZIGORÍTÁS
- **POLARS FIRST:** Adatfeldolgozásnál (`processors`, `data`, `collectors`) TILOS a Pandas és a `for` ciklus. Kizárólag `pl.Expr` és vektorizált műveletek.
- **STRICT DI:** Tilos a direkt példányosítás. Minden függőséget Factory-n keresztül, konstruktorban kell átvenni.
- **PYDANTIC CONFIG:** Minden konfigurációt Pydantic modelleken keresztül KELL kezelni. Ez az új szabvány!
- **STRICT DI:** Tilos a direkt példányosítás. Factory + Constructor Injection kötelező.
- **NO LAZINESS:** Audit során minden fájlt meg kell vizsgálni. Tilos az összefoglalás (Zero-Compression Audit).
- **STORAGE:** Tilos CSV/JSON tárolás. Kizárólag particionált Parquet.
- **LOGGING:** `print()` TILOS. Kizárólag strukturált `structlog`.

## 📁 MAPPASZERKEZET
Minden modul: `interfaces/`, `implementations/`, `exceptions/`, `factory.py`, `__init__.py`.

## 📜 SSOT - AZ IGAZSÁG FORRÁSAI (KÖTELEZŐ OLVASMÁNY)
Mielőtt bármilyen elemzést adnál, kötelezően olvasd be és vedd figyelembe az alábbi 7 dokumentumot:
1. `docs/processors/dimensions/overview.md` (Matematikai definíciók)
2. `docs/planning/technical_design/01_processor_architecture.md` (Rendszerterv)
3. `docs/models/hierarchical/structure.md` (AI modell bemeneti igények)
4. `docs/architecture/hierarchical_system/overview.md` (Logikai hierarchia)
5. `docs/development/architecture_standards.md` (Kódolási törvény)
6. `docs/development/custom_instructions.md` (Működési protokoll)
7. `docs/development/TASK_TREE.md` (Aktuális állapot és Dashboard)