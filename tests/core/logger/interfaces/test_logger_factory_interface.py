"""Logger factory interfész tesztek."""
import pytest

from neural_ai.core.logger.interfaces.factory_interface import LoggerFactoryInterface


class TestLoggerFactoryInterface:
    """LoggerFactoryInterface osztály tesztei."""

    def test_interface_is_abstract(self) -> None:
        """Interfész absztrakt osztály-e."""
        with pytest.raises(TypeError):
            LoggerFactoryInterface()  # type: ignore

    def test_interface_has_required_methods(self) -> None:
        """Interfész tartalmazza a szükséges metódusokat."""
        required_methods = [
            "register_logger",
            "get_logger",
            "configure",
        ]
        for method_name in required_methods:
            assert hasattr(LoggerFactoryInterface, method_name)
            method = getattr(LoggerFactoryInterface, method_name)
            assert callable(method)
