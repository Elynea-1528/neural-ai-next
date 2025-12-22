# Lazy Loading (Lustatöltés)

## Áttekintés

A lustatöltés (lazy loading) egy optimalizációs technika, amely lehetővé teszi, hogy a drága erőforrások (például konfigurációk, adatbázis kapcsolatok, nagy adathalmazok) csak akkor töltődjenek be, amikor valóban szükség van rájuk. Ez jelentősen javítja az alkalmazás indítási idejét és a memóriahasználatot.

## Komponensek

### LazyLoader Osztály

A [`LazyLoader`](../../../neural_ai/core/base/lazy_loading.py) egy általános lustatöltő osztály, amely szálbiztos módon kezeli az erőforrások betöltését.

#### Főbb jellemzők

- **Szálbiztosság**: Többszálú környezetben is biztonságosan használható
- **Egyszeri betöltés**: Az erőforrás csak egyszer töltődik be
- **Gyorsítótárazás**: A betöltött érték gyorsítótárba kerül
- **Újratölthetőség**: Tesztelési célokra lehetőség van az újratöltésre

#### Metódusok

##### `__init__(loader_func: Callable[[], T]) -> None`

Inicializálja a lustatöltőt a megadott betöltő függvénnyel.

**Paraméterek:**
- `loader_func`: A függvény, amely betölti az erőforrást

##### `__call__() -> T`

Visszaadja a betöltött erőforrást. Ha még nincs betöltve, először meghívja a betöltő függvényt.

**Visszatérési érték:**
- A betöltött erőforrás

##### `is_loaded: bool` (property)

Ellenőrzi, hogy az erőforrás betöltve van-e.

**Visszatérési érték:**
- `True`, ha az erőforrás betöltve van, egyébként `False`

##### `reset() -> None`

Visszaállítja a betöltőt az alaphelyzetbe, lehetővé téve az újratöltést.

#### Használati példa

```python
from neural_ai.core.base.lazy_loading import LazyLoader

def load_expensive_resource() -> dict[str, str]:
    """Drága erőforrás betöltése."""
    print("Betöltés folyamatban...")
    return {"adat": "érték"}

# LazyLoader létrehozása
lazy_config = LazyLoader(load_expensive_resource)

# Az erőforrás még nincs betöltve
print(f"Betöltve: {lazy_config.is_loaded}")  # False

# Első hozzáférés - most töltődik be
config = lazy_config()
print(config)  # {"adat": "érték"}
print(f"Betöltve: {lazy_config.is_loaded}")  # True

# További hozzáférés - már gyorsítótárból jön
config2 = lazy_config()
print(config2)  # {"adat": "érték"}
```

### lazy_property Dekorátor

A [`lazy_property`](../../../neural_ai/core/base/lazy_loading.py) dekorátor lustatöltésű property-k létrehozásához.

#### Főbb jellemzők

- **Automatikus gyorsítótárazás**: Az érték csak egyszer számolódik ki
- **Property interfész**: Szabványos property-ként használható
- **Memóriaoptimalizálás**: Csak akkor számol, amikor szükség van rá

#### Használati példa

```python
from neural_ai.core.base.lazy_loading import lazy_property

class DataProcessor:
    """Adatfeldolgozó osztály."""
    
    def __init__(self, data: list[int]) -> None:
        self._data = data
    
    @lazy_property
    def processed_data(self) -> list[int]:
        """Feldolgozott adatok (lustatöltésű)."""
        print("Feldolgozás folyamatban...")
        return [x * 2 for x in self._data]

# Használat
processor = DataProcessor([1, 2, 3])

# A processed_data még nincs kiszámolva
result = processor.processed_data  # Most fut le először
print(result)  # [2, 4, 6]

# Már gyorsítótárból jön
result2 = processor.processed_data  # Nem fut le újra
print(result2)  # [2, 4, 6]
```

## Előnyök

1. **Gyors indítás**: Az alkalmazás gyorsabban indul, mert nem tölt be mindent előre
2. **Hatékony memóriahasználat**: Csak a ténylegesen használt erőforrások kerülnek betöltésre
3. **Szálbiztosság**: Többszálú környezetben is biztonságosan használható
4. **Egyszerű használat**: Tiszta és egyszerű API

## Használati területek

- **Konfigurációk betöltése**: Alkalmazás konfigurációk lustatöltése
- **Adatbázis kapcsolatok**: Adatbázis kapcsolatok késleltetett létrehozása
- **Nagy adathalmazok**: Nagy méretű adatok betöltése csak akkor, amikor szükséges
- **Drága számítások**: Komplex számítások eredményeinek gyorsítótárazása

## Implementáció részletei

### Szálbiztosság

A [`LazyLoader`](../../../neural_ai/core/base/lazy_loading.py) `RLock` objektumot használ a szálbiztosság érdekében. Ez biztosítja, hogy a betöltési művelet csak egyszer történjen meg, még akkor is, ha több szál egyidejűleg próbálja elérni az erőforrást.

### Típusbiztonság

A komponens teljes típusbiztonságot nyújt a Python type hints segítségével. A `TypeVar` használata lehetővé teszi, hogy a [`LazyLoader`](../../../neural_ai/core/base/lazy_loading.py) bármilyen típusú adattal működjön, miközben megtartja a típusbiztonságot.

### Hibakezelés

A betöltési folyamat során a rendszer ellenőrzi, hogy a betöltő függvény ne adjon vissza `None` értéket. Ha mégis, akkor `AssertionError` keletkezik, amely segít azonnal azonosítani a problémát.

## Kapcsolódó komponensek

- [`container.py`](container.md): Függőséginjektálás és életciklus kezelés
- [`singleton.py`](base.md): Egyke mintázat implementációja
- [`factory.py`](base_factory.md): Objektum létrehozási mintázat

## Tesztelés

A komponens teljes tesztlefedettséggel rendelkezik. A tesztek a [`tests/core/base/test_lazy_loading.py`](../../../tests/core/base/test_lazy_loading.py) fájlban találhatók, és a következőket ellenőrzik:

- Alapvető lustatöltési funkcionalitás
- Szálbiztosság
- Property lustatöltés
- Újratöltési képesség
- Típusbiztonság

## Verziótörténet

- **1.0.0**: Kezdeti implementáció
  - [`LazyLoader`](../../../neural_ai/core/base/lazy_loading.py) osztály
  - [`lazy_property`](../../../neural_ai/core/base/lazy_loading.py) dekorátor
  - Szálbiztos implementáció
  - Teljes típusbiztonság