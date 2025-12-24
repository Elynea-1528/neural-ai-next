"""Core segédfunkciók és utility osztályok.

Ez a csomag tartalmazza a Neural AI Next rendszer alapvető segédfunkcióit,
beleértve a hardver detekciót, típuskonverziókat és egyéb általános célú
eszközöket.
"""

from neural_ai.core.utils.hardware import (
    get_cpu_features,
    has_avx2,
    supports_simd,
)

__all__ = [
    "get_cpu_features",
    "has_avx2",
    "supports_simd",
]
