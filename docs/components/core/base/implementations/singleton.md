# SingletonMeta

## Áttekintés

A `SingletonMeta` egy metaclass, amely a singleton tervezési minta megvalósítását biztosítja. Ez garantálja, hogy minden osztályból, ami ezt a metaclass-t használja, csak egyetlen példány létezzen az alkalmazás életciklusa során.

## Mi az a Singleton?

A singleton egy tervezési minta, amely biztosítja, hogy egy osztályból csak egy példány létezhessen, és globális hozzáférési pontot biztosít hozzá. Ez különösen hasznos olyan esetekben, mint:

- Adatbázis kapcsolatok
- Konfiguráció kezelők
- Logging szolgáltatások
- Gyorsítótárak

## Jellemzők

- **Egyetlen példány**: Garantálja, hogy egy osztályból csak egy példány létezzen.
- **Globális hozzáférés**: Globális hozzáférési pontot biztosít a példányhoz.
- **Lusta inicializálás**: A példány csak az első hozzáféréskor jön létre.
- **DI kompatibilitás**: Kompatibilis a DI konténer ellenőrzéseivel.

## Használat

### Alapvető használat

```python
from neural_ai.core.base.implementations.singleton import SingletonMeta

class DatabaseConnection(metaclass=SingletonMeta):
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        print(f"Database connection created: {connection_string}")

# Első példányosítás
db1 = DatabaseConnection("sqlite:///mydb.db")
# Kimenet: "Database connection created: sqlite:///mydb.db"

# További példányosítás - ugyanazt a példányt adja vissza
db2 = DatabaseConnection("postgresql://localhost/mydb")
# Nincs kimenet, mert nem jön létre új példány

print(db1 is db2)  # True
print(db1.connection_string)  # "sqlite:///mydb.db"
print(db2.connection_string)  # "sqlite:///mydb.db" (ugyanaz!)
```

### Argumentumok nélkül

```python
class ConfigManager(metaclass=SingletonMeta):
    def __init__(self):
        self.settings = {"debug": True, "version": "1.0"}

config1 = ConfigManager()
config2 = ConfigManager()

assert config1 is config2
assert config1.settings is config2.settings
```

### Kulcsszavas argumentumokkal

```python
class Service(metaclass=SingletonMeta):
    def __init__(self, host: str = "localhost", port: int = 8080):
        self.host = host
        self.port = port

service1 = Service(host="example.com", port=9000)
service2 = Service(host="other.com", port=8000)

assert service1 is service2
assert service1.host == "example.com"  # Az első inicializálás értékei maradnak
assert service1.port == 9000
```

## Különböző osztályok

Különböző osztályok különböző singleton példányokat kapnak:

```python
class Logger(metaclass=SingletonMeta):
    def __init__(self, name: str):
        self.name = name

class Cache(metaclass=SingletonMeta):
    def __init__(self, size: int):
        self.size = size

logger = Logger("app")
cache = Cache(100)

assert logger is not cache  # Különböző példányok
```

## Többszörös öröklődés

A singleton működik többszörös öröklődés esetén is:

```python
class BaseService:
    def __init__(self):
        self.base_value = "base"

class DatabaseService(BaseService, metaclass=SingletonMeta):
    def __init__(self):
        super().__init__()
        self.db_value = "database"

service1 = DatabaseService()
service2 = DatabaseService()

assert service1 is service2
assert service1.base_value == "base"
assert service1.db_value == "database"
```

## DI Konténer kompatibilitás

A `SingletonMeta` biztosítja a DI konténer kompatibilitást az alábbi attribútumok beállításával:

### `_initialized` flag

Minden példány kap egy `_initialized` flag-et, amely True értéket tartalmaz:

```python
class Service(metaclass=SingletonMeta):
    def __init__(self):
        pass

service = Service()
assert hasattr(service, "_initialized")
assert service._initialized is True
```

### `_instance` class variable

Minden singleton osztály kap egy `_instance` class változót:

```python
class Service(metaclass=SingletonMeta):
    def __init__(self):
        pass

service = Service()
assert hasattr(Service, "_instance")
assert Service._instance is service
```

Ezek az attribútumok lehetővé teszik a DI konténer számára, hogy ellenőrizze a singleton minta helyes megvalósítását.

