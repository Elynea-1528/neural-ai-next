ökéletesen látod. A káosz elkerülése végett szigorú sorrendet kell tartanunk. Nem lehet építkezni, amíg nincs tervrajz, és nem lehet betonozni, amíg áll a szemét a telken.
Itt a "GRAND RELAUNCH PROTOKOLL". Ezt a 3 lépést kövesd, pontosan ebben a sorrendben.


1. FÁZIS: TAKARÍTÁS ÉS TERVEZÉS (Architect Only)
Ebben a fázisban az AI nem ír kódot, csak rendet rak, létrehozza a docs/planning mappát és megírja a specifikációkat. Te ezt nézed át.
Parancs (Új Chatben):


Architect! INDÍTSD A 'GENESIS REBOOT' (PLANNING PHASE) PROTOKOLLT.

HELYZET: A rendszer alapjai hiányosak, a dokumentáció elavult. Tiszta lapot nyitunk.
FELADAT: A teljes rendszer újratervezése és dokumentálása a kódolás előtt.

1. TAKARÍTÁS (Deep Clean):
   - Nézd át a `docs/development` mappát. Ami nem a v5.0 szabvány (régi checklistek), azt töröld vagy archiváld.
   - Hozd létre a `docs/planning/specs/` struktúrát.

2. SPECIFIKÁCIÓK LÉTREHOZÁSA (Blueprints):
   Írd meg a következő terveket a `docs/planning/specs/` mappába:
   - `01_architecture_overview.md`: Nagy kép (EventBus, DB, Parquet).
   - `02_core_database.md`: SQLAlchemy modellek és séma tervek.
   - `03_core_eventbus.md`: Event típusok és feliratkozási logika.
   - `04_data_warehouse.md`: Parquet particionálás és Big Data stratégia.
   - `05_main_system.md`: A `main.py` boot folyamata és a GUI előkészítés.

3. ROADMAP ÉS DASHBOARD:
   - Generáld le az ÚJ `docs/development/TASK_TREE.md`-t a v5.0 formátumban (Token, Complexity, Deps).
   - Töltsd fel a fenti tervek alapján a feladatokat.

INDÍTÁS:
- Csak dokumentálj! Ne implementálj semmit!
- Ha kész a terv, várd a jóváhagyásomat.



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