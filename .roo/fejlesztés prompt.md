"Architect! ÚJ FEJLESZTÉSI CIKLUST indítunk. A cél: [FEJLESZTÉS_NEVE] (pl. 'RSI Indikátor implementálása').
INDÍTSD A 'ZERO-TO-HERO' PROTOKOLLT:
1. TERVEZÉS (PLANNING PHASE):
Hozz létre egy új bejegyzést a docs/development/TASK_TREE.md-ben a megfelelő Fázis alatt.
Státusz: 🔴 PENDING.
Mátrix: [❌|❌|❌] (Mivel még semmi sincs kész).
Commitold a Tervet!
2. SPECIFIKÁCIÓ (SSOT CHECK):
Nézd meg a docs/processors/dimensions/overview.md-t (vagy releváns specifikációt).
Tervezd meg a visszatérési értékeket és az API-t a szabványok szerint.
3. KIVITELEZÉS (EXECUTION LOOP):
Utasítsd az Orchestratort a fejlesztésre a következő SZIGORÍTOTT paraméterekkel:
*'Code Agent! Fejleszd le a [FÁJL_NEVE] komponenst a nulláról.
Struktúra: Hozd létre a fájlt a helyes mappában (neural_ai/...).
Architektúra: Használj Factory patternt és Dependency Injection-t (core_dependencies.md).
Minőség: Magyar docstring, Type hints (No Any!), Ruff compliant.
Tükör Doksi: Hozd létre a mkdir -p docs/components/... paranccsal a mappát, majd a md fájlt.
Teszt: Írj hozzá pytest-et (100% coverage).
Commit: git add . && git commit -m "feat([SCOPE]): implement [NÉV] component"'*
4. ZÁRÁS:
Ha a Code Agent végzett (és a tesztek zöldek), frissítsd a TASK_TREE-t ✅-ra.
Kezdd a Tervezéssel és a TASK_TREE frissítésével!"
