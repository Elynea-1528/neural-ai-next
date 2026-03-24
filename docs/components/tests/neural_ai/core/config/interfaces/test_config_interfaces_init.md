# 🧪 Teszt: tests/neural_ai/core/config/interfaces/test_config_interfaces_init.py

**Tesztelt modul:** [`neural_ai/core/config/interfaces/config_interfaces_init.py`](../../neural_ai/core/config/interfaces/config_interfaces_init.py)

Unit tesztek a neural_ai.core.config.interfaces __init__ modulhoz.

Ez a modul teszteli a config interfaces modul publikus API-ját és exportált interfészeit.

## Teszt Osztály: `TestConfigInterfacesModuleExports`

Tesztek a config interfaces modul exportálásához.

### ✓ `test_interfaces_module_exports_config_manager_interface()`

Ellenőrzi, hogy az interfaces modul exportálja a ConfigManagerInterface-t.

### ✓ `test_interfaces_module_exports_factory_interface()`

Ellenőrzi, hogy az interfaces modul exportálja a ConfigManagerFactoryInterface-t.

### ✓ `test_interfaces_module_exports_pydantic_types()`

Ellenőrzi, hogy az interfaces modul exportálja a Pydantic típusokat.

### ✓ `test_interfaces_module_all_exports()`

Ellenőrzi, hogy a __all__ lista tartalmazza az összes exportált elemet.

## Teszt Osztály: `TestConfigManagerInterfaceMethods`

Tesztek a ConfigManagerInterface metódusaihoz.

### ✓ `test_config_manager_interface_has_get_method()`

Ellenőrzi, hogy a ConfigManagerInterface tartalmazza a get metódust.

### ✓ `test_config_manager_interface_has_get_section_method()`

Ellenőrzi, hogy a ConfigManagerInterface tartalmazza a get_section metódust.

### ✓ `test_config_manager_interface_has_validate_method()`

Ellenőrzi, hogy a ConfigManagerInterface tartalmazza a validate metódust.

## Teszt Osztály: `TestConfigManagerFactoryInterfaceMethods`

Tesztek a ConfigManagerFactoryInterface metódusaihoz.

### ✓ `test_factory_interface_has_create_manager_method()`

Ellenőrzi, hogy a ConfigManagerFactoryInterface tartalmazza a create_manager metódust.

## Teszt Osztály: `TestPydanticConfigModels`

Tesztek a Pydantic config modellekhez.

### ✓ `test_system_config_is_pydantic_model()`

Ellenőrzi, hogy a SystemConfig Pydantic BaseModel.

### ✓ `test_storage_config_is_pydantic_model()`

Ellenőrzi, hogy a StorageConfig Pydantic BaseModel.

### ✓ `test_processors_config_is_pydantic_model()`

Ellenőrzi, hogy a ProcessorsConfig Pydantic BaseModel.

### ✓ `test_logging_config_is_pydantic_model()`

Ellenőrzi, hogy a LoggingConfig Pydantic BaseModel.

### ✓ `test_database_config_is_pydantic_model()`

Ellenőrzi, hogy a DatabaseConfig Pydantic BaseModel.

### ✓ `test_events_config_is_pydantic_model()`

Ellenőrzi, hogy az EventsConfig Pydantic BaseModel.

### ✓ `test_collectors_config_is_pydantic_model()`

Ellenőrzi, hogy a CollectorsConfig Pydantic BaseModel.

### ✓ `test_config_schema_is_pydantic_model()`

Ellenőrzi, hogy a ConfigSchema Pydantic BaseModel.

---

**Teszt fájl:** [`tests/neural_ai/core/config/interfaces/test_config_interfaces_init.py`](../../tests/neural_ai/core/config/interfaces/test_config_interfaces_init.py)

**Tesztelt modul:** [`neural_ai/core/config/interfaces/config_interfaces_init.py`](../../neural_ai/core/config/interfaces/config_interfaces_init.py)
