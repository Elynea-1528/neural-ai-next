"""Strategy Service interfész definíciója.

Ez az interfész definiálja a kereskedési stratégia szolgáltatás szerződését,
amely a stratégiák létrehozását, módosítását és tesztelését végzi.
"""

from typing import TYPE_CHECKING, Any, Protocol, runtime_checkable

if TYPE_CHECKING:
    from pandas import DataFrame


@runtime_checkable
class StrategyServiceInterface(Protocol):
    """Strategy Service interfész - Kereskedési stratégiák kezeléséért felelős.

    Ez az interfész definiálja a stratégiák létrehozását, szerkesztését és
    tesztelését végző metódusokat.
    """

    def get_strategies(self) -> list[dict[str, Any]]:
        """Elérhető stratégiák lekérdezése.

        Returns:
            List[Dict[str, Any]]: A stratégiák listája
        """
        ...

    def create_strategy(self, name: str, config: dict[str, Any], code: str) -> str:
        """Új stratégia létrehozása.

        Args:
            name: A stratégia neve
            config: A stratégia konfigurációja
            code: A stratégia kódja

        Returns:
            str: A létrehozott stratégia azonosítója
        """
        ...

    def update_strategy(
        self, strategy_id: str, config: dict[str, Any] | None = None, code: str | None = None
    ) -> bool:
        """Meglévő stratégia módosítása.

        Args:
            strategy_id: A stratégia azonosítója
            config: Az új konfiguráció
            code: Az új kód

        Returns:
            bool: True, ha sikeres a módosítás
        """
        ...

    def delete_strategy(self, strategy_id: str) -> bool:
        """Stratégia törlése.

        Args:
            strategy_id: A stratégia azonosítója

        Returns:
            bool: True, ha sikeres a törlés
        """
        ...

    def backtest_strategy(
        self, strategy_id: str, start_date: str, end_date: str, initial_capital: float
    ) -> dict[str, Any]:
        """Stratégia backtestelése.

        Args:
            strategy_id: A stratégia azonosítója
            start_date: A teszt kezdő dátuma
            end_date: A teszt záró dátuma
            initial_capital: A kezdeti tőke

        Returns:
            Dict[str, Any]: A backtest eredménye
        """
        ...

    def get_backtest_status(self, backtest_id: str) -> dict[str, Any]:
        """Backtest állapotának lekérdezése.

        Args:
            backtest_id: A backtest azonosítója

        Returns:
            Dict[str, Any]: A backtest állapota
        """
        ...

    def optimize_strategy(
        self, strategy_id: str, parameters: dict[str, list[Any]], optimization_method: str = "grid"
    ) -> dict[str, Any]:
        """Stratégia paraméterek optimalizálása.

        Args:
            strategy_id: A stratégia azonosítója
            parameters: Az optimalizálandó paraméterek
            optimization_method: Az optimalizálási módszer

        Returns:
            Dict[str, Any]: Az optimalizálás eredménye
        """
        ...

    async def get_candles(self, symbol: str, date: str, timeframe: str) -> "DataFrame":
        """OHLCV gyertyák lekérdezése a ResamplerService-en keresztül.

        Args:
            symbol: A kereskedési szimbólum (pl. 'EURUSD')
            date: A dátum (pl. '2024-03-20')
            timeframe: Az időkeret (pl. '1m', '5m', '1h', '4h')

        Returns:
            DataFrame: A resample-ölt OHLCV gyertyák DataFrame-ben
        """
        ...
