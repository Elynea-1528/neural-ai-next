# core/config/implementations/dynamic_config_manager.py

Dinamikus konfiguráció kezelő implementáció.

Ez a modul implementálja a DynamicConfigManager osztályt, amely a futás közben
módosítható konfigurációkat kezeli SQL adatbázisban tárolva, hot reload támogatással.

## Osztályok

### `DynamicConfigManager`

Dinamikus konfiguráció kezelő SQL adatbázissal.

    Ez az osztály kezeli a futás közben módosítható konfigurációkat, amelyek
    hot reload támogatással rendelkeznek. A konfigurációk SQL adatbázisban
    tárolódnak, és változásukról a rendszer azonnal értesítést kap.

    Attributes:
        session: Az adatbázis session (Dependency Injection).
        logger: Logger interfész a naplózásra (opcionális).
        _cache: Konfigurációs értékek gyorsítótára.
        _listeners: Konfiguráció változásokat figyelő callback-ek listája.
        _last_update: Az utolsó frissítés időpontja.
        _hot_reload_task: A háttérben futó hot reload task referenciája.
        _stop_hot_reload: Esemény a hot reload leállításához.


## Függvények

### `__init__`

Inicializálja a DynamicConfigManager-t.

        Args:
            filename: Nincs használatban, csak a kompatibilitás miatt (deprecated).
            session: Az adatbázis session (kötelező a működéshez).
            logger: Logger interfész a naplózásra (opcionális).

        Raises:
            ValueError: Ha nincs megadva session.

### `get`

Konfigurációs érték lekérdezése.

        Args:
            *keys: A konfigurációs kulcs(ok) hierarchiája. Csak egy kulcs támogatott.
            default: Alapértelmezett érték, ha a kulcs nem található.

        Returns:
            A konfigurációs érték vagy az alapértelmezett érték.

        Raises:
            ValueError: Ha több kulcsot adnak meg.

### `set`

Konfigurációs érték beállítása.

        Args:
            *keys: A konfigurációs kulcs(ok) hierarchiája. Csak egy kulcs támogatott.
            value: A beállítandó érték.

        Raises:
            ValueError: Ha több kulcsot adnak meg vagy érvénytelen az érték.

### `get_section`

Teljes konfigurációs szekció lekérése kategória alapján.

        Args:
            section: A konfigurációs kategória neve.

        Returns:
            A kategóriához tartozó összes konfigurációs érték.

        Raises:
            KeyError: Ha a kategória nem található vagy nincs aktív konfiguráció.

### `save`

Konfiguráció mentése (nincs értelmezve dinamikus konfigurációnál).

        A DynamicConfigManager nem támogatja a fájlba mentést, mivel az adatbázisban tárol.
        Ez a metódus csak a kompatibilitás miatt van jelen.

        Args:
            filename: Nincs használatban.

        Raises:
            NotImplementedError: Mindig, mivel nem támogatott művelet.

### `load`

Konfiguráció betöltése (nincs értelmezve dinamikus konfigurációnál).

        A DynamicConfigManager nem támogatja a fájlból betöltést, mivel az adatbázisból olvas.
        Ez a metódus csak a kompatibilitás miatt van jelen.

        Args:
            filename: Nincs használatban.

        Raises:
            NotImplementedError: Mindig, mivel nem támogatott művelet.

### `load_directory`

Konfigurációs mappa betöltése (nincs értelmezve dinamikus konfigurációnál).

        A DynamicConfigManager nem támogatja a mappából betöltést.
        Ez a metódus csak a kompatibilitás miatt van jelen.

        Args:
            path: Nincs használatban.

        Raises:
            NotImplementedError: Mindig, mivel nem támogatott művelet.

### `validate`

Konfiguráció validálása séma alapján.

        Args:
            schema: A validáláshoz használt séma.

        Returns:
            Tuple[bool, dict[str, str] | None]: (sikeres-e a validáció, hibák dictionary vagy None)

        Note:
            A validáció jelenleg csak a cache-ben lévő értékeket ellenőrzi.

### `add_listener`

Listener hozzáadása konfiguráció változásokhoz.

        Args:
            callback: A callback függvény, amelyet hívni kell a változás esetén.
                     A callbacknek két paramétert kell fogadnia: (key, value).

### `remove_listener`

Listener eltávolítása.

        Args:
            callback: Az eltávolítandó callback függvény.

### `start_hot_reload`

Hot reload indítása (háttérben fut).

        A hot reload rendszeres időközönként ellenőrzi az adatbázist
        konfigurációs változásokért, és frissíti a cache-t.

        Args:
            interval: Az ellenőrzési időköz másodpercben (alapértelmezett: 5.0).

        Raises:
            RuntimeError: Ha a hot reload már fut.

### `_hot_reload_loop`

A hot reload fő ciklusa.

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
            category: A konfiguráció kategóriája (alapértelmezett: "system").
            description: A konfiguráció leírása (opcionális).
            is_active: A konfiguráció aktív-e (alapértelmezett: True).

### `delete`

Konfiguráció törlése (soft delete: is_active = False).

        Args:
            key: A törlendő konfigurációs kulcs.

        Returns:
            True ha a konfiguráció törölve lett, False ha nem található.

        Raises:
            ConfigError: Ha hiba történik a törlés során.

### `_notify_listeners`

Listener-ek értesítése konfiguráció változásról.

        Args:
            key: A megváltozott konfigurációs kulcs.
            value: Az új konfigurációs érték.

### `_check_for_updates`

Ellenőrzi, hogy történt-e változás az adatbázisban.

### `_determine_value_type`

Érték típusának meghatározása.

        Args:
            value: Az ellenőrizendő érték.

        Returns:
            Az érték típusa string formátumban.


---

**Forrásfájl:** [`core/config/implementations/dynamic_config_manager.py`](../../../neural_ai/core/config/implementations/dynamic_config_manager.py)
