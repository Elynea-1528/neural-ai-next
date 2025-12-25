"""Hardware modul tesztjei.

Ez a modul a neural_ai.core.utils.hardware modul tesztjeit tartalmazza.
"""

import platform
import tempfile
import unittest.mock
from pathlib import Path

from neural_ai.core.utils.factory import HardwareFactory
from neural_ai.core.utils.implementations.hardware_info import HardwareInfo


class TestHasAvx2:
    """has_avx2() függvény tesztjei."""

    def test_has_avx2_returns_bool(self) -> None:
        """Teszteli, hogy a függvény bool értéket ad vissza."""
        hardware_info = HardwareFactory.get_hardware_info()
        result = hardware_info.has_avx2()
        assert isinstance(result, bool)

    def test_has_avx2_non_linux_returns_false(self) -> None:
        """Teszteli, hogy nem Linux rendszereken False-t ad vissza."""
        hardware_info = HardwareFactory.get_hardware_info()
        with unittest.mock.patch("platform.system", return_value="Windows"):
            result = hardware_info.has_avx2()
            assert result is False

        with unittest.mock.patch("platform.system", return_value="Darwin"):
            result = hardware_info.has_avx2()
            assert result is False

    def test_has_avx2_with_avx2_flag(self) -> None:
        """Teszteli az AVX2 flag detektálását."""
        cpuinfo_content = """
processor   : 0
vendor_id   : GenuineIntel
cpu family  : 6
flags       : fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx pdpe1gb rdtscp lm constant_tsc art arch_perfmon pebs bts rep_good nopl xtopology nonstop_tsc cpuid aperfmperf pni pclmulqdq dtes64 monitor ds_cpl vmx est tm2 ssse3 sdbg fma cx16 xtpr pdcm pcid sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand lahf_lm abm 3dnowprefetch cpuid_fault epb invpcid_single pti ssbd ibrs ibpb stibp tpr_shadow vnmi flexpriority ept vpid ept_ad fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid mpx rdseed adx smap clflushopt intel_pt xsaveopt xsavec xgetbv1 xsaves dtherm ida arat pln pts hwp hwp_notify hwp_act_window hwp_epp
"""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".cpuinfo") as f:
            f.write(cpuinfo_content)
            temp_path = f.name

        try:
            hardware_info = HardwareFactory.get_hardware_info()
            with (
                unittest.mock.patch("platform.system", return_value="Linux"),
                unittest.mock.patch(
                    "neural_ai.core.utils.implementations.hardware_info.os.path.exists", return_value=True
                ),
                unittest.mock.patch(
                    "builtins.open", unittest.mock.mock_open(read_data=cpuinfo_content)
                ),
            ):
                result = hardware_info.has_avx2()
                assert result is True
        finally:
            Path(temp_path).unlink(missing_ok=True)

    def test_has_avx2_without_avx2_flag(self) -> None:
        """Teszteli a helyes viselkedést, ha nincs AVX2 flag."""
        cpuinfo_content = """
processor   : 0
vendor_id   : GenuineIntel
cpu family  : 6
flags       : fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx
"""
        hardware_info = HardwareFactory.get_hardware_info()
        with (
            unittest.mock.patch("platform.system", return_value="Linux"),
            unittest.mock.patch("neural_ai.core.utils.implementations.hardware_info.os.path.exists", return_value=True),
            unittest.mock.patch(
                "builtins.open", unittest.mock.mock_open(read_data=cpuinfo_content)
            ),
        ):
            result = hardware_info.has_avx2()
            assert result is False

    def test_has_avx2_file_not_found(self) -> None:
        """Teszteli a viselkedést, ha a /proc/cpuinfo fájl nem létezik."""
        hardware_info = HardwareFactory.get_hardware_info()
        with (
            unittest.mock.patch("platform.system", return_value="Linux"),
            unittest.mock.patch("neural_ai.core.utils.implementations.hardware_info.os.path.exists", return_value=False),
        ):
            result = hardware_info.has_avx2()
            assert result is False

    def test_has_avx2_io_error(self) -> None:
        """Teszteli a viselkedést IOError esetén."""
        hardware_info = HardwareFactory.get_hardware_info()
        with (
            unittest.mock.patch("platform.system", return_value="Linux"),
            unittest.mock.patch("neural_ai.core.utils.implementations.hardware_info.os.path.exists", return_value=True),
            unittest.mock.patch("builtins.open", side_effect=OSError("Permission denied")),
        ):
            result = hardware_info.has_avx2()
            assert result is False

    def test_has_avx2_permission_error(self) -> None:
        """Teszteli a viselkedést PermissionError esetén."""
        hardware_info = HardwareFactory.get_hardware_info()
        with (
            unittest.mock.patch("platform.system", return_value="Linux"),
            unittest.mock.patch("neural_ai.core.utils.implementations.hardware_info.os.path.exists", return_value=True),
            unittest.mock.patch("builtins.open", side_effect=PermissionError("Permission denied")),
        ):
            result = hardware_info.has_avx2()
            assert result is False

    def test_has_avx2_malformed_cpuinfo(self) -> None:
        """Teszteli a viselkedést hibás cpuinfo formátum esetén."""
        cpuinfo_content = """
processor   : 0
vendor_id   : GenuineIntel
malformed line without colon
"""
        hardware_info = HardwareFactory.get_hardware_info()
        with (
            unittest.mock.patch("platform.system", return_value="Linux"),
            unittest.mock.patch("neural_ai.core.utils.implementations.hardware_info.os.path.exists", return_value=True),
            unittest.mock.patch(
                "builtins.open", unittest.mock.mock_open(read_data=cpuinfo_content)
            ),
        ):
            result = hardware_info.has_avx2()
            assert result is False

    def test_has_avx2_no_flags_line(self) -> None:
        """Teszteli a viselkedést, ha nincs flags sor."""
        cpuinfo_content = """
processor   : 0
vendor_id   : GenuineIntel
cpu family  : 6
"""
        hardware_info = HardwareFactory.get_hardware_info()
        with (
            unittest.mock.patch("platform.system", return_value="Linux"),
            unittest.mock.patch("neural_ai.core.utils.implementations.hardware_info.os.path.exists", return_value=True),
            unittest.mock.patch(
                "builtins.open", unittest.mock.mock_open(read_data=cpuinfo_content)
            ),
        ):
            result = hardware_info.has_avx2()
            assert result is False


