# CoreComponentFactory

## Áttekintés

Core komponensek factory implementáció.

Ez a modul biztosítja a core komponensek (config, logger, storage) létrehozását és kezelését dependency injection pattern használatával. A factory támogatja a lazy loadinget, bootstrap inicializálást és NullObject pattern-t fallback-ként.

## Osztály

### `CoreComponentFactory`

Core komponensek létrehozásáért felelős factory lazy loadinggel.

Ez az osztály biztosítja a core komponensek (config, logger, storage) egységes létrehozását és kezelését. Singleton minta használatával biztosítja, hogy csak egy példány létezik, és lazy loading technikával optimalizálja a teljesítményt.

A factory támogatja a komponensek validációját, függőségi injektálást és automatikus inicializálást különböző konfigurációs forgatókönyvekben.

#### Attribútumok

- `_container`: A dependency injection konténer
- `_logger_loader`: Lazy loader a logger komponenshez
- `_config_loader`: Lazy loader a config manager komponenshez
- `_storage_loader`: Lazy loader a storage komponenshez

#### Metódusok

##### `__init__(container: DIContainer)`

Inicializálja a factory-t lazy-loaded függőségekkel.

**Paraméterek:**
- `container`: A dependency injection konténer

##### `logger` property

Visszaadja a logger példányt (lazy-loaded).

**Visszatérési érték:**
- `LoggerInterface`: A logger példány

##### `config_manager` property

Visszaadja a config manager példányt (lazy-loaded).

**Visszatérési érték:**
- `ConfigManagerInterface`: A config manager példány

##### `storage` property

Visszaadja a storage példányt (lazy-loaded).

**Visszatérési érték:**
- `StorageInterface`: A storage példány

##### `reset_lazy_loaders()`

Visszaállítja az összes lazy loadert.

Ez a metódus visszaállítja az összes lazy loader állapotát, amely hasznos lehet tesztelés során vagy újrainicializáláskor. A lazy property-ket is törli.

##### `create_components(config_path, log_path, storage_path)`

Core komponensek létrehozása és inicializálása.

Létrehozza és inicializálja az összes core komponenst (config, logger, storage) a megadott elérési utak alapján. A komponensek lazy loadinggel kerülnek betöltésre.

**Paraméterek:**
- `config_path`: A konfigurációs fájl elérési útja (opcionális)
- `log_path`: A log fájl elérési útja (opcionális)
- `storage_path`: A tároló alapkönyvtára (opcionális)

**Visszatérési érték:**
- `CoreComponents`: Az inicializált core komponensek gyűjteménye

**Kivételek:**
- `ConfigurationError`: Ha a konfiguráció érvénytelen
- `DependencyError`: Ha szükséges függőségek hiányoznak

##### `create_with_container(container)`

Core komponensek létrehozása meglévő konténerből.

**Paraméterek:**
- `container`: A DI konténer, amely tartalmazza a komponenseket

**Visszatérési érték:**
- `CoreComponents`: Az inicializált core komponensek

##### `create_minimal()`

Minimális core komponens készlet létrehozása.

Létrehoz egy alapvető komponens készletet alapértelmezett beállításokkal. Megpróbálja betölteni a config.yml fájlt, ha létezik, különben alapértelmezett konfigurációt használ.

**Visszatérési érték:**
- `CoreComponents`: Az inicializált minimális komponensek

##### `create_logger(name, config)`

Létrehoz egy logger példányt.

**Paraméterek:**
- `name`: A logger neve
- `config`: Konfigurációs dictionary (opcionális)

**Visszatérési érték:**
- `LoggerInterface`: A létrehozott logger példány

**Kivételek:**
- `ConfigurationError`: Ha a konfiguráció érvénytelen
- `DependencyError`: Ha szükséges függőségek hiányoznak

##### `create_config_manager(config_file_path, config)`

Létrehoz egy config manager példányt.

**Paraméterek:**
- `config_file_path`: A konfigurációs fájl elérési útja
- `config`: Konfigurációs dictionary

**Visszatérési érték:**
- `ConfigManagerInterface`: A létrehozott config manager példány

**Kivételek:**
- `ConfigurationError`: Ha a konfiguráció érvénytelen
- `DependencyError`: Ha szükséges függőségek hiányoznak

##### `create_storage(base_directory, config)`

Létrehoz egy storage példányt.

**Paraméterek:**
- `base_directory`: A tároló alapkönyvtára
- `config`: Konfigurációs dictionary

**Visszatérési érték:**
- `StorageInterface`: A létrehozott storage példány

**Kivételek:**
- `ConfigurationError`: Ha a konfiguráció érvénytelen
- `DependencyError`: Ha szükséges függőségek hiányoznak

## Kapcsolódó Dokumentáció

- [CoreComponents](implementations/component_bundle.md)
- [DIContainer](implementations/di_container.md)
- [LazyLoader](implementations/lazy_loader.md)
- [SingletonMeta](implementations/singleton.md)