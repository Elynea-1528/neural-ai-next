# 🧪 Teszt: tests/neural_ai/core/db/implementations/test_sqlalchemy_session.py

**Tesztelt modul:** [`neural_ai/core/db/implementations/sqlalchemy_session.py`](../../neural_ai/core/db/implementations/sqlalchemy_session.py)

Tesztek a neural_ai.core.db.implementations.sqlalchemy_session modulhoz.

# pyright: reportUnknownArgumentType=false, reportUnknownMemberType=false
# SQLAlchemy async session fixture type hibák.

Ez a modul tartalmazza az adatbázis session kezelő függvények és osztályok tesztjeit.

## Teszt Osztály: `TestDatabaseURL`

Adatbázis URL lekérdezés tesztjei.

### ✓ `test_get_database_url_with_provided_config()`

Teszteli az adatbázis URL lekérdezést megadott konfiggal.

### ✓ `test_get_database_url_fallback_to_env()`

Teszteli az adatbázis URL lekérdezést env fallbackkel.

### ✓ `test_get_database_url_with_non_dict_config()`

Teszteli az adatbázis URL lekérdezést nem dict config esetén (line 57).

### ✓ `test_get_database_url_without_config()`

Teszteli az adatbázis URL lekérdezést konfig nélkül (line 47).

### ✓ `test_get_database_url_raises_error_when_missing()`

Teszteli, hogy a függvény hibát dob, ha az URL hiányzik.

## Teszt Osztály: `TestCreateEngine`

Engine létrehozás tesztjei.

### ✓ `test_create_engine_sqlite()`

Teszteli az engine létrehozást SQLite URL-lel.

### ✓ `test_create_engine_with_echo()`

Teszteli az engine létrehozást echo módban.

### ✓ `test_create_engine_postgresql()`

Teszteli az engine létrehozást PostgreSQL URL-lel (line 114).

### ✓ `test_create_engine_postgresql_with_pool_config()`

Teszteli az engine létrehozást custom pool config-gal (line 115-116).

### ✓ `test_create_engine_postgresql_with_none_pool_values()`

Teszteli az engine létrehozást None pool értékekkel (line 115-116).

## Teszt Osztály: `TestGetEngine`

Globális engine lekérdezés tesztjei.

### ✓ `test_get_engine_creates_on_first_call()`

Teszteli, hogy az engine létrejön az első hívásnál.

### ✓ `test_get_engine_caches_result()`

Teszteli, hogy az engine cache-elődik.

### ✓ `test_get_engine_echo_fallback_exception()`

Teszteli az echo fallback exception handling-et (line 151-157).

### ✓ `test_get_engine_with_pool_config()`

Teszteli a get_engine pool config olvasását (line 159-167).

## Teszt Osztály: `TestGetAsyncSessionMaker`

Session maker lekérdezés tesztjei.

### ✓ `test_get_async_session_maker_creates_once()`

Teszteli, hogy a session maker csak egyszer jön létre.

## Teszt Osztály: `TestDatabaseManager`

DatabaseManager osztály tesztjei.

### ✓ `test_database_manager_initialization_without_config()`

Teszteli a DatabaseManager inicializálását config_manager nélkül (line 321-322).

### ✓ `test_database_manager_initialization_without_logger()`

Teszteli a DatabaseManager inicializálását logger nélkül (line 323-324).

### ✓ `test_database_manager_initialization()`

Teszteli a DatabaseManager inicializálását.

### ✓ `test_database_manager_initialize_with_pool_config()`

Teszteli a DatabaseManager initialize pool config olvasását (line 340-347).

### ✓ `test_database_manager_initialize()`

Teszteli a DatabaseManager initialize metódusát.

### ✓ `test_database_manager_get_session()`

Teszteli a DatabaseManager get_session metódusát.

### ✓ `test_database_manager_get_session_raises_when_not_initialized()`

Teszteli, hogy get_session hibát dob, ha nincs inicializálva.

### ✓ `test_database_manager_close()`

Teszteli a DatabaseManager close metódusát.

### ✓ `test_database_manager_singleton_pattern()`

Teszteli, hogy a DatabaseManager Singleton mintát követ.

### ✓ `test_database_manager_get_session_exception_rollback()`

Teszteli a DatabaseManager get_session exception rollback-ját (lines 295-297).

### ✓ `test_database_manager_get_session_finally_block()`

Teszteli a DatabaseManager get_session finally blokkját (line 393-394).

### ✓ `test_database_manager_get_active_configs()`

Teszteli a DatabaseManager get_active_configs metódusát (lines 312-325).

### ✓ `test_database_manager_get_active_configs_not_initialized()`

Teszteli, hogy get_active_configs hibát dob, ha nincs inicializálva (line 315).

### ✓ `test_database_manager_get_active_configs_empty_result()`

Teszteli a get_active_configs üres eredménnyel.

### ✓ `test_database_manager_close_when_engine_is_none()`

Teszteli a DatabaseManager close metódusát amikor _engine None (line 427).

## Teszt Osztály: `TestContextManagers`

Context manager függvények tesztjei.

### ✓ `test_get_db_session()`

Teszteli a get_db_session context managert.

### ✓ `test_get_db_session_direct()`

Teszteli a get_db_session_direct függvényt.

### ✓ `test_get_db_session_exception_rollback()`

Teszteli a get_db_session exception rollback-ját (lines 169-171).

### ✓ `test_get_db_session_finally_block()`

Teszteli a get_db_session finally blokkját (line 227-228).

## Teszt Osztály: `TestDatabaseInitialization`

Adatbázis inicializálás tesztjei.

### ✓ `test_init_db()`

Teszteli az init_db függvényt.

### ✓ `test_close_db()`

Teszteli a close_db függvényt.

## Teszt Osztály: `TestGetActiveConfigs`

Aktív konfigurációk lekérdezésének tesztjei.

### ✓ `test_get_active_configs()`

Teszteli a get_active_configs függvényt a DatabaseManager-en keresztül.

---

**Teszt fájl:** [`tests/neural_ai/core/db/implementations/test_sqlalchemy_session.py`](../../tests/neural_ai/core/db/implementations/test_sqlalchemy_session.py)

**Tesztelt modul:** [`neural_ai/core/db/implementations/sqlalchemy_session.py`](../../neural_ai/core/db/implementations/sqlalchemy_session.py)
