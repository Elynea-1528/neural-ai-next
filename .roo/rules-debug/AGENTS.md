# Debug Mód Szabályok (Nem Nyilvánvaló Csak)

- **QA Kapu Kötelező**: Kód csak akkor committolható, ha sikeresen átmegy `ruff check` és `pytest` teszteken
- **Abszolút Útvonalak**: Python, Ruff, Pytest parancsoknál teljes conda env útvonalak használata
- **Magyar Kommunikáció**: Minden debug kimenet, log és gondolkodás magyarul
- **Szigorú Típus Ellenőrzés**: Debug strict módban (`python.analysis.typeCheckingMode: "strict"`)
- **Nincs Print Utasítás**: Debug strukturált logolással `extra={}` paraméterekkel
- **Granular Coverage**: Stmt/Brch coverage metrikák követése minden modulnál