# Debug Mód Szabályok (Nem Nyilvánvaló Csak)

- **🛡️ BIZTONSÁGI PROTOKOLL**: **TESZTEK FUTTATÁSA TILOS!** (pytest, python main.py). A rendszer instabil.
- **👁️ OBSERVABILITY AUDIT**: A hiba feltárásakor ellenőrizni kell a LoggerFactory használatot (`__name__` alapú) és a Trace dekorátorok meglétét.
- **🔍 DIAGNÓZIS**: Csak statikus analízis és fájl olvasás engedélyezett.
- **⚠️ PROBLEMS TAB**: Minden piros hiba a Problems fülben prioritást élvez.
- **🇭🇺 NYELV**: A gondolkodás és kommunikáció magyarul kötelező.
