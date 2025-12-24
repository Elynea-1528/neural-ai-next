"""Neural-AI-Next fő inicializációs moduljának tesztjei.

Ez a tesztmodul ellenőrzi a neural_ai.__init__.py modul megfelelő
működését, verziókezelését és típushelyességét.
"""

from typing import Final

import neural_ai


class TestVersion:
    """Verzióinformációk tesztjei."""

    def test_version_exists(self) -> None:
        """Teszteli, hogy a __version__ változó létezik-e."""
        assert hasattr(neural_ai, "__version__")

    def test_version_is_string(self) -> None:
        """Teszteli, hogy a __version__ string típusú-e."""
        assert isinstance(neural_ai.__version__, str)

    def test_version_format(self) -> None:
        """Teszteli a verziószám formátumát (semantic versioning)."""
        version_parts: list[str] = neural_ai.__version__.split(".")
        assert len(version_parts) >= 1  # Legalább egy résznek lennie kell
        # Ellenőrizzük, hogy minden rész szám-e (vagy tartalmaz számot)
        for part in version_parts:
            # Távolítsuk el a nem numerikus karaktereket
            numeric_part = "".join(filter(str.isdigit, part))
            assert numeric_part != "", f"Version part '{part}' should contain digits"

    def test_version_not_empty(self) -> None:
        """Teszteli, hogy a verziószám nem üres."""
        assert len(neural_ai.__version__) > 0

    def test_version_is_final(self) -> None:
        """Teszteli, hogy a __version__ Final típusú-e (csak típusellenőrzés)."""
        # Ez a teszt csak a típusellenőrzőt segíti, futási időben nem ellenőrizhető
        _: Final[str] = neural_ai.__version__


class TestSchemaVersion:
    """Sémaverzió tesztjei."""

    def test_schema_version_exists(self) -> None:
        """Teszteli, hogy a __schema_version__ változó létezik-e."""
        assert hasattr(neural_ai, "__schema_version__")

    def test_schema_version_is_string(self) -> None:
        """Teszteli, hogy a __schema_version__ string típusú-e."""
        assert isinstance(neural_ai.__schema_version__, str)

    def test_schema_version_format(self) -> None:
        """Teszteli a sémaverzió formátumát."""
        schema_parts: list[str] = neural_ai.__schema_version__.split(".")
        assert len(schema_parts) >= 1
        for part in schema_parts:
            numeric_part = "".join(filter(str.isdigit, part))
            assert numeric_part != "", f"Schema version part '{part}' should contain digits"

    def test_schema_version_not_empty(self) -> None:
        """Teszteli, hogy a sémaverzió nem üres."""
        assert len(neural_ai.__schema_version__) > 0

    def test_schema_version_is_final(self) -> None:
        """Teszteli, hogy a __schema_version__ Final típusú-e."""
        _: Final[str] = neural_ai.__schema_version__


class TestModuleExports:
    """Modul exportok tesztjei."""

    def test_all_export_exists(self) -> None:
        """Teszteli, hogy az __all__ változó létezik-e."""
        assert hasattr(neural_ai, "__all__")

    def test_all_is_list(self) -> None:
        """Teszteli, hogy az __all__ lista típusú-e."""
        assert isinstance(neural_ai.__all__, list)

    def test_all_contains_version(self) -> None:
        """Teszteli, hogy az __all__ tartalmazza-e a __version__-t."""
        assert "__version__" in neural_ai.__all__

    def test_all_contains_schema_version(self) -> None:
        """Teszteli, hogy az __all__ tartalmazza-e a __schema_version__-t."""
        assert "__schema_version__" in neural_ai.__all__

    def test_all_contains_only_expected_exports(self) -> None:
        """Teszteli, hogy az __all__ csak az elvárt exportokat tartalmazza."""
        expected: list[str] = ["__version__", "__schema_version__"]
        assert set(neural_ai.__all__) == set(expected)

    def test_all_is_final(self) -> None:
        """Teszteli, hogy az __all__ Final típusú-e."""
        _: Final[list[str]] = neural_ai.__all__


class TestImport:
    """Importálhatósági tesztelők."""

    def test_import_neural_ai(self) -> None:
        """Teszteli a neural_ai modul importálhatóságát."""
        import neural_ai  # noqa: F401

        assert neural_ai is not None

    def test_import_version(self) -> None:
        """Teszteli a __version__ importálhatóságát."""
        from neural_ai import __version__  # noqa: F401

        assert __version__ is not None

    def test_import_schema_version(self) -> None:
        """Teszteli a __schema_version__ importálhatóságát."""
        from neural_ai import __schema_version__  # noqa: F401

        assert __schema_version__ is not None

    def test_import_all_from_module(self) -> None:
        """Teszteli az összes export importálhatóságát."""
        # Az import * csak modul szinten engedélyezett, ezért
        # manuálisan ellenőrizzük a globális szimbólumokat
        import neural_ai

        # Ellenőrizzük, hogy az __all__-ban definiált változók elérhetők-e
        assert hasattr(neural_ai, "__version__")
        assert hasattr(neural_ai, "__schema_version__")


class TestTypeHints:
    """Típushelyességi tesztelők."""

    def test_version_type_annotation(self) -> None:
        """Teszteli, hogy a __version__-nak van-e típusannotációja."""
        # A típusannotációt a forráskódból ellenőrizzük
        import inspect

        module_source = inspect.getsource(neural_ai)
        assert "__version__: Final[str]" in module_source

    def test_schema_version_type_annotation(self) -> None:
        """Teszteli, hogy a __schema_version__-nak van-e típusannotációja."""
        import inspect

        module_source = inspect.getsource(neural_ai)
        assert "__schema_version__: Final[str]" in module_source

    def test_all_type_annotation(self) -> None:
        """Teszteli, hogy az __all__-nak van-e típusannotációja."""
        import inspect

        module_source = inspect.getsource(neural_ai)
        assert "__all__: Final[list[str]]" in module_source


class TestDocumentation:
    """Dokumentációs tesztelők."""

    def test_module_has_docstring(self) -> None:
        """Teszteli, hogy a modulnak van-e docstringje."""
        assert neural_ai.__doc__ is not None
        assert len(neural_ai.__doc__.strip()) > 0

    def test_docstring_is_hungarian(self) -> None:
        """Teszteli, hogy a docstring magyar nyelven van-e."""
        docstring = neural_ai.__doc__ or ""
        # Egyszerű ellenőrzés: tartalmaz magyar karaktereket
        hungarian_chars = ["á", "é", "í", "ó", "ö", "ő", "ú", "ü", "ű"]
        has_hungarian = any(char in docstring.lower() for char in hungarian_chars)
        assert has_hungarian, "A docstringnek magyar nyelvűnek kell lennie"


class TestCompatibility:
    """Kompatibilitási tesztelők."""

    def test_python_version_requirement(self) -> None:
        """Teszteli a Python verziókövetelményt."""
        import sys

        assert sys.version_info >= (3, 12), "A modul Python 3.12 vagy újabb verziót igényel"

    def test_importlib_metadata_available(self) -> None:
        """Teszteli, hogy az importlib.metadata elérhető-e."""
        import sys

        if sys.version_info < (3, 8):
            import importlib_metadata  # noqa: F401
        else:
            from importlib import metadata  # noqa: F401

        assert True  # Ha nem dob kivételt, akkor elérhető
