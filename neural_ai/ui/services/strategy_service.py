"""Strategy Service implementáció.

Ez a modul implementálja a kereskedési stratégia szolgáltatást,
 amely a stratégiák létrehozását, módosítását és tesztelését végzi.
"""

from datetime import datetime
from typing import TYPE_CHECKING, Any

from neural_ai.ui.interfaces.strategy_service_interface import StrategyServiceInterface

if TYPE_CHECKING:
    import polars as pl

    from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
    from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
    from neural_ai.processors.resampler_service.interfaces.resampler_interface import (
        ResamplerInterface,
    )
    from neural_ai.ui.interfaces.core_bridge_interface import CoreBridgeInterface


class StrategyService(StrategyServiceInterface):
    """Strategy Service - Kereskedési stratégiák kezeléséért felelős.

    Ez az osztály implementálja a stratégiák létrehozását, szerkesztését és
    tesztelését végző metódusokat.
    """

    def __init__(self, logger: Any, config: dict[str, Any], core_components: Any) -> None:
        """A Strategy Service inicializálása.

        Args:
            logger: A logger példány
            config: A szolgáltatás konfiguráció
            core_components: A core komponensek
        """
        self._logger = logger
        self._config = config
        self._core_components = core_components
        self._strategies: dict[str, dict[str, Any]] = {
            "moving_avg_cross": {
                "name": "Mozgóátlag Kereszt",
                "description": "Egyszerű mozgóátlag kereszt stratégia",
                "type": "technical",
                "status": "active",
            },
            "rsi_strategy": {
                "name": "RSI Stratégia",
                "description": "RSI indikátoron alapuló stratégia",
                "type": "technical",
                "status": "active",
            },
        }
        self._backtests: dict[str, dict[str, Any]] = {}
        self._optimizations: dict[str, dict[str, Any]] = {}

    def get_strategies(self) -> list[dict[str, str]]:
        """Elérhető stratégiák lekérdezése.

        Returns:
            List[Dict[str, Any]]: A stratégiák listája
        """
        strategies = []
        for strategy_id, info in self._strategies.items():
            strategies.append(
                {
                    "id": strategy_id,
                    "name": info["name"],
                    "description": info["description"],
                    "type": info["type"],
                    "status": info["status"],
                }
            )
        return strategies

    def create_strategy(self, name: str, config: dict[str, Any], code: str) -> str:
        """Új stratégia létrehozása.

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
            "created_at": "2026-01-04T19:24:00Z",
        }

        print(f"Stratégia létrehozva: {strategy_id}")
        return strategy_id

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
        """Stratégia törlése.

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
            "started_at": "2026-01-04T19:24:00Z",
        }

        result = {
            "backtest_id": backtest_id,
            "strategy_id": strategy_id,
            "status": "started",
            "message": "Backtest elindítva",
        }

        return result

    def get_backtest_status(self, backtest_id: str) -> dict[str, Any]:
        """Backtest állapotának lekérdezése.

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
            "win_rate": 0.62,
        }

        return status

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
        if strategy_id not in self._strategies:
            raise ValueError(f"Ismeretlen stratégia: {strategy_id}")

        # Mock optimalizálás indítása
        optimization_id = f"optimization_{strategy_id}_{len(self._optimizations)}"

        self._optimizations[optimization_id] = {
            "strategy_id": strategy_id,
            "parameters": parameters,
            "method": optimization_method,
            "status": "running",
            "started_at": "2026-01-04T19:24:00Z",
        }

        result = {
            "optimization_id": optimization_id,
            "strategy_id": strategy_id,
            "status": "started",
            "message": "Optimalizálás elindítva",
        }

        return result

    async def get_candles(self, symbol: str, date: str, timeframe: str) -> "pl.DataFrame":
        """OHLCV gyertyák lekérdezése a ResamplerService-en keresztül.

        Ez a metódus a megadott szimbólumhoz, dátumhoz és időkerethez
        tartozó resample-ölt OHLCV adatokat kérdezi le.

        Args:
            symbol: A kereskedési szimbólum (pl. 'EURUSD')
            date: A dátum (pl. '2024-03-20')
            timeframe: Az időkeret (pl. '1m', '5m', '1h', '4h')

        Returns:
            pl.DataFrame: A resample-ölt OHLCV gyertyák DataFrame-ben
        """
        # ResamplerService példányosítása Factory-n keresztül
        from neural_ai.processors.resampler_service.factory import (
            ResamplerServiceFactory,
        )

        # ResamplerService példány lekérése a Factory-tól
        resampler: ResamplerInterface = ResamplerServiceFactory.get_instance()

        # Dátum string konvertálása datetime objektummá
        start_date: datetime = datetime.strptime(date, "%Y-%m-%d")
        # A nap végének beállítása
        end_date: datetime = datetime.strptime(f"{date} 23:59:59", "%Y-%m-%d %H:%M:%S")

        # Resample metódus hívása az OHLCV adatok lekéréséhez (async)
        candles: pl.DataFrame = await resampler.resample(
            symbol=symbol, start=start_date, end=end_date, timeframe=timeframe, return_type="polars"
        )

        return candles

    async def run_sma_backtest(
        self,
        symbol: str,
        date: str,
        timeframe: str,
        fast_period: int,
        slow_period: int,
        initial_capital: float = 10000.0,
        df=None,
    ) -> dict[str, Any]:
        """SMA kereszt stratégia backtesztelése VectorBT-vel.

        Ez a metódus betölti az adatokat, kiszámolja az SMA indikátorokat,
        generálja a belépési és kilépési jeleket, majd lefuttatja a backtestet.

        Args:
            symbol: A kereskedési szimbólum (pl. 'EURUSD')
            date: A dátum (pl. '2024-03-20')
            timeframe: Az időkeret (pl. '1m', '5m', '1h', '4h')
            fast_period: A gyors SMA periódusa
            slow_period: A lassú SMA periódusa
            initial_capital: A kezdeti tőke (default: 10000.0)
            df: Opcionális DataFrame az adatokhoz (ha None, akkor betölti get_candles-szel)

        Returns:
            Dict[str, Any]: A backtest eredménye (stats, equity, trades, signals)
        """
        # 1. Adatbetöltés
        if df is None:
            df = await self.get_candles(symbol, date, timeframe)

        if df is None or len(df) == 0:
            return {
                "error": "Nincs elérhető adat a megadott paraméterekhez.",
                "stats": {},
                "equity": [],
                "trades": [],
                "signals": {"entries": [], "exits": []},
            }

        # Oszlopnevek normalizálása (kisbetűsítés)
        df.columns = [col.lower() for col in df.columns]

        try:
            import pandas as pd
            import vectorbt as vbt

            # DataFrame konvertálása Pandas-ra VectorBT-hez (ha szükséges)
            if hasattr(df, "to_pandas"):
                df_pd = df.to_pandas()
            else:
                df_pd = df

            # Oszlopnevek normalizálása (kisbetű)
            df_pd.columns = [col.lower() for col in df_pd.columns]

            # --- AUTO-MAPPING LOGIKA ---
            if "close" not in df_pd.columns:
                if "mid_close" in df_pd.columns:
                    rename_map = {
                        "mid_open": "open",
                        "mid_high": "high",
                        "mid_low": "low",
                        "mid_close": "close",
                    }
                    df_pd = df_pd.rename(columns=rename_map)
                elif "bid_close" in df_pd.columns:
                    rename_map = {
                        "bid_open": "open",
                        "bid_high": "high",
                        "bid_low": "low",
                        "bid_close": "close",
                    }
                    df_pd = df_pd.rename(columns=rename_map)

            # OHLC oszlopok ellenőrzése
            ohlc_columns = ["open", "high", "low", "close"]
            if not all(col in df_pd.columns for col in ohlc_columns):
                return {
                    "error": "Az adatokban nem található OHLC oszlop.",
                    "stats": {},
                    "equity": [],
                    "trades": [],
                    "signals": {"entries": [], "exits": []},
                }

            # Adat előkészítés: Index ellenőrzése és javítása
            if not isinstance(df_pd.index, pd.DatetimeIndex):
                if "timestamp" in df_pd.columns:
                    df_pd.index = pd.to_datetime(df_pd["timestamp"])
                else:
                    df_pd.index = pd.to_datetime(df_pd.index)

            # 2. VBT Logika - SMA indikátorok számolása short_name paraméterekkel
            fast_ma = vbt.MA.run(df_pd["close"], fast_period, short_name="fast")
            slow_ma = vbt.MA.run(df_pd["close"], slow_period, short_name="slow")

            # 3. Jelek generálása
            entries = fast_ma.ma_crossed_above(slow_ma)
            exits = fast_ma.ma_crossed_below(slow_ma)

            # 4. Portfólió futtatása freq paraméterrel az időköz egyértelműségért
            pf = vbt.Portfolio.from_signals(
                df_pd["close"],
                entries,
                exits,
                init_cash=initial_capital,
                fees=0.001,  # 0.1% díj
                freq=timeframe,  # pl. '1m', '1h'
            )

            # 5. Eredmények csomagolása
            stats_dict: dict[str, Any] = pf.stats().to_dict()
            equity_array = pf.value()
            if hasattr(equity_array, "tolist"):
                equity_array = equity_array.tolist()
            else:
                equity_array = list(equity_array)

            # HASZNÁLJUK A READABLE DATAFRAME-ET! (Ez stabilabb)
            trades_df_raw = pf.trades.records_readable

            trades_data: dict[str, int | list[float] | list[str]] = {
                "count": 0,
                "pnl": [],
                "duration": [],
                "entry_time": [],
                "exit_time": [],
            }
            if len(trades_df_raw) > 0:
                # Biztonságos oszlop elérés és típuskonverzió
                # PnL kezelés (Ha nincs PnL, akkor 0)
                pnl = (
                    trades_df_raw["PnL"].fillna(0.0).tolist()
                    if "PnL" in trades_df_raw.columns
                    else []
                )

                # Duration kezelés (Timedelta -> String, hogy a JSON ne haljon be)
                duration = []
                if "Duration" in trades_df_raw.columns:
                    duration = trades_df_raw["Duration"].astype(str).tolist()

                # Entry/Exit idők
                entry_time = (
                    trades_df_raw["Entry Timestamp"].astype(str).tolist()
                    if "Entry Timestamp" in trades_df_raw.columns
                    else []
                )
                exit_time = (
                    trades_df_raw["Exit Timestamp"].astype(str).tolist()
                    if "Exit Timestamp" in trades_df_raw.columns
                    else []
                )

                trades_data = {
                    "count": len(trades_df_raw),
                    "pnl": pnl,
                    "duration": duration,
                    "entry_time": entry_time,
                    "exit_time": exit_time,
                }

            # Signals konvertálása (marad a régi, az jó volt)
            entries_list = (
                [int(i) for i in entries.values] if hasattr(entries, "values") else list(entries)
            )
            exits_list = [int(i) for i in exits.values] if hasattr(exits, "values") else list(exits)

            return {
                "stats": stats_dict,
                "equity": equity_array,
                "trades": trades_data,  # Az új, biztonságos dict
                "signals": {"entries": entries_list, "exits": exits_list},
                "parameters": {
                    "symbol": symbol,
                    "date": date,
                    "timeframe": timeframe,
                    "fast_period": fast_period,
                    "slow_period": slow_period,
                    "initial_capital": initial_capital,
                },
            }
        except Exception as e:
            return {
                "error": f"Hiba a backtest futtatása közben: {str(e)}",
                "stats": {},
                "equity": [],
                "trades": [],
                "signals": {"entries": [], "exits": []},
            }

    async def analyze_market_structure(
        self, symbol: str, date: str, timeframe: str, df: "pl.DataFrame | None" = None
    ) -> "pl.DataFrame":
        """Piaci struktúra elemzése swing pontokkal és szintekkel.

        Ez a metódus a D2 dimenzió processor-t használja a swing pontok és
        piaci szintek kiszámítására az adott szimbólum adataiból.

        Args:
            symbol: A kereskedési szimbólum (pl. 'EURUSD')
            date: A dátum (pl. '2024-03-20')
            timeframe: Az időkeret (pl. '1m', '5m', '1h', '4h')
            df: Opcionális Polars DataFrame (ha None, akkor betölti get_candles-szel)

        Returns:
            pl.DataFrame: A feldolgozott DataFrame swing pontokkal és szintekkel
        """
        # 1. Adatok betöltése, ha nincs megadva
        if df is None:
            df = await self.get_candles(symbol, date, timeframe)

        if df is None or len(df) == 0:
            raise ValueError(
                f"Nincs elérhető adat a megadott paraméterekhez: {symbol}, {date}, {timeframe}"
            )

        # 2. Config és Logger lekérése a core_components-en keresztül
        config: ConfigManagerInterface = self._core_components.get_component("config")
        logger: LoggerInterface = self._core_components.get_component("logger")

        if config is None or logger is None:
            raise RuntimeError("Config vagy Logger komponens nem elérhető")

        self._logger.info(f"D2 elemzés indítása: {symbol} {timeframe}")

        # 3. D2 processor létrehozása Factory-n keresztül
        from neural_ai.processors.factory import create_dimension_processor

        processor = create_dimension_processor(dimension_id=2, config=config, logger=logger)

        # 4. D2 processzálás futtatása
        df_d2 = processor.process(df, timeframe=timeframe)

        return df_d2
