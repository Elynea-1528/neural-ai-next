# Teszt Factory Coverage - Core Base Modul

## Áttekintés

Ez a dokumentáció a [`tests/core/base/test_factory_coverage.py`](../../../../tests/core/base/test_factory_coverage.py) tesztfájlt dokumentálja, amely a [`neural_ai.core.base.factory`](../../../neural_ai/core/base/factory.md) modul tesztelését és stabilizálását célozza meg.

## Cél

A tesztfájl célja a `CoreComponentFactory` osztály stabilizálása és a kódlefedettség növelése. A tesztek a következőkre fókuszálnak:
- A **DI (Dependency Injection) elv** betartásának ellenőrzése.
- A **hibakezelés** és **fallback viselkedés** tesztelése.
- A **lazy loading** mechanizmus ellenőrzése.
- A **belső metódusok** funkcionalitásának biztosítása.

## Tesztesetek

### 1. Logger Komponens Tesztek

#### `test_get_logger_with_fallback`
- **Cél:** Teszteli a logger lekérdezést fallback-kel, amikor nincs regisztrálva a konténerben.
- **Elvárás:** Ha a DI konténer nem tartalmaz logger komponenst, a factory egy alapértelmezett logger példányt ad vissza (NullObject pattern). A teszt a logger létezését és alapvető metódusait ellenőrzi (`info`, `debug`, `warning`, `error`), ami robusztusabb, mint az `isinstance()` használata.
- **Stabilizálás:** A teszt nem támaszkodik a konkrét `DefaultLogger` osztályra, hanem a funkcionalitását ellenőrzi, így betartva a DI elvet.

### 2. Config Manager Tesztek

#### `test_get_config_manager_raises_dependency_error`
- **Cél:** Teszteli a config manager lekérdezését, ha az nem elérhető.
- **Elvárás:** `DependencyError` kivételt dob, ha a config manager nincs regisztrálva a DI konténerben.

### 3. Storage Komponens Tesztek

#### `test_get_storage_raises_dependency_error`
- **Cél:** Teszteli a storage lekérdezését, ha az nem elérhető.
- **Elvárás:** `DependencyError` kivételt dob, ha a storage nincs regisztrálva a DI konténerben.

### 4. Belső Metódus Tesztek

#### `test_process_config_returns_config`
- **Cél:** Teszteli a `_process_config` metódust.
- **Elvárás:** Visszaadja a kapott konfigurációs dictionary-t.

#### `test_load_component_cache_returns_empty_dict`
- **Cél:** Teszteli a `_load_component_cache` metódust.
- **Elvárás:** Üres dictionary-t ad vissza az alapértelmezett implementációban.

### 5. Property Hozzáférési Tesztek

#### `test_property_accessors`
- **Cél:** Teszteli a property hozzáférési metódusokat.
- **Elvárás:** `DependencyError`-t dob, ha a `config_manager` vagy `storage` property-ket megpróbáljuk elérni, de a hozzájuk tartozó komponens nincs regisztrálva.

### 6. Lazy Property Tesztek

#### `test_lazy_properties`
- **Cél:** Teszteli a lazy property-k létezését és működését.
- **Elvárás:** A `_expensive_config` és `_component_cache` lazy property-k léteznek az osztályon, és csak akkor futnak le, amikor először hozzáférnek hozzájuk.

#### `test_reset_lazy_loaders`
- **Cél:** Teszteli a lazy loader-ek visszaállítását.
- **Elvárás:** A `reset_lazy_loaders` metódus sikeresen visszaállítja az összes lazy loader állapotát anélkül, hogy kivételt dobna.

### 7. Függőség Validáció Tesztek

#### `test_validate_dependencies_storage`
- **Cél:** Teszteli a függőség validációt storage-hoz.
- **Elvárás:** `ConfigurationError`-t dob, ha a `base_directory` nincs konfigurálva.

