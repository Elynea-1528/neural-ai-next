# DynamicConfigManager

## Áttekintés

A `DynamicConfigManager` egy aszinkron, adatbázis-alapú konfigurációkezelő osztály, amely a futás közben módosítható konfigurációkat kezeli. Hot reload támogatással rendelkezik, ami azt jelenti, hogy a konfiguráció változásairól a rendszer azonnal értesítést kap anélkül, hogy újra kellene indítani az alkalmazást.

## Jellemzők

- **Aszinkron működés**: Minden művelet aszinkron, nem blokkolja a fő szálat
- **Hot Reload**: Automatikus észlelés és értesítés konfiguráció változásokról
- **Cache-elés**: Gyorsítótárba menti a gyakran használt konfigurációkat
- **Event-driven**: Event listener-ekkel reagál a változásokra
- **Soft Delete**: Konfigurációk deaktiválással történő "törlése"
- **Metaadatok**: Kategória, leírás és aktivitási állapot tárolása
- **Típusbiztonság**: Automatikus típusfelismerés és validáció

## Architektúra

### Osztálydiagram

```
┌─────────────────────────────────────────┐
│   AsyncConfigManagerInterface           │
│   (Interfész)                           │
└─────────────────┬───────────────────────┘
                  │ implements
                  ▼
┌─────────────────────────────────────────┐
│   DynamicConfigManager                  │
│   (Implementáció)                       │
├─────────────────────────────────────────┤
│ - session: AsyncSession                 │
│ - _logger: LoggerInterface              │
│ - _cache: dict[str, Any]                │
│ - _listeners: list[ConfigListener]      │
│ - _last_update: datetime                │
│ - _hot_reload_task: Task                │
│ - _stop_hot_reload: Event               │
└─────────────────────────────────────────┘
                  │ has-a
                  ▼
┌─────────────────────────────────────────┐
│   DynamicConfig (SQLAlchemy Model)      │
│   - key: str                            │
│   - value: JSON                         │
│   - value_type: str                     │
│   - category: str                       │
│   - description: str                    │
│   - is_active: bool                     │
└─────────────────────────────────────────┘
```

### Függőségek

- **SQLAlchemy**: Adatbázis kapcsolat és ORM
- **asyncio**: Aszinkron működés és task kezelés
- **datetime**: Időbélyegezés
- **LoggerInterface**: Naplózás (opcionális)

## Használat

### Alap inicializálás

```python
from sqlalchemy.ext.asyncio import AsyncSession
from neural_ai.core.config.implementations.dynamic_config_manager import DynamicConfigManager
from neural_ai.core.logger.implementations.default_logger import DefaultLogger

# Session létrehozása
session = AsyncSession(...)

# Logger létrehozása (opcionális)
logger = DefaultLogger()

# Manager inicializálása
config_manager = DynamicConfigManager(
    session=session,
    logger=logger
)
```

### Konfiguráció lekérdezése

```python
# Egyszerű lekérdezés
value = await config_manager.get("risk.max_position_size_percent", default=2.0)
print(f"Max position size: {value}%")

# Szekció lekérdezése
risk_configs = await config_manager.get_section("risk")
print(f"Risk configs: {risk_configs}")
```

### Konfiguráció beállítása

```python
# Egyszerű beállítás
await config_manager.set("risk.max_position_size_percent", 3.0)

# Beállítás metaadatokkal
await config_manager.set_with_metadata(
    key="strategy.d1_enabled",
    value=True,
    category="strategy",
    description="D1 Alap adatok processzor engedélyezése"
)
```

### Hot Reload használata

```python
# Hot reload indítása (5 másodperces intervallummal)
await config_manager.start_hot_reload(interval=5.0)

# Listener hozzáadása
async def on_config_change(key: str, value: Any) -> None:
    print(f"Config changed: {key} = {value}")

config_manager.add_listener(on_config_change)

# Hot reload leállítása
await config_manager.stop_hot_reload()
```

### Konfiguráció törlése

```python
# Soft delete (is_active = False)
deleted = await config_manager.delete("obsolete_config_key")
if deleted:
    print("Config successfully deleted")
```

## API Referencia

### Metódusok

#### `__init__(filename, session, logger)`

Inicializálja a DynamicConfigManager-t.

**Paraméterek:**
- `filename`: Nincs használatban, csak kompatibilitás miatt (deprecated)
- `session`: Az adatbázis session (kötelező)
- `logger`: Logger interfész (opcionális)

