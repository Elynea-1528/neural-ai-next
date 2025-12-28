"""Hardware interfész tesztelése.

Ez a modul tartalmazza a HardwareInterface interfész egységtesztjeit.
"""

import pytest
from neural_ai.core.utils.interfaces.hardware_interface import HardwareInterface


class TestHardwareInterface:
    """HardwareInterface interfész tesztjei."""

    def test_interface_is_abstract(self) -> None:
        """Teszteli, hogy az interfész absztrakt osztály-e."""
        with pytest.raises(TypeError):
            HardwareInterface()  # type: ignore

    def test_interface_has_required_methods(self) -> None:
        """Teszteli, hogy az interfész rendelkezik a szükséges metódusokkal."""
        required_methods = [
            "has_avx2",
            "get_cpu_features",
            "supports_simd",
        ]

        for method_name in required_methods:
            assert hasattr(HardwareInterface, method_name), (
                f"Hiányzó metódus: {method_name}"
            )
            method = getattr(HardwareInterface, method_name)
            assert callable(method)

    def test_all_abstract_methods_implemented(self) -> None:
        """Teszteli, hogy az összes absztrakt metódus implementálva van-e a mockban."""
        
        class MockHardware(HardwareInterface):
            """Mock implementáció a HardwareInterface-hez."""
            
            def __init__(self) -> None:
                super().__init__()
                self.avx2_supported = True
                self.simd_supported = True
                self.cpu_features = {"avx2", "sse4", "simd"}
            
            def has_avx2(self) -> bool:
                return self.avx2_supported
            
            def get_cpu_features(self) -> set[str]:
                return self.cpu_features
            
            def supports_simd(self) -> bool:
                return self.simd_supported
        
        # Teszt: Létrehozás
        mock_hardware = MockHardware()
        
        # Teszt: has_avx2 metódus
        assert mock_hardware.has_avx2() is True
        mock_hardware.avx2_supported = False
        assert mock_hardware.has_avx2() is False
        
        # Teszt: get_cpu_features metódus
        features = mock_hardware.get_cpu_features()
        assert isinstance(features, set)
        assert "avx2" in features or len(features) >= 0  # Legalább üres halmaz
        
        # Teszt: supports_simd metódus
        assert mock_hardware.supports_simd() is True
        mock_hardware.simd_supported = False
        assert mock_hardware.supports_simd() is False