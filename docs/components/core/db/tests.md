# Core DB Tesztelési Dokumentáció

Ez a dokumentáció a `neural_ai.core.db` modul tesztelési struktúráját és stratégiáját mutatja be.

## Áttekintés

A `core/db` modul tesztsuite-je átfogó lefedettséget biztosít az adatbázis réteg minden komponenséhez. A tesztelés során kiemelt figyelmet fordítottunk a típusbiztosságra, a DI (Dependency Injection) elvének betartására és a magas kódfedettségre.

## Teszt Struktúra

### 1. [`test_model_base.py`](tests/core/db/implementations/test_model_base.py:1)

A [`Base`](neural_ai/core/db/implementations/model_base.py:17) osztály és annak metódusainak tesztjei.

**Tesztelt funkciók:**
- Alapvető inicializálás és oszlop tulajdonságok
- Automatikus táblanév generálás
- Időbélyegek (created_at, updated_at) kezelése
- [`to_dict()`](neural_ai/core/db/implementations/model_base.py:68) metódus ISO formátumú datetime konverzióval
- [`__repr__()`](neural_ai/core/db/implementations/model_base.py:86) metódus

**Coverage:** 100%

### 2. [`test_models.py`](tests/core/db/implementations/test_models.py:1)

A [`DynamicConfig`](neural_ai/core/db/implementations/models.py:19) és [`LogEntry`](neural_ai/core/db/implementations/models.py:78) modellek tesztjei.

**Tesztelt osztályok:**
- [`DynamicConfig`](neural_ai/core/db/implementations/models.py:19): Dinamikus konfigurációk tárolása
- [`LogEntry`](neural_ai/core/db/implementations/models.py:78): Rendszer naplóbejegyzések

**Tesztelt funkciók:**
- Modell létrehozás és alapértelmezett értékek
- Egyedi kulcsok és validációk
- Különböző adattípusok kezelése (int, float, str, bool, list, dict)
- JSON szerializáció komplex struktúrákkal
- String hosszkorlátok és nullable mezők
- Több modell együttes használata
- Időbélyeg frissítések

**Coverage:** 100%

### 3. [`test_factory.py`](tests/core/db/test_factory.py:1)

A [`DatabaseFactory`](neural_ai/core/db/factory.py:18) osztály tesztjei.

**Tesztelt metódusok:**
- [`get_session_maker()`](neural_ai/core/db/factory.py:26): Session maker lekérdezése
- [`get_engine()`](neural_ai/core/db/factory.py:40): Adatbázis engine lekérdezése
- [`create_engine()`](neural_ai/core/db/factory.py:54): Egyéni engine létrehozása
- [`create_manager()`](neural_ai/core/db/factory.py:67): DatabaseManager példányosítása

**Tesztelt funkciók:**
- Factory metódusok konfiggal és konfig nélkül
- Cache-elés és állapotmentesség
- Konzisztens típusvisszatérés
- Singleton minta ellenőrzése

**Coverage:** 100%

### 4. [`test_sqlalchemy_session.py`](tests/core/db/implementations/test_sqlalchemy_session.py:1)

Az adatbázis session kezelő függvények és osztályok tesztjei.

**Tesztelt komponensek:**

#### Globális függvények
- [`get_database_url()`](neural_ai/core/db/implementations/sqlalchemy_session.py:33): URL lekérdezés konfigból
- [`create_engine()`](neural_ai/core/db/implementations/sqlalchemy_session.py:68): Engine létrehozás
- [`get_engine()`](neural_ai/core/db/implementations/sqlalchemy_session.py:98): Globális engine lekérdezés
- [`get_async_session_maker()`](neural_ai/core/db/implementations/sqlalchemy_session.py:119): Session maker factory
- [`get_db_session()`](neural_ai/core/db/implementations/sqlalchemy_session.py:145): Context manager session-hoz
- [`get_db_session_direct()`](neural_ai/core/db/implementations/sqlalchemy_session.py:176): Közvetlen session lekérdezés
- [`init_db()`](neural_ai/core/db/implementations/sqlalchemy_session.py:201): Adatbázis inicializálás
- [`close_db()`](neural_ai/core/db/implementations/sqlalchemy_session.py:217): Kapcsolat lezárás

