🚀 COMMAND: ULTIMATE REFACTOR & COMPLIANCE AUDIT (PRO VERSION)
"Architect! Csatoltam a FRISSÍTETT @docs mappát. Ez a rendszer megkérdőjelezhetetlen törvénykönyve (SSOT).
INDÍTSD A 'STRICT COMPLIANCE' PROTOKOLLT A KÖVETKEZŐ KIEGÉSZÍTÉSEKKEL:
0. KRITIKUS MŰKÖDÉSI SZABÁLYOK (Azonnali érvényűek):
ATOMIC COMMIT: Minden egyes sikeresen refaktorált fájl után KÖTELEZŐ a git commit -m "..." parancs futtatása. Ha nincs commit, a feladat ❌ FAILED.
REALITY CHECK: Soha ne találgass fájlneveket (pl. config_manager). Használd a find parancsot a pontos útvonal megtalálásához!
MIRROR STRUCTURE: A dokumentációnak mappaszinten követnie kell a kódot (pl. neural_ai/core/base/x.py -> docs/components/core/base/x.md). Ha rossz helyen van, mozgasd át!
1. HIERARCHIKUS SZABÁLYRENDSZER (Prioritások):
Development Guide: docs/development/unified_development_guide.md (Stílus: Hungarian docstrings, Google style, Type hints).
Architektúra: docs/development/core_dependencies.md (KRITIKUS! Körkörös importok ellen Bootstrap minta és NullObject pattern KÖTELEZŐ a core/base mappában).
Dimenziók: A processzoroknál (D1-D15) a docs/processors/dimensions/overview.md-ben leírt dict visszatérési értékek SZENTÍRÁSOK.
2. AUDIT & MÁTRIX TÖLTÉS:
Szkenneld végig a neural_ai/ könyvtárat (ls -R).
Frissítsd a docs/development/TASK_TREE.md-t az [S|T|D] Mátrixszal (Source | Test | Doc).
JELÖLÉS:
🔴 REFACTOR NEEDED: Ha a kód megvan, de angol kommentes, hiányzik a típus, VAGY megsérti a core_dependencies.md import szabályait.
🔴 DOCS MISSING: Ha a kód jó, de nincs meg a párja a docs/components/ (tükör) mappában.
3. VÉGREHAJTÁS (The Fix Loop):
Jelentsd a TASK_TREE állapotát.
Utasítsd az Orchestratort a legkritikusabb 🔴 elem javítására a következő SZIGORÍTOTT PROMPTTAL:
*'Code Agent! A feladat a(z) [FÁJL] refaktorálása.
Keresés: find . -name [fájlnév] (Bizonyosodj meg az útvonalról!).
Architektúra: Olvasd el a docs/development/core_dependencies.md-t. Használj TYPE_CHECKING blokkot az importokhoz!
Refaktor: Magyar docstring, Type hints (No Any!), Dependency Injection.
Dokumentálás: Generáld le a doksit a docs/components/... (tükör) mappába.
Lezárás: Futtass tesztet, majd GIT COMMIT! (Commit nélkül nem fogadom el).'
Kezdd a munkát a neural_ai/core/base modul szigorú átvizsgálásával és a TASK_TREE generálásával!"