**Kivételek:**
- `ValueError`: Ha nincs megadva session

#### `async get(*keys, default=None) -> Any`

Konfigurációs érték lekérdezése.

**Paraméterek:**
- `*keys`: A konfigurációs kulcs (csak egy kulcs támogatott)
- `default`: Alapértelmezett érték, ha a kulcs nem található

**Visszatérési érték:**
- A konfigurációs érték vagy az alapértelmezett érték

**Kivételek:**
- `ValueError`: Ha több kulcsot adnak meg
- `ConfigError`: Ha hiba történik a lekérdezés során

#### `async set(*keys, value) -> None`

Konfigurációs érték beállítása.

**Paraméterek:**
- `*keys`: A konfigurációs kulcs (csak egy kulcs támogatott)
- `value`: A beállítandó érték

**Kivételek:**
- `ValueError`: Ha több kulcsot adnak meg vagy érvénytelen az érték
- `ConfigError`: Ha hiba történik a beállítás során

#### `async get_section(section) -> dict[str, Any]`

Teljes konfigurációs szekció lekérése kategória alapján.

**Paraméterek:**
- `section`: A konfigurációs kategória neve

**Visszatérési érték:**
- A kategóriához tartozó összes konfigurációs érték

**Kivételek:**
- `KeyError`: Ha a kategória nem található
- `ConfigError`: Ha hiba történik a lekérdezés során

#### `async get_all(category=None) -> dict[str, Any]`

Összes konfiguráció lekérdezése.

**Paraméterek:**
- `category`: Opcionális kategória szűréshez

**Visszatérési érték:**
- Szótár az összes (vagy kategóriához tartozó) konfigurációval

#### `async set_with_metadata(key, value, category, description, is_active) -> None`

Konfiguráció beállítása metaadatokkal.

**Paraméterek:**
- `key`: A konfigurációs kulcs
- `value`: A konfigurációs érték
- `category`: A konfiguráció kategóriája (alapértelmezett: "system")
- `description`: A konfiguráció leírása (opcionális)
- `is_active`: A konfiguráció aktív-e (alapértelmezett: True)

#### `async delete(key) -> bool`

Konfiguráció törlése (soft delete).

**Paraméterek:**
- `key`: A törlendő konfigurációs kulcs

**Visszatérési érték:**
- True ha a konfiguráció törölve lett, False ha nem található

#### `add_listener(callback) -> None`

Listener hozzáadása konfiguráció változásokhoz.

**Paraméterek:**
- `callback`: A callback függvény, amelyet hívni kell a változás esetén

#### `remove_listener(callback) -> None`

Listener eltávolítása.

**Paraméterek:**
- `callback`: Az eltávolítandó callback függvény

#### `async start_hot_reload(interval=5.0) -> None`

Hot reload indítása (háttérben fut).

**Paraméterek:**
- `interval`: Az ellenőrzési időköz másodpercben

**Kivételek:**
- `RuntimeError`: Ha a hot reload már fut

#### `async stop_hot_reload() -> None`

Hot reload leállítása.

### Nem támogatott műveletek

A következő metódusok nem támogatottak, mivel a DynamicConfigManager adatbázisban tárol:

- `save()`: `NotImplementedError`-t dob
- `load()`: `NotImplementedError`-t dob
- `load_directory()`: `NotImplementedError`-t dob

## Példák

### 1. Risk Manager integráció

```python
class RiskManager:
    """Kockázatkezelő, ami reagál a konfiguráció változásaira."""

    def __init__(self, config_manager: DynamicConfigManager):
        self.config_manager = config_manager
        self.max_position_size = 2.0  # Default

        # Listener regisztrálása
        config_manager.add_listener(self._on_config_change)

    async def _on_config_change(self, key: str, value: Any) -> None:
        """Konfiguráció változás kezelése."""
        if key == "risk.max_position_size_percent":
            self.max_position_size = float(value)
            print(f"Max position size updated to {value}%")

        elif key == "risk.global_risk_multiplier":
            await self.recalculate_all_positions()
            print(f"Global risk multiplier updated to {value}")

    async def recalculate_all_positions(self) -> None:
        """Összes pozíció újraszámolása."""
        # Implementáció...
        pass
```

### 2. Alap konfigurációk inicializálása

