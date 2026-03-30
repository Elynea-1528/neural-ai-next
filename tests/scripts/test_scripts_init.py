"""Unit tesztek a scripts/__init__.py fájlhoz.

Ez a teszt ellenőrzi, hogy a scripts csomag megfelelően inicializálódik.
"""


def test_scripts_init_imports() -> None:
    """Teszt: A scripts csomag importálható.

    Arrange: -
    Act: Import a scripts csomagot
    Assert: Nincs ImportError
    """
    # Act & Assert
    import scripts  # noqa: F401


def test_scripts_init_is_package() -> None:
    """Teszt: A scripts csomag valóban csomag.

    Arrange: Import a scripts csomagot
    Act: Ellenőrizzük a __package__ attribútumot
    Assert: A __package__ nem None
    """
    # Arrange & Act
    import scripts as pkg

    # Assert
    assert pkg.__package__ is not None
    assert pkg.__package__ == "scripts"


def test_scripts_init_has_docstring() -> None:
    """Teszt: A scripts csomag rendelkezik docstring-gel.

    Arrange: Import a scripts csomagot
    Act: Ellenőrizzük a __doc__ attribútumot
    Assert: A __doc__ nem None és nem üres
    """
    # Arrange & Act
    import scripts as pkg

    # Assert
    assert pkg.__doc__ is not None
    assert len(pkg.__doc__.strip()) > 0
    assert "scripts" in pkg.__doc__.lower()
