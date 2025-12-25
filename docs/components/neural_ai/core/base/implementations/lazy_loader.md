# Lazy Loader - Lustatöltés segédeszközök

## Áttekintés

Ez a modul a lustatöltés (lazy loading) mechanizmust valósítja meg, amely lehetővé teszi, hogy a drága erőforrások csak akkor töltődjenek be, amikor valóban szükség van rájuk. Ez jelentősen javítja az alkalmazás indítási idejét és a memóriahasználatot.

## Exportált osztályok és függvények

- `LazyLoader[T]` - Drága erőforrások lustatöltője
- `lazy_property` - Dekorátor lustatöltésű property-k létrehozásához

## Osztályok

### `LazyLoader[T]`

**Hely:** [`neural_ai.core.base.implementations.lazy_loader:17`](neural_ai/core/base/implementations/lazy_loader.py:17)

Drága erőforrások lustatöltője. Ez az osztály lehetővé teszi, hogy a drága erőforrások (pl. konfigurációk, adatbázis kapcsolatok, nagy adathalmazok) csak akkor töltődjenek be, amikor valóban szükség van rájuk.

A lustatöltés szálbiztos, így többszálú környezetben is biztonságosan használható.

#### Metódusok

##### `__init__(loader_func: Callable[[], T]) -> None`
Inicializálja a lustatöltőt.

**Paraméterek:**
- `loader_func`: A függvény, amely betölti az erőforrást. Ennek a függvénynek vissza kell térnie a betöltött erőforrással.

**Példa:**
```python
from neural_ai.core.base.implementations.lazy_loader import LazyLoader

def load_configuration():
    print("Konfiguráció betöltése...")
    return {"setting": "value"}

loader = LazyLoader(load_configuration)
# A load_configuration még nem futott le
```

##### `_load() -> T`
Betölti az erőforrást, ha még nincs betöltve.

**Visszatérési érték:** A betöltött erőforrás

**Megjegyzés:** Ez egy belső metódus, általában nem kell közvetlenül használni. Ehelyett használd a `__call__` metódust.

##### `__call__() -> T`
Visszaadja a betöltött erőforrást. Ha az erőforrás még nincs betöltve, először meghívja a betöltő függvényt.

**Visszatérési érték:** A betöltött erőforrás

**Példa:**
```python
config = loader()  # Most fut le először: "Konfiguráció betöltése..."
print(config)  # {'setting': 'value'}

config2 = loader()  # Már nem fut le újra, gyorsítótárból jön
print(config2)  # {'setting': 'value'}
```

##### `is_loaded` property
Ellenőrzi, hogy az erőforrás betöltve van-e.

**Visszatérési érték:** `bool` - True, ha az erőforrás betöltve van, egyébként False

**Példa:**
```python
print(loader.is_loaded)  # False
config = loader()
print(loader.is_loaded)  # True
```

##### `reset() -> None`
Visszaállítja a betöltőt az alaphelyzetbe. Ez kiüríti a betöltött erőforrást, lehetővé téve az újratöltést.

Hasznos lehet tesztelés során vagy ha újra szeretnénk tölteni az erőforrást.

**Példa:**
```python
config = loader()  # Betölti az erőforrást
print(loader.is_loaded)  # True

loader.reset()  # Visszaállítás
print(loader.is_loaded)  # False

config = loader()  # Újra betölti az erőforrást
```

## Függvények

### `lazy_property[T](func: Callable[..., T]) -> property`

**Hely:** [`neural_ai.core.base.implementations.lazy_loader:88`](neural_ai/core/base/implementations/lazy_loader.py:88)

Dekorátor lustatöltésű property-k létrehozásához. Ez a dekorátor egy olyan property-t hoz létre, amelynek értéke csak az első hozzáféréskor számolódik ki, majd gyorsítótárba kerül. A későbbi hozzáférések már a gyorsítótárazott értéket adják vissza.

**Paraméterek:**
- `func`: A függvény, amely kiszámolja a property értékét

**Visszatérési érték:** Egy property objektum lustatöltéssel

