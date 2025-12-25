# Integrációs Teszt - Bootstrap (`test_bootstrap.py`)

## Áttekintés

Ez a dokumentáció a [`tests/integration/test_bootstrap.py`](../../../tests/integration/test_bootstrap.py) integrációs tesztfájlt ismerteti, amely a Neural AI Next rendszer fő indító szkriptjének ([`main.py`](../../../main.py)) megfelelő működését ellenőrzi az új CoreComponents struktúra szerint.

## Cél

A tesztmodul célja ellenőrizni, hogy a fő alkalmazás belépési pontja ([`main()`](../../../main.py:13) függvény) megfelelően inicializálja-e a rendszer alapvető komponenseit az új [`bootstrap_core()`](../../../neural_ai/core/__init__.py:89) függvény és [`CoreComponents`](../../../neural_ai/core/__init__.py:47) osztály használatával.

## Tesztosztályok

### 1. `TestMainBootstrap`

Ez az osztály a [`main()`](../../../main.py:13) függvény indítási folyamatát teszteli.

#### Főbb tesztesetek

- **`test_main_function_exists`**: Ellenőrzi, hogy a `main` függvény létezik-e.
- **`test_main_function_is_coroutine`**: Ellenőrzi, hogy a `main` függvény async függvény-e.
- **`test_main_calls_bootstrap_core`**: Ellenőrzi, hogy a `main` függvény meghívja-e a [`bootstrap_core()`](../../../neural_ai/core/__init__.py:89) függvényt.
- **`test_main_calls_event_bus_start`**: Ellenőrzi, hogy a `main` függvény meghívja-e a [`components.event_bus.start()`](../../../main.py:19) metódust.
- **`test_main_calls_database_initialize`**: Ellenőrzi, hogy a `main` függvény meghívja-e a [`components.database.initialize()`](../../../main.py:22) metódust.
- **`test_main_waits_with_event`**: Ellenőrzi, hogy a `main` függvény az [`asyncio.Event().wait()`](../../../main.py:25) hívást végzi.
- **`test_main_handles_keyboard_interrupt`**: Ellenőrzi, hogy a `main` függvény kezeli-e a `KeyboardInterrupt` kivételt.
- **`test_main_handles_general_exception`**: Ellenőrzi, hogy a `main` függvény továbbadja-e az általános kivételeket (mivel a [`main.py`](../../../main.py) nem tartalmaz hibakezelést).
- **`test_main_handles_database_initialization_error`**: Ellenőrzi, hogy a `main` függvény továbbadja-e az adatbázis inicializálási hibákat.
- **`test_main_handles_event_bus_start_error`**: Ellenőrzi, hogy a `main` függvény továbbadja-e az event bus indítási hibákat.

### 2. `TestBootstrapCore`

Ez az osztály a [`bootstrap_core()`](../../../neural_ai/core/__init__.py:89) függvényt teszteli.

#### Főbb tesztesetek

- **`test_bootstrap_core_function_exists`**: Ellenőrzi, hogy a `bootstrap_core` függvény létezik-e.
- **`test_bootstrap_core_returns_core_components`**: Ellenőrzi, hogy a `bootstrap_core` függvény [`CoreComponents`](../../../neural_ai/core/__init__.py:47) objektumot ad vissza.
- **`test_core_components_has_required_attributes`**: Ellenőrzi, hogy a [`CoreComponents`](../../../neural_ai/core/__init__.py:47) osztály rendelkezik-e a szükséges attribútumokkal (`config`, `logger`, `storage`, `database`, `event_bus`, `hardware`).

### 3. `TestCoreModule`

Ez az osztály a core modul globális függvényeit teszteli.

#### Főbb tesztesetek

