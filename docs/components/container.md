# Dependency Injection Konténer

## Áttekintés

A `DIContainer` egy egyszerű, hatékony függőséginjektáló konténer implementáció, amely támogatja a lusta betöltést, singleton mintát és típusbiztos függőség feloldást.

## Főbb Jellemzők

### 1. Lusta Betöltés (Lazy Loading)

A lusta betöltés lehetővé teszi, hogy a komponensek csak akkor jöjjenek létre, amikor először használják őket:

```python
from neural_ai.core.base.container import DIContainer

container = DIContainer()

# Lusta komponens regisztrálása
container.register_lazy("my_service", lambda: MyService())

# Komponens csak itt jön létre
service = container.get("my_service")
```

### 2. Singleton Minta

A konténer automatikusan ellenőrzi és betartatja a singleton mintát:

```python
class MySingleton:
    def __init__(self):
        self._initialized = True

# Regisztráció
container.register("singleton", MySingleton())

# Későbbi hozzáférés ugyanahhoz a példányhoz
instance1 = container.get("singleton")
instance2 = container.get("singleton")
assert instance1 is instance2  # True
```

### 3. Factory Támogatás

Dinamikus példányosítás factory függvényekkel:

```python
def create_database_connection():
    return DatabaseConnection(config)

container.register_factory(DatabaseInterface, create_database_connection)
db = container.resolve(DatabaseInterface)
```

### 4. Típusbiztos Függőség Feloldás

```python
from typing import Protocol

class LoggerInterface(Protocol):
    def log(self, message: str) -> None: ...

class FileLogger:
    def log(self, message: str) -> None:
        with open("app.log", "a") as f:
            f.write(message)

# Regisztráció interfész alapján
container.register_instance(LoggerInterface, FileLogger())

# Típusbiztos feloldás
logger = container.resolve(LoggerInterface)
```

## API Referencia

### LazyComponent

Lusta betöltésű komponensek wrapper osztálya.

#### Metódusok

- `get() -> Any`: Lekéri a komponens példányt (lusta betöltéssel)
- `is_loaded: bool`: Ellenőrzi, hogy a komponens betöltődött-e már

### DIContainer

Fő konténer osztály a függőségek kezeléséhez.

#### Metódusok

##### Regisztráció

- `register_instance(interface: Any, instance: Any) -> None`
  - Példány regisztrálása interfész alapján

- `register_factory(interface: Any, factory: Callable[[], Any]) -> None`
  - Factory függvény regisztrálása

- `register_lazy(component_name: str, factory_func: Callable[[], Any]) -> None`
  - Lusta betöltésű komponens regisztrálása

- `register(component_name: str, instance: Any) -> None`
  - Komponens példány regisztrálása név alapján

##### Feloldás

- `resolve(interface: Any) -> Any | None`
  - Függőség feloldása interfész alapján

- `get(component_name: str) -> Any`
  - Komponens lekérése név alapján (kivételt dob, ha nem található)

##### Életciklus Kezelés

- `preload_components(component_names: list[str]) -> None`
  - Komponensek előzetes betöltése

- `clear() -> None`
  - Konténer ürítése

##### Monitorozás

- `get_lazy_components() -> dict[str, bool]`
  - Lusta komponensek állapotának lekérdezése

- `get_memory_usage() -> dict[str, Any]`
  - Memóriahasználat statisztikák

## Használati Minták

### 1. Alap Használat

```python
from neural_ai.core.base.container import DIContainer

# Konténer létrehozása
container = DIContainer()

# Szolgáltatás regisztrálása
container.register("logger", FileLogger())

# Függőség feloldása
logger = container.get("logger")
```

### 2. Függőség Injektálás

```python
class UserService:
    def __init__(self, logger: LoggerInterface):
        self.logger = logger

# Regisztráció
container.register_instance(LoggerInterface, FileLogger())
container.register("user_service", UserService(container.resolve(LoggerInterface)))
```

### 3. Konfigurálható Komponensek

```python
def create_configurable_service():
    config = load_config()
    return ConfigurableService(config)

container.register_lazy("configurable_service", create_configurable_service)
```

### 4. Tesztelés

```python
# Teszt környezetben mock-ok használata
def test_user_service():
    container = DIContainer()
    mock_logger = Mock()
    container.register_instance(LoggerInterface, mock_logger)
    
    service = UserService(container.resolve(LoggerInterface))
    # teszt logika...
```

## Hibakezelés

### ComponentNotFoundError

Akkor dobódik, ha egy komponens nem található:

```python
try:
    service = container.get("nonexistent_service")
except ComponentNotFoundError as e:
    print(f"Hiba: {e}")
```

### SingletonViolationError

Akkor dobódik, ha a singleton minta megsértésre kerül:

```python
try:
    container.register("service", instance1)
    container.register("service", instance2)  # Hiba!
except SingletonViolationError as e:
    print(f"Singleton hiba: {e}")
```

### ValueError

Érvénytelen paraméterek esetén:

```python
try:
    container.register("", None)  # Hiba!
except ValueError as e:
    print(f"Érvénytelen paraméter: {e}")
```

## Fejlett Használat

### 1. Komponens Életciklus

```python
# Lusta betöltés
container.register_lazy("heavy_service", lambda: HeavyService())

# Későbbi előzetes betöltés
container.preload_components(["heavy_service"])
```

### 2. Memóriakezelés

```python
# Memóriahasználat monitorozása
stats = container.get_memory_usage()
print(f"Példányok száma: {stats['total_instances']}")
print(f"Betöltött lusta komponensek: {stats['loaded_lazy_components']}")
```

### 3. Szálbiztonság

A konténer szálbiztos, beleértve a lusta betöltést is:

```python
import threading

def worker():
    service = container.get("shared_service")
    # biztonságos használat

threads = [threading.Thread(target=worker) for _ in range(10)]
for t in threads:
    t.start()
```

## Best Practices

1. **Interfészek használata**: Mindig interfészek alapján regisztrálj és oldj fel
2. **Lusta betöltés**: Nagy erőforrásigényű komponensekhez használd a lusta betöltést
3. **Singleton minta**: Használj `_initialized` flag-et a singleton osztályokban
4. **Tisztítás**: Tesztelés után mindig hívd meg a `clear()` metódust
5. **Hibakezelés**: Mindig kezeld a lehetséges kivételeket

## Lásd még

- [Base komponensek](base.md)
- [Factory minta](base_factory.md)
- [Függőség kezelés](core_dependencies.md)