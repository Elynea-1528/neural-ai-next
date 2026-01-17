# Code Mód Szabályok (Nem Nyilvánvaló Csak)

- **Modul Minta**: Minden modulnak kötelezően tartalmaznia kell: `interfaces/`, `implementations/`, `exceptions/`, `factory.py`, `__init__.py`
- **Dependency Injection**: Implementációkat soha ne importálj közvetlenül; használd az interfészeket és factory mintát
- **TypedDict Konfiguráció**: A `config.get()` eredményeket mindig castold TypedDict-re a factory-ban
- **Nincs Any Típus**: Szigorú típusozás kényszerített; saját kódban `Any` TILOS
- **Polars Első**: Processzorokban csak `pl.DataFrame`; Pandas csak UI rétegben
- **Strukturált Logolás**: Használd `logger.info("üzenet", extra={"kulcs": érték})`; `print()` TILOS
- **QA Kapu**: Kód csak akkor committolható, ha átmegy a `ruff check` és `pytest` teszteken
- **Abszolút Importok**: Modulok között kötelező; relatív importok csak modulon belül engedélyezettek
- **Körkörös Hivatkozások**: Elkerülése `TYPE_CHECKING` blokkal string-hivatkozásokkal interfészekre
- **Google Docstring**: Magyar nyelvű Google stílusú docstringek kötelezőek minden függvényhez