class TestGetCpuFeatures:
    """get_cpu_features() függvény tesztjei."""

    def test_get_cpu_features_returns_set(self) -> None:
        """Teszteli, hogy a függvény set-et ad vissza."""
        hardware_info = HardwareFactory.get_hardware_info()
        result = hardware_info.get_cpu_features()
        assert isinstance(result, set)

    def test_get_cpu_features_non_linux_returns_empty(self) -> None:
        """Teszteli, hogy nem Linux rendszereken üres halmazt ad vissza."""
        hardware_info = HardwareFactory.get_hardware_info()
        with unittest.mock.patch("platform.system", return_value="Windows"):
            result = hardware_info.get_cpu_features()
            assert result == set()

    def test_get_cpu_features_with_flags(self) -> None:
        """Teszteli a flag-ek helyes kinyerését."""
        cpuinfo_content = """
processor   : 0
flags       : fpu vme de pse tsc msr pae mce cx8 apic sep
"""
        expected = {"fpu", "vme", "de", "pse", "tsc", "msr", "pae", "mce", "cx8", "apic", "sep"}
        hardware_info = HardwareFactory.get_hardware_info()

        with (
            unittest.mock.patch("platform.system", return_value="Linux"),
            unittest.mock.patch("neural_ai.core.utils.implementations.hardware_info.os.path.exists", return_value=True),
            unittest.mock.patch(
                "builtins.open", unittest.mock.mock_open(read_data=cpuinfo_content)
            ),
        ):
            result = hardware_info.get_cpu_features()
            assert result == expected

    def test_get_cpu_features_file_not_found(self) -> None:
        """Teszteli a viselkedést, ha a /proc/cpuinfo fájl nem létezik."""
        hardware_info = HardwareFactory.get_hardware_info()
        with (
            unittest.mock.patch("platform.system", return_value="Linux"),
            unittest.mock.patch("neural_ai.core.utils.implementations.hardware_info.os.path.exists", return_value=False),
        ):
            result = hardware_info.get_cpu_features()
            assert result == set()

    def test_get_cpu_features_io_error(self) -> None:
        """Teszteli a viselkedést IOError esetén."""
        hardware_info = HardwareFactory.get_hardware_info()
        with (
            unittest.mock.patch("platform.system", return_value="Linux"),
            unittest.mock.patch("neural_ai.core.utils.implementations.hardware_info.os.path.exists", return_value=True),
            unittest.mock.patch("builtins.open", side_effect=OSError("Permission denied")),
        ):
            result = hardware_info.get_cpu_features()
            assert result == set()

    def test_get_cpu_features_no_flags_line(self) -> None:
        """Teszteli a viselkedést, ha nincs flags sor."""
        cpuinfo_content = """
processor   : 0
vendor_id   : GenuineIntel
"""
        hardware_info = HardwareFactory.get_hardware_info()
        with (
            unittest.mock.patch("platform.system", return_value="Linux"),
            unittest.mock.patch("neural_ai.core.utils.implementations.hardware_info.os.path.exists", return_value=True),
            unittest.mock.patch(
                "builtins.open", unittest.mock.mock_open(read_data=cpuinfo_content)
            ),
        ):
            result = hardware_info.get_cpu_features()
            assert result == set()


