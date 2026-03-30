"""Unit tesztek a neural_ai.core.logger.__init__ modulhoz.

Ez a teszt ellenőrzi, hogy a logger __init__.py fájl:
1. Importálható
2. Exportálja a megfelelő komponenseket (__all__)
3. Tartalmazza a verzióinformációkat
4. Tartalmazza a megfelelő docstringet
"""

import neural_ai.core.logger as logger_module


def test_logger_init_importable() -> None:
    """Teszt: A logger __init__.py importálható."""
    # Arrange & Act & Assert
    assert logger_module is not None


def test_logger_init_exports_correct_items() -> None:
    """Teszt: A logger __init__.py exportálja a megfelelő komponenseket."""
    # Arrange
    expected_exports = [
        "__version__",
        "__schema_version__",
        "LoggerInterface",
        "LoggerFactoryInterface",
        "LoggerFactory",
        "LoggerError",
        "LoggerConfigurationError",
        "LoggerInitializationError",
    ]

    # Act
    actual_exports = logger_module.__all__

    # Assert
    assert set(actual_exports) == set(
        expected_exports
    ), "A logger __init__.py exportálja az összes szükséges komponenst"


def test_logger_init_has_version() -> None:
    """Teszt: A logger __init__.py tartalmazza a verzióinformációkat."""
    # Arrange & Act
    version = getattr(logger_module, "__version__", None)
    schema_version = getattr(logger_module, "__schema_version__", None)

    # Assert
    assert version is not None, "A __version__ attribútum létezik"
    assert isinstance(version, str), "A __version__ string típusú"
    assert schema_version is not None, "A __schema_version__ attribútum létezik"
    assert isinstance(schema_version, str), "A __schema_version__ string típusú"


def test_logger_init_has_docstring() -> None:
    """Teszt: A logger __init__.py tartalmaz docstringet."""
    # Arrange & Act
    docstring = logger_module.__doc__

    # Assert
    assert docstring is not None, "Az __init__.py fájlnak tartalmaznia kell docstringet"
    assert "Logger" in docstring, "A docstring tartalmazza a 'Logger' szót"
    assert "Factory" in docstring, "A docstring tartalmazza a 'Factory' szót"


def test_logger_init_interface_accessible() -> None:
    """Teszt: A LoggerInterface elérhető a modulból."""
    # Arrange & Act
    logger_interface = getattr(logger_module, "LoggerInterface", None)

    # Assert
    assert logger_interface is not None, "A LoggerInterface elérhető"


def test_logger_init_factory_accessible() -> None:
    """Teszt: A LoggerFactory elérhető a modulból."""
    # Arrange & Act
    logger_factory = getattr(logger_module, "LoggerFactory", None)

    # Assert
    assert logger_factory is not None, "A LoggerFactory elérhető"


def test_logger_init_exceptions_accessible() -> None:
    """Teszt: A logger kivételek elérhetők a modulból."""
    # Arrange & Act
    logger_error = getattr(logger_module, "LoggerError", None)
    config_error = getattr(logger_module, "LoggerConfigurationError", None)
    init_error = getattr(logger_module, "LoggerInitializationError", None)

    # Assert
    assert logger_error is not None, "A LoggerError elérhető"
    assert config_error is not None, "A LoggerConfigurationError elérhető"
    assert init_error is not None, "A LoggerInitializationError elérhető"
