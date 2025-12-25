"""Tesztek a SingletonMeta osztályhoz.

Ez a modul tartalmazza a singleton metaclass tesztjeit, amelyek ellenőrzik
a singleton minta megfelelő működését.
"""

from typing import Any

from neural_ai.core.base.implementations.singleton import SingletonMeta


class TestSingletonMeta:
    """Teszt osztály a SingletonMeta funkcionalitásának ellenőrzéséhez."""

    def test_singleton_returns_same_instance(self) -> None:
        """Teszteli, hogy a singleton ugyanazt a példányt adja vissza."""

        # Given
        class TestClass(metaclass=SingletonMeta):
            def __init__(self, value: int) -> None:
                self.value = value

        # When
        instance1 = TestClass(42)
        instance2 = TestClass(100)

        # Then
        assert instance1 is instance2
        assert instance1.value == 42  # Az első példány értéke marad

    def test_singleton_with_different_classes(self) -> None:
        """Teszteli, hogy különböző osztályok különböző példányokat kapnak."""

        # Given
        class FirstClass(metaclass=SingletonMeta):
            def __init__(self, value: str) -> None:
                self.value = value

        class SecondClass(metaclass=SingletonMeta):
            def __init__(self, value: str) -> None:
                self.value = value

        # When
        first_instance = FirstClass("first")
        second_instance = SecondClass("second")

        # Then
        assert first_instance is not second_instance
        assert first_instance.value == "first"
        assert second_instance.value == "second"

    def test_singleton_with_no_args(self) -> None:
        """Teszteli a singleton működését argumentumok nélkül."""

        # Given
        class SimpleClass(metaclass=SingletonMeta):
            def __init__(self) -> None:
                self.initialized = True

        # When
        instance1 = SimpleClass()
        instance2 = SimpleClass()

        # Then
        assert instance1 is instance2
        assert instance1.initialized is True

    def test_singleton_with_kwargs(self) -> None:
        """Teszteli a singleton működését kulcsszavas argumentumokkal."""

        # Given
        class ConfigClass(metaclass=SingletonMeta):
            def __init__(self, host: str = "localhost", port: int = 8080) -> None:
                self.host = host
                self.port = port

        # When
        instance1 = ConfigClass(host="example.com", port=9000)
        instance2 = ConfigClass(host="other.com", port=8000)

        # Then
        assert instance1 is instance2
        assert instance1.host == "example.com"
        assert instance1.port == 9000

    def test_singleton_preserves_type(self) -> None:
        """Teszteli, hogy a visszaadott példány megfelelő típusú."""

        # Given
        class TypedClass(metaclass=SingletonMeta):
            def __init__(self, data: str) -> None:
                self.data = data

            def get_data(self) -> str:
                return self.data

        # When
        instance = TypedClass("test")

        # Then
        assert isinstance(instance, TypedClass)
        assert hasattr(instance, "get_data")
        assert instance.get_data() == "test"

    def test_singleton_multiple_instantiations(self) -> None:
        """Teszteli a többszöri példányosítás hatását."""

        # Given
        class CounterClass(metaclass=SingletonMeta):
            def __init__(self) -> None:
                self.count = 0

            def increment(self) -> None:
                self.count += 1

        # When
        instance1 = CounterClass()
        instance1.increment()
        instance2 = CounterClass()
        instance2.increment()
        instance3 = CounterClass()

        # Then
        assert instance1 is instance2 is instance3
        assert instance3.count == 2  # Kétszer hívtuk meg az increment-et

    def test_singleton_with_complex_args(self) -> None:
        """Teszteli a singleton működését komplex argumentumokkal."""

        # Given
        class ComplexClass(metaclass=SingletonMeta):
            def __init__(
                self, name: str, items: list[str], config: dict[str, Any], *args: Any, **kwargs: Any
            ) -> None:
                self.name = name
                self.items = items
                self.config = config
                self.args = args
                self.kwargs = kwargs

        # When
        instance1 = ComplexClass(
            "test", ["a", "b", "c"], {"key": "value"}, 1, 2, extra=True, count=5
        )
        instance2 = ComplexClass("different", ["x", "y"], {"other": "data"}, 99, extra=False)

        # Then
        assert instance1 is instance2
        assert instance2.name == "test"
        assert instance2.items == ["a", "b", "c"]
        assert instance2.config == {"key": "value"}
        assert instance2.args == (1, 2)
        assert instance2.kwargs == {"extra": True, "count": 5}

    def test_singleton_thread_safety_simulation(self) -> None:
        """Szimulálja a szálbiztonság tesztelését (alapvető ellenőrzés)."""

        # Given
        class ThreadSafeClass(metaclass=SingletonMeta):
            def __init__(self) -> None:
                self.creation_time = "now"

        # When
        instances: list[ThreadSafeClass] = []
        for _ in range(5):
            instances.append(ThreadSafeClass())

        # Then
        for instance in instances:
            assert instance is instances[0]

    def test_singleton_instances_dict(self) -> None:
        """Teszteli, hogy az _instances szótár megfelelően működik."""

        # Given
        class DictTestClass(metaclass=SingletonMeta):
            def __init__(self, value: str) -> None:
                self.value = value

        # When
        instance1 = DictTestClass("first")
        instance2 = DictTestClass("second")

        # Then
        assert DictTestClass._instances[DictTestClass] is instance1
        assert DictTestClass._instances[DictTestClass] is instance2
        # Csak egy bejegyzés ennél az osztálynál (de a szótár tartalmazhat másokat is)
        assert DictTestClass in DictTestClass._instances

    def test_singleton_clear_instances(self) -> None:
        """Teszteli, hogy az _instances szótár kiüríthető."""

        # Given
        class ClearableClass(metaclass=SingletonMeta):
            def __init__(self, value: int) -> None:
                self.value = value

        # When
        instance1 = ClearableClass(10)
        ClearableClass._instances.clear()
        instance2 = ClearableClass(20)

        # Then
        assert instance1 is not instance2
        assert instance1.value == 10
        assert instance2.value == 20
