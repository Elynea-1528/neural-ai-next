#!/usr/bin/env python3
"""Batch historikus adatgyűjtés indítása minden szimbólumra és időkeretre
Ez a script kihasználja az MT5 által engedélyezett összes historikus adatot
"""

import argparse
import logging
import time
from datetime import datetime, timedelta

import requests

# Konfiguráció
SYMBOLS = ["EURUSD", "GBPUSD", "USDJPY", "XAUUSD"]
TIMEFRAMES = ["M1", "M5", "M15", "H1", "H4", "D1"]
COLLECTOR_API = "http://localhost:8000"


class HistoricalDataCollector:
    """Batch historikus adatgyűjtő"""

    def __init__(self, api_url: str = COLLECTOR_API):
        self.api_url = api_url
        self.logger = self._setup_logger()

    def _setup_logger(self):
        """Logger beállítása"""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
        return logging.getLogger(__name__)

    def get_max_available_dates(self, symbol: str, timeframe: str) -> dict[str, str]:
        """Megpróbálja meghatározni az MT5 által engedélyezett maximális dátumtartományt

        Stratégia:
        1. Először próbálkozzunk 2023.04.11-től (ez a felhasználó által megadott dátum)
        2. Ha nem, akkor próbálkozzunk 1 évvel
        3. Ha az sem, akkor 6 hónappal
        """
        current_date = datetime.now()

        # Próbálkozási dátumok (legtől lefelé)
        attempts = [
            ("2023.04.11-től", datetime(2023, 4, 11)),
            ("1 év", current_date - timedelta(days=1 * 365)),
            ("6 hónap", current_date - timedelta(days=180)),
            ("3 hónap", current_date - timedelta(days=90)),
        ]

        for label, start_date in attempts:
            try:
                # Próbáljunk ki egy kisebb batch-et (pl. 30 nap)
                test_end_date = start_date + timedelta(days=30)

                response = requests.post(
                    f"{self.api_url}/api/v1/historical/request",
                    json={
                        "symbol": symbol,
                        "timeframe": timeframe,
                        "start_date": start_date.strftime("%Y-%m-%d"),
                        "end_date": test_end_date.strftime("%Y-%m-%d"),
                        "batch_size": 99000,
                        "priority": "test",
                    },
                    timeout=10,
                )

                if response.status_code == 200:
                    self.logger.info(f"✅ {symbol}/{timeframe}: {label} elérhető")
                    return {
                        "start_date": start_date.strftime("%Y-%m-%d"),
                        "end_date": current_date.strftime("%Y-%m-%d"),
                        "label": label,
                    }

            except Exception as e:
                self.logger.warning(f"⚠️ {symbol}/{timeframe}: {label} sikertelen - {e}")
                continue

        # Ha semmi sem működik, akkor próbálkozzunk a lehető legrövidebbel
        self.logger.warning(
            f"⚠️ {symbol}/{timeframe}: Minden próbálkozás sikertelen, 30 napot próbálunk"
        )
        return {
            "start_date": (current_date - timedelta(days=30)).strftime("%Y-%m-%d"),
            "end_date": current_date.strftime("%Y-%m-%d"),
            "label": "30 nap",
        }

    def start_historical_job(
        self, symbol: str, timeframe: str, start_date: str, end_date: str
    ) -> str:
        """Historikus adatgyűjtési job indítása"""
        try:
            response = requests.post(
                f"{self.api_url}/api/v1/historical/request",
                json={
                    "symbol": symbol,
                    "timeframe": timeframe,
                    "start_date": start_date,
                    "end_date": end_date,
                    "batch_size": 99000,  # 99,000 gyertya per batch
                    "priority": "high",
                },
                timeout=30,
            )

            if response.status_code == 200:
                result = response.json()
                job_id = result["job_id"]
                self.logger.info(f"✅ {symbol}/{timeframe}: Job elindítva - {job_id}")
                return job_id
            else:
                self.logger.error(f"❌ {symbol}/{timeframe}: Hiba - {response.status_code}")
                return None

        except Exception as e:
            self.logger.error(f"❌ {symbol}/{timeframe}: Kivétel - {e}")
            return None

    def start_all_collections(self, max_attempts: bool = True):
        """Összes szimbólum és időkeret kombinációjának indítása"""
        jobs = []
        total_combinations = len(SYMBOLS) * len(TIMEFRAMES)
        current_combination = 0

        self.logger.info("=" * 80)
        self.logger.info("BATCH HISTORIKUS ADATGYŰJTÉS INDÍTÁSA")
        self.logger.info("=" * 80)
        self.logger.info(f"Szimbólumok: {len(SYMBOLS)}")
        self.logger.info(f"Időkeretek: {len(TIMEFRAMES)}")
        self.logger.info(f"Összes kombináció: {total_combinations}")
        self.logger.info("=" * 80)

        for symbol in SYMBOLS:
            for timeframe in TIMEFRAMES:
                current_combination += 1

                self.logger.info(
                    f"\n[{current_combination}/{total_combinations}] {symbol}/{timeframe}"
                )
                self.logger.info("-" * 80)

                # Maximális dátumtartomány meghatározása
                if max_attempts:
                    date_range = self.get_max_available_dates(symbol, timeframe)
                    start_date = date_range["start_date"]
                    end_date = date_range["end_date"]
                    label = date_range["label"]

                    self.logger.info(f"Maximális elérhető tartomány: {label}")
                    self.logger.info(f"Start date: {start_date}")
                    self.logger.info(f"End date: {end_date}")
                else:
                    # Ha nem akarjuk tesztelni, akkor 2023.04.11-től
                    start_date = "2023-04-11"
                    end_date = datetime.now().strftime("%Y-%m-%d")
                    self.logger.info("Adatgyűjtés 2023.04.11-től")

                # Job indítása
                job_id = self.start_historical_job(symbol, timeframe, start_date, end_date)

                if job_id:
                    jobs.append(
                        {
                            "job_id": job_id,
                            "symbol": symbol,
                            "timeframe": timeframe,
                            "start_date": start_date,
                            "end_date": end_date,
                        }
                    )

                    # Várjunk egy kicsit, ne terheljük túl a rendszert
                    time.sleep(2)
                else:
                    self.logger.error(f"❌ {symbol}/{timeframe}: Nem sikerült elindítani")

        # Összefoglalás
        self.logger.info("\n" + "=" * 80)
        self.logger.info("ÖSSZEFOGLALÁS")
        self.logger.info("=" * 80)
        self.logger.info(f"Elindított job-ok: {len(jobs)}/{total_combinations}")
        self.logger.info(f"Sikeres: {len(jobs)}")
        self.logger.info(f"Sikertelen: {total_combinations - len(jobs)}")
        self.logger.info("=" * 80)

        # Job-ok listájának mentése
        if jobs:
            with open("historical_jobs.txt", "w") as f:
                f.write("Historikus adatgyűjtési job-ok\n")
                f.write("=" * 80 + "\n\n")
                for job in jobs:
                    f.write(f"Job ID: {job['job_id']}\n")
                    f.write(f"Symbol: {job['symbol']}\n")
                    f.write(f"Timeframe: {job['timeframe']}\n")
                    f.write(f"Start: {job['start_date']}\n")
                    f.write(f"End: {job['end_date']}\n")
                    f.write("-" * 80 + "\n")

            self.logger.info("Job-ok listája elmentve: historical_jobs.txt")

        return jobs


def main():
    """Főprogram"""
    parser = argparse.ArgumentParser(description="Batch historikus adatgyűjtés indítása")
    parser.add_argument(
        "--no-max-attempts",
        action="store_true",
        help="Ne próbálja meg meghatározni a maximális dátumtartományt, csak 1 év adatot gyűjtsön",
    )
    parser.add_argument(
        "--api-url",
        default=COLLECTOR_API,
        help=f"Kollektor API URL (alapértelmezett: {COLLECTOR_API})",
    )

    args = parser.parse_args()

    # Kollektor létrehozása
    collector = HistoricalDataCollector(api_url=args.api_url)

    # Adatgyűjtés indítása
    jobs = collector.start_all_collections(max_attempts=not args.no_max_attempts)

    if jobs:
        print(f"\n✅ {len(jobs)} job elindítva!")
        print("A job-ok állapotát a következő paranccsal követheted:")
        print("python scripts/log_viewer.py")
    else:
        print("\n❌ Nem sikerült elindítani egy job-ot sem!")
        print("Ellenőrizd, hogy fut-e a kollektor!")


if __name__ == "__main__":
    main()
