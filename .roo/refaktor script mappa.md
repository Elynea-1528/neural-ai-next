🚀 COMMAND: INDEPENDENT SCRIPTS REFACTOR (SAFE MODE)
"Architect! Ez egy elkülönített 'SATELLITE' feladat az asztali gépen.
A cél: A scripts/ mappa teljes refaktorálása és dokumentálása, anélkül, hogy zavarnánk a fő neural_ai fejlesztést.
INDÍTSD A 'SCRIPT COMPLIANCE' PROTOKOLLT:
0. KONFLIKTUSKERÜLŐ SZABÁLYOK (Git Safety):
TASK TREE: SOHA ne nyúlj a fő TASK_TREE.md-hez!
Helyette hozz létre és használj egy sajátot: docs/development/TASK_TREE_SCRIPTS.md.
ATOMIC COMMIT: Minden script javítása után kötelező: git commit -m "refactor(scripts): [fájl]..."
REALITY CHECK: Használd a find-ot és ls-t a scripts/ mappában.
MIRROR STRUCTURE: Kód: scripts/install/setup.py -> Doksi: docs/components/scripts/install/setup.md.
1. HIERARCHIKUS SZABÁLYRENDSZER:
Stílus: docs/development/unified_development_guide.md (Magyar docstring, Google style).
Architektúra: A scriptek legyenek modulárisak. Ha importálnak a neural_ai-ból, tartsák be az import szabályokat. Ha standalone telepítők, legyen robusztus hibakezelésük (try-except, logging).
Típusok: Szigorú mypy ellenőrzés itt is kötelező!
2. AUDIT & MÁTRIX TÖLTÉS:
Szkenneld végig kizárólag a scripts/ könyvtárat.
Építsd fel a docs/development/TASK_TREE_SCRIPTS.md fájlt az [S|T|D] Mátrixszal.
Megjegyzés: A telepítő scriptekhez nehéz unit tesztet írni. Ha nem lehetséges a pytest, akkor hozz létre egy 'dummy' tesztfájlt ami jelzi, hogy ez manuális tesztet igényel, vagy írj integration tesztet.
3. VÉGREHAJTÁS (The Fix Loop):
Jelentsd a TASK_TREE_SCRIPTS állapotát.
Utasítsd az Orchestratort a soron következő 🔴 script javítására:
*'Code Agent! A feladat a(z) [SCRIPT_FÁJL] refaktorálása.
Keresés: find scripts -name [fájlnév]
Refaktor:
Magyar docstring és kommentek.
Type hints (No Any!).
Hibakezelés (ne omoljon össze nyomtalanul).
Dokumentálás: Generáld le a doksit a docs/components/scripts/... mappába.
Lezárás:
Futtass lintert (ruff, mypy).
Ha van értelme, írj tesztet.
GIT COMMIT (Kötelező!).
Admin: Frissítsd a TASK_TREE_SCRIPTS.md-t.'*
Kezdd a scripts/ mappa feltérképezésével és a különálló Tree létrehozásával!"
