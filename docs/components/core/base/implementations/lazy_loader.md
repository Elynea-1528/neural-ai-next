# LazyLoader és lazy_property

## Áttekintés

A `LazyLoader` egy lustatöltő (lazy loading) segédeszköz, amely lehetővé teszi, hogy a drága erőforrások csak akkor töltődjenek be, amikor valóban szükség van rájuk. A `lazy_property` dekorátor pedig property-k lusta betöltését teszi lehetővé.

## LazyLoader

### Leírás

A `LazyLoader[T]` egy generikus osztály, amely drága erőforrások lusta betöltését valósítja meg. Ez jelentősen javítja az alkalmazás indítási idejét és a memóriahasználatot.

### Jellemzők

- **Lusta betöltés**: Az erőforrás csak az első hozzáféréskor töltődik be.
- **Gyorsítótár**: A betöltött erőforrás gyorsítótárba kerül, a későbbi hozzáféréskor már onnan jön.
- **Szálbiztonság**: RLock-ot használ, így többszálú környezetben is biztonságosan használható.
- **Resetelhetőség**: Az erőforrás újratölthető a `reset()` metódussal.

### Metódusok

- `__init__(loader_func: Callable[[], T]) -> None`: Inicializálja a lustatöltőt a betöltő függvénnyel.
- `__call__() -> T`: Visszaadja a betöltött erőforrást. Ha még nincs betöltve, meghívja a betöltő függvényt.
- `is_loaded: bool`: Property, amely ellenőrzi, hogy az erőforrás betöltve van-e.
- `reset() -> None`: Visszaállítja a betöltőt az alaphelyzetbe, lehetővé téve az újratöltést.

### Példa

```python
from neural_ai.core.base.implementations.lazy_loader import LazyLoader
import time

# Drága erőforrás létrehozása
def load_expensive_data() -> list[int]:
    print("Loading expensive data...")
    time.sleep(2)  # Szimuláljuk a drága műveletet
    return [1, 2, 3, 4, 5]

# Lusta betöltő létrehozása
data_loader = LazyLoader(load_expensive_data)

# Még nem töltődött be
print(data_loader.is_loaded)  # False

# Első hozzáférés - most töltődik be (2 másodperc)
data = data_loader()
print(data)  # [1, 2, 3, 4, 5]
print(data_loader.is_loaded)  # True

# További hozzáférés - már gyorsítótárból jön (azonnal)
data2 = data_loader()
print(data2)  # [1, 2, 3, 4, 5]
assert data is data2  # Ugyanaz az objektum

# Resetelés
data_loader.reset()
print(data_loader.is_loaded)  # False

# Újratöltés
data3 = data_loader()  # Ismét 2 másodperc
```

### Szálbiztonság

A `LazyLoader` szálbiztos, ami azt jelenti, hogy több szál egyidejű hozzáférésénél is csak egyszer hívódik meg a betöltő függvény:

```python
import threading
from neural_ai.core.base.implementations.lazy_loader import LazyLoader

results = []
loader = LazyLoader(lambda: f"loaded_in_{threading.current_thread().name}")

def access_loader():
    results.append(loader())

threads = []
for i in range(5):
    t = threading.Thread(target=access_loader)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

# Minden szál ugyanazt az értéket kapta
assert all(r == results[0] for r in results)
```

## lazy_property dekorátor

### Leírás

A `lazy_property` dekorátor egy olyan property-t hoz létre, amelynek értéke csak az első hozzáféréskor számolódik ki, majd gyorsítótárba kerül.

### Jellemzők

- **Egyszer számol**: A property értéke csak egyszer számolódik ki.
- **Automatikus gyorsítótár**: A kiszámolt érték automatikusan gyorsítótárba kerül.
- **Példányszintű**: Minden példánynak saját gyorsítótára van.

### Példa

```python
from neural_ai.core.base.implementations.lazy_loader import lazy_property

class DataProcessor:
    def __init__(self, data: list[int]):
        self._data = data
        self.computation_count = 0

    @lazy_property
    def processed_data(self) -> list[int]:
        """Drága számítás - csak egyszer fut le."""
        print("Computing processed data...")
        self.computation_count += 1
        return [x * 2 for x in self._data]

# Használat
processor = DataProcessor([1, 2, 3])

print(processor.computation_count)  # 0

# Első hozzáférés - kiszámol
result1 = processor.processed_data  # "Computing processed data..."
print(result1)  # [2, 4, 6]
print(processor.computation_count)  # 1

# További hozzáférés - már gyorsítótárból
result2 = processor.processed_data  # Nincs üzenet
print(result2)  # [2, 4, 6]
print(processor.computation_count)  # 1 (nem nőtt)

assert result1 is result2  # Ugyanaz az objektum
```

