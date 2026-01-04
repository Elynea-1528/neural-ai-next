"""
Strategy Service implementáció.

Ez a modul implementálja a kereskedési stratégia szolgáltatást,
amely a stratégiák létrehozását, módosítását és tesztelését végzi.
"""

from typing import Dict, Any, List, Optional
from typing import TYPE_CHECKING

from neural_ai.ui.interfaces.strategy_service_interface import StrategyServiceInterface

if TYPE_CHECKING:
    from neural_ai.ui.interfaces.core_bridge_interface import CoreBridgeInterface


class StrategyService(StrategyServiceInterface):
    """
    Strategy Service - Kereskedési stratégiák kezeléséért felelős.
    
    Ez az osztály implementálja a stratégiák létrehozását, szerkesztését és
    tesztelését végző metódusokat.
    """

    def __init__(self, bridge: "CoreBridgeInterface") -> None:
        """
        A Strategy Service inicializálása.
        
        Args:
            bridge: A backend bridge példány
        """
        self._bridge = bridge
        self._strategies: Dict[str, Dict[str, Any]] = {
            "moving_avg_cross": {
                "name": "Mozgóátlag Kereszt",
                "description": "Egyszerű mozgóátlag kereszt stratégia",
                "type": "technical",
                "status": "active"
            },
            "rsi_strategy": {
                "name": "RSI Stratégia",
                "description": "RSI indikátoron alapuló stratégia",
                "type": "technical",
                "status": "active"
            }
        }
        self._backtests: Dict[str, Dict[str, Any]] = {}
        self._optimizations: Dict[str, Dict[str, Any]] = {}

    def get_strategies(self) -> List[Dict[str, Any]]:
        """
        Elérhető stratégiák lekérdezése.
        
        Returns:
            List[Dict[str, Any]]: A stratégiák listája
        """
        strategies = []
        for strategy_id, info in self._strategies.items():
            strategies.append({
                "id": strategy_id,
                "name": info["name"],
                "description": info["description"],
                "type": info["type"],
                "status": info["status"]
            })
        return strategies

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
        # Generáljunk egy egyedi azonosítót
        strategy_id = f"strategy_{len(self._strategies) + 1}"
        
        self._strategies[strategy_id] = {
            "name": name,
            "description": f"Új stratégia: {name}",
            "type": "custom",
            "status": "active",
            "config": config,
            "code": code,
            "created_at": "2026-01-04T19:24:00Z"
        }

        print(f"Stratégia létrehozva: {strategy_id}")
        return strategy_id

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
        if strategy_id not in self._strategies:
            raise ValueError(f"Ismeretlen stratégia: {strategy_id}")

        strategy = self._strategies[strategy_id]
        
        if config is not None:
            strategy["config"] = config
        
        if code is not None:
            strategy["code"] = code

        strategy["updated_at"] = "2026-01-04T19:24:00Z"
        
        print(f"Stratégia módosítva: {strategy_id}")
        return True

    def delete_strategy(self, strategy_id: str) -> bool:
        """
        Stratégia törlése.
        
        Args:
            strategy_id: A stratégia azonosítója
            
        Returns:
            bool: True, ha sikeres a törlés
        """
        if strategy_id not in self._strategies:
            raise ValueError(f"Ismeretlen stratégia: {strategy_id}")

        del self._strategies[strategy_id]
        
        print(f"Stratégia törölve: {strategy_id}")
        return True

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
        if strategy_id not in self._strategies:
            raise ValueError(f"Ismeretlen stratégia: {strategy_id}")

        # Mock backtest indítása
        backtest_id = f"backtest_{strategy_id}_{len(self._backtests)}"
        
        self._backtests[backtest_id] = {
            "strategy_id": strategy_id,
            "start_date": start_date,
            "end_date": end_date,
            "initial_capital": initial_capital,
            "status": "running",
            "started_at": "2026-01-04T19:24:00Z"
        }

        result = {
            "backtest_id": backtest_id,
            "strategy_id": strategy_id,
            "status": "started",
            "message": "Backtest elindítva"
        }

        return result

    def get_backtest_status(self, backtest_id: str) -> Dict[str, Any]:
        """
        Backtest állapotának lekérdezése.
        
        Args:
            backtest_id: A backtest azonosítója
            
        Returns:
            Dict[str, Any]: A backtest állapota
        """
        if backtest_id not in self._backtests:
            raise ValueError(f"Ismeretlen backtest: {backtest_id}")

        backtest = self._backtests[backtest_id]
        
        # Mock állapot frissítés
        status = {
            "backtest_id": backtest_id,
            "strategy_id": backtest["strategy_id"],
            "status": "completed",
            "progress": 1.0,
            "start_date": backtest["start_date"],
            "end_date": backtest["end_date"],
            "initial_capital": backtest["initial_capital"],
            "final_capital": backtest["initial_capital"] * 1.15,  # Mock nyereség
            "total_return": 0.15,
            "max_drawdown": -0.05,
            "sharpe_ratio": 1.2,
            "total_trades": 45,
            "win_rate": 0.62
        }

        return status

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
        if strategy_id not in self._strategies:
            raise ValueError(f"Ismeretlen stratégia: {strategy_id}")

        # Mock optimalizálás indítása
        optimization_id = f"optimization_{strategy_id}_{len(self._optimizations)}"
        
        self._optimizations[optimization_id] = {
            "strategy_id": strategy_id,
            "parameters": parameters,
            "method": optimization_method,
            "status": "running",
            "started_at": "2026-01-04T19:24:00Z"
        }

        result = {
            "optimization_id": optimization_id,
            "strategy_id": strategy_id,
            "status": "started",
            "message": "Optimalizálás elindítva"
        }

        return result