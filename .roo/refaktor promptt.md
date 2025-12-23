🚀 **COMMAND: ULTIMATE REFACTOR & COMPLIANCE AUDIT (PRO + PYLANCE STRICT EDITION)**

```text
"Architect! Csatoltam a FRISSÍTETT @docs mappát (benne az új verziókezelési szabályokkal). Ez a rendszer megkérdőjelezhetetlen törvénykönyve (SSOT).

INDÍTSD A 'STRICT COMPLIANCE' PROTOKOLLT A KÖVETKEZŐ BŐVÍTETT SZABÁLYRENDSZERREL:

0. KRITIKUS MŰKÖDÉSI SZABÁLYOK (Azonnali érvényűek):
   - ATOMIC COMMIT: Minden egyes sikeresen refaktorált fájl után KÖTELEZŐ a git commit -m "..." parancs futtatása. Ha nincs commit, a feladat ❌ FAILED.
   - REALITY CHECK: Soha ne találgass fájlneveket. Használd a `find` parancsot a pontos útvonal megtalálásához!
   - MIRROR STRUCTURE: A dokumentációnak mappaszinten követnie kell a kódot. Ha hiányzik, hozd létre!
   - PYLANCE STRICT MODE (ÚJ!): A kódnak Pylance 'basic' helyett 'strict' módban is hiba nélkül kell átmennie.
     * Tilos az 'Any' típus lusta használata.
     * Optional típusoknál kötelező a `None` check (`if x is not None`).
     * Használj `typing.cast`-ot, ha a típuslevezetés nem egyértelmű.
     * A körkörös importokat `if TYPE_CHECKING:` blokkal oldd meg, de a string forward reference-eket (`'ClassName'`) használd a típusannotációkban!

1. HIERARCHIKUS SZABÁLYRENDSZER (Prioritások):
   - Development Guide: docs/development/unified_development_guide.md (Kiemelten a 10. fejezet: Verziókezelés és Pylance Strict szabályok).
   - Architektúra: docs/development/core_dependencies.md (Bootstrap minta és NullObject pattern KÖTELEZŐ).
   - Dimenziók: A processzorok kimeneti formátuma (dict keys) SZENTÍRÁS.

2. AUDIT & MÁTRIX TÖLTÉS:
   - Szkenneld végig a neural_ai/ könyvtárat.
   - Frissítsd a docs/development/TASK_TREE.md-t.
   - JELÖLÉS:
     🔴 REFACTOR NEEDED: Ha a kód megvan, de:
        1. Angol kommentes.
        2. Pylance Strict hibát dob (pl. 'reportUnknownMemberType', 'reportOptionalMemberAccess').
        3. Hiányzik a verziókezelés (Version check).
     🔴 DOCS MISSING: Ha a kód jó, de nincs meg a párja a docs/components/ mappában.

3. VÉGREHAJTÁS (The Fix Loop):
   Jelentsd a TASK_TREE állapotát, majd utasítsd az Orchestratort a legkritikusabb 🔴 elem javítására ezzel a BŐVÍTETT PROMPTTAL:

   'Code Agent! A feladat a(z) [FÁJL] refaktorálása Strict módban.

   1. Keresés: find . -name [fájlnév]
   2. Architektúra: Kövesd a docs/development/core_dependencies.md-t.
   3. PYLANCE JAVÍTÁS (Priority #1):
      - Minden változónak és függvénynek legyen explicit típusa.
      - Szüntesd meg a 256+ Pylance hibát! Ne használj `# type: ignore`-t, helyette javítsd a kódot (pl. `assert variable is not None` vagy `cast(Type, variable)`).
      - Kezeld a `Circular Import` hibákat `TYPE_CHECKING` blokkal.
   4. VERZIÓKEZELÉS (Priority #2):
      - Implementáld a 10. fejezet szerinti verzióvizsgálatot (`schema_version` mentése/betöltése).
      - Az `__init__.py`-ben dinamikus verzióbetöltés legyen (`importlib.metadata`).
   5. Dokumentálás: Generáld le/frissítsd a tükör doksit magyar nyelven.
   6. Lezárás: Futtass tesztet, majd GIT COMMIT!

   Kezdd a munkát a `neural_ai/__init__.py` és a `neural_ai/core/base` modulok szigorú Pylance javításával!"
