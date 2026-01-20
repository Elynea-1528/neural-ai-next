# Debug Mód Szabályok (Nem Nyilvánvaló Csak)

- **🇭🇺 NYELV**: A gondolkodás és kommunikáció MAGYARUL kötelező.
- **🛡️ BIZTONSÁGI PROTOKOLL**: **TESZTEK FUTTATÁSA TILOS!** (pytest, python main.py). Csak Statikus Kódanalízis, Linter futtatás és Kódírás.
- **🔍 DIAGNÓZIS**: Statikus analízis és fájl olvasás engedélyezett.
- **⚠️ PROBLEMS TAB**: Minden piros hiba (Ruff/MyPy) prioritást élvez.
- **👁️ OBSERVABILITY AUDIT**: Ellenőrizni kell a `LoggerFactory.get_logger(__name__)` és a `@trace` dekorátorok meglétét.
- **🛠️ PARANCS ÚTVONAL**: Linter futtatásához KÖTELEZŐ az abszolút útvonal: `/home/elynea/miniconda3/envs/neural-ai-next/bin/ruff check .`
