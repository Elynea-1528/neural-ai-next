# Main - Fő indító szkript

## Áttekintés

A `main.py` a Neural AI Next rendszer fő belépési pontja. Ez a modul felelős az alkalmazás életciklusának kezeléséért, a core komponensek inicializálásáért és a szolgáltatások indításáért.

## Architektúra

### Dependency Injection (DI) Elv

A main modul szigorúan követi a Dependency Injection elvet:

- **Interfész alapú kommunikáció**: A modul kizárólag interfészeken keresztül kommunikál a komponensekkel
- **Factory Pattern**: A komponenseket a `bootstrap_core()` függvényen keresztül kapja meg
- **Típusos hozzáférés**: A `CoreComponents` bundle biztosítja a típusos hozzáférést a szolgáltatásokhoz

### Komponens Struktúra

```python
CoreComponents:
├── logger: LoggerInterface
├── event_bus: EventBusInterface
├── database: DatabaseManager
└── config: ConfigManagerInterface
```

## Funkcionalitás

### Fő funkciók

1. **Core inicializálás**: A `bootstrap_core()` hívással történik
2. **Szolgáltatások indítása**:
   - Event Bus indítása (ha elérhető)
   - Adatbázis inicializálása (ha elérhető)
3. **Életciklus kezelés**:
   - Örök futás biztosítása
   - Elegáns leállás (Ctrl+C kezelése)
   - Hibakezelés és naplózás

### Hibakezelés

A modul robusztus hibakezelést valósít meg:

- **Kivétel kezelés**: A `suppress` kontextus kezeli a `CancelledError`-t
- **Globális hibakezelés**: A `__main__` blokk elkapja az összes nem várt kivételt
- **Rendszeres leállás**: A `KeyboardInterrupt` (Ctrl+C) elegáns leállítást biztosít

## Használat

### Futtatás

```bash
python main.py
```

### Modul importálása

```python
from main import main

# Aszinkron hívás
await main()
```

## Tesztelés

A modult átfogó tesztek védik:

- **Komponens inicializálás**: Ellenőrzi a logger, event bus és adatbázis helyes indítását
- **Resilience tesztek**: Teszteli a hiányzó komponensek esetét
- **Életciklus tesztek**: Ellenőrzi az elegáns leállítást
- **Entry point tesztek**: Validálja a `__main__` blokk helyes működését

### Teszt futtatása

```bash
# Összes teszt futtatása
pytest tests/test_main.py -v

# Coverage jelentés
pytest tests/test_main.py --cov=main --cov-report=html
```

## Kódminőség

- **Típusos**: Szigorú típusos jelölések (`Type Hints`)
- **Dokumentált**: Google Style docstring-ek (magyar nyelven)
- **Linter**: A `ruff check` 0 hibát jelez
- **Coverage**: 72% statement coverage (a hiányzó sorok a `__main__` blokk végrehajtási kódjai)

## Fejlesztés

### Előfeltételek

- Python 3.12+
- neural_ai.core csomag

### Kódolási szabványok

- **Nyelv**: Magyar docstring-ek és kommentek
- **Típusok**: `Optional`, `List`, `Dict` helyes használata
- **Importok**: `TYPE_CHECKING` blokk körkörös importok elkerüléséhez

### Extension Points

A main modul a következőképpen bővíthető:

1. **Új komponensek**: A `CoreComponents` bővítése új interfészekkel
2. **Életciklus hookok**: A `main()` függvény kibővítése előtte/utána hookokkal
3. **Konfiguráció**: A `bootstrap_core()` paraméterezése konfigurációs beállításokkal

## Kapcsolódó dokumentáció

- [Core Bootstrap](core/bootstrap.md) - A core inicializálás részletei
- [Architektúra szabványok](../development/architecture_standards.md) - A projekt architektúrája
- [TASK_TREE](../development/TASK_TREE.md) - A fejlesztés állapota