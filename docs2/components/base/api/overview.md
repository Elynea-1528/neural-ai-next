# Base Komponens API Áttekintés

## Áttekintés

Ez a dokumentum a Base komponens teljes API-ját dokumentálja. A Base komponens a Neural AI Next projekt alapvető infrastruktúráját biztosítja, beleértve a dependency injection konténert, a core komponensek kezelését és a lazy loading mechanizmust.

## API Struktúra

A Base komponens API-ja a következő fő részekből áll:

### 1. Konténer és Függőségkezelés

- **[`DIContainer`](container.md)** - Dependency injection konténer a komponensek életciklusának kezeléséhez
- **[`LazyComponent`](container.md#lazycomponent)** - Lazy loading wrapper osztály

### 2. Core Komponensek

- **[`CoreComponents`](core_components.md)** - A core komponensek gyűjteménye (logger, config, storage)
- **[`LazyLoader`](core_components.md#lazyloader)** - Lazy loader erőforrásokhoz

### 3. Komponens Factory

- **[`CoreComponentFactory`](factory.md)** - Factory osztály a komponensek létrehozásához

### 4. Segédosztályok

- **[`LazyLoader`](lazy_loading.md)** - Általános lazy loading implementáció
- **[`lazy_property`](lazy_loading.md#lazy_property)** - Dekorátor lazy property-khez
- **[`SingletonMeta`](singleton.md)** - Singleton metaclass

### 5. Kivételek

- **[Kivétel hierarchia](exceptions.md)** - Az összes Base komponens kivétel

## Importálás

```python
# Alap importok
from neural_ai.core.base import DIContainer, CoreComponents, CoreComponentFactory

# Kivételek
from neural_ai.core.base.exceptions import (
    ComponentNotFoundError,
    SingletonViolationError,
    ConfigurationError,
    DependencyError
)

# Segédosztályok
from neural_ai.core.base.lazy_loading import LazyLoader, lazy_property
from neural_ai.core.base.singleton import SingletonMeta
```

## API Design Elvek

### 1. Egyszerűség

Minden API egyszerű és intuitív használatú, minimális konfigurációval.

```python
# Példa: Alapvető használat
components = CoreComponentFactory.create_minimal()
components.logger.info("Sikeres inicializálás")
```

### 2. Típusbiztonság

Minden metódus és tulajdonság rendelkezik típusannotációval.

```python
def register_instance(self, interface: Any, instance: Any) -> None:
    """Példány regisztrálása a konténerben."""
    pass
```

### 3. Lazy Loading

Az összes drága művelet lazy loadinggel történik, ami optimalizálja a teljesítményt.

```python
# A logger csak akkor töltődik be, ha először használják
if components.has_logger():
    components.logger.info("Első használat - most töltődik be")
```

### 4. Thread Safety

Minden művelet szálbiztos, biztonságos több szálas környezetben.

```python
# A lazy loading szálbiztos
lazy_loader = LazyLoader(expensive_operation)
# Több szál is biztonságosan használhatja
```

## Főbb API-k

### DIContainer API

A dependency injection konténer API-ja:

```python
class DIContainer:
    """Dependency injection konténer."""

    def register_instance(self, interface: Any, instance: Any) -> None:
        """Példány regisztrálása."""

    def register_factory(self, interface: Any, factory: Any) -> None:
        """Factory regisztrálása."""

    def resolve(self, interface: Any) -> Optional[Any]:
        """Függőség feloldása."""

    def register_lazy(self, component_name: str, factory_func: Callable[[], Any]) -> None:
        """Lazy komponens regisztrálása."""

    def get(self, component_name: str) -> Any:
        """Komponens lekérése."""
```

[Részletes API dokumentáció](container.md)

### CoreComponents API

A core komponensek API-ja:

```python
class CoreComponents:
    """Core components with lazy loading support."""

    @property
    def config(self) -> Optional[ConfigManagerInterface]:
        """Konfiguráció kezelő."""

    @property
    def logger(self) -> Optional[LoggerInterface]:
        """Naplózó komponens."""

    @property
    def storage(self) -> Optional[StorageInterface]:
        """Tároló komponens."""

    def has_config(self) -> bool:
        """Konfiguráció ellenőrzése."""

    def has_logger(self) -> bool:
        """Logger ellenőrzése."""

    def has_storage(self) -> bool:
        """Storage ellenőrzése."""

    def validate(self) -> bool:
        """Komponensek validálása."""
```

[Részletes API dokumentáció](core_components.md)

### CoreComponentFactory API

A komponens factory API-ja:

```python
class CoreComponentFactory(metaclass=SingletonMeta):
    """Factory for creating core components."""

    @staticmethod
    def create_components(
        config_path: Optional[Union[str, Path]] = None,
        log_path: Optional[Union[str, Path]] = None,
        storage_path: Optional[Union[str, Path]] = None,
    ) -> CoreComponents:
        """Komponensek létrehozása."""

    @staticmethod
    def create_minimal() -> CoreComponents:
        """Minimális komponens készlet létrehozása."""

    @staticmethod
    def create_with_container(container: DIContainer) -> CoreComponents:
        """Létrehozás meglévő konténerből."""
```

[Részletes API dokumentáció](factory.md)

## Kivételkezelés

A Base komponens átfogó kivétel hierarchiát biztosít:

```python
NeuralAIException
├── StorageException
│   ├── StorageWriteError
│   ├── StorageReadError
│   ├── StoragePermissionError
│   ├── InsufficientDiskSpaceError
│   └── PermissionDeniedError
├── ConfigurationError
├── DependencyError
├── SingletonViolationError
├── ComponentNotFoundError
└── NetworkException
    ├── TimeoutError
    └── ConnectionError
```

[Részletes kivétel dokumentáció](exceptions.md)

## Használati minták

### 1. Alapvető inicializálás

```python
from neural_ai.core.base import CoreComponentFactory

# Komponensek létrehozása
components = CoreComponentFactory.create_components(
    config_path='config.yaml',
    log_path='app.log',
    storage_path='./data'
)

# Használat
components.logger.info("Alkalmazás elindult")
```

### 2. Egyedi komponens regisztráció

```python
from neural_ai.core.base import DIContainer, CoreComponents

# Konténer létrehozása
container = DIContainer()

# Egyedi komponens hozzáadása
container.register_instance(MyInterface, MyImplementation())

# Core komponensek létrehozása
components = CoreComponents(container=container)
```

### 3. Lazy loading használata

```python
from neural_ai.core.base.lazy_loading import LazyLoader

# Lazy loader létrehozása
loader = LazyLoader(expensive_operation)

# Használat (csak most töltődik be)
result = loader()
```

## Teljesítmény megfontolások

### 1. Lazy Loading

A lazy loading optimalizálja a memóriahasználatot és a betöltési időt:

```python
# A komponens csak akkor töltődik be, amikor először használják
components.logger  # Most töltődik be a logger
```

### 2. Singleton Pattern

A singleton minta biztosítja, hogy minden komponensből csak egy példány legyen:

```python
# Minden hívás ugyanazt a példányt adja vissza
factory1 = CoreComponentFactory(container)
factory2 = CoreComponentFactory(container)
assert factory1 is factory2  # True
```

### 3. Thread Safety

Minden művelet szálbiztos:

```python
# Több szál is biztonságosan használhatja a konténert
def worker():
    component = container.get('my_component')
    # Biztonságos műveletek
```

## Hibakeresés és naplózás

A Base komponens beépített naplózási támogatással rendelkezik:

```python
# Konténer naplózása
container = DIContainer()  # Automatikusan létrehoz egy loggert

# Komponens állapot ellenőrzése
lazy_status = container.get_lazy_components()
print(lazy_status)  # {'logger': False, 'config': True, ...}

# Memóriahasználat ellenőrzése
memory_stats = container.get_memory_usage()
print(memory_stats)
```

## Kapcsolódó dokumentáció

- [Architektúra áttekintés](../architecture/overview.md)
- [Tervezési alapelvek](../architecture/design_principles.md)
- [Komponens kölcsönhatások](../architecture/component_interactions.md)
- [Fejlesztési útmutató](../guides/getting_started.md)

## API referencia

- [DIContainer API](container.md)
- [CoreComponents API](core_components.md)
- [CoreComponentFactory API](factory.md)
- [Kivételek API](exceptions.md)
- [Lazy Loading API](lazy_loading.md)
- [Singleton API](singleton.md)

## Példák

- [Alap használati példák](../examples/basic_usage.md)
- [Haladó példák](../examples/advanced_usage.md)
- [Tesztelési példák](../examples/testing.md)

---

**Dokumentum verzió:** 1.0
**Utolsó frissítés:** 2025-12-19
**API verzió:** 1.0.0
