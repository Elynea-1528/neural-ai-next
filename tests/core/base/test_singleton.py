"""Tesztek a SingletonMeta metaklass-hoz.

Ez a modul tartalmazza a singleton tervezési minta megvalósításának
teszteseteit, beleértve a példány egyediségét, állapot megőrzését és
több osztály esetén a különböző példányok létrehozását.
"""

import pytest
from neural_ai.core.base.singleton import SingletonMeta


class TestSingletonBasic:
    """Alapvető singleton viselkedés tesztelése."""
    
    def test_singleton_creates_only_one_instance(self) -> None:
        """Teszteli, hogy csak egy példány jön létre."""
        class TestClass(metaclass=SingletonMeta):
            def __init__(self, value: int) -> None:
                self.value = value
        
        instance1 = TestClass(42)
        instance2 = TestClass(100)
        
        # Ellenőrizzük, hogy ugyanaz a példány
        assert instance1 is instance2
        assert id(instance1) == id(instance2)
    
    def test_singleton_preserves_initial_state(self) -> None:
        """Teszteli, hogy az első példány állapota megmarad."""
        class TestClass(metaclass=SingletonMeta):
            def __init__(self, value: int) -> None:
                self.value = value
        
        instance1 = TestClass(42)
        instance2 = TestClass(100)
        
        # Az első érték marad meg
        assert instance1.value == 42
        assert instance2.value == 42
        assert instance1.value == instance2.value
    
    def test_singleton_with_no_init_args(self) -> None:
        """Teszteli a singleton működését argumentumok nélkül."""
        class SimpleClass(metaclass=SingletonMeta):
            def __init__(self) -> None:
                self.created = True
        
        instance1 = SimpleClass()
        instance2 = SimpleClass()
        
        assert instance1 is instance2
        assert instance1.created is True
        assert instance2.created is True
    
    def test_singleton_with_kwargs(self) -> None:
        """Teszteli a singleton működését kulcsszavas argumentumokkal."""
        class ConfigClass(metaclass=SingletonMeta):
            def __init__(self, debug: bool = False, level: str = "INFO") -> None:
                self.debug = debug
                self.level = level
        
        instance1 = ConfigClass(debug=True, level="DEBUG")
        instance2 = ConfigClass(debug=False, level="WARNING")
        
        assert instance1 is instance2
        assert instance1.debug is True
        assert instance1.level == "DEBUG"


class TestMultipleSingletons:
    """Több különböző singleton osztály tesztelése."""
    
    def test_different_classes_create_different_instances(self) -> None:
        """Teszteli, hogy különböző osztályok különböző példányokat hoznak létre."""
        class ClassA(metaclass=SingletonMeta):
            def __init__(self) -> None:
                self.type = "A"
        
        class ClassB(metaclass=SingletonMeta):
            def __init__(self) -> None:
                self.type = "B"
        
        instance_a1 = ClassA()
        instance_a2 = ClassA()
        instance_b1 = ClassB()
        instance_b2 = ClassB()
        
        # Ugyanazon osztály példányai azonosak
        assert instance_a1 is instance_a2
        assert instance_b1 is instance_b2
        
        # Különböző osztályok példányai különbözőek
        assert instance_a1 is not instance_b1
        assert instance_a2 is not instance_b2
        
        # Ellenőrizzük az állapotot
        assert instance_a1.type == "A"
        assert instance_b1.type == "B"
    
    def test_multiple_singletons_independence(self) -> None:
        """Teszteli, hogy a különböző singletonok egymástól függetlenek."""
        class Logger(metaclass=SingletonMeta):
            def __init__(self, name: str) -> None:
                self.name = name
                self.logs: list[str] = []
        
        class Database(metaclass=SingletonMeta):
            def __init__(self, connection: str) -> None:
                self.connection = connection
        
        logger = Logger("app")
        database = Database("sqlite://db")
        
        # Különböző példányok
        assert logger is not database
        
        # Mindkettő singleton
        logger2 = Logger("different")
        database2 = Database("postgres://db")
        
        assert logger is logger2
        assert database is database2
        
        # Az eredeti értékek maradnak
        assert logger.name == "app"
        assert database.connection == "sqlite://db"