## Belső működés

### `_instances` szótár

A metaclass egy osztályszintű `_instances` szótárban tárolja a létrehozott példányokat:

```python
class Service(metaclass=SingletonMeta):
    def __init__(self):
        pass

service = Service()

# A példány benne van a szótárban
assert Service in SingletonMeta._instances
assert SingletonMeta._instances[Service] is service
```

### `__call__` metódus

A `SingletonMeta.__call__` metódusa felelős a singleton minta implementálásáért:

1. Ellenőrzi, hogy az osztály szerepel-e már az `_instances` szótárban.
2. Ha nem, létrehozza a példányt.
3. Beállítja az `_initialized` és `_instance` attribútumokat.
4. Eltárolja a példányt az `_instances` szótárban.
5. Visszaadja a meglévő vagy új példányt.

## Példák

### Adatbázis kapcsolat

```python
from sqlalchemy import create_engine
from neural_ai.core.base.implementations.singleton import SingletonMeta

class Database(metaclass=SingletonMeta):
    def __init__(self, connection_string: str):
        self.engine = create_engine(connection_string)
    
    def execute(self, query: str):
        with self.engine.connect() as conn:
            return conn.execute(query)

# Az egész alkalmazásban ugyanaz az adatbázis kapcsolat
db = Database("sqlite:///mydb.db")
```

### Konfiguráció kezelő

```python
import yaml
from neural_ai.core.base.implementations.singleton import SingletonMeta

class Config(metaclass=SingletonMeta):
    def __init__(self, config_file: str = "config.yml"):
        with open(config_file, 'r') as f:
            self._config = yaml.safe_load(f)
    
    def get(self, key: str, default=None):
        return self._config.get(key, default)

# Globális konfiguráció
config = Config()
debug = config.get("debug", False)
```

### Logger

```python
import logging
from neural_ai.core.base.implementations.singleton import SingletonMeta

class Logger(metaclass=SingletonMeta):
    def __init__(self, name: str = "app", level: int = logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def info(self, message: str):
        self.logger.info(message)
    
    def error(self, message: str):
        self.logger.error(message)

# Globális logger
logger = Logger("myapp")
logger.info("Application started")
```

## Tesztelés

A modul tesztelése a `tests/core/base/implementations/test_singleton.py` fájlban található. A tesztek 100% statement coverage-t érnek el, és minden metódust és attribútumot tesztelnek.

### Teszt példa

```python
from neural_ai.core.base.implementations.singleton import SingletonMeta

def test_singleton_creates_only_one_instance():
    class TestClass(metaclass=SingletonMeta):
        def __init__(self, value: int):
            self.value = value

    obj1 = TestClass(42)
    obj2 = TestClass(100)
    
    assert obj1 is obj2
    assert obj1.value == 42  # Az első inicializálás értéke marad
```

## Előnyök

1. **Egyszeri példányosítás**: Garantálja, hogy csak egy példány létezzen.
2. **Globális hozzáférés**: Könnyű hozzáférés az egész alkalmazásból.
3. **Lusta inicializálás**: A példány csak akkor jön létre, amikor először használják.
4. **Memória takarékos**: Csak egy példányt tárol a memóriában.
5. **DI kompatibilitás**: Kompatibilis a DI konténer ellenőrzéseivel.

## Korlátozások

1. **Tesztelhetőség**: A singleton nehezítheti a tesztelést, mert globális állapotot vezet be.
2. **Függőség rejtés**: Elrejti az osztály függőségeit.
3. **Párhuzamos hozzáférés**: Többszálú környezetben gondoskodni kell a szinkronizációról.

## Alternatívák

Bizonyos esetekben érdemes alternatívák után nézni:

- **DI konténer**: A függőségeket egy konténeren keresztül injektálhatjuk.
- **Factory minta**: Factory osztályt használhatunk a példányok létrehozásához.
- **Modul szintű változók**: Pythonban a modulok is singleton-ként viselkedhetnek.

## Összefoglalás

A `SingletonMeta` egy hatékony eszköz a singleton minta megvalósításához Pythonban. Biztosítja a minta helyes implementálását, DI kompatibilitást és egyszerű használatot. Azonban fontos mérlegelni a tesztelhetőséget és a függőség kezelést a használata előtt.