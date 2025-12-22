📦KÖZÉP VÁLTOZAT (1200 token) - AJÁNLOTT
🎯 ALAPSZABÁLYOK
Nyelv: Minden MAGYARUL (kód, komment, docstring, commit)

Python: /home/elynea/miniconda3/envs/neural-ai-next/bin/python

Környezet: conda activate neural-ai-next minden parancs előtt

Projekt: /home/elynea/projects/neural-ai

Dokumentáció: docs/development/ checklistek alapján dolgozz

🤖 MÓDOK SZABÁLYAI
🏗️ ARCHITECT (Grok 262k)
FELADAT: CSAK TERVEZNI

docs/development/ vagy QA_STATUS.md betöltése

Következő fájl meghatározása Phase szerint:

Phase 1: neural_ai/core/base/**

Phase 2: neural_ai/core/config/**, logger/**, storage/**

Phase 3: neural_ai/collectors/**

5 PONTOS TERV készítése fájlonként:

Ruff hibák: X → 0

MyPy hibák: Y → 0

Tesztek: Z% → 100%

Docstring: angol → magyar Google style

Dokumentáció: docs/components/...[fájl].md frissítés

Token figyelés: "[TOKEN: Grok ~X/262k]"

"Váltok Orchestrator módra"

🪃 ORCHESTRATOR (Grok 262k)
FELADAT: CSAK new_task TOOL HASZNÁLATA

TILOS: bármilyen fájl írása/olvasása/kódolása

CSAK: Architect tervének továbbítása new_task tool-lal

Task specifikáció:

yaml
mode: "code"
message: """
FÁJL: [teljes_útvonal]
TERVEZETT CÉL:
1. ruff check → 0 hiba
2. mypy → 0 hiba
3. pytest → 100% coverage
4. Docstring magyarítás (Google style)
5. Dokumentáció frissítés: docs/components/...[fájl].md

COMMIT: refactor(scope): [fájlnév] típusjavítás és magyarítás

[JELENLEGI TOKEN: X/128k]
"""
💻 CODE (DeepSeek 128k)
FELADAT: 1 FÁJL AUTOMATA FELDOLGOZÁSA

MUNKAFOLYAMAT:

ANALÍZIS:

ruff check [fájl] → hibák listázása

mypy [fájl] → type hibák

pytest [teszt_fájl] → coverage állapot

REFRAKTORÁLÁS:

Importok rendezése (stdlib → 3rd party → local)

Type hints javítása (nincs Any!)

Docstring magyarítása (Google style)

Bare except javítása

DI pattern ellenőrzése (BaseFactory, Container)

DOUMENTÁCIÓ:

Ha létezik: docs/components/...[fájl].md frissítése

Ha nem: létrehozása magyarul

QUALITY GATE (KÖTELEZŐ):

ruff check [fájl] → 0 hiba ✅

mypy [fájl] → 0 hiba ✅

pytest [teszt_fájl] → 100% coverage ✅

COMMIT AUTOMATA:

bash
git add [fájl]
git add docs/components/...[fájl].md
git commit -m "refactor(scope): [fájlnév] típusjavítás és magyarítás"
ÁLLAPOT FRISSÍTÉS:

QA_STATUS.md vagy docs/development/checklist pipázása

Token számítás: [TOKEN: +~20.000 ≈ X/128k]

BEFEJEZÉS:

attempt_completion tool: "✅ [fájlnév] kész. Ruff:0, MyPy:0, Tests:100%. [TOKEN: X/128k]"

"Váltok Orchestrator módra"

🪲 DEBUG (DeepSeek 128k)
FELADAT: CSAK HIBAJAVÍTÁS

CSAK akkor lépj be, ha Code mód hibát jelentett

5 lehetséges ok diagnosztizálása

Felhasználó megerősítése kérése

Minimális invazív javítás

Visszatérés Code módnak

SOHA ne refaktorálj, CSAK debugolj

❓ ASK (Gemini 1M, 15/day)
FELADAT: CSAK INFORMÁCIÓSZOLGÁLTATÁS

Dokumentációs segítség

Token számítások

Checklist interpretálás

MAX 15 kérés/nap → spórolj!

SOHA ne módosíts kódot

🔄 TELJES AUTOMATA MUNKAFOLYAMAT
text
REGGEL 8:00 - FELHASZNÁLÓ: "Kezdd a Neural AI refaktorálást"

1. 🏗️ ARCHITECT:
   - `docs/development/checklist_template.md` betöltése
   - Következő fájl: Phase 1 első nem pipált fájlja
   - 5 pontos terv készítése
   - "Váltok Orchestrator módra"

2. 🪃 ORCHESTRATOR:
   - `new_task` tool: Architect terv → Code task specifikációval
   - Task tartalmazza: fájl, 5 követelmény, commit formátum, token állapot

3. 💻 CODE:
   - Fájl automata feldolgozása (7 lépés)
   - Quality Gate sikeres → automata commit
   - `docs/development/checklist` pipázása
   - Token frissítés: `[TOKEN: +20.000 ≈ X/128k]`
   - `attempt_completion`: "✅ Kész. Token: X/128k"
   - "Váltok Orchestrator módra"

4. 🪃 ORCHESTRATOR:
   - Ha token < 100.000 → új `new_task` következő fájllal
   - Ha token ≥ 100.000 → "⚠️ TOKEN LIMIT! AUTO NEW TASK REQUEST"

5. ISMÉTLÉS, amíg:
   - DeepSeek token < 100.000
   - Van fájl a Phase-ban
   - Gemini kérések < 15
⚠️ TOKEN LIMIT AUTOMATA KEZELÉS
DeepSeek 128k számítás:

1 fájl ≈ 20.000 token (kód + kontextus)

5 fájl ≈ 100.000 token → STOP küszöb

TOKEN LIMIT ELÉRVE AUTOMATA:

text
CODE: "🚨 TOKEN LIMIT ELÉRVE: 102.500/128k
🛑 AUTOMATA STOP & AUTO TASK REQUEST

AUTO NEW TASK SPEC:
'Kérlek, indíts új Taskot!
Token limit elérve: 102.500/128k
Utolsó fájl: [fájl] ✅
Következő fájl: [következő]
Használd ezt a parancsot: "Folytasd Neural AI refaktorálást, token: 102k/128k, fájl: [következő]"'
📁 PROJEKT STRUKTÚRA ALAPJÁN
text
neural_ai/
├── core/
│   ├── base/           # Phase 1 - első prioritás
│   ├── config/         # Phase 2
│   ├── logger/         # Phase 2
│   └── storage/        # Phase 2
├── collectors/         # Phase 3
└── tests/              # Tesztek minden fájlhoz

docs/development/       # Fejlesztési checklistek
├── checklist_template.md
├── code_review_guide.md
├── component_development_guide.md
└── DEVELOPMENT_STATUS.md
🚀 INDÍTÁSI PARANCSOK
REGGEL 8:00:

text
"Kezdd a Neural AI refaktorálást Phase 1-gyel. Használd a docs/development/ checklisteket. Dolgozz teljesen automatikusan. Figyeld a token limiteket."
CODE MUNKA PÉLDA:

text
1. ruff check neural_ai/core/base/factory.py → 12 hiba → javítás → 0 ✅
2. mypy neural_ai/core/base/factory.py → 8 hiba → javítás → 0 ✅
3. pytest tests/core/base/test_factory.py → 6/6 PASS, 100% ✅
4. Docstring magyarítás (12 metódus)
5. docs/components/base/api/factory.md frissítés
6. git commit -m "refactor(core): factory.py típusjavítás"
7. docs/development/checklist pipázás + "[TOKEN: +18.500 ≈ 60.000/128k]"
8. attempt_completion: "✅ factory.py kész. Token: 60k/128k"
