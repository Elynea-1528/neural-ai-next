"""Unit tesztek a Tensor Converter Interface-hez."""

from typing import TYPE_CHECKING

import numpy as np
import pytest

from neural_ai.processors.interfaces.tensor_converter_interface import ITensorConverter

if TYPE_CHECKING:
    pass


class ConcreteTensorConverter(ITensorConverter):
    """Teszt implementáció az ITensorConverter interfészhez."""

    def convert_to_tensor(self, data: np.ndarray) -> np.ndarray:
        """Teszt implementáció - visszaadja az eredeti tömböt."""
        return data


class TestITensorConverter:
    """Tesztek az ITensorConverter interfészhez."""

    def test_interface_is_abstract(self) -> None:
        """Ellenőrzi, hogy az interfész absztrakt osztály."""
        # Arrange & Act & Assert
        with pytest.raises(TypeError):
            ITensorConverter()  # type: ignore[abstract]

    def test_concrete_implementation_can_be_instantiated(self) -> None:
        """Ellenőrzi, hogy konkrét implementáció példányosítható."""
        # Arrange & Act
        converter = ConcreteTensorConverter()

        # Assert
        assert isinstance(converter, ITensorConverter)

    def test_convert_to_tensor_signature(self) -> None:
        """Ellenőrzi a convert_to_tensor metódus szignatúráját."""
        # Arrange
        converter = ConcreteTensorConverter()
        data = np.array([1.0, 2.0, 3.0])

        # Act
        result = converter.convert_to_tensor(data)

        # Assert
        assert isinstance(result, np.ndarray)

    def test_interface_has_all_required_methods(self) -> None:
        """Ellenőrzi, hogy az interfész tartalmazza az összes szükséges metódust."""
        # Arrange
        required_methods = ["convert_to_tensor"]

        # Act & Assert
        for method_name in required_methods:
            assert hasattr(ITensorConverter, method_name)
            assert callable(getattr(ITensorConverter, method_name))

    def test_convert_to_tensor_with_1d_array(self) -> None:
        """Ellenőrzi a convert_to_tensor metódust 1D tömbbel."""
        # Arrange
        converter = ConcreteTensorConverter()
        data = np.array([1.0, 2.0, 3.0])

        # Act
        result = converter.convert_to_tensor(data)

        # Assert
        assert isinstance(result, np.ndarray)
        assert result.shape == (3,)

    def test_convert_to_tensor_with_2d_array(self) -> None:
        """Ellenőrzi a convert_to_tensor metódust 2D tömbbel."""
        # Arrange
        converter = ConcreteTensorConverter()
        data = np.array([[1.0, 2.0], [3.0, 4.0]])

        # Act
        result = converter.convert_to_tensor(data)

        # Assert
        assert isinstance(result, np.ndarray)
        assert result.shape == (2, 2)

    def test_convert_to_tensor_with_empty_array(self) -> None:
        """Ellenőrzi a convert_to_tensor metódust üres tömbbel."""
        # Arrange
        converter = ConcreteTensorConverter()
        data = np.array([])

        # Act
        result = converter.convert_to_tensor(data)

        # Assert
        assert isinstance(result, np.ndarray)
        assert result.shape == (0,)
