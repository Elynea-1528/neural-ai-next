"""Tesztek az util kivételekhez.

Ez a modul tartalmazza a UtilError és HardwareDetectionError osztályok
tesztelését, valamint az __init__.py exportjainak ellenőrzését.
"""


from neural_ai.core.utils.exceptions import HardwareDetectionError, UtilError
from neural_ai.core.utils.exceptions.util_error import (
    HardwareDetectionError as UtilHardwareDetectionError,
)
from neural_ai.core.utils.exceptions.util_error import (
    UtilError as UtilUtilError,
)


class TestUtilError:
    """UtilError tesztjei."""

    def test_util_error_creation(self) -> None:
        """Teszteli a UtilError létrehozását."""
        error = UtilError("Általános hiba")
        assert str(error) == "Általános hiba"
        assert error.details is None

    def test_util_error_with_details(self) -> None:
        """Teszteli a UtilError létrehozását részletekkel."""
        error = UtilError("Hiba", "Részletes leírás")
        assert str(error) == "Hiba"
        assert error.details == "Részletes leírás"

    def test_util_error_is_neural_ai_exception(self) -> None:
        """Teszteli, hogy a UtilError a NeuralAIException leszármazottja."""
        from neural_ai.core.base.exceptions import NeuralAIException
        assert issubclass(UtilError, NeuralAIException)

    def test_util_error_is_exception(self) -> None:
        """Teszteli, hogy a UtilError az Exception leszármazottja."""
        assert issubclass(UtilError, Exception)


class TestHardwareDetectionError:
    """HardwareDetectionError tesztjei."""

    def test_hardware_detection_error_creation(self) -> None:
        """Teszteli a HardwareDetectionError létrehozását."""
        error = HardwareDetectionError("Hardver hiba")
        assert str(error) == "Hardver hiba"
        assert error.hardware_type is None
        assert error.details is None

    def test_hardware_detection_error_with_type(self) -> None:
        """Teszteli a HardwareDetectionError létrehozását hardver típussal."""
        error = HardwareDetectionError("Hardver hiba", "CPU")
        assert str(error) == "Hardver hiba"
        assert error.hardware_type == "CPU"
        assert error.details is None

    def test_hardware_detection_error_inheritance(self) -> None:
        """Teszteli, hogy a HardwareDetectionError a UtilError leszármazottja."""
        assert issubclass(HardwareDetectionError, UtilError)

    def test_hardware_detection_error_is_exception(self) -> None:
        """Teszteli, hogy a HardwareDetectionError az Exception leszármazottja."""
        assert issubclass(HardwareDetectionError, Exception)


class TestInitExports:
    """__init__.py exportok tesztjei."""

    def test_init_exports_util_error(self) -> None:
        """Teszteli, hogy az __init__.py exportálja-e a UtilError-t."""
        from neural_ai.core.utils.exceptions import UtilError as InitUtilError
        assert InitUtilError is UtilUtilError

    def test_init_exports_hardware_detection_error(self) -> None:
        """Teszteli, hogy az __init__.py exportálja-e a HardwareDetectionError-t."""
        from neural_ai.core.utils.exceptions import (
            HardwareDetectionError as InitHardwareDetectionError,
        )
        assert InitHardwareDetectionError is UtilHardwareDetectionError

    def test_init_all_list(self) -> None:
        """Teszteli, hogy az __all__ lista tartalmazza-e a szükséges exportokat."""
        import neural_ai.core.utils.exceptions
        assert "UtilError" in neural_ai.core.utils.exceptions.__all__
        assert "HardwareDetectionError" in neural_ai.core.utils.exceptions.__all__
        assert len(neural_ai.core.utils.exceptions.__all__) == 2

    def test_direct_import_from_module(self) -> None:
        """Teszteli a közvetlen importot a modulból."""
        # Ez a teszt lefedi a 6-9 sorokat az __init__.py-ben
        from neural_ai.core.utils.exceptions.util_error import HardwareDetectionError, UtilError
        assert UtilError is not None
        assert HardwareDetectionError is not None
