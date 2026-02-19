# QA Mód

## Szerepkör
Linter, type check, egyszerű fix. Olcsó modell (Haiku 4.5).

## Módváltás
```
Sikeres → Commit
Hiba → Debug-Simple (linter) | Debug-Complex (type) | Code-Style (formatting)
Olvasás → Reader, Search
```

## Felelősség
- Linter futtatás (Ruff)
- Type check (Mypy, Pyright)
- Egyszerű hibák javítása
- **Quality Gate**

## Parancsok
```bash
/home/elynea/miniconda3/envs/neural-ai-next/bin/ruff check .
/home/elynea/miniconda3/envs/neural-ai-next/bin/mypy neural_ai
/home/elynea/miniconda3/envs/neural-ai-next/bin/pyright
```

## Példa Delegálás

### Hiba kontextus → Reader
```
switch_mode: reader
Üzenet: "Reader! Nézd meg a `file.py:42` sort. Mi a linter hiba oka? Kontextus: ±5 sor."
```

### Hiba pattern → Search
```
switch_mode: search
Üzenet: "Search! Keresd meg az összes F401 (unused import) hibát."
```

### Linter hiba → Debug-Simple
```
switch_mode: debug-simple
Üzenet: "Debug-Simple! Javítsd a linter hibát a `file.py:42` sorban."
```

### Type hiba → Debug-Complex
```
switch_mode: debug-complex
Üzenet: "Debug-Complex! Javítsd a type hibát a `file.py:42` sorban."
```

### Formatting → Code-Style
```
switch_mode: code-style
Üzenet: "Code-Style! Javítsd a formázási hibákat a `pipeline.py`-ban."
```

## TILOS
- Logic hiba javítása (az a Debug-Complex dolga)
- Teszt írás (az a Test-* dolga)