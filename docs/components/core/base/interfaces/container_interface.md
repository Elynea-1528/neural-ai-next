# core/base/interfaces/container_interface.py

Dependency injection konténer interfészek.

Ez a modul tartalmazza a DI konténerhez és lusta betöltéshez kapcsolódó interfészeket.

## Osztályok

### `DIContainerInterface`

Dependency injection konténer interfész.

    Ez az interfész definiálja a dependency injection konténer alapvető
    funkcionalitását, amely a komponensek közötti függőségek kezelését biztosítja.

### `LazyComponentInterface`

Lusta betöltésű komponens interfész.

    Ez az interfész definiálja a lusta (lazy) betöltésű komponensek
    alapvető funkcionalitását.


## Függvények

### `register_instance`

Komponens példány regisztrálása a konténerben.

        Args:
            interface: Az interfész típusa, amihez a példányt regisztráljuk
            instance: A regisztrálandó példány

### `register_factory`

Factory függvény regisztrálása a konténerben.

        Args:
            interface: Az interfész típusa, amihez a factory-t regisztráljuk
            factory: A factory függvény, ami létrehozza az implementációt

### `resolve`

Függőség feloldása a konténerből.

        Args:
            interface: Az interfész típusa, amit fel szeretnénk oldani

        Returns:
            A regisztrált példány vagy None ha nem található

### `register_lazy`

Lusta betöltésű komponens regisztrálása.

        Args:
            component_name: A komponens neve
            factory_func: A komponens létrehozásához használt factory függvény

        Raises:
            ValueError: Ha a komponens név érvénytelen vagy a factory függvény nem hívható

### `get`

Komponens példány lekérése (lusta betöltéssel).

        Returns:
            A komponens példánya

### `clear`

Konténer ürítése.

### `is_loaded`

Ellenőrzi, hogy a komponens betöltődött-e már.

        Returns:
            True, ha a komponens már betöltődött, egyébként False


---

**Forrásfájl:** [`core/base/interfaces/container_interface.py`](../../../neural_ai/core/base/interfaces/container_interface.py)
