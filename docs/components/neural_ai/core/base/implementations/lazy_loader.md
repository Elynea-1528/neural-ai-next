# Lazy Loader Implementáció

## Áttekintés

Lustatöltés (lazy loading) segédeszközök.

Ez a modul a lustatöltés mechanizmust valósítja meg, amely lehetővé teszi, hogy a drága erőforrások csak akkor töltődjenek be, amikor valóban szükség van rájuk. Ez jelentősen javítja az alkalmazás indítási idejét és a memóriahasználatot.

## Exportált Osztályok és Függvények

- `LazyLoader[T]`: Drága erőforrások lustatöltője
- `lazy_property`: Dekorátor lustatöltésű property-k létrehozásához

## Osztályok

### `LazyLoader[T]`

Drága erőforrások lustatöltője.

Ez az osztály lehetővé teszi, hogy a drága erőforrások (pl. konfigurációk, adatbázis kapcsolatok, nagy adathalmazok) csak akkor töltődjenek be, amikor valóban szükség van rájuk.

A lustatöltés szálbiztos, így többszálú környezetben is biztonságosan használható.

#### Metódusok

##### `__init__(loader_func)`

Inicializálja a lustatöltőt.

**Paraméterek:**
- `loader_func`: A függvény, amely betölti az erőforrást. Ennek a függvénynek vissza kell térnie a betöltött erőforrással.

##### `_load()`

Betölti az erőforrást, ha még nincs betöltve.

**Visszatérési érték:**
- `T`: A betöltött erőforrás.

**Megjegyzés:**
Ez egy belső metódus, általában nem kell közvetlenül használni. Ehelyett használd a __call__ metódust.

##### `__call__()`

Visszaadja a betöltött erőforrást.

Ha az erőforrás még nincs betöltve, először meghívja a betöltő függvényt.

**Visszatérési érték:**
- `T`: A betöltött erőforrás.

##### `is_loaded` property

Ellenőrzi, hogy az erőforrás betöltve van-e.

**Visszatérési érték:**
- `bool`: True, ha az erőforrás betöltve van, egyébként False.

##### `reset()`

Visszaállítja a betöltőt az alaphelyzetbe.

Ez kiüríti a betöltött erőforrást, lehetővé téve az újratöltést. Hasznos lehet tesztelés során vagy ha újra szeretnénk tölteni az erőforrást.

## Függvények

### `lazy_property(func)`

Dekorátor lustatöltésű property-k létrehozásához.

Ez a dekorátor egy olyan property-t hoz létre, amelynek értéke csak az első hozzáféréskor számolódik ki, majd gyorsítótárba kerül. A későbbi hozzáférések már a gyorsítótárazott értéket adják vissza.

**Paraméterek:**
- `func`: A függvény, amely kiszámolja a property értékét.

**Visszatérési érték:**
- `property`: Egy property objektum lustatöltéssel.

## Használati Példák

### Alap LazyLoader használat

```python
from neural_ai.core.base.implementations.lazy_loader import LazyLoader
import time

def load_expensive_data():
    """Drága adatok betöltését szimulálja."""
    print("Adatok betöltése...")
    time.sleep(2)  # Szimulált drága művelet
    return [1, 2, 3, 4, 5]

# Lusta betöltő létrehozása
data_loader = LazyLoader(load_expensive_data)

print("Lusta betöltő létrejött")
print(f"Betöltve van? {data_loader.is_loaded}")  # False

# Most történik meg a tényleges betöltés
data = data_loader()
print(f"Adatok: {data}")  # [1, 2, 3, 4, 5]
print(f"Betöltve van? {data_loader.is_loaded}")  # True

# További hívások már a gyorsítótárból jönnek
data2 = data_loader()
print(f"Ugyanaz az adat: {data is data2}")  # True
```

### Lazy property használata

```python
from neural_ai.core.base.implementations.lazy_loader import lazy_property

class DataProcessor:
    def __init__(self, data):
        self._data = data
    
    @lazy_property
    def processed_data(self):
        """A feldolgozás csak egyszer történik meg."""
        print("Adatok feldolgozása...")
        return [x * 2 for x in self._data]

# Használat
processor = DataProcessor([1, 2, 3])

# A processed_data még nincs kiszámolva
print("Processor létrejött")

# Most fut le először a feldolgozás
result = processor.processed_data  # Kiírja: "Adatok feldolgozása..."
print(f"Eredmény: {result}")  # [2, 4, 6]

# Már gyorsítótárból jön
result2 = processor.processed_data  # Nem ír ki semmit
print(f"Ugyanaz az eredmény: {result is result2}")  # True
```

### Lusta betöltés resetelése

```python
from neural_ai.core.base.implementations.lazy_loader import LazyLoader

counter = 0

def load_with_counter():
    global counter
    counter += 1
    return f"Adat {counter}"

loader = LazyLoader(load_with_counter)

# Első betöltés
data1 = loader()
print(data1)  # "Adat 1"

# Reset
loader.reset()
print(f"Reset után betöltve: {loader.is_loaded}")  # False

# Újra betöltés
data2 = loader()
print(data2)  # "Adat 2"
```

### Többszálú környezetben

```python
from neural_ai.core.base.implementations.lazy_loader import LazyLoader
import threading
import time

def load_shared_resource():
    print(f"Betöltés a {threading.current_thread().name} szálban")
    time.sleep(1)
    return {"id": 1, "data": "shared"}

shared_loader = LazyLoader(load_shared_resource)

def worker():
    data = shared_loader()
    print(f"{threading.current_thread().name} kapta: {data}")

# Több szál hívja meg egyszerre
threads = []
for i in range(3):
    t = threading.Thread(target=worker, name=f"Worker-{i}")
    threads.append(t)
    t.start()

for t in threads:
    t.join()

# A betöltés csak egyszer fog megtörténni, a többi szál várni fog
```

## Előnyök

1. **Gyors indítás:** Az alkalmazás gyorsabban indul, mert a drága erőforrások csak akkor töltődnek be, amikor szükség van rájuk.

2. **Memóriatakarékosság:** Csak azokat az erőforrásokat töltjük be, amelyeket ténylegesen használunk.

3. **Szálbiztosság:** A RLock használata biztosítja, hogy többszálú környezetben is biztonságosan működik.

4. **Tesztelhetőség:** A `reset()` metódus lehetővé teszi az erőforrások újratöltését tesztelés során.

## Kapcsolódó Dokumentáció

- [Component Bundle](component_bundle.md)
- [DI Container](di_container.md)
- [Singleton](singleton.md)
- [Base Modul](../__init__.md)