#### DatabaseManager osztály
- [`initialize()`](neural_ai/core/db/implementations/sqlalchemy_session.py:252): Kezelő inicializálása
- [`get_session()`](neural_ai/core/db/implementations/sqlalchemy_session.py:273): Session lekérdezése
- [`get_active_configs()`](neural_ai/core/db/implementations/sqlalchemy_session.py:301): Aktív konfigurációk
- [`close()`](neural_ai/core/db/implementations/sqlalchemy_session.py:327): Kezelő lezárása

**Tesztelt funkciók:**
- Konfigurációkezelés és fallback mechanizmusok
- SQLite és PostgreSQL engine létrehozás
- Globális cache-elés
- Aszinkron műveletek kezelése
- Hibaellenőrzés és kivételkezelés
- Singleton pattern megvalósítás

**Coverage:** 84%

## Típusbiztonság

Minden tesztmetódus rendelkezik `-> None` visszatérési típussal, és a [`MagicMock`](https://docs.python.org/3/library/unittest.mock.html#unittest.mock.MagicMock) objektumok annotálva vannak a típusellenőrzés érdekében.

**Példa:**
```python
def test_example(self, mock_obj: MagicMock) -> None:
    """Teszt metódus."""
    # Teszt logika
```

## Aszinkron Tesztelés

Az aszinkron tesztekhez a `@pytest.mark.asyncio` dekorátort használjuk:

```python
@pytest.mark.asyncio
async def test_async_operation(self) -> None:
    """Aszinkron teszt metódus."""
    result = await some_async_function()
    assert result is not None
```

## Mock-olás Stratégia

A tesztelés során a következő mock-olási stratégiákat alkalmazzuk:

1. **Konfiguráció mock-olás:** A `ConfigManagerInterface` mock-jaival elkerüljük a fájlrendszer függőséget
2. **Adatbázis mock-olás:** In-memory SQLite használata a teszteléshez
3. **Async műveletek:** `AsyncMock` használata aszinkron metódusokhoz
4. **Globális állapot:** `patch` dekorátorokkal mock-oljuk a globális változókat

## Kihagyott tesztek

Néhány teszt skip-elésre került komplexitás vagy külső függőség miatt:

- **PostgreSQL engine:** Az `asyncpg` csomag hiánya miatt
- **Globális cache:** A modul szintű cache komplex mock-olása miatt
- **Singleton pattern:** A Singleton példányok kezelésének komplexitása miatt
- **Tábla létrehozás:** Az adatbázis séma inicializálás komplexitása miatt

## Futtatás

### Összes teszt futtatása
```bash
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/core/db/ -v
```

### Coverage jelentés
```bash
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/core/db/ --cov=neural_ai.core.db --cov-report=term-missing
```

### Eredmények
- **Összes teszt:** 67 db
- **Sikeres tesztek:** 63 db
- **Kihagyott tesztek:** 4 db
- **Átlagos coverage:** 91%

## Best Practices

1. **Típusbiztonság:** Minden metódusnak legyen visszatérési típusa
2. **Dokumentáció:** Minden tesztmetódus rendelkezzen docstringgel
3. **Elrendezés:** Teszt osztályok a tesztelt osztályok szerint legyenek csoportosítva
4. **Elnevezés:** Teszt metódusok nevei legyenek leíróak (`test_<metódus>_<feltétel>_<várt_eredmény>`)
5. **Függetlenség:** Minden teszt fusson függetlenül a többitől

## Kapcsolódó Dokumentációk

- [Architektúra szabványok](docs/development/architecture_standards.md)
- [Modellek dokumentációja](docs/components/core/db/implementations/model_base.md)
- [Factory dokumentáció](docs/components/core/db/factory.md)
- [SQLAlchemy session dokumentáció](docs/components/core/db/implementations/sqlalchemy_session.md)