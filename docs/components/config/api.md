# Konfiguráció Kezelő API Referencia

## Interfészek

### ConfigManagerInterface

Alap interfész a konfigurációkezelő implementációkhoz.

```python
class ConfigManagerInterface(ABC):
    @abstractmethod
    def get(self, *keys: str, default: Any = None) -> Any:
        """Érték lekérése a konfigurációból.

        Args:
            *keys: Kulcs útvonal (pl. "database", "host")
            default: Alapértelmezett érték, ha a kulcs nem létezik

        Returns:
            Any: A kért konfigurációs érték vagy az alapértelmezett érték
        """
        pass

    @abstractmethod
    def get_section(self, section: str) -> Dict[str, Any]:
        """Teljes konfigurációs szekció lekérése.

        Args:
            section: A szekció neve

        Returns:
            Dict[str, Any]: A szekció összes beállítása

        Raises:
            KeyError: Ha a szekció nem létezik
        """
        pass

    @abstractmethod
    def set(self, *keys: str, value: Any) -> None:
        """Érték beállítása a konfigurációban.

        Args:
            *keys: Kulcs útvonal (pl. "database", "host")
            value: Az új érték

        Raises:
            ValueError: Ha a kulcs útvonal érvénytelen
        """
        pass

    @abstractmethod
    def save(self, filename: Optional[str] = None) -> None:
        """Aktuális konfiguráció mentése fájlba.

        Args:
            filename: Opcionális fájlnév. Ha nincs megadva,
                     az eredeti fájlba ment

        Raises:
            IOError: Ha a mentés sikertelen
        """
        pass

    @abstractmethod
    def load(self, filename: str) -> None:
        """Konfiguráció betöltése fájlból.

        Args:
            filename: A betöltendő fájl neve

        Raises:
            FileNotFoundError: Ha a fájl nem létezik
            ValueError: Ha a fájl formátuma érvénytelen
        """
        pass

    @abstractmethod
    def validate(self, schema: Dict[str, Any]) -> Tuple[bool, Optional[Dict[str, str]]]:
        """Konfiguráció validálása séma alapján.

        Args:
            schema: Validációs séma

        Returns:
            Tuple[bool, Optional[Dict[str, str]]]: (érvényes-e, hibaüzenetek)
        """
        pass
```

### ConfigManagerFactoryInterface

Logger példányok létrehozásáért felelős interfész.

```python
class ConfigManagerFactoryInterface(ABC):
    @staticmethod
    @abstractmethod
    def get_manager(filename: str, **kwargs: Any) -> ConfigManagerInterface:
        """Megfelelő ConfigManager példány létrehozása.

        Args:
            filename: A konfigurációs fájl neve
            **kwargs: További paraméterek a manager létrehozásához

        Returns:
            ConfigManagerInterface: A létrehozott manager példány

        Raises:
            ValueError: Ha a fájl típusa nem támogatott
        """
        pass

    @staticmethod
    @abstractmethod
    def register_manager(extension: str, manager_class: Type[ConfigManagerInterface]) -> None:
        """Új manager típus regisztrálása.

        Args:
            extension: Fájl kiterjesztés (pl. ".yaml", ".json")
            manager_class: A manager osztály

        Raises:
            ValueError: Ha a kiterjesztés már regisztrálva van
        """
        pass
```

## Implementációk

### YAMLConfigManager

YAML formátumú konfigurációs fájlok kezelése séma alapú validációval.

```python
class YAMLConfigManager(ConfigManagerInterface):
    def __init__(self, filename: Optional[str] = None) -> None:
        """YAML konfiguráció kezelő inicializálása.

        Args:
            filename: Opcionális konfig fájl betöltéséhez
        """
        pass

    def get(self, *keys: str, default: Any = None) -> Any:
        """Érték lekérése a konfigurációból.

        Args:
            *keys: A konfigurációs kulcsok hierarchiája
            default: Alapértelmezett érték, ha a kulcs nem található

        Returns:
            A konfigurációs érték vagy az alapértelmezett érték
        """
        pass

    def get_section(self, section: str) -> Dict[str, Any]:
        """Teljes konfigurációs szekció lekérése.

        Args:
            section: A szekció neve

        Returns:
            A szekció konfigurációs adatai

        Raises:
            KeyError: Ha a szekció nem található
        """
        pass

    def set(self, *keys: str, value: Any) -> None:
        """Érték beállítása a konfigurációban.

        Args:
            *keys: A konfigurációs kulcsok hierarchiája
            value: A beállítandó érték

        Raises:
            ValueError: Ha nincs kulcs megadva vagy érvénytelen hierarchia
        """
        pass

    def save(self, filename: Optional[str] = None) -> None:
        """Aktuális konfiguráció mentése fájlba.

        Args:
            filename: A mentési fájl neve (opcionális, alapértelmezett az eredeti fájlnév)

        Raises:
            ValueError: Ha nincs fájlnév megadva vagy mentési hiba történik
        """
        pass

    def load(self, filename: str) -> None:
        """Konfiguráció betöltése fájlból.

        Args:
            filename: A betöltendő fájl neve

        Raises:
            ConfigLoadError: Ha a fájl nem található vagy betöltési hiba történik
        """
        pass

    def validate(self, schema: Dict[str, Any]) -> Tuple[bool, Optional[Dict[str, str]]]:
        """Konfiguráció validálása séma alapján.

        Args:
            schema: A validációs séma definíció

        Returns:
            Tuple[bool, Dict[str, str] | None]: (sikeres-e a validáció, hibák dictionary vagy None)
        """
        pass
```

