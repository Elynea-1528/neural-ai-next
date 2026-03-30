"""Unit tesztek a neural_ai.processors.__init__ modulhoz.

Ez a teszt ellenőrzi, hogy a processors __init__.py fájl:
1. Importálható
2. Exportálja a megfelelő komponenseket (__all__)
3. Tartalmazza a megfelelő docstringet
"""

import neural_ai.processors as processors_module


def test_processors_init_importable() -> None:
    """Teszt: A processors __init__.py importálható."""
    # Arrange & Act & Assert
    assert processors_module is not None


def test_processors_init_exports_correct_items() -> None:
    """Teszt: A processors __init__.py exportálja a megfelelő komponenseket."""
    # Arrange
    expected_exports = [
        "ResamplerServiceFactory",
    ]

    # Act
    actual_exports = processors_module.__all__

    # Assert
    assert set(actual_exports) == set(
        expected_exports
    ), "A processors __init__.py exportálja az összes szükséges komponenst"


def test_processors_init_has_docstring() -> None:
    """Teszt: A processors __init__.py tartalmaz docstringet."""
    # Arrange & Act
    docstring = processors_module.__doc__

    # Assert
    assert (
        docstring is not None
    ), "Az __init__.py fájlnak tartalmaznia kell docstringet"
    assert "Processing" in docstring or "processing" in docstring


def test_processors_init_factory_accessible() -> None:
    """Teszt: A ResamplerServiceFactory elérhető a modulból."""
    # Arrange & Act
    factory = getattr(processors_module, "ResamplerServiceFactory", None)

    # Assert
    assert factory is not None, "A ResamplerServiceFactory elérhető"
