# Base Komponens Használati Példák

## 1. Komponens Inicializálás

### 1.1 Alap inicializálás

```python
from neural_ai.core.base.core_components import CoreComponents
from neural_ai.core.base.container import DIContainer
from neural_ai.core.base.factory import CoreComponentFactory

# Konténer és komponensek létrehozása
container = DIContainer()
components = CoreComponentFactory.create_components()

# Komponensek használata
components.logger.info("Alkalmazás indítása")
config = components.config.get_section("app")
```

### 1.2 Egyedi konfigurációval

```python
config = {
    "logger": {
        "level": "INFO",
        "format": "detailed"
    },
    "storage": {
        "base_path": "/data"
    }
}

components = CoreComponentFactory.create_components(config)
```

## 2. Dependency Injection

### 2.1 Komponens regisztráció

```python
from typing import Protocol

class DataProcessor(Protocol):
    def process(self, data: Any) -> Any: ...

class CustomProcessor:
    def process(self, data: Any) -> Any:
        return data * 2

# Regisztráció
container = DIContainer()
container.register_instance(DataProcessor, CustomProcessor())

# Használat
processor = container.resolve(DataProcessor)
result = processor.process(10)  # returns 20
```

### 2.2 Factory függvény regisztráció

```python
def create_processor() -> DataProcessor:
    return CustomProcessor()

container.register_factory(DataProcessor, create_processor)
```

## 3. CoreComponents használata

### 3.1 Komponensek elérése

```python
class DataAnalyzer:
    def __init__(self, components: CoreComponents) -> None:
        self.logger = components.logger
        self.config = components.config
        self.storage = components.storage

    def analyze(self, data: pd.DataFrame) -> Dict[str, Any]:
        self.logger.info("Elemzés kezdése")
        try:
            result = self._perform_analysis(data)
            self.storage.save_object(result, "analysis_result.json")
            return result
        except Exception as e:
            self.logger.error(f"Elemzési hiba: {e}")
            raise
```

### 3.2 Komponens validáció

```python
def validate_components(components: CoreComponents) -> None:
    """Komponensek elérhetőségének ellenőrzése."""
    if components.logger is None:
        raise ValueError("Logger komponens nem elérhető")
    if components.config is None:
        raise ValueError("Config komponens nem elérhető")
    if components.storage is None:
        raise ValueError("Storage komponens nem elérhető")
```

## 4. Életciklus kezelés

### 4.1 Komponens inicializálás sorrendje

```python
class Application:
    def __init__(self) -> None:
        # 1. Config inicializálás
        self.components = CoreComponentFactory.create_components()

        # 2. Logger konfigurálás
        log_config = self.components.config.get_section("logger")
        self.components.logger.configure(log_config)

        # 3. Storage inicializálás
        storage_config = self.components.config.get_section("storage")
        self.components.storage.initialize(storage_config)

    def start(self) -> None:
        self.components.logger.info("Alkalmazás indítása")
```

### 4.2 Erőforrások felszabadítása

```python
class Application:
    def __init__(self) -> None:
        self.components = CoreComponentFactory.create_components()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.cleanup()

    def cleanup(self) -> None:
        """Erőforrások felszabadítása."""
        if hasattr(self.components.storage, 'close'):
            self.components.storage.close()
        if hasattr(self.components.logger, 'close'):
            self.components.logger.close()
```

## 5. Hibakezelés

### 5.1 Komponens hibák kezelése

```python
from neural_ai.core.base.exceptions import ComponentError

try:
    components = CoreComponentFactory.create_components()
except ComponentError as e:
    print(f"Hiba a komponensek létrehozásakor: {e}")
    raise SystemExit(1)
```

### 5.2 Graceful degradation

```python
class FallbackLogger:
    def info(self, msg: str) -> None:
        print(f"INFO: {msg}")
    def error(self, msg: str) -> None:
        print(f"ERROR: {msg}", file=sys.stderr)

def get_logger(components: CoreComponents) -> LoggerInterface:
    """Logger komponens biztonságos lekérése."""
    try:
        if components.logger:
            return components.logger
    except Exception as e:
        print(f"Logger nem elérhető: {e}")
    return FallbackLogger()
