"""Util kivételek modulja.

Ez a modul exportálja az összes utility kivételosztályt.
"""

from neural_ai.core.utils.exceptions.util_error import (
    HardwareDetectionError,
    UtilError,
)

__all__ = [
    "UtilError",
    "HardwareDetectionError",
]
