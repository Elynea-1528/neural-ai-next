"""Hardverinformációk lekérdezéséhez szükséges Factory osztály.

Ez a modul a `HardwareFactory` osztályt tartalmazza, amely a
`HardwareInfo` implementáció példányosításáért felelős.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from neural_ai.core.utils.implementations.hardware_info import HardwareInfo
    from neural_ai.core.utils.interfaces.hardware_interface import HardwareInterface


class HardwareFactory:
    """Factory osztály a `HardwareInfo` példányosításához."""

    @staticmethod
    def get_hardware_info() -> "HardwareInfo":
        """Visszaad egy `HardwareInfo` példányt.

        Returns:
            HardwareInfo: A hardverinformációkat tartalmazó osztály példánya.
        """
        from neural_ai.core.utils.implementations.hardware_info import HardwareInfo
        return HardwareInfo()

    @staticmethod
    def get_hardware_interface() -> "HardwareInterface":
        """Visszaad egy `HardwareInterface`-t implementáló példányt.

        Returns:
            HardwareInterface: A hardverinterfészt implementáló osztály példánya.
        """
        from neural_ai.core.utils.implementations.hardware_info import HardwareInfo
        return HardwareInfo()
