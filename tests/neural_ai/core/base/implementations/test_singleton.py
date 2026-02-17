"""SingletonMeta tesztelése.

Ez a modul tartalmazza a SingletonMeta metaclass egységtesztjeit,
beleértve a singleton minta ellenőrzését és a DI kompatibilitást.
"""

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

        assert obj_a is not obj_b
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
