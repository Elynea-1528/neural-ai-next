"""Tesztek a lazy_loading modulhoz.

Ez a modul tartalmazza a LazyLoader és lazy_property tesztjeit.
"""

from typing import Any

import pytest

from neural_ai.core.base.implementations.lazy_loader import LazyLoader, lazy_property


class TestLazyLoader:
    """LazyLoader osztály tesztjei."""

    def test_lazy_loader_initialization(self) -> None:
        """Teszteli a LazyLoader inicializálását."""

        # Given
        def loader() -> str:
            return "loaded_value"

        # When
        lazy_loader = LazyLoader(loader)

        # Then
        assert not lazy_loader.is_loaded

    def test_lazy_loader_call_loads_value(self) -> None:
        """Teszteli, hogy a __call__ metódus betölti az értéket."""

        # Given
        def loader() -> str:
            return "test_value"

        lazy_loader = LazyLoader(loader)

        # When
        result = lazy_loader()

        # Then
        assert result == "test_value"
        assert lazy_loader.is_loaded

    def test_lazy_loader_only_loads_once(self) -> None:
        """Teszteli, hogy az érték csak egyszer töltődik be."""
        # Given
        call_count = 0

        def loader() -> str:
            nonlocal call_count
            call_count += 1
            return f"value_{call_count}"

        lazy_loader = LazyLoader(loader)

        # When
        result1 = lazy_loader()
        result2 = lazy_loader()
        result3 = lazy_loader()

        # Then
        assert call_count == 1
        assert result1 == result2 == result3 == "value_1"

    def test_lazy_loader_with_complex_object(self) -> None:
        """Teszteli a LazyLoader-t komplex objektumokkal."""

        # Given
        def loader() -> dict[str, Any]:
            return {"key": "value", "number": 42}

        lazy_loader = LazyLoader(loader)

        # When
        result = lazy_loader()

        # Then
        assert result == {"key": "value", "number": 42}
        assert lazy_loader.is_loaded

    def test_lazy_loader_reset(self) -> None:
        """Teszteli a reset metódust."""
        # Given
        call_count = 0

        def loader() -> str:
            nonlocal call_count
            call_count += 1
            return f"value_{call_count}"

        lazy_loader = LazyLoader(loader)
        first_result = lazy_loader()

        # When
        lazy_loader.reset()

        # Then
        assert not lazy_loader.is_loaded

        # And when loading again
        second_result = lazy_loader()
        assert call_count == 2
        assert first_result == "value_1"
        assert second_result == "value_2"

    def test_lazy_loader_thread_safety(self) -> None:
        """Teszteli a szálbiztosságot."""
        # Given
        import threading
        import time

        call_count = 0
        results: list[str] = []

        def loader() -> str:
            nonlocal call_count
            call_count += 1
            time.sleep(0.01)  # Kis késleltetés a versenyhelyzet szimulálásához
            return f"value_{call_count}"

        lazy_loader = LazyLoader(loader)

        # When
        def load_value() -> None:
            result = lazy_loader()
            results.append(result)

        threads = [threading.Thread(target=load_value) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Then
        assert call_count == 1
        assert all(r == "value_1" for r in results)

    def test_lazy_loader_with_none_value_raises_error(self) -> None:
        """Teszteli, hogy a None érték esetén hiba keletkezik."""

        # Given
        def loader() -> None:
            return None

        lazy_loader = LazyLoader(loader)

        # When/Then
        with pytest.raises(AssertionError, match="A betöltő függvény None értéket adott vissza"):
            lazy_loader()


class TestLazyProperty:
    """lazy_property dekorátor tesztjei."""

    def test_lazy_property_initialization(self) -> None:
        """Teszteli a lazy_property inicializálását."""

        # Given
        class TestClass:
            def __init__(self) -> None:
                self.call_count = 0

            @lazy_property
            def expensive_value(self) -> str:
                self.call_count += 1
                return f"computed_{self.call_count}"

        # When
        obj = TestClass()

        # Then
        assert not hasattr(obj, "_lazy_expensive_value")
        assert obj.call_count == 0

    def test_lazy_property_computes_only_once(self) -> None:
        """Teszteli, hogy a property értéke csak egyszer számolódik ki."""

        # Given
        class TestClass:
            def __init__(self) -> None:
                self.call_count = 0

            @lazy_property
            def expensive_value(self) -> str:
                self.call_count += 1
                return f"computed_{self.call_count}"

        obj = TestClass()

        # When
        result1 = obj.expensive_value
        result2 = obj.expensive_value
        result3 = obj.expensive_value

        # Then
        assert obj.call_count == 1
        assert result1 == result2 == result3 == "computed_1"

    def test_lazy_property_with_different_instances(self) -> None:
        """Teszteli, hogy különböző instance-oknak külön a gyorsítótár."""

        # Given
        class TestClass:
            def __init__(self, name: str) -> None:
                self.name = name
                self.call_count = 0

            @lazy_property
            def expensive_value(self) -> str:
                self.call_count += 1
                return f"{self.name}_computed_{self.call_count}"

        obj1 = TestClass("obj1")
        obj2 = TestClass("obj2")

        # When
        result1 = obj1.expensive_value
        result2 = obj2.expensive_value
        result1_again = obj1.expensive_value
        result2_again = obj2.expensive_value

        # Then
        assert obj1.call_count == 1
        assert obj2.call_count == 1
        assert result1 == result1_again == "obj1_computed_1"
        assert result2 == result2_again == "obj2_computed_1"

    def test_lazy_property_with_complex_computation(self) -> None:
        """Teszteli a lazy_property-t komplex számítással."""

        # Given
        class DataProcessor:
            def __init__(self, data: list[int]) -> None:
                self.data = data
                self.computation_count = 0

            @lazy_property
            def processed_data(self) -> list[int]:
                self.computation_count += 1
                return [x * 2 for x in self.data]

        processor = DataProcessor([1, 2, 3, 4, 5])

        # When
        result1 = processor.processed_data
        result2 = processor.processed_data

        # Then
        assert processor.computation_count == 1
        assert result1 == result2 == [2, 4, 6, 8, 10]

    def test_lazy_property_attribute_name(self) -> None:
        """Teszteli, hogy a gyorsítótár attribútum neve helyes."""

        # Given
        class TestClass:
            @lazy_property
            def my_value(self) -> str:
                return "test"

        obj = TestClass()

        # When
        _ = obj.my_value

        # Then
        assert hasattr(obj, "_lazy_my_value")
        cached_value: str = obj._lazy_my_value
        assert cached_value == "test"


class TestIntegration:
    """Integrációs tesztek."""

    def test_lazy_loader_with_lazy_property(self) -> None:
        """Teszteli a LazyLoader és lazy_property együttes használatát."""

        # Given
        class DataService:
            def __init__(self) -> None:
                self.load_count = 0

            @lazy_property
            def data_loader(self) -> LazyLoader[list[int]]:
                def load_data() -> list[int]:
                    self.load_count += 1
                    return [1, 2, 3, 4, 5]

                return LazyLoader(load_data)

        service = DataService()

        # When
        data1 = service.data_loader()
        data2 = service.data_loader()

        # Then
        assert data1 == data2 == [1, 2, 3, 4, 5]
        assert service.load_count == 1
