"""Kivételek a konfigurációkezelő modulhoz.

Ez a modul definiálja a konfigurációkezelés során fellépő összes kivételt.
A kivételek hierarchikusan vannak szervezve, a ConfigError alaposztállyal
a gyökéren.
"""


class ConfigError(Exception):
    """Alap kivétel a konfigurációkezelő hibákhoz.

    Ez az osztály szolgál közös alapként az összes konfigurációval
    kapcsolatos kivételnek a rendszerben.

    Attributes:
        message: A hibaüzenet részletes leírása.
        error_code: Opcionális hibakód a hibák kategorizálásához.
    """

    def __init__(self, message: str, error_code: str | None = None) -> None:
        """Inicializálja a ConfigError kivételt.

        Args:
            message: A hibaüzenet részletes leírása.
            error_code: Opcionális hibakód a hibák kategorizálásához.
        """
        self.error_code = error_code
        super().__init__(message)


class ConfigLoadError(ConfigError):
    """Konfiguráció betöltési hiba.

    Akkor dobódik, ha a konfigurációs fájl betöltése sikertelen.
    Ez tartalmazhat fájl nem található, olvasási hiba vagy formátum
    hiba esetét is.

    Attributes:
        file_path: Az érintett konfigurációs fájl elérési útja.
        original_error: Az eredeti kivétel, ami a hibát okozta.
    """

    def __init__(
        self, message: str, file_path: str | None = None, original_error: Exception | None = None
    ) -> None:
        """Inicializálja a ConfigLoadError kivételt.

        Args:
            message: A hibaüzenet részletes leírása.
            file_path: Az érintett konfigurációs fájl elérési útja.
            original_error: Az eredeti kivétel, ami a hibát okozta.
        """
        self.file_path = file_path
        self.original_error = original_error
        super().__init__(message, error_code="CONFIG_LOAD_ERROR")


class ConfigSaveError(ConfigError):
    """Konfiguráció mentési hiba.

    Akkor dobódik, ha a konfiguráció mentése sikertelen.
    Ez tartalmazhat írási jogosultság hiányát, lemezterület hiányt
    vagy egyéb I/O hibákat.

    Attributes:
        file_path: A cél konfigurációs fájl elérési útja.
        original_error: Az eredeti kivétel, ami a hibát okozta.
    """

    def __init__(
        self, message: str, file_path: str | None = None, original_error: Exception | None = None
    ) -> None:
        """Inicializálja a ConfigSaveError kivételt.

        Args:
            message: A hibaüzenet részletes leírása.
            file_path: A cél konfigurációs fájl elérési útja.
            original_error: Az eredeti kivétel, ami a hibát okozta.
        """
        self.file_path = file_path
        self.original_error = original_error
        super().__init__(message, error_code="CONFIG_SAVE_ERROR")


class ConfigValidationError(ConfigError):
    """Konfiguráció validációs hiba.

    Akkor dobódik, ha a konfigurációs adatok érvénytelenek vagy
    nem felelnek meg a várt sémának. Ez tartalmazhatja a kötelező
    mezők hiányát, érvénytelen értékeket vagy típus eltéréseket.

    Attributes:
        field_path: Az érintett konfigurációs mező elérési útja.
        invalid_value: Az érvénytelen érték, ami a hibát okozta.
    """

    def __init__(
        self, message: str, field_path: str | None = None, invalid_value: object | None = None
    ) -> None:
        """Inicializálja a ConfigValidationError kivételt.

        Args:
            message: A hibaüzenet részletes leírása.
            field_path: Az érintett konfigurációs mező elérési útja.
            invalid_value: Az érvénytelen érték, ami a hibát okozta.
        """
        self.field_path = field_path
        self.invalid_value = invalid_value
        super().__init__(message, error_code="CONFIG_VALIDATION_ERROR")


class ConfigTypeError(ConfigError):
    """Típus hiba a konfigurációban.

    Akkor dobódik, ha egy konfigurációs érték típusa nem megfelelő.
    Ez specifikusabb, mint a ConfigValidationError, mivel kizárólag
    a típus hibákra koncentrál.

    Attributes:
        field_path: Az érintett konfigurációs mező elérési útja.
        expected_type: A várt típus neve.
        actual_type: A tényleges típus neve.
    """

    def __init__(
        self,
        message: str,
        field_path: str | None = None,
        expected_type: str | None = None,
        actual_type: str | None = None,
    ) -> None:
        """Inicializálja a ConfigTypeError kivételt.

        Args:
            message: A hibaüzenet részletes leírása.
            field_path: Az érintett konfigurációs mező elérési útja.
            expected_type: A várt típus neve.
            actual_type: A tényleges típus neve.
        """
        self.field_path = field_path
        self.expected_type = expected_type
        self.actual_type = actual_type
        super().__init__(message, error_code="CONFIG_TYPE_ERROR")


class ConfigKeyError(ConfigError):
    """Kulcs hiba a konfigurációban.

    Akkor dobódik, ha egy konfigurációs kulcs nem található vagy
    érvénytelen. Ez hasonlít a Python KeyError kivételéhez, de
    specifikusan a konfigurációkra van szabva.

    Attributes:
        key_path: A hiányzó vagy érvénytelen kulcs elérési útja.
        available_keys: A rendelkezésre álló kulcsok listája.
    """

    def __init__(
        self, message: str, key_path: str | None = None, available_keys: list[str] | None = None
    ) -> None:
        """Inicializálja a ConfigKeyError kivételt.

        Args:
            message: A hibaüzenet részletes leírása.
            key_path: A hiányzó vagy érvénytelen kulcs elérési útja.
            available_keys: A rendelkezésre álló kulcsok listája.
        """
        self.key_path = key_path
        self.available_keys = available_keys or []
        super().__init__(message, error_code="CONFIG_KEY_ERROR")
