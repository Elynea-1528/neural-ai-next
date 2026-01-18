"""UI oldalak csomagja.

Ez a csomag tartalmazza a különböző főoldalakat (Launchpad, Dev Center,
Data Hub, AI Lab, Strategy Lab, Live Ops), amelyek a felhasználói
felület különböző szekcióit reprezentálják.
"""

from typing import TYPE_CHECKING

from neural_ai.ui.core_bridge import CoreBridge

if TYPE_CHECKING:
    from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
    from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
    from neural_ai.ui.interfaces.page_interface import PageInterface


def create_launchpad_page(
    logger: "LoggerInterface", config: "ConfigManagerInterface"
) -> "PageInterface":
    """Launchpad oldal példány létrehozása Dependency Injection segítségével.

    Ez a factory függvény a LaunchpadPage példányt hozza létre a szükséges
    függőségekkel. A függőségeket interfészeken keresztül kapja meg,
    biztosítva a loose coupling-ot.

    Args:
        logger: Logger interfész a logoláshoz.
        config: Konfigurációkezelő interfész.

    Returns:
        PageInterface: A létrehozott Launchpad oldal példány.

    Note:
        A függvény belsőleg létrehozza és inicializálja a CoreBridge-et,
        amely biztosítja a backend kapcsolatot.
    """
    # CoreBridge létrehozása és inicializálása
    bridge = CoreBridge()
    bridge.initialize()

    # Dinamikus import az emoji karakter miatt
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "launchpad_module", "neural_ai/ui/pages/01_🚀_Launchpad.py"
    )
    if spec and spec.loader:
        launchpad_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(launchpad_module)
        LaunchpadPage = launchpad_module.LaunchpadPage
    else:
        raise ImportError("Could not import LaunchpadPage module")

    return LaunchpadPage(bridge, logger)


__all__ = ["create_launchpad_page"]