### Különböző példányok

```python
class DataProcessor:
    def __init__(self, name: str):
        self.name = name

    @lazy_property
    def expensive_value(self) -> str:
        return f"{self.name}_computed"

# Különböző példányoknak külön a gyorsítótár
proc1 = DataProcessor("A")
proc2 = DataProcessor("B")

val1 = proc1.expensive_value  # "A_computed"
val2 = proc2.expensive_value  # "B_computed"

assert val1 != val2
```

### Komplex objektumok

```python
class DataProcessor:
    def __init__(self, data: list[int]):
        self.data = data

    @lazy_property
    def statistics(self) -> dict[str, float]:
        """Komplex objektum gyorsítótárazása."""
        return {
            "sum": sum(self.data),
            "avg": sum(self.data) / len(self.data),
            "min": min(self.data),
            "max": max(self.data)
        }

processor = DataProcessor([10, 20, 30, 40, 50])
stats = processor.statistics

print(stats)
# {'sum': 150, 'avg': 30.0, 'min': 10, 'max': 50}
```

## Használati területek

### Konfiguráció betöltés

```python
from neural_ai.core.base.implementations.lazy_loader import LazyLoader
import yaml

def load_config() -> dict:
    with open("config.yml", "r") as f:
        return yaml.safe_load(f)

config_loader = LazyLoader(load_config)

# A konfiguráció csak akkor töltődik be, ha valóban szükség van rá
def get_setting(key: str):
    config = config_loader()
    return config.get(key)
```

### Adatbázis kapcsolat

```python
from sqlalchemy import create_engine
from neural_ai.core.base.implementations.lazy_loader import LazyLoader

def create_db_engine():
    print("Connecting to database...")
    return create_engine("sqlite:///mydb.db")

db_loader = LazyLoader(create_db_engine)

# A kapcsolat csak az első lekérdezéskor jön létre
def query_data():
    engine = db_loader()
    with engine.connect() as conn:
        return conn.execute("SELECT * FROM users")
```

### Nagy adathalmazok betöltése

```python
import pandas as pd
from neural_ai.core.base.implementations.lazy_loader import LazyLoader

def load_large_dataset() -> pd.DataFrame:
    print("Loading large dataset...")
    return pd.read_parquet("large_data.parquet")

dataset_loader = LazyLoader(load_large_dataset)

# Az adatok csak akkor töltődnek be, ha valóban szükség van rájuk
def process_data():
    df = dataset_loader()
    return df.groupby("category").mean()
```

## Tesztelés

A modul tesztelése a `tests/core/base/implementations/test_lazy_loader.py` fájlban található. A tesztek 100% statement coverage-t érnek el, és minden metódust, property-t és szálbiztonságot is tesztelnek.

### Teszt példa

```python
from neural_ai.core.base.implementations.lazy_loader import LazyLoader, lazy_property
from unittest.mock import MagicMock

def test_lazy_loading():
    mock_value = MagicMock()
    loader_func = MagicMock(return_value=mock_value)
    loader = LazyLoader(loader_func)
    
    # Még nem hívódott meg
    assert not loader.is_loaded
    
    # Első hozzáférés
    result = loader()
    assert result is mock_value
    assert loader.is_loaded
    loader_func.assert_called_once()
    
    # További hozzáférés
    result2 = loader()
    assert result2 is mock_value
    loader_func.assert_called_once()  # Még mindig csak egyszer
```

## Teljesítmény előnyök

A lusta betöltés főbb előnyei:

1. **Gyorsabb indítás**: Az alkalmazás gyorsabban indul, mert nem tölt be mindent azonnal.
2. **Kisebb memóriahasználat**: Csak a ténylegesen használt erőforrások töltődnek be.
3. **Jobb felhasználói élmény**: Az alkalmazás válaszkészsége javul.
4. **Erőforrás takarékosság**: Csak a szükséges erőforrásokat használja.

## Korlátozások

- **Nem megfelelő mindenhol**: Olyan erőforrásoknál, amelyekre azonnal szükség van, nem érdemes lusta betöltést használni.
- **Hiba kezelés**: A betöltő függvény hibát dobhat, ezt kezelni kell.
- **Élettartam**: A lusta betöltő élettartama alatt a betöltött erőforrás a memóriában marad.