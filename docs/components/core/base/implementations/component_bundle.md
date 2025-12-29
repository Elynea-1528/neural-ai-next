# core/base/implementations/component_bundle.py

Core komponensek gyűjtemény.

## Osztályok

### `CoreComponents`

Alap komponensek lusta betöltéssel.


## Függvények

### `__init__`

Alap komponensek inicializálása.

        Args:
            container: Egy függőséginjektáló konténer példány.
                       Ha nincs megadva, új konténert hoz létre.

### `config`

Konfiguráció kezelő komponens lekérése.

        Returns:
            A konfiguráció kezelő példánya, vagy None ha nincs regisztrálva.

### `logger`

Naplózó komponens lekérése.

        Returns:
            A naplózó példánya, vagy None ha nincs regisztrálva.

### `storage`

Tároló komponens lekérése.

        Returns:
            A tároló példánya, vagy None ha nincs regisztrálva.

### `database`

Adatbázis komponens lekérése.

        Returns:
            Az adatbázis példánya, vagy None ha nincs regisztrálva.

### `event_bus`

Esemény busz komponens lekérése.

        Returns:
            Az esemény busz példánya, vagy None ha nincs regisztrálva.

### `hardware`

Hardver információ komponens lekérése.

        Returns:
            A hardver információ példánya, vagy None ha nincs regisztrálva.

### `set_config`

Beállítja a konfiguráció komponenst (csak teszteléshez).

        Args:
            config: A konfiguráció kezelő implementáció példánya.

### `set_logger`

Beállítja a naplózó komponenst (csak teszteléshez).

        Args:
            logger: A naplózó implementáció példánya.

### `set_storage`

Beállítja a tároló komponenst (csak teszteléshez).

        Args:
            storage: A tároló implementáció példánya.

### `set_database`

Beállítja az adatbázis komponenst (csak teszteléshez).

        Args:
            database: Az adatbázis implementáció példánya.

### `set_event_bus`

Beállítja az esemény busz komponenst (csak teszteléshez).

        Args:
            event_bus: Az esemény busz implementáció példánya.

### `set_hardware`

Beállítja a hardver információ komponenst (csak teszteléshez).

        Args:
            hardware: A hardver információ implementáció példánya.

### `has_config`

Ellenőrzi, hogy van-e config komponens.

        Returns:
            bool: True ha van config komponens, False ha nincs

### `has_logger`

Ellenőrzi, hogy van-e logger komponens.

        Returns:
            bool: True ha van logger komponens, False ha nincs

### `has_storage`

Ellenőrzi, hogy van-e storage komponens.

        Returns:
            bool: True ha van storage komponens, False ha nincs

### `has_database`

Ellenőrzi, hogy van-e database komponens.

        Returns:
            bool: True ha van database komponens, False ha nincs

### `has_event_bus`

Ellenőrzi, hogy van-e event_bus komponens.

        Returns:
            bool: True ha van event_bus komponens, False ha nincs

### `has_hardware`

Ellenőrzi, hogy van-e hardware komponens.

        Returns:
            bool: True ha van hardware komponens, False ha nincs

### `validate`

Ellenőrzi, hogy minden szükséges komponens megvan-e.

        Returns:
            bool: True ha minden komponens megvan, False ha valamelyik hiányzik


---

**Forrásfájl:** [`core/base/implementations/component_bundle.py`](../../../neural_ai/core/base/implementations/component_bundle.py)
