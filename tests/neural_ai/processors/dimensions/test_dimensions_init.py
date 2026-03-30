"""Unit tesztek a neural_ai.processors.dimensions.__init__ modulhoz.

Ez a teszt ellenőrzi, hogy a dimensions __init__.py fájl:
1. Importálható
2. Tartalmazza a megfelelő docstringet
"""

import neural_ai.processors.dimensions as dimensions_module


def test_dimensions_init_importable() -> None:
    """Teszt: A dimensions __init__.py importálható."""
    # Arrange & Act & Assert
    assert dimensions_module is not None


def test_dimensions_init_has_docstring() -> None:
    """Teszt: A dimensions __init__.py tartalmaz docstringet."""
    # Arrange & Act
    docstring = dimensions_module.__doc__

    # Assert
    assert (
        docstring is not None
    ), "Az __init__.py fájlnak tartalmaznia kell docstringet"
    assert "Dimenzió" in docstring or "dimension" in docstring.lower()
