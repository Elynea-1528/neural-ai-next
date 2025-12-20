"""Lazy loading tesztek.

Ez a modul a `neural_ai.core.base.lazy_loading` modul teszteit tartalmazza.
"""

import threading
import time
from unittest.mock import Mock

import pytest

from neural_ai.core.base.lazy_loading import LazyLoader, lazy_property


class TestLazyLoader:
    """LazyLoader osztály teszjei."""

    def test_lazy_loader_initialization(self) -> None:
        """Teszteli a LazyLoader inicializálását."""

        def loader_func() -> str:
            return "loaded_value"

        loader = LazyLoader(loader_func)

        assert not loader.is_loaded

    def test_lazy_loader_call_loads_resource(self) -> None:
        """Teszteli, hogy a __call__ betölti az erőforrást."""

        def loader_func() -> str:
            return "loaded_value"

        loader = LazyLoader(loader_func)

        # Első hozzáférés betölti az erőforrást
        result = loader()

        assert result == "loaded_value"
        assert loader.is_loaded

    def test_lazy_loader_multiple_calls_return_same_value(self) -> None:
        """Teszteli, hogy több hívás ugyanazt az értéket adja vissza."""
        call_count = 0

        def loader_func() -> str:
            nonlocal call_count
            call_count += 1
            return f"value_{call_count}"

        loader = LazyLoader(loader_func)

        # Első hozzáférés
        result1 = loader()
        # Második hozzáférés (már gyorsítótárból jön)
        result2 = loader()

        assert result1 == result2
        assert call_count == 1  # Csak egyszer hívódik meg

    def test_lazy_loader_reset(self) -> None:
        """Teszteli a reset működését."""
        call_count = 0

        def loader_func() -> str:
            nonlocal call_count
            call_count += 1
            return f"value_{call_count}"

        loader = LazyLoader(loader_func)

        # Első betöltés
        result1 = loader()
        assert loader.is_loaded

        # Reset
        loader.reset()
        assert not loader.is_loaded

        # Újra betöltés
        result2 = loader()
        assert result1 != result2
        assert call_count == 2

    def test_lazy_loader_thread_safety(self) -> None:
        """Teszteli a szálbiztosságot."""
        call_count = 0
        results: list[int] = []

        def loader_func() -> int:
            nonlocal call_count
            time.sleep(0.01)  # Kis késleltetés a versenyhelyzet szimulálásához
            call_count += 1
            return call_count

        loader = LazyLoader(loader_func)

        def worker() -> None:
            result = loader()
            results.append(result)

        # Több szál indítása
        threads = [threading.Thread(target=worker) for _ in range(10)]

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        # Minden szál ugyanazt az értéket kapta
        assert all(r == 1 for r in results)
        assert call_count == 1  # Csak egyszer hívódik meg

    def test_lazy_loader_with_none_value_raises_assertion(self) -> None:
        """Teszteli, hogy None érték esetén AssertionError keletkezik."""

        def loader_func() -> None:
            return None

        loader = LazyLoader(loader_func)

        with pytest.raises(AssertionError, match="A betöltő függvény None értéket adott vissza"):
            loader()

    def test_lazy_loader_with_complex_object(self) -> None:
        """Teszteli a komplex objektumok betöltését."""

        def loader_func() -> dict[str, int]:
            return {"key1": 1, "key2": 2, "key3": 3}

        loader = LazyLoader(loader_func)

        result = loader()

        assert isinstance(result, dict)
        assert result["key1"] == 1
        assert result["key2"] == 2
        assert result["key3"] == 3


class TestLazyProperty:
    """lazy_property dekorátor teszjei."""

    def test_lazy_property_basic_usage(self) -> None:
        """Teszteli a lazy_property alapvető használatát."""

        class TestClass:
            def __init__(self, value: int) -> None:
                self._value = value
                self._call_count = 0

            @lazy_property
            def computed_value(self) -> int:
                self._call_count += 1
                return self._value * 2

        obj = TestClass(5)

        # A property még nincs kiszámolva
        assert not hasattr(obj, "_lazy_computed_value")

        # Első hozzáférés kiszámolja
        result1 = obj.computed_value
        assert result1 == 10
        assert hasattr(obj, "_lazy_computed_value")

        # Második hozzáférés már gyorsítótárból jön
        result2 = obj.computed_value
        assert result2 == 10

    def test_lazy_property_with_different_instances(self) -> None:
        """Teszteli, hogy különböző instance-oknak külön a gyorsítótár."""

        class TestClass:
            def __init__(self, value: int) -> None:
                self._value = value

            @lazy_property
            def computed_value(self) -> int:
                return self._value * 2

        obj1 = TestClass(5)
        obj2 = TestClass(10)

        assert obj1.computed_value == 10
        assert obj2.computed_value == 20

    def test_lazy_property_with_string(self) -> None:
        """Teszteli a lazy_property-t stringgel."""

        class TestClass:
            def __init__(self, name: str) -> None:
                self._name = name

            @lazy_property
            def greeting(self) -> str:
                return f"Hello, {self._name}!"

        obj = TestClass("World")

        assert obj.greeting == "Hello, World!"

    def test_lazy_property_with_list(self) -> None:
        """Teszteli a lazy_property-t listával."""

        class TestClass:
            def __init__(self, data: list[int]) -> None:
                self._data = data

            @lazy_property
            def processed_data(self) -> list[int]:
                return [x * 2 for x in self._data]

        obj = TestClass([1, 2, 3, 4, 5])

        result = obj.processed_data
        assert result == [2, 4, 6, 8, 10]

    def test_lazy_property_with_dict(self) -> None:
        """Teszteli a lazy_property-t dictionary-vel."""

        class TestClass:
            def __init__(self, config: dict[str, str]) -> None:
                self._config = config

            @lazy_property
            def processed_config(self) -> dict[str, str]:
                return {k.upper(): v.upper() for k, v in self._config.items()}

        obj = TestClass({"key1": "value1", "key2": "value2"})

        result = obj.processed_config
        assert result == {"KEY1": "VALUE1", "KEY2": "VALUE2"}

    def test_lazy_property_multiple_properties(self) -> None:
        """Teszteli több lazy property használatát egy osztályban."""

        class TestClass:
            def __init__(self, value: int) -> None:
                self._value = value

            @lazy_property
            def double(self) -> int:
                return self._value * 2

            @lazy_property
            def triple(self) -> int:
                return self._value * 3

            @lazy_property
            def square(self) -> int:
                return self._value * self._value

        obj = TestClass(5)

        # Minden property-t egyszer használunk
        assert obj.double == 10
        assert obj.triple == 15
        assert obj.square == 25

        # Második hozzáférés már gyorsítótárból jön
        assert obj.double == 10
        assert obj.triple == 15
        assert obj.square == 25


def test_lazy_loader_integration_with_mock() -> None:
    """Integrációs teszt mock objektummal."""
    mock_loader = Mock()
    mock_loader.return_value = "mocked_value"

    loader = LazyLoader(mock_loader)

    # Első hozzáférés
    result1 = loader()
    assert result1 == "mocked_value"
    mock_loader.assert_called_once()

    # Második hozzáférés
    result2 = loader()
    assert result2 == "mocked_value"
    mock_loader.assert_called_once()  # Még mindig csak egyszer hívódott meg
