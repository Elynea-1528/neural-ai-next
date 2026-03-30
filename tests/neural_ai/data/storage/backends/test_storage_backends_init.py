"""Unit tesztek a neural_ai.data.storage.backends.__init__ modulhoz.

Ez a teszt ellenőrzi, hogy a backends __init__.py fájl:
1. Importálható
2. Exportálja a megfelelő komponenseket (__all__)
3. Tartalmazza a megfelelő docstringet
"""

import neural_ai.data.storage.backends as backends_module


def test_backends_init_importable() -> None:
    """Teszt: A backends __init__.py importálható."""
    # Arrange & Act & Assert
    assert backends_module is not None


def test_backends_init_exports_correct_items() -> None:
    """Teszt: A backends __init__.py exportálja a megfelelő komponenseket."""
    # Arrange
    expected_exports = [
        "DataFrameType",
        "StorageBackend",
        "PandasBackend",
        "PolarsBackend",
    ]

    # Act
    actual_exports = backends_module.__all__

    # Assert
    assert set(actual_exports) == set(
        expected_exports
    ), "A backends __init__.py exportálja az összes szükséges komponenst"


def test_backends_init_has_docstring() -> None:
    """Teszt: A backends __init__.py tartalmaz docstringet."""
    # Arrange & Act
    docstring = backends_module.__doc__

    # Assert
    assert (
        docstring is not None
    ), "Az __init__.py fájlnak tartalmaznia kell docstringet"
    assert "Backend" in docstring or "backend" in docstring


def test_backends_init_base_types_accessible() -> None:
    """Teszt: Az alap típusok elérhetők a modulból."""
    # Arrange & Act
    dataframe_type = getattr(backends_module, "DataFrameType", None)
    storage_backend = getattr(backends_module, "StorageBackend", None)

    # Assert
    assert dataframe_type is not None, "A DataFrameType elérhető"
    assert storage_backend is not None, "A StorageBackend elérhető"


def test_backends_init_implementations_accessible() -> None:
    """Teszt: A backend implementációk elérhetők a modulból."""
    # Arrange & Act
    pandas_backend = getattr(backends_module, "PandasBackend", None)
    polars_backend = getattr(backends_module, "PolarsBackend", None)

    # Assert
    assert pandas_backend is not None, "A PandasBackend elérhető"
    assert polars_backend is not None, "A PolarsBackend elérhető"
