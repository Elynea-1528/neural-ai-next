# 04 - Adattárház (Data Warehouse)

## 🎯 Cél és Szándék

Ez a dokumentum definiálja a **Neural AI Next** Big Data tároló rendszerét, amely 25 évnyi Tick adatot képes particionált Parquet formátumban tárolni és gyorsan lekérdezni. A rendszer kizárólag a prémium instrumentumokra fókuszál: `EURUSD, GBPUSD, USDJPY, USDCHF, XAUUSD`.

**Filozófia:** *"Fast reads, efficient storage, easy querying"*

---

## 🏗️ Architektúra Áttekintés

### Tárolási Stratégia

```
/data/tick/
├── EURUSD/
│   ├── tick/
│   │   ├── year=2023/
│   │   │   ├── month=12/
│   │   │   │   ├── day=01/
│   │   │   │   │   └── data.parquet (10-50MB)
│   │   │   │   ├── day=02/
│   │   │   │   └── ...
│   │   │   └── year=2024/
│   │   └── ...
├── GBPUSD/
├── USDJPY/
├── USDCHF/
└── XAUUSD/
```

### Partíció Előnyök

- **Gyors lekérdezés:** Dátum és szimbólum alapú szűrés
- **Hatékony tárolás:** Csak a szükséges adatok betöltése
- **Párhuzamos feldolgozás:** Több partíció egyszerre feldolgozható
- **Skálázhatóság:** Évek óta gyűjtött adatok kezelése

---

## 📦 Technológiai Stack

### Fő Függőségek

```python
# pyproject.toml
dependencies = [
    "fastparquet>=2023.4.0",
    "polars>=0.20.0",  # Gyorsabb mint Pandas
    "pyarrow>=14.0.0",
]
```

### Adatmodell

```python
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TickData(BaseModel):
    """Tick adat modell."""
    timestamp: datetime
    symbol: str
    bid: float
    ask: float
    volume: Optional[int] = None
    source: str  # 'jforex', 'mt5', 'ibkr'
    
    @property
    def spread(self) -> float:
        """Spread kiszámítása."""
        return self.ask - self.bid
    
    @property
    def mid_price(self) -> float:
        """Középár kiszámítása."""
        return (self.bid + self.ask) / 2
```

---

## 🗄️ ParquetStorageService

### Implementáció

```python
import polars as pl
from fastparquet import write, ParquetFile
from pathlib import Path
from typing import Optional, List
import asyncio

class ParquetStorageService:
    """Particionált Parquet tároló szolgáltatás."""
    
    BASE_PATH = Path("/data/tick")
    
    def __init__(self):
        self.engine = "fastparquet"
        self.compression = "snappy"
    
    def _get_path(
        self,
        symbol: str,
        date: datetime
    ) -> Path:
        """Elérési út generálása."""
        return (
            self.BASE_PATH /
            symbol /
            "tick" /
            f"year={date.year}" /
            f"month={date.month:02d}" /
            f"day={date.day:02d}" /
            "data.parquet"
        )
    
    async def store_tick_data(
        self,
        symbol: str,
        data: pl.DataFrame,
        date: datetime
    ) -> None:
        """Tick adatok tárolása."""
        path = self._get_path(symbol, date)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # Polars DataFrame -> Parquet
        data.write_parquet(
            path,
            compression=self.compression
        )
        
        logger.info(
            "tick_data_stored",
            symbol=symbol,
            date=date.isoformat(),
            rows=len(data),
            path=str(path)
        )
    
    async def read_tick_data(
        self,
        symbol: str,
        start_date: datetime,
        end_date: datetime
    ) -> pl.DataFrame:
        """Tick adatok olvasása dátumtartományból."""
        paths = []
        
        # Összes releváns fájl megtalálása
        current_date = start_date
        while current_date <= end_date:
            path = self._get_path(symbol, current_date)
            if path.exists():
                paths.append(path)
            current_date += timedelta(days=1)
        
        if not paths:
            logger.warning(
                "no_data_found",
                symbol=symbol,
                start_date=start_date.isoformat(),
                end_date=end_date.isoformat()
            )
            return pl.DataFrame()
        
        # Adatok betöltése párhuzamosan
        dfs = await asyncio.gather(*[
            self._read_parquet_async(path)
            for path in paths
        ])
        
        # Összefűzés
        result = pl.concat(dfs)
        
        # Dátum szerinti szűrés (pontosabb)
        result = result.filter(
            (pl.col("timestamp") >= start_date) &
            (pl.col("timestamp") <= end_date)
        )
        
        logger.info(
            "tick_data_loaded",
            symbol=symbol,
            rows=len(result),
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat()
        )
        
        return result
    
    async def _read_parquet_async(self, path: Path) -> pl.DataFrame:
        """Aszinkron Parquet olvasás."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            pl.read_parquet,
            path
        )
    
    async def get_available_dates(
        self,
        symbol: str
    ) -> List[datetime]:
        """Elérhető dátumok lekérdezése."""
        symbol_path = self.BASE_PATH / symbol / "tick"
        
        if not symbol_path.exists():
            return []
        
        dates = []
        for year_dir in symbol_path.glob("year=*"):
            year = int(year_dir.name.split("=")[1])
            for month_dir in year_dir.glob("month=*"):
                month = int(month_dir.name.split("=")[1])
                for day_dir in month_dir.glob("day=*"):
                    day = int(day_dir.name.split("=")[1])
                    dates.append(datetime(year, month, day))
        
        return sorted(dates)
```

