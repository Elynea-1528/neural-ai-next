# Base Error - Alap kivételek

## Áttekintés

Ez a modul definiálja az összes kivétel alaposztályait és a specifikus kivételeket a különböző komponensekhez (tárolás, konfiguráció, hálózat, stb.).

## Kivétel osztályok

### `NeuralAIException`

**Hely:** [`neural_ai.core.base.exceptions.base_error:8`](neural_ai/core/base/exceptions/base_error.py:8)

Alap kivétel az összes Neural AI Next kivételhez. Ez az osztály szolgál közös alapként az összes egyéni kivételnek a rendszerben. A kivételek hierarchiájának gyökerét képezi.

```python
class NeuralAIException(Exception):
    """Alap kivétel az összes Neural AI Next kivételhez."""
    pass
```

### `StorageException`

**Hely:** [`neural_ai.core.base.exceptions.base_error:18`](neural_ai/core/base/exceptions/base_error.py:18)

Alap kivétel a tárolással kapcsolatos hibákhoz. Ez a kivétel a fájlrendszerrel, adattárolással és azokhoz kapcsolódó műveletekkel kapcsolatos problémákra használatos.

```python
class StorageException(NeuralAIException):
    """Alap kivétel a tárolással kapcsolatos hibákhoz."""
    pass
```

### `StorageWriteError`

**Hely:** [`neural_ai.core.base.exceptions.base_error:28`](neural_ai/core/base/exceptions/base_error.py:28)

Akkor dobódik, ha a fájlírási művelet sikertelen. Ez a kivétel konkrétan a fájlok írásakor fellépő hibákra vonatkozik, például amikor a rendszer nem tud adatokat írni a célfájlba.

```python
class StorageWriteError(StorageException):
    """Akkor dobódik, ha a fájlírási művelet sikertelen."""
    pass
```

**Használati példa:**
```python
try:
    storage.write("data.txt", content)
except StorageWriteError as e:
    logger.error(f"Fájl írási hiba: {e}")
```

### `StorageReadError`

**Hely:** [`neural_ai.core/base/exceptions/base_error:38`](neural_ai/core/base/exceptions/base_error.py:38)

Akkor dobódik, ha a fájlolvasási művelet sikertelen. Ez a kivétel a fájlok olvasásakor fellépő hibákra vonatkozik, például amikor a fájl nem található vagy sérült az adatszerkezet.

```python
class StorageReadError(StorageException):
    """Akkor dobódik, ha a fájlolvasási művelet sikertelen."""
    pass
```

**Használati példa:**
```python
try:
    data = storage.read("data.txt")
except StorageReadError as e:
    logger.error(f"Fájl olvasási hiba: {e}")
```

### `StoragePermissionError`

**Hely:** [`neural_ai.core.base.exceptions.base_error:48`](neural_ai/core/base/exceptions/base_error.py:48)

Akkor dobódik, ha jogosultsági problémák merülnek fel. Ez a kivétel akkor dobódik, amikor a rendszer nem rendelkezik a szükséges jogosultságokkal a tárolási művelet végrehajtásához.

```python
class StoragePermissionError(StorageException):
    """Akkor dobódik, ha jogosultsági problémák merülnek fel."""
    pass
```

### `ConfigurationError`

**Hely:** [`neural_ai.core.base.exceptions.base_error:58`](neural_ai/core/base/exceptions/base_error.py:58)

Akkor dobódik, ha a konfiguráció érvénytelen vagy hiányos. Ez a kivétel a konfigurációs fájlok feldolgozásakor vagy a beállítások validálásakor fellépő problémákra használatos.

```python
class ConfigurationError(NeuralAIException):
    """Akkor dobódik, ha a konfiguráció érvénytelen vagy hiányos."""
    pass
```

**Használati példa:**
```python
try:
    config = load_config("config.yml")
except ConfigurationError as e:
    logger.error(f"Konfigurációs hiba: {e}")
```

### `DependencyError`

**Hely:** [`neural_ai.core.base.exceptions.base_error:68`](neural_ai/core/base/exceptions/base_error.py:68)

Akkor dobódik, ha szükséges függőségek nem elérhetőek. Ez a kivétel akkor dobódik, amikor a rendszer valamelyik külső függősége (csomag, modul, szolgáltatás) nem érhető el vagy nem megfelelő.

```python
class DependencyError(NeuralAIException):
    """Akkor dobódik, ha szükséges függőségek nem elérhetőek."""
    pass
```

### `SingletonViolationError`

**Hely:** [`neural_ai.core.base.exceptions.base_error:78`](neural_ai/core/base/exceptions/base_error.py:78)

Akkor dobódik, ha a singleton minta megsérül. Ez a kivétel akkor dobódik, amikor egy singleton osztályból többször próbálnak példányt létrehozni, ami a tervezési minta megsértését jelenti.

