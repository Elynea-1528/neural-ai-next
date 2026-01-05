# UI Service Factory

## Áttekintés

A `neural_ai.ui.factory` modul implementálja a UI szolgáltatások létrehozását és kezelését Dependency Injection minta szerint. Ez az osztály felelős a UI szolgáltatások egységes példányosításáért és életciklus-kezeléséért Singleton minta alkalmazásával.

## Architektúra

### Osztálystruktúra

```python
class UIServiceFactory(metaclass=SingletonMeta)
```

A factory Singleton mintát használ, így garantálva, hogy a rendszerben csak egy példány létezzen belőle. Ez biztosítja a konzisztens állapotkezelést és erőforrás-menedzsmentet.

### Főbb komponensek

- **`_bridge: CoreBridgeInterface | None`** - A backend bridge referenciája
- **`_services: dict[str, Any]`** - A létrehozott szolgáltatások gyorsítótár
- **`_initialized: bool`** - A factory inicializáltsági állapota

## Metódusok

### `__init__()`

```python
def __init__(self) -> None
```

A factory alapértelmezett inicializálása. Alapállapotban a bridge `None`, a szolgáltatások szótár üres, és az inicializáltsági flag `False`.

### `initialize(bridge: CoreBridgeInterface) -> None`

```python
def initialize(self, bridge: "CoreBridgeInterface") -> None
```

A factory inicializálása a backend bridge-el. Ez a metódus kötelezően meghívandó a factory használata előtt.

**Paraméterek:**
- `bridge`: A backend bridge példány, amelyen keresztül a szolgáltatások hozzáférnek a backend komponensekhez

### Szolgáltatáslekérdező metódusok

#### `get_navigation_service() -> NavigationServiceInterface`

A Navigation Service példányát adja vissza. Ha még nem létezik, létrehozza és eltárolja a gyorsítótárban.

#### `get_dashboard_service() -> DashboardServiceInterface`

A Dashboard Service példányát adja vissza.

#### `get_data_service() -> DataServiceInterface`

A Data Service példányát adja vissza. Ez a szolgáltatás felelős az adatok betöltéséért, szűréséért és kezeléséért Big Data támogatással.

#### `get_ai_service() -> AIServiceInterface`

Az AI Service példányát adja vissza.

#### `get_strategy_service() -> StrategyServiceInterface`

A Strategy Service példányát adja vissza.

#### `get_live_ops_service() -> LiveOpsServiceInterface`

A Live Ops Service példányát adja vissza.

### `get_all_services() -> dict[str, Any]`

```python
def get_all_services(self) -> dict[str, Any]
```

Visszaadja az összes szolgáltatás példányt egy szótárban. Biztosítja, hogy minden szolgáltatás létrejöjjön a hívás előtt.

**Visszatérési érték:**
- Szótár, amely tartalmazza az összes szolgáltatás példányt kulcs-érték párokként

### `reset() -> None`

```python
def reset(self) -> None
```

A factory visszaállítása alapállapotba. Törli a gyorsítótárazott szolgáltatásokat, visszaállítja az inicializáltsági flaget, és nullázza a bridge referenciát.

### `is_initialized: bool` property

```python
@property
def is_initialized(self) -> bool
```

Csak olvasható property, amely visszaadja a factory inicializáltsági állapotát.

## DataService Kompatibilitás

A factory teljes mértékben kompatibilis a frissített DataService-szel:

1. **Dependency Injection**: A DataService a konstruktorán keresztül kapja meg a CoreBridge-t
2. **Interfész alapú**: A factory interfész típusokat használ, nem konkrét implementációkat
3. **Lazy Loading**: A szolgáltatások csak akkor jönnek létre, amikor először lekérjük őket
4. **Singleton**: A DataService ugyanazt a példányt adja vissza minden hívásnál

### Példa a DataService használatára

```python
from neural_ai.ui.factory import UIServiceFactory
from neural_ai.ui.core_bridge import CoreBridge

# Factory inicializálása
factory = UIServiceFactory()
bridge = CoreBridge()
# ... bridge konfigurálása ...
factory.initialize(bridge)

# DataService lekérése
data_service = factory.get_data_service()

# Adatok betöltése
for chunk in data_service.load_data("tick_data", chunk_size=10000):
    # Chunk feldolgozása
    process_chunk(chunk)
```

## Hibakezelés

A factory szigorú hibakezelést valósít meg:

- **`RuntimeError`**: Ha a factory-t inicializálás nélkül próbáljuk használni
- **`ValueError`**: Ha érvénytelen paramétereket adunk meg
- **Típusellenőrzés**: Futási időben ellenőrzi az interfész kompatibilitást

## Teljesítményoptimalizálás

1. **Lazy Loading**: A szolgáltatások csak akkor jönnek létre, amikor szükség van rájuk
2. **Gyorsítótárazás**: A létrehozott szolgáltatások gyorsítótárban tárolódnak
3. **Singleton**: Csak egy példány létezik minden szolgáltatásból
4. **Dependency Injection**: Minimalizálja az erőforrás-felhasználást

## Tesztelés

A factory-t átfogó teszteszköz állomány fedi le:

- **21 teszteset** minden metódushoz
- **100% code coverage** (76 sor, 0 hiányzó sor)
- **Interfész kompatibilitás** ellenőrzése
- **Singleton minta** tesztelése
- **Hibakezelés** validálása

### Tesztfuttatás

```bash
# Összes teszt futtatása
pytest tests/ui/test_factory.py -v

# Code coverage jelentés
pytest tests/ui/test_factory.py --cov=neural_ai.ui.factory --cov-report=term-missing
```

## Kapcsolódó dokumentáció

- [`CoreBridge`](core_bridge.md) - A backend bridge implementációja
- [`DataService`](services/data_service.md) - Az adatkezelési szolgáltatás
- [`NavigationService`](services/navigation_service.md) - A navigációs szolgáltatás
- [`DashboardService`](services/dashboard_service.md) - Az irányítópult szolgáltatás
- [`AIService`](services/ai_service.md) - Az AI szolgáltatás
- [`StrategyService`](services/strategy_service.md) - A stratégia szolgáltatás
- [`LiveOpsService`](services/live_ops_service.md) - A live ops szolgáltatás

## Verziótörténet

- **v6.0**: Kezdeti implementáció a Neural AI Next rendszerhez
- **Kompatibilitás**: Python 3.12, PyTorch 2.5.1, Lightning 2.5.5