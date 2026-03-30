"""Unit tesztek a neural_ai.processors.resampler_service __init__.py fájlhoz.

Ez a teszt ellenőrzi, hogy a resampler_service csomag megfelelően inicializálódik
és exportálja a publikus API-t.
"""


def test_resampler_service_init_imports() -> None:
    """Teszt: A resampler_service csomag importálható.

    Arrange: -
    Act: Import a resampler_service csomagot
    Assert: Nincs ImportError
    """
    # Act & Assert
    import neural_ai.processors.resampler_service  # noqa: F401  # pyright: ignore[reportUnusedImport]


def test_resampler_service_init_exports_interface() -> None:
    """Teszt: A resampler_service csomag exportálja a ResamplerInterface-t.

    Arrange: Import a resampler_service csomagot
    Act: Ellenőrizzük a ResamplerInterface elérhetőségét
    Assert: A ResamplerInterface elérhető a csomag szintjén
    """
    # Arrange & Act
    from neural_ai.processors.resampler_service import ResamplerInterface

    # Assert
    assert ResamplerInterface is not None
    assert hasattr(ResamplerInterface, "__abstractmethods__")


def test_resampler_service_init_exports_factory() -> None:
    """Teszt: A resampler_service csomag exportálja a ResamplerServiceFactory-t.

    Arrange: Import a resampler_service csomagot
    Act: Ellenőrizzük a ResamplerServiceFactory elérhetőségét
    Assert: A ResamplerServiceFactory elérhető a csomag szintjén
    """
    # Arrange & Act
    from neural_ai.processors.resampler_service import ResamplerServiceFactory

    # Assert
    assert ResamplerServiceFactory is not None
    assert hasattr(ResamplerServiceFactory, "create")


def test_resampler_service_init_has_all() -> None:
    """Teszt: A resampler_service csomag rendelkezik __all__ listával.

    Arrange: Import a resampler_service csomagot
    Act: Ellenőrizzük a __all__ attribútumot
    Assert: A __all__ tartalmazza a publikus API elemeket
    """
    # Arrange & Act
    import neural_ai.processors.resampler_service as pkg

    # Assert
    assert hasattr(pkg, "__all__")
    assert "ResamplerInterface" in pkg.__all__
    assert "ResamplerServiceFactory" in pkg.__all__
    assert len(pkg.__all__) == 2


def test_resampler_service_init_has_docstring() -> None:
    """Teszt: A resampler_service csomag rendelkezik docstring-gel.

    Arrange: Import a resampler_service csomagot
    Act: Ellenőrizzük a __doc__ attribútumot
    Assert: A __doc__ nem None és tartalmazza a modul leírását
    """
    # Arrange & Act
    import neural_ai.processors.resampler_service as pkg

    # Assert
    assert pkg.__doc__ is not None
    assert len(pkg.__doc__.strip()) > 0
    assert "ResamplerService" in pkg.__doc__
    assert "OHLCV" in pkg.__doc__


def test_resampler_service_init_is_package() -> None:
    """Teszt: A resampler_service csomag valóban csomag.

    Arrange: Import a resampler_service csomagot
    Act: Ellenőrizzük a __package__ attribútumot
    Assert: A __package__ nem None
    """
    # Arrange & Act
    import neural_ai.processors.resampler_service as pkg

    # Assert
    assert pkg.__package__ is not None
    assert pkg.__package__ == "neural_ai.processors.resampler_service"