- **`test_get_version_exists`**: Ellenőrzi, hogy a `get_version` függvény létezik-e.
- **`test_get_version_returns_string`**: Ellenőrzi, hogy a `get_version` függvény stringet ad vissza.
- **`test_get_schema_version_exists`**: Ellenőrzi, hogy a `get_schema_version` függvény létezik-e.
- **`test_get_schema_version_returns_string`**: Ellenőrzi, hogy a `get_schema_version` függvény a helyes séma verziót adja vissza ("1.0.0").
- **`test_get_core_components_exists`**: Ellenőrzi, hogy a `get_core_components` függvény létezik-e.
- **`test_get_core_components_returns_singleton`**: Ellenőrzi, hogy a `get_core_components` függvény szingleton példányt ad vissza.

## Mockolás

A tesztesetek során a következő komponenseket mockoljuk:

- **`bootstrap_core`**: A core komponensek inicializálásának elkerülésére.
- **`CoreComponents`**: A tényleges komponensek helyett mock objektumokat használunk.
- **`asyncio.Event`**: Az örök futás elkerülésére.
- **`AsyncMock`**: Az async metódusok (pl. `event_bus.start`, `database.initialize`) mockolására.

## Futtatás

A tesztek futtatása a következő paranccsal lehetséges:

```bash
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/integration/test_bootstrap.py -v
```

## Tesztlefedettség

A tesztfájl jelenleg **19 tesztesetet** tartalmaz, amelyek mindegyike sikeresen lefut. A tesztlefedettség a következő területeket érinti:

- Fő alkalmazás belépési pont ([`main()`](../../../main.py:13) függvény)
- Core komponensek inicializálása ([`bootstrap_core()`](../../../neural_ai/core/__init__.py:89) függvény)
- Core komponensek tároló osztálya ([`CoreComponents`](../../../neural_ai/core/__init__.py:47) osztály)
- Core modul globális függvényei (`get_version`, `get_schema_version`, `get_core_components`)

## Változások az új CoreComponents struktúrához képest

A tesztfájlt frissítettük az új CoreComponents struktúra szerint. A főbb változások:

1. **Régi struktúra**: Külön `setup_database`, `setup_event_bus`, stb. függvények
2. **Új struktúra**: Egyetlen [`bootstrap_core()`](../../../neural_ai/core/__init__.py:89) függvény, ami egy [`CoreComponents`](../../../neural_ai/core/__init__.py:47) objektumot ad vissza

A tesztesetek ennek megfelelően lettek átírva:

- A `test_main_calls_config_loading` helyett most a `test_main_calls_bootstrap_core` teszteli a core inicializálást.
- A `test_main_calls_database_setup` helyett most a `test_main_calls_database_initialize` teszteli az adatbázis inicializálást.
- A `test_main_calls_event_bus_setup` helyett most a `test_main_calls_event_bus_start` teszteli az event bus indítását.
- A `TestSetupFunctions` osztályt teljesen eltávolítottuk, mivel a régi setup függvények már nem léteznek.
- A `TestStaticConfig` osztályt lecseréltük a `TestBootstrapCore` és `TestCoreModule` osztályokra, amelyek az új struktúrát tesztelik.

## Hibakezelés

A [`main.py`](../../../main.py) jelenleg nem tartalmaz explicit hibakezelést (nincs `try-except` blokk és `sys.exit()` hívás). Emiatt a teszteseteknek nem a `sys.exit()` hívást kell ellenőrizniük, hanem azt, hogy a kivételek továbbadódnak-e. Erre a következő tesztesetekben került sor:

- `test_main_handles_general_exception`
- `test_main_handles_database_initialization_error`
- `test_main_handles_event_bus_start_error`

Ezek a tesztesetek a `pytest.raises()` kontextuskezelőt használják a kivétel elkapására.

## Kapcsolódó dokumentáció

- [Main szkript dokumentáció](../../main.md)
- [Core komponensek dokumentáció](../neural_ai/core/__init__.md)
- [CoreComponents osztály dokumentáció](../neural_ai/core/base/core_components.md)
- [Bootstrap függvény dokumentáció](../neural_ai/core/__init__.md)