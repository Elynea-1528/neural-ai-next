# ConfigManagerFactoryInterface

## Áttekintés

A `ConfigManagerFactoryInterface` egy absztrakt interfész, amely egy gyártó (factory) mintát valósít meg a konfiguráció kezelők létrehozásához. Ez az interfész lehetővé teszi különböző konfigurációs formátumok dinamikus kezelését és a kezelők regisztrációját.

## Cél

A factory minta célja, hogy:
- Lehetővé tegye a konfiguráció kezelők típusainak dinamikus regisztrációját
- Automatikusan kiválassza a megfelelő kezelőt a fájlnév kiterjesztése alapján
- Egységes interfészt biztosítson a különböző konfigurációs formátumok kezeléséhez
- Lehetővé tegye a kezelők paraméterezett létrehozását

## Osztály definíció

```python
from abc import ABC, abstractmethod
from typing import Type, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface

class ConfigManagerFactoryInterface(ABC):
    """Konfiguráció kezelő factory interfész.

    Ez az absztrakt osztály definiálja a konfiguráció kezelő gyártó alapvető
    műveleteit, beleértve a kezelők regisztrációját és létrehozását.
    """
```

## Metódusok

### `register_manager`

```python
@classmethod
@abstractmethod
def register_manager(cls, extension: str, manager_class: Type['ConfigManagerInterface']) -> None:
    """Új konfiguráció kezelő típus regisztrálása.

    A metódus lehetővé teszi egy adott fájlkiterjesztéshez tartozó konfiguráció
    kezelő osztály regisztrációját. Ezt követően a gyár képes lesz automatikusan
    kiválasztani a megfelelő kezelőt a fájlnév alapján.

    Args:
        extension: A kezelt fájl kiterjesztése (pl: ".yml", ".yaml", ".json")
        manager_class: A kezelő osztály, amely implementálja a ConfigManagerInterface-t

    Raises:
        ValueError: Ha az extension vagy manager_class érvénytelen
        TypeError: Ha a manager_class nem megfelelő típusú
    """
```

**Paraméterek:**
- `extension` (str): A fájl kiterjesztése, amelyhez a kezelő tartozik
- `manager_class` (Type[ConfigManagerInterface]): A kezelő osztály típusa

**Kivételek:**
- `ValueError`: Ha az extension érvénytelen (pl. üres string)
- `TypeError`: Ha a manager_class nem típus objektum

### `get_manager`

```python
@classmethod
@abstractmethod
def get_manager(cls, filename: str, manager_type: str | None = None) -> 'ConfigManagerInterface':
    """Megfelelő konfiguráció kezelő létrehozása fájlnév vagy típus alapján.

    A metódus a fájlnév kiterjesztése alapján automatikusan kiválasztja a
    megfelelő kezelőt, vagy a megadott típus alapján hozza létre a kezelőt.

    Args:
        filename: Konfigurációs fájl teljes neve (elérési úttal együtt)
        manager_type: Opcionális kezelő típus azonosító

    Returns:
        ConfigManagerInterface: A létrehozott konfiguráció kezelő példány

    Raises:
        ValueError: Ha a fájlnév kiterjesztése nem regisztrált
        KeyError: Ha a megadott manager_type nem létezik
        RuntimeError: Ha a kezelő létrehozása sikertelen
    """
```

**Paraméterek:**
- `filename` (str): A konfigurációs fájl neve
- `manager_type` (str | None): Opcionális explicit kezelő típus

**Visszatérési érték:**
- `ConfigManagerInterface`: A létrehozott kezelő példány

**Kivételek:**
- `ValueError`: Ha a fájlnév kiterjesztése nem regisztrált
- `KeyError`: Ha a megadott manager_type nem létezik
- `RuntimeError`: Ha a kezelő létrehozása sikertelen

### `create_manager`

```python
@classmethod
@abstractmethod
def create_manager(cls, manager_type: str, *args: object, **kwargs: object) -> 'ConfigManagerInterface':
    """Konfiguráció kezelő létrehozása típus alapján.

    A metódus explicit típusmegadással hozza létre a konfiguráció kezelőt,
    lehetővé téve a paraméterek átadását a konstruktornak.

    Args:
        manager_type: A kért kezelő típus azonosítója
        *args: Pozícionális argumentumok a kezelő konstruktorának
        **kwargs: Kulcsszavas argumentumok a kezelő konstruktorának

    Returns:
        ConfigManagerInterface: A létrehozott konfiguráció kezelő példány

    Raises:
        KeyError: Ha a megadott manager_type nem létezik
        TypeError: Ha a paraméterek nem kompatibilisek a kezelő konstruktorával
        RuntimeError: Ha a kezelő létrehozása sikertelen
    """
```

**Paraméterek:**
- `manager_type` (str): A kért kezelő típus azonosítója
- `*args` (object): Pozícionális argumentumok
- `**kwargs` (object): Kulcsszavas argumentumok

**Visszatérési érték:**
- `ConfigManagerInterface`: A létrehozott kezelő példány

**Kivételek:**
- `KeyError`: Ha a megadott manager_type nem létezik
- `TypeError`: Ha a paraméterek nem kompatibilisek
- `RuntimeError`: Ha a kezelő létrehozása sikertelen

## Használati példa

```python
from neural_ai.core.config.interfaces.factory_interface import ConfigManagerFactoryInterface
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface

class MyConfigManager(ConfigManagerInterface):
    def __init__(self, filename: str | None = None):
        # Implementáció
        pass
    
    # További metódusok implementációja...

# Factory implementáció
class MyFactory(ConfigManagerFactoryInterface):
    _managers: dict[str, type[ConfigManagerInterface]] = {}
    
    @classmethod
    def register_manager(cls, extension: str, manager_class: type[ConfigManagerInterface]) -> None:
        cls._managers[extension] = manager_class
    
    @classmethod
    def get_manager(cls, filename: str, manager_type: str | None = None) -> ConfigManagerInterface:
        if manager_type:
            # Típus alapján létrehozás
            pass
        # Fájlnév alapján létrehozás
        extension = "." + filename.split(".")[-1]
        return cls._managers[extension]()
    
    @classmethod
    def create_manager(cls, manager_type: str, *args, **kwargs) -> ConfigManagerInterface:
        # Implementáció
        pass

# Használat
MyFactory.register_manager(".yml", MyConfigManager)
manager = MyFactory.get_manager("config.yml")
```

## Implementációs jegyzetek

1. **Extension kezelés**: A kiterjesztéseknek mindig ponttal kezdődniük kell (pl. ".yml")
2. **Típusbiztonság**: A `TYPE_CHECKING` blokk használatával kerüljük el a körkörös importokat
3. **Paraméterezés**: A `create_manager` metódus támogatja a konstruktor paraméterek átadását
4. **Hibakezelés**: Minden metódus definiálja a potenciális kivételeket

## Kapcsolódó komponensek

- [`ConfigManagerInterface`](config_interface.md): A kezelők alapinterfésze
- [`ConfigManagerFactory`](../implementations/config_manager_factory.md): Konkrét factory implementáció

## Verzió követés

- **Létrehozás dátuma**: 2025-12-22
- **Utolsó módosítás**: 2025-12-22
- **Verzió**: 1.0.0