class TestSupportsSimd:
    """supports_simd() függvény tesztjei."""

    def test_supports_simd_returns_bool(self) -> None:
        """Teszteli, hogy a függvény bool értéket ad vissza."""
        hardware_info = HardwareFactory.get_hardware_info()
        result = hardware_info.supports_simd()
        assert isinstance(result, bool)

    def test_supports_simd_with_all_simd_flags(self) -> None:
        """Teszteli, hogy True-t ad vissza, ha minden SIMD flag megtalálható."""
        cpuinfo_content = """
processor   : 0
flags       : sse sse2 sse3 ssse3 sse4_1 sse4_2 avx
"""
        hardware_info = HardwareFactory.get_hardware_info()
        with (
            unittest.mock.patch("platform.system", return_value="Linux"),
            unittest.mock.patch("neural_ai.core.utils.implementations.hardware_info.os.path.exists", return_value=True),
            unittest.mock.patch(
                "builtins.open", unittest.mock.mock_open(read_data=cpuinfo_content)
            ),
        ):
            result = hardware_info.supports_simd()
            assert result is True

    def test_supports_simd_with_some_simd_flags(self) -> None:
        """Teszteli, hogy True-t ad vissza, ha néhány SIMD flag megtalálható."""
        cpuinfo_content = """
processor   : 0
flags       : sse sse2 avx
"""
        hardware_info = HardwareFactory.get_hardware_info()
        with (
            unittest.mock.patch("platform.system", return_value="Linux"),
            unittest.mock.patch("neural_ai.core.utils.implementations.hardware_info.os.path.exists", return_value=True),
            unittest.mock.patch(
                "builtins.open", unittest.mock.mock_open(read_data=cpuinfo_content)
            ),
        ):
            result = hardware_info.supports_simd()
            assert result is True

    def test_supports_simd_without_simd_flags(self) -> None:
        """Teszteli, hogy False-t ad vissza, ha nincs SIMD flag."""
        cpuinfo_content = """
processor   : 0
flags       : fpu vme de pse tsc msr
"""
        hardware_info = HardwareFactory.get_hardware_info()
        with (
            unittest.mock.patch("platform.system", return_value="Linux"),
            unittest.mock.patch("neural_ai.core.utils.implementations.hardware_info.os.path.exists", return_value=True),
            unittest.mock.patch(
                "builtins.open", unittest.mock.mock_open(read_data=cpuinfo_content)
            ),
        ):
            result = hardware_info.supports_simd()
            assert result is False

    def test_supports_simd_non_linux_returns_false(self) -> None:
        """Teszteli, hogy nem Linux rendszereken False-t ad vissza."""
        hardware_info = HardwareFactory.get_hardware_info()
        with unittest.mock.patch("platform.system", return_value="Windows"):
            result = hardware_info.supports_simd()
            assert result is False


