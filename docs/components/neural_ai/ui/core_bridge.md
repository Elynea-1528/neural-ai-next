# Core Bridge

## Áttekintés

A `CoreBridge` osztály a felhasználói felület (UI) és a Neural AI Next rendszer magja (Core) közötti kapcsolatot biztosítja. Ez az osztály implementálja a Singleton tervezési mintát, és felelős a Core rendszer inicializálásáért, komponensek lekéréséért, valamint a parancsok és rendszerinformációk továbbításáért.

## Architektúra

### Osztálydiagram

```python
class CoreBridge:
    - _instance: Optional[CoreBridge]
    - _core: Optional[CoreComponents]
    - _connected: bool
    - _strategy_service: Optional[StrategyServiceInterface]

    + get_instance() -> CoreBridgeInterface
    + initialize() -> None
    + get_component(component_type: str) -> object | None
    + send_command(command: str, params: Dict[str, Any]) -> Dict[str, Any]
    + get_system_info() -> Dict[str, Any]
    + core: property
    + is_connected: property
```

### Függőségek

- **Core rendszer**: A `neural_ai.core.bootstrap_core()` függvényen keresztül inicializálja a Core-t
- **Logger**: A Core rendszer logger komponensét használja
- **Storage**: Parquet storage komponens a big data műveletekhez
- **JForex Downloader**: BI5 adatok letöltéséhez
- **Config**: Konfiguráció kezelés
- **Strategy Service**: Kereskedési stratégiák kezelése

## Metódusok

### `get_instance()`

```python
def get_instance() -> "CoreBridgeInterface":
    """Singleton példány lekérése."""
```

**Visszatérési érték:**
- A CoreBridge singleton példánya

**Leírás:**
- A Singleton minta implementációja, biztosítja, hogy csak egy példány létezzen az alkalmazás élettartama alatt

---

### `initialize()`

```python
def initialize() -> None:
    """Core rendszer inicializálása."""
```

**Kivételek:**
- `RuntimeError`: Ha az inicializálás sikertelen

**Leírás:**
- Meghívja a `bootstrap_core()` függvényt a Core rendszer inicializálásához
- Beállítja a `_connected` állapotot `True`-ra sikeres inicializálás esetén
- Naplózza az inicializálást az info szinten
- Inicializálja a Strategy Service-t

---

### `get_component()`

```python
def get_component(self, component_type: str) -> object | None:
    """Komponens lekérése típus alapján."""
```

**Paraméterek:**
- `component_type` (str): A lekérendő komponens típusa. Támogatott értékek:
  - `"parquet_storage"`: Parquet alapú adattároló komponens
  - `"bi5_downloader"`: JForex BI5 adatletöltő komponens
  - `"strategy_service"`: Kereskedési stratégiák kezelő szolgáltatás
  - `"config"`: Konfiguráció kezelő komponens

**Visszatérési érték:**
- A lekért komponens példánya vagy None

**Kivételek:**
- `RuntimeError`: Ha a bridge nincs inicializálva

**Leírás:**
- A `parquet_storage` esetén a Core storage komponensét adja vissza
- A `bi5_downloader` esetén a JForexFactory.create_downloader() hívással hozza létre a letöltőt
- A `strategy_service` esetén a Strategy Service komponenst adja vissza
- A `config` esetén a Core config komponensét adja vissza biztonságos hozzáféréssel
- A JForex downloader létrehozásakor `event_bus=None` paramétert használ (UI Direct Mode)

---

### `send_command()`

```python
def send_command(
    self,
    command: str,
    params: Dict[str, Any]
) -> Dict[str, Any]:
    """Parancs küldése a Core rendszernek."""
```

**Paraméterek:**
- `command` (str): A végrehajtandó parancs
- `params` (Dict[str, Any]): A parancshoz tartozó paraméterek

**Visszatérési érték:**
- A parancs végrehajtásának eredménye dictionary formátumban

**Kivételek:**
- `RuntimeError`: Ha a bridge nincs inicializálva

**Leírás:**
- Továbbítja a parancsot a Core rendszernek
- Visszaadja a végrehajtás eredményét

---

### `get_system_info()`

```python
def get_system_info(self) -> Dict[str, Any]:
    """Rendszerinformáció lekérése."""
```

