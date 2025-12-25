"""Alap kivételek a Neural AI Next projektben.

Ez a modul definiálja az összes kivétel alaposztályait és a specifikus
kivételeket a különböző komponensekhez (tárolás, konfiguráció, hálózat, stb.).
"""


class NeuralAIException(Exception):
    """Alap kivétel az összes Neural AI Next kivételhez.

    Ez az osztály szolgál közös alapként az összes egyéni kivételnek
    a rendszerben. A kivételek hierarchiájának gyökerét képezi.
    """

    pass


class StorageException(NeuralAIException):
    """Alap kivétel a tárolással kapcsolatos hibákhoz.

    Ez a kivétel a fájlrendszerrel, adattárolással és azokhoz kapcsolódó
    műveletekkel kapcsolatos problémákra használatos.
    """

    pass


class StorageWriteError(StorageException):
    """Akkor dobódik, ha a fájlírási művelet sikertelen.

    Ez a kivétel konkrétan a fájlok írásakor fellépő hibákra vonatkozik,
    például amikor a rendszer nem tud adatokat írni a célfájlba.
    """

    pass


class StorageReadError(StorageException):
    """Akkor dobódik, ha a fájlolvasási művelet sikertelen.

    Ez a kivétel a fájlok olvasásakor fellépő hibákra vonatkozik,
    például amikor a fájl nem található vagy sérült az adatszerkezet.
    """

    pass


class StoragePermissionError(StorageException):
    """Akkor dobódik, ha jogosultsági problémák merülnek fel.

    Ez a kivétel akkor dobódik, amikor a rendszer nem rendelkezik a szükséges
    jogosultságokkal a tárolási művelet végrehajtásához.
    """

    pass


class ConfigurationError(NeuralAIException):
    """Akkor dobódik, ha a konfiguráció érvénytelen vagy hiányos.

    Ez a kivétel a konfigurációs fájlok feldolgozásakor vagy a beállítások
    validálásakor fellépő problémákra használatos.
    """

    pass


class DependencyError(NeuralAIException):
    """Akkor dobódik, ha szükséges függőségek nem elérhetőek.

    Ez a kivétel akkor dobódik, amikor a rendszer valamelyik külső
    függősége (csomag, modul, szolgáltatás) nem érhető el vagy nem megfelelő.
    """

    pass


class SingletonViolationError(NeuralAIException):
    """Akkor dobódik, ha a singleton minta megsérül.

    Ez a kivétel akkor dobódik, amikor egy singleton osztályból többször
    próbálnak példányt létrehozni, ami a tervezési minta megsértését jelenti.
    """

    pass


class ComponentNotFoundError(NeuralAIException):
    """Akkor dobódik, ha egy komponens nem található a konténerben.

    Ez a kivétel akkor dobódik, amikor a DI konténer nem találja a kért
    komponenst a regisztrált szolgáltatások között.
    """

    pass


class NetworkException(NeuralAIException):
    """Alap kivétel a hálózati hibákhoz.

    Ez a kivétel a hálózati kommunikációval kapcsolatos problémákra használatos,
    mint például a kapcsolódási hibák vagy az időtúllépések.
    """

    pass


class TimeoutError(NetworkException):
    """Akkor dobódik, ha egy művelet időtúllépést okoz.

    Ez a kivétel akkor dobódik, amikor egy hálózati művelet nem fejeződik be
    a várt időn belül, és időtúllépés következik be.
    """

    pass


class ConnectionError(NetworkException):
    """Akkor dobódik, ha a kapcsolódás sikertelen.

    Ez a kivétel akkor dobódik, amikor a rendszer nem tud kapcsolódni
    egy távoli szerverhez vagy szolgáltatáshoz.
    """

    pass


class InsufficientDiskSpaceError(StorageException):
    """Akkor dobódik, ha nincs elég lemezterület.

    Ez a kivétel akkor dobódik, amikor a rendszer nem rendelkezik elegendő
    szabad lemezterülettel egy tárolási művelet végrehajtásához.
    """

    pass


class PermissionDeniedError(StorageException):
    """Akkor dobódik, ha a jogosultság megtagadva.

    Ez a kivétel akkor dobódik, amikor a rendszer hozzáférési jogosultságot
    próbál megadni vagy ellenőrizni, de a műveletet megtagadják.
    """

    pass
