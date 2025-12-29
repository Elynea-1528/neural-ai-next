# core/config/interfaces/config_interface.py

Konfiguráció kezelő interfész.

## Osztályok

### `ConfigManagerInterface`

Konfigurációkezelő interfész.

    Ez az interfész definiálja a konfigurációkezelők által implementálandó metódusokat.


## Függvények

### `__init__`

Inicializálja a konfigurációkezelőt.

        Args:
            filename: Konfigurációs fájl útvonala (opcionális)

### `get`

Érték lekérése a konfigurációból.

### `get_section`

Teljes konfigurációs szekció lekérése.

### `set`

Érték beállítása a konfigurációban.

### `save`

Konfiguráció mentése fájlba.

### `load`

Konfiguráció betöltése fájlból.

### `load_directory`

Betölti az összes YAML fájlt egy mappából namespaced struktúrába.

        Args:
            path: A konfigurációs mappa útvonala

### `validate`

Konfiguráció validálása séma alapján.

        Args:
            schema: A validáláshoz használt séma

        Returns:
            Tuple[bool, Optional[Dict[str, str]]]: (érvényes-e, hibák szótára)


---

**Forrásfájl:** [`core/config/interfaces/config_interface.py`](../../../neural_ai/core/config/interfaces/config_interface.py)
