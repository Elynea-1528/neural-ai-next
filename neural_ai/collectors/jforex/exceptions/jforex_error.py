"""JForex Collector Exceptions."""


class JForexError(Exception):
    """Alap kivétel minden JForex Collector hibához."""

    pass


class DownloadError(JForexError):
    """Adat letöltési hiba esetén dobódik.

    Ide tartoznak a hálózati hibák, szerverhibák és időtúllépések.
    """

    pass


class DecodeError(JForexError):
    """.bi5 adat dekódolási hiba esetén dobódik.

    Ide tartoznak az LZMA dekompressziós hibák és a struct kicsomagolási hibák.
    """

    pass


class DataNotAvailableError(JForexError):
    """A kért dátumhoz nem elérhető adat esetén dobódik.

    Ez általában hétvégéken, ünnepeken vagy amikor a piac zárva volt történik.
    """

    pass
