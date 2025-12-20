"""MT5 collector komponens kivételek."""

from neural_ai.core.base.exceptions import (
    ConnectionError,
    NetworkException,
    TimeoutError,
)


class MT5Exception(NetworkException):
    """Alap kivétel MT5-rel kapcsolatos hibákhoz."""

    pass


class MT5ConnectionError(ConnectionError):
    """Akkor dobódik, ha az MT5 kapcsolat sikertelen."""

    pass


class MT5TimeoutError(TimeoutError):
    """Akkor dobódik, ha az MT5 művelet időtúllépés miatt sikertelen."""

    pass


class MT5DataValidationError(MT5Exception):
    """Akkor dobódik, ha az adatvalidálás sikertelen."""

    pass


class MT5InitializationError(MT5Exception):
    """Akkor dobódik, ha az MT5 inicializálása sikertelen."""

    pass


class MT5SocketError(MT5ConnectionError):
    """Akkor dobódik, ha az MT5 socket integritása sérül."""

    pass
