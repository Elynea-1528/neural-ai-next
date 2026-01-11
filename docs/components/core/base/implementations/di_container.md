# core/base/implementations/di_container.py

Dependency injection konténer implementáció.

## Osztályok

### `LazyComponent[T]`

Lusta betöltésű komponensek wrapper osztálya.

    Ez az osztály biztosítja a komponensek lusta (lazy) betöltését,
    ami azt jelenti, hogy a komponens csak akkor jön létre, amikor
    először használják.

### `DIContainer`

Egyszerű dependency injection konténer.

    A konténer kezeli a komponensek közötti függőségeket és biztosítja
    azok megfelelő inicializálását.


## Függvények

### `__init__`

Konténer inicializálása.

### `register_instance`

Példány regisztrálása a konténerben.

        Args:
            interface: Az interfész típusa
            instance: Az interfészt megvalósító példány

### `register_factory`

Factory függvény regisztrálása a konténerben.

        Args:
            interface: Az interfész típusa
            factory: Az interfész implementációját létrehozó factory függvény

### `resolve`

Függőség feloldása.

        Args:
            interface: Az interfész típusa

        Returns:
            Az interfészhez tartozó példány vagy None

### `register_lazy`

Lusta betöltésű komponens regisztrálása.

        Args:
            component_name: A komponens neve
            factory_func: A komponenst létrehozó függvény

        Raises:
            ValueError: Ha a komponens név érvénytelen vagy a factory
                függvény nem hívható

### `get`

Komponens példány lekérése (lusta betöltés támogatással).

        Args:
            component_name: A lekérendő komponens neve

        Returns:
            A komponens példánya

        Raises:
            ComponentNotFoundError: Ha a komponens nem található

### `get_lazy_components`

A lusta komponensek státuszának lekérése.

        Returns:
            A dictionary where keys are component names and values
            indicate whether the component has been loaded

### `preload_components`

Preload specific components.

        Args:
            component_names: List of component names to preload

### `clear`

Konténer ürítése.

### `register`

Komponens példány regisztrálása.

        Args:
            component_name: A komponens neve
            instance: A regisztrálandó példány

        Raises:
            ValueError: Ha a component_name érvénytelen vagy az instance None
            SingletonViolationError: Ha a singleton minta megsértésre kerül

### `get_memory_usage`

Memória használat statisztikák lekérése.

### `_verify_singleton`

Singleton minta ellenőrzése.

        Args:
            instance: The instance to verify
            component_name: The name of the component

### `_enforce_singleton`

Singleton minta kényszerítése duplikált regisztráció megakadályozásával.

        Args:
            component_name: The name of the component
            instance: The instance being registered

        Raises:
            SingletonViolationError: If singleton pattern is violated


---

**Forrásfájl:** [`core/base/implementations/di_container.py`](../../../neural_ai/core/base/implementations/di_container.py)
