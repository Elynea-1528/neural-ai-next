# core/config/factory.py

Konfiguráció kezelő factory implementáció.

Ez a modul implementálja a ConfigManagerFactory osztályt, amely felelős a különböző
konfiguráció kezelők (YAML, dinamikus adatbázis-alapú) létrehozásáért és életciklusuk
kezeléséért. A factory támogatja a szinkron és aszinkron konfiguráció kezelőket is.

## Osztályok

### `ConfigManagerFactory`

Factory osztály konfiguráció kezelők létrehozásához.

    Ez az osztály felelős a különböző típusú konfiguráció kezelők létrehozásáért,
    regisztrálásáért és életciklusuk kezeléséért. Támogatja a szinkron (YAML fájl)
    és aszinkron (adatbázis-alapú dinamikus) konfiguráció kezelőket is.

    A factory alkalmazza a Dependency Injection elvet, és csak interfészeken keresztül
    kommunikál a konkrét implementációkkal.

    Attributes:
        _manager_types: Regisztrált szinkron konfiguráció kezelő típusok.
        _async_manager_types: Regisztrált aszinkron konfiguráció kezelő típusok.


## Függvények

### `_lazy_load_implementations`

Lazy betölti a konkrét implementációkat a körkörös importok elkerülésére.

        Ez a metódus biztosítja, hogy a konkrét implementációk csak akkor kerüljenek
        betöltésre, amikor valóban szükség van rájuk.

### `register_manager`

Új szinkron konfiguráció kezelő típus regisztrálása.

        Args:
            extension: A kezelt fájl kiterjesztése (pl: ".yml", ".json")
            manager_class: A kezelő osztály, amely implementálja a ConfigManagerInterface-t

        Raises:
            ValueError: Ha az extension vagy manager_class érvénytelen
            TypeError: Ha a manager_class nem megfelelő típusú

### `register_async_manager`

Új aszinkron konfiguráció kezelő típus regisztrálása.

        Args:
            manager_type: A kezelő típusának azonosítója (pl: "dynamic", "database")
            manager_class: A kezelő osztály, amely implementálja az AsyncConfigManagerInterface-t

        Raises:
            ValueError: Ha a manager_type érvénytelen
            TypeError: Ha a manager_class nem megfelelő típusú

### `get_manager`

Megfelelő szinkron konfiguráció kezelő létrehozása.

        A metódus a fájlnév kiterjesztése alapján automatikusan kiválasztja a
        megfelelő kezelőt, vagy a megadott típus alapján hozza létre a kezelőt.

        Args:
            filename: Konfigurációs fájl teljes neve (elérési úttal együtt)
            manager_type: Opcionális kezelő típus azonosító

        Returns:
            ConfigManagerInterface: A létrehozott konfiguráció kezelő példány

        Raises:
            ConfigLoadError: Ha nem található megfelelő kezelő
            ValueError: Ha a fájlnév kiterjesztése nem regisztrált

### `get_async_manager`

Aszinkron konfiguráció kezelő létrehozása.

        A metódus explicit típusmegadással hozza létre az aszinkron konfiguráció kezelőt,
        lehetővé téve a paraméterek átadását a konstruktornak.

        Args:
            manager_type: A kért kezelő típus azonosítója (pl: "dynamic", "database")
            session: Az adatbázis session (kötelező a DynamicConfigManager-hez)
            logger: Logger interfész a naplózásra (opcionális)
            **kwargs: További kulcsszavas argumentumok a kezelő konstruktorának

        Returns:
            AsyncConfigManagerInterface: A létrehozott aszinkron konfiguráció kezelő példány

        Raises:
            ConfigLoadError: Ha a megadott manager_type nem létezik
            ValueError: Ha a session nincs megadva, ahol az szükséges

### `create_manager`

Szinkron konfiguráció kezelő létrehozása típus alapján.

        A metódus explicit típusmegadással hozza létre a konfiguráció kezelőt,
        lehetővé téve a paraméterek átadását a konstruktornak.

        Args:
            manager_type: A kért kezelő típus azonosítója
            *args: Pozícionális argumentumok a kezelő konstruktorának
            **kwargs: Kulcsszavas argumentumok a kezelő konstruktorának

        Returns:
            ConfigManagerInterface: A létrehozott konfiguráció kezelő példány

        Raises:
            ConfigLoadError: Ha a megadott manager_type nem létezik

### `get_supported_extensions`

Támogatott fájl kiterjesztések lekérése.

        Returns:
            list[str]: A támogatott kiterjesztések listája

### `get_supported_async_types`

Támogatott aszinkron konfiguráció kezelő típusok lekérése.

        Returns:
            list[str]: A támogatott aszinkron típusok listája


---

**Forrásfájl:** [`core/config/factory.py`](../../../neural_ai/core/config/factory.py)
