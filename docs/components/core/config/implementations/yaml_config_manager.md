# core/config/implementations/yaml_config_manager.py

YAML alapú konfigurációkezelő implementáció.

## Osztályok

### `ValidationContext`

Séma validációs kontextus.

    Ez az osztály tartalmazza a validációs folyamat során szükséges adatokat.

### `YAMLConfigManager`

YAML fájlokat kezelő konfigurációkezelő.

    A konfigurációk mentésekor automatikusan hozzáadja a schema_version-t,
    és betöltéskor ellenőrzi a kompatibilitást.


## Függvények

### `__init__`

Inicializálja a YAML konfigurációkezelőt.

        Args:
            filename: Konfigurációs fájl útvonala (opcionális)
            logger: Logger interfész a naplózásra (opcionális)
            storage: Storage interfész a perzisztens tárolásra (opcionális)

### `_get_current_schema_version`

Visszaadja a jelenlegi séma verzióját.

        Returns:
            str: A jelenlegi séma verziója

### `_check_schema_compatibility`

Ellenőrzi a betöltött séma kompatibilitását.

        Args:
            loaded_version: A betöltött konfiguráció séma verziója

        Returns:
            bool: True ha kompatibilis, False egyébként

### `_ensure_dict`

Adatok dictionary típusának biztosítása.

        Args:
            data: Ellenőrizendő adatok

        Returns:
            Dict[str, Any]: Az adatok dictionary formátumban

        Raises:
            ConfigLoadError: Ha az adatok nem None és nem dictionary

### `get`

Érték lekérése a konfigurációból.

        Args:
            *keys: A konfigurációs kulcsok hierarchiája
            default: Alapértelmezett érték, ha a kulcs nem található

        Returns:
            A konfigurációs érték vagy az alapértelmezett érték

### `get_section`

Teljes konfigurációs szekció lekérése.

        Args:
            section: A szekció neve

        Returns:
            A szekció konfigurációs adatai

        Raises:
            KeyError: Ha a szekció nem található

### `set`

Érték beállítása a konfigurációban.

        Args:
            *keys: A konfigurációs kulcsok hierarchiája
            value: A beállítandó érték

        Raises:
            ValueError: Ha nincs kulcs megadva vagy érvénytelen hierarchia

### `save`

Aktuális konfiguráció mentése fájlba.

        A konfiguráció mentésekor automatikusan hozzáadja a schema_version-t,
        hogy a jövőbeli betöltések kompatibilitást ellenőrizhessenek.

        Args:
            filename: A mentési fájl neve (opcionális, alapértelmezett az eredeti fájlnév)

        Raises:
            ValueError: Ha nincs fájlnév megadva vagy mentési hiba történik

### `load`

Konfiguráció betöltése fájlból.

        A betöltés során ellenőrzi a séma verzió kompatibilitást, ha a fájl
        tartalmaz verzióinformációt.

        Args:
            filename: A betöltendő fájl neve

        Raises:
            ConfigLoadError: Ha a fájl nem található vagy betöltési hiba történik

### `validate`

Konfiguráció validálása séma alapján.

        Args:
            schema: A validációs séma definíció

        Returns:
            Tuple[bool, dict[str, str] | None]: (sikeres-e a validáció, hibák dictionary vagy None)

### `_validate_dict`

Rekurzív séma validáció.

        Args:
            ctx: Validációs kontextus a konfigurációs adatokkal

### `_validate_required`

Kötelező mező ellenőrzése.

        Args:
            ctx: Validációs kontextus

        Returns:
            bool: True ha a mező érvényes, False ha hiányzik

### `_validate_type`

Típus ellenőrzése.

        Args:
            ctx: Validációs kontextus

        Returns:
            bool: True ha a típus érvényes, False ha nem

### `_validate_nested`

Beágyazott értékek validálása.

        Args:
            ctx: Validációs kontextus

### `_validate_constraints`

Érték korlátok validálása.

        Args:
            ctx: Validációs kontextus

### `_validate_choices`

Választható értékek validálása.

        Args:
            ctx: Validációs kontextus

### `_validate_range`

Érték tartományának validálása.

        Args:
            ctx: Validációs kontextus

### `load_directory`

Betölti az összes YAML fájlt egy mappából namespaced struktúrába.

        A fájlneveket (kiterjesztés nélkül) használja kulcsként, és a tartalmukat
        az adott kulcs alá tölti be. A 'system.yaml' fájl tartalmát a gyökérbe is
        betölti az app_name, debug stb. elérhetősége érdekében.

        Args:
            path: A konfigurációs mappa útvonala

        Raises:
            ConfigLoadError: Ha a mappa nem található vagy betöltési hiba történik


---

**Forrásfájl:** [`core/config/implementations/yaml_config_manager.py`](../../../neural_ai/core/config/implementations/yaml_config_manager.py)
