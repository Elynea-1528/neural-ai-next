"""Logger interfész tesztek."""
import pytest
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface


class TestLoggerInterface:
    """LoggerInterface osztály tesztei."""

    def test_interface_is_abstract(self):
        """Interfész absztrakt osztály-e."""
        with pytest.raises(TypeError):
            LoggerInterface("test")  # type: ignore

    def test_interface_has_required_methods(self):
        """Interfész tartalmazza a szükséges metódusokat."""
        required_methods = [
            "__init__",
            "debug",
            "info",
            "warning",
            "error",
            "critical",
            "set_level",
            "get_level",
        ]
        for method_name in required_methods:
            assert hasattr(LoggerInterface, method_name)
            method = getattr(LoggerInterface, method_name)
            assert callable(method)