# Main Modul - Alkalmazás Belépési Pont

## Áttekintés

A `main.py` modul a Neural AI Next alkalmazás fő belépési pontját tartalmazza. Ez a szkript felelős az alkalmazás teljes életciklusának kezeléséért, a core komponensek inicializálásáért és a rendszer stabil működéséért.

## Szerkezet

### Fő Funkciók

#### `main() -> None`

Az alkalmazás fő aszinkron belépési pontja.

**Felelősségek:**
1. Core komponensek inicializálása a `bootstrap_core()` segítségével
2. Logger komponens lekérése és rendszerindítási üzenet naplózása
3. Esemény busz indítása (ha elérhető)
4. Adatbázis inicializálása (ha elérhető)
5. Örök futás biztosítása, amíg a felhasználó le nem állítja (Ctrl+C)
6. Hiba kezelése és naplózása

**Paraméterek:**
- Nincs paramétere

**Visszatérési érték:**
- `None`

**Kivételek:**
- `SystemExit`: Kritikus hiba esetén az alkalmazás leáll

**Példa:**
```python
await main()
```

### Típusosság és Függőség Injektálás

A modul szigorú típusosságot követ:

```python
from typing import TYPE_CHECKING

# Körkörös importok elkerüléséhez
if TYPE_CHECKING:
    from neural_ai.core.db.implementations.sqlalchemy_session import DatabaseManager
    from neural_ai.core.events.interfaces.event_bus_interface import EventBusInterface
    from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface

# Típusos változók
components: CoreComponents = bootstrap_core()
logger: "LoggerInterface | None" = components.logger
event_bus: "EventBusInterface | None" = components.event_bus
database: "DatabaseManager | None" = components.database
```

### Naplózás

A modul a következő üzeneteket naplózza:

- **Rendszer indítása**: `logger.info("Rendszer indítása", extra={"version": "0.5.0"})`
- **Rendszer fut**: `logger.info("Rendszer fut, eseményekre vár")`

### Hiba Kezelés

A modul két szinten kezeli a hibákat:

1. **Globális hiba kezelés** (a legfelső szinten):
   - `KeyboardInterrupt`: A felhasználó által generált Ctrl+C esemény
   - `Exception`: Bármely egyéb kivétel, amelyet kiír a konzolra és `sys.exit(1)`-el kilép

2. **Aszinkron hiba kezelés** (a `main()` függvényben):
   - A `suppress(asyncio.CancelledError)` biztosítja, hogy a CancelledError ne okozzon problémát

### Komponens Függőségek

A `main.py` a következő core komponenseket használja:

- **CoreComponents**: A rendszer összes alap komponensének tárolója
- **LoggerInterface**: Naplózási műveletekhez
- **EventBusInterface**: Eseményvezérelt kommunikációhoz
- **DatabaseManager**: Adatbázis műveletekhez

## Használat

### Alap indítás

```bash
python main.py
```

### Leállítás

Nyomd meg a `Ctrl+C` billentyűkombinációt a konzolon.

### Várható kimenet

```
2024-12-26 12:00:00 - NeuralAI - INFO - Rendszer indítása
2024-12-26 12:00:01 - NeuralAI - INFO - Rendszer fut, eseményekre vár
^C
🛑 Rendszer leállítva.
```

## Architektúra Elvek

### Dependency Injection

A modul nem példányosít közvetlenül osztályokat, hanem a `bootstrap_core()` függvényen keresztül kapja meg a komponenseket. Ez biztosítja a laza csatolást és a tesztelhetőséget.

### Típusos Változók

Minden változó explicit típusannotációval rendelkezik, ami javítja a kód olvashatóságát és segíti a statikus elemzőket.

### Optional Típusok

A komponensek `Optional` típusúak, mert a `bootstrap_core()` függvény visszaadhat `None` értékeket, ha egy komponens nem inicializálható. A kód minden komponens használata előtt ellenőrzi, hogy nem `None`-e.

## Fejlesztés

### Hibakeresés

A modul hibakereséséhez használhatod a következő technikákat:

1. **Logger szint módosítása**: Állítsd be a logger szintjét `DEBUG`-ra a részletesebb üzenetekért
2. **Komponens tesztelés**: A `bootstrap_core()` által visszaadott komponenseket külön is tesztelheted

### Tesztelés

A modul teszteléséhez lásd: [`tests/test_main.py`](../tests/test_main.py)

## Kapcsolódó Dokumentáció

- [Core Komponensek](../neural_ai/core/__init__.py)
- [Logger Interfész](../neural_ai/core/logger/interfaces/logger_interface.py)
- [Event Bus Interfész](../neural_ai/core/events/interfaces/event_bus_interface.py)
- [Database Manager](../neural_ai/core/db/implementations/sqlalchemy_session.py)