---

## 🔄 Resampler Service

### Tick -> OHLCV Konverzió

```python
import polars as pl
from datetime import datetime, timedelta

class ResamplerService:
    """Tick adatok átalakítása OHLCV formátumba."""
    
    def __init__(self, storage: ParquetStorageService):
        self.storage = storage
    
    async def resample_to_ohlcv(
        self,
        symbol: str,
        start_date: datetime,
        end_date: datetime,
        timeframe: str = "1m"
    ) -> pl.DataFrame:
        """Tick -> OHLCV átalakítás."""
        # Tick adatok betöltése
        ticks = await self.storage.read_tick_data(
            symbol,
            start_date,
            end_date
        )
        
        if len(ticks) == 0:
            return pl.DataFrame()
        
        # Középár számítása
        ticks = ticks.with_columns(
            mid_price=(pl.col("bid") + pl.col("ask")) / 2
        )
        
        # Resampling időalapú ablakokkal
        if timeframe == "1m":
            rule = "1m"
        elif timeframe == "5m":
            rule = "5m"
        elif timeframe == "1h":
            rule = "1h"
        elif timeframe == "1d":
            rule = "1d"
        else:
            raise ValueError(f"Unsupported timeframe: {timeframe}")
        
        # OHLCV aggregáció
        ohlcv = ticks.group_by_dynamic(
            "timestamp",
            every=rule,
            closed="left"
        ).agg([
            pl.col("mid_price").first().alias("open"),
            pl.col("mid_price").max().alias("high"),
            pl.col("mid_price").min().alias("low"),
            pl.col("mid_price").last().alias("close"),
            pl.col("volume").sum().alias("volume"),
        ])
        
        logger.info(
            "resample_completed",
            symbol=symbol,
            timeframe=timeframe,
            input_rows=len(ticks),
            output_rows=len(ohlcv)
        )
        
        return ohlcv
    
    async def resample_for_vectorbt(
        self,
        symbol: str,
        start_date: datetime,
        end_date: datetime,
        timeframes: List[str] = ["1m", "5m", "1h"]
    ) -> Dict[str, pl.DataFrame]:
        """Több időkeretre való resampling VectorBT számára."""
        results = {}
        
        for tf in timeframes:
            results[tf] = await self.resample_to_ohlcv(
                symbol,
                start_date,
                end_date,
                tf
            )
        
        return results
```

---

## 🔍 Adatminőség és Validáció

### Data Quality Checks

```python
class DataQualityService:
    """Adatminőség ellenőrző szolgáltatás."""
    
    @staticmethod
    def validate_tick_data(df: pl.DataFrame) -> Dict[str, Any]:
        """Tick adatok validálása."""
        report = {
            "total_rows": len(df),
            "duplicates": 0,
            "nulls": {},
            "outliers": {},
            "gaps": []
        }
        
        # Duplikátumok ellenőrzése
        duplicates = df.select(
            pl.col("timestamp").is_duplicated().sum()
        ).item()
        report["duplicates"] = duplicates
        
        # Null értékek ellenőrzése
        for col in ["bid", "ask", "timestamp"]:
            null_count = df.select(
                pl.col(col).is_null().sum()
            ).item()
            report["nulls"][col] = null_count
        
        # Outlier detektálás (3 szigma szabály)
        if len(df) > 0:
            bid_mean = df.select(pl.col("bid").mean()).item()
            bid_std = df.select(pl.col("bid").std()).item()
            
            outliers = df.filter(
                (pl.col("bid") > bid_mean + 3 * bid_std) |
                (pl.col("bid") < bid_mean - 3 * bid_std)
            )
            report["outliers"]["bid"] = len(outliers)
        
        # Időbeli hézagok ellenőrzése
        if len(df) > 1:
            df_sorted = df.sort("timestamp")
            time_diffs = df_sorted.select(
                pl.col("timestamp").diff().alias("diff")
            )
            
            # Túl nagy időbeli különbségek
            gaps = time_diffs.filter(
                pl.col("diff") > pl.duration(minutes=5)
            )
            report["gaps"] = gaps.select("timestamp").to_series().to_list()
        
        return report
    
    @staticmethod
    def clean_tick_data(df: pl.DataFrame) -> pl.DataFrame:
        """Tick adatok tisztítása."""
        # Duplikátumok eltávolítása
        df = df.unique(subset=["timestamp"], keep="first")
        
        # Null értékek eltávolítása
        df = df.drop_nulls(subset=["bid", "ask", "timestamp"])
        
        # Rendezés idő szerint
        df = df.sort("timestamp")
        
        return df
```

