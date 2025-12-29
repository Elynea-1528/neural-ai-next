# core/logger/interfaces/logger_interface.py

Logger interfész definíció a naplózási rendszer számára.

## Osztályok

### `LoggerInterface`

Logger interfész a naplózási műveletek absztrakt definíciójához.

    Ez az interfész definiálja azokat a metódusokat, amelyeket minden logger
    implementációnak implementálnia kell a konzisztens naplózási viselkedés
    érdekében.


## Függvények

### `__init__`

Logger inicializálása.

        Args:
            name: A logger egyedi azonosítója.
            config: Opcionális konfigurációs interfész a logger beállításaihoz.
            **kwargs: További opcionális paraméterek (pl. file_path, level).

### `debug`

Debug szintű üzenet naplózása.

        Részletes hibakeresési információk naplózására szolgál, amelyek általában
        csak fejlesztés közben relevánsak.

        Args:
            message: A naplózandó üzenet szövege.
            **kwargs: További kontextusparaméterek (pl. extra, exc_info).

### `info`

Információs szintű üzenet naplózása.

        Általános információk naplózására szolgál, amelyek a rendszer normál
        működéséről adnak tájékoztatást.

        Args:
            message: A naplózandó üzenet szövege.
            **kwargs: További kontextusparaméterek (pl. extra, exc_info).

### `warning`

Figyelmeztető szintű üzenet naplózása.

        Olyan helyzetek naplózására szolgál, amelyek nem kritikusak, de
        figyelmet igényelnek.

        Args:
            message: A naplózandó üzenet szövege.
            **kwargs: További kontextusparaméterek (pl. extra, exc_info).

### `error`

Hiba szintű üzenet naplózása.

        Hibák naplózására szolgál, amelyek befolyásolják a rendszer működését,
        de nem okoznak alkalmazásleállást.

        Args:
            message: A naplózandó üzenet szövege.
            **kwargs: További kontextusparaméterek (pl. extra, exc_info).

### `critical`

Kritikus szintű üzenet naplózása.

        Súlyos hibák naplózására szolgál, amelyek alkalmazásleállást okozhatnak.

        Args:
            message: A naplózandó üzenet szövege.
            **kwargs: További kontextusparaméterek (pl. extra, exc_info).

### `set_level`

Logger naplózási szintjének beállítása.

        Beállítja a minimális naplózási szintet. A szintnél alacsonyabb
        prioritású üzenetek nem lesznek naplózva.

        Args:
            level: Az új naplózási szint (0-50 közötti egész szám).

### `get_level`

Aktuális naplózási szint lekérdezése.

        Returns:
            int: A jelenleg beállított naplózási szint értéke.


---

**Forrásfájl:** [`core/logger/interfaces/logger_interface.py`](../../../neural_ai/core/logger/interfaces/logger_interface.py)
