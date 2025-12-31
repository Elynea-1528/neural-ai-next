"""Tesztelés a neural_ai.__init__.py verzió fallback mechanizmusához.

Ez a modul tartalmazza a verzió lekérdezésének és a PackageNotFoundError
kezelésének tesztjeit.
"""

from unittest.mock import patch

import neural_ai


class TestVersionFallback:
    """Tesztelés a verzió fallback mechanizmusra."""

    def test_version_is_available(self) -> None:
        """Teszteli, hogy a verzió információ elérhető-e."""
        # Ellenőrizzük, hogy a verzió string formátumban van-e
        assert isinstance(neural_ai.__version__, str)
        assert len(neural_ai.__version__) > 0
        # Ellenőrizzük, hogy a verzió formátuma megfelelő (pl. "1.0.0" vagy "0.5.0")
        version_parts = neural_ai.__version__.split(".")
        assert len(version_parts) >= 2  # Legalább major.minor

    def test_schema_version_is_available(self) -> None:
        """Teszteli, hogy a séma verzió elérhető-e."""
        assert isinstance(neural_ai.__schema_version__, str)
        assert neural_ai.__schema_version__ == "1.0"

    def test_all_list_is_exported(self) -> None:
        """Teszteli, hogy az __all__ lista tartalmazza-e a szükséges exportokat."""
        assert "__version__" in neural_ai.__all__
        assert "__schema_version__" in neural_ai.__all__

    @patch("importlib.metadata.version")
    def test_version_fallback_on_package_not_found(self, mock_version) -> None:
        """Teszteli a fallback mechanizmust, ha a csomag nincs telepítve.

        Ez a teszt lefedi a PackageNotFoundError exception handler ágat.
        """
        # Mock-oljuk a PackageNotFoundError kivételt
        from importlib.metadata import PackageNotFoundError

        mock_version.side_effect = PackageNotFoundError("Package not found")

        # Újraimportáljuk a modult, hogy a mock hatásos legyen
        import sys

        # Elmentjük az eredeti modult
        original_module = sys.modules.get("neural_ai")

        try:
            # Töröljük a modult a cache-ből
            if "neural_ai" in sys.modules:
                del sys.modules["neural_ai"]

            # Újraimportáljuk a modult a mock-kal
            import neural_ai as reloaded_neural_ai

            # Ellenőrizzük, hogy a fallback verzió beállításra került-e
            assert reloaded_neural_ai.__version__ == "0.5.0"
            assert isinstance(reloaded_neural_ai.__version__, str)

        finally:
            # Visszaállítjuk az eredeti modult
            if original_module is not None:
                sys.modules["neural_ai"] = original_module

    def test_version_is_final(self) -> None:
        """Teszteli, hogy a verzió Final típusú-e."""
        # A Final annotáció futási időben nem ellenőrizhető,
        # de ellenőrizhetjük, hogy a változó nem módosítható
        from typing import Final, get_type_hints

        hints = get_type_hints(neural_ai)
        assert "__version__" in hints
        # A Final[str] ellenőrzése
        assert hasattr(hints["__version__"], "__origin__")
        assert hints["__version__"].__origin__ is Final
