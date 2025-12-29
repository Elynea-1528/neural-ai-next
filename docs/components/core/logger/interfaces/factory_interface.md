# core/logger/interfaces/factory_interface.py

Logger factory interfész.

Ez az interfész definiálja a logger factory-k alapvető működését,
beleértve a logger típusok regisztrálását, példányosítását és
a logger rendszer konfigurálását.

## Osztályok

### `LoggerFactoryInterface`

Logger factory interfész.

    Az interfész lehetővé teszi különböző logger implementációk
    dinamikus regisztrálását és példányosítását factory pattern
    segítségével.


## Függvények

### `register_logger`

Új logger típus regisztrálása a factory számára.

        Args:
            logger_type: A logger típus egyedi azonosítója
            logger_class: A logger osztály, amely implementálja a LoggerInterface-t

        Raises:
            ValueError: Ha a logger_type már létezik
            TypeError: Ha a logger_class nem implementálja a LoggerInterface-t

### `get_logger`

Logger példány létrehozása vagy visszaadása.

        Args:
            name: A logger egyedi neve
            logger_type: A kért logger típus (alapértelmezett: "default")
            **kwargs: További paraméterek a logger inicializálásához

        Returns:
            LoggerInterface: Az inicializált logger példány

        Raises:
            KeyError: Ha a logger_type nincs regisztrálva
            ValueError: Ha a name üres string

### `configure`

Logger rendszer konfigurálása.

        Args:
            config: Konfigurációs beállítások dictionary formátumban

        Raises:
            ValueError: Ha a konfiguráció érvénytelen


---

**Forrásfájl:** [`core/logger/interfaces/factory_interface.py`](../../../neural_ai/core/logger/interfaces/factory_interface.py)
