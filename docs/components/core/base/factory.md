# core/base/factory.py

Core komponensek factory implementáció.

Ez a modul biztosítja a core komponensek (config, logger, storage) létrehozását
és kezelését dependency injection pattern használatával. A factory támogatja
a lazy loadinget, bootstrap inicializálást és NullObject pattern-t fallback-ként.

## Osztályok

### `CoreComponentFactory`

Core komponensek létrehozásáért felelős factory lazy loadinggel.

    Ez az osztály biztosítja a core komponensek (config, logger, storage) egységes
    létrehozását és kezelését. Singleton minta használatával biztosítja, hogy csak
    egy példány létezik, és lazy loading technikával optimalizálja a teljesítményt.

    A factory támogatja a komponensek validációját, függőségi injektálást és
    automatikus inicializálást különböző konfigurációs forgatókönyvekben.

    Attributes:
        _container: A dependency injection konténer
        _logger_loader: Lazy loader a logger komponenshez
        _config_loader: Lazy loader a config manager komponenshez
        _storage_loader: Lazy loader a storage komponenshez


## Függvények

### `__init__`

Inicializálja a factory-t lazy-loaded függőségekkel.

### `_get_logger`

Lazy loadinggel tölti be a logger komponenst.

### `_get_config_manager`

Lazy loadinggel tölti be a config manager komponenst.

### `_get_storage`

Lazy loadinggel tölti be a storage komponenst.

### `logger`

Visszaadja a logger példányt (lazy-loaded).

### `config_manager`

Visszaadja a config manager példányt (lazy-loaded).

### `storage`

Visszaadja a storage példányt (lazy-loaded).

### `_expensive_config`

Lazy loadinggel tölti be a drága konfigurációt.

### `_component_cache`

Lazy loadinggel tölti be a komponens gyorsítótárát.

### `_process_config`

Feldolgozza a konfigurációt (szimulált drága művelet).

### `_load_component_cache`

Betölti a komponens gyorsítótárát (szimulált drága művelet).

### `reset_lazy_loaders`

Visszaállítja az összes lazy loadert.

        Ez a metódus visszaállítja az összes lazy loader állapotát, amely
        hasznos lehet tesztelés során vagy újrainicializáláskor.
        A lazy property-ket is törli.

### `_validate_dependencies`

Ellenőrzi, hogy minden szükséges függőség elérhető-e.

        Args:
            component_type: A létrehozandó komponens típusa
            config: Konfigurációs dictionary

        Raises:
            ConfigurationError: Ha a konfiguráció érvénytelen vagy hiányzik
            DependencyError: Ha szükséges függőségek nem érhetők el

### `create_components`

Core komponensek létrehozása és inicializálása.

        Létrehozza és inicializálja az összes core komponenst (config, logger, storage)
        a megadott elérési utak alapján. A komponensek lazy loadinggel kerülnek betöltésre.

        Args:
            config_path: A konfigurációs fájl elérési útja (opcionális)
            log_path: A log fájl elérési útja (opcionális)
            storage_path: A tároló alapkönyvtára (opcionális)

        Returns:
            CoreComponents: Az inicializált core komponensek gyűjteménye

        Raises:
            ConfigurationError: Ha a konfiguráció érvénytelen
            DependencyError: Ha szükséges függőségek hiányoznak

### `create_with_container`

Core komponensek létrehozása meglévő konténerből.

        Args:
            container: A DI konténer, amely tartalmazza a komponenseket

        Returns:
            CoreComponents: Az inicializált core komponensek

### `create_minimal`

Minimális core komponens készlet létrehozása.

        Létrehoz egy alapvető komponens készletet alapértelmezett beállításokkal.
        Megpróbálja betölteni a config.yml fájlt, ha létezik, különben alapértelmezett
        konfigurációt használ.

        Returns:
            CoreComponents: Az inicializált minimális komponensek

### `create_logger`

Létrehoz egy logger példányt.

        Args:
            name: A logger neve
            config: Konfigurációs dictionary (opcionális)

        Returns:
            LoggerInterface: A létrehozott logger példány

        Raises:
            ConfigurationError: Ha a konfiguráció érvénytelen
            DependencyError: Ha szükséges függőségek hiányoznak

### `create_config_manager`

Létrehoz egy config manager példányt.

        Args:
            config_file_path: A konfigurációs fájl elérési útja
            config: Konfigurációs dictionary

        Returns:
            ConfigManagerInterface: A létrehozott config manager példány

        Raises:
            ConfigurationError: Ha a konfiguráció érvénytelen
            DependencyError: Ha szükséges függőségek hiányoznak

### `create_storage`

Létrehoz egy storage példányt.

        Args:
            base_directory: A tároló alapkönyvtára
            config: Konfigurációs dictionary

        Returns:
            StorageInterface: A létrehozott storage példány

        Raises:
            ConfigurationError: Ha a konfiguráció érvénytelen
            DependencyError: Ha szükséges függőségek hiányoznak


---

**Forrásfájl:** [`core/base/factory.py`](../../../neural_ai/core/base/factory.py)
