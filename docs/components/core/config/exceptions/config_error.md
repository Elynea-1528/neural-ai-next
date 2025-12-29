# core/config/exceptions/config_error.py

Kivételek a konfigurációkezelő modulhoz.

Ez a modul definiálja a konfigurációkezelés során fellépő összes kivételt.
A kivételek hierarchikusan vannak szervezve, a ConfigError alaposztállyal
a gyökéren.

## Osztályok

### `ConfigError`

Alap kivétel a konfigurációkezelő hibákhoz.

    Ez az osztály szolgál közös alapként az összes konfigurációval
    kapcsolatos kivételnek a rendszerben.

    Attributes:
        message: A hibaüzenet részletes leírása.
        error_code: Opcionális hibakód a hibák kategorizálásához.

### `ConfigLoadError`

Konfiguráció betöltési hiba.

    Akkor dobódik, ha a konfigurációs fájl betöltése sikertelen.
    Ez tartalmazhat fájl nem található, olvasási hiba vagy formátum
    hiba esetét is.

    Attributes:
        file_path: Az érintett konfigurációs fájl elérési útja.
        original_error: Az eredeti kivétel, ami a hibát okozta.

### `ConfigSaveError`

Konfiguráció mentési hiba.

    Akkor dobódik, ha a konfiguráció mentése sikertelen.
    Ez tartalmazhat írási jogosultság hiányát, lemezterület hiányt
    vagy egyéb I/O hibákat.

    Attributes:
        file_path: A cél konfigurációs fájl elérési útja.
        original_error: Az eredeti kivétel, ami a hibát okozta.

### `ConfigValidationError`

Konfiguráció validációs hiba.

    Akkor dobódik, ha a konfigurációs adatok érvénytelenek vagy
    nem felelnek meg a várt sémának. Ez tartalmazhatja a kötelező
    mezők hiányát, érvénytelen értékeket vagy típus eltéréseket.

    Attributes:
        field_path: Az érintett konfigurációs mező elérési útja.
        invalid_value: Az érvénytelen érték, ami a hibát okozta.

### `ConfigTypeError`

Típus hiba a konfigurációban.

    Akkor dobódik, ha egy konfigurációs érték típusa nem megfelelő.
    Ez specifikusabb, mint a ConfigValidationError, mivel kizárólag
    a típus hibákra koncentrál.

    Attributes:
        field_path: Az érintett konfigurációs mező elérési útja.
        expected_type: A várt típus neve.
        actual_type: A tényleges típus neve.

### `ConfigKeyError`

Kulcs hiba a konfigurációban.

    Akkor dobódik, ha egy konfigurációs kulcs nem található vagy
    érvénytelen. Ez hasonlít a Python KeyError kivételéhez, de
    specifikusan a konfigurációkra van szabva.

    Attributes:
        key_path: A hiányzó vagy érvénytelen kulcs elérési útja.
        available_keys: A rendelkezésre álló kulcsok listája.


## Függvények

### `__init__`

Inicializálja a ConfigKeyError kivételt.

        Args:
            message: A hibaüzenet részletes leírása.
            key_path: A hiányzó vagy érvénytelen kulcs elérési útja.
            available_keys: A rendelkezésre álló kulcsok listája.


---

**Forrásfájl:** [`core/config/exceptions/config_error.py`](../../../neural_ai/core/config/exceptions/config_error.py)
