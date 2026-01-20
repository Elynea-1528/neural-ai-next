# Architect Mód Szabályok (Nem Nyilvánvaló Csak)

- **🇭🇺 NYELV**: Minden kommunikáció, tervezés és dokumentáció MAGYARUL kötelező.
- **OPERATION TOTAL RECALL**: Jelenlegi fókusz: LoggerFactory helyreállítása és @trace dekorátorok bevezetése.
- **Réteges Architektúra (DDD)**: Szigorú függőségi irány: Presentation→Domain→Persistence→Input→Infrastructure (Core).
- **Bootstrap Lánc (Szigorú Sorrend)**: HardwareInfo→Config→Logger→EventBus→Storage→Database→SystemMonitor.
- **Granular Dashboard (SSOT)**: `docs/development/TASK_TREE.md` az SSOT. Fájl szintű követés (Stmt/Brch Coverage) kötelező.
- **🛡️ BIZTONSÁGI PROTOKOLL**: **TESZTEK FUTTATÁSA TILOS!** Kizárólag Statikus Kódanalízis és Kódírás tervezhető.
- **DI & TypedDict**: Konstruktor injektálás kötelező. Minden modul `factory.py`-jában kötelező a konfigurációs TypedDict tervezése.
- **Reality Check**: Minden delegálás előtt `ls -R` / `find` KÖTELEZŐ.
