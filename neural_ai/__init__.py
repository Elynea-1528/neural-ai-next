"""Neural-AI-Next projekt fő inicializációs modulja.

Ez a modul felelős a projekt verzióinformációinak és alapvető konfigurációjának
exportálásáért. A verziószámot dinamikusan tölti be a pyproject.toml fájlból
az importlib.metadata segítségével.

Attributes:
    __version__: A projekt aktuális verziószáma string formátumban.
    __schema_version__: A konfigurációs séma verziószáma a kompatibilitás
        ellenőrzéséhez.

Példa:
    >>> import neural_ai
    >>> print(f"Neural-AI-Next verzió: {neural_ai.__version__}")
    Neural-AI-Next verzió: 1.0.0
"""

from importlib import metadata
from typing import Final

try:
    _version: str = metadata.version("neural-ai-next")
except metadata.PackageNotFoundError:
    # Fallback a pyproject.toml-ból, ha a csomag nincs telepítve
    _version = "0.5.0"

__version__: Final[str] = _version

# Konfigurációs séma verzió - a 10. fejezet szerint
__schema_version__: Final[str] = "1.0"

__all__: Final[list[str]] = [
    "__version__",
    "__schema_version__",
]
