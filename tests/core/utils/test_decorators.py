"""Tesztek a neural_ai.core.utils.decorators modulhoz.

Ez a modul tartalmazza a @trace dekorátor tesztjeit, beleértve a
normál működést, hibakezelést, argumentum szerializálást és teljesítményt.
"""

import time
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from neural_ai.core.utils.decorators import trace


class TestTraceDecorator:
    """Tesztek a @trace dekorátorhoz."""

    @patch('neural_ai.core.utils.decorators._TRACE_LOGGER')
    def test_trace_successful_execution(self, mock_logger: MagicMock) -> None:
        """Teszteli a sikeres függvényhívás logolását."""
        # Arrange
        @trace
        def add(a: int, b: int) -> int:
            return a + b

        # Act
        result = add(5, 3)

        # Assert
        assert result == 8
        mock_logger.debug.assert_called_once()

        # Ellenőrizzük a log hívás paramétereit
        call_kwargs = mock_logger.debug.call_args[1]
        assert "call_id" in call_kwargs
        assert call_kwargs["function"] == "add"
        assert call_kwargs["call_args"] == ["5", "3"]
        assert "duration_ms" in call_kwargs
        assert isinstance(call_kwargs["duration_ms"], (int, float))

    @patch('neural_ai.core.utils.decorators._TRACE_LOGGER')
    def test_trace_with_kwargs(self, mock_logger: MagicMock) -> None:
        """Teszteli a kulcsszavas argumentumokkal történő hívást."""
        # Arrange
        @trace
        def multiply(a: int, b: int, factor: int = 1) -> int:
            return a * b * factor

        # Act
        result = multiply(3, 4, factor=2)

        # Assert
        assert result == 24
        mock_logger.debug.assert_called_once()

        call_kwargs = mock_logger.debug.call_args[1]
        assert call_kwargs["function"] == "multiply"
        assert call_kwargs["call_kwargs"] == {"factor": "2"}

    @patch('neural_ai.core.utils.decorators._TRACE_LOGGER')
    def test_trace_with_unsafe_args(self, mock_logger: MagicMock) -> None:
        """Teszteli a nem biztonságos argumentumok logolását."""
        # Arrange
        @trace
        def process_data(data: Any) -> str:
            return "processed"

        # Act
        result = process_data([1, 2, 3])

        # Assert
        assert result == "processed"
        call_kwargs = mock_logger.debug.call_args[1]
        assert call_kwargs["call_args"] == ["UNSAFE_ARG"]

    @patch('neural_ai.core.utils.decorators._TRACE_LOGGER')
    def test_trace_function_name_preserved(self, mock_logger: MagicMock) -> None:
        """Teszteli, hogy a függvény neve megőrződik a dekorálás után."""
        # Arrange
        @trace
        def my_custom_function() -> str:
            return "test"

        # Act
        my_custom_function()

        # Assert
        assert my_custom_function.__name__ == "my_custom_function"

    @patch('neural_ai.core.utils.decorators._TRACE_LOGGER')
    def test_trace_docstring_preserved(self, mock_logger: MagicMock) -> None:
        """Teszteli, hogy a függvény docstringje megőrződik."""
        # Arrange
        @trace
        def documented_function() -> None:
            """Ez egy dokumentált függvény."""
            pass

        # Assert
        assert documented_function.__doc__ == "Ez egy dokumentált függvény."

    @patch('neural_ai.core.utils.decorators._TRACE_LOGGER')
    def test_trace_exception_handling(self, mock_logger: MagicMock) -> None:
        """Teszteli a kivételkezelést és logolást."""
        # Arrange
        @trace
        def failing_function() -> None:
            raise ValueError("Test error")

        # Act & Assert
        with pytest.raises(ValueError, match="Test error"):
            failing_function()

        # Ellenőrizzük, hogy a hiba is logolva lett
        call_kwargs = mock_logger.debug.call_args[1]
        assert call_kwargs["function"] == "failing_function"
        assert "error" in call_kwargs
        assert "Test error" in call_kwargs["error"]

    @patch('neural_ai.core.utils.decorators._TRACE_LOGGER')
    def test_trace_call_id_uniqueness(self, mock_logger: MagicMock) -> None:
        """Teszteli, hogy minden hívás egyedi call_id-t kap."""
        # Arrange
        @trace
        def simple_function() -> None:
            pass

        # Act
        simple_function()
        simple_function()

        # Assert
        assert mock_logger.debug.call_count == 2

        # Ellenőrizzük, hogy a call_id-k különbözőek
        first_call_id = mock_logger.debug.call_args_list[0][1]["call_id"]
        second_call_id = mock_logger.debug.call_args_list[1][1]["call_id"]
        assert first_call_id != second_call_id

    @patch('neural_ai.core.utils.decorators._TRACE_LOGGER')
    def test_trace_duration_measurement(self, mock_logger: MagicMock) -> None:
        """Teszteli a futási idő mérésének helyességét."""
        # Arrange
        @trace
        def slow_function() -> None:
            time.sleep(0.1)  # 100ms késleltetés

        # Act
        slow_function()

        # Assert
        call_kwargs = mock_logger.debug.call_args[1]
        duration_ms = call_kwargs["duration_ms"]

        # A futási időnek legalább 100ms-nak kell lennie
        assert duration_ms >= 100
        assert isinstance(duration_ms, (int, float))

    @patch('neural_ai.core.utils.decorators._TRACE_LOGGER')
    def test_trace_with_mixed_args(self, mock_logger: MagicMock) -> None:
        """Teszteli a vegyes típusú argumentumok kezelését."""
        # Arrange
        @trace
        def mixed_function(safe: str, unsafe: list[int], safe_num: int) -> str:
            return "ok"

        # Act
        result = mixed_function("test", [1, 2, 3], 42)

        # Assert
        assert result == "ok"
        call_kwargs = mock_logger.debug.call_args[1]
        assert call_kwargs["call_args"] == ["test", "UNSAFE_ARG", "42"]

    @patch('neural_ai.core.utils.decorators._TRACE_LOGGER')
    def test_trace_no_args_function(self, mock_logger: MagicMock) -> None:
        """Teszteli az argumentumok nélküli függvényt."""
        # Arrange
        @trace
        def no_args_function() -> str:
            return "no args"

        # Act
        result = no_args_function()

        # Assert
        assert result == "no args"
        call_kwargs = mock_logger.debug.call_args[1]
        assert call_kwargs["call_args"] == []
        assert call_kwargs["call_kwargs"] == {}

    @patch('neural_ai.core.utils.decorators._TRACE_LOGGER')
    def test_trace_with_safe_types(self, mock_logger: MagicMock) -> None:
        """Teszteli a biztonságos típusok logolását."""
        # Arrange
        @trace
        def safe_types_function(s: str, i: int, f: float, b: bool) -> None:
            pass

        # Act
        safe_types_function("text", 42, 3.14, True)

        # Assert
        call_kwargs = mock_logger.debug.call_args[1]
        assert call_kwargs["call_args"] == ["text", "42", "3.14", "True"]


class TestTraceDecoratorIntegration:
    """Integrációs tesztek a @trace dekorátorhoz."""

    def test_trace_real_logger(self) -> None:
        """Teszteli a dekorátort valós loggerrel."""
        # Arrange
        @trace
        def integration_test_function(x: int, y: int) -> int:
            return x + y

        # Act
        result = integration_test_function(10, 20)

        # Assert
        assert result == 30
        # A valós logger hívás nem okoz hibát

    def test_trace_performance_overhead(self) -> None:
        """Teszteli a dekorátor teljesítménybeli hatását."""
        # Arrange
        @trace
        def fast_function() -> int:
            return 42

        # Act - 1000 hívás mérésére
        start_time = time.perf_counter()
        for _ in range(1000):
            fast_function()
        total_time = time.perf_counter() - start_time

        # Assert - Az átlagos hívási időnek elfogadhatónak kell lennie
        avg_time_ms = (total_time / 1000) * 1000
        assert avg_time_ms < 10  # Kevesebb mint 10ms per hívás
