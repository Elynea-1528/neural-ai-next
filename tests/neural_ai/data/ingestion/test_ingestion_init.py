"""Unit tesztek a neural_ai.data.ingestion.__init__ modulhoz.

Ez a teszt ellenőrzi, hogy az ingestion __init__.py fájl:
1. Importálható
2. Exportálja a megfelelő komponenseket (__all__)
3. Tartalmazza a megfelelő docstringet
"""

import neural_ai.data.ingestion as ingestion_module


def test_ingestion_init_importable() -> None:
    """Teszt: Az ingestion __init__.py importálható."""
    # Arrange & Act & Assert
    assert ingestion_module is not None


def test_ingestion_init_exports_correct_items() -> None:
    """Teszt: Az ingestion __init__.py exportálja a megfelelő komponenseket."""
    # Arrange
    expected_exports = [
        "MarketDataPersister",
    ]

    # Act
    actual_exports = ingestion_module.__all__

    # Assert
    assert set(actual_exports) == set(
        expected_exports
    ), "Az ingestion __init__.py exportálja az összes szükséges komponenst"


def test_ingestion_init_has_docstring() -> None:
    """Teszt: Az ingestion __init__.py tartalmaz docstringet."""
    # Arrange & Act
    docstring = ingestion_module.__doc__

    # Assert
    assert (
        docstring is not None
    ), "Az __init__.py fájlnak tartalmaznia kell docstringet"
    assert "Ingestion" in docstring or "ingestion" in docstring


def test_ingestion_init_persister_accessible() -> None:
    """Teszt: A MarketDataPersister elérhető a modulból."""
    # Arrange & Act
    persister = getattr(ingestion_module, "MarketDataPersister", None)

    # Assert
    assert persister is not None, "A MarketDataPersister elérhető"
