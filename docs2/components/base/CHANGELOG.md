# Változások Naplója

## Áttekintés

Ez a dokumentum a Base komponens változásainak teljes történetét tartalmazza. A változások a legújabbtól a legrégebbiig vannak rendezve.

## [1.0.0] - 2025-12-19

### Hozzáadva

#### Főbb funkciók

- **Dependency Injection (DI) Konténer** - [`DIContainer`](api/container.md) osztály implementációja
  - Példány regisztráció és feloldás
  - Factory függvények támogatása
  - Lazy loading támogatás
  - Singleton minta kényszerítése
  - Memóriahasználat monitorozása

- **Core Komponensek** - [`CoreComponents`](api/core_components.md) osztály
  - Egységes komponens elérés (logger, config, storage)
  - Lazy loading támogatás
  - Komponens validáció
  - Preload funkció

- **Komponens Factory** - [`CoreComponentFactory`](api/factory.md) osztály
  - Komponensek létrehozása és konfigurálása
  - Függőség validáció
  - Singleton mintázat
  - Több létrehozási mód (teljes, minimális, egyedi konténerrel)

- **Lazy Loading Mechanizmus** - [`LazyLoader`](api/lazy_loading.md) osztály
  - Erőforrások lustabetöltése
  - Thread-safe működés
  - Reset funkció teszteléshez
  - `lazy_property` dekorátor

- **Singleton Minta** - [`SingletonMeta`](api/singleton.md) metaclass
  - Metaclass alapú implementáció
  - Thread-safe működés
  - Egyszerű használat

- **Kivétel Hierarchia** - [`exceptions.py`](api/exceptions.md) modul
  - `NeuralAIException` - Alap kivétel
  - `StorageException` és leszármazottai
  - `ConfigurationError`
  - `DependencyError`
  - `SingletonViolationError`
  - `ComponentNotFoundError`
  - `NetworkException` és leszármazottai

#### Dokumentáció

- **Teljes API dokumentáció**
  - [`README.md`](README.md) - Áttekintés és gyors kezdés
  - [`api/overview.md`](api/overview.md) - API áttekintés
  - [`api/container.md`](api/container.md) - DIContainer API
  - [`api/core_components.md`](api/core_components.md) - CoreComponents API
  - [`api/factory.md`](api/factory.md) - CoreComponentFactory API
  - [`api/exceptions.md`](api/exceptions.md) - Kivétel hierarchia
  - [`api/lazy_loading.md`](api/lazy_loading.md) - Lazy Loading API
  - [`api/singleton.md`](api/singleton.md) - Singleton API

- **Architektúra dokumentáció**
  - [`architecture/overview.md`](architecture/overview.md) - Architektúra áttekintés
  - [`function_call_map.md`](function_call_map.md) - Funkció-hívási térkép

- **Példák**
  - [`examples/basic_usage.md`](examples/basic_usage.md) - Alapvető használati példák

#### Tesztelés

- **Egységtesztek** - A főbb komponensek tesztelése
- **Integrációs tesztek** - Komponensek közötti interakciók tesztelése
- **Teljesítménytesztek** - Lazy loading és singleton hatékonyságának mérése

### Módosítva

- Nincs módosítás (első verzió)

### Eltávolítva

- Nincs eltávolítás (első verzió)

### Javítva

- Nincs javítás (első verzió)

### Biztonsági frissítések

- **Thread Safety** - Minden komponens szálbiztos működése
- **Singleton Protection** - Singleton minta megfelelő védelme
- **Error Handling** - Átfogó hibakezelés és kivétel hierarchia

### Függőségek

#### Hozzáadva

- `typing` - Típusannotációk támogatása
- `threading` - Szálbiztos működés
- `logging` - Naplózás támogatása
- `pathlib` - Fájlútkezelés
- `dataclasses` - Adatosztályok támogatása
- `functools` - Dekorátorok támogatása

#### Módosítva

- Nincs módosítás (első verzió)

#### Eltávolítva

- Nincs eltávolítás (első verzió)

### Deprecated

- Nincs deprecated funkció (első verzió)

### Breaking Changes

