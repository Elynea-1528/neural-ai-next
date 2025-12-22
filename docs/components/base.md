# Base Modul

## Áttekintés

A `neural_ai.core.base` modul a Neural AI Next rendszer alapvető komponenseinek közös alapjait és a dependency injection (DI) megvalósításához szükséges infrastruktúrát tartalmazza. Ez a modul biztosítja a rendszer magjának a rugalmasságát, tesztelhetőségét és karbantarthatóságát.

## Komponensek

### DIContainer

A `DIContainer` (Dependency Injection Container) a rendszer függőségi injekciójának magja. Ez az osztály felelős azért, hogy a különböző komponensek egymástól függetlenül hozhatóak legyenek létre, és a függőségeiket a konténer biztosítja.

**Főbb jellemzők:**
- Singleton minta alkalmazása
- Komponens regisztráció és feloldás
- Életciklus kezelés

### CoreComponents

A `CoreComponents` osztály a rendszer alapvető komponenseinek gyűjteményét és koordinációját végzi. Ez az osztály felelős azért, hogy a rendszer különböző részei egységesen és koordináltan működjenek.

**Főbb jellemzők:**
- Alapkomponensek centralizált kezelése
- Konfiguráció kezelés
- Életciklus koordináció

### CoreComponentFactory

A `CoreComponentFactory` egy gyártó osztály, amely a rendszer komponenseinek létrehozását végzi. Ez az osztály felelős azért, hogy a komponensek egységes és konzisztens módon jöjjenek létre.

**Főbb jellemzők:**
- Komponens létrehozás egységes interfész mögött
- Konfiguráció alapú inicializáció
- Hibakezelés és validáció

## Használat

### Alapvető importálás

```python
from neural_ai.core.base import DIContainer, CoreComponents, CoreComponentFactory

# DIContainer példányosítás
container = DIContainer()

# CoreComponents inicializálás
components = CoreComponents()

# CoreComponentFactory használata
factory = CoreComponentFactory()
```

### Függőségi injekció használata

```python
from neural_ai.core.base import DIContainer

# Konténer példányosítás
container = DIContainer()

# Szolgáltatás regisztráció
container.register_service('my_service', MyServiceImplementation)

# Szolgáltatás lekérdezése
my_service = container.resolve('my_service')
```

## Architektúra

A base modul a következő fontos tervezési mintákat alkalmazza:

1. **Dependency Injection (DI):** A komponensek függőségeit kívülről injektáljuk, ami javítja a tesztelhetőséget és a rugalmasságot.

2. **Singleton Pattern:** A DIContainer singleton mintát alkalmaz, hogy biztosítsa a konténer egyediségét az egész alkalmazásban.

3. **Factory Pattern:** A CoreComponentFactory gyártó mintát alkalmaz a komponensek létrehozásához.

4. **Interface Segregation:** A komponensek jól definiált interfészeken keresztül kommunikálnak egymással.

## Fejlesztési elvek

A base modul fejlesztése során a következő elveket tartjuk be:

- **Típusbiztonság:** Minden komponensnek rendelkeznie kell megfelelő típusannotációkkal.
- **Tesztelhetőség:** A komponensek egységtesztelhetőek legyenek.
- **Dokumentáció:** Minden komponens rendelkezzen átfogó dokumentációval.
- **Hibakezelés:** A komponenseknek konzisztens hibakezelést kell biztosítaniuk.

## Kapcsolódó dokumentáció

- [Container dokumentáció](container.md)
- [Core Components dokumentáció](core_components.md)
- [Factory dokumentáció](factory.md)
- [Dependency Injection útmutató](../../development/implementation_guide.md)
