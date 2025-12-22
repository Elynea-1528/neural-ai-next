# DIContainer & LazyComponent

## Áttekintés

A `container.py` fájl egy fejlett Dependency Injection (DI) konténer implementációt tartalmaz, amely támogatja a lusta betöltést (lazy loading), szálbiztosságot és singleton mintát.

## Osztályok

### LazyComponent

Lusta betöltésű komponensek wrapper osztálya, amely biztosítja, hogy a komponensek csak akkor jöjjenek létre, amikor először használják őket.

#### Metódusok

- **`__init__(factory_func: Callable[[], T]) -> None`**
  - Inicializálja a lusta komponenst a megadott factory függvénnyel.

- **`get() -> T`**
  - Lekéri a komponens példányt (lusta betöltéssel). Ha még nincs betöltve, létrehozza a példányt.

- **`is_loaded: bool`** (property)
  - Ellenőrzi, hogy a komponens betöltődött-e már.

### DIContainer

Egyszerű dependency injection konténer, amely kezeli a komponensek közötti függőségeket és biztosítja azok megfelelő inicializálását.

#### Főbb jellemzők

- **Példány regisztráció:** Előre létrehozott példányok regisztrálása
- **Factory regisztráció:** Dinamikus példányosítás factory függvényekkel
- **Lusta betöltés:** Komponensek késleltetett betöltése
- **Singleton minta:** Automatikus singleton ellenőrzés és érvényesítés
- **Memóriakezelés:** Memóriahasználat nyomon követése

#### Metódusok

##### Regisztráció

- **`register_instance(interface: InterfaceT, instance: InterfaceT) -> None`**
  - Példány regisztrálása a konténerben.

- **`register_factory(interface: InterfaceT, factory: Callable[[], InterfaceT]) -> None`**
  - Factory függvény regisztrálása a konténerben.

- **`register_lazy(component_name: str, factory_func: Callable[[], T]) -> None`**
  - Lusta betöltésű komponens regisztrálása.
  - `ValueError`-t dob, ha a név érvénytelen vagy a factory nem hívható.

- **`register(component_name: str, instance: object) -> None`**
  - Komponens példány regisztrálása név alapján.
  - `ValueError`-t dob, ha a név érvénytelen vagy a példány `None`.
  - `SingletonViolationError`-t dob, ha a singleton minta megsértésre kerül.

##### Lekérdezés

- **`resolve(interface: InterfaceT) -> InterfaceT | None`**
  - Függőség feloldása interfész alapján.

- **`get(component_name: str) -> object`**
  - Komponens példány lekérése (lusta betöltés támogatással).
  - `ComponentNotFoundError`-t dob, ha a komponens nem található.

##### Egyéb

- **`get_lazy_components() -> dict[str, bool]`**
  - Visszaadja az összes lusta komponens állapotát.

- **`preload_components(component_names: list[str]) -> None`**
  - Előre betölti a megadott komponenseket.

- **`clear() -> None`**
  - Kiüríti a konténert.

- **`get_memory_usage() -> dict[str, int | dict[str, int]]`**
  - Visszaadja a memóriahasználati statisztikákat.

#### Singleton Ellenőrzés

A konténer automatikusan ellenőrzi a singleton mintát:

- **`_verify_singleton(instance: object, component_name: str) -> None`**
  - Ellenőrzi, hogy a példány rendelkezik-e `_initialized` flaggel.
  - Ellenőrzi, hogy az osztály rendelkezik-e `_instance` osztályváltozóval.
  - Figyelmeztetést (`UserWarning`) ad, ha a singleton minta nincs megfelelően implementálva.

- **`_enforce_singleton(component_name: str, instance: object) -> None`**
  - Kikényszeríti a singleton mintát azáltal, hogy megakadályozza a duplikált regisztrációt.
  - `SingletonViolationError`-t dob, ha a minta megsértésre kerül.

## Használati Példák

### Alap regisztráció és feloldás

```python
from neural_ai.core.base.container import DIContainer

# Konténer létrehozása
container = DIContainer()

# Példány regisztrálása
container.register_instance(str, "Hello World")

# Factory regisztrálása
container.register_factory(int, lambda: 42)

# Feloldás
message = container.resolve(str)  # "Hello World"
number = container.resolve(int)   # 42
```

### Lusta betöltés

```python
from neural_ai.core.base.container import DIContainer

container = DIContainer()

# Nehézkes inicializálású komponens regisztrálása
def create_heavy_component() -> HeavyComponent:
    print("Creating heavy component...")
    return HeavyComponent()

container.register_lazy("heavy", create_heavy_component)

# A komponens még nem jött létre
print(container.get_lazy_components())  # {'heavy': False}

# Most jön létre
heavy = container.get("heavy")  # "Creating heavy component..."

# Már betöltődött
print(container.get_lazy_components())  # {}
```

### Komponens regisztráció névvel

```python
from neural_ai.core.base.container import DIContainer

container = DIContainer()

# Komponens regisztrálása névvel
service = MyService()
container.register("my_service", service)

# Lekérés név alapján
retrieved_service = container.get("my_service")
```

### Memóriahasználat nyomon követése

```python
from neural_ai.core.base.container import DIContainer

container = DIContainer()

# Több komponens regisztrálása
container.register_instance("str1", "test_string_1")
container.register_instance("int1", 42)
container.register_instance("list1", [1, 2, 3])

# Memóriahasználat lekérése
stats = container.get_memory_usage()
print(f"Total instances: {stats['total_instances']}")
print(f"Instance sizes: {stats['instance_sizes']}")
```

## Függőségi Injektálás

A konténer támogatja a függőségi injektálást, ami lehetővé teszi a komponensek lazítását és a konfiguráció egyszerűbb kezelését.

### Függőségi Gráf

```
DIContainer
├── Instances (előre létrehozott példányok)
├── Factories (dinamikus létrehozás)
└── Lazy Components (lusta betöltésű komponensek)
    └── Betöltés után áthelyezés az Instances-be
```

## Hibakezelés

A konténer a következő kivételeket dobhatja:

- **`ComponentNotFoundError`**: A komponens nem található a konténerben.
- **`SingletonViolationError`**: A singleton minta megsértésre került.
- **`ValueError`**: Érvénytelen paraméter (üres név, None példány, nem hívható factory).

## Teljesítményoptimalizálás

### Lusta betöltés előnyei

- **Gyorsabb indulás:** A nehézkes komponensek csak akkor jönnek létre, amikor szükség van rájuk.
- **Erőforrás-megtakarítás:** Nem használt komponensek soha nem jönnek létre.
- **Memóriahatékonyság:** Csak a ténylegesen használt komponensek foglalnak helyet a memóriában.

### Szálbiztonság

A `LazyComponent` osztály szálbiztos, ami azt jelenti, hogy többszálú környezetben is biztonságosan használható. A `get()` metódus `RLock`-ot használ a szinkronizációhoz.

## Tesztelés

A konténer teljes tesztlefedettséggel rendelkezik. A tesztek a `tests/core/base/test_container.py` fájlban találhatók.

### Tesztelt területek

- Lusta betöltés működése
- Szálbiztonság
- Singleton ellenőrzés
- Hibakezelés
- Memóriakezelés
- Factory és instance regisztráció

## Kapcsolódó Dokumentáció

- [Core Dependencies](../../../development/core_dependencies.md)
- [Base Exceptions](exceptions.md)
- [Singleton Pattern](singleton.md)