class TestSingletonStateModification:
    """Singleton állapot módosításának tesztelése."""
    
    def test_state_changes_visible_across_references(self) -> None:
        """Teszteli, hogy az állapot változások minden hivatkozásban láthatók."""
        class Counter(metaclass=SingletonMeta):
            def __init__(self) -> None:
                self.count = 0
            
            def increment(self) -> None:
                self.count += 1
        
        counter1 = Counter()
        counter2 = Counter()
        
        # Kezdeti állapot
        assert counter1.count == 0
        assert counter2.count == 0
        
        # Állapot módosítása
        counter1.increment()
        assert counter1.count == 1
        assert counter2.count == 1  # Ugyanaz a példány
        
        counter2.increment()
        assert counter1.count == 2
        assert counter2.count == 2
    
    def test_attribute_addition_visible_across_references(self) -> None:
        """Teszteli, hogy új attribútumok hozzáadása is látható minden hivatkozásban."""
        class DynamicClass(metaclass=SingletonMeta):
            def __init__(self) -> None:
                self.initial_attr = "initial"
        
        instance1 = DynamicClass()
        instance2 = DynamicClass()
        
        # Új attribútum hozzáadása
        instance1.new_attr = "dynamic"  # type: ignore[attr-defined]
        
        # Mindkét hivatkozás látja
        assert hasattr(instance2, 'new_attr')
        assert instance2.new_attr == "dynamic"  # type: ignore[attr-defined]


class TestSingletonEdgeCases:
    """Speciális esetek tesztelése."""
    
    def test_singleton_with_complex_initialization(self) -> None:
        """Teszteli a singleton működését komplex inicializálással."""
        class ComplexClass(metaclass=SingletonMeta):
            def __init__(self, data: dict[str, int]) -> None:
                self.data = data.copy()  # Másolat készítése
                self.sum_value = sum(data.values())
        
        data = {"a": 1, "b": 2, "c": 3}
        instance1 = ComplexClass(data)
        
        # Módosítjuk az eredeti adatot
        data["d"] = 4
        
        instance2 = ComplexClass(data)
        
        # A singleton az első inicializálás adatait használja
        assert instance1 is instance2
        assert instance1.sum_value == 6  # 1+2+3
        assert instance2.sum_value == 6
    
    def test_singleton_inheritance_behavior(self) -> None:
        """Teszteli a singleton viselkedését öröklődés esetén."""
        class BaseClass(metaclass=SingletonMeta):
            def __init__(self) -> None:
                self.base_attr = "base"
        
        class DerivedClass(BaseClass):
            def __init__(self) -> None:
                super().__init__()
                self.derived_attr = "derived"
        
        # A származtatott osztály külön singleton
        derived1 = DerivedClass()
        derived2 = DerivedClass()
        
        assert derived1 is derived2
        assert derived1.base_attr == "base"
        assert derived1.derived_attr == "derived"
        
        # Az alaposztály külön singleton
        base1 = BaseClass()
        base2 = BaseClass()
        
        assert base1 is base2
        assert base1.base_attr == "base"
        
        # A base és derived különböző példányok
        assert base1 is not derived1


class TestSingletonTypeSafety:
    """Típusbiztonság tesztelése."""
    
    def test_singleton_returns_correct_type(self) -> None:
        """Teszteli, hogy a singleton a helyes típust adja vissza."""
        class TypedClass(metaclass=SingletonMeta):
            def __init__(self, value: str) -> None:
                self.value = value
        
        instance = TypedClass("test")
        
        # Típus ellenőrzés
        assert isinstance(instance, TypedClass)
        assert type(instance) is TypedClass
    
    def test_singleton_with_type_annotations(self) -> None:
        """Teszteli a singleton működését típusannotációkkal."""
        class AnnotatedClass(metaclass=SingletonMeta):
            def __init__(self, number: int, text: str) -> None:
                self.number: int = number
                self.text: str = text
        
        instance1 = AnnotatedClass(42, "hello")
        instance2 = AnnotatedClass(100, "world")
        
        assert instance1 is instance2
        assert instance1.number == 42
        assert instance1.text == "hello"
        
        # Típus ellenőrzés
        assert isinstance(instance1.number, int)
        assert isinstance(instance1.text, str)


