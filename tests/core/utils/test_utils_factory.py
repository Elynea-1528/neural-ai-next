"""Tesztek a HardwareFactory osztályhoz.

Ez a modul a `HardwareFactory` osztály tesztjeit tartalmazza, amelyek ellenőrzik
a hardverinformációk lekérdezéséhez szükséges factory metódusok helyes működését.
"""

from unittest.mock import MagicMock, patch

import pytest

from neural_ai.core.utils.factory import HardwareFactory
from neural_ai.core.utils.interfaces.hardware_interface import HardwareInterface


class TestHardwareFactory:
    """Tesztosztály a HardwareFactory metódusainak teszteléséhez."""

    def test_get_hardware_info_returns_hardware_info_instance(self) -> None:
        """Teszteli, hogy a get_hardware_info visszaad-e HardwareInfo példányt."""
        # Act
        hardware_info = HardwareFactory.get_hardware_info()

        # Assert
        assert hardware_info is not None
        assert hasattr(hardware_info, 'has_avx2')
        assert hasattr(hardware_info, 'get_cpu_features')
        assert hasattr(hardware_info, 'supports_simd')
        assert callable(hardware_info.has_avx2)
        assert callable(hardware_info.get_cpu_features)
        assert callable(hardware_info.supports_simd)

    def test_get_hardware_info_returns_new_instance(self) -> None:
        """Teszteli, hogy a get_hardware_info mindig új példányt ad-e vissza."""
        # Act
        hardware_info1 = HardwareFactory.get_hardware_info()
        hardware_info2 = HardwareFactory.get_hardware_info()

        # Assert
        assert hardware_info1 is not hardware_info2
        assert type(hardware_info1) is type(hardware_info2)

    def test_get_hardware_interface_returns_hardware_interface(self) -> None:
        """Teszteli, hogy a get_hardware_interface visszaad-e HardwareInterface-t."""
        # Act
        hardware_interface = HardwareFactory.get_hardware_interface()

        # Assert
        assert hardware_interface is not None
        assert isinstance(hardware_interface, HardwareInterface)
        assert hasattr(hardware_interface, 'has_avx2')
        assert hasattr(hardware_interface, 'get_cpu_features')
        assert hasattr(hardware_interface, 'supports_simd')

    def test_get_hardware_interface_returns_new_instance(self) -> None:
        """Teszteli, hogy a get_hardware_interface mindig új példányt ad-e vissza."""
        # Act
        interface1 = HardwareFactory.get_hardware_interface()
        interface2 = HardwareFactory.get_hardware_interface()

        # Assert
        assert interface1 is not interface2
        assert type(interface1) is type(interface2)

    def test_get_hardware_info_and_interface_return_different_instances(self) -> None:
        """Teszteli, hogy a factory különböző példányokat ad-e vissza."""
        # Act
        hardware_info = HardwareFactory.get_hardware_info()
        hardware_interface = HardwareFactory.get_hardware_interface()

        # Assert
        assert hardware_info is not hardware_interface
        assert type(hardware_info) is type(hardware_interface)

    def test_hardware_info_implements_hardware_interface(self) -> None:
        """Teszteli, hogy a HardwareInfo implementálja-e a HardwareInterface-t."""
        # Act
        hardware_info = HardwareFactory.get_hardware_info()

        # Assert
        assert isinstance(hardware_info, HardwareInterface)

    @patch('neural_ai.core.utils.implementations.hardware_info.HardwareInfo')
    def test_get_hardware_info_imports_correctly(self, mock_hardware_info: MagicMock) -> None:
        """Teszteli, hogy a get_hardware_info helyesen importálja-e a HardwareInfo osztályt."""
        # Arrange
        mock_instance = MagicMock()
        mock_hardware_info.return_value = mock_instance

        # Act
        result = HardwareFactory.get_hardware_info()

        # Assert
        mock_hardware_info.assert_called_once()
        assert result == mock_instance

    @patch('neural_ai.core.utils.implementations.hardware_info.HardwareInfo')
    def test_get_hardware_interface_imports_correctly(self, mock_hardware_info: MagicMock) -> None:
        """Teszteli, hogy a get_hardware_interface helyesen importálja-e a HardwareInfo osztályt."""
        # Arrange
        mock_instance = MagicMock()
        mock_hardware_info.return_value = mock_instance

        # Act
        result = HardwareFactory.get_hardware_interface()

        # Assert
        mock_hardware_info.assert_called_once()
        assert result == mock_instance

    def test_factory_methods_are_static(self) -> None:
        """Teszteli, hogy a factory metódusok statikusak-e."""
        # Assert
        assert hasattr(HardwareFactory, 'get_hardware_info')
        assert hasattr(HardwareFactory, 'get_hardware_interface')

        # Ellenőrizzük, hogy a metódusok valóban statikusak
        import inspect
        _ = HardwareFactory.get_hardware_info
        _ = HardwareFactory.get_hardware_interface

        assert isinstance(
            inspect.getattr_static(HardwareFactory, 'get_hardware_info'), staticmethod
        )
        assert isinstance(
            inspect.getattr_static(HardwareFactory, 'get_hardware_interface'), staticmethod
        )


class TestHardwareFactoryIntegration:
    """Integrációs tesztek a HardwareFactory-hez."""

    def test_factory_creates_working_hardware_info_instance(self) -> None:
        """Teszteli, hogy a factory által létrehozott példány működőképes-e."""
        # Arrange
        hardware_info = HardwareFactory.get_hardware_info()

        # Act
        has_avx2_result = hardware_info.has_avx2()
        cpu_features = hardware_info.get_cpu_features()
        supports_simd_result = hardware_info.supports_simd()

        # Assert
        assert isinstance(has_avx2_result, bool)
        assert isinstance(cpu_features, set)
        assert isinstance(supports_simd_result, bool)

    def test_factory_creates_working_hardware_interface(self) -> None:
        """Teszteli, hogy a factory által létrehozott interfész működőképes-e."""
        # Arrange
        hardware_interface = HardwareFactory.get_hardware_interface()

        # Act
        has_avx2_result = hardware_interface.has_avx2()
        cpu_features = hardware_interface.get_cpu_features()
        supports_simd_result = hardware_interface.supports_simd()

        # Assert
        assert isinstance(has_avx2_result, bool)
        assert isinstance(cpu_features, set)
        assert isinstance(supports_simd_result, bool)


if __name__ == "__main__":
    pytest.main([__file__])