**Példa:**
```python
from neural_ai.core.base.implementations.lazy_loader import lazy_property

class DataProcessor:
    def __init__(self, data):
        self._data = data
    
    @lazy_property
    def processed_data(self):
        # Ez a kód csak egyszer fut le
        print("Adatok feldolgozása...")
        return [x * 2 for x in self._data]

processor = DataProcessor([1, 2, 3])
# A processed_data még nincs kiszámolva

result = processor.processed_data  
# Most fut le először: "Adatok feldolgozása..."
print(result)  # [2, 4, 6]

result2 = processor.processed_data  
# Már gyorsítótárból jön, nem fut le újra
print(result2)  # [2, 4, 6]
```

## Használati területek

### 1. Konfigurációk betöltése

```python
from neural_ai.core.base.implementations.lazy_loader import LazyLoader
import yaml

def load_app_config():
    with open("config.yml", "r") as f:
        return yaml.safe_load(f)

config_loader = LazyLoader(load_app_config)

# A konfiguráció csak akkor töltődik be, amikor először használjuk
def get_setting(key):
    config = config_loader()
    return config.get(key)
```

### 2. Nagy adathalmazok betöltése

```python
from neural_ai.core.base.implementations.lazy_loader import LazyLoader
import pandas as pd

def load_large_dataset():
    print("Nagy adathalmaz betöltése...")
    return pd.read_csv("large_dataset.csv")

dataset_loader = LazyLoader(load_large_dataset)

# Az adathalmaz csak akkor töltődik be, amikor tényleg szükség van rá
if user_wants_analysis:
    data = dataset_loader()
    run_analysis(data)
```

### 3. Drága számítások

```python
from neural_ai.core.base.implementations.lazy_loader import lazy_property

class ExpensiveComputation:
    def __init__(self, input_data):
        self.input_data = input_data
    
    @lazy_property
    def result(self):
        print("Drága számítás futtatása...")
        # Valami drága számítás
        return sum(x**2 for x in self.input_data)

computation = ExpensiveComputation(range(1000))
# A számítás még nem futott le

# Csak akkor fut le, amikor először kérjük
result = computation.result
```

### 4. Adatbázis kapcsolatok

```python
from neural_ai.core.base.implementations.lazy_loader import LazyLoader
import sqlite3

def create_database_connection():
    print("Adatbázis kapcsolat létrehozása...")
    return sqlite3.connect("mydatabase.db")

db_loader = LazyLoader(create_database_connection)

# A kapcsolat csak akkor jön létre, amikor először használjuk
def query_database(query):
    conn = db_loader()
    return conn.execute(query).fetchall()
```

## Függőségek

- `threading` - Szálbiztosság érdekében (RLock használatával)
- `collections.abc.Callable` - Függvény típusokhoz
- `typing.TypeVar` - Generikus típusokhoz

## Jellemzők

- **Szálbiztosság:** Az összes művelet szálbiztos, többszálú környezetben is biztonságosan használható
- **Type Safety:** Generikus típusokkal erős típusosság
- **Egyszerű API:** Könnyen használható és érthető interfész
- **Reset támogatás:** Lehetőség van az erőforrások újratöltésére
- **Állapot követés:** Lehetőség van ellenőrizni, hogy egy erőforrás betöltődött-e már

## Előnyök

1. **Gyorsabb indítás:** Az alkalmazás gyorsabban indul, mert a drága erőforrások nem töltődnek be azonnal
2. **Hatékony memóriahasználat:** Csak azok az erőforrások töltődnek be, amikre tényleg szükség van
3. **Jobb teljesítmény:** A lustatöltésű property-k csak egyszer számolódnak ki
4. **Könnyű tesztelés:** A `reset()` metódussal egyszerűen tesztelhető a betöltési logika

## Kapcsolódó dokumentáció

- [Component Bundle](neural_ai/core/base/implementations/component_bundle.md) - Ahol a LazyLoader használatos
- [DI Container](neural_ai/core/base/implementations/di_container.md) - Lusta komponensek támogatása
- [Core Component Factory](neural_ai/core/base/factory.md) - Factory mintában való használat