# Config Komponens Használati Példák

## 1. Alap használat

### 1.1 Konfiguráció betöltése

```python
from neural_ai.core.config.implementations import ConfigManagerFactory

# YAML konfiguráció betöltése
config = ConfigManagerFactory.get_manager("configs/app.yaml")

# Értékek lekérése
app_name = config.get("app.name", default="MyApp")
log_level = config.get("logger.level", default="INFO")
```

### 1.2 Konfigurációs fájl példa

```yaml
# configs/app.yaml
app:
  name: "MyApp"
  version: "1.0.0"

logger:
  level: "INFO"
  format: "detailed"
  outputs:
    - type: "console"
      colored: true
    - type: "file"
      path: "logs/app.log"

storage:
  base_path: "/data"
  formats:
    - "csv"
    - "json"
```

## 2. Haladó használat

### 2.1 Szekciók kezelése

```python
# Teljes szekció lekérése
logger_config = config.get_section("logger")

# Szekció validálással
storage_config = config.get_section("storage", required=True)

# Alapértelmezett értékekkel
db_config = config.get_section("database", default={
    "host": "localhost",
    "port": 5432
})
```

### 2.2 Környezeti változók használata

```python
# Környezeti változó prioritással
db_url = config.get(
    "database.url",
    env_key="DB_URL",
    default="postgresql://localhost/db"
)

# Környezeti változók gyökere
CONFIG_ROOT = "MYAPP"  # MYAPP_DB_URL, MYAPP_API_KEY, stb.
config = ConfigManagerFactory.get_manager(
    "configs/app.yaml",
    env_prefix=CONFIG_ROOT
)
```

## 3. Validáció

### 3.1 Séma validáció

```python
from neural_ai.core.config.implementations import YAMLConfigManager

# Séma definíció
schema = {
    "type": "object",
    "properties": {
        "app": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "version": {"type": "string"}
            },
            "required": ["name"]
        }
    }
}

# Konfiguráció validálással
config = YAMLConfigManager("configs/app.yaml", schema=schema)
```

### 3.2 Egyedi validátorok

```python
from neural_ai.core.config.interfaces import ConfigValidator

class PortValidator(ConfigValidator):
    def validate(self, value: int) -> None:
        if not isinstance(value, int):
            raise ValueError("Port must be an integer")
        if value < 1 or value > 65535:
            raise ValueError("Port must be between 1 and 65535")

# Validátor használata
config.register_validator("server.port", PortValidator())
```

## 4. Dinamikus konfiguráció

### 4.1 Konfiguráció módosítása

```python
# Érték beállítása
config.set("app.debug", True)

# Szekció módosítása
config.update_section("logger", {
    "level": "DEBUG",
    "format": "detailed"
})

# Konfiguráció mentése
config.save()
```

### 4.2 Változás figyelés

```python
from neural_ai.core.config.implementations import ConfigObserver

class LogLevelObserver(ConfigObserver):
    def on_change(self, key: str, old_value: Any, new_value: Any) -> None:
        if key == "logger.level":
            logger.setLevel(new_value)

# Observer regisztrálása
config.add_observer("logger.level", LogLevelObserver())
```

## 5. Hibakezelés

### 5.1 Kivételek kezelése

```python
from neural_ai.core.config.exceptions import (
    ConfigNotFoundError,
    ConfigValidationError,
    ConfigKeyError
)

try:
    value = config.get("database.password", required=True)
except ConfigKeyError:
    # Hiányzó kulcs kezelése
    value = prompt_password()
except ConfigValidationError as e:
    # Validációs hiba kezelése
    logger.error(f"Érvénytelen konfiguráció: {e}")
    raise
```

### 5.2 Fallback értékek

```python
# Több szintű fallback
db_url = (
    config.get("database.url") or
    os.getenv("DB_URL") or
    "sqlite:///default.db"
)

# Biztonságos konfiguráció lekérés
def get_config_safe(key: str, fallback: Any = None) -> Any:
    try:
        return config.get(key)
    except Exception as e:
        logger.warning(f"Konfiguráció lekérési hiba: {e}")
        return fallback
```

## 6. Integrációs példák

### 6.1 Logger konfigurálás

```python
logger_config = config.get_section("logger")
logger = LoggerFactory.create_logger(__name__, **logger_config)
```

### 6.2 Storage konfigurálás

```python
storage_config = config.get_section("storage")
storage = StorageFactory.get_storage(**storage_config)
```

### 6.3 Adatbázis konfigurálás

```python
db_config = config.get_section("database")
engine = create_engine(
    db_config["url"],
    pool_size=db_config.get("pool_size", 5),
    max_overflow=db_config.get("max_overflow", 10)
)
