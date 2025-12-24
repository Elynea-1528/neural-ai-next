"""Tesztek a neural_ai.core.logger.interfaces.__init__ modulhoz.

Ez a modul tartalmazza a logger interfészek inicializációs moduljának
tesztjeit, amelyek ellenőrzik az exportált interfészek helyes elérhetőségét.
"""

import pytest

from neural_ai.core.logger.interfaces import (
    LoggerFactoryInterface,
    LoggerInterface,
    __version__,
)


class TestLoggerInterfacesInit:
    """Tesztosztály a logger interfaces __init__ modul ellenőrzésére."""

    def test_logger_interface_import(self) -> None:
        """Teszteli, hogy a LoggerInterface importálható-e."""
        assert LoggerInterface is not None
        assert hasattr(LoggerInterface, "__abstractmethods__")

    def test_logger_factory_interface_import(self) -> None:
        """Teszteli, hogy a LoggerFactoryInterface importálható-e."""
        assert LoggerFactoryInterface is not None
        assert hasattr(LoggerFactoryInterface, "__abstractmethods__")

    def test_all_imports_complete(self) -> None:
        """Teszteli, hogy minden exportált elem importálható-e."""
        # Ellenőrizzük, hogy az __all__ lista minden eleme elérhető-e
        import neural_ai.core.logger.interfaces as interfaces_module

        for name in interfaces_module.__all__:
            assert hasattr(interfaces_module, name), f"Hiányzó export: {name}"

    def test_logger_interface_instantiation_fails(self) -> None:
        """Teszteli, hogy az interfész nem példányosítható közvetlenül."""
        with pytest.raises(TypeError):
            LoggerInterface()  # type: ignore

    def test_logger_factory_interface_instantiation_fails(self) -> None:
        """Teszteli, hogy a factory interfész nem példányosítható közvetlenül."""
        with pytest.raises(TypeError):
            LoggerFactoryInterface()  # type: ignore

    def test_interfaces_abstract_methods_defined(self) -> None:
        """Teszteli, hogy az interfészek absztrakt metódusai definiálva vannak-e."""
        # LoggerInterface absztrakt metódusai
        assert "debug" in LoggerInterface.__abstractmethods__
        assert "info" in LoggerInterface.__abstractmethods__
        assert "warning" in LoggerInterface.__abstractmethods__
        assert "error" in LoggerInterface.__abstractmethods__
        assert "critical" in LoggerInterface.__abstractmethods__
        assert "set_level" in LoggerInterface.__abstractmethods__
        assert "get_level" in LoggerInterface.__abstractmethods__

        # LoggerFactoryInterface absztrakt metódusai
        assert "register_logger" in LoggerFactoryInterface.__abstractmethods__
        assert "get_logger" in LoggerFactoryInterface.__abstractmethods__
        assert "configure" in LoggerFactoryInterface.__abstractmethods__

    def test_version_available(self) -> None:
        """Teszteli, hogy a verziószám elérhető-e."""
        assert __version__ is not None
        assert isinstance(__version__, str)
        assert __version__ != ""

    def test_version_format(self) -> None:
        """Teszteli, hogy a verziószám helyes formátumú-e."""
        # A verziószámnak tartalmaznia kell legalább egy pontot (pl. "1.0.0")
        assert "." in __version__

    def test_version_in_all(self) -> None:
        """Teszteli, hogy a verzió benne van-e az __all__ listában."""
        import neural_ai.core.logger.interfaces as interfaces_module

        assert "__version__" in interfaces_module.__all__

    def test_version_fallback_on_package_not_found(self) -> None:
        """Teszteli a fallback verziókezelést, ha a csomag nem található."""
        from importlib.metadata import PackageNotFoundError
        from unittest.mock import patch

        import neural_ai.core.logger.interfaces as interfaces_module

        # Ideiglenesen kiváltjuk a PackageNotFoundError-t
        with patch("neural_ai.core.logger.interfaces.version") as mock_version:
            mock_version.side_effect = PackageNotFoundError("Package not found")

            # Újraimportáljuk a modult, hogy a fallback verziót használja
            import importlib

            importlib.reload(interfaces_module)

            # Ellenőrizzük, hogy a fallback verzió beállításra került-e
            assert interfaces_module.__version__ == "1.0.0"

            # Visszaállítjuk az eredeti modult
            importlib.reload(interfaces_module)
