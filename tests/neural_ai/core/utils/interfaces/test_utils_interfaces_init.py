"""Unit tesztek a neural_ai.core.utils.interfaces.__init__ modulhoz.

Ez a teszt ellenőrzi, hogy a utils interfaces __init__.py fájl:
1. Importálható
2. Exportálja a megfelelő komponenseket (__all__)
3. Tartalmazza a megfelelő docstringet
"""

import neural_ai.core.utils.interfaces as interfaces_module


def test_interfaces_init_importable() -> None:
    """Teszt: Az interfaces __init__.py importálható."""
    # Arrange & Act & Assert
    assert interfaces_module is not None


def test_interfaces_init_exports_correct_items() -> None:
    """Teszt: Az interfaces __init__.py exportálja a megfelelő komponenseket."""
    # Arrange
    expected_exports = [
        "HardwareInterface",
    ]

    # Act
    actual_exports = interfaces_module.__all__

    # Assert
    assert set(actual_exports) == set(
        expected_exports
    ), "Az interfaces __init__.py exportálja az összes szükséges komponenst"


def test_interfaces_init_has_docstring() -> None:
    """Teszt: Az interfaces __init__.py tartalmaz docstringet."""
    # Arrange & Act
    docstring = interfaces_module.__doc__

    # Assert
    assert (
        docstring is not None
    ), "Az __init__.py fájlnak tartalmaznia kell docstringet"
    assert "interfész" in docstring or "interface" in docstring.lower()


def test_interfaces_init_hardware_interface_accessible() -> None:
    """Teszt: A HardwareInterface elérhető a modulból."""
    # Arrange & Act
    hardware_interface = getattr(interfaces_module, "HardwareInterface", None)

    # Assert
    assert hardware_interface is not None, "A HardwareInterface elérhető"
