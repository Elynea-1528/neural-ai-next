# Code Mód Szabályok (Nem Nyilvánvaló Csak)

- **🇭🇺 NYELV**: Magyar docstringek, kommentek KÖTELEZŐEK.
- **🛡️ BIZTONSÁGI PROTOKOLL**: **TESZTEK FUTTATÁSA TILOS!** (Kizárólag kódírás és linter/ruff engedélyezett).
- **👁️ OBSERVABILITY**:
  - Csak `LoggerFactory.get_logger(__name__)` engedélyezett. `structlog` és `print()` TILOS.
  - `@trace` dekorátor KÖTELEZŐ minden kritikus függvényre.
- **🧬 TÍPUSBIZTONSÁG**: `Any` TILOS. Configokhoz `TypedDict` definiálása és `cast()` KÖTELEZŐ a factory-ban.
- **🏗️ MODUL SZERKEZET & DI**: Konstruktor injektálás kötelező. Modul szerkezet: `interfaces/`, `implementations/`, `exceptions/`, `factory.py`, `__init__.py`. Abszolút importok kényszerítése.
- **📦 ADATKEZELÉS**: Polars (`pl.DataFrame`) kötelező a processzorokban. Pandas csak a UI-ban. **Polarsnál `for row in df` hurok TILOS.**
- **⚠️ QA**: Minden piros hiba (Ruff/MyPy) SZIGORÚAN javítandó commit előtt.