class TestSingletonIntegration:
    """Integrációs tesztek."""
    
    def test_singleton_with_multiple_attributes(self) -> None:
        """Teszteli a singleton működését több attribútummal."""
        class MultiAttrClass(metaclass=SingletonMeta):
            def __init__(self, x: int, y: int, z: int) -> None:
                self.x = x
                self.y = y
                self.z = z
                self.computed = x + y + z
        
        instance1 = MultiAttrClass(1, 2, 3)
        instance2 = MultiAttrClass(10, 20, 30)
        
        assert instance1 is instance2
        assert instance1.x == 1
        assert instance1.y == 2
        assert instance1.z == 3
        assert instance1.computed == 6
    
    def test_singleton_persistence_across_calls(self) -> None:
        """Teszteli, hogy a singleton tartósan megmarad."""
        class PersistentClass(metaclass=SingletonMeta):
            def __init__(self) -> None:
                self.call_count = 0
            
            def call(self) -> None:
                self.call_count += 1
        
        # Több hívás sorozat
        for _ in range(5):
            instance = PersistentClass()
            instance.call()
        
        # Utolsó ellenőrzés
        final_instance = PersistentClass()
        assert final_instance.call_count == 5


def test_singleton_meta_class_attributes() -> None:
    """Teszteli a SingletonMeta osztály attribútumait."""
    class TestClass(metaclass=SingletonMeta):
        pass
    
    # A metaklass-nak van _instances attribútuma
    assert hasattr(SingletonMeta, '_instances')
    assert isinstance(SingletonMeta._instances, dict)
    
    # Példányosítás után bekerül a szótárba
    instance = TestClass()
    assert TestClass in SingletonMeta._instances
    assert SingletonMeta._instances[TestClass] is instance


def test_singleton_meta_independence() -> None:
    """Teszteli, hogy a különböző osztályok külön bejegyzést kapnak."""
    class ClassA(metaclass=SingletonMeta):
        pass
    
    class ClassB(metaclass=SingletonMeta):
        pass
    
    instance_a = ClassA()
    instance_b = ClassB()
    
    # Mindkét osztály szerepel a szótárban
    assert ClassA in SingletonMeta._instances
    assert ClassB in SingletonMeta._instances
    
    # Különböző bejegyzések
    assert SingletonMeta._instances[ClassA] is instance_a
    assert SingletonMeta._instances[ClassB] is instance_b
    assert SingletonMeta._instances[ClassA] is not SingletonMeta._instances[ClassB]


# Szolgáltatói függvények tesztekhez

class TestSingletonWithFixtures:
    """Tesztek fixture-ökkel."""
    
    @pytest.fixture
    def singleton_class(self) -> type:
        """Singleton osztály fixture."""
        class FixtureClass(metaclass=SingletonMeta):
            def __init__(self, value: int = 0) -> None:
                self.value = value
        
        return FixtureClass
    
    def test_singleton_with_fixture(self, singleton_class: type) -> None:
        """Teszteli a singleton működését fixture-rel."""
        instance1 = singleton_class(42)
        instance2 = singleton_class(100)
        
        assert instance1 is instance2
        assert instance1.value == 42
    
    def test_multiple_singleton_classes_with_fixture(self, singleton_class: type) -> None:
        """Teszteli több singleton osztályt fixture-rel."""
        # Külön osztály definiálása
        class OtherClass(metaclass=SingletonMeta):
            def __init__(self, value: str = "") -> None:
                self.value = value
        
        instance1 = singleton_class(42)
        instance2 = OtherClass("test")
        
        assert instance1 is not instance2
        assert instance1.value == 42
        assert instance2.value == "test"


# Teljesítmény és stressz tesztek

