"""Singleton metaclass tests."""

import unittest

from neural_ai.core.base.singleton import SingletonMeta


class TestSingletonMeta(unittest.TestCase):
    """Test cases for SingletonMeta metaclass."""

    def test_singleton_creates_only_one_instance(self):
        """Test that singleton creates only one instance."""

        # Arrange
        class TestClass(metaclass=SingletonMeta):
            def __init__(self, value: int = 0):
                self.value = value

        # Act
        instance1 = TestClass(10)
        instance2 = TestClass(20)

        # Assert
        self.assertIs(instance1, instance2)
        self.assertEqual(instance1.value, 10)
        self.assertEqual(instance2.value, 10)

    def test_singleton_with_different_classes(self):
        """Test that different classes have different instances."""

        # Arrange
        class FirstClass(metaclass=SingletonMeta):
            def __init__(self):
                self.name = "First"

        class SecondClass(metaclass=SingletonMeta):
            def __init__(self):
                self.name = "Second"

        # Act
        first1 = FirstClass()
        first2 = FirstClass()
        second1 = SecondClass()
        second2 = SecondClass()

        # Assert
        self.assertIs(first1, first2)
        self.assertIs(second1, second2)
        self.assertIsNot(first1, second1)
        self.assertEqual(first1.name, "First")
        self.assertEqual(second1.name, "Second")

    def test_singleton_with_keyword_arguments(self):
        """Test singleton with keyword arguments."""

        # Arrange
        class ConfigClass(metaclass=SingletonMeta):
            def __init__(self, host: str = "localhost", port: int = 8080):
                self.host = host
                self.port = port

        # Act
        config1 = ConfigClass(host="example.com", port=9000)
        config2 = ConfigClass(host="other.com", port=3000)

        # Assert
        self.assertIs(config1, config2)
        self.assertEqual(config1.host, "example.com")
        self.assertEqual(config2.host, "example.com")
        self.assertEqual(config1.port, 9000)

    def test_singleton_without_arguments(self):
        """Test singleton without arguments."""

        # Arrange
        class SimpleClass(metaclass=SingletonMeta):
            def __init__(self):
                self.created = True

        # Act
        instance1 = SimpleClass()
        instance2 = SimpleClass()

        # Assert
        self.assertIs(instance1, instance2)
        self.assertTrue(instance1.created)

    def test_singleton_preserves_methods(self):
        """Test that singleton preserves class methods."""

        # Arrange
        class ServiceClass(metaclass=SingletonMeta):
            def __init__(self):
                self.counter = 0

            def increment(self) -> int:
                self.counter += 1
                return self.counter

            def get_value(self) -> int:
                return self.counter

        # Act
        service1 = ServiceClass()
        service2 = ServiceClass()

        # Assert
        self.assertIs(service1, service2)
        self.assertEqual(service1.get_value(), 0)
        self.assertEqual(service1.increment(), 1)
        self.assertEqual(service2.get_value(), 1)
        self.assertEqual(service2.increment(), 2)
        self.assertEqual(service1.get_value(), 2)

    def test_singleton_with_inheritance(self):
        """Test that singleton works with inheritance."""

        # Arrange
        class BaseClass(metaclass=SingletonMeta):
            def __init__(self):
                self.base_value = "base"

        class DerivedClass(BaseClass):
            def __init__(self):
                super().__init__()
                self.derived_value = "derived"

        # Act
        base1 = BaseClass()
        base2 = BaseClass()
        derived1 = DerivedClass()
        derived2 = DerivedClass()

        # Assert
        self.assertIs(base1, base2)
        self.assertIs(derived1, derived2)
        # Base and derived should be different instances
        self.assertIsNot(base1, derived1)


if __name__ == "__main__":
    unittest.main()
