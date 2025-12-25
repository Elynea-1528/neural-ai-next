# Core Base Modul - Alap komponensek

## Áttekintés

Ez a modul tartalmazza a Neural AI Next projekt core komponenseinek közös alapjait és a dependency injection (DI) megvalósításához szükséges infrastruktúrát.

## Importált osztályok

### `CoreComponentFactory`
A core komponensek (config, logger, storage) létrehozásáért és kezeléséért felelős factory osztály.

**Hely:** [`neural_ai.core.base.factory`](neural_ai/core/base/factory.py:27)

**Feladat:** Biztosítja a komponensek egységes létrehozását dependency injection pattern használatával, lazy loadinggel és singleton mintával.

### `CoreComponents`
Core komponensek gyűjteménye, amely lusta betöltéssel és DI konténerrel rendelkezik.

**Hely:** [`neural_ai.core.base.implementations.component_bundle`](neural_ai/core/base/implementations/component_bundle.py:74)

**Feladat:** Egyesíti a config, logger és storage komponenseket, és biztosítja azok egységes elérését.

### `DIContainer`
Egyszerű dependency injection konténer a komponensek közötti függőségek kezelésére.

**Hely:** [`neural_ai.core.base.implementations.di_container`](neural_ai/core/base/implementations/di_container.py:57)

**Feladat:** Kezeli a komponensek regisztrációját, feloldását és lusta betöltését.

## Használati példa

```python
from neural_ai.core.base import CoreComponentFactory, CoreComponents, DIContainer

# Konténer létrehozása
container = DIContainer()

# Core komponensek létrehozása
components = CoreComponentFactory.create_with_container(container)

# Komponensek elérése
config = components.config
logger = components.logger
storage = components.storage
```

## Függőségek

- `typing.TYPE_CHECKING`: Körkörös importok elkerüléséhez
- `neural_ai.core.base.factory`: Factory implementáció
- `neural_ai.core.base.implementations.component_bundle`: Komponens gyűjtemény
- `neural_ai.core.base.implementations.di_container`: DI konténer

## Jellemzők

- **Dependency Injection:** Minden komponens DI konténeren keresztül kapja meg függőségeit
- **Lazy Loading:** A drága erőforrások csak akkor töltődnek be, amikor szükség van rájuk
- **Singleton Pattern:** Biztosítja, hogy minden komponensből csak egy példány létezzen
- **Type Safety:** Erős típusosság a `TYPE_CHECKING` segítségével

## Kapcsolódó dokumentáció

- [Core Component Factory](neural_ai/core/base/factory.md)
- [Core Components](neural_ai/core/base/implementations/component_bundle.md)
- [DI Container](neural_ai/core/base/implementations/di_container.md)