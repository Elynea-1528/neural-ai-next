"""Hardverinformációk lekérdezését implementáló osztály.

Ez a modul a `HardwareInfo` osztályt tartalmazza, amely a
`HardwareInterface` interfészt implementálja, és a hardver-specifikus
képességek (CPU feature-ök) lekérdezését valósítja meg a `/proc/cpuinfo`
fájl elemzésével.
"""

import os
import platform
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from neural_ai.core.utils.interfaces.hardware_interface import HardwareInterface


class HardwareInfo:
    """Hardverinformációk lekérdezését implementáló osztály.

    Ez az osztály a `HardwareInterface` interfészt implementálja, és
    a hardver-specifikus képességek (mint az AVX2, SIMD) biztonságos
    és egységes lekérdezését valósítja meg a `/proc/cpuinfo` fájl
    elemzésével.
    """

    def has_avx2(self) -> bool:
        """Ellenőrzi, hogy a CPU támogatja-e az AVX2 utasításkészletet.

        A függvény a `/proc/cpuinfo` fájlt elemzi Linux rendszereken, hogy
        detektálja az AVX2 támogatást. Ez a metódus nem okozhat Illegal
        Instruction hibát, mivel csak fájlolvasást végez, nem pedig közvetlen
        utasításkészlet-használatot.

        Returns:
            bool: True, ha a CPU támogatja az AVX2-t, False egyébként.

        Examples:
            >>> hardware_info = HardwareInfo()
            >>> if hardware_info.has_avx2():
            ...     # Használhatunk AVX2-gyorsított műveleteket
            ...     pass
            ... else:
            ...     # Fallback implementáció használata
            ...     pass

        Note:
            Jelenleg csak Linux rendszereken támogatott. Más platformokon
            (Windows, macOS) a függvény False értéket ad vissza.

            Ez a metódus biztonságosabb, mint a CPUID utasítás közvetlen
            használata, mivel nem próbálja végrehajtani az AVX2 utasításokat
            olyan CPU-n, amely nem támogatja azokat.
        """
        if platform.system() != "Linux":
            # Nem Linux rendszeren nem tudjuk ellenőrizni a /proc/cpuinfo-t
            # Ebben az esetben biztonságosan feltételezzük, hogy nincs AVX2 támogatás
            return False

        cpuinfo_path = "/proc/cpuinfo"

        if not os.path.exists(cpuinfo_path):
            # Ha valamiért nem létezik a fájl, biztonságosabb False-t visszaadni
            return False

        try:
            with open(cpuinfo_path, encoding="utf-8") as f:
                cpuinfo_content = f.read()

            # Az AVX2 támogatását a 'avx2' flag jelzi a cpuinfo-ban
            # A flag-ek a 'flags' sorban vannak felsorolva
            lines = cpuinfo_content.splitlines()

            for line in lines:
                if line.startswith("flags"):
                    # A flags sor formátuma: "flags : flag1 flag2 ... flagn"
                    flags_part = line.split(":", 1)
                    if len(flags_part) == 2:
                        flags = flags_part[1].strip().split()
                        return "avx2" in flags

            return False

        except (OSError, PermissionError):
            # Ha bármilyen hiba történik a fájl olvasása közben,
            # biztonságosabb False-t visszaadni
            return False

    def get_cpu_features(self) -> set[str]:
        """Visszaadja a CPU által támogatott összes feature flag-et.

        A függvény a `/proc/cpuinfo` fájlból kinyeri az összes elérhető
        processzor-feature-t Linux rendszereken.

        Returns:
            set[str]: A CPU által támogatott feature flag-ek halmaza.
                Üres halmazt ad vissza, ha nem sikerült beolvasni a flag-eket.

        Note:
            Csak Linux rendszereken működik. Más platformokon üres halmazt ad vissza.
        """
        if platform.system() != "Linux":
            return set()

        cpuinfo_path = "/proc/cpuinfo"

        if not os.path.exists(cpuinfo_path):
            return set()

        try:
            with open(cpuinfo_path, encoding="utf-8") as f:
                cpuinfo_content = f.read()

            lines = cpuinfo_content.splitlines()

            for line in lines:
                if line.startswith("flags"):
                    flags_part = line.split(":", 1)
                    if len(flags_part) == 2:
                        flags = flags_part[1].strip().split()
                        return set(flags)

            return set()

        except (OSError, PermissionError):
            return set()

    def supports_simd(self) -> bool:
        """Ellenőrzi, hogy a CPU támogatja-e az alapvető SIMD utasításokat.

        A függvény ellenőrzi az SSE, SSE2, SSE3, SSE4.1, SSE4.2 és AVX
        támogatását. Ezek az utasításkészlet-bővítmények gyakran hasznosak
        numerikus számításokhoz és adatfeldolgozáshoz.

        Returns:
            bool: True, ha a CPU támogatja az alapvető SIMD utasításokat.

        Note:
            Csak Linux rendszereken működik. Más platformokon False-t ad vissza.
        """
        features = self.get_cpu_features()
        simd_flags = {"sse", "sse2", "sse3", "ssse3", "sse4_1", "sse4_2", "avx"}
        return bool(features & simd_flags)