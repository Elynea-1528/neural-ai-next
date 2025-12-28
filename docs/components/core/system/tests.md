# System Modul Teszt Dokumentáció

## Áttekintés

Ez a dokumentáció a `neural_ai.core.system` modul tesztsuite-jét írja le. A tesztek a következő célokat szolgálják:

- **Típusbiztonság**: Minden metódusnak kötelező a helyes visszatérési típusa
- **Magyar nyelvű dokumentáció**: Az összes teszt és docstring magyar nyelven van megírva
- **100% Coverage**: A tesztek célja a teljes kódlefedettség elérése
- **Strict Type Hints**: `MagicMock` objektumok annotálása és szigorú típusellenőrzés

## Teszt Struktúra

### 1. Factory Tesztek (`tests/core/system/test_factory.py`)

A `SystemComponentFactory` osztály tesztjei, amely a következőket ellenőrzik:

#### Alapvető funkcionalitás
- `test_create_health_monitor_default`: Alapértelmezett HealthMonitor létrehozása
- `test_create_health_monitor_with_name`: HealthMonitor létrehozása névvel
- `test_create_health_monitor_with_logger`: HealthMonitor létrehozása loggerrel
- `test_create_health_monitor_caching`: Gyorsítótár tesztelése

#### HealthCheck létrehozás
- `test_create_health_check_default`: Alapértelmezett HealthCheck létrehozása
- `test_create_health_check_with_logger`: HealthCheck létrehozása loggerrel
- `test_create_health_check_invalid_type`: Érvénytelen típus kezelése

#### Komponens kezelés
- `test_register_component`: Komponens regisztrálása
- `test_register_component_with_custom_check`: Komponens regisztrálása egyedi ellenőrzéssel
- `test_register_component_nonexistent_monitor`: Hibakezelés nem létező monitorhoz
- `test_unregister_component`: Komponens eltávolítása
- `test_unregister_component_nonexistent_monitor`: Hibakezelés nem létező monitorból

#### Monitor kezelés
- `test_get_health_monitor`: HealthMonitor lekérdezése
- `test_get_health_monitor_nonexistent`: Nem létező monitor lekérdezése
- `test_get_registered_monitors`: Regisztrált monitorok listázása
- `test_clear_monitors`: Monitorok törlése

#### Integrációs tesztek
- `test_health_monitor_integration`: Teljes integrációs teszt
- `test_health_monitor_with_system_metrics`: Rendszer metrikák gyűjtésének tesztelése
- `test_register_component_fallback_implementation`: Fallback implementáció tesztelése

### 2. HealthMonitor Implementáció Tesztek (`tests/core/system/implementations/test_health_monitor.py`)

A `HealthMonitor` és `DefaultHealthCheck` osztályok tesztjei.

#### DefaultHealthCheck tesztek
- `test_check_returns_healthy`: Ellenőrzi, hogy a check metódus mindig HEALTHY státuszt ad vissza
- `test_get_name_returns_component_name`: Ellenőrzi a komponensnév visszaadását
- `test_default_health_check_with_logger`: Loggerrel való használat tesztelése

#### HealthMonitor alapvető tesztek
- `test_initial_state`: Kezdeti állapot ellenőrzése
- `test_register_component`: Komponens regisztráció
- `test_register_component_with_custom_check`: Egyedi ellenőrzéssel való regisztráció
- `test_unregister_component`: Komponens eltávolítás
- `test_unregister_nonexistent_component`: Nem létező komponens eltávolítása

#### Egészségügyi ellenőrzések
- `test_check_component_success`: Sikeres komponens ellenőrzés
- `test_check_component_nonexistent`: Nem létező komponens ellenőrzése
- `test_check_component_with_exception`: Kivétel kezelése komponens ellenőrzésénél

#### Rendszer egészségügyi állapot
- `test_check_health_no_components`: Üres komponenslista tesztelése
- `test_check_health_with_healthy_components`: Egészséges komponensekkel
- `test_check_health_with_warning_component`: Figyelmeztető komponenssel
- `test_check_health_with_critical_component`: Kritikus komponenssel
- `test_check_health_mixed_components`: Vegyes komponensekkel
- `test_check_health_with_exception_in_component_check`: Kivétel kezelése check_health-ban
- `test_check_health_with_unknown_status_components`: Ismeretlen státuszú komponensekkel

#### Rendszer metrikák
- `test_collect_system_metrics_success`: Sikeres metrikagyűjtés
- `test_collect_system_metrics_with_exception`: Kivétel kezelése metrikagyűjtésnél
- `test_collect_system_metrics_with_disk_error`: Lemezhiba kezelése
- `test_collect_system_metrics_with_net_error`: Hálózati hiba kezelése
- `test_collect_system_metrics_logs_error_on_exception`: Error logolás tesztelése

