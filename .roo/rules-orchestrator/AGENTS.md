# Orchestrator Mód Szabályok (Nem Nyilvánvaló Csak)

- **Delegálási Sablon**: Használd a pontos sablont Code Agent delegáláshoz DI, réteg, import specifikációkkal
- **Fájl Lebontás**: Komplex feladatokat bonts egyéni fájlműveletekre (3 fájl létrehozása, 2 módosítása)
- **Architektúra Kikényszerítés**: Biztosítsd hogy minden delegált feladat követi a réteges architektúrát és factory mintát
- **Magyar Tervezés**: Minden feladatleírás, lebontás és kommunikáció magyarul
- **QA Ellenőrzés**: Követeld Code Agent-től QA Kapu (ruff + pytest) és commit hash jelentését
- **Atomikus Műveletek**: Egy fájlváltoztatás per delegáció, azonnali commit követő