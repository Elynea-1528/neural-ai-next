"""Tesztek a lazy_loading modulhoz.

Ez a modul tartalmazza a LazyLoader és lazy_property tesztjeit,
biztosítva a komponens megfelelő működését és a 100%-os tesztlefedettséget.
"""

import threading
import time
from typing import Any

import pytest

from neural_ai.core.base.lazy_loading import LazyLoader, lazy_property


class TestLazyLoader:
    """Tesztek a LazyLoader osztályhoz."""

    def test_basic_lazy_loading(self) -> None:
        """Teszteli az alapvető lustatöltési funkcionalitást."""
        load_count = 0

        def loader() -> str:
            nonlocal load_count
            load_count += 1
            return "loaded_value"

        lazy_loader = LazyLoader(loader)

        # Ellenőrizzük, hogy még nincs betöltve
        assert not lazy_loader.is_loaded
        assert load_count == 0

        # Első hozzáférés
        value = lazy_loader()
        assert value == "loaded_value"
        assert lazy_loader.is_loaded
        assert load_count == 1

        # További hozzáférés - már ne töltsön be újra
        value2 = lazy_loader()
        assert value2 == "loaded_value"
        assert load_count == 1  # Továbbra is 1 marad

    def test_lazy_loading_with_complex_object(self) -> None:
        """Teszteli a lustatöltést komplex objektumokkal."""
        def loader() -> dict[str, Any]:
            return {
                "config": {"host": "localhost", "port": 8080},
                "data": [1, 2, 3, 4, 5],
                "metadata": {"version": "1.0.0"}
            }

        lazy_loader = LazyLoader(loader)
        config = lazy_loader()

        assert config["config"]["host"] == "localhost"
        assert config["data"] == [1, 2, 3, 4, 5]
        assert config["metadata"]["version"] == "1.0.0"

    def test_reset_functionality(self) -> None:
        """Teszteli az újratöltési funkcionalitást."""
        load_count = 0

        def loader() -> int:
            nonlocal load_count
            load_count += 1
            return 42

        lazy_loader = LazyLoader(loader)

        # Első betöltés
        value1 = lazy_loader()
        assert value1 == 42
        assert load_count == 1

        # Reset
        lazy_loader.reset()
        assert not lazy_loader.is_loaded

        # Újra betöltés
        value2 = lazy_loader()
        assert value2 == 42
        assert load_count == 2

    def test_thread_safety(self) -> None:
        """Teszteli a szálbiztosságot."""
        load_count = 0
        results: list[int] = []

        def loader() -> int:
            nonlocal load_count
            # Szimuláljuk a lassú betöltést
            time.sleep(0.1)
            load_count += 1
            return 123

        lazy_loader = LazyLoader(loader)

        def access_loader() -> None:
            value = lazy_loader()
            results.append(value)

        # Több szál egyidejű hozzáférés
        threads = [threading.Thread(target=access_loader) for _ in range(10)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        # Ellenőrizzük, hogy csak egyszer töltődött be
        assert load_count == 1
        # Minden szál ugyanazt az értéket kapta
        assert all(result == 123 for result in results)

    def test_none_value_raises_error(self) -> None:
        """Teszteli, hogy a None érték hibát okoz."""
        def loader() -> None:
            return None

        lazy_loader = LazyLoader(loader)

        with pytest.raises(AssertionError, match="A betöltő függvény None értéket adott vissza"):
            lazy_loader()

    def test_type_hints(self) -> None:
        """Teszteli a típusbiztonságot."""
        def string_loader() -> str:
            return "test"

        def int_loader() -> int:
            return 42

        str_loader = LazyLoader(string_loader)
        int_loader_instance = LazyLoader(int_loader)

        str_value: str = str_loader()
        int_value: int = int_loader_instance()

        assert str_value == "test"
        assert int_value == 42


class TestLazyProperty:
    """Tesztek a lazy_property dekorátorhoz."""

    def test_basic_lazy_property(self) -> None:
        """Teszteli az alapvető lustatöltésű property funkcionalitást."""
        calculation_count = 0

        class TestClass:
            def __init__(self, data: list[int]) -> None:
                self._data = data

            @lazy_property
            def processed_data(self) -> list[int]:
                nonlocal calculation_count
                calculation_count += 1
                return [x * 2 for x in self._data]

        obj = TestClass([1, 2, 3])

        # Ellenőrizzük, hogy még nincs kiszámolva
        assert calculation_count == 0

        # Első hozzáférés
        result1 = obj.processed_data
        assert result1 == [2, 4, 6]
        assert calculation_count == 1

        # További hozzáférés - már ne számolja ki újra
        result2 = obj.processed_data
        assert result2 == [2, 4, 6]
        assert calculation_count == 1  # Továbbra is 1 marad

    def test_lazy_property_with_different_instances(self) -> None:
        """Teszteli, hogy különböző példányok külön gyorsítótárral rendelkeznek."""
        calculation_count = 0

        class TestClass:
            def __init__(self, data: list[int]) -> None:
                self._data = data

            @lazy_property
            def processed_data(self) -> list[int]:
                nonlocal calculation_count
                calculation_count += 1
                return [x * 2 for x in self._data]

        obj1 = TestClass([1, 2, 3])
        obj2 = TestClass([4, 5, 6])

        # Mindkét objektum számoljon
        result1 = obj1.processed_data
        result2 = obj2.processed_data

        assert result1 == [2, 4, 6]
        assert result2 == [8, 10, 12]
        assert calculation_count == 2

    def test_lazy_property_with_complex_calculation(self) -> None:
        """Teszteli a lustatöltésű property-t komplex számítással."""
        class DataProcessor:
            def __init__(self, data: list[dict[str, int]]) -> None:
                self._data = data

            @lazy_property
            def statistics(self) -> dict[str, float]:
                """Számolja ki a statisztikákat."""
                if not self._data:
                    return {"mean": 0.0, "min": 0.0, "max": 0.0}

                values = [item["value"] for item in self._data]
                return {
                    "mean": sum(values) / len(values),
                    "min": min(values),
                    "max": max(values)
                }

        processor = DataProcessor([
            {"value": 10},
            {"value": 20},
            {"value": 30}
        ])

        stats = processor.statistics
        assert stats["mean"] == 20.0
        assert stats["min"] == 10
        assert stats["max"] == 30

    def test_lazy_property_type_safety(self) -> None:
        """Teszteli a típusbiztonságot."""
        class TypedClass:
            @lazy_property
            def string_value(self) -> str:
                return "test"

            @lazy_property
            def int_value(self) -> int:
                return 42

        obj = TypedClass()
        
        str_val: str = obj.string_value
        int_val: int = obj.int_value

        assert str_val == "test"
        assert int_val == 42


class TestIntegration:
    """Integrációs tesztek."""

    def test_lazy_loader_with_lazy_property(self) -> None:
        """Teszteli a LazyLoader és lazy_property együttes használatát."""
        config_load_count = 0

        def load_config() -> dict[str, str]:
            nonlocal config_load_count
            config_load_count += 1
            return {"host": "localhost", "port": "8080"}

        class Service:
            _config_loader = LazyLoader(load_config)

            @lazy_property
            def config(self) -> dict[str, str]:
                return self._config_loader()

        service1 = Service()
        service2 = Service()

        # Mindkét szolgáltatás ugyanazt a konfigurációt használja
        config1 = service1.config
        config2 = service2.config

        assert config1 == config2 == {"host": "localhost", "port": "8080"}
        # A konfiguráció csak egyszer töltődik be
        assert config_load_count == 1

    def test_lazy_loading_performance(self) -> None:
        """Teszteli a lustatöltés teljesítménybeli előnyeit."""
        expensive_calls = 0

        def expensive_operation() -> list[int]:
            nonlocal expensive_calls
            expensive_calls += 1
            # Szimuláljuk a drága műveletet
            return list(range(1000))

        loader = LazyLoader(expensive_operation)

        # Többszöri hozzáférés
        for _ in range(100):
            _ = loader()

        # Az drága művelet csak egyszer futott le
        assert expensive_calls == 1


def test_import_star() -> None:
    """Teszteli a modul importálhatóságát import * használatával."""
    from neural_ai.core.base.lazy_loading import __all__

    assert "LazyLoader" in __all__
    assert "lazy_property" in __all__


if __name__ == "__main__":
    pytest.main([__file__, "-v"])