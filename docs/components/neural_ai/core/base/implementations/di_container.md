# DIContainer Implementáció

A `DIContainer` osztály egyszerű dependency injection konténert valósít meg, amely kezeli a komponensek közötti függőségeket és biztosítja azok megfelelő inicializálását.

## Osztályok

### LazyComponent[T]

Lusta betöltésű komponensek wrapper osztálya.

Ez az osztály biztosítja a komponensek lusta (lazy) betöltését, ami azt jelenti, hogy a komponens csak akkor jön létre, amikor először használják.

#### Konstruktor

- `__init__(factory_func: Callable[[], T]) -> None`: Inicializálja a lusta komponenst a factory függvénnyel.

#### Metódusok

- `get() -> T`: Lekéri a komponens példányt (lusta betöltéssel).
- `is_loaded -> bool`: Ellenőrzi, hogy a komponens betöltődött-e már.

### DIContainer

Egyszerű dependency injection konténer.

#### Konstruktor

- `__init__() -> None`: Inicializálja a konténert üres szótárakkal.

#### Metódusok

- `register_instance(interface: InterfaceT, instance: InterfaceT) -> None`: Példány regisztrálása az interfészhez.
- `register_factory(interface: InterfaceT, factory: Callable[[], InterfaceT]) -> None`: Factory függvény regisztrálása az interfészhez.
- `resolve(interface: InterfaceT) -> InterfaceT | None`: Függőség feloldása az interfész alapján.
- `register_lazy(component_name: str, factory_func: Callable[[], T]) -> None`: Lusta betöltésű komponens regisztrálása.
- `get(component_name: str) -> object`: Komponens példány lekérése név alapján.
- `get_lazy_components() -> dict[str, bool]`: Lekéri az összes lazy komponens állapotát.
- `preload_components(component_names: list[str]) -> None`: Előre betölti a megadott komponenseket.
- `clear() -> None`: Törli a konténer tartalmát.
- `_verify_singleton(instance: object, component_name: str) -> None`: Ellenőrzi, hogy az instance követi-e a singleton mintát. (Frissítve, hogy tartalmazza a megfelelő ellenőrzéseket és kommentált warnings.warn hívásokat.)
- `_enforce_singleton(component_name: str, instance: object) -> None`: Kikényszeríti a singleton mintát duplikált regisztráció megakadályozásával.
- `register(component_name: str, instance: object) -> None`: Komponens példány regisztrálása név alapján.
- `get_memory_usage() -> dict[str, int | dict[str, int]]`: Lekéri a memória használati statisztikákat.

## Használat

A konténer példányosítása és használat példája:

```python
container = DIContainer()
container.register_instance(SomeInterface, some_instance)
resolved = container.resolve(SomeInterface)
```

## Architektúra Megjegyzések

- Dependency Injection: Konkrét osztályokat TILOS importálni, csak interfészeket használj Factory-kon keresztül.
- Körkörös hivatkozások: TYPE_CHECKING blokk használata szükséges.
- Singleton ellenőrzés: A `_verify_singleton` metódus tartalmazza a szükséges ellenőrzéseket, a zajgeneráló warningok kikommentálva.