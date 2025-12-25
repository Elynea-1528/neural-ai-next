"""Logger komponens kivételei.

Ez a modul tartalmazza a logger komponenshez tartozó kivételeket.
"""


class LoggerError(Exception):
    """Alap kivétel a logger komponenshez."""

    pass


class LoggerConfigurationError(LoggerError):
    """Logger konfigurációs hiba."""

    pass


class LoggerInitializationError(LoggerError):
    """Logger inicializálási hiba."""

    pass
