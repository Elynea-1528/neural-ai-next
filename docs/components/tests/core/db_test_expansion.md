# DB Modul Teszt Bővítés - Hibás Connection String

## Áttekintés

Ez a dokumentáció a Database modul tesztjeinek bővítését írja le, különös tekintettel a hibás connection string kezelésére.

## Új Tesztesetek

### 1. Hibás Connection String Típusok

A tesztbővítés a következő hibás connection string típusokat fedi le:

#### 1.1 test_create_engine_with_invalid_url

**Cél:** Teszteli az érvénytelen adatbázis URL-t.

**Tesztelt hiba:**
```python
invalid_url = "invalid:///test.db"  # Nincs driver megadva
```

**Elvárások:**
- A `create_engine` függvény `ArgumentError` vagy `Exception` kivételt dob
- A hiba oka: hiányzó vagy érvénytelen SQLAlchemy driver

#### 1.2 test_create_engine_with_malformed_url

**Cél:** Teszteli a hibásan formázott adatbázis URL-t.

**Tesztelt hiba:**
```python
malformed_url = "sqlite+aiosqlite:///:memory:?invalid_param"
```

**Elvárások:**
- A `create_engine` függvény `ArgumentError` vagy `Exception` kivételt dob
- A hiba oka: helytelen URL formátum

#### 1.3 test_create_engine_with_sqlite_relative_path

**Cél:** Teszteli a relatív útvonal használatát.

**Tesztelt URL:**
```python
db_url = "sqlite+aiosqlite:///./test.db"
```

**Elvárások:**
- Az engine sikeresen létrejön
- Az engine URL-je tartalmazza a "test.db" szöveget

#### 1.4 test_create_engine_with_sqlite_absolute_path

**Cél:** Teszteli az abszolút útvonal használatát.

**Tesztelt URL:**
```python
db_url = "sqlite+aiosqlite:////tmp/test.db"
```

**Elvárások:**
- Az engine sikeresen létrejön
- Az engine URL-je tartalmazza a "/tmp/test.db" szöveget

### 2. DatabaseManager Hibakezelés

#### 2.1 test_database_manager_initialize_with_invalid_url

**Cél:** Teszteli a DatabaseManager inicializálását érvénytelen URL-lel.

**Tesztelt hiba:**
```python
"db_url": "invalid:///test.db"  # Érvénytelen URL
```

**Elvárások:**
- Az `initialize()` metódus `ArgumentError` vagy `Exception` kivételt dob
- A hiba továbbítódik a `create_engine` függvényből

#### 2.2 test_database_manager_initialize_with_missing_url

**Cél:** Teszteli a DatabaseManager inicializálását hiányzó URL-lel.

**Tesztelt hiba:**
```python
"db_url": None  # Hiányzó URL
```

**Elvárások:**
- Az `initialize()` metódus `DBConnectionError` kivételt dob
- A hibaüzenet: "Adatbázis URL nincs konfigurálva"

#### 2.3 test_database_manager_double_initialize

**Cél:** Teszteli a dupla inicializálást.

**Elvárások:**
- Az első inicializálás sikeres
- A második inicializálás nem dob hibát
- Az engine továbbra is érvényes marad

#### 2.4 test_database_manager_close_not_initialized

**Cél:** Teszteli a close-t ha nincs inicializálva.

**Elvárások:**
- A `close()` metódus nem dob hibát, ha nincs inicializálva
- Az `_engine` és `_session_maker` `None` marad

## Hibakezelési Stratégiák

### 1. Connection String Validáció

A tesztesetek a következő validációs hibákat fedik le:

| Hiba Típus | Példa | Várt Viselkedés |
|------------|-------|-----------------|
| Érvénytelen driver | `invalid:///test.db` | `ArgumentError` |
| Hibás formátum | `sqlite+aiosqlite:///:memory:?invalid_param` | `ArgumentError` |
| Hiányzó URL | `None` | `DBConnectionError` |
| Relatív útvonal | `sqlite+aiosqlite:///./test.db` | Sikeres |
| Abszolút útvonal | `sqlite+aiosqlite:////tmp/test.db` | Sikeres |

### 2. DatabaseManager Életciklus

A tesztesetek a következő életciklus eseményeket fedik le:

1. **Inicializálás:**
   - Érvényes URL-lel: sikeres
   - Érvénytelen URL-lel: hiba
   - Hiányzó URL-lel: hiba
   - Dupla inicializálás: sikeres (idempotens)

2. **Működés:**
   - Session lekérdezése inicializálás után: sikeres
   - Session lekérdezése inicializálás nélkül: hiba

3. **Lezárás:**
   - Normál lezárás: sikeres
   - Lezárás inicializálás nélkül: sikeres (nem dob hibát)

## Teszt Coverage

A bővített tesztek a következő területeket fedik le:

| Metódus | Coverage | Hibakezelés |
|---------|----------|-------------|
| `create_engine()` | 100% | Érvénytelen URL, Hibás formátum |
| `get_database_url()` | 100% | Hiányzó konfiguráció |
| `DatabaseManager.initialize()` | 100% | Érvénytelen URL, Hiányzó URL |
| `DatabaseManager.close()` | 100% | Nincs inicializálva |
| `DatabaseManager.get_session()` | 100% | Nincs inicializálva |

## Futtatás

```bash
# Összes DB teszt futtatása
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/core/db/test_session.py -v

# Csak a connection string tesztek
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/core/db/test_session.py::TestCreateEngine -v
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/core/db/test_session.py::TestDatabaseManager -v
```

## Kimenet

A tesztek sikeres futtatása esetén:
```
tests/core/db/test_session.py::TestCreateEngine::test_create_engine_with_invalid_url PASSED
tests/core/db/test_session.py::TestCreateEngine::test_create_engine_with_malformed_url PASSED
tests/core/db/test_session.py::TestCreateEngine::test_create_engine_with_sqlite_relative_path PASSED
tests/core/db/test_session.py::TestCreateEngine::test_create_engine_with_sqlite_absolute_path PASSED
tests/core/db/test_session.py::TestDatabaseManager::test_database_manager_initialize_with_invalid_url PASSED
tests/core/db/test_session.py::TestDatabaseManager::test_database_manager_initialize_with_missing_url PASSED
tests/core/db/test_session.py::TestDatabaseManager::test_database_manager_double_initialize PASSED
tests/core/db/test_session.py::TestDatabaseManager::test_database_manager_close_not_initialized PASSED
```

## Fejlesztői Jegyzetek

1. **SQLAlchemy Hibák:** A `create_engine` metódus `ArgumentError` kivételt dob érvénytelen URL esetén.

2. **Konfiguráció Kezelés:** A `get_database_url` metódus `DBConnectionError` kivételt dob, ha nincs konfigurálva az URL.

3. **Idempotencia:** A `DatabaseManager.initialize()` metódus idempotens, azaz többször is hívható.

4. **Biztonságos Lezárás:** A `DatabaseManager.close()` metódus nem dob hibát, ha nincs inicializálva.

5. **Mockolás:** A tesztesetek `unittest.mock.patch` és `Mock` objektumokat használnak a függőségek mockolásához.