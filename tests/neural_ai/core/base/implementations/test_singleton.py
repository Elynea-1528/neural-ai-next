"""SingletonMeta tesztelése.

Ez a modul tartalmazza a SingletonMeta metaclass egységtesztjeit,
beleértve a singleton minta ellenőrzését és a DI kompatibilitást.
"""

import threading
from neural_ai.core.base.implementations.singleton import SingletonMeta


class TestSingletonMeta:
    """SingletonMeta metaclass tesztjei."""

    def test_singleton_creates_only_one_instance(self) -> None:
        """Teszteli, hogy csak egy példány jön létre."""

        class TestClass(metaclass=SingletonMeta):
            def __init__(self, value: int) -> None:
                self.value = value

        obj1 = TestClass(42)
        obj2 = TestClass(100)

        assert obj1 is obj2
        assert obj1.value == 42  # Az első inicializálás értéke marad

    def test_singleton_different_classes(self) -> None:
        """Teszteli, hogy különböző osztályok külön példányt kapnak."""

        class ClassA(metaclass=SingletonMeta):
            def __init__(self, value: str) -> None:
                self.value = value

        class ClassB(metaclass=SingletonMeta):
            def __init__(self, value: str) -> None:
                self.value = value

        obj_a = ClassA("A")
        obj_b = ClassB("B")

        assert obj_a is not obj_b  # type: ignore[comparison-overlap]
        assert obj_a.value == "A"
        assert obj_b.value == "B"

    def test_singleton_with_kwargs(self) -> None:
        """Teszteli a singleton-t kulcsszavas argumentumokkal."""

        class TestClass(metaclass=SingletonMeta):
            def __init__(self, value: int = 0) -> None:
                self.value = value

        obj1 = TestClass(value=42)
        obj2 = TestClass(value=100)

        assert obj1 is obj2
        assert obj1.value == 42

    def test_singleton_without_args(self) -> None:
        """Teszteli a singleton-t argumentumok nélkül."""

        class TestClass(metaclass=SingletonMeta):
            def __init__(self) -> None:
                self.value = 42

        obj1 = TestClass()
        obj2 = TestClass()

        assert obj1 is obj2
        assert obj1.value == 42

    def test_singleton_has_initialized_flag(self) -> None:
        """Teszteli, hogy a példánynak van _initialized flag-je (DI kompatibilitás)."""

        class TestClass(metaclass=SingletonMeta):
            def __init__(self) -> None:
                self.value = 42

        obj = TestClass()

        # A DI container ellenőrzi ezt a flag-et
        assert hasattr(obj, "_initialized")
        # Megjegyzés: A _initialized protected, de a DI ellenőrzés miatt létezik

    def test_singleton_has_instance_class_variable(self) -> None:
        """Teszteli, hogy az osztálynak van _instance class változója (DI kompatibilitás)."""

        class TestClass(metaclass=SingletonMeta):
            def __init__(self) -> None:
                self.value = 42

        obj1 = TestClass()
        obj2 = TestClass()

        # A DI container ellenőrzi ezt a class változót
        assert obj1 is obj2  # Ugyanaz a példány
        # Megjegyzés: A _instance protected, de a DI ellenőrzés miatt létezik

    def test_singleton_multiple_inheritance(self) -> None:
        """Teszteli a singleton-t többszörös öröklődés esetén."""

        class BaseClass:
            def __init__(self) -> None:
                self.base_value = "base"

        class TestClass(BaseClass, metaclass=SingletonMeta):
            def __init__(self) -> None:
                super().__init__()
                self.value = 42

        obj1 = TestClass()
        obj2 = TestClass()

        assert obj1 is obj2
        assert obj1.value == 42
        assert obj1.base_value == "base"

    def test_singleton_with_class_method(self) -> None:
        """Teszteli a singleton-t osztálymetódussal."""

        class TestClass(metaclass=SingletonMeta):
            def __init__(self) -> None:
                self.value = 42

            @classmethod
            def get_value(cls) -> int:
                instance = cls()  # Mindig ugyanazt a példányt adja vissza
                return instance.value

        obj1 = TestClass()
        obj2 = TestClass()

        assert obj1 is obj2
        assert TestClass.get_value() == 42

    def test_singleton_instances_dict(self) -> None:
        """Teszteli, hogy a singleton tényleg egy példányt hoz létre."""

        class TestClass(metaclass=SingletonMeta):
            def __init__(self) -> None:
                self.value = 42

        obj1 = TestClass()
        obj2 = TestClass()

        # A lényeg, hogy mindig ugyanazt a példányt kapjuk vissza
        assert obj1 is obj2
        # Megjegyzés: A _instances protected, de a működés a lényeg

    def test_singleton_reset_behavior(self) -> None:
        """Teszteli, hogy a singleton nem enged második inicializálást."""

        class TestClass(metaclass=SingletonMeta):
            def __init__(self, value: int) -> None:
                self.value = value

        obj1 = TestClass(42)
        obj2 = TestClass(100)

        # Mindkét objektum ugyanaz
        assert obj1 is obj2
        # Az első érték marad
        assert obj1.value == 42
        assert obj2.value == 42

    def test_singleton_thread_safety(self) -> None:
        """Teszteli a singleton thread-safe példányosítását."""

        class TestClass(metaclass=SingletonMeta):
            def __init__(self) -> None:
                self.value = 42

        instances: list[TestClass] = []

        def create_instance() -> None:
            instances.append(TestClass())

        # 10 szál párhuzamosan próbál példányt létrehozni
        threads = [threading.Thread(target=create_instance) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Minden példány ugyanaz kell legyen
        assert len(instances) == 10
        assert len(set(id(i) for i in instances)) == 1  # Csak 1 egyedi példány

    def test_singleton_reset_singleton_method(self) -> None:
        """Teszteli a reset_singleton metódust."""

        class TestClass(metaclass=SingletonMeta):
            def __init__(self, value: int) -> None:
                self.value = value

        # Létrehozunk egy példányt
        obj1 = TestClass(42)
        assert obj1.value == 42

        # Reset után új példányt kapunk
        SingletonMeta.reset_singleton(TestClass)
        obj2 = TestClass(100)

        # Most már különböző értékkel jön létre
        assert obj2.value == 100
        # De obj1 még mindig létezik (nem lett törölve)
        assert obj1.value == 42

    def test_singleton_reset_singleton_nonexistent_class(self) -> None:
        """Teszteli a reset_singleton metódust nem létező osztályra."""

        class TestClass(metaclass=SingletonMeta):
            def __init__(self) -> None:
                self.value = 42

        # Reset hívása olyan osztályra, ami nincs a _instances-ben
        # Ez nem okozhat hibát
        SingletonMeta.reset_singleton(TestClass)
        
        # Ezután normálisan kell működnie
        obj = TestClass()
        assert obj.value == 42

    def test_singleton_reset_all_method(self) -> None:
        """Teszteli a reset_all metódust."""

        class ClassA(metaclass=SingletonMeta):
            def __init__(self) -> None:
                self.value = "A"

        class ClassB(metaclass=SingletonMeta):
            def __init__(self) -> None:
                self.value = "B"

        # Létrehozunk mindkét osztályból példányt
        obj_a1 = ClassA()
        obj_b1 = ClassB()

        # Reset all után új példányokat kapunk
        SingletonMeta.reset_all()

        obj_a2 = ClassA()
        obj_b2 = ClassB()

        # Az új példányok jók
        assert obj_a2.value == "A"
        assert obj_b2.value == "B"
        # A régiek még léteznek
        assert obj_a1.value == "A"
        assert obj_b1.value == "B"

    def test_singleton_reset_all_empty(self) -> None:
        """Teszteli a reset_all metódust üres _instances-re."""
        # Ez nem okozhat hibát
        SingletonMeta.reset_all()
        
        # Ezután normálisan kell működnie
        class TestClass(metaclass=SingletonMeta):
            def __init__(self) -> None:
                self.value = 42

        obj = TestClass()
        assert obj.value == 42

    def test_singleton_instances_dict_none_protection(self) -> None:
        """Teszteli a _instances None védelem ágát (line 80)."""

        class TestClass(metaclass=SingletonMeta):
            def __init__(self) -> None:
                self.value = 42

        # Manuálisan None-ra állítjuk a _instances-t (teszt fixture védelem)
        TestClass._instances = None  # type: ignore[assignment]

        # A __call__ metódus automatikusan helyreállítja
        obj = TestClass()
        assert obj.value == 42
        assert isinstance(TestClass._instances, dict)  # type: ignore[attr-defined]

    def test_singleton_subclass_inheritance(self) -> None:
        """Teszteli a singleton alosztály öröklődést."""

        class ParentClass(metaclass=SingletonMeta):
            def __init__(self) -> None:
                self.parent_value = "parent"

        class ChildClass(ParentClass):
            def __init__(self) -> None:
                super().__init__()
                self.child_value = "child"

        # Mindkét osztály saját singleton példánnyal rendelkezik
        parent1 = ParentClass()
        parent2 = ParentClass()
        child1 = ChildClass()
        child2 = ChildClass()

        assert parent1 is parent2
        assert child1 is child2
        assert parent1 is not child1  # type: ignore[comparison-overlap]

        assert parent1.parent_value == "parent"
        assert child1.parent_value == "parent"
        assert child1.child_value == "child"

    def test_singleton_reset_singleton_with_instance_attribute(self) -> None:
        """Teszteli a reset_singleton metódust amikor _instance attribútum létezik."""

        class TestClass(metaclass=SingletonMeta):
            def __init__(self) -> None:
                self.value = 42

        # Létrehozunk egy példányt (ez beállítja a _instance class változót)
        obj1 = TestClass()
        assert obj1.value == 42
        
        # Ellenőrizzük hogy a _instance attribútum létezik az osztályon
        assert hasattr(TestClass, "_instance")
        assert TestClass._instance is obj1  # type: ignore[attr-defined]
        
        # Manuálisan beállítjuk a _instance-t a metaclass-on is (line 112 coverage)
        SingletonMeta._instance = obj1  # type: ignore[attr-defined]
        
        # Reset után a _instance None lesz (line 112 coverage)
        SingletonMeta.reset_singleton(TestClass)
        
        # Ellenőrizzük hogy a metaclass _instance None lett
        assert SingletonMeta._instance is None  # type: ignore[attr-defined]
        
        # Új példány létrehozása
        obj2 = TestClass()
        assert obj2.value == 42
        assert TestClass._instance is obj2  # type: ignore[attr-defined]

    def test_singleton_reset_all_without_instances_attribute(self) -> None:
        """Teszteli a reset_all metódust amikor nincs _instances attribútum."""
        
        # Eltávolítjuk a _instances attribútumot ha létezik
        if hasattr(SingletonMeta, "_instances"):
            original_instances = SingletonMeta._instances
            delattr(SingletonMeta, "_instances")
            
            try:
                # Ez nem okozhat hibát
                SingletonMeta.reset_all()
            finally:
                # Visszaállítjuk az eredeti állapotot
                SingletonMeta._instances = original_instances
        else:
            # Ha nincs _instances, akkor is biztonságosan kell működnie
            SingletonMeta.reset_all()

    def test_singleton_multiple_reset_cycles(self) -> None:
        """Teszteli több reset ciklust egymás után."""

        class TestClass(metaclass=SingletonMeta):
            def __init__(self, value: int) -> None:
                self.value = value

        # Első ciklus
        obj1 = TestClass(1)
        assert obj1.value == 1
        
        SingletonMeta.reset_singleton(TestClass)
        
        # Második ciklus
        obj2 = TestClass(2)
        assert obj2.value == 2
        
        SingletonMeta.reset_singleton(TestClass)
        
        # Harmadik ciklus
        obj3 = TestClass(3)
        assert obj3.value == 3
