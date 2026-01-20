# Code Mód Szabályok (Nem Nyilvánvaló Csak)

- **👁️ OBSERVABILITY (KÖTELEZŐ)**:
  - Csak `LoggerFactory.get_logger(__name__)` engedélyezett.
  - `structlog` direkt importja és a `print()` használata szigorúan TILOS.
  - `@trace` dekorátor használata minden kritikus üzleti logikát tartalmazó függvényre kötelező.
- **🧬 TÍPUSBIZTONSÁG**:
  - `config.get()` hívás után a factory-ban KÖTELEZŐ a `TypedDict` cast: `cast(MyConfig, raw_cfg)`.
  - Az `Any` típus használata a saját kódban TILOS.
- **🛡️ BIZTONSÁGI PROTOKOLL**: **TESZTEK FUTTATÁSA TILOS!** (pytest, python main.py). Csak kódírás és linter (ruff) használható.
- **🏗️ MODUL SZERKEZET**: Minden modulnál kötelező: `interfaces/`, `implementations/`, `exceptions/`, `factory.py`, `__init__.py`.
- **📦 ADAT**: Polars (`pl.DataFrame`) kötelező a processzorokban. Pandas csak a UI-ban.
- **🇭🇺 NYELV**: Magyar docstringek és kommentek kötelezőek.
- **⚠️ PROBLEMS TAB**: Minden linter hiba (piros) SZIGORÚAN javítandó a commit előtt.
