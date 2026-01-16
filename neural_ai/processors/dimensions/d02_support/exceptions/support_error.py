"""Kivételek a D02 Support/Resistance processzor modulhoz.

Ez a modul definiálja a support/resistance szintek számítása során
fellépő összes kivételt.
"""


class SupportError(Exception):
    """Alap kivétel a support/resistance processzor hibákhoz.

    Ez az osztály szolgál közös alapként az összes support/resistance
    számítással kapcsolatos kivételnek a rendszerben.

    Attributes:
        message: A hibaüzenet részletes leírása.
        error_code: Opcionális hibakód a hibák kategorizálásához.
    """

    def __init__(self, message: str, error_code: str | None = None) -> None:
        """Inicializálja a SupportError kivételt.

        Args:
            message: A hibaüzenet részletes leírása.
            error_code: Opcionális hibakód a hibák kategorizálásához.
        """
        self.error_code = error_code
        super().__init__(message)


class SwingPointCalculationError(SupportError):
    """Swing pont számítási hiba.

    Akkor dobódik, ha a swing high vagy swing low pontok számítása
    sikertelen. Ez tartalmazhatja a rolling window műveletek hibáit
    vagy érvénytelen adatokat.

    Attributes:
        window_size: A használt rolling window mérete.
        column_name: Az érintett oszlop neve.
    """

    def __init__(
        self, message: str, window_size: int | None = None, column_name: str | None = None
    ) -> None:
        """Inicializálja a SwingPointCalculationError kivételt.

        Args:
            message: A hibaüzenet részletes leírása.
            window_size: A használt rolling window mérete.
            column_name: Az érintett oszlop neve.
        """
        self.window_size = window_size
        self.column_name = column_name
        super().__init__(message, error_code="SWING_POINT_CALCULATION_ERROR")


class SupportResistanceLevelError(SupportError):
    """Support/Resistance szint számítási hiba.

    Akkor dobódik, ha a support vagy resistance szintek aggregálása
    sikertelen. Ez tartalmazhatja az átlagolási műveletek hibáit
    vagy érvénytelen swing pont adatokat.

    Attributes:
        level_type: A szint típusa ("support" vagy "resistance").
        aggregation_method: A használt aggregációs módszer.
    """

    def __init__(
        self, message: str, level_type: str | None = None, aggregation_method: str | None = None
    ) -> None:
        """Inicializálja a SupportResistanceLevelError kivételt.

        Args:
            message: A hibaüzenet részletes leírása.
            level_type: A szint típusa ("support" vagy "resistance").
            aggregation_method: A használt aggregációs módszer.
        """
        self.level_type = level_type
        self.aggregation_method = aggregation_method
        super().__init__(message, error_code="SUPPORT_RESISTANCE_LEVEL_ERROR")


class TimeframeConfigurationError(SupportError):
    """Timeframe konfigurációs hiba.

    Akkor dobódik, ha a timeframe-specifikus konfiguráció érvénytelen
    vagy hiányzik. Ez tartalmazhatja a swing_window vagy min_distance
    paraméterek hibás értékeit.

    Attributes:
        timeframe: Az érintett timeframe.
        config_key: A hiányzó vagy érvénytelen konfigurációs kulcs.
    """

    def __init__(
        self, message: str, timeframe: str | None = None, config_key: str | None = None
    ) -> None:
        """Inicializálja a TimeframeConfigurationError kivételt.

        Args:
            message: A hibaüzenet részletes leírása.
            timeframe: Az érintett timeframe.
            config_key: A hiányzó vagy érvénytelen konfigurációs kulcs.
        """
        self.timeframe = timeframe
        self.config_key = config_key
        super().__init__(message, error_code="TIMEFRAME_CONFIGURATION_ERROR")
