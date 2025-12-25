# Base Exceptions Modul

## Áttekintés

Ez a modul exportálja az összes alap és specifikus kivétel osztályt, amelyeket a rendszer különböző komponensei használnak.

## Exportált kivétel osztályok

### Alap kivételek

#### `NeuralAIException`
**Hely:** [`neural_ai.core.base.exceptions.base_error:8`](neural_ai/core/base/exceptions/base_error.py:8)

Az összes Neural AI Next kivétel közös alaposztálya. A kivételek hierarchiájának gyökerét képezi.

#### `StorageException`
**Hely:** [`neural_ai.core.base.exceptions.base_error:18`](neural_ai/core/base/exceptions/base_error.py:18)

Alap kivétel a tárolással kapcsolatos hibákhoz. A fájlrendszerrel, adattárolással és azokhoz kapcsolódó műveletekkel kapcsolatos problémákra használatos.

#### `ConfigurationError`
**Hely:** [`neural_ai.core.base.exceptions.base_error:58`](neural_ai/core/base/exceptions/base_error.py:58)

Akkor dobódik, ha a konfiguráció érvénytelen vagy hiányos. A konfigurációs fájlok feldolgozásakor vagy a beállítások validálásakor fellépő problémákra használatos.

#### `DependencyError`
**Hely:** [`neural_ai.core.base.exceptions.base_error:68`](neural_ai/core/base/exceptions/base_error.py:68)

Akkor dobódik, ha szükséges függőségek nem elérhetőek. Akkor dobódik, amikor a rendszer valamelyik külső függősége (csomag, modul, szolgáltatás) nem érhető el vagy nem megfelelő.

#### `NetworkException`
**Hely:** [`neural_ai.core.base.exceptions.base_error:98`](neural_ai/core/base/exceptions/base_error.py:98)

Alap kivétel a hálózati hibákhoz. A hálózati kommunikációval kapcsolatos problémákra használatos, mint például a kapcsolódási hibák vagy az időtúllépések.

### Tárolási kivételek

#### `StorageWriteError`
**Hely:** [`neural_ai.core.base.exceptions.base_error:28`](neural_ai/core/base/exceptions/base_error.py:28)

Akkor dobódik, ha a fájlírási művelet sikertelen. Konkrétan a fájlok írásakor fellépő hibákra vonatkozik, például amikor a rendszer nem tud adatokat írni a célfájlba.

#### `StorageReadError`
**Hely:** [`neural_ai.core.base.exceptions.base_error:38`](neural_ai/core/base/exceptions/base_error.py:38)

Akkor dobódik, ha a fájlolvasási művelet sikertelen. A fájlok olvasásakor fellépő hibákra vonatkozik, például amikor a fájl nem található vagy sérült az adatszerkezet.

#### `StoragePermissionError`
**Hely:** [`neural_ai.core.base.exceptions.base_error:48`](neural_ai/core/base/exceptions/base_error.py:48)

Akkor dobódik, ha jogosultsági problémák merülnek fel. Akkor dobódik, amikor a rendszer nem rendelkezik a szükséges jogosultságokkal a tárolási művelet végrehajtásához.

#### `InsufficientDiskSpaceError`
**Hely:** [`neural_ai.core.base.exceptions.base_error:128`](neural_ai/core/base/exceptions/base_error.py:128)

Akkor dobódik, ha nincs elég lemezterület. Akkor dobódik, amikor a rendszer nem rendelkezik elegendő szabad lemezterülettel egy tárolási művelet végrehajtásához.

#### `PermissionDeniedError`
**Hely:** [`neural_ai.core.base.exceptions.base_error:138`](neural_ai/core/base/exceptions/base_error.py:138)

Akkor dobódik, ha a jogosultság megtagadva. Akkor dobódik, amikor a rendszer hozzáférési jogosultságot próbál megadni vagy ellenőrizni, de a műveletet megtagadják.

### Singleton és komponens kivételek

#### `SingletonViolationError`
**Hely:** [`neural_ai.core.base.exceptions.base_error:78`](neural_ai/core/base/exceptions/base_error.py:78)

Akkor dobódik, ha a singleton minta megsérül. Akkor dobódik, amikor egy singleton osztályból többször próbálnak példányt létrehozni, ami a tervezési minta megsértését jelenti.

#### `ComponentNotFoundError`
**Hely:** [`neural_ai.core.base.exceptions.base_error:88`](neural_ai/core/base/exceptions/base_error.py:88)

Akkor dobódik, ha egy komponens nem található a konténerben. Akkor dobódik, amikor a DI konténer nem találja a kért komponenst a regisztrált szolgáltatások között.

### Hálózati kivételek

#### `TimeoutError`
**Hely:** [`neural_ai.core.base.exceptions.base_error:108`](neural_ai/core/base/exceptions/base_error.py:108)

Akkor dobódik, ha egy művelet időtúllépést okoz. Akkor dobódik, amikor egy hálózati művelet nem fejeződik be a várt időn belül, és időtúllépés következik be.

#### `ConnectionError`
**Hely:** [`neural_ai.core/base/exceptions/base_error:118`](neural_ai/core/base/exceptions/base_error.py:118)

Akkor dobódik, ha a kapcsolódás sikertelen. Akkor dobódik, amikor a rendszer nem tud kapcsolódni egy távoli szerverhez vagy szolgáltatáshoz.

## Használati példa

```python
from neural_ai.core.base.exceptions import (
    ConfigurationError,
    StorageException,
    DependencyError
)

try:
    # Valamilyen művelet, ami hibát dobhat
    process_data()
except ConfigurationError as e:
    print(f"Konfigurációs hiba: {e}")
except StorageException as e:
    print(f"Tárolási hiba: {e}")
except DependencyError as e:
    print(f"Függőségi hiba: {e}")
```

## Kivétel hierarchia

```
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

## Kapcsolódó dokumentáció

- [Base Error](neural_ai/core/base/exceptions/base_error.md) - Az összes kivétel osztály részletes leírása