```python
async def initialize_default_configs(config_manager: DynamicConfigManager) -> None:
    """Alap konfigurációk létrehozása az adatbázisban."""

    default_configs = [
        {
            "key": "risk.max_position_size_percent",
            "value": 2.0,
            "category": "risk",
            "description": "Maximum pozícióméret a portfólió százalékában"
        },
        {
            "key": "risk.max_daily_loss_percent",
            "value": 5.0,
            "category": "risk",
            "description": "Maximum napi veszteség százalékban"
        },
        {
            "key": "trading.active_symbols",
            "value": ["EURUSD", "XAUUSD", "GBPUSD"],
            "category": "trading",
            "description": "Aktív kereskedési szimbólumok listája"
        },
    ]

    for config in default_configs:
        await config_manager.set_with_metadata(**config)
```

### 3. Hot Reload tesztelése

```python
import asyncio

async def test_hot_reload():
    """Hot reload funkcionalitás tesztelése."""

    # Manager létrehozása
    session = AsyncSession(...)
    config_manager = DynamicConfigManager(session=session)

    # Listener hozzáadása
    async def config_changed(key: str, value: Any) -> None:
        print(f"🔥 Config changed: {key} = {value}")

    config_manager.add_listener(config_changed)

    # Hot reload indítása
    await config_manager.start_hot_reload(interval=2.0)

    # Várakozás a változásokra
    await asyncio.sleep(10)

    # Hot reload leállítása
    await config_manager.stop_hot_reload()

if __name__ == "__main__":
    asyncio.run(test_hot_reload())
```

## Hibakezelés

A DynamicConfigManager a következő hibákat dobhatja:

### `ConfigError`

Alap konfigurációs hiba, amely a következő esetekben fordulhat elő:

- Adatbázis kapcsolati hiba
- Érvénytelen konfigurációs kulcs
- Érvénytelen konfigurációs érték
- Tranzakciós hiba

**Példa hibakezelésre:**

```python
from neural_ai.core.config.exceptions import ConfigError

try:
    value = await config_manager.get("nonexistent_key")
except ConfigError as e:
    print(f"Config error: {e}")
    # Fallback érték használata
    value = default_value
```

### `ValueError`

Érvénytelen paraméter esetén fordulhat elő:

- Több kulcs megadása a `get()` vagy `set()` metódusban
- Érvénytelen érték típus

### `RuntimeError`

Hot reload indítása esetén, ha az már fut.

## Teljesítményoptimalizálás

### Cache-elés

A DynamicConfigManager automatikusan gyorsítótárba helyezi a lekérdezett konfigurációkat. A cache a következő esetekben frissül:

- Konfiguráció beállításakor
- Hot reload során észlelt változás esetén
- Manuális cache frissítéskor

### Adatbázis optimalizálás

- **Indexek**: A `DynamicConfig` modell indexekkel rendelkezik a gyors keresés érdekében
- **Soft Delete**: A törölt konfigurációk nem törlődnek fizikailag, csak `is_active=False` értéket kapnak

## Biztonság

- **Session Management**: Minden művelet egy adatbázis session-en keresztül történik
- **Tranzakciós biztonság**: A `set()` és `delete()` műveletek tranzakciókban futnak
- **Rollback**: Hiba esetén automatikus rollback történik

## Korlátozások

1. **Csak egy kulcs**: A `get()` és `set()` metódusok csak egyetlen kulcsot támogatnak (nem hierarchikus)
2. **Nincs fájl támogatás**: Nem támogatja a konfigurációk fájlba mentését vagy onnan betöltését
3. **Aszinkron működés**: Minden metódus aszinkron, ezért `await` kulcsszó szükséges

## Jövőbeli fejlesztések

- **Hierarchikus kulcsok**: Több kulcs támogatása (pl. `get("database", "connection", "url")`)
- **Fájl szinkronizáció**: Konfigurációk exportálása/importálása YAML fájlokba
- **Validáció**: Séma-alapú validáció fejlesztése
- **GUI**: Webes felület a konfigurációk kezeléséhez

## Kapcsolódó dokumentumok

- [Dinamikus konfiguráció specifikáció](../../../planning/specs/02_dynamic_configuration.md)
- [DynamicConfig modell](../db/implementations/models.md)
- [AsyncConfigManagerInterface](../interfaces/async_config_interface.md)
- [ConfigManagerFactory](../factory.md)