class TestSingletonPerformance:
    """Teljesítmény tesztek."""
    
    def test_singleton_creation_performance(self) -> None:
        """Teszteli a singleton létrehozás teljesítményét."""
        class PerfClass(metaclass=SingletonMeta):
            def __init__(self) -> None:
                pass
        
        # Többszörös példányosítás
        instances: list[PerfClass] = []
        for _ in range(1000):
            instances.append(PerfClass())
        
        # Minden példány azonos
        first: PerfClass = instances[0]
        for instance in instances[1:]:
            assert instance is first
    
    def test_singleton_with_large_data(self) -> None:
        """Teszteli a singleton működését nagy adatmennyiséggel."""
        class LargeDataClass(metaclass=SingletonMeta):
            def __init__(self) -> None:
                self.data = list(range(10000))
        
        instance1 = LargeDataClass()
        instance2 = LargeDataClass()
        
        assert instance1 is instance2
        assert len(instance1.data) == 10000
        assert len(instance2.data) == 10000


# Cleanup és reset tesztek

class TestSingletonCleanup:
    """Singleton resetelésének tesztelése (csak tesztelési célokra)."""
    
    def test_singleton_reset_behavior(self) -> None:
        """Teszteli a singleton resetelését (nem ajánlott a termelési kódban)."""
        class ResettableClass(metaclass=SingletonMeta):
            def __init__(self, value: int) -> None:
                self.value = value
        
        # Első példány
        instance1 = ResettableClass(42)
        
        # Reset (csak tesztelési célokra!)
        if ResettableClass in SingletonMeta._instances:
            del SingletonMeta._instances[ResettableClass]
        
        # Új példány új értékkel
        instance2 = ResettableClass(100)
        
        # Mivel reseteltük, különböző példányok
        assert instance1 is not instance2
        assert instance1.value == 42
        assert instance2.value == 100


# Dokumentációs tesztek (doctest kompatibilitás)

def test_singleton_docstring_examples() -> None:
    """Teszteli a dokumentációban szereplő példákat."""
    # Első példa a dokumentációból
    class MyClass(metaclass=SingletonMeta):
        def __init__(self, value: int):
            self.value = value
    
    obj1 = MyClass(42)
    obj2 = MyClass(100)
    
    assert obj1 is obj2
    assert obj1.value == 42
    
    # Második példa a dokumentációból
    class Database(metaclass=SingletonMeta):
        def __init__(self, connection_string: str):
            self.connection_string = connection_string
    
    db1 = Database("sqlite:///mydb.db")
    db2 = Database("postgresql://localhost/mydb")
    
    assert db1 is db2
    assert db1.connection_string == "sqlite:///mydb.db"


# Konvenciók és best practices tesztek

class TestSingletonBestPractices:
    """Best practices tesztek."""
    
    def test_singleton_naming_convention(self) -> None:
        """Teszteli az elnevezési konvenciókat."""
        # Singleton osztályoknak egyértelműnek kell lenniük
        class ConfigurationManager(metaclass=SingletonMeta):
            pass
        
        class LoggerService(metaclass=SingletonMeta):
            pass
        
        # A név utaljon a singleton jellegre
        config = ConfigurationManager()
        logger = LoggerService()
        
        assert config is ConfigurationManager()
        assert logger is LoggerService()
    
    def test_singleton_with_clear_purpose(self) -> None:
        """Teszteli, hogy a singletonnak egyértelmű célja legyen."""
        class ResourceManager(metaclass=SingletonMeta):
            def __init__(self) -> None:
                self.resources: dict[str, object] = {}
            
            def register(self, name: str, resource: object) -> None:
                self.resources[name] = resource
            
            def get(self, name: str) -> object | None:
                return self.resources.get(name)
        
        manager1 = ResourceManager()
        manager2 = ResourceManager()
        
        assert manager1 is manager2
        
        # Erőforrás regisztráció
        manager1.register("db", {"connection": "test"})
        
        # A másik hivatkozás is látja
        assert manager2.get("db") == {"connection": "test"}


if __name__ == "__main__":
    pytest.main([__file__, "-v"])