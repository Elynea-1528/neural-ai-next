# DB Interfészek Modul

## Áttekintés

Adatbázis interfészek a Neural AI Next rendszerhez.

Ez a modul tartalmazza az adatbázis műveletek interfészeit.

## Jelenlegi Állapot

Ez a modul jelenleg üres, mivel a DB modul a következő közvetlen implementációkat használja:

- [`DatabaseManager`](../implementations/sqlalchemy_session.md#databasemanager): Adatbázis kezelő osztály
- [`Base`](../implementations/model_base.md#base): SQLAlchemy deklaratív alaposztály
- [`DynamicConfig`](../implementations/models.md#dynamicconfig): Dinamikus konfigurációs modell
- [`LogEntry`](../implementations/models.md#logentry): Naplóbejegyzés modell

## Jövőbeli Fejlesztések

A jövőben ez a modul tartalmazhatja az adatbázis műveletek interfészeit, mint például:

- `DatabaseInterface`: Általános adatbázis műveletek interfésze
- `ModelInterface`: Adatbázis modellek interfésze
- `SessionInterface`: Session kezelés interfésze

## Kapcsolódó Dokumentáció

- [DB Implementációk](../implementations/__init__.md)
- [DB Modul](../__init__.md)