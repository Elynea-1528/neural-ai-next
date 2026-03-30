# 🧪 Teszt: tests/neural_ai/core/base/test_base_factory.py

**Tesztelt modul:** [`neural_ai/core/base/base_factory.py`](../../neural_ai/core/base/base_factory.py)

CoreComponentFactory tesztelése.

Ez a modul tartalmazza a CoreComponentFactory osztály egységtesztjeit,
beleértve a lazy loading, dependency injection és komponens létrehozási
funkcionalitás tesztelését.

## Teszt Osztály: `DummyLogger`

## Teszt Osztály: `DummyLogger`

## Teszt Osztály: `DummyLogger`

## Teszt Osztály: `InvalidLogger`

## Teszt Osztály: `DummyConfigManager`

## Teszt Osztály: `TestCoreComponentFactory`

CoreComponentFactory osztály tesztjei.

### ✓ `test_init_with_container()`

Teszteli a factory inicializálását DI konténerrel.

## Teszt Függvények

### ✓ `test_logger_property_returns_logger()`

Teszteli, hogy a logger property logger interfészt ad vissza.

### ✓ `test_config_manager_property_raises_dependency_error()`

Teszteli, hogy a config manager property DependencyError-t dob, ha nincs regisztrálva.

### ✓ `test_storage_property_raises_dependency_error()`

Teszteli, hogy a storage property DependencyError-t dob, ha nincs regisztrálva.

### ✓ `test_reset_lazy_loaders()`

Teszteli a lazy loader-ek visszaállítását.

### ✓ `test_validate_dependencies_storage_missing_base_directory()`

Teszteli a storage függőség validálását hiányzó base_path esetén.

### ✓ `test_validate_dependencies_storage_invalid_path()`

Teszteli a storage függőség validálását érvénytelen elérési úttal.

### ✓ `test_validate_dependencies_storage_valid()`

Teszteli a storage függőség validálását érvényes konfiggal.

### ✓ `test_validate_dependencies_logger_missing_name()`

Teszteli a logger függőség validálását hiányzó névvel.

### ✓ `test_validate_dependencies_logger_valid()`

Teszteli a logger függőség validálását érvényes konfiggal.

### ✓ `test_validate_dependencies_config_manager_missing_path()`

Teszteli a config manager függőség validálását hiányzó fájlúttal.

### ✓ `test_validate_dependencies_config_manager_nonexistent_file()`

Teszteli a config manager függőség validálását nem létező fájllal.

### ✓ `test_validate_dependencies_config_manager_valid()`

Teszteli a config manager függőség validálását érvényes konfiggal.

### ✓ `test_validate_dependencies_invalid_component_type()`

Teszteli a függőség validálását érvénytelen komponens típussal.

### ✓ `test_create_components_with_all_paths()`

Teszteli a komponensek létrehozását minden elérési úttal.

### ✓ `test_create_with_container()`

Teszteli a komponensek létrehozását meglévő konténerből.

### ✓ `test_create_minimal_with_config_file()`

Teszteli a minimális komponensek létrehozását config fájllal.

### ✓ `test_create_minimal_without_config_file()`

Teszteli a minimális komponensek létrehozását config fájl nélkül.

### ✓ `test_create_minimal_with_config_file_no_logger_section()`

Teszteli a komponensek létrehozását config fájllal, de logger section nélkül.

### ✓ `test_create_logger()`

Teszteli a logger létrehozását (funkcionális teszt).

### ✓ `test_create_logger_invalid_config()`

Teszteli a logger létrehozását érvénytelen konfiggal.

### ✓ `test_create_config_manager()`

Teszteli a config manager létrehozását.

### ✓ `test_create_config_manager_invalid_path()`

Teszteli a config manager létrehozását érvénytelen elérési úttal.

### ✓ `test_create_storage()`

Teszteli a storage létrehozását.

### ✓ `test_create_storage_invalid_path()`

Teszteli a storage létrehozását érvénytelen elérési úttal.

### ✓ `test_lazy_property_decorator_exists()`

Teszteli, hogy a lazy property dekorátorok léteznek.

### ✓ `test_component_cache_lazy_property()`

Teszteli a komponens gyorsítótár lazy property működését.

### ✓ `test_get_logger_with_registered_logger()`

Teszteli a logger property-t regisztrált loggerrel (funkcionális teszt).

### ✓ `test_get_logger_fallback_to_default_logger_factory()`

Teszteli, hogy a logger property fallbackel a LoggerFactory-ra (funkcionális teszt).

### ✓ `test_get_logger_with_invalid_logger_raises_dependency_error()`

Teszteli, hogy érvénytelen logger DependencyError-t dob (funkcionális teszt).

### ✓ `test_get_config_manager_with_registered_config()`

Teszteli a _get_config_manager metódust regisztrált config managerrel (funkcionális teszt).

### ✓ `test_get_storage_raises_dependency_error_if_not_found()`

Teszteli, hogy a _get_storage DependencyError-t dob, ha nincs regisztrálva.

### ✓ `test_expensive_config_lazy_property()`

Teszteli az _expensive_config lazy property működését (111-114. sorok).

### ✓ `test_process_config()`

Teszteli a _process_config metódust (125. sor).

### ✓ `test_reset_lazy_loaders_clears_lazy_properties()`

Teszteli, hogy a reset_lazy_loaders törli a lazy property-ket (146. sor).

---

**Teszt fájl:** [`tests/neural_ai/core/base/test_base_factory.py`](../../tests/neural_ai/core/base/test_base_factory.py)

**Tesztelt modul:** [`neural_ai/core/base/base_factory.py`](../../neural_ai/core/base/base_factory.py)
