# Core Bootstrap Modul

## Áttekintés

A `neural_ai.core.__init__.py` modul a Neural-AI-Next rendszer alapvető infrastrukturális komponenseinek inicializációs pontja. Ez a modul biztosítja a core komponensek megfelelő sorrendű inicializálását és függőségi injektálását, elkerülve a körkörös függőségeket.

## Főbb Jellemzők

- **Dependency Injection (DI)**: Minden komponens interfészen keresztül kommunikál
- **Lazy Loading**: A komponensek csak akkor töltődnek be, amikor szükség van rájuk
- **Singleton Pattern**: A `get_core_components()` globális hozzáférést biztosít
- **Type Safety**: Szigorú típusosság `TYPE_CHECKING` blokkokkal

## Komponensek

A bootstrap folyamat a következő komponenseket inicializálja:

1. **Hardware** - Hardver információk lekérdezése
2. **Config** - Konfiguráció betöltése
3. **Logger** - Naplózási rendszer
4. **Database** - Adatbázis kapcsolat
5. **EventBus** - Eseménykezelés
6. **Storage** - Adattárolás
7. **System** - Rendszer monitorozás

## Függvények

### `get_version() -> str`

Dynamikusan betölti a csomag verzióját.

**Visszatérési érték:**
- A csomag verziója stringként
- `"unknown"` ha a verzió nem érhető el

**Példa:**
```python
version = get_version()
print(f"Verzió: {version}")
```

### `get_schema_version() -> str`

Visszaadja az aktuális séma verziót.

**Visszatérési érték:**
- Az aktuális séma verziója stringként (jelenleg: `"1.0.0"`)

### `bootstrap_core(config_path: str | None = None, log_level: str | None = None) -> CoreComponents`

Bootstrap funkció a core komponensek inicializálásához.

**Paraméterek:**
- `config_path`: Opcionális konfigurációs fájl útvonala. Ha `None`, akkor a `configs` könyvtárat tölti be.
- `log_level`: Opcionális log szint beállítás. Ha `None`, akkor a konfigurációból olvassa ki.

**Visszatérési érték:**
- A teljesen inicializált `CoreComponents` példány

**Kivételek:**
- `ConfigError`: Ha a konfiguráció betöltése sikertelen
- `LoggerError`: Ha a logger inicializálása sikertelen
- `DatabaseError`: Ha az adatbázis kapcsolat létrehozása sikertelen

**Példa:**
```python
from neural_ai.core import bootstrap_core

# Core komponensek inicializálása
core = bootstrap_core()

# Komponensek használata
core.logger.info("Alkalmazás elindult")
await core.database.initialize()
await core.event_bus.start()

# Rendszer állapot ellenőrzése
health = core.health_monitor.check_health()
print(f"Rendszer állapota: {health.overall_status.value}")
```

### `get_core_components() -> CoreComponents`

Globális core komponensek lekérdezése. Ez a függvény egy szingleton példányt ad vissza, biztosítva, hogy az alkalmazás egészében ugyanazok a komponensek legyenek elérhetőek.

**Visszatérési érték:**
- A globális `CoreComponents` példány

**Példa:**
```python
from neural_ai.core import get_core_components

core = get_core_components()
core.logger.info("Komponens használatban")
```

## Bootstrap Folyamat

A bootstrap folyamat szigorúan definiált sorrendben történik:

1. **Hardware inicializálása**
   - Hardver információk lekérdezése a `HardwareFactory` segítségével
   - Regisztráció a DI containerben

2. **Konfiguráció betöltése**
   - YAML konfiguráció betöltése a `configs/` mappából
   - Regisztráció a DI containerben

3. **Logger inicializálása**
   - Logger konfigurálása a konfigurációs adatok alapján
   - Alap logger példány létrehozása
   - Regisztráció a DI containerben

4. **Adatbázis inicializálása**
   - Adatbázis manager létrehozása
   - Regisztráció a DI containerben

5. **EventBus inicializálása**
   - Esemény busz létrehozása a konfiguráció alapján
   - Regisztráció a DI containerben

6. **Storage inicializálása**
   - Tárhely létrehozása (Config+Logger+HardwareInfo)
   - Regisztráció a DI containerben

7. **Rendszer monitorozás**
   - Health monitor létrehozása
   - Regisztráció a DI containerben

## Függőségi Injektálás (DI)

A modul a `DIContainer` osztályt használja a függőségek kezelésére. Minden komponens interfészen keresztül kerül regisztrálásra, ami lehetővé teszi:

- **Könnyű tesztelés**: Mock objektumokkal való helyettesítés
- **Laza csatolás**: Komponensek egyszerű cseréje
- **Életciklus kezelés**: A container kezeli a komponensek életciklusát

## Körkörös Függőségek Kezelése

A modul több technikát is alkalmaz a körkörös függőségek elkerülésére:

1. **TYPE_CHECKING blokkok**: A típusok csak típusellenőrzéskor töltődnek be
2. **Lazy Import**: A konkrét implementációk a függvényekben kerülnek importálásra
3. **Interfész alapú tervezés**: Komponensek csak interfészeken keresztül kommunikálnak

## Használati Minták

### Alap inicializálás
```python
from neural_ai.core import bootstrap_core

core = bootstrap_core()
core.logger.info("Rendszer inicializálva")
```

### Konfigurációval történő inicializálás
```python
from neural_ai.core import bootstrap_core

core = bootstrap_core(
    config_path="custom_configs/",
    log_level="DEBUG"
)
```

### Globális hozzáférés
```python
from neural_ai.core import get_core_components

def process_data():
    core = get_core_components()
    core.logger.info("Adatfeldolgozás elkezdve")
    
    # Adatok mentése
    await core.storage.save_data("data.parquet", data)
```

### Rendszer állapot ellenőrzés
```python
from neural_ai.core import get_core_components

core = get_core_components()
health = core.health_monitor.check_health()

if health.overall_status.value == "healthy":
    print("Minden komponens működik")
else:
    print(f"Hiba: {health.message}")
```

## Kapcsolódó Dokumentáció

- [Architektúra Szabványok](docs/development/architecture_standards.md)
- [Core Base Komponensek](docs/components/core/base/factory.md)
- [Konfiguráció Kezelés](docs/components/core/config/factory.md)
- [Adatbázis Kezelés](docs/components/core/db/implementations/model_base.md)
- [Tárhely Kezelés](docs/components/core/storage/implementations/parquet_storage.md)
- [Rendszer Monitorozás](docs/components/core/system/factory.md)

## Verzió Történet

- **1.0.0**: Kezdeti implementáció a core bootstrap funkcionalitással
