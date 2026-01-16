"""Live Ops Service interfész definíciója.

Ez az interfész definiálja a live műveletek szolgáltatás szerződését,
amely a valós idejű kereskedést és monitorozást végzi.
"""

from typing import TYPE_CHECKING, Any, Protocol, runtime_checkable

if TYPE_CHECKING:
    pass


@runtime_checkable
class LiveOpsServiceInterface(Protocol):
    """Live Ops Service interfész - Valós idejű műveletekért felelős.
    
    Ez az interfész definiálja a live kereskedést és monitorozást
    végző metódusokat.
    """

    def get_active_positions(self) -> list[dict[str, Any]]:
        """Aktív pozíciók lekérdezése.
        
        Returns:
            List[Dict[str, Any]]: Az aktív pozíciók listája
        """
        ...

    def get_account_status(self) -> dict[str, Any]:
        """Fiók állapotának lekérdezése.
        
        Returns:
            Dict[str, Any]: A fiók aktuális állapota
        """
        ...

    def place_order(
        self,
        symbol: str,
        order_type: str,
        volume: float,
        price: float | None = None,
        stop_loss: float | None = None,
        take_profit: float | None = None
    ) -> str:
        """Új rendelés leadása.
        
        Args:
            symbol: A kereskedendő szimbólum
            order_type: A rendelés típusa (BUY/SELL)
            volume: A kereskedési volumen
            price: A rendelés ára (opcionális)
            stop_loss: Stop loss szint (opcionális)
            take_profit: Take profit szint (opcionális)
            
        Returns:
            str: A rendelés azonosítója
        """
        ...

    def modify_order(
        self,
        order_id: str,
        price: float | None = None,
        stop_loss: float | None = None,
        take_profit: float | None = None
    ) -> bool:
        """Meglévő rendelés módosítása.
        
        Args:
            order_id: A rendelés azonosítója
            price: Az új ár
            stop_loss: Az új stop loss
            take_profit: Az új take profit
            
        Returns:
            bool: True, ha sikeres a módosítás
        """
        ...

    def cancel_order(self, order_id: str) -> bool:
        """Rendelés visszavonása.
        
        Args:
            order_id: A rendelés azonosítója
            
        Returns:
            bool: True, ha sikeres a visszavonás
        """
        ...

    def close_position(self, position_id: str) -> bool:
        """Pozíció lezárása.
        
        Args:
            position_id: A pozíció azonosítója
            
        Returns:
            bool: True, ha sikeres a lezárás
        """
        ...

    def get_market_data(self, symbol: str) -> dict[str, Any]:
        """Piaci adatok lekérdezése.
        
        Args:
            symbol: A szimbólum
            
        Returns:
            Dict[str, Any]: A piaci adatok
        """
        ...

    def subscribe_to_market_updates(
        self,
        symbol: str,
        callback: Any
    ) -> None:
        """Feliratkozás piaci frissítésekre.
        
        Args:
            symbol: A szimbólum
            callback: A hívandó callback függvény
        """
        ...

    def get_performance_summary(self) -> dict[str, Any]:
        """Teljesítmény összegzés lekérdezése.
        
        Returns:
            Dict[str, Any]: A teljesítmény adatok
        """
        ...
