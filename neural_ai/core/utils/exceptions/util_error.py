"""Util-specifikus kivételek.

Ez a modul tartalmazza az összes utility-műveletekhez kapcsolódó kivételeket.
"""

from neural_ai.core.base.exceptions import NeuralAIException


class UtilError(NeuralAIException):
    """Általános utility hiba."""

    def __init__(self, message: str, details: str | None = None) -> None:
        """Inicializálja a UtilError kivételt.

        Args:
            message: A hibaüzenet.
            details: Opcionális részletes leírás a hibáról.
        """
        super().__init__(message)
        self.details = details


class HardwareDetectionError(UtilError):
    """Hardver detektálási hiba."""

    def __init__(self, message: str, hardware_type: str | None = None) -> None:
        """Inicializálja a HardwareDetectionError kivételt.

        Args:
            message: A hibaüzenet.
            hardware_type: A hardver típusa, amelynek detektálása során hiba történt.
        """
        super().__init__(message)
        self.hardware_type = hardware_type
