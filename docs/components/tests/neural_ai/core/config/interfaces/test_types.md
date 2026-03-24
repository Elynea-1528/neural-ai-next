# 🧪 Teszt: tests/neural_ai/core/config/interfaces/test_types.py

**Tesztelt modul:** [`neural_ai/core/config/interfaces/types.py`](../../neural_ai/core/config/interfaces/types.py)

Unit tesztek a neural_ai.core.config.interfaces.types modulhoz.

Ez a modul teszteli a Pydantic config típusokat és validációt.

## Teszt Osztály: `TestPydanticConfigTypesExist`

Tesztek a Pydantic config típusok létezéséhez.

### ✓ `test_system_config_exists()`

Ellenőrzi, hogy a SystemConfig létezik.

### ✓ `test_storage_config_exists()`

Ellenőrzi, hogy a StorageConfig létezik.

### ✓ `test_processors_config_exists()`

Ellenőrzi, hogy a ProcessorsConfig létezik.

### ✓ `test_logging_config_exists()`

Ellenőrzi, hogy a LoggingConfig létezik.

### ✓ `test_database_config_exists()`

Ellenőrzi, hogy a DatabaseConfig létezik.

### ✓ `test_events_config_exists()`

Ellenőrzi, hogy az EventsConfig létezik.

### ✓ `test_collectors_config_exists()`

Ellenőrzi, hogy a CollectorsConfig létezik.

### ✓ `test_config_schema_exists()`

Ellenőrzi, hogy a ConfigSchema létezik.

## Teszt Osztály: `TestPydanticBaseModelInheritance`

Tesztek a Pydantic BaseModel örökléshez.

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

## Teszt Osztály: `TestPydanticValidation`

Tesztek a Pydantic validációhoz.

### ✓ `test_handler_config_validates_level_pattern()`

Ellenőrzi, hogy a HandlerConfig validálja a level pattern-t.

### ✓ `test_paths_config_validates_min_length()`

Ellenőrzi, hogy a PathsConfig validálja a min_length-et.

### ✓ `test_handler_config_validates_max_bytes_positive()`

Ellenőrzi, hogy a HandlerConfig validálja a max_bytes pozitív értékét.

### ✓ `test_handler_config_validates_backup_count_non_negative()`

Ellenőrzi, hogy a HandlerConfig validálja a backup_count nem-negatív értékét.

## Teszt Osztály: `TestPydanticModelConfig`

Tesztek a Pydantic model config-hoz.

### ✓ `test_system_config_forbids_extra_fields()`

Ellenőrzi, hogy a SystemConfig tiltja az extra mezőket.

### ✓ `test_storage_config_forbids_extra_fields()`

Ellenőrzi, hogy a StorageConfig tiltja az extra mezőket.

### ✓ `test_config_schema_forbids_extra_fields()`

Ellenőrzi, hogy a ConfigSchema tiltja az extra mezőket.

## Teszt Osztály: `TestAdditionalConfigTypes`

Tesztek további config típusokhoz.

### ✓ `test_paths_config_exists()`

Ellenőrzi, hogy a PathsConfig létezik.

### ✓ `test_handler_config_exists()`

Ellenőrzi, hogy a HandlerConfig létezik.

### ✓ `test_logger_config_exists()`

Ellenőrzi, hogy a LoggerConfig létezik.

### ✓ `test_ingestion_config_exists()`

Ellenőrzi, hogy az IngestionConfig létezik.

### ✓ `test_ui_config_exists()`

Ellenőrzi, hogy a UIConfig létezik.

---

**Teszt fájl:** [`tests/neural_ai/core/config/interfaces/test_types.py`](../../tests/neural_ai/core/config/interfaces/test_types.py)

**Tesztelt modul:** [`neural_ai/core/config/interfaces/types.py`](../../neural_ai/core/config/interfaces/types.py)