#### Logger funkcionalitás
- `test_register_component_with_logger`: Komponens regisztráció logolással
- `test_unregister_component_with_logger`: Komponens eltávolítás logolással
- `test_register_duplicate_component`: Duplikált regisztráció kezelése
- `test_unregister_component_logs_warning_when_not_registered`: Warning logolás nem regisztrált komponensnél

### 3. Health Interface Tesztek (`tests/core/system/interfaces/test_health_interface.py`)

Az interfészek és adatmodell osztályok tesztjei.

#### Enum tesztek
- `TestComponentStatus`: ComponentStatus enum értékeinek és tagjainak tesztelése
- `TestHealthStatus`: HealthStatus enum értékeinek és tagjainak tesztelése

#### Adatmodell tesztek
- `TestComponentHealth`: 
  - Létrehozás kötelező mezőkkel
  - Létrehozás opcionális metrikákkal
  - Adatok megváltoztathatóságának tesztelése

- `TestSystemHealth`:
  - Létrehozás kötelező mezőkkel
  - Létrehozás opcionális metrikákkal
  - Üres komponenslista kezelése

#### Interfész tesztek
- `TestHealthMonitorInterface`:
  - Interfész absztraktságának ellenőrzése
  - Metódusok absztraktságának ellenőrzése
  - Interfész implementációjának tesztelése

- `TestHealthCheckInterface`:
  - Interfész absztraktságának ellenőrzése
  - Check metódus absztraktságának ellenőrzése
  - Interfész implementációjának tesztelése

#### Integrációs tesztek
- `TestIntegration`: 
  - ComponentHealth integrációja SystemHealth-ben
  - Egészségügyi állapotok aggregációjának tesztelése

#### Típusbiztonság tesztek
- `TestTypeSafety`:
  - ComponentStatus típusának ellenőrzése
  - HealthStatus típusának ellenőrzése
  - ComponentHealth mezőinek típusellenőrzése
  - SystemHealth mezőinek típusellenőrzése

## Típusannotációk és Best Practices

### MagicMock Annotációk

Minden `MagicMock` objektumot explicit módon annotálni kell:

```python
def test_example(self) -> None:
    """Példa teszt metódus."""
    mock_logger: MagicMock = MagicMock()
    mock_check: MagicMock = MagicMock(spec=HealthCheckInterface)
```

### Visszatérési Típusok

Minden teszt metódusnak kötelező a `-> None` visszatérési típus:

```python
def test_example(self) -> None:
    """Példa teszt metódus."""
    # Teszt logika
```

### Type Narrowing

Ha egy változó típusa `Optional`, akkor a használat előtt ellenőrizni kell:

```python
metrics = health.system_metrics
assert metrics is not None  # Type narrowing
self.assertIn("cpu_percent", metrics)
```

## Teszt Futtatása

### Összes teszt futtatása

```bash
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/core/system/ -v
```

### Coverage reporttal

```bash
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/core/system/ --cov=neural_ai.core.system --cov-report=term-missing
```

### Jelenlegi Coverage

- **neural_ai/core/system/__init__.py**: 100%
- **neural_ai/core/system/factory.py**: 100%
- **neural_ai/core/system/implementations/health_monitor.py**: 96%
- **neural_ai/core/system/interfaces/health_interface.py**: 87%
- **Összesen**: 94%

A hiányzó sorok főleg interfész definíciókban lévő abstract metódusok, amelyek nem számítanak bele a coverage-ba.

## Teszt Elvek

1. **Dependency Injection**: Minden teszt csak interfészeken keresztül kommunikál
2. **Type Safety**: Szigorú típusellenőrzés mindenhol
3. **Magyar nyelv**: Az összes dokumentáció és üzenet magyarul
4. **Comprehensive**: Minden edge case és error handling le van fedve
5. **Isolated**: Minden teszt független a többitől

## Hibakeresés

Ha egy teszt bukik, a következő lépéseket kell követni:

1. Futtasd a tesztet külön: `pytest [fájl_útvonal]::[Osztály]::[teszt_metódus] -v`
2. Ellenőrizd a hibaüzenetet és a stack trace-et
3. Javítsd a hibát a kódban vagy a teszthez
4. Futtasd újra a teljes tesztcsomagot
5. Ellenőrizd, hogy minden teszt átmegy-e

## Commit Előtti Ellenőrzés

Mielőtt commitolsz, mindig ellenőrizd:

1. Minden teszt átmegy: `pytest tests/core/system/`
2. Nincs linting hiba: `ruff check tests/core/system/`
3. A coverage legalább 90%: `pytest --cov=neural_ai.core.system tests/core/system/`
4. Minden új fájl rendelkezik megfelelő dokumentációval