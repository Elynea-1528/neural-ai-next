"""Unit tesztek a neural_ai.core.utils.__init__ modulhoz.

Ez a teszt ellenőrzi, hogy a utils __init__.py fájl:
1. Importálható
2. Exportálja a megfelelő komponenseket (__all__)
3. Tartalmazza a megfelelő docstringet
"""

import neural_ai.core.utils as utils_module


def test_utils_init_importable() -> None:
    """Teszt: A utils __init__.py importálható."""
    # Arrange & Act & Assert
    assert utils_module is not None


def test_utils_init_exports_correct_items() -> None:
    """Teszt: A utils __init__.py exportálja a megfelelő komponenseket."""
    # Arrange
    expected_exports = [
        "HardwareInterface",
        "HardwareFactory",
        "UtilError",
        "HardwareDetectionError",
    ]

    # Act
    actual_exports = utils_module.__all__

    # Assert
    assert set(actual_exports) == set(
        expected_exports
    ), "A utils __init__.py exportálja az összes szükséges komponenst"


def test_utils_init_has_docstring() -> None:
    """Teszt: A utils __init__.py tartalmaz docstringet."""
    # Arrange & Act
    docstring = utils_module.__doc__

    # Assert
    assert docstring is not None, "Az __init__.py fájlnak tartalmaznia kell docstringet"
    assert "segédfunkciók" in docstring or "utility" in docstring
    assert "DDD" in docstring, "A docstring tartalmazza a DDD szabályt"


def test_utils_init_interface_accessible() -> None:
    """Teszt: A HardwareInterface elérhető a modulból."""
    # Arrange & Act
    hardware_interface = getattr(utils_module, "HardwareInterface", None)

    # Assert
    assert hardware_interface is not None, "A HardwareInterface elérhető"


def test_utils_init_factory_accessible() -> None:
    """Teszt: A HardwareFactory elérhető a modulból."""
    # Arrange & Act
    hardware_factory = getattr(utils_module, "HardwareFactory", None)

    # Assert
    assert hardware_factory is not None, "A HardwareFactory elérhető"


def test_utils_init_exceptions_accessible() -> None:
    """Teszt: A utils kivételek elérhetők a modulból."""
    # Arrange & Act
    util_error = getattr(utils_module, "UtilError", None)
    hw_error = getattr(utils_module, "HardwareDetectionError", None)

    # Assert
    assert util_error is not None, "A UtilError elérhető"
    assert hw_error is not None, "A HardwareDetectionError elérhető"
