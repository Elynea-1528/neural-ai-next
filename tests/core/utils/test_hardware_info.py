"""HardwareInfo teszt modul.

Ez a modul a HardwareInfo osztály tesztjeit tartalmazza.
"""

from unittest.mock import mock_open, patch

from neural_ai.core.utils.implementations.hardware_info import HardwareInfo


class TestHardwareInfo:
    """HardwareInfo osztály tesztjei."""

    def test_has_avx2_linux_with_avx2(self) -> None:
        """Teszteli az AVX2 támogatás detektálását AVX2-es CPU-n."""
        mock_cpuinfo = """
processor   : 0
vendor_id   : GenuineIntel
cpu family  : 6
model       : 158
flags       : fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx pdpe1gb rdtscp lm constant_tsc art arch_perfmon pebs bts rep_good nopl xtopology nonstop_tsc cpuid aperfmperf pni pclmulqdq dtes64 monitor ds_cpl vmx est tm2 ssse3 sdbg fma cx16 xtpr pdcm pcid sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand lahf_lm abm 3dnowprefetch cpuid_fault epb invpcid_single pti ssbd ibrs ibpb stibp tpr_shadow vnmi flexpriority ept vpid ept_ad fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid mpx rdseed adx smap clflushopt intel_pt xsaveopt xsavec xgetbv1 xsaves dtherm ida arat pln pts hwp hwp_notify hwp_act_window hwp_epp
"""
        with patch("builtins.open", mock_open(read_data=mock_cpuinfo)):
            with patch("platform.system", return_value="Linux"):
                hardware_info = HardwareInfo()
                assert hardware_info.has_avx2() is True

    def test_has_avx2_linux_without_avx2(self) -> None:
        """Teszteli az AVX2 támogatás detektálását AVX2 nélküli CPU-n."""
        mock_cpuinfo = """
processor   : 0
vendor_id   : GenuineIntel
flags       : fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx lm constant_tsc
"""
        with patch("builtins.open", mock_open(read_data=mock_cpuinfo)):
            with patch("platform.system", return_value="Linux"):
                hardware_info = HardwareInfo()
                assert hardware_info.has_avx2() is False

    def test_has_avx2_non_linux(self) -> None:
        """Teszteli az AVX2 támogatás detektálását nem Linux rendszeren."""
        with patch("platform.system", return_value="Windows"):
            hardware_info = HardwareInfo()
            assert hardware_info.has_avx2() is False

    def test_has_avx2_file_not_found(self) -> None:
        """Teszteli az AVX2 támogatás detektálását, ha a /proc/cpuinfo nem létezik."""
        with patch("os.path.exists", return_value=False):
            with patch("platform.system", return_value="Linux"):
                hardware_info = HardwareInfo()
                assert hardware_info.has_avx2() is False

    def test_get_cpu_features_linux(self) -> None:
        """Teszteli a CPU feature-ök lekérdezését Linux rendszeren."""
        mock_cpuinfo = """
processor   : 0
flags       : fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx lm constant_tsc avx2
"""
        with patch("builtins.open", mock_open(read_data=mock_cpuinfo)):
            with patch("platform.system", return_value="Linux"):
                hardware_info = HardwareInfo()
                features = hardware_info.get_cpu_features()
                assert "avx2" in features
                assert "sse" in features

    def test_get_cpu_features_non_linux(self) -> None:
        """Teszteli a CPU feature-ök lekérdezését nem Linux rendszeren."""
        with patch("platform.system", return_value="Windows"):
            hardware_info = HardwareInfo()
            features = hardware_info.get_cpu_features()
            assert features == set()

    def test_get_cpu_features_file_not_found(self) -> None:
        """Teszteli a CPU feature-ök lekérdezését, ha a /proc/cpuinfo nem létezik."""
        with patch("os.path.exists", return_value=False):
            with patch("platform.system", return_value="Linux"):
                hardware_info = HardwareInfo()
                features = hardware_info.get_cpu_features()
                assert features == set()

    def test_supports_simd_with_simd(self) -> None:
        """Teszteli a SIMD támogatás detektálását SIMD-s CPU-n."""
        mock_cpuinfo = """
processor   : 0
flags       : fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx lm constant_tsc avx
"""
        with patch("builtins.open", mock_open(read_data=mock_cpuinfo)):
            with patch("platform.system", return_value="Linux"):
                hardware_info = HardwareInfo()
                assert hardware_info.supports_simd() is True

    def test_supports_simd_without_simd(self) -> None:
        """Teszteli a SIMD támogatás detektálását SIMD nélküli CPU-n."""
        mock_cpuinfo = """
processor   : 0
flags       : fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat
"""
        with patch("builtins.open", mock_open(read_data=mock_cpuinfo)):
            with patch("platform.system", return_value="Linux"):
                hardware_info = HardwareInfo()
                assert hardware_info.supports_simd() is False

    def test_supports_simd_partial_simd(self) -> None:
        """Teszteli a SIMD támogatás detektálását részleges SIMD támogatással."""
        mock_cpuinfo = """
processor   : 0
flags       : fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse
"""
        with patch("builtins.open", mock_open(read_data=mock_cpuinfo)):
            with patch("platform.system", return_value="Linux"):
                hardware_info = HardwareInfo()
                # Csak SSE van, a többi SIMD flag hiányzik
                assert hardware_info.supports_simd() is True  # Még mindig True, mert SSE is SIMD

    def test_interface_implementation(self) -> None:
        """Teszteli, hogy az osztály megfelelően implementálja-e az interfészt."""
        hardware_info = HardwareInfo()
        assert hasattr(hardware_info, 'has_avx2')
        assert hasattr(hardware_info, 'get_cpu_features')
        assert hasattr(hardware_info, 'supports_simd')
        assert callable(hardware_info.has_avx2)
        assert callable(hardware_info.get_cpu_features)
        assert callable(hardware_info.supports_simd)

    def test_has_avx2_file_read_error(self) -> None:
        """Teszteli az AVX2 támogatás detektálását fájlolvasási hiba esetén."""
        with patch("builtins.open", side_effect=OSError("Permission denied")):
            with patch("platform.system", return_value="Linux"):
                with patch("os.path.exists", return_value=True):
                    hardware_info = HardwareInfo()
                    assert hardware_info.has_avx2() is False

    def test_get_cpu_features_file_read_error(self) -> None:
        """Teszteli a CPU feature-ök lekérdezését fájlolvasási hiba esetén."""
        with patch("builtins.open", side_effect=OSError("Permission denied")):
            with patch("platform.system", return_value="Linux"):
                with patch("os.path.exists", return_value=True):
                    hardware_info = HardwareInfo()
                    features = hardware_info.get_cpu_features()
                    assert features == set()