class TestIntegration:
    """Integrációs tesztek a hardware modulhoz."""

    def test_all_functions_work_together(self) -> None:
        """Teszteli, hogy az összes függvény együttműködik."""
        # Csak ellenőrizzük, hogy minden függvény hívható anélkül, hogy kivételt dobna
        hardware_info = HardwareFactory.get_hardware_info()
        hardware_info.has_avx2()
        hardware_info.get_cpu_features()
        hardware_info.supports_simd()

    def test_actual_system_compatibility(self) -> None:
        """Teszteli a függvényeket a tényleges rendszeren."""
        # Ez a teszt a tényleges rendszeren fut, és ellenőrzi a valós viselkedést
        hardware_info = HardwareFactory.get_hardware_info()
        if platform.system() == "Linux":
            # Linux rendszeren ellenőrizzük, hogy a függvények értelmes értékeket adnak vissza
            features = hardware_info.get_cpu_features()
            assert isinstance(features, set)

            avx2_result = hardware_info.has_avx2()
            assert isinstance(avx2_result, bool)

            simd_result = hardware_info.supports_simd()
            assert isinstance(simd_result, bool)
        else:
            # Nem Linux rendszeren ellenőrizzük a helyes viselkedést
            features = hardware_info.get_cpu_features()
            assert features == set()

            avx2_result = hardware_info.has_avx2()
            assert avx2_result is False

            simd_result = hardware_info.supports_simd()
            assert simd_result is False


