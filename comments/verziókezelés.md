Ez egy kiváló stratégiai kérdés. Sokan elkövetik azt a hibát, hogy túlbonyolítják a verziózást, vagy épp elhanyagolják.
Mivel "Institutional Grade" rendszert építünk, a válaszom egyértelmű: NE verziózd a fájlokat egyenként kézzel a kódban, mert az káoszhoz vezet.
Itt a "Best Practice" (Bevált Gyakorlat) a modern szoftverfejlesztésben:
1. MIÉRT NE VERZIÓZD A FÁJLOKAT (A Fájl Fejlécében)?
Ha minden fájlba beleírjuk, hogy __version__ = "1.0.5", és ezt az AI-val próbáljuk léptetni minden módosításnál:
Zaj: A Git history tele lesz "bump version" bejegyzésekkel ahelyett, hogy a lényegi változást látnád.
Hibaforrás: Az AI el fogja felejteni. Vagy 1.0.5-ről véletlenül 1.0.7-re ugrik.
Felesleges: A GIT pontosan erre való. Minden egyes commit hash (pl. a1b2c3d) egy pontos verziója a fájlnak. A Git a te fájl-verziókezelőd.
2. A HELYES ÚT: SEMANTIC VERSIONING (A Projekt Szintjén)
A verziózást a PROJEKTRE alkalmazzuk, nem a fájlokra.
A formátum: MAJOR.MINOR.PATCH (pl. 0.2.1)
MAJOR (0.x.x): Hatalmas változás, ami mindent eltörhet (pl. a mostani Refactor).
MINOR (x.1.x): Új funkció (pl. JForex Collector elkészült).
PATCH (x.x.1): Hibajavítás (pl. a tesztek zöldre hozása).
Hol tároljuk?
Egyetlen helyen: pyproject.toml (és esetleg a fő neural_ai/__init__.py-ban, hogy a kód is lássa).
🏛️ A JAVASOLT STRATÉGIA (Így csináljuk mostantól)
Ne várj a végéig az 1.0-val, de ne is verziózz túl korán. Kövesd a "Milestone" (Mérföldkő) alapú verziózást:
Jelenlegi állapot: 0.1.0 (Pre-Alpha / Prototípus).
A Nagy Refactor után: Ez egy hatalmas ugrás. Ha minden zöld (Tesztek + Struktúra), akkor léptetünk 0.2.0-ra. Ez jelzi, hogy "Stabil az Alap".
Collectorok után: Ha kész a JForex és MT5, az lesz a 0.3.0.
Teendő:
Nem kell a Custom Instructions-be bonyolult szabályokat írni a fájlverziókról. Helyette a Release Managementet vezetjük be.
🚀 A "RELEASE COMMAND" (Ezt használd mérföldköveknél)
Amikor egy nagy fázissal (Phase) végzünk, kiadjuk ezt a parancsot az AI-nak. Ez elvégzi a verzióemelést profin.
(Ezt mentsd el későbbre, akkor használd, ha a Refactor + Exception javítás ✅ DONE)
"Architect! RELEASE PROTOKOLL INDÍTÁSA.
HELYZET: Befejeztük a Phase 1.5 (Architektúra Refactor) fázist. A rendszer stabil, a tesztek zöldek.
FELADAT: Verzióemelés (Bump Version) 0.2.0-ra.
FRISSÍTÉS: Írd át a verziót 0.2.0-ra ezekben a fájlokban:
pyproject.toml
neural_ai/__init__.py
CHANGELOG: Hozz létre/Frissítsd a CHANGELOG.md fájlt a gyökérben.
Írd bele a dátumot és a fő változásokat (Architecture Standardization, Interface segregation, Strict Typing).
LEZÁRÁS:
git add .
git commit -m "chore(release): bump version to 0.2.0 - Architecture Refactor Complete"
git tag v0.2.0 (Ha van jogosultsága, ha nincs, ezt te csinálod kézzel).
HAJTSD VÉGRE!"
Összegzés:
Fájlok: Bízd a Gitre.
Projekt: Használd a pyproject.toml-t.
Mikor? Minden sikeres Fázis (Phase) végén.
1.0.0: Majd akkor, ha az első éles Trade lement pénzzel.
Most fókuszálj a Refactorra, az a legfontosabb!