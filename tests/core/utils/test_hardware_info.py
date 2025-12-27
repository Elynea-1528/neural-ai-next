"""Tesztek a HardwareInfo osztályhoz.

Ez a modul a `HardwareInfo` osztály tesztjeit tartalmazza, amelyek ellenőrzik
a hardverinformációk lekérdezésének helyes működését.
"""

import platform
import unittest
from unittest.mock import mock_open, patch

from neural_ai.core.utils.factory import HardwareFactory


class TestHardwareInfo(unittest.TestCase):
    """Tesztosztály a HardwareInfo metódusainak teszteléséhez."""

    def setUp(self) -> None:
        """Tesztelés előtti beállítások."""
        self.hardware_info = HardwareFactory.get_hardware_info()

    def test_has_avx2_linux_with_avx2(self) -> None:
        """Teszteli az AVX2 támogatás detektálását Linuxon AVX2 flag-gel."""
        if platform.system() != "Linux":
            self.skipTest("Csak Linux rendszeren futtatható")

        cpuinfo_content = (
            "flags\t\t: fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca "
            "cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall "
            "nx pdpe1gb rdtscp lm constant_tsc art arch_perfmon pebs bts rep_good "
            "nopl xtopology nonstop_tsc cpuid aperfmperf tsc_known_freq pni "
            "pclmulqdq dtes64 monitor ds_cpl vmx est tm2 ssse3 sdbg fma cx16 xtpr "
            "pdcm pcid sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes "
            "xsave avx f16c rdrand lahf_lm abm 3dnowprefetch cpuid_fault epb "
            "invpcid_single pti ssbd ibrs ibpb stibp tpr_shadow vnmi flexpriority "
            "ept vpid ept_ad fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid "
            "mpx rdseed adx smap clflushopt intel_pt xsaveopt xsavec xgetbv1 xsaves "
            "dtherm ida arat pln pts hwp hwp_notify hwp_act_window hwp_epp"
        )

        with patch("builtins.open", mock_open(read_data=cpuinfo_content)):
            result = self.hardware_info.has_avx2()
            self.assertTrue(result)

    def test_has_avx2_linux_without_avx2(self) -> None:
        """Teszteli az AVX2 támogatás detektálását Linuxon AVX2 flag nélkül."""
        if platform.system() != "Linux":
            self.skipTest("Csak Linux rendszeren futtatható")

        cpuinfo_content = (
            "flags\t\t: fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca "
            "cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall "
            "nx pdpe1gb rdtscp lm constant_tsc art arch_perfmon pebs bts rep_good "
            "nopl xtopology nonstop_tsc cpuid aperfmperf tsc_known_freq pni "
            "pclmulqdq dtes64 monitor ds_cpl vmx est tm2 ssse3 sdbg fma cx16 xtpr "
            "pdcm pcid sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes "
            "xsave avx f16c rdrand lahf_lm abm 3dnowprefetch cpuid_fault epb "
            "invpcid_single pti ssbd ibrs ibpb stibp tpr_shadow vnmi flexpriority "
            "ept vpid ept_ad fsgsbase tsc_adjust bmi1 smep bmi2 erms invpcid "
            "mpx rdseed adx smap clflushopt intel_pt xsaveopt xsavec xgetbv1 xsaves "
            "dtherm ida arat pln pts hwp hwp_notify hwp_act_window hwp_epp"
        )

        with patch("builtins.open", mock_open(read_data=cpuinfo_content)):
            result = self.hardware_info.has_avx2()
            self.assertFalse(result)

    def test_has_avx2_non_linux(self) -> None:
        """Teszteli az AVX2 támogatás detektálását nem Linux rendszeren."""
        with patch("platform.system", return_value="Windows"):
            result = self.hardware_info.has_avx2()
            self.assertFalse(result)

    def test_has_avx2_file_not_found(self) -> None:
        """Teszteli az AVX2 támogatás detektálását, ha a cpuinfo fájl nem létezik."""
        if platform.system() != "Linux":
            self.skipTest("Csak Linux rendszeren futtatható")

        with patch("os.path.exists", return_value=False):
            result = self.hardware_info.has_avx2()
            self.assertFalse(result)

    def test_get_cpu_features_linux(self) -> None:
        """Teszteli a CPU feature-ök lekérdezését Linuxon."""
        if platform.system() != "Linux":
            self.skipTest("Csak Linux rendszeren futtatható")

        cpuinfo_content = (
            "flags\t\t: fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca "
            "cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall "
            "nx pdpe1gb rdtscp lm constant_tsc art arch_perfmon pebs bts rep_good "
            "nopl xtopology nonstop_tsc cpuid aperfmperf tsc_known_freq pni "
            "pclmulqdq dtes64 monitor ds_cpl vmx est tm2 ssse3 sdbg fma cx16 xtpr "
            "pdcm pcid sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes "
            "xsave avx f16c rdrand lahf_lm abm 3dnowprefetch cpuid_fault epb "
            "invpcid_single pti ssbd ibrs ibpb stibp tpr_shadow vnmi flexpriority "
            "ept vpid ept_ad fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid "
            "mpx rdseed adx smap clflushopt intel_pt xsaveopt xsavec xgetbv1 xsaves "
            "dtherm ida arat pln pts hwp hwp_notify hwp_act_window hwp_epp"
        )

        with patch("builtins.open", mock_open(read_data=cpuinfo_content)):
            features = self.hardware_info.get_cpu_features()
            self.assertIsInstance(features, set)
            self.assertIn("avx2", features)
            self.assertIn("sse", features)
            self.assertIn("sse2", features)

    def test_get_cpu_features_non_linux(self) -> None:
        """Teszteli a CPU feature-ök lekérdezését nem Linux rendszeren."""
        with patch("platform.system", return_value="Windows"):
            features = self.hardware_info.get_cpu_features()
            self.assertIsInstance(features, set)
            self.assertEqual(len(features), 0)

    def test_get_cpu_features_file_not_found(self) -> None:
        """Teszteli a CPU feature-ök lekérdezését, ha a cpuinfo fájl nem létezik."""
        if platform.system() != "Linux":
            self.skipTest("Csak Linux rendszeren futtatható")

        with patch("os.path.exists", return_value=False):
            features = self.hardware_info.get_cpu_features()
            self.assertIsInstance(features, set)
            self.assertEqual(len(features), 0)

    def test_supports_simd_with_simd(self) -> None:
        """Teszteli a SIMD támogatás detektálását, ha van SIMD támogatás."""
        simd_features = {"sse", "sse2", "sse3", "ssse3", "sse4_1", "sse4_2", "avx"}
        with patch.object(self.hardware_info, "get_cpu_features", return_value=simd_features):
            result = self.hardware_info.supports_simd()
            self.assertTrue(result)

    def test_supports_simd_without_simd(self) -> None:
        """Teszteli a SIMD támogatás detektálását, ha nincs SIMD támogatás."""
        non_simd_features = {"fpu", "vme", "de", "pse"}
        with patch.object(self.hardware_info, "get_cpu_features", return_value=non_simd_features):
            result = self.hardware_info.supports_simd()
            self.assertFalse(result)

    def test_supports_simd_partial_simd(self) -> None:
        """Teszteli a SIMD támogatás detektálását részleges SIMD támogatás esetén."""
        partial_simd_features = {"sse", "sse2", "fpu", "vme"}
        with patch.object(
            self.hardware_info, "get_cpu_features", return_value=partial_simd_features
        ):
            result = self.hardware_info.supports_simd()
            self.assertTrue(result)

    def test_interface_implementation(self) -> None:
        """Teszteli, hogy a HardwareInfo osztály megfelelően implementálja-e az interfészt."""
        self.assertTrue(hasattr(self.hardware_info, "has_avx2"))
        self.assertTrue(hasattr(self.hardware_info, "get_cpu_features"))
        self.assertTrue(hasattr(self.hardware_info, "supports_simd"))
        self.assertTrue(callable(self.hardware_info.has_avx2))
        self.assertTrue(callable(self.hardware_info.get_cpu_features))
        self.assertTrue(callable(self.hardware_info.supports_simd))


if __name__ == "__main__":
    unittest.main()
