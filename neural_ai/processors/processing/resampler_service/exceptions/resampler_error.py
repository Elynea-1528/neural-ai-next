"""ResamplerService kivételek."""


from neural_ai.core.base.exceptions.base_error import NeuralAIException


class ResamplerError(NeuralAIException):
    """Alapértelmezett hiba a ResamplerService-hez."""

    def __init__(
        self,
        message: str,
        details: str | None = None,
        original_error: Exception | None = None
    ):
        """ResamplerError inicializálása.

        Args:
            message: A hibaüzenet
            details: Részletes hibainformációk
            original_error: Az eredeti kivétel (ha van)
        """
        super().__init__(message)
        self.details = details
        self.original_error = original_error
        self.component = "ResamplerService"


class DataLoadError(ResamplerError):
    """Hiba adatok betöltése során."""

    def __init__(
        self,
        symbol: str,
        start: str,
        end: str,
        original_error: Exception | None = None
    ):
        """DataLoadError inicializálása.

        Args:
            symbol: A kereskedési szimbólum
            start: A kezdő időpont
            end: A záró időpont
            original_error: Az eredeti kivétel
        """
        message = f"Adatok betöltése sikertelen a(z) {symbol} szimbólumhoz"
        details = f"Időintervallum: {start} - {end}"
        super().__init__(
            message=message,
            details=details,
            original_error=original_error
        )


class ResamplingError(ResamplerError):
    """Hiba az adatok átalakítása (resampling) során."""

    def __init__(
        self,
        symbol: str,
        timeframe: str,
        original_error: Exception | None = None
    ):
        """ResamplingError inicializálása.

        Args:
            symbol: A kereskedési szimbólum
            timeframe: Az időkeret
            original_error: Az eredeti kivétel
        """
        message = f"Az adatok átalakítása sikertelen a(z) {symbol} szimbólumhoz"
        details = f"Időkeret: {timeframe}"
        super().__init__(
            message=message,
            details=details,
            original_error=original_error
        )


class InvalidTimeframeError(ResamplerError):
    """Hiba érvénytelen időkeret esetén."""

    def __init__(self, timeframe: str):
        """InvalidTimeframeError inicializálása.

        Args:
            timeframe: Az érvénytelen időkeret
        """
        message = f"Érvénytelen időkeret: {timeframe}"
        details = (
            "Az időkeretnek a Pandas offset formátumban kell lennie "
            "(pl. '1m', '5m', '1h', '1D')"
        )
        super().__init__(message=message, details=details)
