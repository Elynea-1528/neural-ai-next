"""LazyLoader és lazy_property tesztek.

Ez a modul tartalmazza a LazyLoader osztály és a lazy_property dekorátor
egységtesztjeit, beleértve a lusta betöltést, resetelést és szálbiztosságot.
"""

import threading
from unittest.mock import MagicMock

from neural_ai.core.base.implementations.lazy_loader import LazyLoader, lazy_property


class TestLazyLoader:
    """LazyLoader osztály tesztjei."""

    def test_init(self) -> None:
        """Teszteli a LazyLoader inicializálását."""
        loader_func: MagicMock = MagicMock(return_value="test_value")
        loader: LazyLoader[str] = LazyLoader(loader_func)

        assert not loader.is_loaded
        # Megjegyzés: A _loader_func protected, de a tesztelés miatt ellenőrizzük
        # A valós használatban csak a __call__ metódust használjuk

    def test_call_first_time(self) -> None:
        """Teszteli a LazyLoader hívását első alkalommal."""
        mock_value: MagicMock = MagicMock()
        loader_func: MagicMock = MagicMock(return_value=mock_value)
        loader: LazyLoader[MagicMock] = LazyLoader(loader_func)

        result = loader()

        assert result is mock_value
        assert loader.is_loaded
        loader_func.assert_called_once()

    def test_call_multiple_times(self) -> None:
        """Teszteli, hogy a loader_func csak egyszer hívódik meg."""
        mock_value: MagicMock = MagicMock()
        loader_func: MagicMock = MagicMock(return_value=mock_value)
        loader: LazyLoader[MagicMock] = LazyLoader(loader_func)

        result1 = loader()
        result2 = loader()
        result3 = loader()

        assert result1 is mock_value
        assert result2 is mock_value
        assert result3 is mock_value
        assert loader.is_loaded
        loader_func.assert_called_once()

    def test_is_loaded_property(self) -> None:
        """Teszteli az is_loaded property-t."""
        loader_func: MagicMock = MagicMock(return_value="value")
        loader: LazyLoader[str] = LazyLoader(loader_func)

        assert not loader.is_loaded
        loader()
        assert loader.is_loaded

    def test_reset(self) -> None:
        """Teszteli a loader resetelését."""
        mock_value: MagicMock = MagicMock()
        loader_func: MagicMock = MagicMock(return_value=mock_value)
        loader: LazyLoader[MagicMock] = LazyLoader(loader_func)

        # Először betöltjük
        _ = loader()
        assert loader.is_loaded

        # Reseteljük
        loader.reset()
        assert not loader.is_loaded

        # Újra betöltjük
        _ = loader()
        assert loader.is_loaded
        assert loader_func.call_count == 2

    def test_thread_safety(self) -> None:
        """Teszteli a szálbiztosságot."""
        results: list[str] = []
        loader_func_calls: list[int] = []

        def loader_func() -> str:
            loader_func_calls.append(1)
            return f"value_{threading.current_thread().name}"

        loader: LazyLoader[str] = LazyLoader(loader_func)

        def access_loader() -> None:
            result = loader()
            results.append(result)

        # Több szál egyidejű hozzáférés
        threads: list[threading.Thread] = []
        for i in range(5):
            thread = threading.Thread(target=access_loader, name=f"Thread-{i}")
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        # A loader_func csak egyszer hívódjon meg
        assert len(loader_func_calls) == 1
        # Minden szál ugyanazt az értéket kapta
        assert all(r == results[0] for r in results)


class TestLazyProperty:
    """lazy_property dekorátor tesztjei."""

    def test_lazy_property_first_access(self) -> None:
        """Teszteli a lazy property első hozzáférését."""

        class TestClass:
            def __init__(self) -> None:
                self.call_count = 0

            @lazy_property
            def expensive_value(self) -> str:
                self.call_count += 1
                return f"computed_{self.call_count}"

        obj = TestClass()
        assert obj.call_count == 0

        result = obj.expensive_value
        assert result == "computed_1"
        assert obj.call_count == 1

    def test_lazy_property_multiple_access(self) -> None:
        """Teszteli, hogy a lazy property csak egyszer számolódik ki."""

        class TestClass:
            def __init__(self) -> None:
                self.call_count = 0

            @lazy_property
            def expensive_value(self) -> str:
                self.call_count += 1
                return f"computed_{self.call_count}"

        obj = TestClass()

        result1 = obj.expensive_value
        result2 = obj.expensive_value
        result3 = obj.expensive_value

        assert result1 == "computed_1"
        assert result2 == "computed_1"
        assert result3 == "computed_1"
        assert obj.call_count == 1

    def test_lazy_property_different_instances(self) -> None:
        """Teszteli, hogy különböző példányoknak külön a gyorsítótár."""

        class TestClass:
            def __init__(self, name: str) -> None:
                self.name = name
                self.call_count = 0

            @lazy_property
            def expensive_value(self) -> str:
                self.call_count += 1
                return f"{self.name}_computed_{self.call_count}"

        obj1 = TestClass("A")
        obj2 = TestClass("B")

        result1 = obj1.expensive_value
        result2 = obj2.expensive_value
        result1_again = obj1.expensive_value
        result2_again = obj2.expensive_value

        assert result1 == "A_computed_1"
        assert result2 == "B_computed_1"
        assert result1_again == "A_computed_1"
        assert result2_again == "B_computed_1"
        assert obj1.call_count == 1
        assert obj2.call_count == 1

    def test_lazy_property_with_complex_object(self) -> None:
        """Teszteli a lazy property-t komplex objektummal."""

        class TestClass:
            def __init__(self) -> None:
                self.data = [1, 2, 3]

            @lazy_property
            def processed_data(self) -> list[int]:
                return [x * 2 for x in self.data]

        obj = TestClass()

        result1 = obj.processed_data
        result2 = obj.processed_data

        assert result1 == [2, 4, 6]
        assert result2 == [2, 4, 6]
        assert result1 is result2  # Ugyanaz az objektum
