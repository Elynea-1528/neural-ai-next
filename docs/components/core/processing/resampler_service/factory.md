# ResamplerService Factory

## Áttekintés

A `ResamplerServiceFactory` a ResamplerService létrehozásáért és életciklusának kezeléséért felelős factory osztály. Ez az osztály biztosítja a dependency injection elvét és a singleton mintázatot a ResamplerService-hez.

## Osztály struktúra

```python
class ResamplerServiceFactory:
    """Factory osztály a ResamplerService létrehozásához és kezeléséhez."""
    
    @staticmethod
    def create(storage: "StorageInterface") -> ResamplerInterface:
        """ResamplerService példány létrehozása."""
        
    @classmethod
    def get_instance(cls) -> ResamplerInterface:
        """ResamplerService példány lekérdezése a DI konténerből."""
```

## Metódusok

### `create(storage)`

Statikus metódus, amely létrehozza a ResamplerService példányt.

**Paraméterek:**
- `storage` (StorageInterface): A tárolási interfész példány

**Visszatérési érték:**
- `ResamplerInterface`: A létrehozott ResamplerService példány

**Példa:**
```python
from neural_ai.core.storage.factory import StorageFactory
from neural_ai.core.processing.resampler_service import ResamplerServiceFactory

# Storage létrehozása
storage = StorageFactory.get_storage(storage_type="parquet")

# ResamplerService létrehozása
resampler = ResamplerServiceFactory.create(storage=storage)
```

### `get_instance()`

Osztálymetódus, amely lekéri a ResamplerService példányt a DI konténerből. Ha még nem létezik, létrehozza és regisztrálja.

**Visszatérési érték:**
- `ResamplerInterface`: A ResamplerService példány

**Kivételek:**
- `ComponentNotFoundError`: Ha a komponens nem található a konténerben

**Példa:**
```python
from neural_ai.core.processing.resampler_service import ResamplerServiceFactory

# Példány lekérése (automatikus létrehozással)
resampler = ResamplerServiceFactory.get_instance()
```

## DI konténer integráció

A ResamplerServiceFactory a `DIContainer` osztályt használja a példányok kezeléséhez:

```python
from neural_ai.core.base.implementations.di_container import DIContainer

container = DIContainer()

# Komponens lekérése
instance = container.get("ResamplerService")

# Ha nem létezik, létrehozzuk és regisztráljuk
if instance is None:
    storage = StorageFactory.get_storage(storage_type="parquet")
    instance = ResamplerServiceFactory.create(storage=storage)
    container.register("ResamplerService", instance)
```

## Használati minták

### 1. Egyszerű használat (ajánlott)

```python
# Automatikus létrehozás és DI kezelés
resampler = ResamplerServiceFactory.get_instance()
```

### 2. Manuális létrehozás

```python
# Saját storage példánnyal
storage = StorageFactory.get_storage(storage_type="parquet")
resampler = ResamplerServiceFactory.create(storage=storage)
```

### 3. Teszteléshez

```python
# Mock storage használata
from unittest.mock import Mock

mock_storage = Mock(spec=StorageInterface)
resampler = ResamplerServiceFactory.create(storage=mock_storage)
```

## Függőségek

- `neural_ai.core.base.implementations.di_container.DIContainer`
- `neural_ai.core.storage.factory.StorageFactory`
- `neural_ai.core.processing.resampler_service.implementations.resampler_service.ResamplerService`
- `neural_ai.core.processing.resampler_service.interfaces.resampler_interface.ResamplerInterface`

## Teljesítmény optimalizációk

- **Lazy Loading**: A példány csak akkor jön létre, amikor először szükség van rá
- **Singleton Pattern**: Mindig ugyanaz a példány kerül visszaadásra
- **DI Integration**: Automatikus függőség-kezelés a konténer segítségével

## Hibakezelés

A factory biztosítja, hogy a ResamplerService mindig érvényes StorageInterface-et kapjon:

```python
try:
    resampler = ResamplerServiceFactory.get_instance()
except ComponentNotFoundError as e:
    # Kezeljük a hibát
    print(f"Komponens nem található: {e}")
except Exception as e:
    # Egyéb hibák
    print(f"Váratlan hiba: {e}")
```

## Kapcsolódó dokumentáció

- [ResamplerService](../index.md)
- [ResamplerInterface](interfaces/resampler_interface.md)
- [ResamplerService Implementation](implementations/resampler_service.md)