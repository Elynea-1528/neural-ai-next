"""Unit tesztek a neural_ai.data.__init__ modulhoz.

Ez a teszt ellenőrzi, hogy a data __init__.py fájl:
1. Importálható
2. Tartalmazza a megfelelő docstringet
"""

import neural_ai.data as data_module


def test_data_init_importable() -> None:
    """Teszt: A data __init__.py importálható."""
    # Arrange & Act & Assert
    assert data_module is not None


def test_data_init_has_docstring() -> None:
    """Teszt: A data __init__.py tartalmaz docstringet."""
    # Arrange & Act
    docstring = data_module.__doc__

    # Assert
    assert (
        docstring is not None
    ), "Az __init__.py fájlnak tartalmaznia kell docstringet"
    assert "Data" in docstring or "data" in docstring
