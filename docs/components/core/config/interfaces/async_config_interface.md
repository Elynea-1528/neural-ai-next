# core/config/interfaces/async_config_interface.py

Aszinkron konfiguráció kezelő interfész.

Ez az interfész definiálja az aszinkron konfigurációkezelők által implementálandó metódusokat,
különösen az adatbázis-alapú dinamikus konfigurációkezelőkhöz.

## Osztályok

### `AsyncConfigManagerInterface`

Aszinkron konfigurációkezelő interfész.

    Ez az interfész definiálja az aszinkron konfigurációkezelők által implementálandó metódusokat,
    amelyek főleg adatbázis-alapú dinamikus konfigurációkezelésre szolgálnak.


## Függvények

### `__init__`

Inicializálja az aszinkron konfigurációkezelőt.

        Args:
            filename: Konfigurációs fájl útvonala (opcionális, lehet None)
            session: Adatbázis session (opcionális)
            logger: Logger interfész (opcionális)

### `get`

Érték lekérése a konfigurációból.

        Args:
            *keys: A konfigurációs kulcs(ok) hierarchiája.
            default: Alapértelmezett érték, ha a kulcs nem található.

        Returns:
            A konfigurációs érték vagy az alapértelmezett érték.

### `get_section`

Teljes konfigurációs szekció lekérése.

        Args:
            section: A konfigurációs szekció/kategória neve.

        Returns:
            A szekció konfigurációs adatai.

        Raises:
            KeyError: Ha a szekció nem található.

### `set`

Érték beállítása a konfigurációban.

        Args:
            *keys: A konfigurációs kulcs(ok) hierarchiája.
            value: A beállítandó érték.

        Raises:
            ValueError: Ha érvénytelen a kulcs vagy érték.

### `save`

Konfiguráció mentése.

        Args:
            filename: A mentési cél (opcionális, implementációfüggő).

        Raises:
            NotImplementedError: Ha a művelet nem támogatott.

### `load`

Konfiguráció betöltése.

        Args:
            filename: A betöltési forrás.

        Raises:
            NotImplementedError: Ha a művelet nem támogatott.

### `load_directory`

Betölti az összes konfigurációs fájlt egy mappából.

        Args:
            path: A konfigurációs mappa útvonala.

        Raises:
            NotImplementedError: Ha a művelet nem támogatott.

### `validate`

Konfiguráció validálása séma alapján.

        Args:
            schema: A validáláshoz használt séma.

        Returns:
            Tuple[bool, dict[str, str] | None]: (sikeres-e a validáció, hibák dictionary vagy None)

### `add_listener`

Listener hozzáadása konfiguráció változásokhoz.

        Args:
            callback: A callback függvény, amelyet hívni kell a változás esetén.

### `remove_listener`

Listener eltávolítása.

        Args:
            callback: Az eltávolítandó callback függvény.

### `start_hot_reload`

Hot reload indítása (háttérben fut).

        Args:
            interval: Az ellenőrzési időköz másodpercben.

        Raises:
            RuntimeError: Ha a hot reload már fut.

### `stop_hot_reload`

Hot reload leállítása.

### `get_all`

Összes konfiguráció lekérdezése.

        Args:
            category: Opcionális kategória szűréshez.

        Returns:
            Szótár az összes (vagy kategóriához tartozó) konfigurációval.

### `set_with_metadata`

Konfiguráció beállítása metaadatokkal.

        Args:
            key: A konfigurációs kulcs.
            value: A konfigurációs érték.
            category: A konfiguráció kategóriája.
            description: A konfiguráció leírása.
            is_active: A konfiguráció aktív-e.

### `delete`

Konfiguráció törlése (soft delete).

        Args:
            key: A törlendő konfigurációs kulcs.

        Returns:
            True ha a konfiguráció törölve lett, False ha nem található.


---

**Forrásfájl:** [`core/config/interfaces/async_config_interface.py`](../../../neural_ai/core/config/interfaces/async_config_interface.py)
