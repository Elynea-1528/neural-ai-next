# Base Error Kivételek

## Áttekintés

Alap kivételek a Neural AI Next projektben.

Ez a modul definiálja az összes kivétel alaposztályait és a specifikus kivételeket a különböző komponensekhez (tárolás, konfiguráció, hálózat, stb.).

## Kivétel Osztályok

### `NeuralAIException`

Alap kivétel az összes Neural AI Next kivételhez.

Ez az osztály szolgál közös alapként az összes egyéni kivételnek a rendszerben. A kivételek hierarchiájának gyökerét képezi.

### `StorageException`

Alap kivétel a tárolással kapcsolatos hibákhoz.

Ez a kivétel a fájlrendszerrel, adattárolással és azokhoz kapcsolódó műveletekkel kapcsolatos problémákra használatos.

### `StorageWriteError`

Akkor dobódik, ha a fájlírási művelet sikertelen.

Ez a kivétel konkrétan a fájlok írásakor fellépő hibákra vonatkozik, például amikor a rendszer nem tud adatokat írni a célfájlba.

### `StorageReadError`

Akkor dobódik, ha a fájlolvasási művelet sikertelen.

Ez a kivétel a fájlok olvasásakor fellépő hibákra vonatkozik, például amikor a fájl nem található vagy sérült az adatszerkezet.

### `StoragePermissionError`

Akkor dobódik, ha jogosultsági problémák merülnek fel.

Ez a kivétel akkor dobódik, amikor a rendszer nem rendelkezik a szükséges jogosultságokkal a tárolási művelet végrehajtásához.

### `ConfigurationError`

Akkor dobódik, ha a konfiguráció érvénytelen vagy hiányos.

Ez a kivétel a konfigurációs fájlok feldolgozásakor vagy a beállítások validálásakor fellépő problémákra használatos.

### `DependencyError`

Akkor dobódik, ha szükséges függőségek nem elérhetőek.

Ez a kivétel akkor dobódik, amikor a rendszer valamelyik külső függősége (csomag, modul, szolgáltatás) nem érhető el vagy nem megfelelő.

### `SingletonViolationError`

Akkor dobódik, ha a singleton minta megsérül.

Ez a kivétel akkor dobódik, amikor egy singleton osztályból többször próbálnak példányt létrehozni, ami a tervezési minta megsértését jelenti.

### `ComponentNotFoundError`

Akkor dobódik, ha egy komponens nem található a konténerben.

Ez a kivétel akkor dobódik, amikor a DI konténer nem találja a kért komponenst a regisztrált szolgáltatások között.

### `NetworkException`

Alap kivétel a hálózati hibákhoz.

Ez a kivétel a hálózati kommunikációval kapcsolatos problémákra használatos, mint például a kapcsolódási hibák vagy az időtúllépések.

### `TimeoutError`

Akkor dobódik, ha egy művelet időtúllépést okoz.

Ez a kivétel akkor dobódik, amikor egy hálózati művelet nem fejeződik be a várt időn belül, és időtúllépés következik be.

### `ConnectionError`

Akkor dobódik, ha a kapcsolódás sikertelen.

Ez a kivétel akkor dobódik, amikor a rendszer nem tud kapcsolódni egy távoli szerverhez vagy szolgáltatáshoz.

### `InsufficientDiskSpaceError`

Akkor dobódik, ha nincs elég lemezterület.

Ez a kivétel akkor dobódik, amikor a rendszer nem rendelkezik elegendő szabad lemezterülettel egy tárolási művelet végrehajtásához.

### `PermissionDeniedError`

Akkor dobódik, ha a jogosultság megtagadva.

Ez a kivétel akkor dobódik, amikor a rendszer hozzáférési jogosultságot próbál megadni vagy ellenőrizni, de a műveletet megtagadják.

## Kivétel Hierarchia

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

## Használati Példák

### Alap kivétel használata

```python
from neural_ai.core.base.exceptions import ConfigurationError

def validate_config(config):
    if not config.get('required_key'):
        raise ConfigurationError("A required_key hiányzik a konfigurációból")
```

### Tárolási hiba kezelése

```python
from neural_ai.core.base.exceptions import StorageWriteError, StorageReadError

try:
    with open('data.txt', 'w') as f:
        f.write(data)
except IOError as e:
    raise StorageWriteError(f"Failed to write data: {e}")

try:
    with open('data.txt', 'r') as f:
        content = f.read()
except IOError as e:
    raise StorageReadError(f"Failed to read data: {e}")
```

### Hálózati hiba kezelése

```python
from neural_ai.core.base.exceptions import ConnectionError, TimeoutError
import requests

try:
    response = requests.get('https://api.example.com', timeout=10)
    response.raise_for_status()
except requests.exceptions.Timeout:
    raise TimeoutError("Az API hívás túllépte az időkorlátot")
except requests.exceptions.ConnectionError:
    raise ConnectionError("Nem sikerült kapcsolódni az API-hoz")
```

## Kapcsolódó Dokumentáció

- [Kivételek Modul](__init__.md)
- [Base Modul](../__init__.md)