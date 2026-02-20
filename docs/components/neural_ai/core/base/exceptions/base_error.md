# neural_ai/core/base/exceptions/base_error.py

Alap kivételek a Neural AI Next projektben.

Ez a modul definiálja az összes kivétel alaposztályait és a specifikus
kivételeket a különböző komponensekhez (tárolás, konfiguráció, hálózat, stb.).

## Osztály: `NeuralAIException(Exception)`

Alap kivétel az összes Neural AI Next kivételhez.

Ez az osztály szolgál közös alapként az összes egyéni kivételnek
a rendszerben. A kivételek hierarchiájának gyökerét képezi.

## Osztály: `StorageException(NeuralAIException)`

Alap kivétel a tárolással kapcsolatos hibákhoz.

Ez a kivétel a fájlrendszerrel, adattárolással és azokhoz kapcsolódó
műveletekkel kapcsolatos problémákra használatos.

## Osztály: `StorageWriteError(StorageException)`

Akkor dobódik, ha a fájlírási művelet sikertelen.

Ez a kivétel konkrétan a fájlok írásakor fellépő hibákra vonatkozik,
például amikor a rendszer nem tud adatokat írni a célfájlba.

## Osztály: `StorageReadError(StorageException)`

Akkor dobódik, ha a fájlolvasási művelet sikertelen.

Ez a kivétel a fájlok olvasásakor fellépő hibákra vonatkozik,
például amikor a fájl nem található vagy sérült az adatszerkezet.

## Osztály: `StoragePermissionError(StorageException)`

Akkor dobódik, ha jogosultsági problémák merülnek fel.

Ez a kivétel akkor dobódik, amikor a rendszer nem rendelkezik a szükséges
jogosultságokkal a tárolási művelet végrehajtásához.

## Osztály: `ConfigurationError(NeuralAIException)`

Akkor dobódik, ha a konfiguráció érvénytelen vagy hiányos.

Ez a kivétel a konfigurációs fájlok feldolgozásakor vagy a beállítások
validálásakor fellépő problémákra használatos.

## Osztály: `DependencyError(NeuralAIException)`

Akkor dobódik, ha szükséges függőségek nem elérhetőek.

Ez a kivétel akkor dobódik, amikor a rendszer valamelyik külső
függősége (csomag, modul, szolgáltatás) nem érhető el vagy nem megfelelő.

## Osztály: `SingletonViolationError(NeuralAIException)`

Akkor dobódik, ha a singleton minta megsérül.

Ez a kivétel akkor dobódik, amikor egy singleton osztályból többször
próbálnak példányt létrehozni, ami a tervezési minta megsértését jelenti.

## Osztály: `ComponentNotFoundError(NeuralAIException)`

Akkor dobódik, ha egy komponens nem található a konténerben.

Ez a kivétel akkor dobódik, amikor a DI konténer nem találja a kért
komponenst a regisztrált szolgáltatások között.

## Osztály: `NetworkException(NeuralAIException)`

Alap kivétel a hálózati hibákhoz.

Ez a kivétel a hálózati kommunikációval kapcsolatos problémákra használatos,
mint például a kapcsolódási hibák vagy az időtúllépések.

## Osztály: `TimeoutError(NetworkException)`

Akkor dobódik, ha egy művelet időtúllépést okoz.

Ez a kivétel akkor dobódik, amikor egy hálózati művelet nem fejeződik be
a várt időn belül, és időtúllépés következik be.

## Osztály: `ConnectionError(NetworkException)`

Akkor dobódik, ha a kapcsolódás sikertelen.

Ez a kivétel akkor dobódik, amikor a rendszer nem tud kapcsolódni
egy távoli szerverhez vagy szolgáltatáshoz.

## Osztály: `InsufficientDiskSpaceError(StorageException)`

Akkor dobódik, ha nincs elég lemezterület.

Ez a kivétel akkor dobódik, amikor a rendszer nem rendelkezik elegendő
szabad lemezterülettel egy tárolási művelet végrehajtásához.

## Osztály: `PermissionDeniedError(StorageException)`

Akkor dobódik, ha a jogosultság megtagadva.

Ez a kivétel akkor dobódik, amikor a rendszer hozzáférési jogosultságot
próbál megadni vagy ellenőrizni, de a műveletet megtagadják.

---

**Forrásfájl:** [`neural_ai/core/base/exceptions/base_error.py`](../../neural_ai/core/base/exceptions/base_error.py)