class TestHardwareInfoExceptionHandling:
    """HardwareInfo kivételkezelés tesztjei."""

    def test_cpuinfo_missing_exception_handling(self) -> None:
        """Teszteli a /proc/cpuinfo hiányának kivételkezelését."""
        hardware_info = HardwareInfo()

        # Szimuláljuk, hogy a /proc/cpuinfo fájl nem létezik
        with unittest.mock.patch("platform.system", return_value="Linux"):
            with unittest.mock.patch("neural_ai.core.utils.implementations.hardware_info.os.path.exists", return_value=False):
                # A függvényeknek nem szabad kivételt dobniuk, hanem biztonságos értéket kell visszaadniuk
                result_avx2 = hardware_info.has_avx2()
                result_features = hardware_info.get_cpu_features()
                result_simd = hardware_info.supports_simd()

                assert result_avx2 is False
                assert result_features == set()
                assert result_simd is False

    def test_cpuinfo_read_permission_error(self) -> None:
        """Teszteli a /proc/cpuinfo olvasási jogosultság hiányát."""
        hardware_info = HardwareInfo()

        with unittest.mock.patch("platform.system", return_value="Linux"):
            with unittest.mock.patch("neural_ai.core.utils.implementations.hardware_info.os.path.exists", return_value=True):
                with unittest.mock.patch("builtins.open", side_effect=PermissionError("Access denied")):
                    # A függvényeknek nem szabad kivételt dobniuk
                    result_avx2 = hardware_info.has_avx2()
                    result_features = hardware_info.get_cpu_features()
                    result_simd = hardware_info.supports_simd()

                    assert result_avx2 is False
                    assert result_features == set()
                    assert result_simd is False

    def test_cpuinfo_file_io_error(self) -> None:
        """Teszteli az IOError kezelését /proc/cpuinfo olvasásakor."""
        hardware_info = HardwareInfo()

        with unittest.mock.patch("platform.system", return_value="Linux"):
            with unittest.mock.patch("neural_ai.core.utils.implementations.hardware_info.os.path.exists", return_value=True):
                with unittest.mock.patch("builtins.open", side_effect=OSError("IO Error")):
                    # A függvényeknek nem szabad kivételt dobniuk
                    result_avx2 = hardware_info.has_avx2()
                    result_features = hardware_info.get_cpu_features()
                    result_simd = hardware_info.supports_simd()

                    assert result_avx2 is False
                    assert result_features == set()
                    assert result_simd is False

    def test_cpuinfo_empty_file(self) -> None:
        """Teszteli az üres /proc/cpuinfo fájl kezelését."""
        hardware_info = HardwareInfo()

        with unittest.mock.patch("platform.system", return_value="Linux"):
            with unittest.mock.patch("neural_ai.core.utils.implementations.hardware_info.os.path.exists", return_value=True):
                with unittest.mock.patch("builtins.open", unittest.mock.mock_open(read_data="")):
                    # Üres fájl esetén is biztonságos viselkedés
                    result_avx2 = hardware_info.has_avx2()
                    result_features = hardware_info.get_cpu_features()
                    result_simd = hardware_info.supports_simd()

                    assert result_avx2 is False
                    assert result_features == set()
                    assert result_simd is False

    def test_cpuinfo_malformed_content(self) -> None:
        """Teszteli a hibásan formázott /proc/cpuinfo tartalom kezelését."""
        hardware_info = HardwareInfo()

        # Teljesen hibás formátum
        malformed_content = """
sdfasdfasdf
asdfasdfasdf
asdfasdf
"""
        with unittest.mock.patch("platform.system", return_value="Linux"):
            with unittest.mock.patch("neural_ai.core.utils.implementations.hardware_info.os.path.exists", return_value=True):
                with unittest.mock.patch("builtins.open", unittest.mock.mock_open(read_data=malformed_content)):
                    # Hibás formátum esetén is biztonságos viselkedés
                    result_avx2 = hardware_info.has_avx2()
                    result_features = hardware_info.get_cpu_features()
                    result_simd = hardware_info.supports_simd()

                    assert result_avx2 is False
                    assert result_features == set()
                    assert result_simd is False

    def test_non_linux_platform_safety(self) -> None:
        """Teszteli a nem Linux platformok biztonságos viselkedését."""
        hardware_info = HardwareInfo()

        # Windows platform
        with unittest.mock.patch("platform.system", return_value="Windows"):
            result_avx2 = hardware_info.has_avx2()
            result_features = hardware_info.get_cpu_features()
            result_simd = hardware_info.supports_simd()

            assert result_avx2 is False
            assert result_features == set()
            assert result_simd is False

        # macOS platform
        with unittest.mock.patch("platform.system", return_value="Darwin"):
            result_avx2 = hardware_info.has_avx2()
            result_features = hardware_info.get_cpu_features()
            result_simd = hardware_info.supports_simd()

            assert result_avx2 is False
            assert result_features == set()
            assert result_simd is False

    def test_cpuinfo_partial_flags_line(self) -> None:
        """Teszteli a részleges flags sor kezelését."""
        hardware_info = HardwareInfo()

        # Flags sor ":" nélkül
        cpuinfo_content = """
processor   : 0
vendor_id   : GenuineIntel
flags       fpu vme de pse tsc msr
"""
        with unittest.mock.patch("platform.system", return_value="Linux"):
            with unittest.mock.patch("neural_ai.core.utils.implementations.hardware_info.os.path.exists", return_value=True):
                with unittest.mock.patch("builtins.open", unittest.mock.mock_open(read_data=cpuinfo_content)):
                    result_avx2 = hardware_info.has_avx2()
                    result_features = hardware_info.get_cpu_features()
                    result_simd = hardware_info.supports_simd()

                    # A split(":", 1) nem talál ":"-t, így a flags rész None lesz
                    assert result_avx2 is False
                    assert result_features == set()
                    assert result_simd is False
