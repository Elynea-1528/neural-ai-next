# 🏗️ Architect Mód - Neural AI Next

## Alapelvek

Az Architect módban a következő alapelvekre kell koncentrálni:

1. **Rendszerszintű tervezés** - Mindig a teljes rendszer architektúráját vedd figyelembe
2. **Komponens alapú megközelítés** - A projekt komponens-alapú architektúrát használ
3. **Hierarchikus struktúra** - Kövesd a hierarchikus rendszer elveit
4. **Dokumentáció vezérelt fejlesztés** - Minden tervezési döntést dokumentálj

## Fő tervezési szempontok

### 1. Factory + DI Container Hibrid Architektúra

A projekt **Factory + DI Container hibrid megoldást** használ:

- **CoreComponentFactory** - Komponensek egységes létrehozásáért felel
- **DIContainer** - Függőségek kezeléséért felel (háttérben)
- **CoreComponents** - Komponensek közös eléréséért felel

**Fontos:** A meglévő kódban (pl. MT5Collector) még nem használják ezt a hibrid architektúrát, de az új komponenseknek ezt kell követniük.

### 2. Komponens Struktúra

Minden új komponens kövesse a standard struktúrát:
```
neural_ai/[komponens_neve]/
├── __init__.py
├── interfaces/
│   ├── __init__.py
│   └── [komponens]_interface.py
├── implementations/
│   ├── __init__.py
│   ├── [komponens]_factory.py
│   └── [implementációk]/
└── exceptions.py
```

### 3. Base Komponensek Használata

**Új komponensek esetén kötelező használni a base komponenseket:**

```python
from neural_ai.core.base import CoreComponentFactory, CoreComponents

class MyComponent:
    def __init__(self, config):
        # Komponensek létrehozása a Factory-vel
        self.components: CoreComponents = CoreComponentFactory.create_components(
            config_path=config.get('config_path'),
            log_path=config.get('log_path'),
            storage_path=config.get('storage_path')
        )
        
        # Komponensek használata
        self.components.logger.info("MyComponent initialized")
        
    def process_data(self, data):
        # Naplózás
        self.components.logger.debug(f"Processing data: {data}")
        
        # Adattárolás
        self.components.storage.save_object(data, "processed_data.json")
```

**Meglévő komponensek migrálása (opcionális, de ajánlott):**
```python
# RÉGI (manuális inicializálás)
class OldComponent:
    def __init__(self):
        self.config_manager = ConfigManagerFactory.get_manager(...)
        self.logger = LoggerFactory.get_logger(...)
        self.storage = StorageFactory.get_storage(...)

# ÚJ (base komponensekkel)
class OldComponent:
    def __init__(self, config):
        self.components = CoreComponentFactory.create_components(
            config_path=config.get('config_path'),
            log_path=config.get('log_path'),
            storage_path=config.get('storage_path')
        )
        # A komponensek elérhetők: self.components.config, self.components.logger, stb.
```

### 4. Konfigurációkezelés

- Használd a `neural_ai.core.config` komponenst YAML alapú konfigurációhoz
- Minden komponensnek legyen elkülönített konfigurációs fájlja
- Validáld a konfigurációt a betöltéskor
- **Új komponensek esetén:** A konfigurációt a `CoreComponentFactory`-n keresztül add át

### 5. Naplózás

- Használd a `neural_ai.core.logger` komponenst strukturált naplózáshoz
- Implementálj különböző naplózási szinteket (INFO, DEBUG, ERROR)
- Használj rotációs file logger-t hosszú futású folyamatokhoz
- **Új komponensek esetén:** A loggert a `CoreComponents`-ből érd el

### 6. Adattárolás

- Használd a `neural_ai.core.storage` komponenst fájl alapú tároláshoz
- Tervezz adatbázis integrációt a jövőre nézve
- Implementálj adatminőség ellenőrzést
- **Új komponensek esetén:** A storage-t a `CoreComponents`-ből érd el

## Tervezési folyamat

1. **Követelmények elemzése** - Mindig kezdd a dokumentáció átnézésével
2. **Architektúra tervezés** - Tervezd meg a komponens struktúrát
3. **Interfész definiálás** - Hozd létre az interfészeket először
4. **Implementációs terv** - Döntsd el a konkrét implementációt
5. **Tesztelési stratégia** - Tervezd meg a tesztelést
6. **Dokumentáció** - Frissítsd a dokumentációt

## Projekt specifikus szempontok

### MT5 Integráció

- Az MT5 Collector a kulcsfontosságú komponens
- Tervezd meg az Expert Advisor kommunikációt
- Implementálj historikus adatgyűjtést
- Biztosítsd az adatminőséget

### Adatfeldolgozás

- Dimension Processor komponensek tervezése
- Hierarchikus modell struktúra
- Training dataset generálás

## Dokumentációs követelmények

Minden tervezéshez kötelezően készítsd el:
- [Komponens Tervezési Specifikáció](../../docs/templates/component_template.py)
- [Fejlesztési Checklista](../../docs/development/checklist_template.md)
- API dokumentáció
- Architektúra leírás
- Használati példák

## Hasznos linkek

- [Rendszer Architektúra](../../docs/architecture/overview.md)
- [Hierarchikus Rendszer](../../docs/architecture/hierarchical_system/overview.md)
- [Komponens Fejlesztési Útmutató](../../docs/development/component_development_guide.md)
- [Egységes Fejlesztési Útmutató](../../docs/development/unified_development_guide.md)
