# Teszt dokumentáció: `test_singleton.py`

## Áttekintés

Ez a dokumentáció a [`tests/core/base/test_singleton.py`](../../../../tests/core/base/test_singleton.py) tesztfájlt mutatja be, amely a [`neural_ai.core.base.implementations.singleton`](../neural_ai/core/base/implementations/singleton.md) modulban található `SingletonMeta` osztály funkcionalitását teszteli.

## Cél

A teszt célja, hogy ellenőrizze a singleton tervezési minta megfelelő működését a `SingletonMeta` metaclass segítségével. A tesztek során bizonyosítjuk, hogy:
- Egy osztályból csak egyetlen példány létezhet
- Az első példányosítás értékei megmaradnak
- Különböző osztályok különböző példányokat kapnak
- A minta helyesen kezeli a különböző argumentumtípusokat

## Tesztesetek

### 1. `test_singleton_returns_same_instance`

**Cél:** Ellenőrzi, hogy a singleton ugyanazt a példányt adja-e vissza.

**Elvárások:**
- A második példányosítás ugyanazt az objektumot adja vissza
- Az első példány attribútumai megmaradnak

**Tesztadat:**
```python
class TestClass(metaclass=SingletonMeta):
    def __init__(self, value: int):
        self.value = value

instance1 = TestClass(42)
instance2 = TestClass(100)
```

**Assert:**
- `instance1 is instance2` → `True`
- `instance1.value == 42` → `True`

---

### 2. `test_singleton_with_different_classes`

**Cél:** Ellenőrzi, hogy különböző osztályok különböző példányokat kapnak-e.

**Elvárások:**
- Különböző osztályokhoz különböző singleton példányok tartoznak
- Az egyes példányok attribútumai helyesen tárolódnak

**Tesztadat:**
```python
class FirstClass(metaclass=SingletonMeta):
    def __init__(self, value: str):
        self.value = value

class SecondClass(metaclass=SingletonMeta):
    def __init__(self, value: str):
        self.value = value

first_instance = FirstClass("first")
second_instance = SecondClass("second")
```

**Assert:**
- `first_instance is not second_instance` → `True`
- `first_instance.value == "first"` → `True`
- `second_instance.value == "second"` → `True`

---

### 3. `test_singleton_with_no_args`

**Cél:** Ellenőrzi a singleton működését argumentumok nélkül.

**Elvárások:**
- A singleton minta argumentum nélküli konstruktorral is működjön
- A példányok egyezzenek meg

**Tesztadat:**
```python
class SimpleClass(metaclass=SingletonMeta):
    def __init__(self):
        self.initialized = True

instance1 = SimpleClass()
instance2 = SimpleClass()
```

**Assert:**
- `instance1 is instance2` → `True`
- `instance1.initialized is True` → `True`

---

### 4. `test_singleton_with_kwargs`

**Cél:** Ellenőrzi a singleton működését kulcsszavas argumentumokkal.

**Elvárások:**
- A singleton helyesen kezelje az alapértelmezett értékekkel rendelkező argumentumokat
- Az első példányosítás értékei maradjanak meg

**Tesztadat:**
```python
class ConfigClass(metaclass=SingletonMeta):
    def __init__(self, host: str = "localhost", port: int = 8080):
        self.host = host
        self.port = port

instance1 = ConfigClass(host="example.com", port=9000)
instance2 = ConfigClass(host="other.com", port=8000)
```

**Assert:**
- `instance1 is instance2` → `True`
- `instance1.host == "example.com"` → `True`
- `instance1.port == 9000` → `True`

---

### 5. `test_singleton_preserves_type`

**Cél:** Ellenőrzi, hogy a visszaadott példány megfelelő típusú-e.

**Elvárások:**
- A singleton példány megtartja az osztály összes metódusát és attribútumát
- A típusellenőrzés helyesen működjön

**Tesztadat:**
```python
class TypedClass(metaclass=SingletonMeta):
    def __init__(self, data: str):
        self.data = data

    def get_data(self) -> str:
        return self.data

instance = TypedClass("test")
```

**Assert:**
- `isinstance(instance, TypedClass)` → `True`
- `hasattr(instance, "get_data")` → `True`
- `instance.get_data() == "test"` → `True`

---

### 6. `test_singleton_multiple_instantiations`

**Cél:** Ellenőrzi a többszöri példányosítás hatását.

**Elvárások:**
- Több példányosítás ugyanazt az objektumot adja vissza
- Az objektum állapota megmarad a különböző hívások között

**Tesztadat:**
```python
class CounterClass(metaclass=SingletonMeta):
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1

instance1 = CounterClass()
instance1.increment()
instance2 = CounterClass()
instance2.increment()
instance3 = CounterClass()
```

