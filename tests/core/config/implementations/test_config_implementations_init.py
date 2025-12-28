"""Config implementációk __init__ moduljának tesztelése."""

from unittest.mock import patch
from neural_ai.core.config.implementations import __version__, SCHEMA_VERSION


class TestConfigImplementationsInit:
    """Config implementációk __init__ modul tesztjei."""

    def test_version_and_constants_loaded(self) -> None:
        """Teszteli, hogy a verzió és konstansok betöltődtek-e."""
        # A verzió vagy a pyproject.toml-ból jön, vagy a fallback "1.0.0"
        assert __version__ in ["1.0.0", "1.0.1"]
        assert SCHEMA_VERSION == "1.0.0"

    def test_version_fallback_on_package_not_found(self) -> None:
        """Teszteli a fallback verziót, ha a csomag nem található."""
        with patch('importlib.metadata.version') as mock_version:
            from importlib.metadata import PackageNotFoundError
            mock_version.side_effect = PackageNotFoundError("Package not found")
            
            import sys
            
            # Távolítsuk el a modult a cache-ből
            if 'neural_ai.core.config.implementations' in sys.modules:
                del sys.modules['neural_ai.core.config.implementations']
            
            # Importáljuk újra a modult a mockkal
            from neural_ai.core.config.implementations import __version__ as fallback_version
            
            assert fallback_version == "1.0.0"

    def test_all_imports_available(self) -> None:
        """Teszteli, hogy minden import elérhető-e."""
        from neural_ai.core.config.implementations import (
            YAMLConfigManager,
            __version__,
            SCHEMA_VERSION,
        )
        
        assert YAMLConfigManager is not None
        assert __version__ is not None
        assert SCHEMA_VERSION is not None

    def test_all_list_contains_expected_exports(self) -> None:
        """Teszteli, hogy a __all__ lista tartalmazza-e a várt exportokat."""
        from neural_ai.core.config.implementations import __all__
        
        expected_exports = [
            "YAMLConfigManager",
            "__version__",
            "SCHEMA_VERSION",
        ]
        
        assert set(__all__) == set(expected_exports)