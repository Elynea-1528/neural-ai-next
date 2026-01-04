"""
Strategy Service interfész definíciója.

Ez az interfész definiálja a kereskedési stratégia szolgáltatás szerződését,
amely a stratégiák létrehozását, módosítását és tesztelését végzi.
"""

from typing import Protocol, runtime_checkable, Dict, Any, List, Optional
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from neural_ai.ui.interfaces.core_bridge_interface import CoreBridgeInterface


@runtime_checkable
class StrategyServiceInterface(Protocol):
    """
    Strategy Service interfész - Kereskedési stratégiák kezeléséért felelős.
    
    Ez az interfész definiálja a stratégiák létrehozását, szerkesztését és
    tesztelését végző metódusokat.
    """

    def get_strategies(self) -> List[Dict[str, Any]]:
        """
        Elérhető stratégiák lekérdezése.
        
        Returns:
            List[Dict[str, Any]]: A stratégiák listája
        """
        ...

    def create_strategy(
        self,
        name: str,
        config: Dict[str, Any],
        code: str
    ) -> str:
        """
        Új stratégia létrehozása.
        
        Args:
            name: A stratégia neve
            config: A stratégia konfigurációja
            code: A stratégia kódja
            
        Returns:
            str: A létrehozott stratégia azonosítója
        """
        ...

    def update_strategy(
        self,
        strategy_id: str,
        config: Optional[Dict[str, Any]] = None,
        code: Optional[str] = None
    ) -> bool:
        """
        Meglévő stratégia módosítása.
        
        Args:
            strategy_id: A stratégia azonosítója
            config: Az új konfiguráció
            code: Az új kód
            
        Returns:
            bool: True, ha sikeres a módosítás
        """
        ...

    def delete_strategy(self, strategy_id: str) -> bool:
        """
        Stratégia törlése.
        
        Args:
            strategy_id: A stratégia azonosítója
            
        Returns:
            bool: True, ha sikeres a törlés
        """
        ...

    def backtest_strategy(
        self,
        strategy_id: str,
        start_date: str,
        end_date: str,
        initial_capital: float
    ) -> Dict[str, Any]:
        """
        Stratégia backtestelése.
        
        Args:
            strategy_id: A stratégia azonosítója
            start_date: A teszt kezdő dátuma
            end_date: A teszt záró dátuma
            initial_capital: A kezdeti tőke
            
        Returns:
            Dict[str, Any]: A backtest eredménye
        """
        ...

    def get_backtest_status(self, backtest_id: str) -> Dict[str, Any]:
        """
        Backtest állapotának lekérdezése.
        
        Args:
            backtest_id: A backtest azonosítója
            
        Returns:
            Dict[str, Any]: A backtest állapota
        """
        ...

    def optimize_strategy(
        self,
        strategy_id: str,
        parameters: Dict[str, List[Any]],
        optimization_method: str = "grid"
    ) -> Dict[str, Any]:
        """
        Stratégia paraméterek optimalizálása.
        
        Args:
            strategy_id: A stratégia azonosítója
            parameters: Az optimalizálandó paraméterek
            optimization_method: Az optimalizálási módszer
            
        Returns:
            Dict[str, Any]: Az optimalizálás eredménye
        """
        ...