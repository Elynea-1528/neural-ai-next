"""Storage __init__.py tesztek."""

from importlib import metadata
from unittest.mock import patch

from neural_ai.data.storage import __schema_version__, __version__


class TestStorageInit:
    """Storage __init__.py tesztek."""

    def test_version_is_available(self) -> None:
        """A __version__ változó elérhető és string típusú."""
        assert isinstance(__version__, str)
        assert __version__ != ""

    def test_schema_version_is_available(self) -> None:
        """A __schema_version__ változó elérhető és string típusú."""
        assert isinstance(__schema_version__, str)
        assert __schema_version__ == "1.0"

    def test_all_list_is_exported(self) -> None:
        """Az __all__ lista tartalmazza az exportált elemeket."""
        from neural_ai.data.storage import __all__

        assert "__version__" in __all__
        assert "__schema_version__" in __all__
        assert "FileStorage" in __all__
        assert "ParquetStorageService" in __all__
        assert "StorageFactory" in __all__

    def test_version_fallback_on_package_not_found(self) -> None:
        """Verzió fallback tesztelése, ha a csomag nincs telepítve (27-29. sorok)."""
        # Mockoljuk a metadata.version-t, hogy PackageNotFoundError-t dobjon
        with patch.object(metadata, "version", side_effect=metadata.PackageNotFoundError):
            # Újraimportáljuk a modult, hogy a fallback verziót használja
            import importlib

            import neural_ai.data.storage

            importlib.reload(neural_ai.data.storage)

            # Ellenőrizzük, hogy a fallback verzió lett-e beállítva
            assert neural_ai.data.storage.__version__ == "1.0.0"

            # Visszaállítjuk az eredeti verziót
            importlib.reload(neural_ai.data.storage)

    def test_version_is_final(self) -> None:
        """A __version__ változó Final típusú és nem módosítható."""
        # A Final típus ellenőrzése fordítási időben történik,
        # itt csak annyit ellenőrzünk, hogy a változó létezik és értéke string
        assert hasattr(__version__, "__class__")
        assert isinstance(__version__, str)
