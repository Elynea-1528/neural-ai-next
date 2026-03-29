"""Unit tesztek a neural_ai.core.logger.interfaces.__init__ modulhoz."""

import neural_ai.core.logger.interfaces as interfaces_module
from neural_ai.core.logger.interfaces.factory_interface import LoggerFactoryInterface
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface


class TestLoggerInterfacesInit:
    """Tesztek a logger interfaces __init__.py modulhoz."""

    def test_module_has_all(self) -> None:
        """Teszteli, hogy a modul rendelkezik __all__ attribútummal."""
        assert hasattr(interfaces_module, "__all__")
        assert isinstance(interfaces_module.__all__, list)

    def test_all_exports_logger_interface(self) -> None:
        """Teszteli, hogy az __all__ tartalmazza a LoggerInterface-t."""
        assert "LoggerInterface" in interfaces_module.__all__

    def test_all_exports_logger_factory_interface(self) -> None:
        """Teszteli, hogy az __all__ tartalmazza a LoggerFactoryInterface-t."""
        assert "LoggerFactoryInterface" in interfaces_module.__all__

    def test_all_exports_version(self) -> None:
        """Teszteli, hogy az __all__ tartalmazza a __version__-t."""
        assert "__version__" in interfaces_module.__all__

    def test_logger_interface_is_correct_class(self) -> None:
        """Teszteli, hogy a LoggerInterface a helyes osztály."""
        assert interfaces_module.LoggerInterface is LoggerInterface

    def test_logger_factory_interface_is_correct_class(self) -> None:
        """Teszteli, hogy a LoggerFactoryInterface a helyes osztály."""
        assert interfaces_module.LoggerFactoryInterface is LoggerFactoryInterface

    def test_version_exists(self) -> None:
        """Teszteli, hogy a __version__ attribútum létezik."""
        assert hasattr(interfaces_module, "__version__")
        assert isinstance(interfaces_module.__version__, str)

    def test_version_format(self) -> None:
        """Teszteli, hogy a __version__ formátuma helyes."""
        version = interfaces_module.__version__
        # Verzió formátum: X.Y.Z vagy X.Y.Z.devN
        parts = version.split(".")
        assert len(parts) >= 3
        assert parts[0].isdigit()
        assert parts[1].isdigit()

    def test_module_has_docstring(self) -> None:
        """Teszteli, hogy a modul rendelkezik docstring-gel."""
        assert interfaces_module.__doc__ is not None
        assert len(interfaces_module.__doc__) > 0

    def test_docstring_mentions_interfaces(self) -> None:
        """Teszteli, hogy a docstring említi az interfészeket."""
        assert interfaces_module.__doc__ is not None
        assert "interfész" in interfaces_module.__doc__.lower()

    def test_docstring_mentions_version(self) -> None:
        """Teszteli, hogy a docstring említi a verziót."""
        assert interfaces_module.__doc__ is not None
        assert "verzió" in interfaces_module.__doc__.lower()

    def test_no_private_exports(self) -> None:
        """Teszteli, hogy nincsenek privát exportok az __all__-ban."""
        for name in interfaces_module.__all__:
            if not name.startswith("__"):
                assert not name.startswith("_")

    def test_all_exports_exist(self) -> None:
        """Teszteli, hogy az __all__-ban felsorolt elemek léteznek."""
        for name in interfaces_module.__all__:
            assert hasattr(interfaces_module, name)

    def test_logger_interface_is_abstract(self) -> None:
        """Teszteli, hogy a LoggerInterface absztrakt osztály."""
        from abc import ABCMeta

        assert isinstance(interfaces_module.LoggerInterface, ABCMeta)

    def test_logger_factory_interface_is_abstract(self) -> None:
        """Teszteli, hogy a LoggerFactoryInterface absztrakt osztály."""
        from abc import ABCMeta

        assert isinstance(interfaces_module.LoggerFactoryInterface, ABCMeta)
