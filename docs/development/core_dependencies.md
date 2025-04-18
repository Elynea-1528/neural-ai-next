# Core Komponensek Függőségi Analízis

## Jelenlegi Helyzet

A core komponensek egymásra épülhetnek, ami körkörös függőségi helyzetet teremthet:

### Logger
- **Szükséges függőségek**:
  - Config: Logger konfigurációk kezelése
    - Log szintek
    - Formátumok
    - Output csatornák
  - Storage (opcionális):
    - File alapú logging esetén
    - Log rotálás és archiválás

### Config
- **Szükséges függőségek**:
  - Logger: Műveletek naplózása
  - Storage (opcionális):
    - Konfigurációk perzisztens tárolása
    - Konfig fájlok kezelése

### Storage
- **Szükséges függőségek**:
  - Logger: Műveletek naplózása
  - Config: Storage beállítások

## Problémák

1. Körkörös függőségek:
   ```
   Logger -> Config -> Logger
   Logger -> Config -> Storage -> Logger
   Config -> Storage -> Config
   ```

2. Inicializációs sorrend:
   - Ki inicializálja először a másikat?
   - Hogyan kerüljük el a deadlock-ot?

## Javasolt Megoldás

### 1. Függőség Injektálás

```python
class Logger:
    def __init__(self, config: Optional[ConfigInterface] = None):
        self._config = config or DefaultConfig()

class Config:
    def __init__(self, logger: Optional[LoggerInterface] = None):
        self._logger = logger or NullLogger()

class Storage:
    def __init__(
        self,
        config: Optional[ConfigInterface] = None,
        logger: Optional[LoggerInterface] = None
    ):
        self._config = config or DefaultConfig()
        self._logger = logger or NullLogger()
```

### 2. Alapértelmezett Implementációk

```python
class NullLogger(LoggerInterface):
    """Nem csinál semmit, alapértelmezett fallback."""
    def log(self, level: str, message: str) -> None:
        pass

class DefaultConfig(ConfigInterface):
    """Alapértelmezett beállításokkal."""
    def get(self, key: str, default: Any = None) -> Any:
        return default
```

### 3. Bootstrap Folyamat

```python
def bootstrap_core():
    # 1. Alap konfiguráció létrehozása
    config = Config(logger=NullLogger())

    # 2. Logger inicializálása a konfiggal
    logger = Logger(config=config)

    # 3. Konfig frissítése a valódi loggerrel
    config._logger = logger

    # 4. Storage inicializálása
    storage = Storage(config=config, logger=logger)

    return CoreComponents(
        config=config,
        logger=logger,
        storage=storage
    )
```

### 4. Factory Pattern

```python
class CoreComponentFactory:
    @staticmethod
    def create_components(
        config_path: str = "config.yml",
        log_path: str = "app.log"
    ) -> CoreComponents:
        # 1. Konfig betöltése
        config = Config.load(config_path)

        # 2. Logger létrehozása
        logger = Logger.create(config)

        # 3. Storage inicializálása
        storage = Storage(config, logger)

        return CoreComponents(config, logger, storage)
```

## Használat

```python
# Alap használat alapértelmezett implementációkkal
logger = Logger()  # NullConfig-ot használ
config = Config()  # NullLogger-t használ
storage = Storage()  # Mindkettőből az alapértelmezettet

# Teljes inicializálás
core = CoreComponentFactory.create_components()
logger = core.logger
config = core.config
storage = core.storage
```

## További Fejlesztési Lehetőségek

1. **Dependency Injection Container**:
   - Automatikus függőség feloldás
   - Lifecycle management
   - Scope kezelés

2. **Lazy Loading**:
   - Függőségek késleltetett betöltése
   - Csak amikor tényleg szükséges

3. **Plugin Rendszer**:
   - Dinamikusan cserélhető implementációk
   - Könnyű bővíthetőség

4. **Metrikák és Monitorozás**:
   - Függőségi gráf vizualizáció
   - Teljesítmény mérés
   - Erőforrás használat követése

## Következő Lépések

1. Core komponensek refaktorálása a javasolt minta szerint
2. Bootstrap folyamat implementálása
3. Dependency injection container bevezetése
4. Tesztek frissítése az új architektúrához
