# Architect Mód Szabályok (Nem Nyilvánvaló Csak)

- **OPERATION TOTAL RECALL**: A rendszer jelenleg néma és instabil. A tervezés fókuszában a LoggerFactory helyreállítása és a Trace dekorátorok bevezetése áll.
- **Réteges Architektúra**: Presentation→Domain→Persistence→Input→Infrastructure (függőségek csak lefelé).
- **Bootstrap Lánc**: HardwareInfo→Config→Logger→EventBus→Storage→Database→SystemMonitor (szigorú sorrend).
- **Reality Check**: Minden delegálás előtt `ls -R` kötelező. Ne hallucinálj fájlokat!
- **Granular Dashboard**: A `docs/development/TASK_TREE.md` az SSOT. Fájl szintű követés kötelező Stmt/Brch coverage metrikákkal.
- **🛡️ BIZTONSÁGI PROTOKOLL**: **TESZTEK FUTTATÁSA TILOS!** Kizárólag Statikus Kódanalízis és Kódírás tervezhető.
- **DI Szabály**: Konstruktor injektálás kötelező; konkrét osztályok soha nem importálódnak közvetlenül.
- **TypedDict Definíció**: Minden modul `factory.py`-jában kötelező a konfigurációs TypedDict tervezése.
