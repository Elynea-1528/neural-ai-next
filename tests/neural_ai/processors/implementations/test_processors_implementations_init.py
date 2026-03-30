"""Unit tesztek a neural_ai.processors.implementations.__init__ modulhoz.

Ez a teszt ellenőrzi, hogy az implementations __init__.py fájl:
1. Importálható
2. Tartalmazza a megfelelő docstringet
"""

import neural_ai.processors.implementations as implementations_module


def test_implementations_init_importable() -> None:
    """Teszt: Az implementations __init__.py importálható."""
    # Arrange & Act & Assert
    assert implementations_module is not None


def test_implementations_init_has_docstring() -> None:
    """Teszt: Az implementations __init__.py tartalmaz docstringet."""
    # Arrange & Act
    docstring = implementations_module.__doc__

    # Assert
    assert (
        docstring is not None
    ), "Az __init__.py fájlnak tartalmaznia kell docstringet"
    assert "Processor" in docstring or "processor" in docstring.lower()
