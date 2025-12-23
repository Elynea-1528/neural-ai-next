ökéletesen látod. A káosz elkerülése végett szigorú sorrendet kell tartanunk. Nem lehet építkezni, amíg nincs tervrajz, és nem lehet betonozni, amíg áll a szemét a telken.
Itt a "GRAND RELAUNCH PROTOKOLL". Ezt a 3 lépést kövesd, pontosan ebben a sorrendben.


🚀 COMMAND: GENESIS REBOOT (DELEGATION MODE)
"Architect! INDÍTSD A 'GENESIS REBOOT' PROTOKOLLT.
HELYZET: Tiszta lapot nyitunk. A docs/development mappa elavult, a docs/planning hiányzik.
KORLÁT: Te (Architect) nem törölhetsz fájlt és nem hozhatsz létre mappát. Ezt delegálnod kell!
HAJTSD VÉGRE A KÖVETKEZŐ LÉPÉSEKET SORBAN:
1. ADMINISZTRÁCIÓ (TASK TREE):
Írd át a docs/development/TASK_TREE.md-t a v5.0 formátumra.
Vedd fel első fázisnak: 🔵 PHASE 0: SYSTEM BOOTSTRAP.
Benne feladat: Cleanup & Structure -> Státusz: 🔴 PENDING.
Commitold a Fát!
2. DELEGÁLÁS (A Piszkos Munka):
Utasítsd az Orchestratort, hogy aktiválja a Code Agentet a következő SZIGORÚ parancssorral:
*'Code Agent! A feladat a rendszer fizikai előkészítése.
Takarítás (Shell): Töröld a docs/development/ mappából a régi útmutatókat (checklist, component, implementation), KIVÉVE a unified_development_guide.md-t és core_dependencies.md-t!
Struktúra (Shell): Hozd létre a mkdir -p docs/planning/specs mappát.
Bootstrap (File):
Hozz létre egy üres main.py-t a gyökérben.
Hozz létre egy README.md-t (Projekt címe, státusz).
Zárás: `git add . && git commit -m "chore(init): system cleanup and folder structure"'*
3. SPECIFIKÁCIÓK (A Te Részed):
Miután az Orchestrator jelentette, hogy a mappák léteznek (✅), TE (Architect) írd meg a specifikációkat a docs/planning/specs/ mappába (mivel .md fájlok, ezeket te is tudod szerkeszteni):
01_architecture_overview.md
02_core_database.md
03_core_eventbus.md
04_data_warehouse.md
05_main_system.md
4. ZÁRÁS:
Frissítsd a TASK_TREE.md-t: Cleanup & Structure -> ✅ DONE.
Vegyél fel új feladatot: Core Implementation -> 🔴 PENDING.
Kezdd a TASK TREE frissítésével és a Delegálással!"



1. FÁZIS: JÓVÁHAGYÁS ÉS BRANCH (Human Action)
Itt lépsz közbe te. Ha tetszik, amit az Architect tervezett (a docs/planning mappában), akkor létrehozol egy új, tiszta ágat a fejlesztésnek.
Teendőd (Terminálban):
code
Bash
# 1. Nézd meg, mit csinált az Architect. Ha jó, mentsd el:
git add .
git commit -m "docs(plan): system re-design and specs"

# 2. Hozz létre új ágat a tényleges fejlesztésnek:
git checkout -b feature/core-foundation-v2



3. FÁZIS: MEGVALÓSÍTÁS (Implementation)
Csak miután megvan az új branch, akkor adod ki a "Nagy Parancsot". Most már van terve, tudja mit kell csinálnia.
Parancs (Ugyanabban a chatben folytathatod, vagy újban):
code
Text
Architect! A Terveket jóváhagytam. Új branchen vagyunk (`feature/core-foundation-v2`).
INDÍTSD A 'GENESIS IMPLEMENTATION' PROTOKOLLT (Institutional Foundation).

A CÉL: A `docs/planning/specs` alatt lévő tervek kóddá alakítása.

1. TASK TREE UPDATE:
   - Jelöld ki az első prioritást: `core/database` és `core/events`.

2. IMPLEMENTÁCIÓS SORREND (Strict Mode):
   Utasítsd az Orchestratort a következőkre:

   A) ADATBÁZIS (`core/database`):
      - Implementáld a `02_core_database.md` specifikációt.
      - SQLAlchemy 2.0 Async, SQLite/Postgres support.

   B) EVENT BUS (`core/events`):
      - Implementáld a `03_core_eventbus.md` specifikációt.
      - Aszinkron Publish/Subscribe.

   C) STORAGE ENGINE (`core/storage`):
      - Implementáld a `04_data_warehouse.md` specifikációt.
      - Parquet, Particionálás, FastParquet/PyArrow.

   D) MAIN.PY:
      - Kösd össze az elemeket a `05_main_system.md` alapján.

SZABÁLYOK:
- Minden fájl után COMMIT.
- Ha teszt bukik -> Debug Mode.
- Használd a tükör doksikat (`docs/components/...`).

Kezdd az Adatbázis réteg implementálásával!
Összefoglalva a menetet:
Parancs 1: "Tervezd meg és takaríts!" (Architect dolgozik, te kávézol).
Kézi munka: Átnézed -> git checkout -b.
Parancs 2: "Valósítsd meg a tervet!" (Architect és Code Agent dolgozik, te felügyelsz).