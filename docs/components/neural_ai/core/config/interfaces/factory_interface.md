# neural_ai/core/config/interfaces/factory_interface.py

Konfiguráció kezelő factory interfész definíciója.

Ez az interfész egy gyártó (factory) mintát valósít meg a konfiguráció kezelők
létrehozásához. Lehetővé teszi különböző konfigurációs formátumok kezelését
és a kezelők dinamikus regisztrációját.

## Importok

```python
from abc import ABC
from abc import abstractmethod
from typing import TYPE_CHECKING
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
```

## Osztály: `ConfigManagerFactoryInterface(ABC)`

Konfiguráció kezelő factory interfész.

Ez az absztrakt osztály definiálja a konfiguráció kezelő gyártó alapvető
műveleteit, beleértve a kezelők regisztrációját és létrehozását.

### Metódusok

#### `register_manager()`

```python
def register_manager(cls, extension: str, manager_class: type['ConfigManagerInterface']) -> None
```

Új konfiguráció kezelő típus regisztrálása. A metódus lehetővé teszi egy adott fájlkiterjesztéshez tartozó konfiguráció kezelő osztály regisztrációját. Ezt követően a gyár képes lesz automatikusan kiválasztani a megfelelő kezelőt a fájlnév alapján.

**Paraméterek:**

- **`cls`**
- **`extension`** (`str`): A kezelt fájl kiterjesztése (pl: ".yml", ".yaml", ".json")
- **`manager_class`** (`type['ConfigManagerInterface']`): A kezelő osztály, amely implementálja a ConfigManagerInterface-t

**Visszatérési érték:**

- Típus: `None`

**Kivételek:**

- **`ValueError`**: Ha az extension vagy manager_class érvénytelen
- **`TypeError`**: Ha a manager_class nem megfelelő típusú

#### `get_manager()`

```python
def get_manager(cls, filename: str, manager_type: str | None = None) -> 'ConfigManagerInterface'
```

Megfelelő konfiguráció kezelő létrehozása fájlnév vagy típus alapján. A metódus a fájlnév kiterjesztése alapján automatikusan kiválasztja a megfelelő kezelőt, vagy a megadott típus alapján hozza létre a kezelőt.

**Paraméterek:**

- **`cls`**
- **`filename`** (`str`): Konfigurációs fájl teljes neve (elérési úttal együtt)
- **`manager_type`** (`str | None`) = `None`: Opcionális kezelő típus azonosító

**Visszatérési érték:**

- Típus: `'ConfigManagerInterface'`
- ConfigManagerInterface: A létrehozott konfiguráció kezelő példány

**Kivételek:**

- **`ValueError`**: Ha a fájlnév kiterjesztése nem regisztrált
- **`KeyError`**: Ha a megadott manager_type nem létezik
- **`RuntimeError`**: Ha a kezelő létrehozása sikertelen

#### `create_manager()`

```python
def create_manager(cls, manager_type: str) -> 'ConfigManagerInterface'
```

Konfiguráció kezelő létrehozása típus alapján. A metódus explicit típusmegadással hozza létre a konfiguráció kezelőt, lehetővé téve a paraméterek átadását a konstruktornak.

**Paraméterek:**

- **`cls`**
- **`manager_type`** (`str`): A kért kezelő típus azonosítója *args: Pozícionális argumentumok a kezelő konstruktorának **kwargs: Kulcsszavas argumentumok a kezelő konstruktorának

**Visszatérési érték:**

- Típus: `'ConfigManagerInterface'`
- ConfigManagerInterface: A létrehozott konfiguráció kezelő példány

**Kivételek:**

- **`KeyError`**: Ha a megadott manager_type nem létezik
- **`TypeError`**: Ha a paraméterek nem kompatibilisek a kezelő konstruktorával
- **`RuntimeError`**: Ha a kezelő létrehozása sikertelen

---

**Forrásfájl:** [`neural_ai/core/config/interfaces/factory_interface.py`](../../neural_ai/core/config/interfaces/factory_interface.py)
