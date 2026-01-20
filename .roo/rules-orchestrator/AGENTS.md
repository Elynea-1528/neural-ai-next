# Orchestrator Mód Szabályok (Nem Nyilvánvaló Csak)

- **DELEGÁLÁSI PROTOKOLL**: Minden feladatnál kötelezően át kell adni a Code Agentnek:
  - LoggerFactory elvárást (`__name__` alapú).
  - @trace dekorátor elvárást.
  - TypedDict cast elvárást a factory-ban.
  - Szigorú réteg korlátozásokat.
- **🛡️ BIZTONSÁGI PROTOKOLL**: Szigorúan TILOS olyan feladatot kiadni, ami tesztfuttatást (`pytest`) igényel.
- **🇭🇺 NYELV**: Minden delegálás és tervezés magyarul kötelező.
- **📝 DASHBOARD FRISSÍTÉS**: Minden sikeres commit után követeld meg a `TASK_TREE.md` frissítését.
