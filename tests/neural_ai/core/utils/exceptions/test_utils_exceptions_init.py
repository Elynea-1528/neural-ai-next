"""Unit tesztek a neural_ai.core.utils.exceptions.__init__ modulhoz.

Ez a teszt ellenőrzi, hogy a utils exceptions __init__.py fájl:
1. Importálható
2. Exportálja a megfelelő komponenseket (__all__)
3. Tartalmazza a megfelelő docstringet
"""

import neural_ai.core.utils.exceptions as exceptions_module


def test_exceptions_init_importable() -> None:
    """Teszt: Az exceptions __init__.py importálható."""
    # Arrange & Act & Assert
    assert exceptions_module is not None


def test_exceptions_init_exports_correct_items() -> None:
    """Teszt: Az exceptions __init__.py exportálja a megfelelő komponenseket."""
    # Arrange
    expected_exports = [
        "UtilError",
        "HardwareDetectionError",
    ]

    # Act
    actual_exports = exceptions_module.__all__

    # Assert
    assert set(actual_exports) == set(
        expected_exports
    ), "Az exceptions __init__.py exportálja az összes szükséges komponenst"


def test_exceptions_init_has_docstring() -> None:
    """Teszt: Az exceptions __init__.py tartalmaz docstringet."""
    # Arrange & Act
    docstring = exceptions_module.__doc__

    # Assert
    assert (
        docstring is not None
    ), "Az __init__.py fájlnak tartalmaznia kell docstringet"
    assert "kivétel" in docstring or "exception" in docstring.lower()


def test_exceptions_init_util_error_accessible() -> None:
    """Teszt: A UtilError elérhető a modulból."""
    # Arrange & Act
    util_error = getattr(exceptions_module, "UtilError", None)

    # Assert
    assert util_error is not None, "A UtilError elérhető"


def test_exceptions_init_hardware_error_accessible() -> None:
    """Teszt: A HardwareDetectionError elérhető a modulból."""
    # Arrange & Act
    hw_error = getattr(exceptions_module, "HardwareDetectionError", None)

    # Assert
    assert hw_error is not None, "A HardwareDetectionError elérhető"
