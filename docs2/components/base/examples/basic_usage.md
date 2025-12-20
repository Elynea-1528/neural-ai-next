# Alapvető Használati Példák

## Áttekintés

Ez a dokumentum a Base komponens alapvető használati példáit tartalmazza. Ezek a példák segítenek megérteni, hogyan lehet a Base komponenst használni gyakori feladatokhoz.

## Tartalomjegyzék

1. [Komponensek létrehozása](#komponensek-létrehozása)
2. [Alapvető műveletek](#alapvető-műveletek)
3. [Hibakezelés](#hibakezelés)
4. [Lazy loading demonstráció](#lazy-loading-demonstráció)
5. [Komponensek ellenőrzése](#komponensek-ellenőrzése)
6. [Memóriahasználat monitorozása](#memóriahasználat-monitorozása)

## Komponensek létrehozása

### 1. Alapvető inicializálás

```python
from neural_ai.core.base import CoreComponentFactory, CoreComponents

# Komponensek létrehozása a Factory-vel
components: CoreComponents = CoreComponentFactory.create_components(
    config_path='configs/system_config.yaml',
    log_path='logs/app.log',
    storage_path='./data'
)

print("Komponensek sikeresen létrehozva")
print(f"Logger elérhető: {components.has_logger()}")
print(f"Config elérhető: {components.has_config()}")
print(f"Storage elérhető: {components.has_storage()}")
```

### 2. Minimális konfiguráció

```python
from neural_ai.core.base import CoreComponentFactory

# Minimális komponens készlet létrehozása
components = CoreComponentFactory.create_minimal()

# Használat
if components.has_logger():
    components.logger.info("Minimális konfigurációval működik")

if components.has_storage():
    components.storage.save_object({"test": "data"}, "test.json")
```

### 3. Egyedi komponens regisztráció

```python
from neural_ai.core.base import DIContainer, CoreComponents

# Konténer létrehozása
container = DIContainer()

# Egyedi komponens hozzáadása
class MyCustomService:
    def process(self, data):
        return f"Processed: {data}"

container.register_instance(MyCustomService, MyCustomService())

# Core komponensek létrehozása a konténerrel
components = CoreComponents(container=container)

# Használat
custom_service = container.get(MyCustomService)
result = custom_service.process("test data")
print(result)  # "Processed: test data"
```

## Alapvető műveletek

### 1. Naplózás

```python
from neural_ai.core.base import CoreComponentFactory

# Komponensek létrehozása
components = CoreComponentFactory.create_components(
    log_path='logs/application.log'
)

# Naplózás különböző szinteken
components.logger.debug("Részletes hibakeresési információ")
components.logger.info("Információs üzenet")
components.logger.warning("Figyelmeztető üzenet")
components.logger.error("Hibaüzenet")
components.logger.critical("Kritikus hiba")
```

### 2. Konfiguráció kezelés

```python
from neural_ai.core.base import CoreComponentFactory

# Komponensek létrehozása
components = CoreComponentFactory.create_components(
    config_path='configs/app_config.yaml'
)

# Konfigurációs szekciók lekérdezése
app_config = components.config.get_section('app')
database_config = components.config.get_section('database')
logger_config = components.config.get_section('logger')

# Konkrét beállítások lekérdezése
app_name = app_config.get('name')
database_host = database_config.get('host')
log_level = logger_config.get('level')

print(f"Alkalmazás neve: {app_name}")
print(f"Adatbázis hoszt: {database_host}")
print(f"Log szint: {log_level}")
```

### 3. Adattárolás

```python
from neural_ai.core.base import CoreComponentFactory
import json

# Komponensek létrehozása
components = CoreComponentFactory.create_components(
    storage_path='./data'
)

# Objektum mentése
user_data = {
    "id": 123,
    "name": "John Doe",
    "email": "john@example.com",
    "preferences": {
        "theme": "dark",
        "language": "hu"
    }
}

components.storage.save_object(user_data, "users/user_123.json")
print("Felhasználói adatok elmentve")

# Objektum betöltése
loaded_data = components.storage.load_object("users/user_123.json")
print(f"Betöltött adatok: {json.dumps(loaded_data, indent=2)}")

# Fájl létezésének ellenőrzése
if components.storage.file_exists("users/user_123.json"):
    print("A fájl létezik")
```

### 4. Komponensek együttes használata

```python
from neural_ai.core.base import CoreComponentFactory

# Komponensek létrehozása
components = CoreComponentFactory.create_components(
    config_path='configs/app_config.yaml',
    log_path='logs/app.log',
    storage_path='./data'
)

# Alkalmazás indítása
components.logger.info("Alkalmazás elindítva")

# Konfiguráció betöltése
app_config = components.config.get_section('app')
components.logger.info(f"Alkalmazás neve: {app_config.get('name')}")

# Adatok mentése
status_data = {
    "status": "running",
    "started_at": "2025-12-19T10:00:00",
    "version": app_config.get('version')
}

components.storage.save_object(status_data, "status.json")
components.logger.info("Állapot információk elmentve")

# Alkalmazás leállítása
components.logger.info("Alkalmazás leállítva")
```

## Hibakezelés

### 1. Komponens nem található

```python
from neural_ai.core.base import DIContainer
from neural_ai.core.base.exceptions import ComponentNotFoundError

container = DIContainer()

try:
    component = container.get('non_existent_component')
    print("Komponens sikeresen lekérve")
except ComponentNotFoundError as e:
    print(f"Hiba: {e}")
    print("A komponens nem található a konténerben")
    # Alternatív megoldás
    fallback_component = get_fallback_component()
    print("Fallback komponens használata")
```

### 2. Konfigurációs hiba

```python
from neural_ai.core.base import CoreComponentFactory
from neural_ai.core.base.exceptions import ConfigurationError

try:
    components = CoreComponentFactory.create_components(
        config_path='non_existent_config.yaml'
    )
    print("Komponensek sikeresen létrehozva")
except ConfigurationError as e:
    print(f"Konfigurációs hiba: {e}")
    print("Alapértelmezett konfiguráció használata")
    components = CoreComponentFactory.create_minimal()
```

### 3. Tárolási hiba

```python
from neural_ai.core.base import CoreComponentFactory
from neural_ai.core.base.exceptions import (
    StorageWriteError,
    StorageReadError,
    InsufficientDiskSpaceError
)

components = CoreComponentFactory.create_components(
    storage_path='./data'
)

# Írási hiba kezelése
try:
    large_data = {"data": "x" * 10000000}  # Nagy adat
    components.storage.save_object(large_data, "large_file.json")
except StorageWriteError as e:
    print(f"Írási hiba: {e}")
except InsufficientDiskSpaceError as e:
    print(f"Nincs elég lemezterület: {e}")
    print("Adatok tömörítése vagy törlése")

# Olvasási hiba kezelése
try:
    data = components.storage.load_object("non_existent_file.json")
except StorageReadError as e:
    print(f"Olvasási hiba: {e}")
    print("Alapértelmezett adatok használata")
    data = get_default_data()
```

### 4. Függőségi hiba

```python
from neural_ai.core.base import CoreComponentFactory
from neural_ai.core.base.exceptions import DependencyError

try:
    # Komponensek létrehozása hiányzó függőségekkel
    components = CoreComponentFactory.create_components()
    if not components.validate():
        raise DependencyError("Néhány komponens hiányzik")
except DependencyError as e:
    print(f"Függőségi hiba: {e}")
    print("Minimális komponens készlet használata")
    components = CoreComponentFactory.create_minimal()
```

## Lazy loading demonstráció

### 1. Alapvető lazy loading

```python
from neural_ai.core.base import CoreComponentFactory
import time

# Komponensek létrehozása
components = CoreComponentFactory.create_components(
    config_path='configs/app_config.yaml',
    log_path='logs/app.log',
    storage_path='./data'
)

print("Komponensek létrehozva, de még nincsenek betöltve")

# Logger használata (első alkalommal töltődik be)
print("\n1. Logger használata (első alkalommal töltődik be):")
start_time = time.time()
components.logger.info("Első naplóbejegyzés")
end_time = time.time()
print(f"Betöltési idő: {end_time - start_time:.2f} másodperc")

# Config használata (első alkalommal töltődik be)
print("\n2. Config használata (első alkalommal töltődik be):")
start_time = time.time()
settings = components.config.get_section('app')
end_time = time.time()
print(f"Betöltési idő: {end_time - start_time:.2f} másodperc")

# Második használat (már betöltve van)
print("\n3. Második használat (már betöltve van):")
start_time = time.time()
components.logger.info("Második naplóbejegyzés")
end_time = time.time()
print(f"Hozzáférési idő: {end_time - start_time:.4f} másodperc")
```

### 2. Preload használata

```python
from neural_ai.core.base import CoreComponentFactory
import time

# Komponensek létrehozása
components = CoreComponentFactory.create_components(
    config_path='config.yaml',
    log_path='app.log',
    storage_path='./data'
)

print("Komponensek előtöltése...")
start_time = time.time()
components.preload_all()
end_time = time.time()
print(f"Előtöltési idő: {end_time - start_time:.2f} másodperc")

print("\nKomponensek használata (azonnal elérhetők):")
start_time = time.time()
components.logger.info("Azonnali hozzáférés")
settings = components.config.get_section('app')
components.storage.save_object({}, "test.json")
end_time = time.time()
print(f"Használati idő: {end_time - start_time:.4f} másodperc")
```

### 3. LazyLoader egyedi használata

```python
from neural_ai.core.base.lazy_loading import LazyLoader
import time

def load_expensive_resource():
    """Drága erőforrás betöltése."""
    print("Erőforrás betöltése...")
    time.sleep(3)  # Szimulált drága művelet
    return {"data": [1, 2, 3, 4, 5], "timestamp": time.time()}

# Lazy loader létrehozása
resource_loader = LazyLoader(load_expensive_resource)

print("Lazy loader létrehozva")
print(f"Betöltve: {resource_loader.is_loaded}")

# Erőforrás használata
print("\nErőforrás első használata:")
start_time = time.time()
resource = resource_loader()
end_time = time.time()
print(f"Betöltési idő: {end_time - start_time:.2f} másodperc")
print(f"Betöltve: {resource_loader.is_loaded}")
print(f"Adatok: {resource}")

# Második használat (már betöltve van)
print("\nErőforrás második használata:")
start_time = time.time()
resource2 = resource_loader()
end_time = time.time()
print(f"Hozzáférési idő: {end_time - start_time:.4f} másodperc")
print(f"Azonos objektum: {resource is resource2}")
```

## Komponensek ellenőrzése

### 1. Alapvető ellenőrzés

```python
from neural_ai.core.base import CoreComponentFactory

# Komponensek létrehozása
components = CoreComponentFactory.create_components(
    config_path='config.yaml',
    log_path='app.log',
    storage_path='./data'
)

# Komponensek ellenőrzése
print("Komponens ellenőrzés:")
print(f"  Logger elérhető: {components.has_logger()}")
print(f"  Config elérhető: {components.has_config()}")
print(f"  Storage elérhető: {components.has_storage()}")

# Teljes validáció
if components.validate():
    print("\nMinden komponens elérhető, az alkalmazás készen áll")
else:
    print("\nFigyelmeztetés: néhány komponens hiányzik")
    if not components.has_config():
        print("  - Konfiguráció hiányzik")
    if not components.has_logger():
        print("  - Logger hiányzik")
    if not components.has_storage():
        print("  - Storage hiányzik")
```

### 2. Komponens állapot nyomon követése

```python
from neural_ai.core.base import DIContainer

# Konténer létrehozása
container = DIContainer()

# Több lazy komponens regisztrálása
container.register_lazy('logger', lambda: create_logger())
container.register_lazy('config', lambda: create_config())
container.register_lazy('storage', lambda: create_storage())

# Lazy komponensek állapotának ellenőrzése
print("Kezdeti állapot:")
lazy_status = container.get_lazy_components()
for component, loaded in lazy_status.items():
    print(f"  {component}: {'Betöltve' if loaded else 'Nem betöltve'}")

# Egy komponens használata
print("\nLogger használata...")
logger = container.get('logger')

# Állapot ellenőrzése újra
print("\nLogger használata után:")
lazy_status = container.get_lazy_components()
for component, loaded in lazy_status.items():
    print(f"  {component}: {'Betöltve' if loaded else 'Nem betöltve'}")
```

## Memóriahasználat monitorozása

### 1. Memóriastatisztikák lekérdezése

```python
from neural_ai.core.base import DIContainer

# Konténer létrehozása és feltöltése
container = DIContainer()

# Több komponens regisztrálása
container.register_lazy('service1', lambda: Service1())
container.register_lazy('service2', lambda: Service2())
container.register_lazy('service3', lambda: Service3())

# Memóriahasználat ellenőrzése
print("Kezdeti memóriahasználat:")
stats = container.get_memory_usage()
print(f"  Összes példány: {stats['total_instances']}")
print(f"  Lazy komponensek: {stats['lazy_components']}")
print(f"  Betöltött lazy komponensek: {stats['loaded_lazy_components']}")

# Néhány komponens használata
print("\nKomponensek használata...")
service1 = container.get('service1')
service2 = container.get('service2')

# Memóriahasználat ellenőrzése újra
print("\nKomponensek használata után:")
stats = container.get_memory_usage()
print(f"  Összes példány: {stats['total_instances']}")
print(f"  Lazy komponensek: {stats['lazy_components']}")
print(f"  Betöltött lazy komponensek: {stats['loaded_lazy_components']}")
print(f"  Példány méretek: {stats['instance_sizes']}")
```

### 2. Memóriahasználat optimalizálás

```python
from neural_ai.core.base import DIContainer, LazyLoader
import sys

class MemoryIntensiveService:
    def __init__(self):
        self.data = [i for i in range(10**6)]  # 1 millió elem

# Konténer létrehozása
container = DIContainer()

# Nagy memóriát igénylő szolgáltatás regisztrálása
container.register_lazy('heavy_service', lambda: MemoryIntensiveService())

print("Konténer létrehozva")
print(f"Memóriahasználat: {sys.getsizeof(container)} bájt")

# Szolgáltatás használata (csak most töltődik be)
print("\nSzolgáltatás használata...")
service = container.get('heavy_service')
service_size = sys.getsizeof(service.data)
print(f"Szolgáltatás mérete: {service_size} bájt")

# Memóriastatisztikák
stats = container.get_memory_usage()
print(f"Összes példány: {stats['total_instances']}")
print(f"Példány méretek: {stats['instance_sizes']}")
```

## Gyakorlati példák

### 1. Webalkalmazás inicializálása

```python
from neural_ai.core.base import CoreComponentFactory
from flask import Flask

# Komponensek létrehozása
components = CoreComponentFactory.create_components(
    config_path='configs/webapp_config.yaml',
    log_path='logs/webapp.log',
    storage_path='./data'
)

# Flask alkalmazás létrehozása
app = Flask(__name__)

# Konfiguráció betöltése
app_config = components.config.get_section('flask')
app.secret_key = app_config.get('secret_key')

# Route definiálása
@app.route('/')
def index():
    components.logger.info("Index oldal meglátogatva")
    return "Hello World!"

@app.route('/status')
def status():
    components.logger.info("Status oldal meglátogatva")
    status_data = {
        "status": "ok",
        "version": app_config.get('version')
    }
    components.storage.save_object(status_data, "status.json")
    return status_data

if __name__ == '__main__':
    components.logger.info("Webalkalmazás indítása")
    app.run(
        host=app_config.get('host', '0.0.0.0'),
        port=app_config.get('port', 5000),
        debug=app_config.get('debug', False)
    )
```

### 2. Adatfeldolgozó alkalmazás

```python
from neural_ai.core.base import CoreComponentFactory
import pandas as pd

# Komponensek létrehozása
components = CoreComponentFactory.create_components(
    config_path='configs/data_processor.yaml',
    log_path='logs/processor.log',
    storage_path='./processed_data'
)

def process_data(input_file, output_file):
    """Adatok feldolgozása."""
    components.logger.info(f"Adatok feldolgozása: {input_file}")

    try:
        # Konfiguráció betöltése
        processor_config = components.config.get_section('processor')
        chunk_size = processor_config.get('chunk_size', 1000)

        # Adatok beolvasása
        components.logger.info("Adatok beolvasása")
        df = pd.read_csv(input_file, chunksize=chunk_size)

        processed_chunks = []
        for i, chunk in enumerate(df):
            components.logger.debug(f"Chunk {i+1} feldolgozása")

            # Adatok feldolgozása
            processed_chunk = process_chunk(chunk)
            processed_chunks.append(processed_chunk)

        # Eredmények összefűzése
        result = pd.concat(processed_chunks)

        # Eredmények mentése
        components.storage.save_object(result.to_dict(), output_file)
        components.logger.info(f"Feldolgozás befejezve: {output_file}")

        return True

    except Exception as e:
        components.logger.error(f"Hiba a feldolgozás során: {e}")
        return False

def process_chunk(chunk):
    """Chunk feldolgozása."""
    # Feldolgozási logika
    return chunk

# Használat
success = process_data('input.csv', 'output.json')
if success:
    print("Feldolgozás sikeres")
else:
    print("Feldolgozás sikertelen")
```

## Kapcsolódó dokumentáció

- [API Áttekintés](../api/overview.md)
- [Haladó példák](advanced_usage.md)
- [Egyedi komponensek](custom_components.md)
- [Tesztelési példák](testing.md)
- [Fejlesztési útmutató](../guides/getting_started.md)

---

**Dokumentum verzió:** 1.0
**Utolsó frissítés:** 2025-12-19
**Példák:** Alapvető használat
