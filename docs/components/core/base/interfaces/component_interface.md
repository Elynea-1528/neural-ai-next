# core/base/interfaces/component_interface.py

Core komponens interfészek.

Ez a modul tartalmazza a core komponensekhez kapcsolódó interfészeket.

## Osztályok

### `CoreComponentsInterface`

Core komponensek interfész.

    Ez az interfész definiálja a core komponensek gyűjteményének
    alapvető funkcionalitását és hozzáférését.

### `CoreComponentFactoryInterface`

Core komponens factory interfész.

    Ez az interfész definiálja a core komponensek létrehozásáért
    és inicializálásáért felelős factory osztály alapvető funkcionalitását.


## Függvények

### `config`

Konfiguráció kezelő komponens.

        Returns:
            A konfiguráció kezelő komponens vagy None

### `logger`

Logger komponens.

        Returns:
            A logger komponens vagy None

### `storage`

Storage komponens.

        Returns:
            A storage komponens vagy None

### `has_config`

Ellenőrzi, hogy van-e konfigurációs komponens.

        Returns:
            True ha van konfigurációs komponens, különben False

### `has_logger`

Ellenőrzi, hogy van-e logger komponens.

        Returns:
            True ha van logger komponens, különben False

### `has_storage`

Ellenőrzi, hogy van-e storage komponens.

        Returns:
            True ha van storage komponens, különben False

### `validate`

Ellenőrzi, hogy minden szükséges komponens rendelkezésre áll-e.

        Returns:
            True ha minden komponens elérhető, különben False

### `create_components`

Core komponensek létrehozása és inicializálása.

        Args:
            config_path: Konfiguráció útvonala (opcionális)
            log_path: Log fájl útvonala (opcionális)
            storage_path: Storage alap útvonal (opcionális)

        Returns:
            Az inicializált komponensek

### `create_with_container`

Core komponensek létrehozása meglévő konténerből.

        Args:
            container: A dependency injection konténer

        Returns:
            Az inicializált komponensek

### `create_minimal`

Minimális core komponens készlet létrehozása alapértelmezett beállításokkal.

        Returns:
            Az alapértelmezett komponensek


---

**Forrásfájl:** [`core/base/interfaces/component_interface.py`](../../../neural_ai/core/base/interfaces/component_interface.py)