#### `test_validate_dependencies_storage_invalid_path`
- **Cél:** Teszteli a függőség validációt storage-hoz érvénytelen úttal.
- **Elvárás:** `ConfigurationError`-t dob, ha a `base_directory` szülőkönyvtára nem létezik.

#### `test_validate_dependencies_logger`
- **Cél:** Teszteli a függőség validációt logger-hez.
- **Elvárás:** `ConfigurationError`-t dob, ha a `name` nincs konfigurálva.

#### `test_validate_dependencies_config_manager`
- **Cél:** Teszteli a függőség validációt config manager-hez.
- **Elvárás:** `ConfigurationError`-t dob, ha a `config_file_path` nincs konfigurálva.

#### `test_validate_dependencies_config_manager_invalid_path`
- **Cél:** Teszteli a függőség validációt config manager-hez érvénytelen úttal.
- **Elvárás:** `ConfigurationError`-t dob, ha a `config_file_path` által mutatott fájl nem létezik.

### 8. Komponens Létrehozási Tesztek

#### `test_create_components_without_config`
- **Cél:** Teszteli a komponensek létrehozását konfiguráció nélkül.
- **Elvárás:** Sikeresen létrehozza a komponenseket alapértelmezett beállításokkal.

#### `test_create_components_with_config_only`
- **Cél:** Teszteli a komponensek létrehozását csak konfigurációs fájllal.
- **Elvárás:** Sikeresen inicializálja a komponenseket a megadott konfigurációval.

#### `test_create_components_with_storage_path`
- **Cél:** Teszteli a komponensek létrehozását storage úttal.
- **Elvárás:** Sikeresen inicializálja a storage komponenst a megadott elérési úttal.

#### `test_create_with_container`
- **Cél:** Teszteli a komponensek létrehozását meglévő konténerből.
- **Elvárás:** Sikeresen létrehozza a `CoreComponents` példányt a megadott DI konténerrel.

#### `test_create_minimal_with_existing_config`
- **Cél:** Teszteli a minimális komponensek létrehozását létező configgel.
- **Elvárás:** Sikeresen létrehozza a komponenseket a létező `config.yml` fájl alapján.

#### `test_create_minimal_no_config`
- **Cél:** Teszteli a minimális komponensek létrehozását config nélkül.
- **Elvárás:** Sikeresen létrehozza a komponenseket alapértelmezett konfigurációval, ha a `config.yml` nem létezik.

### 9. Egyedi Komponens Létrehozási Tesztek

#### `test_create_logger_with_config_dict`
- **Cél:** Teszteli a logger létrehozását konfigurációs dictionary-vel.
- **Elvárás:** Sikeresen létrehozza a loggert a megadott konfigurációs beállításokkal.

#### `test_create_config_manager_with_config_dict`
- **Cél:** Teszteli a config manager létrehozását konfigurációs dictionary-vel.
- **Elvárás:** Sikeresen létrehozza a config managert a további konfigurációs paraméterekkel.

#### `test_create_storage_with_config_dict`
- **Cél:** Teszteli a storage létrehozását konfigurációs dictionary-vel.
- **Elvárás:** Sikeresen létrehozza a storage-t a további konfigurációs paraméterekkel.

## Metrikák

- **Összes teszteset:** 22
- **Aktuális kódlefedettség:** 89%
- **Státusz:** ✅ Stabilizálva

## Futtatás

```bash
# Összes teszt futtatása
pytest tests/core/base/test_factory_coverage.py -v

# Tesztek futtatása coverage-jel
pytest tests/core/base/test_factory_coverage.py --cov=neural_ai.core.base.factory --cov-report=term-missing

# Linter ellenőrzés
ruff check tests/core/base/test_factory_coverage.py
```

## Kapcsolódó Dokumentáció

- [`neural_ai.core.base.factory`](../../../neural_ai/core/base/factory.md) - A tesztelt osztály dokumentációja
- [`tests/core/base/test_core_components.py`](../test_core_components.md) - Alapvető komponens tesztek
- [Architektúra Szabványok](../../../development/architecture_standards.md) - A projekt architektúra szabványai