- Nincs breaking change (első verzió)

## [0.9.0] - 2025-12-01

### Hozzáadva

#### Előzetes funkciók

- **Alap konténer struktúra** - Kezdetleges DI konténer implementáció
- **Komponens váz** - Core komponensek vázlatos implementációja
- **Factory minta** - Alap factory osztály

#### Dokumentáció

- **Kezdetleges dokumentáció** - Alapvető leírások és példák

### Módosítva

- Nincs módosítás (előzetes verzió)

### Eltávolítva

- Nincs eltávolítás (előzetes verzió)

### Javítva

- Nincs javítás (előzetes verzió)

## Verziószámozási stratégia

A Base komponens a [Semantic Versioning](https://semver.org/) szabványt követi: `MAJOR.MINOR.PATCH`

- **MAJOR**: Kompatibilitástörő változások
- **MINOR**: Új funkciók, visszamenőlegesen kompatibilis változások
- **PATCH**: Hibajavítások, visszamenőlegesen kompatibilis változások

### Verzió történet

```
1.0.0 (2025-12-19) - Első stabil verzió
  └─ 0.9.0 (2025-12-01) - Előzetes verzió
```

## Kiadási jegyzetek

### 1.0.0 - Első stabil verzió

**Dátum:** 2025-12-19

**Főbb jellemzők:**
- Teljes körű DI konténer implementáció
- Lazy loading támogatás
- Singleton minta
- Átfogó kivétel hierarchia
- Szálbiztos működés
- Teljes dokumentáció

**Ismert problémák:**
- Nincs ismert probléma

**Jövőbeli tervek:**
- További optimalizációk
- Új komponensek hozzáadása
- További dokumentáció

**Köszönetnyilvánítás:**
- A Base komponens csapatának
- A tesztelő csapatnak
- A dokumentáció íróinak

## Migrációs útmutatók

### 0.9.0-ről 1.0.0-ra

#### Breaking Changes

Nincsenek breaking changes, mivel az 1.0.0 az első stabil verzió.

#### Új funkciók használata

```python
# Régi módszer (0.9.0)
from neural_ai.core.base import BasicContainer

container = BasicContainer()
container.register('service', MyService())

# Új módszer (1.0.0)
from neural_ai.core.base import DIContainer, CoreComponentFactory

# 1. DIContainer használata
container = DIContainer()
container.register_instance(MyInterface, MyService())

# 2. Factory használata (ajánlott)
components = CoreComponentFactory.create_components(
    config_path='config.yaml',
    log_path='app.log',
    storage_path='./data'
)
```

## Fejlesztői információk

### Verziókezelés

A verziószámokat a következő fájlokban kell frissíteni:

- [`pyproject.toml`](../../../pyproject.toml) - Projekt verzió
- [`CHANGELOG.md`](CHANGELOG.md) - Változások naplója
- Dokumentációk - Verzió információk

### Kiadási folyamat

1. **Verzió növelése** - A megfelelő verziószám beállítása
2. **CHANGELOG frissítése** - Az összes változás dokumentálása
3. **Tesztelés** - Komplett tesztelés végrehajtása
4. **Dokumentáció frissítése** - Új funkciók dokumentálása
5. **Kiadás** - Verzió kiadása és címkézése
6. **Közlemény** - Kiadási jegyzetek közzététele

### Verzió címkézés

```bash
# Verzió címke létrehozása
git tag -a v1.0.0 -m "Base komponens 1.0.0 kiadása"

# Címke leküldése
git push origin v1.0.0
```

## Kapcsolódó dokumentáció

- [API Áttekintés](api/overview.md)
- [Architektúra áttekintés](architecture/overview.md)
- [Fejlesztési útmutató](../development/component_development_guide.md)
- [Kiadási jegyzetek](#kiadási-jegyzetek)

## Visszajelzés

Ha bármilyen problémát észlelsz vagy javaslatod van, kérjük nyiss egy issue-t a projekt GitHub repository-jában.

---

**Utolsó frissítés:** 2025-12-19
**Verzió:** 1.0.0
**Felelős:** Base Komponens Csapat
