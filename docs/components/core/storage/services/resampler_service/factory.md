# ResamplerServiceFactory

## Áttekintés

A `ResamplerServiceFactory` egy factory osztály, amely felelős a [`ResamplerService`](../implementations/resampler_service.md) létrehozásáért és kezeléséért. A factory minta segítségével biztosítja a ResamplerService példányok egységes létrehozását és a DI konténerrel való integrációt.

## Osztály

```python
class ResamplerServiceFactory
```

## Metódusok

### `create()`

ResamplerService példány létrehozása.

```python
@staticmethod
def create(storage: StorageInterface) -> ResamplerInterface
```

**Paraméterek:**

- `storage` (StorageInterface): A tárolási interfész példány

**Visszatérési érték:**

- `ResamplerInterface`: A létrehozott ResamplerService példány

**Példa:**

```python
from neural_ai.core.storage.services.resampler_service import (
    ResamplerServiceFactory,
    ResamplerInterface
)
from neural_ai.core.storage.interfaces.storage_interface import StorageInterface

# Tároló létrehozása
storage: StorageInterface = ...

# ResamplerService létrehozása
resampler: ResamplerInterface = ResamplerServiceFactory.create(storage=storage)
```

### `get_instance()`

ResamplerService példány lekérdezése a DI konténerből.

```python
@classmethod
def get_instance(cls) -> ResamplerInterface
```

**Visszatérési érték:**

- `ResamplerInterface`: A ResamplerService példány

**Kivételek:**

- `ComponentNotFoundError`: Ha a komponens nem található a konténerben

**Példa:**

```python
from neural_ai.core.storage.services.resampler_service import (
    ResamplerServiceFactory,
    ResamplerInterface
)

# ResamplerService példány lekérése
resampler: ResamplerInterface = ResamplerServiceFactory.get_instance()
```

## Használati minták

### Alap használat

```python
from datetime import datetime
from neural_ai.core.storage.services.resampler_service import (
    ResamplerServiceFactory,
    ResamplerInterface
)

# ResamplerService példány létrehozása
resampler: ResamplerInterface = ResamplerServiceFactory.get_instance()

# Használat
start = datetime(2024, 1, 1, 0, 0, 0)
end = datetime(2024, 1, 1, 23, 59, 59)

ohlcv_data = await resampler.resample(
    symbol="EURUSD",
    start=start,
    end=end,
    timeframe="1m"
)
```

### Egyéni tárolóval

```python
from neural_ai.core.storage.services.resampler_service import (
    ResamplerServiceFactory,
    ResamplerInterface
)
from neural_ai.core.storage.factory import StorageFactory
from neural_ai.core.storage.interfaces.storage_interface import StorageInterface

# Egyéni tároló létrehozása
storage: StorageInterface = StorageFactory.get_storage(storage_type="parquet")

# ResamplerService létrehozása egyéni tárolóval
resampler: ResamplerInterface = ResamplerServiceFactory.create(storage=storage)
```

### DI konténer integráció

```python
from neural_ai.core.base.implementations.di_container import DIContainer
from neural_ai.core.storage.services.resampler_service import (
    ResamplerServiceFactory,
    ResamplerInterface
)

# DI konténer példányosítása
container = DIContainer()

# ResamplerService regisztrálása
resampler = ResamplerServiceFactory.get_instance()
container.register("ResamplerService", resampler)

# Későbbi lekérdezés
retrieved_resampler: ResamplerInterface = container.get("ResamplerService")
```

## Factory minta előnyei

### 1. Létrehozás egységesítése

A factory biztosítja, hogy minden ResamplerService példány konzisztens módon jöjjön létre a szükséges függőségekkel.

### 2. DI konténer integráció

A factory automatikusan kezeli a ResamplerService regisztrációt a DI konténerben, egyszerűsítve a függőség kezelését.

### 3. Tesztelhetőség

A factory mintának köszönhetően könnyen cserélhető mock objektumokkal teszteléskor.

```python
# Tesztelés mock tárolóval
class MockStorage:
    def load_tick_data(self, symbol, start, end):
        return create_mock_tick_data()

mock_storage = MockStorage()
test_resampler = ResamplerServiceFactory.create(storage=mock_storage)
```

## Hibakezelés

### Komponens nem található

```python
from neural_ai.core.base.exceptions import ComponentNotFoundError

try:
    resampler = ResamplerServiceFactory.get_instance()
except ComponentNotFoundError as e:
    print(f"Komponens nem található: {e}")
```

### Érvénytelen tároló

```python
from neural_ai.core.storage.exceptions import StorageError

try:
    storage = StorageFactory.get_storage(storage_type="invalid")
    resampler = ResamplerServiceFactory.create(storage=storage)
except StorageError as e:
    print(f"Tároló létrehozása sikertelen: {e}")
```

## Lásd még

- [ResamplerInterface](../interfaces/resampler_interface.md)
- [ResamplerService](../implementations/resampler_service.md)
- [ResamplerError](../exceptions/resampler_error.md)
- [DIContainer](../../../../core/base/implementations/di_container.md)