# Architect Mód Szabályok (Nem Nyilvánvaló Csak)

- **Réteges Architektúra**: Presentation→Domain→Persistence→Input→Infrastructure (függőségek csak lefelé)
- **Bootstrap Lánc**: HardwareInfo→Config→Logger→EventBus→Storage→Database→SystemMonitor (függőségi sorrend)
- **DDD Minta**: Domain-Driven Design event-driven (ZeroMQ/AsyncIO), adatbázis-első megközelítéssel
- **Modul Minta**: Minden modul: interfaces/ABC, implementations/konkret, exceptions/tipizált, factory/létrehozás, __init__/facade
- **Dependency Injection**: Konstruktor injektálás; konkrét osztályok soha nem importálódnak közvetlenül
- **Reality Check**: Mindig futtass `ls -R` / `find` parancsot tervezés előtt (nincs hallucinált fájl)
- **Granular Dashboard**: Fájl szintű követés TASK_TREE.md-ben Stmt/Brch coverage metrikákkal
- **Hierarchikus Rendszer**: Hivatkozz `docs/architecture/hierarchical_system/overview.md`-re rendszer tervezésnél