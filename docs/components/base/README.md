# Base Komponens

A Base komponens a Neural AI Next projekt alapvető infrastruktúráját biztosítja a komponensek közötti függőségek kezeléséhez és az egységes komponens inicializáláshoz.

## Főbb funkciók

- Dependency injection konténer
- Core komponensek egységes kezelése
- Központi komponens inicializálás
- Automatikus függőség feloldás

## Használat

### 1. Alap használat

```python
from neural_ai.core.base import CoreComponentFactory

# Komponensek létrehozása alapértelmezett beállításokkal
components = CoreComponentFactory.create_minimal()

# Komponensek használata
components.logger.info("Hello World")
components.storage.save_object({"key": "value"}, "data.json")
```

### 2. Konfigurált használat

```python
from neural_ai.core.base import CoreComponentFactory

# Komponensek létrehozása konfigurációval
components = CoreComponentFactory.create_components(
    config_path="config.yml",
    log_path="app.log",
    storage_path="data"
)

# Komponensek elérhetőségének ellenőrzése
if components.has_logger():
    components.logger.info("Logger initialized")
```

### 3. Saját konténer használata

```python
from neural_ai.core.base import DIContainer, CoreComponentFactory
from neural_ai.core.logger import LoggerInterface, ColoredLogger

# Konténer létrehozása és konfigurálása
container = DIContainer()
container.register_instance(LoggerInterface, ColoredLogger())

# Komponensek létrehozása konténerből
components = CoreComponentFactory.create_with_container(container)
```

## Architektúra

A base komponens három fő részből áll:

1. **DIContainer**: Dependency injection konténer
   - Komponens példányok és factory-k kezelése
   - Automatikus függőség feloldás
   - Típusbiztos interfész

2. **CoreComponents**: Komponens gyűjtemény
   - Core komponensek egységes elérése
   - Komponens státusz ellenőrzés
   - Validáció

3. **CoreComponentFactory**: Komponens gyár
   - Egységes inicializálási folyamat
   - Konfigurációs opciók kezelése
   - Komponensek összekapcsolása

## Következő lépések

1. **Meglévő komponensek frissítése**
   - Logger, Config és Storage komponensek átalakítása az új architektúra szerint
   - Factory-k optimalizálása az új használati módhoz

2. **Új komponensek fejlesztése**
   - MT5 Collector és további komponensek már az új architektúrára épülnek
   - A CoreComponentFactory bővítése az új komponensekkel

3. **Dokumentáció és példák**
   - Részletes migrációs útmutató
   - Példa alkalmazások az új architektúra használatához
   - Teljesítmény benchmarkok
