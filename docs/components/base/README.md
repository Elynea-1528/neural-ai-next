# Neural AI - Base Komponens

## Áttekintés

A Base komponens a Neural AI Next projekt alapvető infrastruktúráját biztosítja. Felelős a komponensek közötti függőségek kezeléséért, a komponensek inicializálásáért és az egységes hozzáférés biztosításáért.

## Főbb funkciók

- Dependency injection konténer
- Core komponensek egységes kezelése
- Központi komponens inicializálás
- Automatikus függőség feloldás
- Típusbiztos interfészek
- Komponens életciklus kezelés

## Telepítés és függőségek

A komponens a Neural AI keretrendszer alapvető része, külső függőségeket nem igényel. A Python standard library elegendő a működéséhez.

## Használat

### 1. Alap inicializálás

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

### 3. Dependency Injection

```python
from neural_ai.core.base import DIContainer
from typing import Protocol

class DataProcessor(Protocol):
    def process(self, data: Any) -> Any: ...

class CustomProcessor:
    def process(self, data: Any) -> Any:
        return data * 2

# Komponens regisztráció
container = DIContainer()
container.register_instance(DataProcessor, CustomProcessor())

# Komponensek használata konténerből
processor = container.resolve(DataProcessor)
```

## Architektúra

A komponens három fő részből áll:

```
neural_ai/core/base/
├── container.py        # DIContainer implementáció
├── core_components.py  # CoreComponents osztály
└── factory.py         # CoreComponentFactory implementáció
```

### Főbb osztályok

1. **DIContainer**
   - Komponens példányok és factory-k kezelése
   - Automatikus függőség feloldás
   - Típusbiztos interfész

2. **CoreComponents**
   - Core komponensek egységes elérése
   - Komponens státusz ellenőrzés
   - Validáció

3. **CoreComponentFactory**
   - Egységes inicializálási folyamat
   - Konfigurációs opciók kezelése
   - Komponensek összekapcsolása

## API gyorsreferencia

```python
# DIContainer
container = DIContainer()
container.register_instance(Interface, implementation)
container.register_factory(Interface, factory_func)
instance = container.resolve(Interface)

# CoreComponents
components = CoreComponents()
components.has_logger()
components.has_config()
components.validate()

# CoreComponentFactory
components = CoreComponentFactory.create_minimal()
components = CoreComponentFactory.create_components(config_path="config.yml")
components = CoreComponentFactory.create_with_container(container)
```

## Fejlesztői információk

### Új komponens integrálása

1. Definiálja a komponens interfészét
2. Implementálja a komponenst
3. Bővítse a CoreComponents osztályt
4. Frissítse a CoreComponentFactory-t

### Konvenciók

- Minden komponens rendelkezik interfész definícióval
- Factory pattern használata az inicializáláshoz
- Explicit függőség injektálás
- Típusannotációk használata

## Tesztelés

```bash
# Unit tesztek futtatása
pytest tests/core/base/

# Lefedettség ellenőrzése
pytest --cov=neural_ai.core.base tests/core/base/
```

## Közreműködés

1. Fork létrehozása
2. Feature branch létrehozása (`git checkout -b feature/új_funkció`)
3. Változtatások commit-olása (`git commit -am 'Új funkció: xyz'`)
4. Branch feltöltése (`git push origin feature/új_funkció`)
5. Pull Request nyitása

## Licensz

MIT License - lásd a LICENSE fájlt a részletekért.

## További dokumentáció

- [API Dokumentáció](api.md)
- [Architektúra leírás](architecture.md)
- [Fejlesztési checklist](development_checklist.md)
- [Példák](examples.md)
