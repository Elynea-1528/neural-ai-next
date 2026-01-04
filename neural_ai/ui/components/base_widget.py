"""
Base Widget - Alap widget osztály.

Ez a modul implementálja az alap widget osztályt, amelyet
az összes UI komponens örököl.
"""

from typing import Any, Dict, Optional


class BaseWidget:
    """
    Base Widget - Alap widget osztály.
    
    Ez az osztály az összes UI komponens alapját képezi.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        A widget inicializálása.
        
        Args:
            config: A widget konfigurációja
        """
        self._config = config or {}
        self._visible = True

    def render(self) -> str:
        """
        A widget tartalmának renderelése.
        
        Returns:
            str: A renderelt tartalom
        """
        return "Base Widget"

    def show(self) -> None:
        """A widget megjelenítése."""
        self._visible = True

    def hide(self) -> None:
        """A widget elrejtése."""
        self._visible = False

    @property
    def is_visible(self) -> bool:
        """
        A widget láthatóságát ellenőrző property.
        
        Returns:
            bool: True, ha a widget látható, egyébként False
        """
        return self._visible