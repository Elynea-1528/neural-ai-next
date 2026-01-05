# UI Application (`neural_ai/ui/app.py`)

## Áttekintés

A `UIApplication` osztály a felhasználói felület fő alkalmazásának belépési pontja. Ez az osztály felelős a teljes UI rendszer inicializálásáért és működtetéséért, összekapcsolva az összes komponenst.

## Osztály szerkezet

### UIApplication

A felhasználói felület fő alkalmazás osztálya.

#### Metódusok

##### `__init__(config: Optional[Dict[str, Any]] = None, logger: Optional["LoggerInterface"] = None) -> None`

Az UI alkalmazás inicializálása.

**Paraméterek:**
- `config`: Konfigurációs beállítások (opcionális)
- `logger`: Logger példány (opcionális)

##### `initialize() -> bool`

Az alkalmazás inicializálása. Létrehozza a Core Bridge-et, a UI Service Factory-t, és lekéri a Navigation Service-t.

**Visszatérési érték:**
- `bool`: True, ha sikeres az inicializálás

##### `run() -> None`

Az alkalmazás indítása. Ellenőrzi az inicializáltságot, majd elindítja a fő UI ciklust.

**Kivételek:**
- `RuntimeError`: Ha az alkalmazás nincs inicializálva

##### `stop() -> None`

Az alkalmazás leállítása. Beállítja a `_running` flag-et False-ra és naplózza a leállítást.

##### `get_navigation_service() -> "NavigationServiceInterface"`

Navigation Service lekérdezése.

**Visszatérési érték:**
- `NavigationServiceInterface`: A Navigation Service példány

**Kivételek:**
- `RuntimeError`: Ha az alkalmazás nincs inicializálva

##### `get_factory() -> UIServiceFactory`

UI Service Factory lekérdezése.

**Visszatérési érték:**
- `UIServiceFactory`: Az UI Service Factory példány

**Kivételek:**
- `RuntimeError`: Ha az alkalmazás nincs inicializálva

#### Tulajdonságok

##### `is_running: bool` (read-only)

Az alkalmazás futási állapotát ellenőrző property.

**Visszatérési érték:**
- `bool`: True, ha az alkalmazás fut, egyébként False

##### `is_initialized: bool` (read-only)

Az alkalmazás inicializáltságát ellenőrző property.

**Visszatérési érték:**
- `bool`: True, ha az alkalmazás inicializálva van, egyébként False

## Függőségek

- [`neural_ai.ui.core_bridge.CoreBridge`](core_bridge.md)
- [`neural_ai.ui.factory.UIServiceFactory`](factory.md)
- [`neural_ai.ui.interfaces.navigation_service_interface.NavigationServiceInterface`](interfaces/navigation_service_interface.md)
- [`neural_ai.core.logger.interfaces.logger_interface.LoggerInterface`](../../core/logger/interfaces/logger_interface.md)

## Használati példa

```python
from neural_ai.ui.app import UIApplication
from neural_ai.core.logger.factory import LoggerFactory

# Logger létrehozása
logger_factory = LoggerFactory()
logger = logger_factory.get_logger("ui")

# Alkalmazás létrehozása és indítása
app = UIApplication(config={"theme": "dark"}, logger=logger)

if app.initialize():
    try:
        app.run()
    except KeyboardInterrupt:
        app.stop()
```

## Típusjelölés (Type Hints)

A modul szigorú típusjelölést használ:
- Forward reference-ek idézőjelezése (`"NavigationServiceInterface"`)
- `TYPE_CHECKING` blokk a körkörös importok elkerülésére
- `Optional` típusok a None értékek kezelésére
- `Dict[str, Any]` a konfiguráció reprezentálására

## Hibakezelés

Az osztály robusztus hibakezelést valósít meg:
- Inicializálási hibák elkapása és naplózása
- Futási idejű hibák ellenőrzése (`is_initialized` property)
- `RuntimeError` dobása megfelelő hibaüzenettel