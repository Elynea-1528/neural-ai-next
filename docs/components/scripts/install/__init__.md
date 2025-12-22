# scripts.install - Telepítő Rendszer

## Áttekintés

A `scripts.install` modul a Neural AI Next keretrendszer telepítési folyamatát kezelő fő komponenseket tartalmazza. Ez a modul biztosítja a telepítési konfiguráció kezelését, a függőségek ellenőrzését, a telepítési lépések koordinációját és a hibakezelést.

## Fő Komponensek

### InstallationError

Kivétel osztály a telepítési hibák kezelésére.

**Attribútumok:**
- `message`: A hiba részletes leírása magyar nyelven
- `error_code`: Opcionális hibakód a hibák kategorizálásához
- `installation_step`: Annak a lépésnek a neve, ahol a hiba fellépett

**Használat:**
```python
from scripts.install import InstallationError

try:
    # Telepítési művelet
    pass
except Exception as e:
    raise InstallationError(
        message="Telepítési hiba történt",
        error_code="INSTALL_ERROR",
        installation_step="dependencies_install"
    )
```

### InstallationConfig

Telepítési konfiguráció kezelő osztály, amely felelős a konfigurációs beállítások betöltéséért, validálásáért és kezeléséért.

**Attribútumok:**
- `config_data`: Konfigurációs beállítások szótárban tárolva
- `config_file_path`: A konfigurációs fájl elérési útja

**Metódusok:**

#### `__init__(config_file_path=None, config_manager=None)`
Inicializálja a konfiguráció kezelőt.

#### `load_config()`
Betölti a konfigurációs beállításokat a megadott fájlból vagy alapértelmezett konfigurációt használ.

#### `validate_config() -> tuple[bool, list[str]]`
Validálja a betöltött konfigurációs beállításokat. Visszaad egy tuple-t, amely tartalmazza a validálás sikerességét és a hibák listáját.

**Használat:**
```python
from scripts.install import InstallationConfig

config = InstallationConfig()
config.load_config()
successful, errors = config.validate_config()

if not successful:
    print(f"Konfigurációs hibák: {errors}")
```

### InstallationController

Telepítési folyamat vezérlő osztálya, amely koordinálja a telepítési lépéseket.

**Attribútumok:**
- `config`: A telepítési konfiguráció objektuma
- `logger`: A naplózó interfész (opcionális)
- `installation_steps`: A végrehajtandó telepítési lépések listája

**Metódusok:**

#### `__init__(config, logger=None)`
Inicializálja a telepítési vezérlőt.

#### `add_installation_step(step_name: str) -> None`
Hozzáad egy új telepítési lépést a végrehajtandó lépések listájához.

#### `remove_installation_step(step_name: str) -> None`
Eltávolít egy telepítési lépést a listából.

#### `start_installation() -> bool`
Elindítja a telepítési folyamatot. Visszaadja a telepítés sikerességét.

**Használat:**
```python
from scripts.install import InstallationConfig, InstallationController

config = InstallationConfig()
controller = InstallationController(config=config)

# Egyéni lépés hozzáadása
controller.add_installation_step("custom_step")

# Telepítés indítása
try:
    success = controller.start_installation()
    if success:
        print("A telepítés sikeresen befejeződött.")
except Exception as e:
    print(f"Telepítési hiba: {e}")
```

### installation_controller

Gyárfüggvény az InstallationController létrehozásához.

**Paraméterek:**
- `config`: Opcionális InstallationConfig objektum
- `logger`: Opcionális LoggerInterface objektum

**Visszatérési érték:**
- Egy új InstallationController példány

**Használat:**
```python
from scripts.install import installation_controller

# Alapértelmezett vezérlő létrehozása
controller = installation_controller()

# Vagy egyéni konfigurációval
config = InstallationConfig()
controller = installation_controller(config=config)
```

## Alapértelmezett Telepítési Lépések

A modul a következő alapértelmezett telepítési lépéseket támogatja:

1. **check_dependencies**: Ellenőrzi a szükséges függőségeket
2. **activate_environment**: Aktiválja a conda környezetet
3. **create_install_directory**: Létrehozza a telepítési könyvtárat
4. **install_dependencies**: Telepíti a szükséges függőségeket
5. **setup_mt5**: Beállítja az MT5 környezetet (ha konfigurálva van)
6. **setup_jupyter**: Beállítja a Jupyter notebook környezetet

## Konfiguráció

Az alapértelmezett konfiguráció a következő beállításokat tartalmazza:

```python
{
    "install_directory": "/opt/neural-ai-next",
    "python_path": "/home/elynea/miniconda3/envs/neural-ai-next/bin/python",
    "environment_name": "neural-ai-next",
    "dependencies": [
        "numpy", "pandas", "scikit-learn", "torch", "transformers",
        "yaml", "pytest", "ruff", "mypy"
    ],
    "mt5_installation": True,
    "wine_config": {
        "prefix": "~/.wine-mt5",
        "arch": "win64"
    },
    "jupyter_settings": {
        "port": 8888,
        "password_protected": True
    }
}
```

## Hibakezelés

A modul átfogó hibakezelést biztosít a telepítési folyamat során:

- **InstallationError**: Speciális kivétel osztály a telepítési hibákhoz
- **Konfigurációs validálás**: Automatikus konfiguráció ellenőrzés
- **Lépésenkénti hibajelzés**: Pontos hibajelzés az egyes telepítési lépéseknél

## Példa: Teljes Telepítési Folyamat

```python
from scripts.install import (
    InstallationConfig,
    InstallationController,
    installation_controller
)

# Konfiguráció létrehozása
config = InstallationConfig()

# Telepítési vezérlő létrehozása
controller = installation_controller(config=config)

# Telepítés indítása
try:
    success = controller.start_installation()
    if success:
        print("✅ A Neural AI Next telepítése sikeresen befejeződött.")
    else:
        print("❌ A telepítés sikertelen.")
except Exception as e:
    print(f"❌ Hiba történt a telepítés során: {e}")
```

## Fejlesztés

### Típusbiztonság

A modul szigorú típusellenőrzést használ a `mypy` segítségével. Minden függvény és metódus tartalmaz típusannotációkat.

### Tesztelés

A modulhoz átfogó unit tesztek tartoznak a `tests/scripts/install/test___init__.py` fájlban. A tesztek 94% kódfedettséget érnek el.

### Linter

A kód `ruff` linterrel van ellenőrizve, és 0 hiba állapotban van.

## Kapcsolódó Dokumentáció

- [Telepítési útmutató](../../INSTALLATION_GUIDE.md)
- [Fejlesztői dokumentáció](../../development/implementation_guide.md)
- [Típusbiztonság és linting](../../development/code_review_guide.md)