---

## 📊 Teljesítmény Optimalizáció

### Chunking és Streamelés

```python
class ChunkedStorageService:
    """Nagy adathalmazok chunkolva történő tárolása."""
    
    CHUNK_SIZE = 100_000  # 100k tick per chunk
    
    async def store_large_tick_dataset(
        self,
        symbol: str,
        data: pl.DataFrame,
        start_date: datetime
    ) -> None:
        """Nagy adathalmaz tárolása chunkokban."""
        total_rows = len(data)
        num_chunks = (total_rows // self.CHUNK_SIZE) + 1
        
        logger.info(
            "large_dataset_storage_started",
            symbol=symbol,
            total_rows=total_rows,
            chunk_size=self.CHUNK_SIZE,
            num_chunks=num_chunks
        )
        
        for i in range(num_chunks):
            start_idx = i * self.CHUNK_SIZE
            end_idx = min((i + 1) * self.CHUNK_SIZE, total_rows)
            
            chunk = data[start_idx:end_idx]
            
            # Dátum meghatározása a chunk első eleméből
            chunk_date = chunk[0, "timestamp"]
            
            await self.storage.store_tick_data(
                symbol,
                chunk,
                chunk_date
            )
            
            logger.debug(
                "chunk_stored",
                chunk_index=i,
                rows=len(chunk)
            )
        
        logger.info(
            "large_dataset_storage_completed",
            symbol=symbol,
            total_rows=total_rows
        )
```

### Predicate Pushdown

```python
# Polars automatikusan alkalmazza a predicate pushdown-ot
# Csak a szükséges partíciók és sorok lesznek betöltve

# Példa: Gyors lekérdezés csak bizonyos órákra
morning_ticks = await storage.read_tick_data(
    symbol="EURUSD",
    start_date=datetime(2023, 12, 23, 8, 0),
    end_date=datetime(2023, 12, 23, 12, 0)
)

# Polars csak a 2023-12-23 nap adatait tölti be
# és utána szűri az időintervallumra
```

---

## 🔐 Biztonság és Integritás

### Adatbiztonság

```python
import hashlib

class DataIntegrityService:
    """Adatintegritás ellenőrző."""
    
    @staticmethod
    def calculate_checksum(df: pl.DataFrame) -> str:
        """DataFrame checksum számítása."""
        # Csak a fontos oszlopok alapján
        data_str = df.select(["timestamp", "bid", "ask"]).to_csv()
        return hashlib.sha256(data_str.encode()).hexdigest()
    
    @staticmethod
    async def verify_data_integrity(
        symbol: str,
        date: datetime
    ) -> bool:
        """Adatintegritás ellenőrzése."""
        path = storage._get_path(symbol, date)
        
        if not path.exists():
            return False
        
        try:
            # Parquet fájl ellenőrzése
            df = pl.read_parquet(path)
            
            # Alapvető ellenőrzések
            assert len(df) > 0, "Empty dataframe"
            assert "timestamp" in df.columns
            assert "bid" in df.columns
            assert "ask" in df.columns
            
            # Rendezés ellenőrzése
            assert df["timestamp"].is_sorted(), "Data not sorted"
            
            logger.info(
                "data_integrity_verified",
                symbol=symbol,
                date=date.isoformat(),
                rows=len(df)
            )
            
            return True
            
        except Exception as e:
            logger.error(
                "data_integrity_check_failed",
                symbol=symbol,
                date=date.isoformat(),
                error=str(e)
            )
            return False
```

---

## 📋 Következő Lépések

1. **Collectorok:** Lásd [`05_collectors_strategy.md`](05_collectors_strategy.md)

---

## 🔗 Kapcsolódó Dokumentumok

- [Rendszerarchitektúra](01_system_architecture.md)
- [Dinamikus Konfiguráció](02_dynamic_configuration.md)
- [Megfigyelhetőség](03_observability_logging.md)
- [Fejlesztési Útmutató](docs/development/unified_development_guide.md)