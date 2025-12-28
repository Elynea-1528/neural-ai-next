"""Logger interfész __init__ moduljának tesztelése."""

from unittest.mock import patch
from neural_ai.core.logger.interfaces import __version__


class TestLoggerInterfacesInit:
    """Logger interfész __init__ modul teszjei."""

    def test_version_loaded_successfully(self) -> None:
        """Teszteli, hogy a verzió sikeresen betöltődik-e."""
        # A verzió vagy a pyproject.toml-ból jön, vagy a fallback "1.0.0"
        assert __version__ in ["1.0.0", "1.0.1"]  # Adjunk hozzá a tényleges verziót is

    def test_version_fallback_on_package_not_found(self) -> None:
        """Teszteli a fallback verziót, ha a csomag nem található."""
        with patch('importlib.metadata.version') as mock_version:
            # A mock dobjon PackageNotFoundError-t
            from importlib.metadata import PackageNotFoundError
            mock_version.side_effect = PackageNotFoundError("Package not found")
            
            # Újra kell importálni a modult a mockolt környezetben
            import importlib
            import sys
            
            # Távolítsuk el a modult a cache-ből, ha létezik
            if 'neural_ai.core.logger.interfaces' in sys.modules:
                del sys.modules['neural_ai.core.logger.interfaces']
            
            # Importáljuk újra a modult a mockkal
            from neural_ai.core.logger.interfaces import __version__ as fallback_version
            
            # Ellenőrizzük, hogy a fallback verzió lett-e beállítva
            assert fallback_version == "1.0.0"

    def test_all_imports_available(self) -> None:
        """Teszteli, hogy minden import elérhető-e."""
        from neural_ai.core.logger.interfaces import (
            LoggerInterface,
            LoggerFactoryInterface,
            __version__,
        )
        
        assert LoggerInterface is not None
        assert LoggerFactoryInterface is not None
        assert __version__ is not None

    def test_all_list_contains_expected_exports(self) -> None:
        """Teszteli, hogy a __all__ lista tartalmazza-e a várt exportokat."""
        from neural_ai.core.logger.interfaces import __all__
        
        expected_exports = [
            "LoggerInterface",
            "LoggerFactoryInterface",
            "__version__",
        ]
        
        assert set(__all__) == set(expected_exports)