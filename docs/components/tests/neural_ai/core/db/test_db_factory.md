# 🧪 Teszt: tests/neural_ai/core/db/test_db_factory.py

**Tesztelt modul:** [`neural_ai/core/db/db_factory.py`](../../neural_ai/core/db/db_factory.py)

Tesztek a neural_ai.core.db.factory modulhoz.

Ez a modul tartalmazza a DatabaseFactory osztály és annak metódusainak tesztjeit.

## Teszt Osztály: `TestDatabaseFactory`

DatabaseFactory osztály tesztjei.

### ✓ `test_get_session_maker_without_config()`

Teszteli a session maker lekérdezést konfig nélkül.

### ✓ `test_get_session_maker_with_config()`

Teszteli a session maker lekérdezést konfiggal.

### ✓ `test_get_engine_without_config()`

Teszteli az engine lekérdezést konfig nélkül.

### ✓ `test_get_engine_with_config()`

Teszteli az engine lekérdezést konfiggal.

### ✓ `test_create_engine_with_custom_url()`

Teszteli az egyéni engine létrehozást.

### ✓ `test_create_engine_with_echo_enabled()`

Teszteli az engine létrehozást echo módban.

### ✓ `test_create_manager_without_config()`

Teszteli a DatabaseManager létrehozást konfig nélkül.

### ✓ `test_create_manager_with_config()`

Teszteli a DatabaseManager létrehozást konfiggal.

### ✓ `test_get_session_maker_caches_result()`

Teszteli, hogy a session maker cache-elődik a modul szintjén.

### ✓ `test_get_engine_caches_result()`

Teszteli, hogy az engine cache-elődik a modul szintjén.

### ✓ `test_create_engine_different_urls()`

Teszteli az engine létrehozást különböző URL-ekkel.

### ✓ `test_factory_methods_return_consistent_types()`

Teszteli, hogy a factory metódusok konzisztens típusokat adnak vissza.

### ✓ `test_factory_is_stateless()`

Teszteli, hogy a factory osztály állapotmentes-e.

## Teszt Osztály: `TestDatabaseConfigPydanticValidation`

Pydantic DatabaseConfig validációs tesztek.

Ezek a tesztek ellenőrzik a DatabaseConfig Pydantic model működését,
beleértve a URL formátum validációt és a pool size ellenőrzést.

### ✓ `test_database_config_valid_sqlite_url()`

Érvényes SQLite URL validálása.

### ✓ `test_database_config_valid_postgresql_url()`

Érvényes PostgreSQL URL validálása.

### ✓ `test_database_config_valid_mysql_url()`

Érvényes MySQL URL validálása.

### ✓ `test_database_config_invalid_url_raises_error()`

Érvénytelen URL formátum hibát dob.

### ✓ `test_database_config_missing_url_raises_error()`

Hiányzó URL esetén hibát dob.

### ✓ `test_database_config_pool_size_validation_valid()`

Pool size >= 1 esetén sikeres validáció.

### ✓ `test_database_config_pool_size_validation_invalid()`

Pool size < 1 esetén hibát dob.

### ✓ `test_database_config_pool_optional()`

Pool konfig opcionális - None is érvényes.

### ✓ `test_factory_with_real_yaml_config()`

Factory valós YAML konfigurációval.

---

**Teszt fájl:** [`tests/neural_ai/core/db/test_db_factory.py`](../../tests/neural_ai/core/db/test_db_factory.py)

**Tesztelt modul:** [`neural_ai/core/db/db_factory.py`](../../neural_ai/core/db/db_factory.py)
