"""Alap kivételek a Neural AI Next projektben.

Ez a modul definiálja az összes kivétel alaposztályait és a specifikus
kivételeket a különböző komponensekhez.
"""


class NeuralAIException(Exception):
    """Alap kivétel az összes Neural AI Next kivételhez."""

    pass


class StorageException(NeuralAIException):
    """Alap kivétel a tárolással kapcsolatos hibákhoz."""

    pass


class StorageWriteError(StorageException):
    """Akkor dobódik, ha a fájlírási művelet sikertelen."""

    pass


class StorageReadError(StorageException):
    """Akkor dobódik, ha a fájlolvasási művelet sikertelen."""

    pass


class StoragePermissionError(StorageException):
    """Akkor dobódik, ha jogosultsági problémák merülnek fel."""

    pass


class ConfigurationError(NeuralAIException):
    """Akkor dobódik, ha a konfiguráció érvénytelen vagy hiányos."""

    pass


class DependencyError(NeuralAIException):
    """Akkor dobódik, ha szükséges függőségek nem elérhetőek."""

    pass


class SingletonViolationError(NeuralAIException):
    """Akkor dobódik, ha a singleton minta megsérül."""

    pass


class ComponentNotFoundError(NeuralAIException):
    """Akkor dobódik, ha egy komponens nem található a konténerben."""

    pass


class NetworkException(NeuralAIException):
    """Alap kivétel a hálózati hibákhoz."""

    pass


class TimeoutError(NetworkException):
    """Akkor dobódik, ha egy művelet időtúllépést okoz."""

    pass


class ConnectionError(NetworkException):
    """Akkor dobódik, ha a kapcsolódás sikertelen."""

    pass


class InsufficientDiskSpaceError(StorageException):
    """Akkor dobódik, ha nincs elég lemezterület."""

    pass


class PermissionDeniedError(StorageException):
    """Akkor dobódik, ha a jogosultság megtagadva."""

    pass