Támogatott típusok:
- str: Szöveges érték
- int: Egész szám
- float: Lebegőpontos szám
- bool: Logikai érték
- list: Lista
- dict: Szótár

Validációs lehetőségek:
- Kötelező/elhagyható mezők (`optional`)
- Típus ellenőrzés (`type`)
- Érték tartomány (`min`, `max`)
- Választék ellenőrzés (`choices`)
- Beágyazott validáció (`schema`)

### ConfigManagerFactory

Konfigurációkezelő példányok létrehozása és kezelése.

```python
class ConfigManagerFactory(ConfigManagerFactoryInterface):
    _manager_types: dict[str, type[ConfigManagerInterface]] = {
        ".yml": YAMLConfigManager,
        ".yaml": YAMLConfigManager,
    }

    @classmethod
    def register_manager(cls, extension: str, manager_class: type[ConfigManagerInterface]) -> None:
        """Új konfiguráció kezelő típus regisztrálása.

        Args:
            extension: A kezelt fájl kiterjesztése (pl: ".yml")
            manager_class: A kezelő osztály

        Raises:
            ValueError: Ha a kiterjesztés már regisztrálva van
        """
        pass

    @classmethod
    def get_manager(cls, filename: str | Path, manager_type: str | None = None) -> ConfigManagerInterface:
        """Megfelelő konfiguráció kezelő létrehozása.

        Args:
            filename: Konfigurációs fájl neve vagy Path objektum
            manager_type: Kért kezelő típus (opcionális)

        Returns:
            ConfigManagerInterface: A létrehozott kezelő

        Raises:
            ConfigLoadError: Ha nem található megfelelő kezelő
        """
        pass

    @classmethod
    def get_supported_extensions(cls) -> list[str]:
        """Támogatott fájl kiterjesztések lekérése.

        Returns:
            list[str]: A támogatott kiterjesztések listája
        """
        pass

    @classmethod
    def create_manager(cls, manager_type: str, *args: Any, **kwargs: Any) -> ConfigManagerInterface:
        """Konfiguráció kezelő létrehozása típus alapján.

        Args:
            manager_type: A kért kezelő típus
            *args: Pozícionális paraméterek
            **kwargs: Kulcsszavas paraméterek

        Returns:
            ConfigManagerInterface: A létrehozott kezelő

        Raises:
            ConfigLoadError: Ha nem található megfelelő kezelő
        """
        pass
```

## Séma Definíció

A validációs séma felépítése:

```python
schema = {
    "field_name": {
        # Típus meghatározás
        "type": "str",  # str, int, float, bool, list, dict

        # Érték korlátok számokhoz
        "min": 0,
        "max": 100,

        # Választható értékek
        "choices": ["option1", "option2"],

        # Kötelezőség
        "optional": True,  # Alapértelmezetten False

        # Beágyazott séma dict típushoz
        "schema": {
            "nested_field": {
                "type": "str"
            }
        }
    }
}
```

## Példák

### 1. Alap műveletek

```python
# Manager létrehozása
config = ConfigManagerFactory.get_manager("config.yaml")

# Értékek kezelése
host = config.get("database", "host", default="localhost")
config.set("database", "port", 5432)

# Szekció kezelése
db_config = config.get_section("database")
```

### 2. Validáció

```python
# Séma definiálása
schema = {
    "server": {
        "host": {"type": "str"},
        "port": {
            "type": "int",
            "min": 1,
            "max": 65535
        }
    }
}

# Validálás
is_valid, errors = config.validate(schema)
```

### 3. Factory használata

```python
# Új formátum regisztrálása
ConfigManagerFactory.register_manager(".custom", CustomConfigManager)

# Manager lekérése fájl alapján
config = ConfigManagerFactory.get_manager("config.custom")

# Manager lekérése típus alapján
config = ConfigManagerFactory.create_manager("yaml", filename="config.yaml")

# Támogatott kiterjesztések lekérése
extensions = ConfigManagerFactory.get_supported_extensions()
# ['.yml', '.yaml', '.custom']
```

## Hibaüzenetek

### Validációs hibák

| Hiba | Leírás | Példa üzenet |
|------|--------|--------------|
| Típus hiba | Nem megfelelő típusú érték | "Érvénytelen típus, várt: int" |
| Tartomány hiba | Érték a megengedett tartományon kívül | "Értéknek >= 0 kell lennie" |
| Választék hiba | Nem megengedett érték | "Értéknek a következőek egyikének kell lennie: [A, B, C]" |
| Hiányzó mező | Kötelező mező hiányzik | "Kötelező mező hiányzik" |

### Runtime hibák

| Kivétel | Ok | Kezelés |
|---------|----|----|
| FileNotFoundError | Nem létező fájl | Ellenőrizze az útvonalat |
| ValueError | Érvénytelen YAML | Ellenőrizze a szintaxist |
| KeyError | Nem létező szekció | Ellenőrizze a kulcsot |