**Visszatérési érték:**
- A rendszer aktuális állapotinformációi dictionary formátumban

**Kivételek:**
- `RuntimeError`: Ha a bridge nincs inicializálva

**Leírás:**
- Lekéri a Core rendszer állapotinformációit
- Információk tartalmazzák a verziót, komponensek állapotát, stb.

---

## Tulajdonságok

### `core` (property)

```python
@property
def core(self) -> Optional[CoreComponents]:
    """Core rendszer példányának lekérése."""
```

**Visszatérési érték:**
- A Core rendszer példánya vagy None

---

### `is_connected` (property)

```python
@property
def is_connected(self) -> bool:
    """Kapcsolati állapot lekérdezése."""
```

**Visszatérési érték:**
- `True`, ha a bridge inicializálva van és csatlakoztatott
- `False` egyébként

---

## Használati példa

```python
from neural_ai.ui.core_bridge import CoreBridge

# CoreBridge példány lekérése
bridge = CoreBridge()

# Core rendszer inicializálása
bridge.initialize()

# Komponensek lekérése
storage = bridge.get_component("parquet_storage")
downloader = bridge.get_component("bi5_downloader")
strategy_service = bridge.get_component("strategy_service")
config = bridge.get_component("config")

# Parancs küldése
result = bridge.send_command("process_data", {"symbol": "EURUSD"})

# Rendszerinformáció lekérése
info = bridge.get_system_info()

# Kapcsolati állapot ellenőrzése
if bridge.is_connected:
    print("Core Bridge csatlakoztatva")
```

## Implementáció részletei

### Singleton minta

A CoreBridge osztály a Singleton tervezési mintát implementálja, ami biztosítja, hogy az alkalmazásban csak egy példány létezzen belőle. Ez kritikus fontosságú a Core rendszer egységes kezeléséhez.

### Dependency Injection

A CoreBridge nem példányosít közvetlenül komponenseket, hanem a Core rendszer Factory metódusait használja:

- **Parquet Storage**: A Core storage komponensét közvetlenül visszaadja
- **BI5 Downloader**: A `JForexFactory.create_downloader()` hívással hozza létre
- **Strategy Service**: A StrategyService osztályt példányosítja, ha szükséges
- **Config**: A Core config komponensét közvetlenül visszaadja

### Big Data támogatás

A CoreBridge támogatja a big data műveleteket:

- **Parquet formátum**: Particionált Parquet fájlok kezelése
- **Chunkolás**: Nagy adatmennyiségek feldolgozása chunkokban
- **Aszinkronitás**: Aszinkron műveletek támogatása

### UI Direct Mode

A JForex downloader létrehozásakor `event_bus=None` paramétert használ, ami az ún. "UI Direct Mode"-ot aktiválja. Ez azt jelenti, hogy a letöltő közvetlenül kommunikál a UI-val, nem pedig eseményvezérelt módon.

## Hibakezelés

A CoreBridge robusztus hibakezelést implementál:

- **Inicializálási hibák**: `RuntimeError` kivételt dob, ha a Core rendszer inicializálása sikertelen
- **Komponens hibák**: Loggolja a hibákat és None-t ad vissza sikertelen komponens létrehozáskor
- **Kapcsolati hibák**: `RuntimeError` kivétel, ha műveletet próbálnak végrehajtani inicializálatlan bridge-en

## Tesztelés

A CoreBridge osztályt átfogó tesztesetekkel ellenőrizzük:

- **Singleton minta**: Két példány létrehozása és azonosságuk ellenőrzése
- **Inicializálás**: Sikeres és sikertelen inicializálás tesztelése
- **Komponens lekérés**: Minden támogatott komponens típus lekérésének tesztelése
- **Parancs küldés**: Parancsok továbbításának tesztelése
- **Rendszerinformáció**: Rendszerállapot lekérdezésének tesztelése
- **Tulajdonságok**: Core és is_connected property-k tesztelése

## Kapcsolódó dokumentáció

- [UI Architektúra](docs/components/ui/architecture.md)
- [Core rendszer](docs/components/core/base/index.md)
- [JForex Collector](docs/components/collectors/jforex/index.md)
- [Parquet Storage](docs/components/core/storage/implementations/parquet_storage.md)
- [Strategy Service](docs/components/neural_ai/ui/services/strategy_service.md)