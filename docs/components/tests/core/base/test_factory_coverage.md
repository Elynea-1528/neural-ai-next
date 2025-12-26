# Test Factory Coverage - Core Base Modul

## Áttekintés

Ez a dokumentáció a [`tests/core/base/test_factory_coverage.py`](../../../../tests/core/base/test_factory_coverage.py) tesztfájlt dokumentálja, amely a [`neural_ai.core.base.factory`](../../../neural_ai/core/base/factory.md) modul hiányzó sorainak lefedését célozza meg.

## Cél

A tesztfájl célja, hogy a `CoreComponentFactory` osztály 100%-os kódlefedettségét biztosítsa. A meglévő tesztek mellett további teszteseteket tartalmaz, amelyek a hiányzó sorokat és ágakat fedik le.

## Tesztesetek

### 1. Logger Komponens Tesztek

#### `test_get_logger_with_fallback`
- **Cél:** Teszteli a logger lekérdezést fallback-kel
- **Hiányzó sorok:** 53-65
- **Elvárás:** Ha nincs logger regisztrálva a konténerben, a factory visszaad egy `DefaultLogger` példányt

### 2. Config Manager Tesztek

#### `test_get_config_manager_raises_dependency_error`
- **Cél:** Teszteli a config manager lekérdezést, ha nincs elérhető
- **Hiányzó sorok:** 69-78
- **Elvárás:** `DependencyError` kivételt dob, ha a config manager nem érhető el

### 3. Storage Komponens Tesztek

#### `test_get_storage_raises_dependency_error`
- **Cél:** Teszteli a storage lekérdezést, ha nincs elérhető
- **Hiányzó sorok:** 82-89
- **Elvárás:** `DependencyError` kivételt dob, ha a storage nem érhető el

### 4. Belső Metódus Tesztek

#### `test_process_config_returns_config`
- **Cél:** Teszteli a `_process_config` metódust
- **Hiányzó sorok:** 119
- **Elvárás:** Visszaadja a kapott konfigurációt

#### `test_load_component_cache_returns_empty_dict`
- **Cél:** Teszteli a `_load_component_cache` metódust
- **Hiányzó sorok:** 129
- **Elvárás:** Üres dictionary-t ad vissza

### 5. Property Hozzáférési Tesztek

#### `test_property_accessors`
- **Cél:** Teszteli a property hozzáférési metódusokat
- **Hiányzó sorok:** 94, 99, 104
- **Elvárás:** `DependencyError`-t dob, ha a komponens nem érhető el

### 6. Lazy Property Tesztek

#### `test_lazy_properties`
- **Cél:** Teszteli a lazy property-kat
- **Hiányzó sorok:** 110-113, 119
- **Elvárás:** A lazy property-k csak akkor futnak le, ha először hozzáférésük van

#### `test_reset_lazy_loaders`
- **Cél:** Teszteli a lazy loader-ek visszaállítását
- **Hiányzó sorok:** 138-145
- **Elvárás:** Sikeresen visszaállítja a lazy loader-eket

### 7. Függőség Validáció Tesztek

#### `test_validate_dependencies_storage`
- **Cél:** Teszteli a függőség validációt storage-hoz
- **Hiányzó sorok:** 169
- **Elvárás:** `ConfigurationError`-t dob, ha nincs `base_directory` konfigurálva

#### `test_validate_dependencies_storage_invalid_path`
- **Cél:** Teszteli a függőség validációt storage-hoz érvénytelen úttal
- **Hiányzó sorok:** 177
- **Elvárás:** `ConfigurationError`-t dob, ha az útvonal érvénytelen

#### `test_validate_dependencies_logger`
- **Cél:** Teszteli a függőség validációt logger-hez
- **Hiányzó sorok:** 184
- **Elvárás:** `ConfigurationError`-t dob, ha nincs `name` konfigurálva

#### `test_validate_dependencies_config_manager`
- **Cél:** Teszteli a függőség validációt config manager-hez
- **Hiányzó sorok:** 191
- **Elvárás:** `ConfigurationError`-t dob, ha nincs `config_file_path` konfigurálva

#### `test_validate_dependencies_config_manager_invalid_path`
- **Cél:** Teszteli a függőség validációt config manager-hez érvénytelen úttal
- **Hiányzó sorok:** 198
- **Elvárás:** `ConfigurationError`-t dob, ha a konfigurációs fájl nem létezik

### 8. Komponens Létrehozási Tesztek

#### `test_create_components_without_config`
- **Cél:** Teszteli a komponensek létrehozását konfig nélkül
- **Elvárás:** Sikeresen létrehozza a komponenseket

#### `test_create_components_with_config_only`
- **Cél:** Teszteli a komponensek létrehozását csak konfiggal
- **Elvárás:** Sikeresen létrehozza a komponenseket

#### `test_create_components_with_storage_path`
- **Cél:** Teszteli a komponensek létrehozását storage úttal
- **Hiányzó sorok:** 244, 256-257
- **Elvárás:** Sikeresen létrehozza a komponenseket

#### `test_create_with_container`
- **Cél:** Teszteli a komponensek létrehozását konténerből
- **Hiányzó sorok:** 279-281
- **Elvárás:** Sikeresen létrehozza a komponenseket

#### `test_create_minimal_with_existing_config`
- **Cél:** Teszteli a minimális komponensek létrehozását létező configgel
- **Hiányzó sorok:** 307-308
- **Elvárás:** Sikeresen létrehozza a komponenseket

#### `test_create_minimal_no_config`
- **Cél:** Teszteli a minimális komponensek létrehozását config nélkül
- **Hiányzó sorok:** 308-311, 326
- **Elvárás:** Sikeresen létrehozza a komponenseket alapértelmezett konfigurációval

### 9. Egyedi Komponens Létrehozási Tesztek

#### `test_create_logger_with_config_dict`
- **Cél:** Teszteli a logger létrehozását konfigurációs dictionary-vel
- **Elvárás:** Sikeresen létrehozza a loggert

#### `test_create_config_manager_with_config_dict`
- **Cél:** Teszteli a config manager létrehozását konfigurációs dictionary-vel
- **Elvárás:** Sikeresen létrehozza a config managert

#### `test_create_storage_with_config_dict`
- **Cél:** Teszteli a storage létrehozását konfigurációs dictionary-vel
- **Elvárás:** Sikeresen létrehozza a storage-t

## Metrikák

- **Összes teszteset:** 22
- **Cél kódlefedettség:** 100%
- **Aktuális kódlefedettség:** 89%
- **Hiányzó sorok:** 18 sor

## Futtatás

```bash
# Tesztek futtatása coverage-jel
pytest tests/core/base/test_factory_coverage.py --cov=neural_ai.core.base.factory --cov-report=term-missing

# Linter ellenőrzés
ruff check tests/core/base/test_factory_coverage.py
```

## Kapcsolódó Dokumentáció

- [`neural_ai.core.base.factory`](../../../neural_ai/core/base/factory.md) - A tesztelt osztály dokumentációja
- [`tests/core/base/test_core_components.py`](../test_core_components.md) - Alapvető komponens tesztek
- [Architektúra Szabványok](../../../development/architecture_standards.md) - A projekt architektúra szabványai