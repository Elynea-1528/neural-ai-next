"""Tesztek a neural_ai.core.storage.__init__ modulhoz.

Ez a modul tartalmazza a storage komponens fő exportjainak tesztelését,
beleértve az implementációk ellenőrzését.
"""

import sys
from importlib import import_module, metadata
from unittest import mock

import pytest

# A tesztelendő modul importálása
storage_module = import_module("neural_ai.core.storage")


class TestStorageModuleExports:
    """Teszteli a storage modul exportjait."""

    def test_file_storage_export(self) -> None:
        """Teszteli, hogy a FileStorage elérhető-e a modulból."""
        assert hasattr(storage_module, "FileStorage"), "FileStorage nem elérhető"
        from neural_ai.core.storage.implementations.file_storage import (
            FileStorage as ExpectedFileStorage,
        )

        assert storage_module.FileStorage is ExpectedFileStorage

    def test_storage_factory_export(self) -> None:
        """Teszteli, hogy a StorageFactory elérhető-e a modulból."""
        assert hasattr(storage_module, "StorageFactory"), "StorageFactory nem elérhető"
        from neural_ai.core.storage.implementations.storage_factory import (
            StorageFactory as ExpectedStorageFactory,
        )

        assert storage_module.StorageFactory is ExpectedStorageFactory

    def test_all_export_list(self) -> None:
        """Teszteli, hogy a __all__ lista tartalmazza-e a várt exportokat."""
        expected_exports = [
            # Verzióinformációk
            "__version__",
            "__schema_version__",
            # Implementációk
            "FileStorage",
            "StorageFactory",
            # Interfészek
            "StorageInterface",
            "StorageFactoryInterface",
            # Típusok
            "LoggerInterface",
            "ConfigManagerInterface",
        ]

        assert hasattr(storage_module, "__all__"), "__all__ nem létezik"
        assert isinstance(storage_module.__all__, list), "__all__ nem list típusú"

        for export in expected_exports:
            assert export in storage_module.__all__, f"{export} nincs benne a __all__ listában"

        # Ellenőrizzük, hogy nincsenek-e felesleges exportok
        assert len(storage_module.__all__) == len(expected_exports), (
            f"__all__ váratlan elemet tartalmaz: {set(storage_module.__all__) - set(expected_exports)}"
        )


class TestStorageModuleTypeHints:
    """Teszteli a modul típus hintjeit."""

    def test_file_storage_type_annotation(self) -> None:
        """Teszteli, hogy a FileStorage típus hintje helyes-e."""
        # A TYPE_CHECKING blokkban lévő típusoknak nem kell fizikailag
        # jelen lenniük futásidőben, de az importálásnak működnie kell
        if sys.version_info >= (3, 7):
            # Python 3.7+ támogatja a from __future__ import annotations-t
            # Itt csak ellenőrizzük, hogy az osztály elérhető-e
            assert hasattr(storage_module, "FileStorage")


class TestStorageModuleDocstring:
    """Teszteli a modul docstringjét."""

    def test_module_has_docstring(self) -> None:
        """Teszteli, hogy a modulnak van-e docstringje."""
        assert storage_module.__doc__ is not None, "A modulnak nincs docstringje"
        assert len(storage_module.__doc__.strip()) > 0, "A modul docstringje üres"

    def test_docstring_is_in_hungarian(self) -> None:
        """Teszteli, hogy a docstring magyar nyelven van-e."""
        docstring = storage_module.__doc__
        # Egyszerű ellenőrzés magyar karakterekre
        hungarian_chars = ["á", "é", "í", "ó", "ö", "ő", "ú", "ü", "ű"]
        has_hungarian = any(char in docstring.lower() for char in hungarian_chars)
        assert has_hungarian, "A docstring nem tartalmaz magyar karaktereket"


class TestStorageModuleImportCompleteness:
    """Teszteli a modul importjainak teljességét."""

    def test_all_imports_successful(self) -> None:
        """Teszteli, hogy minden import sikeres volt-e."""
        # Ha bármelyik import hibát okozott volna, a modul betöltése sikertelen lenne
        # Ez a teszt csak akkor fut le, ha az összes import sikeres
        assert True  # A teszt lényege, hogy eljut idáig a kód

    def test_no_circular_imports(self) -> None:
        """Teszteli, hogy nincsenek-e körkörös importok."""
        # A TYPE_CHECKING blokk használata megakadályozza a körkörös importokat
        # Ez a teszt ellenőrzi, hogy a modul betöltődött-e probléma nélkül
        assert storage_module is not None
        assert hasattr(storage_module, "FileStorage")
        assert hasattr(storage_module, "StorageFactory")


class TestStorageModuleVersion:
    """Teszteli a modul verziókezelését."""

    def test_version_export(self) -> None:
        """Teszteli, hogy a __version__ elérhető-e a modulból."""
        assert hasattr(storage_module, "__version__"), "__version__ nem elérhető"
        assert isinstance(storage_module.__version__, str), "__version__ nem string típusú"
        assert len(storage_module.__version__.strip()) > 0, "__version__ üres"

    def test_schema_version_export(self) -> None:
        """Teszteli, hogy a __schema_version__ elérhető-e a modulból."""
        assert hasattr(storage_module, "__schema_version__"), "__schema_version__ nem elérhető"
        assert isinstance(storage_module.__schema_version__, str), (
            "__schema_version__ nem string típusú"
        )
        assert storage_module.__schema_version__ == "1.0", "__schema_version__ nem megfelelő"

    def test_version_format(self) -> None:
        """Teszteli, hogy a verziószám formátuma helyes-e."""
        import re

        version_pattern = r"^\d+\.\d+\.\d+.*$"
        assert re.match(version_pattern, storage_module.__version__), (
            f"__version__ formátuma nem megfelelő: {storage_module.__version__}"
        )

    def test_version_fallback_on_package_not_found(self) -> None:
        """Teszteli a fallback verziót, ha a csomag nincs telepítve."""
        # Mock-oljuk a metadata.version-t, hogy PackageNotFoundError-t dobjon
        with mock.patch("importlib.metadata.version", side_effect=metadata.PackageNotFoundError):
            # Újra kell tölteni a modult a mock-kal
            import importlib

            import neural_ai.core.storage

            # Reload the module to trigger the exception path
            reloaded_module = importlib.reload(neural_ai.core.storage)

            # Ellenőrizzük, hogy a fallback verzió "1.0.0" lett-e
            assert reloaded_module.__version__ == "1.0.0", (
                f"Fallback verzió nem megfelelő: {reloaded_module.__version__}"
            )

            # Visszaállítjuk az eredeti modult
            importlib.reload(neural_ai.core.storage)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
