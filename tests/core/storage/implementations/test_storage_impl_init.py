"""Storage implementációk modul tesztjei."""

import importlib
import sys

import pytest

from neural_ai.core.storage.implementations import FileStorage, ParquetStorageService


class TestStorageImplementationsModuleExports:
    """Storage implementációk modul exportjainak tesztelése."""

    def test_file_storage_export(self) -> None:
        """Teszteli, hogy a FileStorage elérhető-e az importban."""
        assert hasattr(sys.modules["neural_ai.core.storage.implementations"], "FileStorage")
        from neural_ai.core.storage.implementations import FileStorage as FS

        assert FS is FileStorage

    def test_parquet_storage_service_export(self) -> None:
        """Teszteli, hogy a ParquetStorageService elérhető-e az importban."""
        module = sys.modules["neural_ai.core.storage.implementations"]
        assert hasattr(module, "ParquetStorageService")
        from neural_ai.core.storage.implementations import ParquetStorageService as PSS
        assert PSS is ParquetStorageService

    def test_all_export_list(self) -> None:
        """Teszteli, hogy az __all__ lista csak exportálandó neveket tartalmaz."""
        from neural_ai.core.storage.implementations import __all__ as module_exports

        expected_exports = {"FileStorage", "ParquetStorageService"}
        actual_exports = set(module_exports)

        assert actual_exports == expected_exports, (
            f"Várt exportok: {expected_exports}, Kapott exportok: {actual_exports}"
        )


class TestStorageImplementationsModuleTypeHints:
    """Storage implementációk modul típusannotációinak tesztelése."""

    def test_file_storage_type_annotation(self) -> None:
        """Teszteli, hogy a FileStorage rendelkezik-e helyes típusannotációkkal."""
        from neural_ai.core.storage.implementations.file_storage import FileStorage as FS

        # Ellenőrizzük, hogy az osztály rendelkezik-e type hints-ekkel
        assert hasattr(FS, "__init__")

        # Importáljuk be az osztályt és ellenőrizzük az annotációkat
        import inspect

        signature = inspect.signature(FS.__init__)
        assert "return" in signature.return_annotation or signature.return_annotation is None


class TestStorageImplementationsModuleDocstring:
    """Storage implementációk modul dokumentációjának tesztelése."""

    def test_module_has_docstring(self) -> None:
        """Teszteli, hogy a modul rendelkezik-e docstringgel."""
        module = sys.modules["neural_ai.core.storage.implementations"]
        assert module.__doc__ is not None
        assert len(module.__doc__.strip()) > 0

    def test_docstring_is_in_hungarian(self) -> None:
        """Teszteli, hogy a docstring magyar nyelven van-e."""
        module = sys.modules["neural_ai.core.storage.implementations"]
        docstring = module.__doc__

        # Egyszerű ellenőrzés magyar karakterekre
        hungarian_chars = ["á", "é", "í", "ó", "ö", "ő", "ú", "ü", "ű"]
        has_hungarian = any(char in docstring.lower() for char in hungarian_chars)
        assert has_hungarian, "A modul docstringjének magyar nyelvűnek kell lennie"


class TestStorageImplementationsModuleImportCompleteness:
    """Storage implementációk modul importjainak teljességének tesztelése."""

    def test_all_imports_successful(self) -> None:
        """Teszteli, hogy minden import sikeresen végrehajtódik-e."""
        # A teszt lényege, hogy eljut idáig a kód
        assert True

    def test_no_circular_imports(self) -> None:
        """Teszteli, hogy nincsenek-e körkörös importok."""
        try:
            # Újraimportáljuk a modult, hogy ellenőrizzük a körkörös importokat
            module_name = "neural_ai.core.storage.implementations"
            if module_name in sys.modules:
                del sys.modules[module_name]

            importlib.import_module(module_name)
            assert True
        except ImportError as e:
            pytest.fail(f"Körkörös import észlelve: {e}")


class TestStorageImplementationsModuleTypeSafety:
    """Storage implementációk modul típusbiztonságának tesztelése."""

    def test_exported_classes_have_type_hints(self) -> None:
        """Teszteli, hogy az exportált osztályok rendelkeznek-e típusannotációkkal."""
        # Ellenőrizzük az osztályok __init__ metódusának annotációit
        import inspect

        from neural_ai.core.storage.implementations import FileStorage, ParquetStorageService

        for cls in [FileStorage, ParquetStorageService]:
            if hasattr(cls, "__init__"):
                signature = inspect.signature(cls.__init__)
                # Legalább egy paraméternek legyen annotációja (az 'self' kivételével)
                params = list(signature.parameters.values())[1:]  # 'self' kihagyása
                if params:
                    assert any(p.annotation != inspect.Parameter.empty for p in params), (
                        f"{cls.__name__}.__init__ metódusának legalább egy paraméterének "
                        f"rendelkeznie kell típusannotációval"
                    )


class TestStorageImplementationsModuleDependencyInjection:
    """Storage implementációk modul függőség injektálásának tesztelése."""

    def test_classes_support_dependency_injection(self) -> None:
        """Teszteli, hogy az osztályok támogatják-e a függőség injektálást."""
        # Ellenőrizzük, hogy az osztályok __init__ metódusa elfogad-e opcionális paramétereket
        import inspect

        from neural_ai.core.storage.implementations import FileStorage, ParquetStorageService

        for cls in [FileStorage, ParquetStorageService]:
            signature = inspect.signature(cls.__init__)
            # Ellenőrizzük, hogy vannak-e opcionális paraméterek (config, logger stb.)
            params = list(signature.parameters.values())[1:]  # 'self' kihagyása
            optional_params = [p for p in params if p.default != inspect.Parameter.empty]

            # A storage osztályoknak legalább egy opcionális paraméterük kell legyen
            # (config vagy logger)
            assert len(optional_params) >= 1, (
                f"{cls.__name__} osztálynak támogatnia kell a függőség injektálást "
                f"opcionális paraméterekkel"
            )
