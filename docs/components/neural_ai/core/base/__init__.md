# neural_ai.core.base

A Neural AI core komponensek alap modulja.

## Áttekintés

Ez a modul tartalmazza a core komponensek közös alapjait és a dependency injection megvalósításához szükséges infrastruktúrát.

## Modulok

### `DIContainer`

A dependency injection container osztály, amely felelős a komponensek életciklusának és függőségeinek kezeléséért.

**További információ:** [`container`](container.md)

### `CoreComponents`

A core komponensek tárolója, amely a konfigurációt, loggert és storage-ot egyesíti.

**További információ:** [`core_components`](core_components.md)

### `CoreComponentFactory`

A core komponensek létrehozásáért felelős factory osztály.

**További információ:** [`factory`](factory.md)

## Használat

```python
from neural_ai.core.base import DIContainer, CoreComponents, CoreComponentFactory

# Core komponensek létrehozása a factory segítségével
core = CoreComponentFactory.create_components()

# Vagy manuálisan a DI containerrel
container = DIContainer()
config = container.get_config()
logger = container.get_logger()
storage = container.get_storage()
```

## Függőségi Injektálás

A modul támogatja a függőségi injektálást a `DIContainer` osztályon keresztül. Ez lehetővé teszi a komponensek lazítását és a tesztelhetőség javítását.

## Típusok

A modul szigorú típusellenőrzést használ, és minden osztályhoz tartoznak megfelelő interfészek.

## Kapcsolódó Dokumentáció

- [Core Dependencies](../../../development/core_dependencies.md)
- [Component Development Guide](../../../development/component_development_guide.md)