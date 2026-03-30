"""Unit tesztek a neural_ai.processors.interfaces __init__.py fájlhoz.

Ez a teszt ellenőrzi, hogy a processors.interfaces csomag megfelelően inicializálódik.
"""


def test_processors_interfaces_init_imports() -> None:
    """Teszt: A processors.interfaces csomag importálható.

    Arrange: -
    Act: Import a processors.interfaces csomagot
    Assert: Nincs ImportError
    """
    # Act & Assert
    import neural_ai.processors.interfaces  # noqa: F401  # pyright: ignore[reportUnusedImport]


def test_processors_interfaces_init_is_package() -> None:
    """Teszt: A processors.interfaces csomag valóban csomag.

    Arrange: Import a processors.interfaces csomagot
    Act: Ellenőrizzük a __package__ attribútumot
    Assert: A __package__ nem None
    """
    # Arrange & Act
    import neural_ai.processors.interfaces as pkg

    # Assert
    assert pkg.__package__ is not None
    assert pkg.__package__ == "neural_ai.processors.interfaces"


def test_processors_interfaces_init_has_docstring() -> None:
    """Teszt: A processors.interfaces csomag rendelkezik docstring-gel.

    Arrange: Import a processors.interfaces csomagot
    Act: Ellenőrizzük a __doc__ attribútumot
    Assert: A __doc__ nem None és nem üres
    """
    # Arrange & Act
    import neural_ai.processors.interfaces as pkg

    # Assert
    assert pkg.__doc__ is not None
    assert len(pkg.__doc__.strip()) > 0
    assert "interfész" in pkg.__doc__.lower()
