# Lazy Loading Modul

## Áttekintés

A `lazy_loading` modul lustatöltés (lazy loading) mechanizmust valósít meg, amely lehetővé teszi, hogy a drága erőforrások csak akkor töltődjenek be, amikor valóban szükség van rájuk. Ez jelentősen javítja az alkalmazás indítási idejét és a memóriahasználatot.

## Tartalomjegyzék

- [LazyLoader Osztály](#lazyloader-osztály)
- [lazy_property Dekorátor](#lazy_property-dekorátor)
- [Használati Példák](#használati-példák)
- [Teljesítményoptimalizálás](#teljesítményoptimalizálás)
- [Szálbiztonság](#szálbiztonság)

## LazyLoader Osztály

A `LazyLoader` egy általános célú lustatöltő osztály, amely drága erőforrások késleltetett betöltését valósítja meg.

### Inicializálás

```python
from neural_ai.core.base.lazy_loading import LazyLoader

def load_expensive_resource() -> str:
    # Drága művelet
    return "betöltött_érték"

loader = LazyLoader(load_expensive_resource)
```

### Metódusok

#### `__init__(loader_func: Callable[[], T]) -> None`

Inicializálja a lustatöltőt egy betöltő függvénnyel.

**Paraméterek:**
- `loader_func`: A függvény, amely betölti az erőforrást. Ennek a függvénynek vissza kell térnie a betöltött erőforrással.

#### `__call__() -> T`

Visszaadja a betöltött erőforrást. Ha az erőforrás még nincs betöltve, először meghívja a betöltő függvényt.

**Visszatérési érték:**
- A betöltött erőforrás.

#### `is_loaded: bool` (property)

Ellenőrzi, hogy az erőforrás betöltve van-e.

**Visszatérési érték:**
- `True`, ha az erőforrás betöltve van, egyébként `False`.

#### `reset() -> None`

Visszaállítja a betöltőt az alaphelyzetbe. Ez kiüríti a betöltött erőforrást, lehetővé téve az újratöltést.

### Példa

```python
from neural_ai.core.base.lazy_loading import LazyLoader

class DatabaseConnection:
    def __init__(self):
        self._connection_loader = LazyLoader(self._create_connection)
    
    def _create_connection(self) -> Connection:
        # Drága adatbázis kapcsolat létrehozása
        return create_db_connection()
    
    def get_connection(self) -> Connection:
        return self._connection_loader()

# Használat
db = DatabaseConnection()
# A kapcsolat még nincs létrehozva

connection = db.get_connection()  # Most jön létre a kapcsolat
# További hívások már a gyorsítótárazott kapcsolatot adják vissza
```

## lazy_property Dekorátor

A `lazy_property` dekorátor egy olyan property-t hoz létre, amelynek értéke csak az első hozzáféréskor számolódik ki, majd gyorsítótárba kerül.

### Szintaxis

```python
from neural_ai.core.base.lazy_loading import lazy_property

class MyClass:
    @lazy_property
    def expensive_value(self) -> str:
        # Drága számítás
        return "számított_érték"
```

### Működés

1. **Első hozzáférés:** A property függvénytörzse lefut, az eredményt elmenti egy `_lazy_<property_name>` attribútumba.
2. **További hozzáférések:** A gyorsítótárazott értéket adja vissza, a függvénytörzs nem fut le újra.

### Példa

```python
class DataProcessor:
    def __init__(self, data: list[int]):
        self.data = data
    
    @lazy_property
    def processed_data(self) -> list[int]:
        print("Feldolgozás folyamatban...")
        return [x * 2 for x in self.data]

processor = DataProcessor([1, 2, 3, 4, 5])

# Első hozzáférés - a feldolgozás megtörténik
result1 = processor.processed_data
# Kimenet: "Feldolgozás folyamatban..."

# Második hozzáférés - már a gyorsítótárból jön
result2 = processor.processed_data
# Nincs kimenet, a függvény nem fut le újra

assert result1 == result2 == [2, 4, 6, 8, 10]
```

## Használati Példák

### 1. Konfiguráció Betöltése

```python
from neural_ai.core.base.lazy_loading import LazyLoader, lazy_property
import yaml

class AppConfig:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self._config_loader = LazyLoader(self._load_config)
    
    def _load_config(self) -> dict:
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def get_config(self) -> dict:
        return self._config_loader()

# Használat
config = AppConfig('config.yaml')
# A konfiguráció még nincs betöltve

app_config = config.get_config()  # Most töltődik be
```

### 2. Nagy Adathalmaz Feldolgozása

```python
class DataAnalyzer:
    def __init__(self, raw_data: list[float]):
        self.raw_data = raw_data
    
    @lazy_property
    def statistics(self) -> dict[str, float]:
        return {
            'mean': sum(self.raw_data) / len(self.raw_data),
            'min': min(self.raw_data),
            'max': max(self.raw_data),
            'std_dev': self._calculate_std_dev()
        }
    
    def _calculate_std_dev(self) -> float:
        # Komplex számítás
        mean = sum(self.raw_data) / len(self.raw_data)
        variance = sum((x - mean) ** 2 for x in self.raw_data) / len(self.raw_data)
        return variance ** 0.5

# Használat
analyzer = DataAnalyzer([1.2, 3.4, 5.6, 7.8, 9.0])
stats = analyzer.statistics  # A statisztika kiszámolása
```

### 3. Integráció LazyLoader és lazy_property

```python
class DataService:
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    @lazy_property
    def data_loader(self) -> LazyLoader[list[dict]]:
        def load_from_database() -> list[dict]:
            # Adatbázisból történő betöltés
            return query_database(self.db_path)
        
        return LazyLoader(load_from_database)
    
    def get_data(self) -> list[dict]:
        return self.data_loader()

# Használat
service = DataService('database.db')
data = service.get_data()  # Az adatok betöltése
```

## Teljesítményoptimalizálás

### Előnyök

1. **Gyorsabb indítás:** Az alkalmazás gyorsabban indul, mert nem tölt be mindent előre.
2. **Kisebb memóriahasználat:** Csak a ténylegesen használt erőforrások kerülnek betöltésre.
3. **Hatékony erőforrás-kezelés:** Az erőforrások csak akkor kerülnek felhasználásra, amikor szükség van rájuk.

### Best Practices

- Használd lustatöltést nagy erőforrásigényű műveletekhez (adatbázis kapcsolatok, fájlbetöltés, hálózati hívások).
- Kerüld a túlzott használatát egyszerű, gyors műveleteknél, mert a lustatöltésnek is van overhead-je.
- A `LazyLoader`-t használd, ha több helyről szeretnéd elérni ugyanazt az erőforrást.
- A `lazy_property`-t használd osztályon belüli egyszeri számításokhoz.

## Szálbiztonság

A `LazyLoader` osztály szálbiztos, így többszálú környezetben is biztonságosan használható. A belső zárolás (`RLock`) biztosítja, hogy a betöltő függvény csak egyszer fusson le, még akkor is, ha több szál egyidejűleg próbálja elérni az erőforrást.

### Példa szálbiztonságra

```python
import threading
from neural_ai.core.base.lazy_loading import LazyLoader

def expensive_operation() -> str:
    import time
    time.sleep(0.1)
    return "loaded_value"

loader = LazyLoader(expensive_operation)
results = []

def worker():
    result = loader()
    results.append(result)

threads = [threading.Thread(target=worker) for _ in range(10)]
for t in threads:
    t.start()
for t in threads:
    t.join()

# Minden szál ugyanazt az értéket kapta, és a betöltés csak egyszer történt meg
assert all(r == "loaded_value" for r in results)
```

## Hibakezelés

### None értékek kezelése

A `LazyLoader` ellenőrzi, hogy a betöltő függvény nem adott-e vissza `None` értéket. Ha igen, `AssertionError`-t dob.

```python
def bad_loader() -> None:
    return None

loader = LazyLoader(bad_loader)
try:
    value = loader()  # AssertionError: A betöltő függvény None értéket adott vissza
except AssertionError as e:
    print(f"Hiba: {e}")
```

### Kivételek továbbadása

Ha a betöltő függvény kivételt dob, az továbbadódik a hívónak:

```python
def failing_loader() -> str:
    raise ValueError("Nem sikerült betölteni az erőforrást")

loader = LazyLoader(failing_loader)
try:
    value = loader()  # ValueError-t dob
except ValueError as e:
    print(f"Betöltési hiba: {e}")
```

## Összehasonlítás más megoldásokkal

### LazyLoader vs lazy_property

| Szempont | LazyLoader | lazy_property |
|----------|------------|---------------|
| Használat | Független objektum | Osztály dekorátor |
| Többszörös hozzáférés | Igen, ugyanazt az erőforrást | Igen, ugyanazt a property-t |
| Újratöltés | `reset()` metódussal | Nincs beépített támogatás |
| Több erőforrás | Több LazyLoader példány | Több lazy_property |

### Lazy Loading vs Eager Loading

| Szempont | Lazy Loading | Eager Loading |
|----------|--------------|---------------|
| Indítási idő | Gyors | Lassú |
| Memóriahasználat | Alacsony | Magas |
| Első hozzáférés | Lassú | Gyors |
| Későbbi hozzáférések | Gyors | Gyors |
| Erőforrás-kezelés | Hatékony | Pazaroló |

## Kapcsolódó dokumentáció

- [Core Components](core_components.md) - Alap komponensek áttekintése
- [Factory Pattern](factory.md) - Objektum létrehozási minta
- [Dependency Injection](../interfaces.md) - Függőség injektálás