```python
class SingletonViolationError(NeuralAIException):
    """Akkor dobódik, ha a singleton minta megsérül."""
    pass
```

### `ComponentNotFoundError`

**Hely:** [`neural_ai.core.base/exceptions/base_error:88`](neural_ai/core/base/exceptions/base_error.py:88)

Akkor dobódik, ha egy komponens nem található a konténerben. Ez a kivétel akkor dobódik, amikor a DI konténer nem találja a kért komponenst a regisztrált szolgáltatások között.

```python
class ComponentNotFoundError(NeuralAIException):
    """Akkor dobódik, ha egy komponens nem található a konténerben."""
    pass
```

### `NetworkException`

**Hely:** [`neural_ai.core.base.exceptions.base_error:98`](neural_ai/core/base/exceptions/base_error.py:98)

Alap kivétel a hálózati hibákhoz. Ez a kivétel a hálózati kommunikációval kapcsolatos problémákra használatos, mint például a kapcsolódási hibák vagy az időtúllépések.

```python
class NetworkException(NeuralAIException):
    """Alap kivétel a hálózati hibákhoz."""
    pass
```

### `TimeoutError`

**Hely:** [`neural_ai.core/base/exceptions/base_error:108`](neural_ai/core/base/exceptions/base_error.py:108)

Akkor dobódik, ha egy művelet időtúllépést okoz. Ez a kivétel akkor dobódik, amikor egy hálózati művelet nem fejeződik be a várt időn belül, és időtúllépés következik be.

```python
class TimeoutError(NetworkException):
    """Akkor dobódik, ha egy művelet időtúllépést okoz."""
    pass
```

### `ConnectionError`

**Hely:** [`neural_ai.core/base/exceptions/base_error:118`](neural_ai/core/base/exceptions/base_error.py:118)

Akkor dobódik, ha a kapcsolódás sikertelen. Ez a kivétel akkor dobódik, amikor a rendszer nem tud kapcsolódni egy távoli szerverhez vagy szolgáltatáshoz.

```python
class ConnectionError(NetworkException):
    """Akkor dobódik, ha a kapcsolódás sikertelen."""
    pass
```

### `InsufficientDiskSpaceError`

**Hely:** [`neural_ai.core/base/exceptions/base_error:128`](neural_ai/core/base/exceptions/base_error.py:128)

Akkor dobódik, ha nincs elég lemezterület. Ez a kivétel akkor dobódik, amikor a rendszer nem rendelkezik elegendő szabad lemezterülettel egy tárolási művelet végrehajtásához.

```python
class InsufficientDiskSpaceError(StorageException):
    """Akkor dobódik, ha nincs elég lemezterület."""
    pass
```

### `PermissionDeniedError`

**Hely:** [`neural_ai.core/base/exceptions/base_error:138`](neural_ai/core/base/exceptions/base_error.py:138)

Akkor dobódik, ha a jogosultság megtagadva. Ez a kivétel akkor dobódik, amikor a rendszer hozzáférési jogosultságot próbál megadni vagy ellenőrizni, de a műveletet megtagadják.

```python
class PermissionDeniedError(StorageException):
    """Akkor dobódik, ha a jogosultság megtagadva."""
    pass
```

## Kivétel hierarchia

```
NeuralAIException (Exception)
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

## Használati példák

### Alap kivétel kezelés

```python
from neural_ai.core.base.exceptions.base_error import (
    NeuralAIException,
    StorageException,
    ConfigurationError
)

try:
    # Valamilyen művelet
    process_data()
except ConfigurationError as e:
    print(f"Konfigurációs hiba: {e}")
except StorageException as e:
    print(f"Tárolási hiba: {e}")
except NeuralAIException as e:
    print(f"Általános hiba: {e}")
```

### Tárolási hibák kezelése

```python
from neural_ai.core.base.exceptions.base_error import (
    StorageWriteError,
    StorageReadError,
    InsufficientDiskSpaceError
)

try:
    # Fájl írása
    with open("large_file.dat", "wb") as f:
        f.write(large_data)
except InsufficientDiskSpaceError:
    print("Nincs elég lemezterület!")
except StorageWriteError:
    print("Írási hiba történt!")
```

### Hálózati hibák kezelése

```python
from neural_ai.core.base.exceptions.base_error import (
    ConnectionError,
    TimeoutError
)

try:
    response = api_client.get_data(timeout=30)
except TimeoutError:
    print("Az API válasz ideje túllépte a limitet")
except ConnectionError:
    print("Nem sikerült kapcsolódni az API-hoz")
```

## Kapcsolódó dokumentáció

- [Exceptions Init](neural_ai/core/base/exceptions/__init__.md) - A kivételek exportáló modulja