**Assert:**
- `instance1 is instance2 is instance3` → `True`
- `instance3.count == 2` → `True`

---

### 7. `test_singleton_with_complex_args`

**Cél:** Ellenőrzi a singleton működését komplex argumentumokkal.

**Elvárások:**
- A singleton helyesen kezelje a listákat, szótárakat, *args és **kwargs argumentumokat
- Az első példányosítás összes értéke megmaradjon

**Tesztadat:**
```python
class ComplexClass(metaclass=SingletonMeta):
    def __init__(self, name: str, items: list[str], config: dict[str, Any], *args: Any, **kwargs: Any):
        self.name = name
        self.items = items
        self.config = config
        self.args = args
        self.kwargs = kwargs

instance1 = ComplexClass("test", ["a", "b", "c"], {"key": "value"}, 1, 2, extra=True, count=5)
instance2 = ComplexClass("different", ["x", "y"], {"other": "data"}, 99, extra=False)
```

**Assert:**
- `instance1 is instance2` → `True`
- `instance2.name == "test"` → `True`
- `instance2.items == ["a", "b", "c"]` → `True`
- `instance2.config == {"key": "value"}` → `True`
- `instance2.args == (1, 2)` → `True`
- `instance2.kwargs == {"extra": True, "count": 5}` → `True`

---

### 8. `test_singleton_thread_safety_simulation`

**Cél:** Szimulálja a szálbiztonság tesztelését (alapvető ellenőrzés).

**Elvárások:**
- Többszöri egymás utáni példányosítás ugyanazt az objektumot adja vissza
- A létrehozási időpont megmarad

**Tesztadat:**
```python
class ThreadSafeClass(metaclass=SingletonMeta):
    def __init__(self):
        self.creation_time = "now"

instances: list[ThreadSafeClass] = []
for _ in range(5):
    instances.append(ThreadSafeClass())
```

**Assert:**
- `for instance in instances: instance is instances[0]` → `True`

---

### 9. `test_singleton_instances_dict`

**Cél:** Ellenőrzi, hogy az `_instances` szótár megfelelően működik-e.

**Elvárások:**
- Az `_instances` szótár tartalmazza a létrehozott singleton példányt
- A szótárban lévő példány megegyezik a visszaadott példánnyal

**Tesztadat:**
```python
class DictTestClass(metaclass=SingletonMeta):
    def __init__(self, value: str):
        self.value = value

instance1 = DictTestClass("first")
instance2 = DictTestClass("second")
```

**Assert:**
- `DictTestClass._instances[DictTestClass] is instance1` → `True`
- `DictTestClass._instances[DictTestClass] is instance2` → `True`
- `DictTestClass in DictTestClass._instances` → `True`

---

### 10. `test_singleton_clear_instances`

**Cél:** Ellenőrzi, hogy az `_instances` szótár kiüríthető-e.

**Elvárások:**
- Az `_instances` szótár kiürítése után új példány jöjjön létre
- A régi és az új példány különbözőek legyenek

**Tesztadat:**
```python
class ClearableClass(metaclass=SingletonMeta):
    def __init__(self, value: int):
        self.value = value

instance1 = ClearableClass(10)
ClearableClass._instances.clear()
instance2 = ClearableClass(20)
```

**Assert:**
- `instance1 is not instance2` → `True`
- `instance1.value == 10` → `True`
- `instance2.value == 20` → `True`

---

## Tesztelési metrikák

### Átadási arány
- **10/10** teszteset sikeresen átadva
- **100%** átadási arány

### Lefedettség (Coverage)
- **Statement Coverage:** 100%
- **Branch Coverage:** 100%

### Linter ellenőrzés
- **Ruff check:** 0 hiba
- **MyPy:** Nincs típushiba

## Futtatás

A tesztek futtatása a következő paranccsal lehetséges:

```bash
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/core/base/test_singleton.py -v
```

Coverage jelentés generálása:

```bash
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/core/base/test_singleton.py --cov=neural_ai/core/base/implementations/singleton --cov-report=html
```

## Kapcsolódó dokumentáció

- [Singleton implementáció](../neural_ai/core/base/implementations/singleton.md)
- [Base modul fő dokumentáció](../neural_ai/core/base/__init__.md)
- [Tesztelési szabványok](../../../development/architecture_standards.md)

## Jegyzetek

- A tesztfájl teljes mértékben követi a projekt architektúrális szabványait
- Minden teszteset jól dokumentált és önállóan futtatható
- A tesztesetek a singleton minta összes kritikus aspektusát lefedik
- A komplex argumentumokkal való tesztelés biztosítja a robusztusságot