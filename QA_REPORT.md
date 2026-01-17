# NEURAL AI NEXT - QA REPORT
## 1. Pylance / Ruff Hibák (Static Analysis)
```
E501 Line too long (111 > 100)
   --> neural_ai/core/base/factory.py:424:101
    |
422 |         config_manager = ConfigManagerFactory.get_manager("config.yml")  # fallback
423 |         event_bus = EventBusFactory.get_event_bus(logger=logger)
424 |         return FileStorage(logger=logger, config=config_manager, event_bus=event_bus, base_path=base_directory)
    |                                                                                                     ^^^^^^^^^^^
    |

D107 Missing docstring in `__init__`
  --> neural_ai/core/events/factory.py:28:9
   |
26 |     """
27 |
28 |     def __init__(self, logger: "LoggerInterface", config_manager: "ConfigManagerInterface") -> None:
   |         ^^^^^^^^
29 |         self._logger = logger
30 |         self._config_manager = config_manager
   |

E501 Line too long (116 > 100)
  --> neural_ai/core/events/factory.py:94:101
   |
92 |             self._logger.debug("Konfigurációs adatok lekérdezve", data=data)
93 |         except (KeyError, ValueError) as e:
94 |             self._logger.warning("Konfigurációs szekció hiányzik, alapértelmezett értékek használata", error=str(e))
   |                                                                                                     ^^^^^^^^^^^^^^^^
95 |             data = {}
   |

D417 Missing argument description in the docstring for `__init__`: `logger`
  --> neural_ai/core/events/implementations/zeromq_bus.py:60:9
   |
58 |         return self._config
59 |
60 |     def __init__(self, config: EventBusConfig | None = None, logger: "LoggerInterface | None" = None) -> None:
   |         ^^^^^^^^
61 |         """Inicializálja az EventBus-t.
   |

E501 Line too long (110 > 100)
  --> neural_ai/core/events/implementations/zeromq_bus.py:60:101
   |
58 |         return self._config
59 |
60 |     def __init__(self, config: EventBusConfig | None = None, logger: "LoggerInterface | None" = None) -> None:
   |                                                                                                     ^^^^^^^^^^
61 |         """Inicializálja az EventBus-t.
   |

E501 Line too long (107 > 100)
  --> neural_ai/data/storage/implementations/file_storage.py:66:101
   |
64 |         self.event_bus = event_bus
65 |         self.storage_config = cast(StorageConfig, config.get("storage", {}) if config else {})
66 |         self._base_path = Path(base_path) if base_path else Path(self.storage_config.get("base_path", "."))
   |                                                                                                     ^^^^^^^
67 |         self._setup_format_handlers()
68 |         self._initialized = True
   |

E402 Module level import not at top of file
  --> neural_ai/data/storage/implementations/parquet_storage.py:27:1
   |
25 | """
26 |
27 | import asyncio
   | ^^^^^^^^^^^^^^
28 | import hashlib
29 | from collections.abc import Sequence
   |

E402 Module level import not at top of file
  --> neural_ai/data/storage/implementations/parquet_storage.py:28:1
   |
27 | import asyncio
28 | import hashlib
   | ^^^^^^^^^^^^^^
29 | from collections.abc import Sequence
30 | from datetime import datetime, timedelta
   |

E402 Module level import not at top of file
  --> neural_ai/data/storage/implementations/parquet_storage.py:29:1
   |
27 | import asyncio
28 | import hashlib
29 | from collections.abc import Sequence
   | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
30 | from datetime import datetime, timedelta
31 | from pathlib import Path
   |

E402 Module level import not at top of file
  --> neural_ai/data/storage/implementations/parquet_storage.py:30:1
   |
28 | import hashlib
29 | from collections.abc import Sequence
30 | from datetime import datetime, timedelta
   | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
31 | from pathlib import Path
32 | from typing import TYPE_CHECKING, Any, TypedDict, cast
   |

E402 Module level import not at top of file
  --> neural_ai/data/storage/implementations/parquet_storage.py:31:1
   |
29 | from collections.abc import Sequence
30 | from datetime import datetime, timedelta
31 | from pathlib import Path
   | ^^^^^^^^^^^^^^^^^^^^^^^^
32 | from typing import TYPE_CHECKING, Any, TypedDict, cast
   |

E402 Module level import not at top of file
  --> neural_ai/data/storage/implementations/parquet_storage.py:32:1
   |
30 | from datetime import datetime, timedelta
31 | from pathlib import Path
32 | from typing import TYPE_CHECKING, Any, TypedDict, cast
   | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
33 |
34 | from neural_ai.core.base.implementations.singleton import SingletonMeta
   |

E402 Module level import not at top of file
  --> neural_ai/data/storage/implementations/parquet_storage.py:34:1
   |
32 | from typing import TYPE_CHECKING, Any, TypedDict, cast
33 |
34 | from neural_ai.core.base.implementations.singleton import SingletonMeta
   | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
35 | from neural_ai.core.utils.decorators import trace
36 | from neural_ai.data.storage.exceptions import StorageIOError, StorageNotFoundError
   |

E402 Module level import not at top of file
  --> neural_ai/data/storage/implementations/parquet_storage.py:35:1
   |
34 | from neural_ai.core.base.implementations.singleton import SingletonMeta
35 | from neural_ai.core.utils.decorators import trace
   | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
36 | from neural_ai.data.storage.exceptions import StorageIOError, StorageNotFoundError
37 | from neural_ai.data.storage.interfaces.storage_interface import StorageInterface
   |

E402 Module level import not at top of file
  --> neural_ai/data/storage/implementations/parquet_storage.py:36:1
   |
34 | from neural_ai.core.base.implementations.singleton import SingletonMeta
35 | from neural_ai.core.utils.decorators import trace
36 | from neural_ai.data.storage.exceptions import StorageIOError, StorageNotFoundError
   | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
37 | from neural_ai.data.storage.interfaces.storage_interface import StorageInterface
   |

E402 Module level import not at top of file
  --> neural_ai/data/storage/implementations/parquet_storage.py:37:1
   |
35 | from neural_ai.core.utils.decorators import trace
36 | from neural_ai.data.storage.exceptions import StorageIOError, StorageNotFoundError
37 | from neural_ai.data.storage.interfaces.storage_interface import StorageInterface
   | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
38 |
39 | if TYPE_CHECKING:
   |

E501 Line too long (114 > 100)
   --> neural_ai/data/storage/implementations/parquet_storage.py:122:101
    |
120 |         self.event_bus = event_bus
121 |         self.storage_config = cast(StorageConfig, config.get("storage", {}) if config else {})
122 |         self.BASE_PATH = Path(base_path) if base_path else Path(self.storage_config.get("base_path", "data/tick"))
    |                                                                                                     ^^^^^^^^^^^^^^
123 |         self.engine = self.storage_config.get("engine", "fastparquet")
124 |         self.compression = compression or self.storage_config.get("compression", "snappy")
    |

D417 Missing argument descriptions in the docstring for `get_storage`: `config`, `event_bus`
  --> neural_ai/data/storage/interfaces/factory_interface.py:47:9
   |
45 |     @classmethod
46 |     @abstractmethod
47 |     def get_storage(
   |         ^^^^^^^^^^^
48 |         cls,
49 |         logger: "LoggerInterface",
   |

E501 Line too long (124 > 100)
  --> neural_ai/processors/dimensions/d01_price/processor.py:60:101
   |
58 |         market_hours_config = self.dim_config.get("market_hours", {})
59 |         if market_hours_config.get("enabled", False):
60 |             enabled_weekdays = market_hours_config.get("weekdays", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
   |                                                                                                     ^^^^^^^^^^^^^^^^^^^^^^^^
61 |             hours_range = market_hours_config.get("hours", ["00:00", "23:59"])
62 |             timezone = market_hours_config.get("timezone", "UTC")
   |

F841 Local variable `timezone` is assigned to but never used
  --> neural_ai/processors/dimensions/d01_price/processor.py:62:13
   |
60 |             enabled_weekdays = market_hours_config.get("weekdays", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
61 |             hours_range = market_hours_config.get("hours", ["00:00", "23:59"])
62 |             timezone = market_hours_config.get("timezone", "UTC")
   |             ^^^^^^^^
63 |
64 |             # Számoljuk a market hours-on kívüli sorokat
   |
help: Remove assignment to unused variable `timezone`

E501 Line too long (119 > 100)
  --> neural_ai/processors/dimensions/d01_price/processor.py:69:101
   |
67 |                 # Polars expr a market hours ellenőrzéshez
68 |                 weekday_expr = pl.col("timestamp").dt.weekday().replace_strict(
69 |                     {1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday", 7: "Sunday"}
   |                                                                                                     ^^^^^^^^^^^^^^^^^^^
70 |                 ).is_in(enabled_weekdays)
   |

E501 Line too long (105 > 100)
  --> neural_ai/processors/dimensions/d01_price/processor.py:79:101
   |
78 |                 time_minutes = pl.col("timestamp").dt.hour() * 60 + pl.col("timestamp").dt.minute()
79 |                 time_in_range = (time_minutes >= start_time_minutes) & (time_minutes <= end_time_minutes)
   |                                                                                                     ^^^^^
80 |
81 |                 market_hours_mask = weekday_expr & time_in_range
   |

E501 Line too long (124 > 100)
  --> neural_ai/processors/dimensions/d01_price/processor.py:82:101
   |
81 |                 market_hours_mask = weekday_expr & time_in_range
82 |                 outside_market_hours_count = df.select((~market_hours_mask).sum().alias("outside")).select("outside").item()
   |                                                                                                     ^^^^^^^^^^^^^^^^^^^^^^^^
83 |
84 |                 if outside_market_hours_count > 0 and market_hours_config.get("log_filtering", False):
   |

E501 Line too long (102 > 100)
  --> neural_ai/processors/dimensions/d01_price/processor.py:84:101
   |
82 |                 outside_market_hours_count = df.select((~market_hours_mask).sum().alias("outside")).select("outside").item()
83 |
84 |                 if outside_market_hours_count > 0 and market_hours_config.get("log_filtering", False):
   |                                                                                                     ^^
85 |                     self.logger.info(
86 |                         "Market hours szűrés eredménye",
   |

E501 Line too long (124 > 100)
   --> neural_ai/processors/dimensions/d02_support/implementations/support_processor.py:332:101
    |
330 |         market_hours_config = self.dim_config.get("market_hours", {})
331 |         if market_hours_config.get("enabled", False):
332 |             enabled_weekdays = market_hours_config.get("weekdays", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
    |                                                                                                     ^^^^^^^^^^^^^^^^^^^^^^^^
333 |             hours_range = market_hours_config.get("hours", ["00:00", "23:59"])
334 |             timezone = market_hours_config.get("timezone", "UTC")
    |

F841 Local variable `timezone` is assigned to but never used
   --> neural_ai/processors/dimensions/d02_support/implementations/support_processor.py:334:13
    |
332 |             enabled_weekdays = market_hours_config.get("weekdays", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
333 |             hours_range = market_hours_config.get("hours", ["00:00", "23:59"])
334 |             timezone = market_hours_config.get("timezone", "UTC")
    |             ^^^^^^^^
335 |
336 |             # Számoljuk a market hours-on kívüli sorokat
    |
help: Remove assignment to unused variable `timezone`

E501 Line too long (119 > 100)
   --> neural_ai/processors/dimensions/d02_support/implementations/support_processor.py:341:101
    |
339 |                 # Polars expr a market hours ellenőrzéshez
340 |                 weekday_expr = pl.col("timestamp").dt.weekday().replace_strict(
341 |                     {1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday", 7: "Sunday"}
    |                                                                                                     ^^^^^^^^^^^^^^^^^^^
342 |                 ).is_in(enabled_weekdays)
    |

E501 Line too long (105 > 100)
   --> neural_ai/processors/dimensions/d02_support/implementations/support_processor.py:351:101
    |
350 |                 time_minutes = pl.col("timestamp").dt.hour() * 60 + pl.col("timestamp").dt.minute()
351 |                 time_in_range = (time_minutes >= start_time_minutes) & (time_minutes <= end_time_minutes)
    |                                                                                                     ^^^^^
352 |
353 |                 market_hours_mask = weekday_expr & time_in_range
    |

E501 Line too long (124 > 100)
   --> neural_ai/processors/dimensions/d02_support/implementations/support_processor.py:354:101
    |
353 |                 market_hours_mask = weekday_expr & time_in_range
354 |                 outside_market_hours_count = df.select((~market_hours_mask).sum().alias("outside")).select("outside").item()
    |                                                                                                     ^^^^^^^^^^^^^^^^^^^^^^^^
355 |
356 |                 if outside_market_hours_count > 0 and market_hours_config.get("log_filtering", False):
    |

E501 Line too long (102 > 100)
   --> neural_ai/processors/dimensions/d02_support/implementations/support_processor.py:356:101
    |
354 |                 outside_market_hours_count = df.select((~market_hours_mask).sum().alias("outside")).select("outside").item()
355 |
356 |                 if outside_market_hours_count > 0 and market_hours_config.get("log_filtering", False):
    |                                                                                                     ^^
357 |                     self.logger.info(
358 |                         "Market hours szűrés eredménye",
    |

E501 Line too long (113 > 100)
   --> neural_ai/ui/pages/05_🪲_Strategy_Lab.py:270:101
    |
268 |             logger = self._bridge.get_component("logger")
269 |             if logger:
270 |                 logger.error("Backtest eredmény renderelés hiba", extra={"error": str(e), "page": "StrategyLab"})
    |                                                                                                     ^^^^^^^^^^^^^
271 |
272 |     def _prepare_data_for_view(self, df: "pl.DataFrame", price_type: str) -> "pl.DataFrame":
    |

E501 Line too long (104 > 100)
   --> neural_ai/ui/pages/05_🪲_Strategy_Lab.py:483:101
    |
481 |             if "nearest_resistance" in df_plot.columns and "resistance_strength" in df_plot.columns:
482 |                 # Unique resistance szintek gyűjtése strength-szel
483 |                 resistance_levels = df_plot.dropna(subset=["nearest_resistance", "resistance_strength"])
    |                                                                                                     ^^^^
484 |                 if not resistance_levels.empty:
485 |                     unique_resistances = (
    |

E501 Line too long (101 > 100)
   --> neural_ai/ui/pages/05_🪲_Strategy_Lab.py:558:101
    |
556 |             logger = self._bridge.get_component("logger")
557 |             if logger:
558 |                 logger.error("Chart renderelés hiba", extra={"error": str(e), "page": "StrategyLab"})
    |                                                                                                     ^
559 |
560 |     def _render_data_table(self) -> None:
    |

E501 Line too long (106 > 100)
   --> neural_ai/ui/pages/05_🪲_Strategy_Lab.py:617:101
    |
615 |             logger = self._bridge.get_component("logger")
616 |             if logger:
617 |                 logger.error("Data table renderelés hiba", extra={"error": str(e), "page": "StrategyLab"})
    |                                                                                                     ^^^^^^
618 |
619 |     def _get_symbols(self) -> list[str]:
    |

D101 Missing docstring in public class
  --> scripts/install.py:46:7
   |
45 | # Színek a konzolhoz
46 | class Colors:
   |       ^^^^^^
47 |     RED = "\033[0;31m"
48 |     GREEN = "\033[0;32m"
   |

E501 Line too long (121 > 100)
   --> scripts/install.py:591:101
    |
589 |     if gpu_available:
590 |         print(
591 |             "  python -c \"import torch; print(f'PyTorch: {torch.__version__}, CUDA: {torch.cuda.get_device_name(0)}')\""
    |                                                                                                     ^^^^^^^^^^^^^^^^^^^^^
592 |         )
593 |     else:
    |

E501 Line too long (108 > 100)
  --> scripts/migrate_structure.py:56:101
   |
55 |                 if dest_path.exists():
56 |                     logger.warning("Célútvonal már létezik, átugrás", source=str(item), dest=str(dest_path))
   |                                                                                                     ^^^^^^^^
57 |                     continue
   |

E501 Line too long (101 > 100)
  --> scripts/migrate_structure.py:61:101
   |
59 |                 if item.is_file():
60 |                     shutil.move(str(item), str(dest_path))
61 |                     logger.debug("Fájl áthelyezve", file=str(item.name), symbol=str(symbol_dir.name))
   |                                                                                                     ^
62 |                 elif item.is_dir():
63 |                     shutil.move(str(item), str(dest_path))
   |

E501 Line too long (101 > 100)
  --> scripts/migrate_structure.py:64:101
   |
62 |                 elif item.is_dir():
63 |                     shutil.move(str(item), str(dest_path))
64 |                     logger.debug("Mappa áthelyezve", dir=str(item.name), symbol=str(symbol_dir.name))
   |                                                                                                     ^
65 |
66 |             # Törölje az üres tick almappát
   |

E501 Line too long (137 > 100)
  --> scripts/migrate_structure.py:71:101
   |
69 | …ve", symbol=str(symbol_dir.name))
70 | …
71 | …s migráció után", symbol=str(symbol_dir.name), remaining=list(tick_subdir.iterdir()))
   |                                                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
72 | …
73 | …
   |

E501 Line too long (103 > 100)
   --> scripts/smart_pack.py:183:101
    |
182 |         # Ellenőrizzük, hogy az útvonal bármely része (mappa) tiltólistás-e
183 |         # Ez pontosabb, mint a string 'in', mert pl. a "data_loader.py" nem akad fenn a "data" tiltáson
    |                                                                                                     ^^^
184 |         for part in rel_path.parts:
185 |             if part in IGNORE_DIRS:
    |

C414 Unnecessary `list()` call within `sorted()`
   --> scripts/smart_pack.py:224:20
    |
223 |     # Egyedi lista, rendezve
224 |     unique_files = sorted(list(set(all_files)))
    |                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
225 |     count = 0
    |
help: Remove the inner `list()` call

E501 Line too long (116 > 100)
   --> scripts/test_d2_standalone.py:98:101
    |
 97 |         # Ellenőrizzük, hogy az új függvények léteznek
 98 |         assert hasattr(processor, '_find_swing_points_close_open'), "Hiányzó _find_swing_points_close_open függvény"
    |                                                                                                     ^^^^^^^^^^^^^^^^
 99 |         assert hasattr(processor, '_find_swing_points_high_low'), "Hiányzó _find_swing_points_high_low függvény"
100 |         assert hasattr(processor, '_merge_levels'), "Hiányzó _merge_levels függvény"
    |

E501 Line too long (112 > 100)
   --> scripts/test_d2_standalone.py:99:101
    |
 97 |         # Ellenőrizzük, hogy az új függvények léteznek
 98 |         assert hasattr(processor, '_find_swing_points_close_open'), "Hiányzó _find_swing_points_close_open függvény"
 99 |         assert hasattr(processor, '_find_swing_points_high_low'), "Hiányzó _find_swing_points_high_low függvény"
    |                                                                                                     ^^^^^^^^^^^^
100 |         assert hasattr(processor, '_merge_levels'), "Hiányzó _merge_levels függvény"
101 |         print("   ✅ Új függvények ellenőrizve")
    |

F841 Local variable `storage` is assigned to but never used
  --> scripts/test_tick_pipeline.py:28:9
   |
26 |         config = _create_mock_config()
27 |         logger = _create_mock_logger()
28 |         storage = _create_mock_storage()
   |         ^^^^^^^
29 |
30 |         print("✅ Mock komponensek létrehozva")
   |
help: Remove assignment to unused variable `storage`

E501 Line too long (115 > 100)
   --> scripts/test_tick_pipeline.py:120:101
    |
120 | def _validate_resample(tick_data: "pl.DataFrame", config: dict[str, Any], logger: Any) -> Optional["pl.DataFrame"]:
    |                                                                                                     ^^^^^^^^^^^^^^^
121 |     """Resample komponens validációja.
    |

E501 Line too long (103 > 100)
   --> scripts/test_tick_pipeline.py:166:101
    |
166 | def _validate_d1_processor(resample_data: "pl.DataFrame", config: dict[str, Any], logger: Any) -> bool:
    |                                                                                                     ^^^
167 |     """D1 Dimension Processor validációja.
    |

B905 `zip()` without an explicit `strict=` parameter
  --> tests/collectors/jforex/test_bi5_downloader.py:58:44
   |
56 |         """
57 |         data = b""
58 |         for delta, ask_price, bid_price in zip(timestamps_delta, ask, bid):
   |                                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
59 |             data += struct.pack(">III", delta, ask_price, bid_price)
   |
help: Add explicit value for parameter `strict=`

B905 `zip()` without an explicit `strict=` parameter
  --> tests/collectors/jforex/test_bi5_downloader.py:84:68
   |
82 |           """
83 |           data = b""
84 |           for delta, ask_price, bid_price, ask_volume, bid_volume in zip(
   |  ____________________________________________________________________^
85 | |             timestamps_delta, ask, bid, ask_vol, bid_vol
86 | |         ):
   | |_________^
87 |               data += struct.pack(">IIIff", delta, ask_price, bid_price, ask_volume, bid_volume)
   |
help: Add explicit value for parameter `strict=`

E501 Line too long (118 > 100)
   --> tests/collectors/jforex/test_bi5_downloader.py:425:101
    |
423 |     def test_validate_bi5_data_20_byte_format(self, downloader):
424 |         """Test validation of valid 20-byte format data."""
425 |         bi5_data = self.create_bi5_data_20_byte([0, 1000], [112345, 112346], [112340, 112341], [1.5, 2.0], [1.2, 1.8])
    |                                                                                                     ^^^^^^^^^^^^^^^^^^
426 |
427 |         assert downloader.validate_bi5_data(bi5_data) is True
    |

E501 Line too long (101 > 100)
   --> tests/collectors/jforex/test_live_feed.py:242:101
    |
240 |     ) -> JForexLiveFeed:
241 |         """JForexLiveFeed példány létrehozása üres configgal."""
242 |         return JForexLiveFeed(logger=mock_logger, event_bus=mock_event_bus, config=mock_config_empty)
    |                                                                                                     ^
243 |
244 |     def test_init_with_empty_config_logs_warning(
    |

E501 Line too long (105 > 100)
   --> tests/collectors/jforex/test_live_feed.py:249:101
    |
247 |         """Teszteli, hogy üres config esetén warning log jelenik meg."""
248 |         # Az inicializálás során warningnak kell lennie
249 |         mock_logger.warning.assert_called_once_with("jforex_live_config_missing - Using defaults (5555)")
    |                                                                                                     ^^^^^
250 |
251 |     @pytest.fixture
    |

E501 Line too long (105 > 100)
   --> tests/collectors/jforex/test_live_feed.py:271:101
    |
269 |     ) -> JForexLiveFeed:
270 |         """JForexLiveFeed példány létrehozása config adatokkal."""
271 |         return JForexLiveFeed(logger=mock_logger, event_bus=mock_event_bus, config=mock_config_with_data)
    |                                                                                                     ^^^^^
272 |
273 |     def test_init_with_config_logs_debug(
    |

B017 Do not assert blind exception: `Exception`
   --> tests/core/base/implementations/test_di_container.py:268:14
    |
266 |         container.register("singleton_comp", instance1)
267 |
268 |         with pytest.raises(Exception):  # SingletonViolationError
    |              ^^^^^^^^^^^^^^^^^^^^^^^^
269 |             container.register("singleton_comp", instance2)
    |

E501 Line too long (101 > 100)
   --> tests/core/base/test_factory.py:215:101
    |
213 |         self, mock_get_logger: MagicMock, mock_get_manager: MagicMock
214 |     ) -> None:
215 |         """Teszteli a minimális komponensek létrehozását config fájllal, de logger section nélkül."""
    |                                                                                                     ^
216 |         mock_config = MagicMock()
217 |         mock_config.get_section.return_value = None  # No logger section
    |

E501 Line too long (130 > 100)
   --> tests/core/base/test_factory.py:272:101
    |
270 |     @patch("neural_ai.core.logger.factory.LoggerFactory.get_logger")
271 |     @patch("neural_ai.core.config.factory.ConfigManagerFactory.get_manager")
272 |     def test_create_storage(self, mock_get_manager: MagicMock, mock_get_logger: MagicMock, mock_get_event_bus: MagicMock) -> None:
    |                                                                                                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
273 |         """Teszteli a storage létrehozását."""
274 |         mock_config = MagicMock()
    |

E501 Line too long (106 > 100)
   --> tests/core/config/implementations/test_dynamic_config_manager_comprehensive.py:265:101
    |
263 |     @pytest.mark.asyncio
264 |     async def test_add_and_remove_listener_logging(self) -> None:
265 |         """Teszteli a debug logolást az add_listener és remove_listener metódusokban (296, 308. sorok)."""
    |                                                                                                     ^^^^^^
266 |         mock_session = MagicMock(spec=AsyncSession)
267 |         mock_logger = MagicMock()
    |

E501 Line too long (112 > 100)
   --> tests/core/config/implementations/test_yaml_config_manager.py:821:101
    |
819 |         # Most próbáljunk beágyazott kulcsot beállítani
820 |         # Ez hibát kell, hogy dobjon, mert a 'key' nem dictionary
821 |         with pytest.raises(ValueError, match="Nem lehet beágyazott kulcsot beállítani nem dictionary értékben"):
    |                                                                                                     ^^^^^^^^^^^^
822 |             manager.set("key", "nested", value="value")
    |

E721 Use `is` and `is not` for type comparisons, or `isinstance()` for isinstance checks
   --> tests/core/config/interfaces/test_async_config_interface.py:153:16
    |
151 |         # get_section
152 |         get_section_method = AsyncConfigManagerInterface.get_section
153 |         assert get_section_method.__annotations__["section"] == str
    |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
154 |         assert get_section_method.__annotations__["return"] == dict[str, Any]
    |

E721 Use `is` and `is not` for type comparisons, or `isinstance()` for isinstance checks
   --> tests/core/config/interfaces/test_async_config_interface.py:168:16
    |
166 |         # load
167 |         load_method = AsyncConfigManagerInterface.load
168 |         assert load_method.__annotations__["filename"] == str
    |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
169 |         assert load_method.__annotations__["return"] is None
    |

E721 Use `is` and `is not` for type comparisons, or `isinstance()` for isinstance checks
   --> tests/core/config/interfaces/test_async_config_interface.py:173:16
    |
171 |         # load_directory
172 |         load_directory_method = AsyncConfigManagerInterface.load_directory
173 |         assert load_directory_method.__annotations__["path"] == str
    |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
174 |         assert load_directory_method.__annotations__["return"] is None
    |

E721 Use `is` and `is not` for type comparisons, or `isinstance()` for isinstance checks
   --> tests/core/config/interfaces/test_async_config_interface.py:193:16
    |
191 |         # start_hot_reload
192 |         start_hot_reload_method = AsyncConfigManagerInterface.start_hot_reload
193 |         assert start_hot_reload_method.__annotations__["interval"] == float
    |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
194 |         assert start_hot_reload_method.__annotations__["return"] is None
    |

E721 Use `is` and `is not` for type comparisons, or `isinstance()` for isinstance checks
   --> tests/core/config/interfaces/test_async_config_interface.py:207:16
    |
205 |         # set_with_metadata
206 |         set_with_metadata_method = AsyncConfigManagerInterface.set_with_metadata
207 |         assert set_with_metadata_method.__annotations__["key"] == str
    |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
208 |         assert set_with_metadata_method.__annotations__["value"] == Any
209 |         assert set_with_metadata_method.__annotations__["category"] == str
    |

E721 Use `is` and `is not` for type comparisons, or `isinstance()` for isinstance checks
   --> tests/core/config/interfaces/test_async_config_interface.py:209:16
    |
207 |         assert set_with_metadata_method.__annotations__["key"] == str
208 |         assert set_with_metadata_method.__annotations__["value"] == Any
209 |         assert set_with_metadata_method.__annotations__["category"] == str
    |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
210 |         assert set_with_metadata_method.__annotations__["description"] == str | None
211 |         assert set_with_metadata_method.__annotations__["is_active"] == bool
    |

E721 Use `is` and `is not` for type comparisons, or `isinstance()` for isinstance checks
   --> tests/core/config/interfaces/test_async_config_interface.py:211:16
    |
209 |         assert set_with_metadata_method.__annotations__["category"] == str
210 |         assert set_with_metadata_method.__annotations__["description"] == str | None
211 |         assert set_with_metadata_method.__annotations__["is_active"] == bool
    |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
212 |         assert set_with_metadata_method.__annotations__["return"] is None
    |

E721 Use `is` and `is not` for type comparisons, or `isinstance()` for isinstance checks
   --> tests/core/config/interfaces/test_async_config_interface.py:216:16
    |
214 |         # delete
215 |         delete_method = AsyncConfigManagerInterface.delete
216 |         assert delete_method.__annotations__["key"] == str
    |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
217 |         assert delete_method.__annotations__["return"] == bool
    |

E721 Use `is` and `is not` for type comparisons, or `isinstance()` for isinstance checks
   --> tests/core/config/interfaces/test_async_config_interface.py:217:16
    |
215 |         delete_method = AsyncConfigManagerInterface.delete
216 |         assert delete_method.__annotations__["key"] == str
217 |         assert delete_method.__annotations__["return"] == bool
    |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
218 |
219 |     def test_config_listener_type_alias(self) -> None:
    |

E721 Use `is` and `is not` for type comparisons, or `isinstance()` for isinstance checks
  --> tests/core/config/interfaces/test_config_interface.py:94:16
   |
92 |         # get_section
93 |         get_section_method = ConfigManagerInterface.get_section
94 |         assert get_section_method.__annotations__["section"] == str
   |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
95 |         assert get_section_method.__annotations__["return"] == dict[str, Any]
   |

E721 Use `is` and `is not` for type comparisons, or `isinstance()` for isinstance checks
   --> tests/core/config/interfaces/test_config_interface.py:109:16
    |
107 |         # load
108 |         load_method = ConfigManagerInterface.load
109 |         assert load_method.__annotations__["filename"] == str
    |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
110 |         assert load_method.__annotations__["return"] is None
    |

E721 Use `is` and `is not` for type comparisons, or `isinstance()` for isinstance checks
   --> tests/core/config/interfaces/test_config_interface.py:114:16
    |
112 |         # load_directory
113 |         load_directory_method = ConfigManagerInterface.load_directory
114 |         assert load_directory_method.__annotations__["path"] == str
    |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
115 |         assert load_directory_method.__annotations__["return"] is None
    |

E721 Use `is` and `is not` for type comparisons, or `isinstance()` for isinstance checks
   --> tests/core/config/interfaces/test_factory_interface.py:135:16
    |
133 |         # register_manager
134 |         register_method = ConfigManagerFactoryInterface.register_manager
135 |         assert register_method.__annotations__["extension"] == str
    |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
136 |         assert register_method.__annotations__["manager_class"] == type["ConfigManagerInterface"]
137 |         assert register_method.__annotations__["return"] is None
    |

E721 Use `is` and `is not` for type comparisons, or `isinstance()` for isinstance checks
   --> tests/core/config/interfaces/test_factory_interface.py:141:16
    |
139 |         # get_manager
140 |         get_manager_method = ConfigManagerFactoryInterface.get_manager
141 |         assert get_manager_method.__annotations__["filename"] == str
    |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
142 |         assert get_manager_method.__annotations__["manager_type"] == str | None
143 |         assert get_manager_method.__annotations__["return"] == "ConfigManagerInterface"
    |

E721 Use `is` and `is not` for type comparisons, or `isinstance()` for isinstance checks
   --> tests/core/config/interfaces/test_factory_interface.py:147:16
    |
145 |         # create_manager
146 |         create_manager_method = ConfigManagerFactoryInterface.create_manager
147 |         assert create_manager_method.__annotations__["manager_type"] == str
    |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
148 |         assert create_manager_method.__annotations__["return"] == "ConfigManagerInterface"
    |

E501 Line too long (103 > 100)
   --> tests/core/config/test_config_factory.py:375:101
    |
374 |     def test_register_async_manager_should_validate_async_interface_implementation(self) -> None:
375 |         """Teszteli, hogy a register_async_manager ellenőrzi az interfész implementációt (125. sor)."""
    |                                                                                                     ^^^
376 |         # Given
377 |         class NotAnAsyncConfigManager:
    |

E501 Line too long (101 > 100)
   --> tests/core/config/test_processors_config.py:175:101
    |
173 |         assert isinstance(strength_window, int)
174 |
175 |     def test_d02_timeframe_configs_structure(self, config_manager: "ConfigManagerInterface") -> None:
    |                                                                                                     ^
176 |         """Teszteli a d02 timeframe_configs struktúrát."""
177 |         timeframe_configs = config_manager.get("processors", "d02", "timeframe_configs")
    |

E501 Line too long (107 > 100)
  --> tests/core/db/test_db_factory.py:59:101
   |
58 |     @patch("neural_ai.core.db.factory.get_engine")
59 |     def test_get_engine_without_config(self, mock_get_engine: MagicMock, factory: DatabaseFactory) -> None:
   |                                                                                                     ^^^^^^^
60 |         """Teszteli az engine lekérdezést konfig nélkül."""
61 |         mock_engine = MagicMock()
   |

E501 Line too long (104 > 100)
  --> tests/core/db/test_db_factory.py:70:101
   |
69 |     @patch("neural_ai.core.db.factory.get_engine")
70 |     def test_get_engine_with_config(self, mock_get_engine: MagicMock, factory: DatabaseFactory) -> None:
   |                                                                                                     ^^^^
71 |         """Teszteli az engine lekérdezést konfiggal."""
72 |         mock_engine = MagicMock()
   |

E501 Line too long (112 > 100)
  --> tests/core/db/test_db_factory.py:97:101
   |
96 |     @patch("neural_ai.core.config.factory.ConfigManagerFactory.get_manager")
97 |     def test_create_manager_without_config(self, mock_get_manager: MagicMock, factory: DatabaseFactory) -> None:
   |                                                                                                     ^^^^^^^^^^^^
98 |         """Teszteli a DatabaseManager létrehozást konfig nélkül."""
99 |         mock_config = MagicMock()
   |

E501 Line too long (114 > 100)
   --> tests/core/db/test_db_factory.py:116:101
    |
115 |     @patch("neural_ai.core.db.factory.get_async_session_maker")
116 |     def test_get_session_maker_caches_result(self, mock_get_session: MagicMock, factory: DatabaseFactory) -> None:
    |                                                                                                     ^^^^^^^^^^^^^^
117 |         """Teszteli, hogy a session maker cache-elődik a modul szintjén."""
118 |         mock_session_maker = MagicMock()
    |

E501 Line too long (106 > 100)
   --> tests/core/db/test_db_factory.py:129:101
    |
128 |     @patch("neural_ai.core.db.factory.get_engine")
129 |     def test_get_engine_caches_result(self, mock_get_engine: MagicMock, factory: DatabaseFactory) -> None:
    |                                                                                                     ^^^^^^
130 |         """Teszteli, hogy az engine cache-elődik a modul szintjén."""
131 |         mock_engine = MagicMock()
    |

E501 Line too long (101 > 100)
   --> tests/core/db/test_db_factory.py:156:101
    |
154 |     @patch("neural_ai.core.db.factory.get_engine")
155 |     def test_factory_methods_return_consistent_types(
156 |         self, mock_get_engine: MagicMock, mock_get_session_maker: MagicMock, factory: DatabaseFactory
    |                                                                                                     ^
157 |     ) -> None:
158 |         """Teszteli, hogy a factory metódusok konzisztens típusokat adnak vissza."""
    |

E501 Line too long (103 > 100)
   --> tests/core/db/test_db_factory.py:177:101
    |
176 |     @patch("neural_ai.core.config.factory.ConfigManagerFactory.get_manager")
177 |     def test_factory_is_stateless(self, mock_get_manager: MagicMock, factory: DatabaseFactory) -> None:
    |                                                                                                     ^^^
178 |         """Teszteli, hogy a factory osztály állapotmentes-e."""
179 |         mock_config = MagicMock()
    |

W293 Blank line contains whitespace
   --> tests/core/logger/implementations/test_colored_logger.py:103:1
    |
101 |     def test_existing_handlers_removed(self) -> None:
102 |         """Teszteli, hogy a meglévő handlerek eltávolításra kerülnek.
103 |         
    | ^^^^^^^^
104 |         Ez a teszt lefedi a 54-55. sorokat, ahol a meglévő handlerek
105 |         eltávolítása történik, hogy ne legyenek duplikált üzenetek.
    |
help: Remove whitespace from blank line

W293 Blank line contains whitespace
  --> tests/core/logger/implementations/test_rotating_file_logger.py:29:1
   |
27 |     def test_init_with_empty_file_raises_error(self) -> None:
28 |         """Logger inicializálás üres fájlnévvel hibát dob.
29 |         
   | ^^^^^^^^
30 |         Ez a teszt lefedi a 60. sort, ahol a ValueError-t dobjuk.
31 |         """
   |
help: Remove whitespace from blank line

W293 Blank line contains whitespace
  --> tests/core/logger/implementations/test_rotating_file_logger.py:66:1
   |
64 |     def test_debug_logging_without_kwargs(self) -> None:
65 |         """Debug üzenet logolásának tesztelése kwargs nélkül.
66 |         
   | ^^^^^^^^
67 |         Ez a teszt lefedi a 106. sort.
68 |         """
   |
help: Remove whitespace from blank line

W293 Blank line contains whitespace
  --> tests/core/logger/implementations/test_rotating_file_logger.py:91:1
   |
89 |     def test_info_logging_without_kwargs(self) -> None:
90 |         """Info üzenet logolásának tesztelése kwargs nélkül.
91 |         
   | ^^^^^^^^
92 |         Ez a teszt lefedi a 118. sort.
93 |         """
   |
help: Remove whitespace from blank line

W293 Blank line contains whitespace
   --> tests/core/logger/implementations/test_rotating_file_logger.py:114:1
    |
112 |     def test_warning_logging_without_kwargs(self) -> None:
113 |         """Warning üzenet logolásának tesztelése kwargs nélkül.
114 |         
    | ^^^^^^^^
115 |         Ez a teszt lefedi a 130. sort.
116 |         """
    |
help: Remove whitespace from blank line

W293 Blank line contains whitespace
   --> tests/core/logger/implementations/test_rotating_file_logger.py:137:1
    |
135 |     def test_error_logging_without_kwargs(self) -> None:
136 |         """Error üzenet logolásának tesztelése kwargs nélkül.
137 |         
    | ^^^^^^^^
138 |         Ez a teszt lefedi a 142. sort.
139 |         """
    |
help: Remove whitespace from blank line

W293 Blank line contains whitespace
   --> tests/core/logger/implementations/test_rotating_file_logger.py:160:1
    |
158 |     def test_critical_logging_without_kwargs(self) -> None:
159 |         """Critical üzenet logolásának tesztelése kwargs nélkül.
160 |         
    | ^^^^^^^^
161 |         Ez a teszt lefedi a 154. sort.
162 |         """
    |
help: Remove whitespace from blank line

W293 Blank line contains whitespace
   --> tests/core/logger/implementations/test_rotating_file_logger.py:199:1
    |
197 |     def test_time_based_rotation(self) -> None:
198 |         """Időalapú rotáció tesztelése.
199 |         
    | ^^^^^^^^
200 |         Ez a teszt lefedi a 75. sort, ahol a TimedRotatingFileHandler-t hozzuk létre.
201 |         """
    |
help: Remove whitespace from blank line

W293 Blank line contains whitespace
   --> tests/core/logger/implementations/test_rotating_file_logger.py:228:1
    |
226 |     def test_existing_handlers_removed(self) -> None:
227 |         """Teszteli, hogy a meglévő handlerek eltávolításra kerülnek.
228 |         
    | ^^^^^^^^
229 |         Ez a teszt lefedi a 56. sort, ahol a meglévő handlerek
230 |         eltávolítása történik.
    |
help: Remove whitespace from blank line

E501 Line too long (102 > 100)
   --> tests/core/logger/implementations/test_rotating_file_logger.py:257:101
    |
255 |             # Ellenőrizzük, hogy az új handler RotatingFileHandler vagy TimedRotatingFileHandler
256 |             handler_type = type(rotating_logger.logger.handlers[0]).__name__
257 |             assert "RotatingFileHandler" in handler_type or "TimedRotatingFileHandler" in handler_type
    |                                                                                                     ^^
258 |
259 |     def test_di_dependencies_none(self) -> None:
    |

W293 Blank line contains whitespace
  --> tests/core/logger/interfaces/test_logger_factory_interface.py:29:1
   |
27 |     def test_register_logger_raises_not_implemented(self) -> None:
28 |         """register_logger metódus NotImplementedError-t dob.
29 |         
   | ^^^^^^^^
30 |         Ez a teszt lefedi a 35. sort.
31 |         """
   |
help: Remove whitespace from blank line

W293 Blank line contains whitespace
  --> tests/core/logger/interfaces/test_logger_factory_interface.py:37:1
   |
35 |     def test_get_logger_raises_not_implemented(self) -> None:
36 |         """get_logger metódus NotImplementedError-t dob.
37 |         
   | ^^^^^^^^
38 |         Ez a teszt lefedi a 54. sort.
39 |         """
   |
help: Remove whitespace from blank line

W293 Blank line contains whitespace
  --> tests/core/logger/interfaces/test_logger_factory_interface.py:45:1
   |
43 |     def test_configure_raises_not_implemented(self) -> None:
44 |         """configure metódus NotImplementedError-t dob.
45 |         
   | ^^^^^^^^
46 |         Ez a teszt lefedi a 67. sort.
47 |         """
   |
help: Remove whitespace from blank line

E501 Line too long (109 > 100)
  --> tests/core/logger/interfaces/test_logger_interface.py:41:101
   |
39 |             """Mock logger implementáció a teszteléshez."""
40 |
41 |             def __init__(self, name: str, config: Any | None = None, **kwargs: Mapping[str, AnyStr]) -> None:
   |                                                                                                     ^^^^^^^^^
42 |                 super().__init__(name, config, **kwargs)
43 |                 self.name = name
   |

W293 Blank line contains whitespace
  --> tests/core/test_init_version_fallback.py:37:1
   |
35 |     def test_version_fallback_on_package_not_found(self, mock_version) -> None:
36 |         """Teszteli a fallback mechanizmust, ha a csomag nincs telepítve.
37 |         
   | ^^^^^^^^
38 |         Ez a teszt lefedi a PackageNotFoundError exception handler ágat.
39 |         """
   |
help: Remove whitespace from blank line

UP036 Version block is outdated for minimum Python version
  --> tests/core/test_init_version_fallback.py:72:12
   |
70 |         # de ellenőrizhetjük, hogy a változó nem módosítható
71 |         import sys
72 |         if sys.version_info >= (3, 8):
   |            ^^^^^^^^^^^^^^^^^^^^^^^^^^
73 |             from typing import Final, get_type_hints
74 |             hints = get_type_hints(neural_ai)
   |
help: Remove outdated version block

E501 Line too long (729 > 100)
  --> tests/core/utils/test_hardware_info.py:21:101
   |
19 | …
20 | …
21 | …ts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx pdpe1gb rdtscp lm constant_tsc art arch_perfmon pebs bts rep_good nopl xtopology nonstop_tsc cpuid aperfmperf pni pclmulqdq dtes64 monitor ds_cpl vmx est tm2 ssse3 sdbg fma cx16 xtpr pdcm pcid sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand lahf_lm abm 3dnowprefetch cpuid_fault epb invpcid_single pti ssbd ibrs ibpb stibp tpr_shadow vnmi flexpriority ept vpid ept_ad fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid mpx rdseed adx smap clflushopt intel_pt xsaveopt xsavec xgetbv1 xsaves dtherm ida arat pln pts hwp hwp_notify hwp_act_window hwp_epp
   |       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
22 | …
23 | …
   |

E501 Line too long (160 > 100)
  --> tests/core/utils/test_hardware_info.py:33:101
   |
31 | …
32 | …
33 | …ge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx lm constant_tsc
   |                                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
34 | …
35 | …info)):
   |

E501 Line too long (165 > 100)
  --> tests/core/utils/test_hardware_info.py:57:101
   |
55 | …
56 | …
57 | … mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx lm constant_tsc avx2
   |                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
58 | …
59 | …fo)):
   |

E501 Line too long (164 > 100)
  --> tests/core/utils/test_hardware_info.py:85:101
   |
83 | …
84 | …
85 | … mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx lm constant_tsc avx
   |                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
86 | …
87 | …fo)):
   |

E501 Line too long (115 > 100)
   --> tests/core/utils/test_hardware_info.py:107:101
    |
105 |         mock_cpuinfo = """
106 | processor   : 0
107 | flags       : fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse
    |                                                                                                     ^^^^^^^^^^^^^^^
108 | """
109 |         with patch("builtins.open", mock_open(read_data=mock_cpuinfo)):
    |

E501 Line too long (101 > 100)
   --> tests/data/ingestion/test_market_data_persister.py:100:101
    |
 99 |         persister = MarketDataPersister(
100 |             event_bus=mock_event_bus, storage=mock_storage, logger=mock_logger, config=default_config
    |                                                                                                     ^
101 |         )
102 |         persister.running = True
    |

E501 Line too long (101 > 100)
   --> tests/data/ingestion/test_market_data_persister.py:117:101
    |
116 |         persister = MarketDataPersister(
117 |             event_bus=mock_event_bus, storage=mock_storage, logger=mock_logger, config=default_config
    |                                                                                                     ^
118 |         )
119 |         persister.running = True
    |

E501 Line too long (101 > 100)
   --> tests/data/ingestion/test_market_data_persister.py:146:101
    |
145 |         persister = MarketDataPersister(
146 |             event_bus=mock_event_bus, storage=mock_storage, logger=mock_logger, config=default_config
    |                                                                                                     ^
147 |         )
148 |         persister.running = False
    |

E501 Line too long (141 > 100)
   --> tests/data/ingestion/test_market_data_persister.py:166:101
    |
165 | …
166 | …age, logger=mock_logger, config={"buffer_size_limit": 5, "flush_interval_minutes": 60}
    |                                               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
167 | …
168 | …
    |

E501 Line too long (130 > 100)
   --> tests/data/ingestion/test_market_data_persister.py:191:101
    |
189 |         mock_logger = MagicMock()
190 |
191 |         persister = MarketDataPersister(event_bus=mock_event_bus, storage=mock_storage, logger=mock_logger, config=default_config)
    |                                                                                                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
192 |         persister.running = True
    |

E501 Line too long (101 > 100)
   --> tests/data/ingestion/test_market_data_persister.py:218:101
    |
217 |         persister = MarketDataPersister(
218 |             event_bus=mock_event_bus, storage=mock_storage, logger=mock_logger, config=default_config
    |                                                                                                     ^
219 |         )
220 |         persister.running = True
    |

E501 Line too long (141 > 100)
   --> tests/data/ingestion/test_market_data_persister.py:233:101
    |
232 | …
233 | …age, logger=MagicMock(), config={"buffer_size_limit": 3, "flush_interval_minutes": 60}
    |                                               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
234 | …
235 | …
    |

E501 Line too long (130 > 100)
   --> tests/data/ingestion/test_market_data_persister.py:269:101
    |
267 |         mock_logger = MagicMock()
268 |
269 |         persister = MarketDataPersister(event_bus=mock_event_bus, storage=mock_storage, logger=mock_logger, config=default_config)
    |                                                                                                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
270 |         persister.running = True
    |

E501 Line too long (101 > 100)
   --> tests/data/ingestion/test_market_data_persister.py:302:101
    |
301 |         persister = MarketDataPersister(
302 |             event_bus=mock_event_bus, storage=mock_storage, logger=mock_logger, config=default_config
    |                                                                                                     ^
303 |         )
304 |         persister.running = True
    |

E501 Line too long (130 > 100)
   --> tests/data/ingestion/test_market_data_persister.py:332:101
    |
330 |         mock_storage = MagicMock()
331 |
332 |         persister = MarketDataPersister(event_bus=mock_event_bus, storage=mock_storage, logger=MagicMock(), config=default_config)
    |                                                                                                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
333 |         persister.running = True
    |

E501 Line too long (101 > 100)
   --> tests/data/ingestion/test_market_data_persister.py:362:101
    |
361 |         persister = MarketDataPersister(
362 |             event_bus=mock_event_bus, storage=mock_storage, logger=mock_logger, config=default_config
    |                                                                                                     ^
363 |         )
    |

E501 Line too long (113 > 100)
  --> tests/data/storage/backends/test_pandas_backend.py:94:101
   |
92 |         assert backend._pandas_wrapper.fp.ParquetFile(str(path)) is not None
93 |
94 |     def test_write_with_compression(self, backend: PandasBackend, sample_dataframe: Any, temp_dir: Path) -> None:
   |                                                                                                     ^^^^^^^^^^^^^
95 |         """Teszteli a write műveletet tömörítéssel."""
96 |         path = temp_dir / "test_compressed.parquet"
   |

E501 Line too long (101 > 100)
   --> tests/data/storage/backends/test_pandas_backend.py:112:101
    |
110 |             backend.write(sample_dataframe, "/invalid/path.txt")
111 |
112 |     def test_read_basic(self, backend: PandasBackend, sample_dataframe: Any, temp_dir: Path) -> None:
    |                                                                                                     ^
113 |         """Teszteli az alap read műveletet."""
114 |         path = temp_dir / "test.parquet"
    |

E501 Line too long (108 > 100)
   --> tests/data/storage/backends/test_pandas_backend.py:121:101
    |
119 |         assert list(result.columns) == ['id', 'name', 'age']
120 |
121 |     def test_read_with_columns(self, backend: PandasBackend, sample_dataframe: Any, temp_dir: Path) -> None:
    |                                                                                                     ^^^^^^^^
122 |         """Teszteli a read műveletet oszlopszűréssel."""
123 |         path = temp_dir / "test.parquet"
    |

E501 Line too long (103 > 100)
   --> tests/data/storage/backends/test_pandas_backend.py:136:101
    |
134 |             backend.read(str(path))
135 |
136 |     def test_read_chunked(self, backend: PandasBackend, sample_dataframe: Any, temp_dir: Path) -> None:
    |                                                                                                     ^^^
137 |         """Teszteli a chunkolt olvasást."""
138 |         path = temp_dir / "test.parquet"
    |

E501 Line too long (109 > 100)
   --> tests/data/storage/backends/test_pandas_backend.py:144:101
    |
142 |         assert len(result) == 3
143 |
144 |     def test_append_to_new_file(self, backend: PandasBackend, sample_dataframe: Any, temp_dir: Path) -> None:
    |                                                                                                     ^^^^^^^^^
145 |         """Teszteli a hozzáfűzést új fájlhoz."""
146 |         path = temp_dir / "test.parquet"
    |

E501 Line too long (114 > 100)
   --> tests/data/storage/backends/test_pandas_backend.py:153:101
    |
151 |         assert len(result) == 3
152 |
153 |     def test_append_to_existing_file(self, backend: PandasBackend, sample_dataframe: Any, temp_dir: Path) -> None:
    |                                                                                                     ^^^^^^^^^^^^^^
154 |         """Teszteli a hozzáfűzést meglévő fájlhoz."""
155 |         path = temp_dir / "test.parquet"
    |

E501 Line too long (126 > 100)
   --> tests/data/storage/backends/test_pandas_backend.py:170:101
    |
168 |         assert len(result) == 5
169 |
170 |     def test_append_with_schema_validation_valid(self, backend: PandasBackend, sample_dataframe: Any, temp_dir: Path) -> None:
    |                                                                                                     ^^^^^^^^^^^^^^^^^^^^^^^^^^
171 |         """Teszteli a hozzáfűzést sémavizsgálattal - érvényes eset."""
172 |         path = temp_dir / "test.parquet"
    |

E501 Line too long (128 > 100)
   --> tests/data/storage/backends/test_pandas_backend.py:187:101
    |
185 |         assert len(result) == 4
186 |
187 |     def test_append_with_schema_validation_invalid(self, backend: PandasBackend, sample_dataframe: Any, temp_dir: Path) -> None:
    |                                                                                                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
188 |         """Teszteli a hozzáfűzést sémavizsgálattal - érvénytelen eset."""
189 |         path = temp_dir / "test.parquet"
    |

E501 Line too long (108 > 100)
   --> tests/data/storage/backends/test_pandas_backend.py:249:101
    |
247 |         assert 'parquet' in repr_str
248 |
249 |     def test_write_partitioned(self, backend: PandasBackend, sample_dataframe: Any, temp_dir: Path) -> None:
    |                                                                                                     ^^^^^^^^
250 |         """Teszteli a particionált írást."""
251 |         path = temp_dir / "partitioned.parquet"
    |

E501 Line too long (107 > 100)
   --> tests/data/storage/backends/test_pandas_backend.py:257:101
    |
255 |         assert path.exists() or path.parent.exists()
256 |
257 |     def test_write_with_index(self, backend: PandasBackend, sample_dataframe: Any, temp_dir: Path) -> None:
    |                                                                                                     ^^^^^^^
258 |         """Teszteli az írást index mentéssel."""
259 |         path = temp_dir / "test_index.parquet"
    |

E501 Line too long (108 > 100)
   --> tests/data/storage/backends/test_pandas_backend.py:264:101
    |
262 |         assert path.exists()
263 |
264 |     def test_read_with_filters(self, backend: PandasBackend, sample_dataframe: Any, temp_dir: Path) -> None:
    |                                                                                                     ^^^^^^^^
265 |         """Teszteli az olvasást szűrőkkel."""
266 |         path = temp_dir / "test.parquet"
    |

E501 Line too long (102 > 100)
  --> tests/data/storage/backends/test_polars_backend.py:90:101
   |
88 |         assert backend._initialized is True
89 |
90 |     def test_write_basic(self, backend: PolarsBackend, sample_dataframe: Any, temp_dir: Path) -> None:
   |                                                                                                     ^^
91 |         """Teszteli az alap write műveletet."""
92 |         path = temp_dir / "test.parquet"
   |

E501 Line too long (113 > 100)
   --> tests/data/storage/backends/test_polars_backend.py:101:101
    |
 99 |         assert parquet_file is not None
100 |
101 |     def test_write_with_compression(self, backend: PolarsBackend, sample_dataframe: Any, temp_dir: Path) -> None:
    |                                                                                                     ^^^^^^^^^^^^^
102 |         """Teszteli a write műveletet tömörítéssel."""
103 |         path = temp_dir / "test_compressed.parquet"
    |

E501 Line too long (101 > 100)
   --> tests/data/storage/backends/test_polars_backend.py:119:101
    |
117 |             backend.write(sample_dataframe, "/invalid/path.txt")
118 |
119 |     def test_read_basic(self, backend: PolarsBackend, sample_dataframe: Any, temp_dir: Path) -> None:
    |                                                                                                     ^
120 |         """Teszteli az alap read műveletet."""
121 |         path = temp_dir / "test.parquet"
    |

E501 Line too long (108 > 100)
   --> tests/data/storage/backends/test_polars_backend.py:130:101
    |
128 |         assert 'age' in result.columns
129 |
130 |     def test_read_with_columns(self, backend: PolarsBackend, sample_dataframe: Any, temp_dir: Path) -> None:
    |                                                                                                     ^^^^^^^^
131 |         """Teszteli a read műveletet oszlopszűréssel."""
132 |         path = temp_dir / "test.parquet"
    |

E501 Line too long (103 > 100)
   --> tests/data/storage/backends/test_polars_backend.py:145:101
    |
143 |             backend.read(str(path))
144 |
145 |     def test_read_chunked(self, backend: PolarsBackend, sample_dataframe: Any, temp_dir: Path) -> None:
    |                                                                                                     ^^^
146 |         """Teszteli a chunkolt olvasást."""
147 |         path = temp_dir / "test.parquet"
    |

E501 Line too long (109 > 100)
   --> tests/data/storage/backends/test_polars_backend.py:156:101
    |
154 |         assert len(result) == 3
155 |
156 |     def test_append_to_new_file(self, backend: PolarsBackend, sample_dataframe: Any, temp_dir: Path) -> None:
    |                                                                                                     ^^^^^^^^^
157 |         """Teszteli a hozzáfűzést új fájlhoz."""
158 |         path = temp_dir / "test.parquet"
    |

E501 Line too long (114 > 100)
   --> tests/data/storage/backends/test_polars_backend.py:165:101
    |
163 |         assert len(result) == 3
164 |
165 |     def test_append_to_existing_file(self, backend: PolarsBackend, sample_dataframe: Any, temp_dir: Path) -> None:
    |                                                                                                     ^^^^^^^^^^^^^^
166 |         """Teszteli a hozzáfűzést meglévő fájlhoz."""
167 |         path = temp_dir / "test.parquet"
    |

E501 Line too long (126 > 100)
   --> tests/data/storage/backends/test_polars_backend.py:182:101
    |
180 |         assert len(result) == 5
181 |
182 |     def test_append_with_schema_validation_valid(self, backend: PolarsBackend, sample_dataframe: Any, temp_dir: Path) -> None:
    |                                                                                                     ^^^^^^^^^^^^^^^^^^^^^^^^^^
183 |         """Teszteli a hozzáfűzést sémavizsgálattal - érvényes eset."""
184 |         path = temp_dir / "test.parquet"
    |

E501 Line too long (128 > 100)
   --> tests/data/storage/backends/test_polars_backend.py:199:101
    |
197 |         assert len(result) == 4
198 |
199 |     def test_append_with_schema_validation_invalid(self, backend: PolarsBackend, sample_dataframe: Any, temp_dir: Path) -> None:
    |                                                                                                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
200 |         """Teszteli a hozzáfűzést sémavizsgálattal - érvénytelen eset."""
201 |         path = temp_dir / "test.parquet"
    |

E501 Line too long (108 > 100)
   --> tests/data/storage/backends/test_polars_backend.py:261:101
    |
259 |         assert 'parquet' in repr_str
260 |
261 |     def test_write_partitioned(self, backend: PolarsBackend, sample_dataframe: Any, temp_dir: Path) -> None:
    |                                                                                                     ^^^^^^^^
262 |         """Teszteli a particionált írást."""
263 |         path = temp_dir / "partitioned.parquet"
    |

E501 Line too long (108 > 100)
   --> tests/data/storage/backends/test_polars_backend.py:273:101
    |
271 |         assert path.exists() or path.parent.exists()
272 |
273 |     def test_read_with_filters(self, backend: PolarsBackend, sample_dataframe: Any, temp_dir: Path) -> None:
    |                                                                                                     ^^^^^^^^
274 |         """Teszteli az olvasást szűrőkkel."""
275 |         path = temp_dir / "test.parquet"
    |

E501 Line too long (118 > 100)
   --> tests/data/storage/backends/test_polars_backend.py:322:101
    |
320 |         assert backend._validate_schema("invalid", "invalid") is False
321 |
322 |     def test_read_chunked_implementation(self, backend: PolarsBackend, sample_dataframe: Any, temp_dir: Path) -> None:
    |                                                                                                     ^^^^^^^^^^^^^^^^^^
323 |         """Teszteli a _read_chunked metódust."""
324 |         path = temp_dir / "test.parquet"
    |

F821 Undefined name `PermissionDeniedError`
   --> tests/data/storage/implementations/test_file_storage.py:238:16
    |
236 |         try:
237 |             storage._check_permissions(test_file, check_write=False)
238 |         except PermissionDeniedError:
    |                ^^^^^^^^^^^^^^^^^^^^^
239 |             pytest.fail("Unexpected PermissionDeniedError")
    |

E501 Line too long (101 > 100)
   --> tests/data/storage/implementations/test_file_storage.py:420:101
    |
418 |         monkeypatch.setattr(os_module, "statvfs", mock_statvfs)
419 |
420 |         with pytest.raises(StorageIOError, match="Nem sikerült lekérdezni a tárolási információkat"):
    |                                                                                                     ^
421 |             storage.get_storage_info(temp_dir)
    |

F841 Local variable `mock_pl` is assigned to but never used
   --> tests/data/storage/implementations/test_parquet_storage.py:435:84
    |
433 |     def test_deduplicate_data_polars(self, storage_service):
434 |         """Teszteli a deduplikációt Polars esetén."""
435 |         with patch("neural_ai.data.storage.implementations.parquet_storage.pl") as mock_pl:
    |                                                                                    ^^^^^^^
436 |             mock_df = MagicMock()
437 |             mock_df.columns = ["timestamp", "bid", "ask"]
    |
help: Remove assignment to unused variable `mock_pl`

F841 Local variable `mock_pl` is assigned to but never used
   --> tests/data/storage/implementations/test_parquet_storage.py:461:84
    |
459 |     def test_sort_by_timestamp_polars(self, storage_service):
460 |         """Teszteli a rendezést timestamp szerint Polars esetén."""
461 |         with patch("neural_ai.data.storage.implementations.parquet_storage.pl") as mock_pl:
    |                                                                                    ^^^^^^^
462 |             mock_df = MagicMock()
463 |             mock_sorted = MagicMock()
    |
help: Remove assignment to unused variable `mock_pl`

F841 Local variable `mock_pd` is assigned to but never used
   --> tests/data/storage/implementations/test_parquet_storage.py:474:84
    |
472 |     def test_sort_by_timestamp_pandas(self, storage_service):
473 |         """Teszteli a rendezést timestamp szerint Pandas esetén."""
474 |         with patch("neural_ai.data.storage.implementations.parquet_storage.pd") as mock_pd:
    |                                                                                    ^^^^^^^
475 |             mock_df = MagicMock()
476 |             mock_sorted = MagicMock()
    |
help: Remove assignment to unused variable `mock_pd`

E501 Line too long (105 > 100)
   --> tests/data/storage/test_storage_factory.py:169:101
    |
167 |     def test_get_storage_with_hardware_none(self, tmp_path: Path) -> None:
168 |         """Teszteli a storage létrehozást hardware=None paraméterrel."""
169 |         storage = StorageFactory.get_storage(storage_type="file", base_path=str(tmp_path), hardware=None)
    |                                                                                                     ^^^^^
170 |
171 |         assert isinstance(storage, FileStorage)
    |

B007 Loop control variable `i` not used within loop body
  --> tests/integration/test_d1_full.py:75:9
   |
73 |     closes = []
74 |
75 |     for i in range(100):
   |         ^
76 |         open_price = base_price + np.random.normal(0, 0.001)
77 |         close_price = open_price + np.random.normal(0, 0.002)
   |
help: Rename unused `i` to `_i`

D415 First line should end with a period, question mark, or exclamation point
  --> tests/integration/test_resampling.py:2:1
   |
 1 |   #!/usr/bin/env python3
 2 | / """Tick -> OHLCV Resampling Demo Script
 3 | |
 4 | | Ez a szkript demonstrálja a Tick adatok OHLCV (Open, High, Low, Close, Volume)
 5 | | formátumba való konvertálását 1 perces (M1) és 1 órás (H1) időkeretekben.
 6 | |
 7 | | A szkript a következő lépéseket hajtja végre:
 8 | | 1. Bootstrap: Rendszer inicializálása
 9 | | 2. Discovery: Elérhető dátumok lekérdezése
10 | | 3. Load: Tick adatok betöltése
11 | | 4. Resample M1: 1 perces OHLCV generálás
12 | | 5. Resample H1: 1 órás OHLCV generálás
13 | | 6. Display: Eredmények színes megjelenítése
14 | | 7. Export: CSV fájlba mentés
15 | |
16 | | Author: Neural AI Next Team
17 | | Version: 1.0.0
18 | | """
   | |___^
19 |
20 |   import asyncio
   |
help: Add closing punctuation

E501 Line too long (115 > 100)
   --> tests/integration/test_resampling.py:101:101
    |
 99 |                 print(f"{Fore.RED}❌ Hiba: Nincsenek elérhető dátumok az EURUSD szimbólumhoz!")
100 |                 print(
101 |                     f"{Fore.RED}   Kérjük, először töltsön le adatokat a scripts/download_history.py szkripttel.\n"
    |                                                                                                     ^^^^^^^^^^^^^^^
102 |                 )
103 |                 return
    |

E501 Line too long (109 > 100)
   --> tests/integration/test_resampling.py:124:101
    |
122 |             print("   - Szimbólum: EURUSD")
123 |             print(
124 |                 f"   - Dátumtartomány: {start_date.strftime('%Y-%m-%d')} - {end_date.strftime('%Y-%m-%d')}\n"
    |                                                                                                     ^^^^^^^^^
125 |             )
    |

E501 Line too long (109 > 100)
   --> tests/integration/test_resampling.py:263:101
    |
261 |         # Fejléc
262 |         print(
263 |             f"{Fore.CYAN}{'Időbélyeg':<25} {'Open':<12} {'High':<12} {'Low':<12} {'Close':<12} {'Ticks':<10}"
    |                                                                                                     ^^^^^^^^^
264 |         )
265 |         print(f"{Fore.CYAN}{'─' * 80}{Style.RESET_ALL}")
    |

D100 Missing docstring in public module
--> tests/integration/test_time_alignment.py:1:1

F841 Local variable `expected_strength` is assigned to but never used
   --> tests/processors/dimensions/d02_support/test_d02_processor.py:401:9
    |
399 |         result = processor._calculate_level_strength(levels)
400 |
401 |         expected_strength = (5 * 0.1) * 1.0  # volume_factor alapértelmezett 1.0, max_strength = 0.5, normalizált 1.0
    |         ^^^^^^^^^^^^^^^^^
402 |         assert len(result) == 1
403 |         assert result[0]["strength"] == 1.0  # Normalizált
    |
help: Remove assignment to unused variable `expected_strength`

E501 Line too long (117 > 100)
   --> tests/processors/dimensions/d02_support/test_d02_processor.py:401:101
    |
399 |         result = processor._calculate_level_strength(levels)
400 |
401 |         expected_strength = (5 * 0.1) * 1.0  # volume_factor alapértelmezett 1.0, max_strength = 0.5, normalizált 1.0
    |                                                                                                     ^^^^^^^^^^^^^^^^^
402 |         assert len(result) == 1
403 |         assert result[0]["strength"] == 1.0  # Normalizált
    |

E501 Line too long (108 > 100)
   --> tests/processors/dimensions/d02_support/test_d02_processor.py:575:101
    |
573 |         """Teszteli a _categorize_zones metódust min_touches határán."""
574 |         levels = [
575 |             {"price": 1.0520, "touches": 2, "type": "resistance", "strength": 0.8}  # touches == min_touches
    |                                                                                                     ^^^^^^^^
576 |         ]
577 |         result = processor._categorize_zones(levels)
    |

E501 Line too long (115 > 100)
   --> tests/scripts/test_download_history.py:105:101
    |
103 |     @pytest.mark.asyncio
104 |     async def test_save_ticks_direct_creates_correct_dataframe_columns(self) -> None:
105 |         """Teszteli, hogy a _save_ticks_direct függvény helyesen hozza létre a DataFrame-et a forrásoszlopokkal."""
    |                                                                                                     ^^^^^^^^^^^^^^^
106 |         from scripts.download_history import _save_ticks_direct
    |

E501 Line too long (102 > 100)
   --> tests/ui/pages/test_data_hub_page.py:190:101
    |
188 |         page = DataHubPage(mock_bridge)
189 |
190 |         # A render metódus try-except blokkal van védve, ezért nem szabad a kivételnek továbbterjednie
    |                                                                                                     ^^
191 |         try:
192 |             page.render()
    |

F841 Local variable `mock_get_candles` is assigned to but never used
   --> tests/ui/services/test_strategy_service.py:592:14
    |
590 |         with patch.object(
591 |             strategy_service, "get_candles", new_callable=AsyncMock, return_value=None
592 |         ) as mock_get_candles:
    |              ^^^^^^^^^^^^^^^^
593 |             with pytest.raises(ValueError, match="Nincs elérhető adat"):
594 |                 await strategy_service.analyze_market_structure(
    |
help: Remove assignment to unused variable `mock_get_candles`

Found 155 errors.
No fixes available (27 hidden fixes can be enabled with the `--unsafe-fixes` option).
```

## 2. Teszt Hibák (Unit Tests)
```
============================= test session starts ==============================
platform linux -- Python 3.12.12, pytest-9.0.2, pluggy-1.6.0 -- /home/elynea/miniconda3/envs/neural-ai-next/bin/python3.12
cachedir: .pytest_cache
rootdir: /home/elynea/Dokumentumok/neural-ai-next
configfile: pyproject.toml
testpaths: tests
plugins: anyio-4.12.0, asyncio-1.3.0, cov-7.0.0
asyncio: mode=Mode.AUTO, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collecting ... collected 1663 items

tests/collectors/jforex/exceptions/test_exceptions_init.py::TestJForexExceptionsInit::test_jforexerror_exported PASSED [  0%]
tests/collectors/jforex/exceptions/test_exceptions_init.py::TestJForexExceptionsInit::test_downloaderror_exported PASSED [  0%]
tests/collectors/jforex/exceptions/test_exceptions_init.py::TestJForexExceptionsInit::test_decodeerror_exported PASSED [  0%]
tests/collectors/jforex/exceptions/test_exceptions_init.py::TestJForexExceptionsInit::test_datanotavailableerror_exported PASSED [  0%]
tests/collectors/jforex/exceptions/test_exceptions_init.py::TestJForexExceptionsInit::test_exception_instantiation PASSED [  0%]
tests/collectors/jforex/interfaces/test_interfaces_init.py::TestJForexInterfacesInit::test_ijforexdownloader_exported PASSED [  0%]
tests/collectors/jforex/interfaces/test_interfaces_init.py::TestJForexInterfacesInit::test_ilivefeed_exported PASSED [  0%]
tests/collectors/jforex/interfaces/test_interfaces_init.py::TestJForexInterfacesInit::test_tickdata_exported PASSED [  0%]
tests/collectors/jforex/test_bi5_downloader.py::TestBi5Downloader::test_base_timestamp_calculation_retains_hour PASSED [  0%]
tests/collectors/jforex/test_bi5_downloader.py::TestBi5Downloader::test_base_timestamp_calculation_different_hours PASSED [  0%]
tests/collectors/jforex/test_bi5_downloader.py::TestBi5Downloader::test_process_bi5_data_12_byte_format PASSED [  0%]
tests/collectors/jforex/test_bi5_downloader.py::TestBi5Downloader::test_process_bi5_data_20_byte_format PASSED [  0%]
tests/collectors/jforex/test_bi5_downloader.py::TestBi5Downloader::test_process_bi5_data_empty_file PASSED [  0%]
tests/collectors/jforex/test_bi5_downloader.py::TestBi5Downloader::test_process_bi5_data_invalid_prices PASSED [  0%]
tests/collectors/jforex/test_bi5_downloader.py::TestBi5Downloader::test_process_bi5_data_invalid_timestamp_delta PASSED [  0%]
tests/collectors/jforex/test_bi5_downloader.py::TestBi5Downloader::test_process_bi5_data_date_mismatch PASSED [  0%]
tests/collectors/jforex/test_bi5_downloader.py::TestBi5Downloader::test_build_url PASSED [  1%]
tests/collectors/jforex/test_bi5_downloader.py::TestBi5Downloader::test_build_storage_path PASSED [  1%]
tests/collectors/jforex/test_bi5_downloader.py::TestBi5Downloader::test_download_tick_data_success PASSED [  1%]
tests/collectors/jforex/test_bi5_downloader.py::TestBi5Downloader::test_download_tick_data_not_available PASSED [  1%]
tests/collectors/jforex/test_bi5_downloader.py::TestBi5Downloader::test_download_tick_data_already_exists PASSED [  1%]
tests/collectors/jforex/test_bi5_downloader.py::TestBi5Downloader::test_validate_bi5_data_valid PASSED [  1%]
tests/collectors/jforex/test_bi5_downloader.py::TestBi5Downloader::test_validate_bi5_data_invalid_size PASSED [  1%]
tests/collectors/jforex/test_bi5_downloader.py::TestBi5Downloader::test_validate_bi5_data_invalid_lzma PASSED [  1%]
tests/collectors/jforex/test_bi5_downloader.py::TestBi5Downloader::test_validate_bi5_data_empty_decompressed PASSED [  1%]
tests/collectors/jforex/test_bi5_downloader.py::TestBi5Downloader::test_validate_bi5_data_invalid_record_count PASSED [  1%]
tests/collectors/jforex/test_bi5_downloader.py::TestBi5Downloader::test_validate_bi5_data_negative_timestamp_delta PASSED [  1%]
tests/collectors/jforex/test_bi5_downloader.py::TestBi5Downloader::test_validate_bi5_data_invalid_prices PASSED [  1%]
tests/collectors/jforex/test_bi5_downloader.py::TestBi5Downloader::test_validate_bi5_data_extreme_prices PASSED [  1%]
tests/collectors/jforex/test_bi5_downloader.py::TestBi5Downloader::test_validate_bi5_data_20_byte_format PASSED [  1%]
tests/collectors/jforex/test_bi5_downloader.py::TestBi5Downloader::test_validate_bi5_data_20_byte_noise_volumes PASSED [  1%]
tests/collectors/jforex/test_bi5_downloader.py::TestBi5Downloader::test_validate_bi5_data_zero_records PASSED [  1%]
tests/collectors/jforex/test_bi5_downloader.py::TestBi5Downloader::test_close PASSED [  1%]
tests/collectors/jforex/test_bi5_downloader.py::TestBi5Downloader::test_detect_format_12_byte_default PASSED [  2%]
tests/collectors/jforex/test_bi5_downloader.py::TestBi5Downloader::test_detect_format_20_byte_with_valid_volumes PASSED [  2%]
tests/collectors/jforex/test_bi5_downloader.py::TestBi5Downloader::test_detect_format_20_byte_rejects_noise_volumes PASSED [  2%]
tests/collectors/jforex/test_bi5_downloader.py::TestBi5Downloader::test_detect_format_20_byte_rejects_zero_volumes PASSED [  2%]
tests/collectors/jforex/test_bi5_downloader.py::TestBi5Downloader::test_detect_format_12_byte_only PASSED [  2%]
tests/collectors/jforex/test_factory.py::TestJForexFactory::test_create_downloader_returns_downloader_interface PASSED [  2%]
tests/collectors/jforex/test_factory.py::TestJForexFactory::test_create_downloader_passes_storage_to_bi5downloader PASSED [  2%]
tests/collectors/jforex/test_factory.py::TestJForexFactory::test_create_downloader_handles_config_exception PASSED [  2%]
tests/collectors/jforex/test_factory.py::TestJForexFactory::test_create_live_feed_returns_live_interface PASSED [  2%]
tests/collectors/jforex/test_factory.py::TestJForexFactory::test_create_live_feed_logs_warning_when_disabled PASSED [  2%]
tests/collectors/jforex/test_factory.py::TestJForexFactory::test_create_live_feed_handles_config_exception PASSED [  2%]
tests/collectors/jforex/test_jforex_init.py::TestJForexCollectorInit::test_jforexfactory_exported PASSED [  2%]
tests/collectors/jforex/test_jforex_init.py::TestJForexCollectorInit::test_ijforexdownloader_exported PASSED [  2%]
tests/collectors/jforex/test_live_feed.py::TestJForexLiveFeed::test_start_success PASSED [  2%]
tests/collectors/jforex/test_live_feed.py::TestJForexLiveFeed::test_start_when_already_running PASSED [  2%]
tests/collectors/jforex/test_live_feed.py::TestJForexLiveFeed::test_stop_success PASSED [  2%]
tests/collectors/jforex/test_live_feed.py::TestJForexLiveFeed::test_stop_when_not_running PASSED [  3%]
tests/collectors/jforex/test_live_feed.py::TestJForexLiveFeed::test_process_tick_data_success PASSED [  3%]
tests/collectors/jforex/test_live_feed.py::TestJForexLiveFeed::test_process_tick_data_error PASSED [  3%]
tests/collectors/jforex/test_live_feed.py::TestJForexLiveFeed::test_listen_loop_processes_tick PASSED [  3%]
tests/collectors/jforex/test_live_feed.py::TestJForexLiveFeed::test_is_running_returns_correct_state PASSED [  3%]
tests/collectors/jforex/test_live_feed.py::TestJForexLiveFeed::test_init_with_empty_config_logs_warning PASSED [  3%]
tests/collectors/jforex/test_live_feed.py::TestJForexLiveFeed::test_init_with_config_logs_debug PASSED [  3%]
tests/collectors/jforex/test_live_feed.py::TestJForexLiveFeed::test_start_raises_exception_on_zmq_failure PASSED [  3%]
tests/collectors/jforex/test_live_feed.py::TestJForexLiveFeed::test_listen_loop_handles_socket_none PASSED [  3%]
tests/core/base/exceptions/test_base_error.py::TestNeuralAIException::test_base_exception_can_be_raised PASSED [  3%]
tests/core/base/exceptions/test_base_error.py::TestNeuralAIException::test_base_exception_with_message PASSED [  3%]
tests/core/base/exceptions/test_base_error.py::TestNeuralAIException::test_base_exception_inheritance PASSED [  3%]
tests/core/base/exceptions/test_base_error.py::TestStorageException::test_storage_exception_can_be_raised PASSED [  3%]
tests/core/base/exceptions/test_base_error.py::TestStorageException::test_storage_exception_inheritance PASSED [  3%]
tests/core/base/exceptions/test_base_error.py::TestStorageException::test_storage_exception_with_message PASSED [  3%]
tests/core/base/exceptions/test_base_error.py::TestStorageWriteError::test_storage_write_error_can_be_raised PASSED [  3%]
tests/core/base/exceptions/test_base_error.py::TestStorageWriteError::test_storage_write_error_inheritance PASSED [  3%]
tests/core/base/exceptions/test_base_error.py::TestStorageWriteError::test_storage_write_error_message PASSED [  4%]
tests/core/base/exceptions/test_base_error.py::TestStorageReadError::test_storage_read_error_can_be_raised PASSED [  4%]
tests/core/base/exceptions/test_base_error.py::TestStorageReadError::test_storage_read_error_inheritance PASSED [  4%]
tests/core/base/exceptions/test_base_error.py::TestStorageReadError::test_storage_read_error_message PASSED [  4%]
tests/core/base/exceptions/test_base_error.py::TestStoragePermissionError::test_storage_permission_error_can_be_raised PASSED [  4%]
tests/core/base/exceptions/test_base_error.py::TestStoragePermissionError::test_storage_permission_error_inheritance PASSED [  4%]
tests/core/base/exceptions/test_base_error.py::TestStoragePermissionError::test_storage_permission_error_message PASSED [  4%]
tests/core/base/exceptions/test_base_error.py::TestConfigurationError::test_configuration_error_can_be_raised PASSED [  4%]
tests/core/base/exceptions/test_base_error.py::TestConfigurationError::test_configuration_error_inheritance PASSED [  4%]
tests/core/base/exceptions/test_base_error.py::TestConfigurationError::test_configuration_error_message PASSED [  4%]
tests/core/base/exceptions/test_base_error.py::TestDependencyError::test_dependency_error_can_be_raised PASSED [  4%]
tests/core/base/exceptions/test_base_error.py::TestDependencyError::test_dependency_error_inheritance PASSED [  4%]
tests/core/base/exceptions/test_base_error.py::TestDependencyError::test_dependency_error_message PASSED [  4%]
tests/core/base/exceptions/test_base_error.py::TestSingletonViolationError::test_singleton_violation_error_can_be_raised PASSED [  4%]
tests/core/base/exceptions/test_base_error.py::TestSingletonViolationError::test_singleton_violation_error_inheritance PASSED [  4%]
tests/core/base/exceptions/test_base_error.py::TestSingletonViolationError::test_singleton_violation_error_message PASSED [  4%]
tests/core/base/exceptions/test_base_error.py::TestComponentNotFoundError::test_component_not_found_error_can_be_raised PASSED [  4%]
tests/core/base/exceptions/test_base_error.py::TestComponentNotFoundError::test_component_not_found_error_inheritance PASSED [  5%]
tests/core/base/exceptions/test_base_error.py::TestComponentNotFoundError::test_component_not_found_error_message PASSED [  5%]
tests/core/base/exceptions/test_base_error.py::TestNetworkException::test_network_exception_can_be_raised PASSED [  5%]
tests/core/base/exceptions/test_base_error.py::TestNetworkException::test_network_exception_inheritance PASSED [  5%]
tests/core/base/exceptions/test_base_error.py::TestNetworkException::test_network_exception_message PASSED [  5%]
tests/core/base/exceptions/test_base_error.py::TestTimeoutError::test_timeout_error_can_be_raised PASSED [  5%]
tests/core/base/exceptions/test_base_error.py::TestTimeoutError::test_timeout_error_inheritance PASSED [  5%]
tests/core/base/exceptions/test_base_error.py::TestTimeoutError::test_timeout_error_message PASSED [  5%]
tests/core/base/exceptions/test_base_error.py::TestConnectionError::test_connection_error_can_be_raised PASSED [  5%]
tests/core/base/exceptions/test_base_error.py::TestConnectionError::test_connection_error_inheritance PASSED [  5%]
tests/core/base/exceptions/test_base_error.py::TestConnectionError::test_connection_error_message PASSED [  5%]
tests/core/base/exceptions/test_base_error.py::TestInsufficientDiskSpaceError::test_insufficient_disk_space_error_can_be_raised PASSED [  5%]
tests/core/base/exceptions/test_base_error.py::TestInsufficientDiskSpaceError::test_insufficient_disk_space_error_inheritance PASSED [  5%]
tests/core/base/exceptions/test_base_error.py::TestInsufficientDiskSpaceError::test_insufficient_disk_space_error_message PASSED [  5%]
tests/core/base/exceptions/test_base_error.py::TestPermissionDeniedError::test_permission_denied_error_can_be_raised PASSED [  5%]
tests/core/base/exceptions/test_base_error.py::TestPermissionDeniedError::test_permission_denied_error_inheritance PASSED [  5%]
tests/core/base/exceptions/test_base_error.py::TestPermissionDeniedError::test_permission_denied_error_message PASSED [  6%]
tests/core/base/exceptions/test_exceptions_init.py::TestExceptionsInit::test_neural_ai_exception_import PASSED [  6%]
tests/core/base/exceptions/test_exceptions_init.py::TestExceptionsInit::test_storage_exception_import PASSED [  6%]
tests/core/base/exceptions/test_exceptions_init.py::TestExceptionsInit::test_storage_write_error_import PASSED [  6%]
tests/core/base/exceptions/test_exceptions_init.py::TestExceptionsInit::test_storage_read_error_import PASSED [  6%]
tests/core/base/exceptions/test_exceptions_init.py::TestExceptionsInit::test_storage_permission_error_import PASSED [  6%]
tests/core/base/exceptions/test_exceptions_init.py::TestExceptionsInit::test_configuration_error_import PASSED [  6%]
tests/core/base/exceptions/test_exceptions_init.py::TestExceptionsInit::test_dependency_error_import PASSED [  6%]
tests/core/base/exceptions/test_exceptions_init.py::TestExceptionsInit::test_singleton_violation_error_import PASSED [  6%]
tests/core/base/exceptions/test_exceptions_init.py::TestExceptionsInit::test_component_not_found_error_import PASSED [  6%]
tests/core/base/exceptions/test_exceptions_init.py::TestExceptionsInit::test_network_exception_import PASSED [  6%]
tests/core/base/exceptions/test_exceptions_init.py::TestExceptionsInit::test_timeout_error_import PASSED [  6%]
tests/core/base/exceptions/test_exceptions_init.py::TestExceptionsInit::test_connection_error_import PASSED [  6%]
tests/core/base/exceptions/test_exceptions_init.py::TestExceptionsInit::test_insufficient_disk_space_error_import PASSED [  6%]
tests/core/base/exceptions/test_exceptions_init.py::TestExceptionsInit::test_permission_denied_error_import PASSED [  6%]
tests/core/base/exceptions/test_exceptions_init.py::TestExceptionsInit::test_all_exports_available PASSED [  6%]
tests/core/base/exceptions/test_exceptions_init.py::TestExceptionsInit::test_exception_inheritance_hierarchy PASSED [  6%]
tests/core/base/exceptions/test_exceptions_init.py::TestExceptionsInit::test_exceptions_can_be_raised PASSED [  7%]
tests/core/base/exceptions/test_exceptions_init.py::TestExceptionsInit::test_exception_messages PASSED [  7%]
tests/core/base/implementations/test_component_bundle.py::TestCoreComponents::test_init_with_container PASSED [  7%]
tests/core/base/implementations/test_component_bundle.py::TestCoreComponents::test_init_without_container PASSED [  7%]
tests/core/base/implementations/test_component_bundle.py::TestCoreComponents::test_config_property_none PASSED [  7%]
tests/core/base/implementations/test_component_bundle.py::TestCoreComponents::test_config_property_with_instance PASSED [  7%]
tests/core/base/implementations/test_component_bundle.py::TestCoreComponents::test_logger_property_none PASSED [  7%]
tests/core/base/implementations/test_component_bundle.py::TestCoreComponents::test_logger_property_with_instance PASSED [  7%]
tests/core/base/implementations/test_component_bundle.py::TestCoreComponents::test_storage_property_none PASSED [  7%]
tests/core/base/implementations/test_component_bundle.py::TestCoreComponents::test_storage_property_with_instance PASSED [  7%]
tests/core/base/implementations/test_component_bundle.py::TestCoreComponents::test_database_property_none PASSED [  7%]
tests/core/base/implementations/test_component_bundle.py::TestCoreComponents::test_database_property_with_instance PASSED [  7%]
tests/core/base/implementations/test_component_bundle.py::TestCoreComponents::test_event_bus_property_none PASSED [  7%]
tests/core/base/implementations/test_component_bundle.py::TestCoreComponents::test_event_bus_property_with_instance PASSED [  7%]
tests/core/base/implementations/test_component_bundle.py::TestCoreComponents::test_hardware_property_none PASSED [  7%]
tests/core/base/implementations/test_component_bundle.py::TestCoreComponents::test_hardware_property_with_instance PASSED [  7%]
tests/core/base/implementations/test_component_bundle.py::TestCoreComponents::test_has_config_false PASSED [  7%]
tests/core/base/implementations/test_component_bundle.py::TestCoreComponents::test_has_config_true PASSED [  8%]
tests/core/base/implementations/test_component_bundle.py::TestCoreComponents::test_has_logger_false PASSED [  8%]
tests/core/base/implementations/test_component_bundle.py::TestCoreComponents::test_has_logger_true PASSED [  8%]
tests/core/base/implementations/test_component_bundle.py::TestCoreComponents::test_has_storage_false PASSED [  8%]
tests/core/base/implementations/test_component_bundle.py::TestCoreComponents::test_has_storage_true PASSED [  8%]
tests/core/base/implementations/test_component_bundle.py::TestCoreComponents::test_has_database_false PASSED [  8%]
tests/core/base/implementations/test_component_bundle.py::TestCoreComponents::test_has_database_true PASSED [  8%]
tests/core/base/implementations/test_component_bundle.py::TestCoreComponents::test_has_event_bus_false PASSED [  8%]
tests/core/base/implementations/test_component_bundle.py::TestCoreComponents::test_has_event_bus_true PASSED [  8%]
tests/core/base/implementations/test_component_bundle.py::TestCoreComponents::test_has_hardware_false PASSED [  8%]
tests/core/base/implementations/test_component_bundle.py::TestCoreComponents::test_has_hardware_true PASSED [  8%]
tests/core/base/implementations/test_component_bundle.py::TestCoreComponents::test_validate_false_when_empty PASSED [  8%]
tests/core/base/implementations/test_component_bundle.py::TestCoreComponents::test_validate_true_when_all_present PASSED [  8%]
tests/core/base/implementations/test_component_bundle.py::TestCoreComponents::test_validate_false_when_some_missing PASSED [  8%]
tests/core/base/implementations/test_component_bundle.py::TestCoreComponents::test_persister_property_none PASSED [  8%]
tests/core/base/implementations/test_component_bundle.py::TestCoreComponents::test_persister_property_with_instance PASSED [  8%]
tests/core/base/implementations/test_component_bundle.py::TestCoreComponents::test_live_feed_property_none PASSED [  9%]
tests/core/base/implementations/test_component_bundle.py::TestCoreComponents::test_live_feed_property_with_instance PASSED [  9%]
tests/core/base/implementations/test_component_bundle.py::TestCoreComponents::test_set_persister PASSED [  9%]
tests/core/base/implementations/test_component_bundle.py::TestCoreComponents::test_set_live_feed PASSED [  9%]
tests/core/base/implementations/test_component_bundle.py::TestCoreComponents::test_has_persister_false PASSED [  9%]
tests/core/base/implementations/test_component_bundle.py::TestCoreComponents::test_has_persister_true PASSED [  9%]
tests/core/base/implementations/test_component_bundle.py::TestCoreComponents::test_has_live_feed_false PASSED [  9%]
tests/core/base/implementations/test_component_bundle.py::TestCoreComponents::test_has_live_feed_true PASSED [  9%]
tests/core/base/implementations/test_di_container.py::TestLazyComponent::test_initialization PASSED [  9%]
tests/core/base/implementations/test_di_container.py::TestLazyComponent::test_get_multiple_times PASSED [  9%]
tests/core/base/implementations/test_di_container.py::TestDIContainer::test_initialization PASSED [  9%]
tests/core/base/implementations/test_di_container.py::TestDIContainer::test_register_instance PASSED [  9%]
tests/core/base/implementations/test_di_container.py::TestDIContainer::test_register_factory PASSED [  9%]
tests/core/base/implementations/test_di_container.py::TestDIContainer::test_resolve_instance PASSED [  9%]
tests/core/base/implementations/test_di_container.py::TestDIContainer::test_resolve_factory PASSED [  9%]
tests/core/base/implementations/test_di_container.py::TestDIContainer::test_resolve_not_found PASSED [  9%]
tests/core/base/implementations/test_di_container.py::TestDIContainer::test_register_lazy PASSED [  9%]
tests/core/base/implementations/test_di_container.py::TestDIContainer::test_register_lazy_invalid_name PASSED [ 10%]
tests/core/base/implementations/test_di_container.py::TestDIContainer::test_register_lazy_invalid_factory PASSED [ 10%]
tests/core/base/implementations/test_di_container.py::TestDIContainer::test_get_regular_instance PASSED [ 10%]
tests/core/base/implementations/test_di_container.py::TestDIContainer::test_get_lazy_component PASSED [ 10%]
tests/core/base/implementations/test_di_container.py::TestDIContainer::test_get_not_found PASSED [ 10%]
tests/core/base/implementations/test_di_container.py::TestDIContainer::test_get_lazy_components_status PASSED [ 10%]
tests/core/base/implementations/test_di_container.py::TestDIContainer::test_preload_components PASSED [ 10%]
tests/core/base/implementations/test_di_container.py::TestDIContainer::test_preload_components_not_found PASSED [ 10%]
tests/core/base/implementations/test_di_container.py::TestDIContainer::test_clear PASSED [ 10%]
tests/core/base/implementations/test_di_container.py::TestDIContainer::test_register_method PASSED [ 10%]
tests/core/base/implementations/test_di_container.py::TestDIContainer::test_register_invalid_name PASSED [ 10%]
tests/core/base/implementations/test_di_container.py::TestDIContainer::test_register_none_instance PASSED [ 10%]
tests/core/base/implementations/test_di_container.py::TestDIContainer::test_enforce_singleton_violation PASSED [ 10%]
tests/core/base/implementations/test_di_container.py::TestDIContainer::test_enforce_singleton_no_violation PASSED [ 10%]
tests/core/base/implementations/test_di_container.py::TestDIContainer::test_get_memory_usage PASSED [ 10%]
tests/core/base/implementations/test_implementations_init.py::TestImplementationsInit::test_core_components_import PASSED [ 10%]
tests/core/base/implementations/test_implementations_init.py::TestImplementationsInit::test_dicontainer_import PASSED [ 11%]
tests/core/base/implementations/test_implementations_init.py::TestImplementationsInit::test_lazy_component_import PASSED [ 11%]
tests/core/base/implementations/test_implementations_init.py::TestImplementationsInit::test_lazy_loader_import PASSED [ 11%]
tests/core/base/implementations/test_implementations_init.py::TestImplementationsInit::test_lazy_property_import PASSED [ 11%]
tests/core/base/implementations/test_implementations_init.py::TestImplementationsInit::test_singleton_meta_import PASSED [ 11%]
tests/core/base/implementations/test_implementations_init.py::TestImplementationsInit::test_all_exports_available PASSED [ 11%]
tests/core/base/implementations/test_implementations_init.py::TestImplementationsInit::test_core_components_instantiation PASSED [ 11%]
tests/core/base/implementations/test_implementations_init.py::TestImplementationsInit::test_dicontainer_instantiation PASSED [ 11%]
tests/core/base/implementations/test_implementations_init.py::TestImplementationsInit::test_lazy_component_instantiation PASSED [ 11%]
tests/core/base/implementations/test_implementations_init.py::TestImplementationsInit::test_lazy_loader_instantiation PASSED [ 11%]
tests/core/base/implementations/test_implementations_init.py::TestImplementationsInit::test_singleton_meta_as_metaclass PASSED [ 11%]
tests/core/base/implementations/test_implementations_init.py::TestImplementationsInit::test_lazy_property_decorator PASSED [ 11%]
tests/core/base/implementations/test_lazy_loader.py::TestLazyLoader::test_init PASSED [ 11%]
tests/core/base/implementations/test_lazy_loader.py::TestLazyLoader::test_call_first_time PASSED [ 11%]
tests/core/base/implementations/test_lazy_loader.py::TestLazyLoader::test_call_multiple_times PASSED [ 11%]
tests/core/base/implementations/test_lazy_loader.py::TestLazyLoader::test_is_loaded_property PASSED [ 11%]
tests/core/base/implementations/test_lazy_loader.py::TestLazyLoader::test_reset PASSED [ 11%]
tests/core/base/implementations/test_lazy_loader.py::TestLazyLoader::test_thread_safety PASSED [ 12%]
tests/core/base/implementations/test_lazy_loader.py::TestLazyProperty::test_lazy_property_first_access PASSED [ 12%]
tests/core/base/implementations/test_lazy_loader.py::TestLazyProperty::test_lazy_property_multiple_access PASSED [ 12%]
tests/core/base/implementations/test_lazy_loader.py::TestLazyProperty::test_lazy_property_different_instances PASSED [ 12%]
tests/core/base/implementations/test_lazy_loader.py::TestLazyProperty::test_lazy_property_with_complex_object PASSED [ 12%]
tests/core/base/implementations/test_singleton.py::TestSingletonMeta::test_singleton_creates_only_one_instance PASSED [ 12%]
tests/core/base/implementations/test_singleton.py::TestSingletonMeta::test_singleton_different_classes PASSED [ 12%]
tests/core/base/implementations/test_singleton.py::TestSingletonMeta::test_singleton_with_kwargs PASSED [ 12%]
tests/core/base/implementations/test_singleton.py::TestSingletonMeta::test_singleton_without_args PASSED [ 12%]
tests/core/base/implementations/test_singleton.py::TestSingletonMeta::test_singleton_has_initialized_flag PASSED [ 12%]
tests/core/base/implementations/test_singleton.py::TestSingletonMeta::test_singleton_has_instance_class_variable PASSED [ 12%]
tests/core/base/implementations/test_singleton.py::TestSingletonMeta::test_singleton_multiple_inheritance PASSED [ 12%]
tests/core/base/implementations/test_singleton.py::TestSingletonMeta::test_singleton_with_class_method PASSED [ 12%]
tests/core/base/implementations/test_singleton.py::TestSingletonMeta::test_singleton_instances_dict PASSED [ 12%]
tests/core/base/implementations/test_singleton.py::TestSingletonMeta::test_singleton_reset_behavior PASSED [ 12%]
tests/core/base/interfaces/test_component_interface.py::TestCoreComponentsInterface::test_interface_is_abstract PASSED [ 12%]
tests/core/base/interfaces/test_component_interface.py::TestCoreComponentsInterface::test_interface_has_required_methods PASSED [ 12%]
tests/core/base/interfaces/test_component_interface.py::TestCoreComponentsInterface::test_interface_methods_are_abstract PASSED [ 13%]
tests/core/base/interfaces/test_component_interface.py::TestCoreComponentsInterface::test_interface_has_correct_type_hints PASSED [ 13%]
tests/core/base/interfaces/test_component_interface.py::TestCoreComponentsInterface::test_interface_properties_accessible PASSED [ 13%]
tests/core/base/interfaces/test_component_interface.py::TestCoreComponentFactoryInterface::test_interface_is_abstract PASSED [ 13%]
tests/core/base/interfaces/test_component_interface.py::TestCoreComponentFactoryInterface::test_interface_has_required_methods PASSED [ 13%]
tests/core/base/interfaces/test_component_interface.py::TestCoreComponentFactoryInterface::test_interface_methods_are_abstract_and_static PASSED [ 13%]
tests/core/base/interfaces/test_component_interface.py::TestCoreComponentFactoryInterface::test_interface_has_correct_signatures PASSED [ 13%]
tests/core/base/interfaces/test_component_interface.py::TestCoreComponentFactoryInterface::test_all_abstract_methods_implemented PASSED [ 13%]
tests/core/base/interfaces/test_component_interface.py::TestCoreComponentFactoryInterface::test_factory_create_components_with_parameters PASSED [ 13%]
tests/core/base/interfaces/test_component_interface.py::TestCoreComponentFactoryInterface::test_factory_create_with_container_parameter PASSED [ 13%]
tests/core/base/interfaces/test_component_interface.py::TestCoreComponentFactoryInterface::test_factory_create_minimal_implementation PASSED [ 13%]
tests/core/base/interfaces/test_container_interface.py::TestDIContainerInterface::test_interface_is_abstract PASSED [ 13%]
tests/core/base/interfaces/test_container_interface.py::TestDIContainerInterface::test_interface_has_required_methods PASSED [ 13%]
tests/core/base/interfaces/test_container_interface.py::TestDIContainerInterface::test_interface_methods_are_abstract PASSED [ 13%]
tests/core/base/interfaces/test_container_interface.py::TestDIContainerInterface::test_interface_has_correct_type_hints PASSED [ 13%]
tests/core/base/interfaces/test_container_interface.py::TestDIContainerInterface::test_interface_methods_are_callable PASSED [ 13%]
tests/core/base/interfaces/test_container_interface.py::TestDIContainerInterface::test_interface_uses_generic_types PASSED [ 14%]
tests/core/base/interfaces/test_container_interface.py::TestDIContainerInterface::test_mock_implementation_register_instance PASSED [ 14%]
tests/core/base/interfaces/test_container_interface.py::TestDIContainerInterface::test_mock_implementation_register_factory PASSED [ 14%]
tests/core/base/interfaces/test_container_interface.py::TestDIContainerInterface::test_mock_implementation_resolve PASSED [ 14%]
tests/core/base/interfaces/test_container_interface.py::TestDIContainerInterface::test_mock_implementation_register_lazy PASSED [ 14%]
tests/core/base/interfaces/test_container_interface.py::TestDIContainerInterface::test_mock_implementation_get PASSED [ 14%]
tests/core/base/interfaces/test_container_interface.py::TestDIContainerInterface::test_mock_implementation_clear PASSED [ 14%]
tests/core/base/interfaces/test_container_interface.py::TestLazyComponentInterface::test_interface_is_abstract PASSED [ 14%]
tests/core/base/interfaces/test_container_interface.py::TestLazyComponentInterface::test_interface_has_required_methods PASSED [ 14%]
tests/core/base/interfaces/test_container_interface.py::TestLazyComponentInterface::test_interface_methods_are_abstract PASSED [ 14%]
tests/core/base/interfaces/test_container_interface.py::TestLazyComponentInterface::test_interface_has_correct_type_hints PASSED [ 14%]
tests/core/base/interfaces/test_container_interface.py::TestLazyComponentInterface::test_interface_methods_are_callable PASSED [ 14%]
tests/core/base/interfaces/test_container_interface.py::TestLazyComponentInterface::test_interface_defines_lazy_loading_contract PASSED [ 14%]
tests/core/base/interfaces/test_container_interface.py::TestLazyComponentInterface::test_mock_implementation_get PASSED [ 14%]
tests/core/base/interfaces/test_container_interface.py::TestLazyComponentInterface::test_mock_implementation_is_loaded PASSED [ 14%]
tests/core/base/interfaces/test_interfaces_init.py::TestInterfacesInit::test_dicontainer_interface_import PASSED [ 14%]
tests/core/base/interfaces/test_interfaces_init.py::TestInterfacesInit::test_lazy_component_interface_import PASSED [ 14%]
tests/core/base/interfaces/test_interfaces_init.py::TestInterfacesInit::test_core_components_interface_import PASSED [ 15%]
tests/core/base/interfaces/test_interfaces_init.py::TestInterfacesInit::test_core_component_factory_interface_import PASSED [ 15%]
tests/core/base/interfaces/test_interfaces_init.py::TestInterfacesInit::test_all_exports_available PASSED [ 15%]
tests/core/base/interfaces/test_interfaces_init.py::TestInterfacesInit::test_interfaces_are_abstract PASSED [ 15%]
tests/core/base/interfaces/test_interfaces_init.py::TestInterfacesInit::test_dicontainer_interface_methods PASSED [ 15%]
tests/core/base/interfaces/test_interfaces_init.py::TestInterfacesInit::test_lazy_component_interface_methods PASSED [ 15%]
tests/core/base/interfaces/test_interfaces_init.py::TestInterfacesInit::test_core_components_interface_methods PASSED [ 15%]
tests/core/base/interfaces/test_interfaces_init.py::TestInterfacesInit::test_core_component_factory_interface_methods PASSED [ 15%]
tests/core/base/interfaces/test_interfaces_init.py::TestInterfacesInit::test_interfaces_cannot_be_instantiated PASSED [ 15%]
tests/core/base/interfaces/test_interfaces_init.py::TestInterfacesInit::test_interface_methods_are_abstract PASSED [ 15%]
tests/core/base/test_base_init.py::TestBaseInit::test_dicontainer_import PASSED [ 15%]
tests/core/base/test_base_init.py::TestBaseInit::test_core_components_import PASSED [ 15%]
tests/core/base/test_base_init.py::TestBaseInit::test_core_component_factory_import PASSED [ 15%]
tests/core/base/test_base_init.py::TestBaseInit::test_all_exports_available PASSED [ 15%]
tests/core/base/test_base_init.py::TestBaseInit::test_type_checking_imports PASSED [ 15%]
tests/core/base/test_base_init.py::TestBaseInit::test_dicontainer_instantiation PASSED [ 15%]
tests/core/base/test_base_init.py::TestBaseInit::test_core_components_instantiation PASSED [ 15%]
tests/core/base/test_base_init.py::TestBaseInit::test_core_component_factory_instantiation PASSED [ 16%]
tests/core/base/test_factory.py::TestCoreComponentFactory::test_init_with_container PASSED [ 16%]
tests/core/base/test_factory.py::TestCoreComponentFactory::test_logger_property_returns_logger PASSED [ 16%]
tests/core/base/test_factory.py::TestCoreComponentFactory::test_config_manager_property_raises_dependency_error PASSED [ 16%]
tests/core/base/test_factory.py::TestCoreComponentFactory::test_storage_property_raises_dependency_error PASSED [ 16%]
tests/core/base/test_factory.py::TestCoreComponentFactory::test_reset_lazy_loaders PASSED [ 16%]
tests/core/base/test_factory.py::TestCoreComponentFactory::test_validate_dependencies_storage_missing_base_directory PASSED [ 16%]
tests/core/base/test_factory.py::TestCoreComponentFactory::test_validate_dependencies_storage_invalid_path PASSED [ 16%]
tests/core/base/test_factory.py::TestCoreComponentFactory::test_validate_dependencies_storage_valid PASSED [ 16%]
tests/core/base/test_factory.py::TestCoreComponentFactory::test_validate_dependencies_logger_missing_name PASSED [ 16%]
tests/core/base/test_factory.py::TestCoreComponentFactory::test_validate_dependencies_logger_valid PASSED [ 16%]
tests/core/base/test_factory.py::TestCoreComponentFactory::test_validate_dependencies_config_manager_missing_path PASSED [ 16%]
tests/core/base/test_factory.py::TestCoreComponentFactory::test_validate_dependencies_config_manager_nonexistent_file PASSED [ 16%]
tests/core/base/test_factory.py::TestCoreComponentFactory::test_validate_dependencies_config_manager_valid PASSED [ 16%]
tests/core/base/test_factory.py::TestCoreComponentFactory::test_validate_dependencies_invalid_component_type PASSED [ 16%]
tests/core/base/test_factory.py::TestCoreComponentFactory::test_create_components_with_all_paths PASSED [ 16%]
tests/core/base/test_factory.py::TestCoreComponentFactory::test_create_components_without_paths PASSED [ 17%]
tests/core/base/test_factory.py::TestCoreComponentFactory::test_create_with_container PASSED [ 17%]
tests/core/base/test_factory.py::TestCoreComponentFactory::test_create_minimal_with_config_file PASSED [ 17%]
tests/core/base/test_factory.py::TestCoreComponentFactory::test_create_minimal_without_config_file PASSED [ 17%]
tests/core/base/test_factory.py::TestCoreComponentFactory::test_create_minimal_with_config_file_no_logger_section PASSED [ 17%]
tests/core/base/test_factory.py::TestCoreComponentFactory::test_create_logger PASSED [ 17%]
tests/core/base/test_factory.py::TestCoreComponentFactory::test_create_logger_invalid_config PASSED [ 17%]
tests/core/base/test_factory.py::TestCoreComponentFactory::test_create_config_manager PASSED [ 17%]
tests/core/base/test_factory.py::TestCoreComponentFactory::test_create_config_manager_invalid_path PASSED [ 17%]
tests/core/base/test_factory.py::TestCoreComponentFactory::test_create_storage PASSED [ 17%]
tests/core/base/test_factory.py::TestCoreComponentFactory::test_create_storage_invalid_path PASSED [ 17%]
tests/core/base/test_factory.py::TestCoreComponentFactory::test_lazy_property_decorator_exists PASSED [ 17%]
tests/core/base/test_factory.py::TestCoreComponentFactory::test_component_cache_lazy_property PASSED [ 17%]
tests/core/base/test_factory.py::TestCoreComponentFactory::test_get_logger_with_registered_logger PASSED [ 17%]
tests/core/base/test_factory.py::TestCoreComponentFactory::test_get_logger_with_invalid_logger_raises_assertion_error PASSED [ 17%]
tests/core/base/test_factory.py::TestCoreComponentFactory::test_get_config_manager_with_registered_config PASSED [ 17%]
tests/core/base/test_factory.py::TestCoreComponentFactory::test_get_storage_with_registered_storage PASSED [ 17%]
tests/core/base/test_factory.py::TestCoreComponentFactory::test_expensive_config_lazy_property PASSED [ 18%]
tests/core/base/test_factory.py::TestCoreComponentFactory::test_process_config PASSED [ 18%]
tests/core/base/test_factory.py::TestCoreComponentFactory::test_reset_lazy_loaders_clears_lazy_properties PASSED [ 18%]
tests/core/config/exceptions/test_config_error_comprehensive.py::TestConfigError::test_base_error_creation PASSED [ 18%]
tests/core/config/exceptions/test_config_error_comprehensive.py::TestConfigError::test_base_error_with_code PASSED [ 18%]
tests/core/config/exceptions/test_config_error_comprehensive.py::TestConfigLoadError::test_load_error_creation PASSED [ 18%]
tests/core/config/exceptions/test_config_error_comprehensive.py::TestConfigLoadError::test_load_error_without_optional_params PASSED [ 18%]
tests/core/config/exceptions/test_config_error_comprehensive.py::TestConfigSaveError::test_save_error_creation PASSED [ 18%]
tests/core/config/exceptions/test_config_error_comprehensive.py::TestConfigSaveError::test_save_error_without_optional_params PASSED [ 18%]
tests/core/config/exceptions/test_config_error_comprehensive.py::TestConfigValidationError::test_validation_error_creation PASSED [ 18%]
tests/core/config/exceptions/test_config_error_comprehensive.py::TestConfigValidationError::test_validation_error_without_optional_params PASSED [ 18%]
tests/core/config/exceptions/test_config_error_comprehensive.py::TestConfigTypeError::test_type_error_creation PASSED [ 18%]
tests/core/config/exceptions/test_config_error_comprehensive.py::TestConfigTypeError::test_type_error_without_optional_params PASSED [ 18%]
tests/core/config/exceptions/test_config_error_comprehensive.py::TestConfigKeyError::test_key_error_creation PASSED [ 18%]
tests/core/config/exceptions/test_config_error_comprehensive.py::TestConfigKeyError::test_key_error_without_optional_params PASSED [ 18%]
tests/core/config/exceptions/test_config_error_comprehensive.py::TestConfigKeyError::test_key_error_with_none_available_keys PASSED [ 18%]
tests/core/config/exceptions/test_config_error_comprehensive.py::TestExceptionHierarchy::test_exception_inheritance PASSED [ 19%]
tests/core/config/exceptions/test_config_error_comprehensive.py::TestExceptionHierarchy::test_exception_is_exception PASSED [ 19%]
tests/core/config/implementations/test_config_implementations_init.py::TestConfigImplementationsInit::test_version_and_constants_loaded PASSED [ 19%]
tests/core/config/implementations/test_config_implementations_init.py::TestConfigImplementationsInit::test_version_fallback_on_package_not_found PASSED [ 19%]
tests/core/config/implementations/test_config_implementations_init.py::TestConfigImplementationsInit::test_all_imports_available PASSED [ 19%]
tests/core/config/implementations/test_config_implementations_init.py::TestConfigImplementationsInit::test_all_list_contains_expected_exports PASSED [ 19%]
tests/core/config/implementations/test_dynamic_config_manager.py::TestDynamicConfigManagerInit::test_init_without_session_raises_value_error PASSED [ 19%]
tests/core/config/implementations/test_dynamic_config_manager.py::TestDynamicConfigManagerInit::test_init_with_session_success PASSED [ 19%]
tests/core/config/implementations/test_dynamic_config_manager.py::TestDynamicConfigManagerInit::test_init_with_session_and_logger_success PASSED [ 19%]
tests/core/config/implementations/test_dynamic_config_manager.py::TestDynamicConfigManagerGet::test_get_with_multiple_keys_raises_value_error PASSED [ 19%]
tests/core/config/implementations/test_dynamic_config_manager.py::TestDynamicConfigManagerGet::test_get_from_cache PASSED [ 19%]
tests/core/config/implementations/test_dynamic_config_manager.py::TestDynamicConfigManagerGet::test_get_from_database_success PASSED [ 19%]
tests/core/config/implementations/test_dynamic_config_manager.py::TestDynamicConfigManagerGet::test_get_from_database_not_found_returns_default PASSED [ 19%]
tests/core/config/implementations/test_dynamic_config_manager.py::TestDynamicConfigManagerGet::test_get_database_error_raises_config_error PASSED [ 19%]
tests/core/config/implementations/test_dynamic_config_manager.py::TestDynamicConfigManagerSet::test_set_with_multiple_keys_raises_value_error PASSED [ 19%]
tests/core/config/implementations/test_dynamic_config_manager.py::TestDynamicConfigManagerSet::test_set_new_config_success PASSED [ 19%]
tests/core/config/implementations/test_dynamic_config_manager.py::TestDynamicConfigManagerSet::test_set_existing_config_success PASSED [ 19%]
tests/core/config/implementations/test_dynamic_config_manager.py::TestDynamicConfigManagerSet::test_set_database_error_raises_config_error PASSED [ 20%]
tests/core/config/implementations/test_dynamic_config_manager.py::TestDynamicConfigManagerGetSection::test_get_section_success PASSED [ 20%]
tests/core/config/implementations/test_dynamic_config_manager.py::TestDynamicConfigManagerGetSection::test_get_section_not_found_raises_key_error PASSED [ 20%]
tests/core/config/implementations/test_dynamic_config_manager.py::TestDynamicConfigManagerGetSection::test_get_section_database_error_raises_config_error PASSED [ 20%]
tests/core/config/implementations/test_dynamic_config_manager.py::TestDynamicConfigManagerNotImplementedMethods::test_save_raises_not_implemented_error PASSED [ 20%]
tests/core/config/implementations/test_dynamic_config_manager.py::TestDynamicConfigManagerNotImplementedMethods::test_load_raises_not_implemented_error PASSED [ 20%]
tests/core/config/implementations/test_dynamic_config_manager.py::TestDynamicConfigManagerNotImplementedMethods::test_load_directory_raises_not_implemented_error PASSED [ 20%]
tests/core/config/implementations/test_dynamic_config_manager.py::TestDynamicConfigManagerValidate::test_validate_success PASSED [ 20%]
tests/core/config/implementations/test_dynamic_config_manager.py::TestDynamicConfigManagerValidate::test_validate_missing_required_field PASSED [ 20%]
tests/core/config/implementations/test_dynamic_config_manager.py::TestDynamicConfigManagerValidate::test_validate_invalid_type PASSED [ 20%]
tests/core/config/implementations/test_dynamic_config_manager.py::TestDynamicConfigManagerListeners::test_add_listener_success PASSED [ 20%]
tests/core/config/implementations/test_dynamic_config_manager.py::TestDynamicConfigManagerListeners::test_remove_listener_success PASSED [ 20%]
tests/core/config/implementations/test_dynamic_config_manager.py::TestDynamicConfigManagerListeners::test_remove_nonexistent_listener_no_error PASSED [ 20%]
tests/core/config/implementations/test_dynamic_config_manager.py::TestDynamicConfigManagerHotReload::test_start_hot_reload_success PASSED [ 20%]
tests/core/config/implementations/test_dynamic_config_manager.py::TestDynamicConfigManagerHotReload::test_start_hot_reload_when_already_running_raises_runtime_error PASSED [ 20%]
tests/core/config/implementations/test_dynamic_config_manager.py::TestDynamicConfigManagerHotReload::test_stop_hot_reload_success PASSED [ 20%]
tests/core/config/implementations/test_dynamic_config_manager.py::TestDynamicConfigManagerHotReload::test_stop_hot_reload_when_not_running_no_error PASSED [ 20%]
tests/core/config/implementations/test_dynamic_config_manager.py::TestDynamicConfigManagerGetAll::test_get_all_success PASSED [ 21%]
tests/core/config/implementations/test_dynamic_config_manager.py::TestDynamicConfigManagerGetAll::test_get_all_with_category_filter PASSED [ 21%]
tests/core/config/implementations/test_dynamic_config_manager.py::TestDynamicConfigManagerGetAll::test_get_all_database_error_raises_config_error PASSED [ 21%]
tests/core/config/implementations/test_dynamic_config_manager.py::TestDynamicConfigManagerSetWithMetadata::test_set_with_metadata_new_config_success PASSED [ 21%]
tests/core/config/implementations/test_dynamic_config_manager.py::TestDynamicConfigManagerSetWithMetadata::test_set_with_metadata_existing_config_success PASSED [ 21%]
tests/core/config/implementations/test_dynamic_config_manager.py::TestDynamicConfigManagerDelete::test_delete_existing_config_success PASSED [ 21%]
tests/core/config/implementations/test_dynamic_config_manager.py::TestDynamicConfigManagerDelete::test_delete_nonexistent_config_returns_false PASSED [ 21%]
tests/core/config/implementations/test_dynamic_config_manager.py::TestDynamicConfigManagerDelete::test_delete_database_error_raises_config_error PASSED [ 21%]
tests/core/config/implementations/test_dynamic_config_manager.py::TestDynamicConfigManagerDetermineValueType::test_determine_value_type_bool PASSED [ 21%]
tests/core/config/implementations/test_dynamic_config_manager.py::TestDynamicConfigManagerDetermineValueType::test_determine_value_type_int PASSED [ 21%]
tests/core/config/implementations/test_dynamic_config_manager.py::TestDynamicConfigManagerDetermineValueType::test_determine_value_type_float PASSED [ 21%]
tests/core/config/implementations/test_dynamic_config_manager.py::TestDynamicConfigManagerDetermineValueType::test_determine_value_type_str PASSED [ 21%]
tests/core/config/implementations/test_dynamic_config_manager.py::TestDynamicConfigManagerDetermineValueType::test_determine_value_type_list PASSED [ 21%]
tests/core/config/implementations/test_dynamic_config_manager.py::TestDynamicConfigManagerDetermineValueType::test_determine_value_type_dict PASSED [ 21%]
tests/core/config/implementations/test_dynamic_config_manager.py::TestDynamicConfigManagerDetermineValueType::test_determine_value_type_unknown_defaults_to_str PASSED [ 21%]
tests/core/config/implementations/test_dynamic_config_manager.py::TestDynamicConfigManagerNotifyListeners::test_notify_listeners_success PASSED [ 21%]
tests/core/config/implementations/test_dynamic_config_manager.py::TestDynamicConfigManagerNotifyListeners::test_notify_listeners_with_exception_in_listener PASSED [ 22%]
tests/core/config/implementations/test_dynamic_config_manager.py::TestDynamicConfigManagerCheckForUpdates::test_check_for_updates_first_time_loads_all PASSED [ 22%]
tests/core/config/implementations/test_dynamic_config_manager.py::TestDynamicConfigManagerCheckForUpdates::test_check_for_updates_with_changes PASSED [ 22%]
tests/core/config/implementations/test_dynamic_config_manager.py::TestDynamicConfigManagerCheckForUpdates::test_check_for_updates_database_error_logged PASSED [ 22%]
tests/core/config/implementations/test_dynamic_config_manager_comprehensive.py::TestDynamicConfigManagerComprehensive::test_get_logs_error_on_exception PASSED [ 22%]
tests/core/config/implementations/test_dynamic_config_manager_comprehensive.py::TestDynamicConfigManagerComprehensive::test_set_logs_info_on_success PASSED [ 22%]
tests/core/config/implementations/test_dynamic_config_manager_comprehensive.py::TestDynamicConfigManagerComprehensive::test_set_logs_error_on_exception PASSED [ 22%]
tests/core/config/implementations/test_dynamic_config_manager_comprehensive.py::TestDynamicConfigManagerComprehensive::test_get_section_logs_error_on_exception PASSED [ 22%]
tests/core/config/implementations/test_dynamic_config_manager_comprehensive.py::TestDynamicConfigManagerComprehensive::test_start_hot_reload_logs_info_and_error PASSED [ 22%]
tests/core/config/implementations/test_dynamic_config_manager_comprehensive.py::TestDynamicConfigManagerComprehensive::test_stop_hot_reload_logs_warning_on_timeout PASSED [ 22%]
tests/core/config/implementations/test_dynamic_config_manager_comprehensive.py::TestDynamicConfigManagerComprehensive::test_stop_hot_reload_logs_info_on_successful_stop PASSED [ 22%]
tests/core/config/implementations/test_dynamic_config_manager_comprehensive.py::TestDynamicConfigManagerComprehensive::test_get_all_logs_error_on_exception PASSED [ 22%]
tests/core/config/implementations/test_dynamic_config_manager_comprehensive.py::TestDynamicConfigManagerComprehensive::test_set_with_metadata_logs_info_and_error PASSED [ 22%]
tests/core/config/implementations/test_dynamic_config_manager_comprehensive.py::TestDynamicConfigManagerComprehensive::test_delete_logs_info_and_error PASSED [ 22%]
tests/core/config/implementations/test_dynamic_config_manager_comprehensive.py::TestDynamicConfigManagerComprehensive::test_notify_listeners_logs_error PASSED [ 22%]
tests/core/config/implementations/test_dynamic_config_manager_comprehensive.py::TestDynamicConfigManagerComprehensive::test_check_for_updates_logs_error PASSED [ 22%]
tests/core/config/implementations/test_dynamic_config_manager_comprehensive.py::TestDynamicConfigManagerComprehensive::test_add_and_remove_listener_logging PASSED [ 22%]
tests/core/config/implementations/test_yaml_config_manager.py::TestValidationContext::test_initialization PASSED [ 23%]
tests/core/config/implementations/test_yaml_config_manager.py::TestValidationContext::test_initialization_with_none_value PASSED [ 23%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_initialization_without_filename PASSED [ 23%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_initialization_with_filename PASSED [ 23%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_get_current_schema_version PASSED [ 23%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_check_schema_compatibility PASSED [ 23%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_ensure_dict_with_dict PASSED [ 23%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_ensure_dict_with_none PASSED [ 23%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_ensure_dict_with_invalid_type PASSED [ 23%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_get_existing_value PASSED [ 23%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_get_nonexistent_value_with_default PASSED [ 23%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_get_nonexistent_path PASSED [ 23%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_get_section_existing PASSED [ 23%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_get_section_nonexistent PASSED [ 23%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_set_single_key PASSED [ 23%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_set_nested_keys PASSED [ 23%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_set_without_keys PASSED [ 23%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_set_overwriting_value PASSED [ 24%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_save_with_filename PASSED [ 24%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_save_without_filename PASSED [ 24%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_save_with_manager_filename PASSED [ 24%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_load_existing_file PASSED [ 24%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_load_nonexistent_file PASSED [ 24%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_load_invalid_yaml PASSED [ 24%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_load_with_schema_version PASSED [ 24%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_validate_valid_config PASSED [ 24%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_validate_invalid_type PASSED [ 24%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_validate_missing_required PASSED [ 24%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_validate_optional_field PASSED [ 24%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_validate_choices_valid PASSED [ 24%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_validate_choices_invalid PASSED [ 24%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_validate_range_valid PASSED [ 24%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_validate_range_invalid_min PASSED [ 24%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_validate_range_invalid_max PASSED [ 25%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_validate_nested_dict PASSED [ 25%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_validate_nested_dict_invalid PASSED [ 25%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_load_directory PASSED [ 25%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_load_directory_nonexistent PASSED [ 25%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_load_directory_not_a_directory PASSED [ 25%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_validate_dict_with_non_dict_value PASSED [ 25%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_validate_unsupported_type PASSED [ 25%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_save_creates_directory PASSED [ 25%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_save_error_handling PASSED [ 25%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_get_with_logger_debug PASSED [ 25%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_set_nested_creates_intermediate_dicts PASSED [ 25%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_load_with_incompatible_schema_version_warning PASSED [ 25%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_validate_dict_with_dict_value PASSED [ 25%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_validate_type_with_none_value PASSED [ 25%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_validate_nested_dict_valid PASSED [ 25%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_load_directory_logs_debug_messages PASSED [ 25%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_load_directory_system_yaml_special_handling PASSED [ 26%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_get_without_logger_no_debug PASSED [ 26%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_set_creates_intermediate_dicts_edge_case PASSED [ 26%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_validate_dict_with_none_value PASSED [ 26%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_validate_type_with_no_type_specified PASSED [ 26%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_validate_nested_without_schema PASSED [ 26%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_load_directory_without_logger_no_debug PASSED [ 26%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_load_directory_system_yaml_no_overwrite PASSED [ 26%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_get_returns_default_when_current_not_dict PASSED [ 26%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_set_raises_error_when_intermediate_not_dict PASSED [ 26%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_validate_dict_with_non_dict_value_error_path PASSED [ 26%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_validate_nested_with_non_dict_value_error_path PASSED [ 26%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_load_directory_error_handling PASSED [ 26%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_validate_dict_with_non_dict_no_type_specified PASSED [ 26%]
tests/core/config/implementations/test_yaml_config_manager.py::TestYAMLConfigManager::test_validate_nested_with_non_dict_no_type_specified PASSED [ 26%]
tests/core/config/interfaces/test_async_config_interface.py::TestAsyncConfigManagerInterface::test_interface_is_abstract PASSED [ 26%]
tests/core/config/interfaces/test_async_config_interface.py::TestAsyncConfigManagerInterface::test_interface_has_abstract_methods PASSED [ 26%]
tests/core/config/interfaces/test_async_config_interface.py::TestAsyncConfigManagerInterface::test_interface_method_signatures PASSED [ 27%]
tests/core/config/interfaces/test_async_config_interface.py::TestAsyncConfigManagerInterface::test_config_listener_type_alias PASSED [ 27%]
tests/core/config/interfaces/test_async_config_interface.py::TestAsyncConfigManagerInterface::test_implementation_can_be_instantiated PASSED [ 27%]
tests/core/config/interfaces/test_async_config_interface.py::TestAsyncConfigManagerInterface::test_implementation_has_all_methods PASSED [ 27%]
tests/core/config/interfaces/test_async_config_interface.py::TestAsyncConfigManagerInterface::test_async_methods_are_awaitable PASSED [ 27%]
tests/core/config/interfaces/test_async_config_interface.py::TestAsyncConfigManagerInterface::test_sync_methods_are_callable PASSED [ 27%]
tests/core/config/interfaces/test_async_config_interface.py::TestAsyncConfigManagerInterface::test_interface_enforces_method_implementation PASSED [ 27%]
tests/core/config/interfaces/test_async_config_interface.py::TestAsyncConfigManagerInterface::test_interface_docstrings_present PASSED [ 27%]
tests/core/config/interfaces/test_async_config_interface.py::TestAsyncConfigManagerInterface::test_interface_method_order PASSED [ 27%]
tests/core/config/interfaces/test_async_config_interface.py::TestAsyncConfigManagerInterface::test_constructor_accepts_optional_params PASSED [ 27%]
tests/core/config/interfaces/test_async_config_interface.py::TestAsyncConfigManagerInterface::test_get_method_accepts_variable_keys PASSED [ 27%]
tests/core/config/interfaces/test_async_config_interface.py::TestAsyncConfigManagerInterface::test_get_method_returns_default PASSED [ 27%]
tests/core/config/interfaces/test_async_config_interface.py::TestAsyncConfigManagerInterface::test_set_method_accepts_variable_keys PASSED [ 27%]
tests/core/config/interfaces/test_async_config_interface.py::TestAsyncConfigManagerInterface::test_get_section_returns_dict PASSED [ 27%]
tests/core/config/interfaces/test_async_config_interface.py::TestAsyncConfigManagerInterface::test_validate_returns_tuple PASSED [ 27%]
tests/core/config/interfaces/test_async_config_interface.py::TestAsyncConfigManagerInterface::test_save_accepts_optional_filename PASSED [ 27%]
tests/core/config/interfaces/test_async_config_interface.py::TestAsyncConfigManagerInterface::test_load_accepts_filename PASSED [ 28%]
tests/core/config/interfaces/test_async_config_interface.py::TestAsyncConfigManagerInterface::test_load_directory_accepts_path PASSED [ 28%]
tests/core/config/interfaces/test_async_config_interface.py::TestAsyncConfigManagerInterface::test_start_hot_reload_accepts_interval PASSED [ 28%]
tests/core/config/interfaces/test_async_config_interface.py::TestAsyncConfigManagerInterface::test_stop_hot_reload_is_callable PASSED [ 28%]
tests/core/config/interfaces/test_async_config_interface.py::TestAsyncConfigManagerInterface::test_get_all_accepts_optional_category PASSED [ 28%]
tests/core/config/interfaces/test_async_config_interface.py::TestAsyncConfigManagerInterface::test_set_with_metadata_accepts_params PASSED [ 28%]
tests/core/config/interfaces/test_async_config_interface.py::TestAsyncConfigManagerInterface::test_delete_returns_bool PASSED [ 28%]
tests/core/config/interfaces/test_config_interface.py::TestConfigManagerInterface::test_interface_is_abstract PASSED [ 28%]
tests/core/config/interfaces/test_config_interface.py::TestConfigManagerInterface::test_interface_has_abstract_methods PASSED [ 28%]
tests/core/config/interfaces/test_config_interface.py::TestConfigManagerInterface::test_interface_method_signatures PASSED [ 28%]
tests/core/config/interfaces/test_config_interface.py::TestConfigManagerInterface::test_implementation_can_be_instantiated PASSED [ 28%]
tests/core/config/interfaces/test_config_interface.py::TestConfigManagerInterface::test_implementation_has_all_methods PASSED [ 28%]
tests/core/config/interfaces/test_config_interface.py::TestConfigManagerInterface::test_get_method_accepts_variable_keys PASSED [ 28%]
tests/core/config/interfaces/test_config_interface.py::TestConfigManagerInterface::test_get_method_returns_default PASSED [ 28%]
tests/core/config/interfaces/test_config_interface.py::TestConfigManagerInterface::test_set_method_accepts_variable_keys PASSED [ 28%]
tests/core/config/interfaces/test_config_interface.py::TestConfigManagerInterface::test_get_section_returns_dict PASSED [ 28%]
tests/core/config/interfaces/test_config_interface.py::TestConfigManagerInterface::test_validate_returns_tuple PASSED [ 28%]
tests/core/config/interfaces/test_config_interface.py::TestConfigManagerInterface::test_save_accepts_optional_filename PASSED [ 29%]
tests/core/config/interfaces/test_config_interface.py::TestConfigManagerInterface::test_load_accepts_filename PASSED [ 29%]
tests/core/config/interfaces/test_config_interface.py::TestConfigManagerInterface::test_load_directory_accepts_path PASSED [ 29%]
tests/core/config/interfaces/test_config_interface.py::TestConfigManagerInterface::test_interface_enforces_method_implementation PASSED [ 29%]
tests/core/config/interfaces/test_config_interface.py::TestConfigManagerInterface::test_implementation_preserves_type_hints PASSED [ 29%]
tests/core/config/interfaces/test_config_interface.py::TestConfigManagerInterface::test_interface_docstrings_present PASSED [ 29%]
tests/core/config/interfaces/test_config_interface.py::TestConfigManagerInterface::test_interface_method_order PASSED [ 29%]
tests/core/config/interfaces/test_factory_interface.py::TestConfigManagerFactoryInterface::test_interface_is_abstract PASSED [ 29%]
tests/core/config/interfaces/test_factory_interface.py::TestConfigManagerFactoryInterface::test_interface_has_abstract_methods PASSED [ 29%]
tests/core/config/interfaces/test_factory_interface.py::TestConfigManagerFactoryInterface::test_interface_methods_are_classmethods PASSED [ 29%]
tests/core/config/interfaces/test_factory_interface.py::TestConfigManagerFactoryInterface::test_interface_method_signatures PASSED [ 29%]
tests/core/config/interfaces/test_factory_interface.py::TestConfigManagerFactoryInterface::test_implementation_can_be_instantiated PASSED [ 29%]
tests/core/config/interfaces/test_factory_interface.py::TestConfigManagerFactoryInterface::test_implementation_has_all_methods PASSED [ 29%]
tests/core/config/interfaces/test_factory_interface.py::TestConfigManagerFactoryInterface::test_register_manager_method PASSED [ 29%]
tests/core/config/interfaces/test_factory_interface.py::TestConfigManagerFactoryInterface::test_get_manager_method PASSED [ 29%]
tests/core/config/interfaces/test_factory_interface.py::TestConfigManagerFactoryInterface::test_get_manager_with_type PASSED [ 29%]
tests/core/config/interfaces/test_factory_interface.py::TestConfigManagerFactoryInterface::test_get_manager_with_invalid_extension PASSED [ 30%]
tests/core/config/interfaces/test_factory_interface.py::TestConfigManagerFactoryInterface::test_get_manager_with_invalid_type PASSED [ 30%]
tests/core/config/interfaces/test_factory_interface.py::TestConfigManagerFactoryInterface::test_create_manager_method PASSED [ 30%]
tests/core/config/interfaces/test_factory_interface.py::TestConfigManagerFactoryInterface::test_create_manager_with_kwargs PASSED [ 30%]
tests/core/config/interfaces/test_factory_interface.py::TestConfigManagerFactoryInterface::test_create_manager_with_invalid_type PASSED [ 30%]
tests/core/config/interfaces/test_factory_interface.py::TestConfigManagerFactoryInterface::test_interface_enforces_method_implementation PASSED [ 30%]
tests/core/config/interfaces/test_factory_interface.py::TestConfigManagerFactoryInterface::test_interface_docstrings_present PASSED [ 30%]
tests/core/config/interfaces/test_factory_interface.py::TestConfigManagerFactoryInterface::test_interface_method_order PASSED [ 30%]
tests/core/config/interfaces/test_factory_interface.py::TestConfigManagerFactoryInterface::test_register_manager_raises_not_implemented_error PASSED [ 30%]
tests/core/config/interfaces/test_factory_interface.py::TestConfigManagerFactoryInterface::test_get_manager_raises_not_implemented_error PASSED [ 30%]
tests/core/config/interfaces/test_factory_interface.py::TestConfigManagerFactoryInterface::test_create_manager_raises_not_implemented_error PASSED [ 30%]
tests/core/config/interfaces/test_factory_interface.py::TestConfigManagerFactoryInterface::test_factory_returns_config_manager_interface PASSED [ 30%]
tests/core/config/interfaces/test_factory_interface.py::TestConfigManagerFactoryInterface::test_factory_creates_separate_instances PASSED [ 30%]
tests/core/config/interfaces/test_factory_interface.py::TestConfigManagerFactoryInterface::test_factory_supports_multiple_manager_types PASSED [ 30%]
tests/core/config/test_config_factory.py::TestConfigManagerFactory::test_get_manager_should_return_valid_interface PASSED [ 30%]
tests/core/config/test_config_factory.py::TestConfigManagerFactory::test_get_manager_with_invalid_extension_should_raise_error PASSED [ 30%]
tests/core/config/test_config_factory.py::TestConfigManagerFactory::test_get_async_manager_should_return_valid_interface PASSED [ 30%]
tests/core/config/test_config_factory.py::TestConfigManagerFactory::test_get_async_manager_should_be_created PASSED [ 31%]
tests/core/config/test_config_factory.py::TestConfigManagerFactory::test_get_manager_should_handle_yaml_extension PASSED [ 31%]
tests/core/config/test_config_factory.py::TestConfigManagerFactory::test_get_manager_should_handle_yml_extension PASSED [ 31%]
tests/core/config/test_config_factory.py::TestConfigManagerFactory::test_get_manager_without_extension_should_use_default_yaml PASSED [ 31%]
tests/core/config/test_config_factory.py::TestConfigManagerFactory::test_create_manager_should_return_valid_interface PASSED [ 31%]
tests/core/config/test_config_factory.py::TestConfigManagerFactory::test_create_manager_with_invalid_type_should_raise_error PASSED [ 31%]
tests/core/config/test_config_factory.py::TestConfigManagerFactory::test_get_async_manager_with_invalid_type_should_raise_error PASSED [ 31%]
tests/core/config/test_config_factory.py::TestConfigManagerFactory::test_get_supported_extensions_should_return_list PASSED [ 31%]
tests/core/config/test_config_factory.py::TestConfigManagerFactory::test_get_supported_async_types_should_return_list PASSED [ 31%]
tests/core/config/test_config_factory.py::TestConfigManagerFactory::test_register_manager_should_add_new_manager PASSED [ 31%]
tests/core/config/test_config_factory.py::TestConfigManagerFactory::test_register_manager_with_invalid_class_should_raise_error PASSED [ 31%]
tests/core/config/test_config_factory.py::TestConfigManagerFactory::test_get_async_manager_should_pass_session_and_logger PASSED [ 31%]
tests/core/config/test_config_factory.py::TestConfigManagerFactory::test_get_manager_should_create_separate_instances PASSED [ 31%]
tests/core/config/test_config_factory.py::TestConfigManagerFactory::test_get_async_manager_should_handle_valid_kwargs PASSED [ 31%]
tests/core/config/test_config_factory.py::TestConfigManagerFactory::test_register_async_manager_should_add_new_async_manager PASSED [ 31%]
tests/core/config/test_config_factory.py::TestConfigManagerFactory::test_register_async_manager_with_invalid_class_should_raise_error PASSED [ 31%]
tests/core/config/test_config_factory.py::TestConfigManagerFactory::test_get_async_manager_without_session_should_raise_error PASSED [ 31%]
tests/core/config/test_config_factory.py::TestConfigManagerFactory::test_get_manager_with_explicit_type_should_use_that_type PASSED [ 32%]
tests/core/config/test_config_factory.py::TestConfigManagerFactory::test_register_manager_should_normalize_extension PASSED [ 32%]
tests/core/config/test_config_factory.py::TestConfigManagerFactory::test_register_manager_should_validate_extension_not_empty PASSED [ 32%]
tests/core/config/test_config_factory.py::TestConfigManagerFactory::test_register_manager_should_validate_manager_is_type PASSED [ 32%]
tests/core/config/test_config_factory.py::TestConfigManagerFactory::test_register_manager_should_validate_interface_implementation PASSED [ 32%]
tests/core/config/test_config_factory.py::TestConfigManagerFactory::test_register_async_manager_should_validate_manager_type_not_empty PASSED [ 32%]
tests/core/config/test_config_factory.py::TestConfigManagerFactory::test_register_async_manager_should_validate_async_manager_is_type PASSED [ 32%]
tests/core/config/test_config_factory.py::TestConfigManagerFactory::test_get_manager_with_explicit_type_should_normalize_type PASSED [ 32%]
tests/core/config/test_config_factory.py::TestConfigManagerFactory::test_register_async_manager_should_validate_async_interface_implementation PASSED [ 32%]
tests/core/config/test_config_factory.py::TestConfigManagerFactory::test_get_manager_with_explicit_type_should_handle_dot_prefix PASSED [ 32%]
tests/core/config/test_config_factory.py::TestConfigManagerFactory::test_get_manager_with_explicit_type_should_raise_error_for_invalid_type PASSED [ 32%]
tests/core/config/test_processors_config.py::TestProcessorsConfig::test_processors_config_loaded PASSED [ 32%]
tests/core/config/test_processors_config.py::TestProcessorsConfig::test_d01_processor_config_exists PASSED [ 32%]
tests/core/config/test_processors_config.py::TestProcessorsConfig::test_required_timeframes_config PASSED [ 32%]
tests/core/config/test_processors_config.py::TestProcessorsConfig::test_timeframe_configs_structure PASSED [ 32%]
tests/core/config/test_processors_config.py::TestProcessorsConfig::test_tick_timeframe_config PASSED [ 32%]
tests/core/config/test_processors_config.py::TestProcessorsConfig::test_1m_timeframe_config PASSED [ 33%]
tests/core/config/test_processors_config.py::TestProcessorsConfig::test_general_z_score_window_config PASSED [ 33%]
tests/core/config/test_processors_config.py::TestProcessorsConfig::test_calc_shadows_config PASSED [ 33%]
tests/core/config/test_processors_config.py::TestProcessorsConfig::test_timeframe_configs_keys_exist PASSED [ 33%]
tests/core/config/test_processors_config.py::TestProcessorsConfig::test_timeframe_configs_z_score_window_type PASSED [ 33%]
tests/core/config/test_processors_config.py::TestProcessorsConfig::test_config_section_accessible_via_get_section PASSED [ 33%]
tests/core/config/test_processors_config.py::TestProcessorsConfig::test_d02_processor_config_exists PASSED [ 33%]
tests/core/config/test_processors_config.py::TestProcessorsConfig::test_d02_swing_window_config PASSED [ 33%]
tests/core/config/test_processors_config.py::TestProcessorsConfig::test_d02_min_distance_config PASSED [ 33%]
tests/core/config/test_processors_config.py::TestProcessorsConfig::test_d02_use_close_open_config PASSED [ 33%]
tests/core/config/test_processors_config.py::TestProcessorsConfig::test_d02_use_high_low_config PASSED [ 33%]
tests/core/config/test_processors_config.py::TestProcessorsConfig::test_d02_primary_weight_config PASSED [ 33%]
tests/core/config/test_processors_config.py::TestProcessorsConfig::test_d02_secondary_weight_config PASSED [ 33%]
tests/core/config/test_processors_config.py::TestProcessorsConfig::test_d02_level_merge_config PASSED [ 33%]
tests/core/config/test_processors_config.py::TestProcessorsConfig::test_d02_min_touches_config PASSED [ 33%]
tests/core/config/test_processors_config.py::TestProcessorsConfig::test_d02_volume_confirmation_config PASSED [ 33%]
tests/core/config/test_processors_config.py::TestProcessorsConfig::test_d02_strength_window_config PASSED [ 33%]
tests/core/config/test_processors_config.py::TestProcessorsConfig::test_d02_timeframe_configs_structure PASSED [ 34%]
tests/core/config/test_processors_config.py::TestProcessorsConfig::test_d02_m1_timeframe_config PASSED [ 34%]
tests/core/config/test_processors_config.py::TestProcessorsConfig::test_d02_h1_timeframe_config PASSED [ 34%]
tests/core/config/test_processors_config.py::TestProcessorsConfig::test_d02_d1_timeframe_config PASSED [ 34%]
tests/core/db/exceptions/test_db_error.py::TestDatabaseError::test_database_error_creation PASSED [ 34%]
tests/core/db/exceptions/test_db_error.py::TestDatabaseError::test_database_error_with_details PASSED [ 34%]
tests/core/db/exceptions/test_db_error.py::TestDatabaseError::test_database_error_is_neural_ai_exception PASSED [ 34%]
tests/core/db/exceptions/test_db_error.py::TestDBConnectionError::test_db_connection_error_creation PASSED [ 34%]
tests/core/db/exceptions/test_db_error.py::TestDBConnectionError::test_db_connection_error_with_connection_string PASSED [ 34%]
tests/core/db/exceptions/test_db_error.py::TestDBConnectionError::test_db_connection_error_inheritance PASSED [ 34%]
tests/core/db/exceptions/test_db_error.py::TestTransactionError::test_transaction_error_creation PASSED [ 34%]
tests/core/db/exceptions/test_db_error.py::TestTransactionError::test_transaction_error_with_transaction_id PASSED [ 34%]
tests/core/db/exceptions/test_db_error.py::TestTransactionError::test_transaction_error_inheritance PASSED [ 34%]
tests/core/db/exceptions/test_db_exceptions_init.py::TestExceptionsInit::test_database_error_import PASSED [ 34%]
tests/core/db/exceptions/test_db_exceptions_init.py::TestExceptionsInit::test_db_connection_error_import PASSED [ 34%]
tests/core/db/exceptions/test_db_exceptions_init.py::TestExceptionsInit::test_transaction_error_import PASSED [ 34%]
tests/core/db/exceptions/test_db_exceptions_init.py::TestExceptionsInit::test_all_list_content PASSED [ 34%]
tests/core/db/exceptions/test_db_exceptions_init.py::TestExceptionsInit::test_exception_instantiation PASSED [ 35%]
tests/core/db/implementations/test_db_implementations_init.py::TestImplementationsInit::test_base_model_import PASSED [ 35%]
tests/core/db/implementations/test_db_implementations_init.py::TestImplementationsInit::test_models_import PASSED [ 35%]
tests/core/db/implementations/test_db_implementations_init.py::TestImplementationsInit::test_session_functions_import PASSED [ 35%]
tests/core/db/implementations/test_db_implementations_init.py::TestImplementationsInit::test_classes_import PASSED [ 35%]
tests/core/db/implementations/test_db_implementations_init.py::TestImplementationsInit::test_helper_functions_import PASSED [ 35%]
tests/core/db/implementations/test_db_implementations_init.py::TestImplementationsInit::test_all_imports_are_not_none PASSED [ 35%]
tests/core/db/implementations/test_db_implementations_init.py::TestImplementationsInit::test_all_list_content PASSED [ 35%]
tests/core/db/implementations/test_db_implementations_init.py::TestImplementationsInit::test_model_base_relationship PASSED [ 35%]
tests/core/db/implementations/test_model_base.py::TestBase::test_base_initialization PASSED [ 35%]
tests/core/db/implementations/test_model_base.py::TestBase::test_id_column_properties PASSED [ 35%]
tests/core/db/implementations/test_model_base.py::TestBase::test_created_at_column_properties PASSED [ 35%]
tests/core/db/implementations/test_model_base.py::TestBase::test_updated_at_column_properties PASSED [ 35%]
tests/core/db/implementations/test_model_base.py::TestBase::test_automatic_tablename_generation PASSED [ 35%]
tests/core/db/implementations/test_model_base.py::TestBase::test_model_creation_with_defaults PASSED [ 35%]
tests/core/db/implementations/test_model_base.py::TestBase::test_to_dict_method PASSED [ 35%]
tests/core/db/implementations/test_model_base.py::TestBase::test_to_dict_datetime_isoformat PASSED [ 36%]
tests/core/db/implementations/test_model_base.py::TestBase::test_repr_method PASSED [ 36%]
tests/core/db/implementations/test_model_base.py::TestBase::test_updated_at_changes_on_update PASSED [ 36%]
tests/core/db/implementations/test_model_base.py::TestBase::test_created_at_does_not_change_on_update PASSED [ 36%]
tests/core/db/implementations/test_model_base.py::TestBase::test_multiple_models_have_different_ids PASSED [ 36%]
tests/core/db/implementations/test_models.py::TestDynamicConfig::test_dynamic_config_creation PASSED [ 36%]
tests/core/db/implementations/test_models.py::TestDynamicConfig::test_dynamic_config_default_values PASSED [ 36%]
tests/core/db/implementations/test_models.py::TestDynamicConfig::test_dynamic_config_repr PASSED [ 36%]
tests/core/db/implementations/test_models.py::TestDynamicConfig::test_dynamic_config_to_dict PASSED [ 36%]
tests/core/db/implementations/test_models.py::TestDynamicConfig::test_dynamic_config_unique_key PASSED [ 36%]
tests/core/db/implementations/test_models.py::TestDynamicConfig::test_dynamic_config_different_value_types PASSED [ 36%]
tests/core/db/implementations/test_models.py::TestDynamicConfig::test_dynamic_config_json_serialization PASSED [ 36%]
tests/core/db/implementations/test_models.py::TestLogEntry::test_log_entry_creation PASSED [ 36%]
tests/core/db/implementations/test_models.py::TestLogEntry::test_log_entry_optional_fields PASSED [ 36%]
tests/core/db/implementations/test_models.py::TestLogEntry::test_log_entry_repr PASSED [ 36%]
tests/core/db/implementations/test_models.py::TestLogEntry::test_log_entry_to_dict PASSED [ 36%]
tests/core/db/implementations/test_models.py::TestLogEntry::test_log_entry_different_levels PASSED [ 36%]
tests/core/db/implementations/test_models.py::TestLogEntry::test_log_entry_extra_data_types PASSED [ 37%]
tests/core/db/implementations/test_models.py::TestLogEntry::test_log_entry_long_message PASSED [ 37%]
tests/core/db/implementations/test_models.py::TestLogEntry::test_log_entry_exception_data PASSED [ 37%]
tests/core/db/implementations/test_models.py::TestModelRelationships::test_multiple_models_same_session PASSED [ 37%]
tests/core/db/implementations/test_models.py::TestModelRelationships::test_model_timestamps PASSED [ 37%]
tests/core/db/implementations/test_models.py::TestModelRelationships::test_model_deletion PASSED [ 37%]
tests/core/db/implementations/test_models.py::TestModelValidation::test_dynamic_config_nullable_fields PASSED [ 37%]
tests/core/db/implementations/test_models.py::TestModelValidation::test_log_entry_nullable_fields PASSED [ 37%]
tests/core/db/implementations/test_models.py::TestModelValidation::test_dynamic_config_string_length_limits PASSED [ 37%]
tests/core/db/implementations/test_models.py::TestModelValidation::test_log_entry_string_length_limits PASSED [ 37%]
tests/core/db/implementations/test_sqlalchemy_session.py::TestDatabaseURL::test_get_database_url_with_provided_config PASSED [ 37%]
tests/core/db/implementations/test_sqlalchemy_session.py::TestDatabaseURL::test_get_database_url_fallback_to_env PASSED [ 37%]
tests/core/db/implementations/test_sqlalchemy_session.py::TestDatabaseURL::test_get_database_url_without_config PASSED [ 37%]
tests/core/db/implementations/test_sqlalchemy_session.py::TestDatabaseURL::test_get_database_url_raises_error_when_missing PASSED [ 37%]
tests/core/db/implementations/test_sqlalchemy_session.py::TestCreateEngine::test_create_engine_sqlite PASSED [ 37%]
tests/core/db/implementations/test_sqlalchemy_session.py::TestCreateEngine::test_create_engine_with_echo PASSED [ 37%]
tests/core/db/implementations/test_sqlalchemy_session.py::TestCreateEngine::test_create_engine_postgresql PASSED [ 38%]
tests/core/db/implementations/test_sqlalchemy_session.py::TestGetEngine::test_get_engine_creates_on_first_call PASSED [ 38%]
tests/core/db/implementations/test_sqlalchemy_session.py::TestGetEngine::test_get_engine_caches_result SKIPPED [ 38%]
tests/core/db/implementations/test_sqlalchemy_session.py::TestGetAsyncSessionMaker::test_get_async_session_maker_creates_once PASSED [ 38%]
tests/core/db/implementations/test_sqlalchemy_session.py::TestDatabaseManager::test_database_manager_initialization PASSED [ 38%]
tests/core/db/implementations/test_sqlalchemy_session.py::TestDatabaseManager::test_database_manager_initialize PASSED [ 38%]
tests/core/db/implementations/test_sqlalchemy_session.py::TestDatabaseManager::test_database_manager_get_session PASSED [ 38%]
tests/core/db/implementations/test_sqlalchemy_session.py::TestDatabaseManager::test_database_manager_get_session_raises_when_not_initialized SKIPPED [ 38%]
tests/core/db/implementations/test_sqlalchemy_session.py::TestDatabaseManager::test_database_manager_close PASSED [ 38%]
tests/core/db/implementations/test_sqlalchemy_session.py::TestDatabaseManager::test_database_manager_singleton_pattern PASSED [ 38%]
tests/core/db/implementations/test_sqlalchemy_session.py::TestDatabaseManager::test_database_manager_get_session_exception_rollback PASSED [ 38%]
tests/core/db/implementations/test_sqlalchemy_session.py::TestDatabaseManager::test_database_manager_get_active_configs PASSED [ 38%]
tests/core/db/implementations/test_sqlalchemy_session.py::TestDatabaseManager::test_database_manager_get_active_configs_not_initialized PASSED [ 38%]
tests/core/db/implementations/test_sqlalchemy_session.py::TestContextManagers::test_get_db_session PASSED [ 38%]
tests/core/db/implementations/test_sqlalchemy_session.py::TestContextManagers::test_get_db_session_direct PASSED [ 38%]
tests/core/db/implementations/test_sqlalchemy_session.py::TestContextManagers::test_get_db_session_exception_rollback PASSED [ 38%]
tests/core/db/implementations/test_sqlalchemy_session.py::TestDatabaseInitialization::test_init_db PASSED [ 38%]
tests/core/db/implementations/test_sqlalchemy_session.py::TestDatabaseInitialization::test_close_db PASSED [ 39%]
tests/core/db/implementations/test_sqlalchemy_session.py::TestGetActiveConfigs::test_get_active_configs SKIPPED [ 39%]
tests/core/db/interfaces/test_db_interfaces_init.py::TestInterfacesInit::test_module_has_docstring PASSED [ 39%]
tests/core/db/interfaces/test_db_interfaces_init.py::TestInterfacesInit::test_all_list_is_empty_or_nonexistent PASSED [ 39%]
tests/core/db/interfaces/test_db_interfaces_init.py::TestInterfacesInit::test_no_explicit_exports PASSED [ 39%]
tests/core/db/interfaces/test_db_interfaces_init.py::TestInterfacesInit::test_import_does_not_fail PASSED [ 39%]
tests/core/db/test_db_factory.py::TestDatabaseFactory::test_get_session_maker_without_config PASSED [ 39%]
tests/core/db/test_db_factory.py::TestDatabaseFactory::test_get_session_maker_with_config PASSED [ 39%]
tests/core/db/test_db_factory.py::TestDatabaseFactory::test_get_engine_without_config PASSED [ 39%]
tests/core/db/test_db_factory.py::TestDatabaseFactory::test_get_engine_with_config PASSED [ 39%]
tests/core/db/test_db_factory.py::TestDatabaseFactory::test_create_engine_with_custom_url PASSED [ 39%]
tests/core/db/test_db_factory.py::TestDatabaseFactory::test_create_engine_with_echo_enabled PASSED [ 39%]
tests/core/db/test_db_factory.py::TestDatabaseFactory::test_create_manager_without_config PASSED [ 39%]
tests/core/db/test_db_factory.py::TestDatabaseFactory::test_create_manager_with_config PASSED [ 39%]
tests/core/db/test_db_factory.py::TestDatabaseFactory::test_get_session_maker_caches_result PASSED [ 39%]
tests/core/db/test_db_factory.py::TestDatabaseFactory::test_get_engine_caches_result PASSED [ 39%]
tests/core/db/test_db_factory.py::TestDatabaseFactory::test_create_engine_different_urls PASSED [ 39%]
tests/core/db/test_db_factory.py::TestDatabaseFactory::test_factory_methods_return_consistent_types PASSED [ 40%]
tests/core/db/test_db_factory.py::TestDatabaseFactory::test_factory_is_stateless PASSED [ 40%]
tests/core/db/test_db_init.py::TestDbInit::test_base_import PASSED       [ 40%]
tests/core/db/test_db_init.py::TestDbInit::test_models_import PASSED     [ 40%]
tests/core/db/test_db_init.py::TestDbInit::test_session_functions_import PASSED [ 40%]
tests/core/db/test_db_init.py::TestDbInit::test_classes_import PASSED    [ 40%]
tests/core/db/test_db_init.py::TestDbInit::test_helper_functions_import PASSED [ 40%]
tests/core/db/test_db_init.py::TestDbInit::test_all_imports_are_callable PASSED [ 40%]
tests/core/db/test_db_init.py::TestDbInit::test_all_imports_are_not_none PASSED [ 40%]
tests/core/db/test_db_init.py::TestDbInit::test_model_base_relationship PASSED [ 40%]
tests/core/events/exceptions/test_event_error.py::TestEventBusError::test_event_bus_error_creation PASSED [ 40%]
tests/core/events/exceptions/test_event_error.py::TestEventBusError::test_event_bus_error_with_details PASSED [ 40%]
tests/core/events/exceptions/test_event_error.py::TestEventBusError::test_event_bus_error_is_neural_ai_exception PASSED [ 40%]
tests/core/events/exceptions/test_event_error.py::TestPublishError::test_publish_error_creation PASSED [ 40%]
tests/core/events/exceptions/test_event_error.py::TestPublishError::test_publish_error_with_event_type PASSED [ 40%]
tests/core/events/exceptions/test_event_error.py::TestPublishError::test_publish_error_inheritance PASSED [ 40%]
tests/core/events/exceptions/test_event_error.py::TestSubscriberError::test_subscriber_error_creation PASSED [ 41%]
tests/core/events/exceptions/test_event_error.py::TestSubscriberError::test_subscriber_error_with_subscriber_id PASSED [ 41%]
tests/core/events/exceptions/test_event_error.py::TestSubscriberError::test_subscriber_error_inheritance PASSED [ 41%]
tests/core/events/exceptions/test_events_exceptions_init.py::TestExceptionsInitExports::test_event_bus_error_exported PASSED [ 41%]
tests/core/events/exceptions/test_events_exceptions_init.py::TestExceptionsInitExports::test_publish_error_exported PASSED [ 41%]
tests/core/events/exceptions/test_events_exceptions_init.py::TestExceptionsInitExports::test_subscriber_error_exported PASSED [ 41%]
tests/core/events/exceptions/test_events_exceptions_init.py::TestExceptionsInitExports::test_all_imports_in_all_list PASSED [ 41%]
tests/core/events/exceptions/test_events_exceptions_init.py::TestExceptionsInitExports::test_import_from_exceptions_package PASSED [ 41%]
tests/core/events/implementations/test_events_implementations_init.py::TestImplementationsInitExports::test_event_bus_exported PASSED [ 41%]
tests/core/events/implementations/test_events_implementations_init.py::TestImplementationsInitExports::test_event_bus_config_exported PASSED [ 41%]
tests/core/events/implementations/test_events_implementations_init.py::TestImplementationsInitExports::test_all_imports_in_all_list PASSED [ 41%]
tests/core/events/implementations/test_events_implementations_init.py::TestImplementationsInitExports::test_import_from_implementations_package PASSED [ 41%]
tests/core/events/implementations/test_zeromq_bus.py::TestEventBusInitialization::test_default_initialization PASSED [ 41%]
tests/core/events/implementations/test_zeromq_bus.py::TestEventBusInitialization::test_custom_config_initialization PASSED [ 41%]
tests/core/events/implementations/test_zeromq_bus.py::TestEventBusInitialization::test_external_zmq_context PASSED [ 41%]
tests/core/events/implementations/test_zeromq_bus.py::TestEventBusInitialization::test_zmq_import_error PASSED [ 41%]
tests/core/events/implementations/test_zeromq_bus.py::TestEventBusStartStop::test_start_success PASSED [ 41%]
tests/core/events/implementations/test_zeromq_bus.py::TestEventBusStartStop::test_start_with_inproc PASSED [ 42%]
tests/core/events/implementations/test_zeromq_bus.py::TestEventBusStartStop::test_start_twice PASSED [ 42%]
tests/core/events/implementations/test_zeromq_bus.py::TestEventBusStartStop::test_stop_success PASSED [ 42%]
tests/core/events/implementations/test_zeromq_bus.py::TestEventBusStartStop::test_stop_without_start PASSED [ 42%]
tests/core/events/implementations/test_zeromq_bus.py::TestEventBusStartStop::test_stop_twice PASSED [ 42%]
tests/core/events/implementations/test_zeromq_bus.py::TestEventBusPublish::test_publish_success PASSED [ 42%]
tests/core/events/implementations/test_zeromq_bus.py::TestEventBusPublish::test_publish_not_started PASSED [ 42%]
tests/core/events/implementations/test_zeromq_bus.py::TestEventBusPublish::test_publish_no_publisher PASSED [ 42%]
tests/core/events/implementations/test_zeromq_bus.py::TestEventBusPublish::test_publish_batch_events PASSED [ 42%]
tests/core/events/implementations/test_zeromq_bus.py::TestEventBusSubscribeUnsubscribe::test_subscribe_new_event_type PASSED [ 42%]
tests/core/events/implementations/test_zeromq_bus.py::TestEventBusSubscribeUnsubscribe::test_subscribe_multiple_callbacks PASSED [ 42%]
tests/core/events/implementations/test_zeromq_bus.py::TestEventBusSubscribeUnsubscribe::test_unsubscribe_existing PASSED [ 42%]
tests/core/events/implementations/test_zeromq_bus.py::TestEventBusSubscribeUnsubscribe::test_unsubscribe_non_existing PASSED [ 42%]
tests/core/events/implementations/test_zeromq_bus.py::TestEventBusSubscribeUnsubscribe::test_unsubscribe_non_existing_event_type PASSED [ 42%]
tests/core/events/implementations/test_zeromq_bus.py::TestEventBusContextManager::test_async_context_manager PASSED [ 42%]
tests/core/events/implementations/test_zeromq_bus.py::TestEventBusDeserialization::test_deserialize_market_data PASSED [ 42%]
tests/core/events/implementations/test_zeromq_bus.py::TestEventBusDeserialization::test_deserialize_unknown_event_type PASSED [ 42%]
tests/core/events/implementations/test_zeromq_bus.py::TestEventBusDeserialization::test_deserialize_invalid_data PASSED [ 43%]
tests/core/events/implementations/test_zeromq_bus.py::TestEventBusDispatch::test_dispatch_event_success PASSED [ 43%]
tests/core/events/implementations/test_zeromq_bus.py::TestEventBusDispatch::test_dispatch_event_no_subscribers PASSED [ 43%]
tests/core/events/implementations/test_zeromq_bus.py::TestEventBusDispatch::test_dispatch_event_callback_error PASSED [ 43%]
tests/core/events/implementations/test_zeromq_bus.py::TestEventBusDeserializationAdditional::test_deserialize_trade_event PASSED [ 43%]
tests/core/events/implementations/test_zeromq_bus.py::TestEventBusDeserializationAdditional::test_deserialize_signal_event PASSED [ 43%]
tests/core/events/implementations/test_zeromq_bus.py::TestEventBusDeserializationAdditional::test_deserialize_system_log_event PASSED [ 43%]
tests/core/events/implementations/test_zeromq_bus.py::TestEventBusDeserializationAdditional::test_deserialize_order_event PASSED [ 43%]
tests/core/events/implementations/test_zeromq_bus.py::TestEventBusDeserializationAdditional::test_deserialize_position_event PASSED [ 43%]
tests/core/events/implementations/test_zeromq_bus.py::TestEventBusDispatchExceptionHandling::test_dispatch_event_deserialization_error PASSED [ 43%]
tests/core/events/implementations/test_zeromq_bus.py::TestEventBusDispatchExceptionHandling::test_dispatch_event_deserialization_returns_none PASSED [ 43%]
tests/core/events/implementations/test_zeromq_bus.py::TestEventBusDispatchExceptionHandling::test_dispatch_event_outer_exception_handling PASSED [ 43%]
tests/core/events/implementations/test_zeromq_bus.py::TestEventBusRunForever::test_run_forever_success PASSED [ 43%]
tests/core/events/implementations/test_zeromq_bus.py::TestEventBusRunForever::test_run_forever_timeout_handling PASSED [ 43%]
tests/core/events/implementations/test_zeromq_bus.py::TestEventBusRunForever::test_run_forever_not_started PASSED [ 43%]
tests/core/events/implementations/test_zeromq_bus.py::TestEventBusRunForever::test_run_forever_message_processing PASSED [ 43%]
tests/core/events/implementations/test_zeromq_bus.py::TestEventBusRunForever::test_run_forever_invalid_message_format PASSED [ 44%]
tests/core/events/implementations/test_zeromq_bus.py::TestEventBusRunForever::test_run_forever_json_decode_error PASSED [ 44%]
tests/core/events/implementations/test_zeromq_bus.py::TestEventBusRunForever::test_run_forever_general_exception_handling PASSED [ 44%]
tests/core/events/implementations/test_zeromq_bus.py::TestEventBusRunForever::test_run_forever_with_inproc PASSED [ 44%]
tests/core/events/implementations/test_zeromq_bus.py::TestEventBusErrorHandling::test_publish_error_zmq_exception PASSED [ 44%]
tests/core/events/implementations/test_zeromq_bus.py::TestEventBusErrorHandling::test_publish_error_general_exception PASSED [ 44%]
tests/core/events/implementations/test_zeromq_bus.py::TestEventBusErrorHandling::test_publish_error_with_callback PASSED [ 44%]
tests/core/events/implementations/test_zeromq_bus.py::TestEventBusErrorHandling::test_subscribe_error_setsockopt_exception PASSED [ 44%]
tests/core/events/implementations/test_zeromq_bus.py::TestEventBusErrorHandling::test_subscribe_error_setsockopt_general_exception PASSED [ 44%]
tests/core/events/implementations/test_zeromq_bus.py::TestEventBusErrorHandling::test_start_error_socket_bind_failure PASSED [ 44%]
tests/core/events/implementations/test_zeromq_bus.py::TestEventBusErrorHandling::test_stop_error_socket_close_failure PASSED [ 44%]
tests/core/events/interfaces/test_event_bus_interface.py::TestEventBusConfig::test_default_config PASSED [ 44%]
tests/core/events/interfaces/test_event_bus_interface.py::TestEventBusConfig::test_custom_config PASSED [ 44%]
tests/core/events/interfaces/test_event_bus_interface.py::TestEventBusConfig::test_config_immutability PASSED [ 44%]
tests/core/events/interfaces/test_event_bus_interface.py::TestEventBusInterface::test_interface_is_abstract PASSED [ 44%]
tests/core/events/interfaces/test_event_bus_interface.py::TestEventBusInterface::test_interface_has_required_methods PASSED [ 44%]
tests/core/events/interfaces/test_event_bus_interface.py::TestEventBusInterface::test_config_property_is_abstract PASSED [ 44%]
tests/core/events/interfaces/test_event_bus_interface.py::TestEventBusInterface::test_start_is_abstract PASSED [ 45%]
tests/core/events/interfaces/test_event_bus_interface.py::TestEventBusInterface::test_stop_is_abstract PASSED [ 45%]
tests/core/events/interfaces/test_event_bus_interface.py::TestEventBusInterface::test_publish_is_abstract PASSED [ 45%]
tests/core/events/interfaces/test_event_bus_interface.py::TestEventBusInterface::test_subscribe_is_abstract PASSED [ 45%]
tests/core/events/interfaces/test_event_bus_interface.py::TestEventBusInterface::test_unsubscribe_is_abstract PASSED [ 45%]
tests/core/events/interfaces/test_event_bus_interface.py::TestEventBusInterface::test_run_forever_is_abstract PASSED [ 45%]
tests/core/events/interfaces/test_event_bus_interface.py::TestEventBusInterface::test_interface_method_signatures PASSED [ 45%]
tests/core/events/interfaces/test_event_bus_interface.py::TestEventBusInterface::test_config_property_has_docstring PASSED [ 45%]
tests/core/events/interfaces/test_event_bus_interface.py::TestEventBusInterface::test_start_method_has_docstring PASSED [ 45%]
tests/core/events/interfaces/test_event_bus_interface.py::TestEventBusInterface::test_stop_method_has_docstring PASSED [ 45%]
tests/core/events/interfaces/test_event_bus_interface.py::TestEventBusInterface::test_publish_method_has_docstring PASSED [ 45%]
tests/core/events/interfaces/test_event_bus_interface.py::TestEventBusInterface::test_subscribe_method_has_docstring PASSED [ 45%]
tests/core/events/interfaces/test_event_bus_interface.py::TestEventBusInterface::test_unsubscribe_method_has_docstring PASSED [ 45%]
tests/core/events/interfaces/test_event_bus_interface.py::TestEventBusInterface::test_run_forever_method_has_docstring PASSED [ 45%]
tests/core/events/interfaces/test_event_bus_interface.py::TestEventBusInterface::test_event_callback_type_alias PASSED [ 45%]
tests/core/events/interfaces/test_event_bus_interface.py::TestEventBusInterface::test_event_bus_config_repr PASSED [ 45%]
tests/core/events/interfaces/test_event_bus_interface.py::TestEventBusInterface::test_event_bus_config_str PASSED [ 46%]
tests/core/events/interfaces/test_event_bus_interface.py::TestEventBusInterface::test_event_bus_config_equality PASSED [ 46%]
tests/core/events/interfaces/test_event_bus_interface.py::TestEventBusInterface::test_event_bus_config_inequality PASSED [ 46%]
tests/core/events/interfaces/test_event_bus_interface.py::TestEventBusInterface::test_concrete_implementation_calls_pass_statements PASSED [ 46%]
tests/core/events/interfaces/test_event_bus_interface.py::TestEventBusInterface::test_interface_cannot_be_instantiated_directly PASSED [ 46%]
tests/core/events/interfaces/test_event_models.py::TestEventType::test_event_type_values PASSED [ 46%]
tests/core/events/interfaces/test_event_models.py::TestMarketDataEvent::test_valid_market_data_event PASSED [ 46%]
tests/core/events/interfaces/test_event_models.py::TestMarketDataEvent::test_market_data_event_without_volume PASSED [ 46%]
tests/core/events/interfaces/test_event_models.py::TestMarketDataEvent::test_market_data_event_invalid_source PASSED [ 46%]
tests/core/events/interfaces/test_event_models.py::TestMarketDataEvent::test_market_data_event_invalid_bid PASSED [ 46%]
tests/core/events/interfaces/test_event_models.py::TestMarketDataEvent::test_market_data_event_invalid_ask PASSED [ 46%]
tests/core/events/interfaces/test_event_models.py::TestTradeEvent::test_valid_trade_event PASSED [ 46%]
tests/core/events/interfaces/test_event_models.py::TestTradeEvent::test_trade_event_without_strategy_id PASSED [ 46%]
tests/core/events/interfaces/test_event_models.py::TestTradeEvent::test_trade_event_invalid_direction PASSED [ 46%]
tests/core/events/interfaces/test_event_models.py::TestTradeEvent::test_trade_event_invalid_price PASSED [ 46%]
tests/core/events/interfaces/test_event_models.py::TestSignalEvent::test_valid_signal_event PASSED [ 46%]
tests/core/events/interfaces/test_event_models.py::TestSignalEvent::test_signal_event_without_prices PASSED [ 46%]
tests/core/events/interfaces/test_event_models.py::TestSignalEvent::test_signal_event_invalid_signal_type PASSED [ 47%]
tests/core/events/interfaces/test_event_models.py::TestSignalEvent::test_signal_event_invalid_confidence PASSED [ 47%]
tests/core/events/interfaces/test_event_models.py::TestSystemLogEvent::test_valid_system_log_event PASSED [ 47%]
tests/core/events/interfaces/test_event_models.py::TestSystemLogEvent::test_system_log_event_without_extra_data PASSED [ 47%]
tests/core/events/interfaces/test_event_models.py::TestSystemLogEvent::test_system_log_event_invalid_level PASSED [ 47%]
tests/core/events/interfaces/test_event_models.py::TestOrderEvent::test_valid_order_event PASSED [ 47%]
tests/core/events/interfaces/test_event_models.py::TestOrderEvent::test_order_event_with_price PASSED [ 47%]
tests/core/events/interfaces/test_event_models.py::TestOrderEvent::test_order_event_invalid_order_type PASSED [ 47%]
tests/core/events/interfaces/test_event_models.py::TestOrderEvent::test_order_event_invalid_direction PASSED [ 47%]
tests/core/events/interfaces/test_event_models.py::TestOrderEvent::test_order_event_invalid_status PASSED [ 47%]
tests/core/events/interfaces/test_event_models.py::TestPositionEvent::test_valid_position_event PASSED [ 47%]
tests/core/events/interfaces/test_event_models.py::TestPositionEvent::test_position_event_without_profit_loss PASSED [ 47%]
tests/core/events/interfaces/test_event_models.py::TestPositionEvent::test_position_event_invalid_direction PASSED [ 47%]
tests/core/events/interfaces/test_event_models.py::TestPositionEvent::test_position_event_invalid_status PASSED [ 47%]
tests/core/events/interfaces/test_events_interfaces_init.py::TestInterfacesInitExports::test_event_bus_interface_exported PASSED [ 47%]
tests/core/events/interfaces/test_events_interfaces_init.py::TestInterfacesInitExports::test_event_bus_config_exported PASSED [ 47%]
tests/core/events/interfaces/test_events_interfaces_init.py::TestInterfacesInitExports::test_event_type_exported PASSED [ 47%]
tests/core/events/interfaces/test_events_interfaces_init.py::TestInterfacesInitExports::test_market_data_event_exported PASSED [ 48%]
tests/core/events/interfaces/test_events_interfaces_init.py::TestInterfacesInitExports::test_trade_event_exported PASSED [ 48%]
tests/core/events/interfaces/test_events_interfaces_init.py::TestInterfacesInitExports::test_signal_event_exported PASSED [ 48%]
tests/core/events/interfaces/test_events_interfaces_init.py::TestInterfacesInitExports::test_system_log_event_exported PASSED [ 48%]
tests/core/events/interfaces/test_events_interfaces_init.py::TestInterfacesInitExports::test_order_event_exported PASSED [ 48%]
tests/core/events/interfaces/test_events_interfaces_init.py::TestInterfacesInitExports::test_position_event_exported PASSED [ 48%]
tests/core/events/interfaces/test_events_interfaces_init.py::TestInterfacesInitExports::test_all_imports_in_all_list PASSED [ 48%]
tests/core/events/interfaces/test_events_interfaces_init.py::TestInterfacesInitExports::test_import_from_interfaces_package PASSED [ 48%]
tests/core/events/test_events_factory.py::TestEventBusFactoryCreate::test_create_default PASSED [ 48%]
tests/core/events/test_events_factory.py::TestEventBusFactoryCreate::test_create_with_config PASSED [ 48%]
tests/core/events/test_events_factory.py::TestEventBusFactoryCreate::test_create_returns_interface PASSED [ 48%]
tests/core/events/test_events_factory.py::TestEventBusFactoryCreateAndStart::test_create_and_start_default PASSED [ 48%]
tests/core/events/test_events_factory.py::TestEventBusFactoryCreateAndStart::test_create_and_start_with_config PASSED [ 48%]
tests/core/events/test_events_factory.py::TestEventBusFactoryCreateAndStart::test_create_and_start_returns_interface PASSED [ 48%]
tests/core/events/test_events_factory.py::TestEventBusFactoryCreateFromConfig::test_create_from_config_success PASSED [ 48%]
tests/core/events/test_events_factory.py::TestEventBusFactoryCreateFromConfig::test_create_from_config_with_key_error PASSED [ 48%]
tests/core/events/test_events_factory.py::TestEventBusFactoryCreateFromConfig::test_create_from_config_with_value_error PASSED [ 49%]
tests/core/events/test_events_factory.py::TestEventBusFactoryCreateFromConfig::test_create_from_config_partial_config PASSED [ 49%]
tests/core/events/test_events_factory.py::TestEventBusFactoryCreateFromConfig::test_create_from_config_returns_interface PASSED [ 49%]
tests/core/events/test_events_factory.py::TestEventBusFactoryStaticMethods::test_factory_methods_are_instance_methods FAILED [ 49%]
tests/core/events/test_events_init.py::TestEventsInitExports::test_event_bus_factory_exported PASSED [ 49%]
tests/core/events/test_events_init.py::TestEventsInitExports::test_event_type_exported PASSED [ 49%]
tests/core/events/test_events_init.py::TestEventsInitExports::test_market_data_event_exported PASSED [ 49%]
tests/core/events/test_events_init.py::TestEventsInitExports::test_trade_event_exported PASSED [ 49%]
tests/core/events/test_events_init.py::TestEventsInitExports::test_signal_event_exported PASSED [ 49%]
tests/core/events/test_events_init.py::TestEventsInitExports::test_system_log_event_exported PASSED [ 49%]
tests/core/events/test_events_init.py::TestEventsInitExports::test_order_event_exported PASSED [ 49%]
tests/core/events/test_events_init.py::TestEventsInitExports::test_position_event_exported PASSED [ 49%]
tests/core/events/test_events_init.py::TestEventsInitExports::test_all_imports_in_all_list PASSED [ 49%]
tests/core/events/test_events_init.py::TestEventsInitExports::test_import_from_package_root PASSED [ 49%]
tests/core/logger/exceptions/test_logger_error.py::TestLoggerError::test_logger_error_is_exception PASSED [ 49%]
tests/core/logger/exceptions/test_logger_error.py::TestLoggerError::test_logger_error_can_be_raised PASSED [ 49%]
tests/core/logger/exceptions/test_logger_error.py::TestLoggerError::test_logger_error_has_message PASSED [ 49%]
tests/core/logger/exceptions/test_logger_error.py::TestLoggerError::test_logger_error_without_message PASSED [ 50%]
tests/core/logger/exceptions/test_logger_error.py::TestLoggerConfigurationError::test_logger_configuration_error_is_logger_error PASSED [ 50%]
tests/core/logger/exceptions/test_logger_error.py::TestLoggerConfigurationError::test_logger_configuration_error_can_be_raised PASSED [ 50%]
tests/core/logger/exceptions/test_logger_error.py::TestLoggerConfigurationError::test_logger_configuration_error_has_message PASSED [ 50%]
tests/core/logger/exceptions/test_logger_error.py::TestLoggerConfigurationError::test_logger_configuration_error_without_message PASSED [ 50%]
tests/core/logger/exceptions/test_logger_error.py::TestLoggerInitializationError::test_logger_initialization_error_is_logger_error PASSED [ 50%]
tests/core/logger/exceptions/test_logger_error.py::TestLoggerInitializationError::test_logger_initialization_error_can_be_raised PASSED [ 50%]
tests/core/logger/exceptions/test_logger_error.py::TestLoggerInitializationError::test_logger_initialization_error_has_message PASSED [ 50%]
tests/core/logger/exceptions/test_logger_error.py::TestLoggerInitializationError::test_logger_initialization_error_without_message PASSED [ 50%]
tests/core/logger/exceptions/test_logger_error.py::TestLoggerErrorHierarchy::test_logger_error_hierarchy PASSED [ 50%]
tests/core/logger/exceptions/test_logger_error.py::TestLoggerErrorHierarchy::test_catch_logger_error_catches_subclasses PASSED [ 50%]
tests/core/logger/formatters/test_logger_formatters.py::TestColoredFormatter::test_format_debug PASSED [ 50%]
tests/core/logger/formatters/test_logger_formatters.py::TestColoredFormatter::test_format_info PASSED [ 50%]
tests/core/logger/formatters/test_logger_formatters.py::TestColoredFormatter::test_format_warning PASSED [ 50%]
tests/core/logger/formatters/test_logger_formatters.py::TestColoredFormatter::test_format_error PASSED [ 50%]
tests/core/logger/formatters/test_logger_formatters.py::TestColoredFormatter::test_format_critical PASSED [ 50%]
tests/core/logger/formatters/test_logger_formatters.py::TestColoredFormatter::test_format_unknown_level PASSED [ 50%]
tests/core/logger/implementations/test_colored_logger.py::TestColoredLogger::test_init_basic PASSED [ 51%]
tests/core/logger/implementations/test_colored_logger.py::TestColoredLogger::test_init_with_custom_level PASSED [ 51%]
tests/core/logger/implementations/test_colored_logger.py::TestColoredLogger::test_debug_logging PASSED [ 51%]
tests/core/logger/implementations/test_colored_logger.py::TestColoredLogger::test_info_logging PASSED [ 51%]
tests/core/logger/implementations/test_colored_logger.py::TestColoredLogger::test_warning_logging PASSED [ 51%]
tests/core/logger/implementations/test_colored_logger.py::TestColoredLogger::test_error_logging PASSED [ 51%]
tests/core/logger/implementations/test_colored_logger.py::TestColoredLogger::test_critical_logging PASSED [ 51%]
tests/core/logger/implementations/test_colored_logger.py::TestColoredLogger::test_set_level PASSED [ 51%]
tests/core/logger/implementations/test_colored_logger.py::TestColoredLogger::test_logger_name PASSED [ 51%]
tests/core/logger/implementations/test_colored_logger.py::TestColoredLogger::test_colored_formatter_present PASSED [ 51%]
tests/core/logger/implementations/test_colored_logger.py::TestColoredLogger::test_existing_handlers_removed PASSED [ 51%]
tests/core/logger/implementations/test_colored_logger.py::TestColoredLogger::test_di_dependencies_none PASSED [ 51%]
tests/core/logger/implementations/test_default_logger.py::TestDefaultLogger::test_init_basic PASSED [ 51%]
tests/core/logger/implementations/test_default_logger.py::TestDefaultLogger::test_init_with_custom_level PASSED [ 51%]
tests/core/logger/implementations/test_default_logger.py::TestDefaultLogger::test_debug_logging PASSED [ 51%]
tests/core/logger/implementations/test_default_logger.py::TestDefaultLogger::test_info_logging PASSED [ 51%]
tests/core/logger/implementations/test_default_logger.py::TestDefaultLogger::test_warning_logging PASSED [ 52%]
tests/core/logger/implementations/test_default_logger.py::TestDefaultLogger::test_error_logging PASSED [ 52%]
tests/core/logger/implementations/test_default_logger.py::TestDefaultLogger::test_critical_logging PASSED [ 52%]
tests/core/logger/implementations/test_default_logger.py::TestDefaultLogger::test_set_level PASSED [ 52%]
tests/core/logger/implementations/test_default_logger.py::TestDefaultLogger::test_logger_name PASSED [ 52%]
tests/core/logger/implementations/test_default_logger.py::TestDefaultLogger::test_no_duplicate_handlers PASSED [ 52%]
tests/core/logger/implementations/test_default_logger.py::TestDefaultLogger::test_di_dependencies_none PASSED [ 52%]
tests/core/logger/implementations/test_rotating_file_logger.py::TestRotatingFileLogger::test_init_basic PASSED [ 52%]
tests/core/logger/implementations/test_rotating_file_logger.py::TestRotatingFileLogger::test_init_without_file_raises_error PASSED [ 52%]
tests/core/logger/implementations/test_rotating_file_logger.py::TestRotatingFileLogger::test_init_with_empty_file_raises_error PASSED [ 52%]
tests/core/logger/implementations/test_rotating_file_logger.py::TestRotatingFileLogger::test_init_with_custom_level PASSED [ 52%]
tests/core/logger/implementations/test_rotating_file_logger.py::TestRotatingFileLogger::test_init_creates_directory PASSED [ 52%]
tests/core/logger/implementations/test_rotating_file_logger.py::TestRotatingFileLogger::test_debug_logging PASSED [ 52%]
tests/core/logger/implementations/test_rotating_file_logger.py::TestRotatingFileLogger::test_debug_logging_without_kwargs PASSED [ 52%]
tests/core/logger/implementations/test_rotating_file_logger.py::TestRotatingFileLogger::test_info_logging PASSED [ 52%]
tests/core/logger/implementations/test_rotating_file_logger.py::TestRotatingFileLogger::test_info_logging_without_kwargs PASSED [ 52%]
tests/core/logger/implementations/test_rotating_file_logger.py::TestRotatingFileLogger::test_warning_logging PASSED [ 52%]
tests/core/logger/implementations/test_rotating_file_logger.py::TestRotatingFileLogger::test_warning_logging_without_kwargs PASSED [ 53%]
tests/core/logger/implementations/test_rotating_file_logger.py::TestRotatingFileLogger::test_error_logging PASSED [ 53%]
tests/core/logger/implementations/test_rotating_file_logger.py::TestRotatingFileLogger::test_error_logging_without_kwargs PASSED [ 53%]
tests/core/logger/implementations/test_rotating_file_logger.py::TestRotatingFileLogger::test_critical_logging PASSED [ 53%]
tests/core/logger/implementations/test_rotating_file_logger.py::TestRotatingFileLogger::test_critical_logging_without_kwargs PASSED [ 53%]
tests/core/logger/implementations/test_rotating_file_logger.py::TestRotatingFileLogger::test_set_level PASSED [ 53%]
tests/core/logger/implementations/test_rotating_file_logger.py::TestRotatingFileLogger::test_logger_name PASSED [ 53%]
tests/core/logger/implementations/test_rotating_file_logger.py::TestRotatingFileLogger::test_invalid_rotation_type_raises_error PASSED [ 53%]
tests/core/logger/implementations/test_rotating_file_logger.py::TestRotatingFileLogger::test_time_based_rotation PASSED [ 53%]
tests/core/logger/implementations/test_rotating_file_logger.py::TestRotatingFileLogger::test_clean_old_logs PASSED [ 53%]
tests/core/logger/implementations/test_rotating_file_logger.py::TestRotatingFileLogger::test_existing_handlers_removed PASSED [ 53%]
tests/core/logger/implementations/test_rotating_file_logger.py::TestRotatingFileLogger::test_di_dependencies_none PASSED [ 53%]
tests/core/logger/interfaces/test_logger_factory_interface.py::TestLoggerFactoryInterface::test_interface_is_abstract PASSED [ 53%]
tests/core/logger/interfaces/test_logger_factory_interface.py::TestLoggerFactoryInterface::test_interface_has_required_methods PASSED [ 53%]
tests/core/logger/interfaces/test_logger_factory_interface.py::TestLoggerFactoryInterface::test_register_logger_raises_not_implemented PASSED [ 53%]
tests/core/logger/interfaces/test_logger_factory_interface.py::TestLoggerFactoryInterface::test_get_logger_raises_not_implemented PASSED [ 53%]
tests/core/logger/interfaces/test_logger_factory_interface.py::TestLoggerFactoryInterface::test_configure_raises_not_implemented PASSED [ 53%]
tests/core/logger/interfaces/test_logger_interface.py::TestLoggerInterface::test_interface_is_abstract PASSED [ 54%]
tests/core/logger/interfaces/test_logger_interface.py::TestLoggerInterface::test_interface_has_required_methods PASSED [ 54%]
tests/core/logger/interfaces/test_logger_interface.py::TestLoggerInterface::test_all_abstract_methods_implemented PASSED [ 54%]
tests/core/logger/interfaces/test_logger_interfaces_init.py::TestLoggerInterfacesInit::test_version_loaded_successfully PASSED [ 54%]
tests/core/logger/interfaces/test_logger_interfaces_init.py::TestLoggerInterfacesInit::test_version_fallback_on_package_not_found PASSED [ 54%]
tests/core/logger/interfaces/test_logger_interfaces_init.py::TestLoggerInterfacesInit::test_all_imports_available PASSED [ 54%]
tests/core/logger/interfaces/test_logger_interfaces_init.py::TestLoggerInterfacesInit::test_all_list_contains_expected_exports PASSED [ 54%]
tests/core/logger/test_logger_factory.py::TestLoggerFactory::test_get_logger_default PASSED [ 54%]
tests/core/logger/test_logger_factory.py::TestLoggerFactory::test_get_logger_colored PASSED [ 54%]
tests/core/logger/test_logger_factory.py::TestLoggerFactory::test_get_logger_rotating_without_file PASSED [ 54%]
tests/core/logger/test_logger_factory.py::TestLoggerFactory::test_get_logger_rotating_with_file PASSED [ 54%]
tests/core/logger/test_logger_factory.py::TestLoggerFactory::test_get_logger_caching PASSED [ 54%]
tests/core/logger/test_logger_factory.py::TestLoggerFactory::test_register_logger PASSED [ 54%]
tests/core/logger/test_logger_factory.py::TestLoggerFactory::test_get_registered_types PASSED [ 54%]
tests/core/logger/test_logger_factory.py::TestLoggerFactory::test_is_logger_registered PASSED [ 54%]
tests/core/logger/test_logger_factory.py::TestLoggerFactory::test_clear_instances PASSED [ 54%]
tests/core/logger/test_logger_factory.py::TestLoggerFactory::test_configure_basic PASSED [ 55%]
tests/core/logger/test_logger_factory.py::TestLoggerFactory::test_get_set_schema_version PASSED [ 55%]
tests/core/logger/test_logger_factory.py::TestLoggerFactory::test_get_logger_invalid_type_fallback_to_default PASSED [ 55%]
tests/core/logger/test_logger_factory.py::TestLoggerFactory::test_configure_file_handler_with_rotating PASSED [ 55%]
tests/core/logger/test_logger_factory.py::TestLoggerFactory::test_configure_file_handler_without_rotating PASSED [ 55%]
tests/core/logger/test_logger_factory.py::TestLoggerFactory::test_configure_file_handler_creates_parent_directories PASSED [ 55%]
tests/core/logger/test_logger_factory.py::TestLoggerFactory::test_configure_loggers_with_propagate_false PASSED [ 55%]
tests/core/logger/test_logger_init.py::TestLoggerInitExports::test_version_export PASSED [ 55%]
tests/core/logger/test_logger_init.py::TestLoggerInitExports::test_schema_version_export PASSED [ 55%]
tests/core/logger/test_logger_init.py::TestLoggerInitExports::test_logger_interface_export PASSED [ 55%]
tests/core/logger/test_logger_init.py::TestLoggerInitExports::test_logger_factory_interface_export PASSED [ 55%]
tests/core/logger/test_logger_init.py::TestLoggerInitExports::test_logger_factory_export PASSED [ 55%]
tests/core/logger/test_logger_init.py::TestLoggerInitExports::test_colored_logger_export PASSED [ 55%]
tests/core/logger/test_logger_init.py::TestLoggerInitExports::test_default_logger_export PASSED [ 55%]
tests/core/logger/test_logger_init.py::TestLoggerInitExports::test_rotating_file_logger_export PASSED [ 55%]
tests/core/logger/test_logger_init.py::TestLoggerInitExports::test_logger_error_export PASSED [ 55%]
tests/core/logger/test_logger_init.py::TestLoggerInitExports::test_logger_configuration_error_export PASSED [ 55%]
tests/core/logger/test_logger_init.py::TestLoggerInitExports::test_logger_initialization_error_export PASSED [ 56%]
tests/core/logger/test_logger_init.py::TestLoggerInitExports::test_all_exports_in_all_list PASSED [ 56%]
tests/core/logger/test_logger_init.py::TestLoggerInitExports::test_import_all_from_logger PASSED [ 56%]
tests/core/logger/test_logger_init.py::TestLoggerInitExports::test_version_fallback_on_package_not_found PASSED [ 56%]
tests/core/system/implementations/test_health_monitor.py::TestDefaultHealthCheck::test_check_returns_healthy PASSED [ 56%]
tests/core/system/implementations/test_health_monitor.py::TestDefaultHealthCheck::test_get_name_returns_component_name PASSED [ 56%]
tests/core/system/implementations/test_health_monitor.py::TestHealthMonitor::test_check_component_nonexistent PASSED [ 56%]
tests/core/system/implementations/test_health_monitor.py::TestHealthMonitor::test_check_component_success PASSED [ 56%]
tests/core/system/implementations/test_health_monitor.py::TestHealthMonitor::test_check_component_with_exception PASSED [ 56%]
tests/core/system/implementations/test_health_monitor.py::TestHealthMonitor::test_check_health_exception_in_for_loop_coverage PASSED [ 56%]
tests/core/system/implementations/test_health_monitor.py::TestHealthMonitor::test_check_health_mixed_components PASSED [ 56%]
tests/core/system/implementations/test_health_monitor.py::TestHealthMonitor::test_check_health_no_components PASSED [ 56%]
tests/core/system/implementations/test_health_monitor.py::TestHealthMonitor::test_check_health_with_critical_component PASSED [ 56%]
tests/core/system/implementations/test_health_monitor.py::TestHealthMonitor::test_check_health_with_exception_in_component_check PASSED [ 56%]
tests/core/system/implementations/test_health_monitor.py::TestHealthMonitor::test_check_health_with_healthy_components PASSED [ 56%]
tests/core/system/implementations/test_health_monitor.py::TestHealthMonitor::test_check_health_with_unknown_status_components PASSED [ 56%]
tests/core/system/implementations/test_health_monitor.py::TestHealthMonitor::test_check_health_with_warning_component PASSED [ 57%]
tests/core/system/implementations/test_health_monitor.py::TestHealthMonitor::test_collect_system_metrics_logs_error_on_exception PASSED [ 57%]
tests/core/system/implementations/test_health_monitor.py::TestHealthMonitor::test_collect_system_metrics_success PASSED [ 57%]
tests/core/system/implementations/test_health_monitor.py::TestHealthMonitor::test_collect_system_metrics_with_disk_error PASSED [ 57%]
tests/core/system/implementations/test_health_monitor.py::TestHealthMonitor::test_collect_system_metrics_with_exception PASSED [ 57%]
tests/core/system/implementations/test_health_monitor.py::TestHealthMonitor::test_collect_system_metrics_with_net_error PASSED [ 57%]
tests/core/system/implementations/test_health_monitor.py::TestHealthMonitor::test_default_health_check_with_logger PASSED [ 57%]
tests/core/system/implementations/test_health_monitor.py::TestHealthMonitor::test_initial_state PASSED [ 57%]
tests/core/system/implementations/test_health_monitor.py::TestHealthMonitor::test_register_component PASSED [ 57%]
tests/core/system/implementations/test_health_monitor.py::TestHealthMonitor::test_register_component_with_custom_check PASSED [ 57%]
tests/core/system/implementations/test_health_monitor.py::TestHealthMonitor::test_register_component_with_logger PASSED [ 57%]
tests/core/system/implementations/test_health_monitor.py::TestHealthMonitor::test_register_duplicate_component PASSED [ 57%]
tests/core/system/implementations/test_health_monitor.py::TestHealthMonitor::test_unregister_component PASSED [ 57%]
tests/core/system/implementations/test_health_monitor.py::TestHealthMonitor::test_unregister_component_logs_warning_when_not_registered PASSED [ 57%]
tests/core/system/implementations/test_health_monitor.py::TestHealthMonitor::test_unregister_component_with_logger PASSED [ 57%]
tests/core/system/implementations/test_health_monitor.py::TestHealthMonitor::test_unregister_nonexistent_component PASSED [ 57%]
tests/core/system/interfaces/test_health_interface.py::TestComponentStatus::test_enum_values PASSED [ 57%]
tests/core/system/interfaces/test_health_interface.py::TestComponentStatus::test_enum_members PASSED [ 58%]
tests/core/system/interfaces/test_health_interface.py::TestHealthStatus::test_enum_values PASSED [ 58%]
tests/core/system/interfaces/test_health_interface.py::TestHealthStatus::test_enum_members PASSED [ 58%]
tests/core/system/interfaces/test_health_interface.py::TestComponentHealth::test_create_with_required_fields PASSED [ 58%]
tests/core/system/interfaces/test_health_interface.py::TestComponentHealth::test_create_with_optional_metrics PASSED [ 58%]
tests/core/system/interfaces/test_health_interface.py::TestComponentHealth::test_immutability PASSED [ 58%]
tests/core/system/interfaces/test_health_interface.py::TestSystemHealth::test_create_with_required_fields PASSED [ 58%]
tests/core/system/interfaces/test_health_interface.py::TestSystemHealth::test_create_with_optional_metrics PASSED [ 58%]
tests/core/system/interfaces/test_health_interface.py::TestSystemHealth::test_empty_components_list PASSED [ 58%]
tests/core/system/interfaces/test_health_interface.py::TestHealthMonitorInterface::test_interface_is_abstract PASSED [ 58%]
tests/core/system/interfaces/test_health_interface.py::TestHealthMonitorInterface::test_check_health_is_abstract PASSED [ 58%]
tests/core/system/interfaces/test_health_interface.py::TestHealthMonitorInterface::test_implement_interface PASSED [ 58%]
tests/core/system/interfaces/test_health_interface.py::TestHealthCheckInterface::test_interface_is_abstract PASSED [ 58%]
tests/core/system/interfaces/test_health_interface.py::TestHealthCheckInterface::test_check_is_abstract PASSED [ 58%]
tests/core/system/interfaces/test_health_interface.py::TestHealthCheckInterface::test_implement_interface PASSED [ 58%]
tests/core/system/interfaces/test_health_interface.py::TestIntegration::test_component_health_in_system_health PASSED [ 58%]
tests/core/system/interfaces/test_health_interface.py::TestIntegration::test_health_status_aggregation PASSED [ 58%]
tests/core/system/interfaces/test_health_interface.py::TestTypeSafety::test_component_status_type PASSED [ 59%]
tests/core/system/interfaces/test_health_interface.py::TestTypeSafety::test_health_status_type PASSED [ 59%]
tests/core/system/interfaces/test_health_interface.py::TestTypeSafety::test_component_health_types PASSED [ 59%]
tests/core/system/interfaces/test_health_interface.py::TestTypeSafety::test_system_health_types PASSED [ 59%]
tests/core/system/test_system_factory.py::TestSystemComponentFactory::test_clear_monitors PASSED [ 59%]
tests/core/system/test_system_factory.py::TestSystemComponentFactory::test_create_health_check_default PASSED [ 59%]
tests/core/system/test_system_factory.py::TestSystemComponentFactory::test_create_health_check_invalid_type PASSED [ 59%]
tests/core/system/test_system_factory.py::TestSystemComponentFactory::test_create_health_check_with_logger PASSED [ 59%]
tests/core/system/test_system_factory.py::TestSystemComponentFactory::test_create_health_monitor_caching PASSED [ 59%]
tests/core/system/test_system_factory.py::TestSystemComponentFactory::test_create_health_monitor_default PASSED [ 59%]
tests/core/system/test_system_factory.py::TestSystemComponentFactory::test_create_health_monitor_with_logger PASSED [ 59%]
tests/core/system/test_system_factory.py::TestSystemComponentFactory::test_create_health_monitor_with_name PASSED [ 59%]
tests/core/system/test_system_factory.py::TestSystemComponentFactory::test_get_health_monitor PASSED [ 59%]
tests/core/system/test_system_factory.py::TestSystemComponentFactory::test_get_health_monitor_nonexistent PASSED [ 59%]
tests/core/system/test_system_factory.py::TestSystemComponentFactory::test_get_registered_monitors PASSED [ 59%]
tests/core/system/test_system_factory.py::TestSystemComponentFactory::test_health_monitor_integration PASSED [ 59%]
tests/core/system/test_system_factory.py::TestSystemComponentFactory::test_health_monitor_with_system_metrics PASSED [ 60%]
tests/core/system/test_system_factory.py::TestSystemComponentFactory::test_register_component PASSED [ 60%]
tests/core/system/test_system_factory.py::TestSystemComponentFactory::test_register_component_fallback_implementation PASSED [ 60%]
tests/core/system/test_system_factory.py::TestSystemComponentFactory::test_register_component_nonexistent_monitor PASSED [ 60%]
tests/core/system/test_system_factory.py::TestSystemComponentFactory::test_register_component_with_custom_check PASSED [ 60%]
tests/core/system/test_system_factory.py::TestSystemComponentFactory::test_unregister_component PASSED [ 60%]
tests/core/system/test_system_factory.py::TestSystemComponentFactory::test_unregister_component_nonexistent_monitor PASSED [ 60%]
tests/core/test_core_init.py::TestVersionFunctions::test_get_version_success PASSED [ 60%]
tests/core/test_core_init.py::TestVersionFunctions::test_get_version_failure PASSED [ 60%]
tests/core/test_core_init.py::TestVersionFunctions::test_get_version_returns_string PASSED [ 60%]
tests/core/test_core_init.py::TestVersionFunctions::test_get_schema_version PASSED [ 60%]
tests/core/test_core_init.py::TestVersionFunctions::test_get_schema_version_returns_string PASSED [ 60%]
tests/core/test_core_init.py::TestBootstrapCore::test_bootstrap_core_success FAILED [ 60%]
tests/core/test_core_init.py::TestBootstrapCore::test_bootstrap_core_with_custom_config FAILED [ 60%]
tests/core/test_core_init.py::TestBootstrapCore::test_bootstrap_core_import_error PASSED [ 60%]
tests/core/test_core_init.py::TestBootstrapCore::test_bootstrap_core_returns_core_components FAILED [ 60%]
tests/core/test_core_init.py::TestBootstrapCore::test_bootstrap_core_with_jforex_enabled FAILED [ 60%]
tests/core/test_core_init.py::TestBootstrapCore::test_bootstrap_core_with_jforex_disabled FAILED [ 61%]
tests/core/test_core_init.py::TestGetCoreComponents::test_get_core_components_first_call PASSED [ 61%]
tests/core/test_core_init.py::TestGetCoreComponents::test_get_core_components_cached PASSED [ 61%]
tests/core/test_core_init.py::TestGetCoreComponents::test_get_core_components_returns_core_components PASSED [ 61%]
tests/core/test_core_init.py::TestIntegration::test_version_and_bootstrap_integration PASSED [ 61%]
tests/core/test_core_init.py::TestIntegration::test_all_imports_available PASSED [ 61%]
tests/core/test_core_init.py::TestIntegration::test_core_components_singleton_pattern PASSED [ 61%]
tests/core/test_init_version_fallback.py::TestVersionFallback::test_version_is_available PASSED [ 61%]
tests/core/test_init_version_fallback.py::TestVersionFallback::test_schema_version_is_available PASSED [ 61%]
tests/core/test_init_version_fallback.py::TestVersionFallback::test_all_list_is_exported PASSED [ 61%]
tests/core/test_init_version_fallback.py::TestVersionFallback::test_version_fallback_on_package_not_found FAILED [ 61%]
tests/core/test_init_version_fallback.py::TestVersionFallback::test_version_is_final PASSED [ 61%]
tests/core/test_pyproject_ui_dependencies.py::test_ui_optional_dependencies_exist PASSED [ 61%]
tests/core/test_pyproject_ui_dependencies.py::test_ui_dependencies_contain_required_packages PASSED [ 61%]
tests/core/test_pyproject_ui_dependencies.py::test_ui_dependencies_have_correct_versions PASSED [ 61%]
tests/core/test_pyproject_ui_dependencies.py::test_full_includes_ui PASSED [ 61%]
tests/core/test_pyproject_ui_dependencies.py::test_ui_dependencies_no_duplicates PASSED [ 61%]
tests/core/test_pyproject_ui_dependencies.py::test_pyproject_toml_is_valid PASSED [ 62%]
tests/core/utils/exceptions/test_util_errors.py::TestUtilError::test_util_error_creation PASSED [ 62%]
tests/core/utils/exceptions/test_util_errors.py::TestUtilError::test_util_error_with_details PASSED [ 62%]
tests/core/utils/exceptions/test_util_errors.py::TestUtilError::test_util_error_is_neural_ai_exception PASSED [ 62%]
tests/core/utils/exceptions/test_util_errors.py::TestUtilError::test_util_error_is_exception PASSED [ 62%]
tests/core/utils/exceptions/test_util_errors.py::TestHardwareDetectionError::test_hardware_detection_error_creation PASSED [ 62%]
tests/core/utils/exceptions/test_util_errors.py::TestHardwareDetectionError::test_hardware_detection_error_with_type PASSED [ 62%]
tests/core/utils/exceptions/test_util_errors.py::TestHardwareDetectionError::test_hardware_detection_error_inheritance PASSED [ 62%]
tests/core/utils/exceptions/test_util_errors.py::TestHardwareDetectionError::test_hardware_detection_error_is_exception PASSED [ 62%]
tests/core/utils/exceptions/test_util_errors.py::TestInitExports::test_init_exports_util_error PASSED [ 62%]
tests/core/utils/exceptions/test_util_errors.py::TestInitExports::test_init_exports_hardware_detection_error PASSED [ 62%]
tests/core/utils/exceptions/test_util_errors.py::TestInitExports::test_init_all_list PASSED [ 62%]
tests/core/utils/exceptions/test_util_errors.py::TestInitExports::test_direct_import_from_module PASSED [ 62%]
tests/core/utils/interfaces/test_hardware_interface.py::TestHardwareInterface::test_interface_is_abstract PASSED [ 62%]
tests/core/utils/interfaces/test_hardware_interface.py::TestHardwareInterface::test_interface_has_required_methods PASSED [ 62%]
tests/core/utils/interfaces/test_hardware_interface.py::TestHardwareInterface::test_all_abstract_methods_implemented PASSED [ 62%]
tests/core/utils/test_decorators.py::TestTraceDecorator::test_trace_successful_execution PASSED [ 63%]
tests/core/utils/test_decorators.py::TestTraceDecorator::test_trace_with_kwargs PASSED [ 63%]
tests/core/utils/test_decorators.py::TestTraceDecorator::test_trace_with_unsafe_args PASSED [ 63%]
tests/core/utils/test_decorators.py::TestTraceDecorator::test_trace_function_name_preserved PASSED [ 63%]
tests/core/utils/test_decorators.py::TestTraceDecorator::test_trace_docstring_preserved PASSED [ 63%]
tests/core/utils/test_decorators.py::TestTraceDecorator::test_trace_exception_handling PASSED [ 63%]
tests/core/utils/test_decorators.py::TestTraceDecorator::test_trace_call_id_uniqueness PASSED [ 63%]
tests/core/utils/test_decorators.py::TestTraceDecorator::test_trace_duration_measurement PASSED [ 63%]
tests/core/utils/test_decorators.py::TestTraceDecorator::test_trace_with_mixed_args PASSED [ 63%]
tests/core/utils/test_decorators.py::TestTraceDecorator::test_trace_no_args_function PASSED [ 63%]
tests/core/utils/test_decorators.py::TestTraceDecorator::test_trace_with_safe_types PASSED [ 63%]
tests/core/utils/test_decorators.py::TestTraceDecoratorIntegration::test_trace_real_logger PASSED [ 63%]
tests/core/utils/test_decorators.py::TestTraceDecoratorIntegration::test_trace_performance_overhead PASSED [ 63%]
tests/core/utils/test_hardware_info.py::TestHardwareInfo::test_has_avx2_linux_with_avx2 PASSED [ 63%]
tests/core/utils/test_hardware_info.py::TestHardwareInfo::test_has_avx2_linux_without_avx2 PASSED [ 63%]
tests/core/utils/test_hardware_info.py::TestHardwareInfo::test_has_avx2_non_linux PASSED [ 63%]
tests/core/utils/test_hardware_info.py::TestHardwareInfo::test_has_avx2_file_not_found PASSED [ 63%]
tests/core/utils/test_hardware_info.py::TestHardwareInfo::test_get_cpu_features_linux PASSED [ 64%]
tests/core/utils/test_hardware_info.py::TestHardwareInfo::test_get_cpu_features_non_linux PASSED [ 64%]
tests/core/utils/test_hardware_info.py::TestHardwareInfo::test_get_cpu_features_file_not_found PASSED [ 64%]
tests/core/utils/test_hardware_info.py::TestHardwareInfo::test_supports_simd_with_simd PASSED [ 64%]
tests/core/utils/test_hardware_info.py::TestHardwareInfo::test_supports_simd_without_simd PASSED [ 64%]
tests/core/utils/test_hardware_info.py::TestHardwareInfo::test_supports_simd_partial_simd PASSED [ 64%]
tests/core/utils/test_hardware_info.py::TestHardwareInfo::test_interface_implementation PASSED [ 64%]
tests/core/utils/test_hardware_info.py::TestHardwareInfo::test_has_avx2_file_read_error PASSED [ 64%]
tests/core/utils/test_hardware_info.py::TestHardwareInfo::test_get_cpu_features_file_read_error PASSED [ 64%]
tests/core/utils/test_hardware_info.py::TestHardwareInfo::test_has_avx2_linux_no_flags_line PASSED [ 64%]
tests/core/utils/test_hardware_info.py::TestHardwareInfo::test_get_cpu_features_linux_no_flags_line PASSED [ 64%]
tests/core/utils/test_utils_factory.py::TestHardwareFactory::test_get_hardware_info_returns_hardware_info_instance PASSED [ 64%]
tests/core/utils/test_utils_factory.py::TestHardwareFactory::test_get_hardware_info_returns_new_instance PASSED [ 64%]
tests/core/utils/test_utils_factory.py::TestHardwareFactory::test_get_hardware_interface_returns_hardware_interface PASSED [ 64%]
tests/core/utils/test_utils_factory.py::TestHardwareFactory::test_get_hardware_interface_returns_new_instance PASSED [ 64%]
tests/core/utils/test_utils_factory.py::TestHardwareFactory::test_get_hardware_info_and_interface_return_different_instances PASSED [ 64%]
tests/core/utils/test_utils_factory.py::TestHardwareFactory::test_hardware_info_implements_hardware_interface PASSED [ 65%]
tests/core/utils/test_utils_factory.py::TestHardwareFactory::test_get_hardware_info_imports_correctly PASSED [ 65%]
tests/core/utils/test_utils_factory.py::TestHardwareFactory::test_get_hardware_interface_imports_correctly PASSED [ 65%]
tests/core/utils/test_utils_factory.py::TestHardwareFactory::test_factory_methods_are_static PASSED [ 65%]
tests/core/utils/test_utils_factory.py::TestHardwareFactoryIntegration::test_factory_creates_working_hardware_info_instance PASSED [ 65%]
tests/core/utils/test_utils_factory.py::TestHardwareFactoryIntegration::test_factory_creates_working_hardware_interface PASSED [ 65%]
tests/data/ingestion/test_market_data_persister.py::TestMarketDataPersisterInit::test_init_with_default_values PASSED [ 65%]
tests/data/ingestion/test_market_data_persister.py::TestMarketDataPersisterInit::test_init_with_custom_buffer_size PASSED [ 65%]
tests/data/ingestion/test_market_data_persister.py::TestMarketDataPersisterStartStop::test_start_success PASSED [ 65%]
tests/data/ingestion/test_market_data_persister.py::TestMarketDataPersisterStartStop::test_start_when_already_running PASSED [ 65%]
tests/data/ingestion/test_market_data_persister.py::TestMarketDataPersisterStartStop::test_stop_success PASSED [ 65%]
tests/data/ingestion/test_market_data_persister.py::TestMarketDataPersisterStartStop::test_stop_when_not_running PASSED [ 65%]
tests/data/ingestion/test_market_data_persister.py::TestMarketDataPersisterOnMarketData::test_on_market_data_single_event PASSED [ 65%]
tests/data/ingestion/test_market_data_persister.py::TestMarketDataPersisterOnMarketData::test_on_market_data_batch_events PASSED [ 65%]
tests/data/ingestion/test_market_data_persister.py::TestMarketDataPersisterOnMarketData::test_on_market_data_unknown_format PASSED [ 65%]
tests/data/ingestion/test_market_data_persister.py::TestMarketDataPersisterOnMarketData::test_on_market_data_triggers_flush_at_limit PASSED [ 65%]
tests/data/ingestion/test_market_data_persister.py::TestMarketDataPersisterPeriodicFlush::test_periodic_flush_triggers_on_new_hour SKIPPED [ 65%]
tests/data/ingestion/test_market_data_persister.py::TestMarketDataPersisterPeriodicFlush::test_periodic_flush_handles_exception SKIPPED [ 66%]
tests/data/ingestion/test_market_data_persister.py::TestMarketDataPersisterFlush::test_flush_all_buffers_with_data PASSED [ 66%]
tests/data/ingestion/test_market_data_persister.py::TestMarketDataPersisterFlush::test_flush_all_buffers_empty PASSED [ 66%]
tests/data/ingestion/test_market_data_persister.py::TestMarketDataPersisterFlush::test_flush_symbol_buffer_success FAILED [ 66%]
tests/data/ingestion/test_market_data_persister.py::TestMarketDataPersisterFlush::test_flush_symbol_buffer_empty FAILED [ 66%]
tests/data/ingestion/test_market_data_persister.py::TestMarketDataPersisterFlush::test_flush_symbol_buffer_handles_exception FAILED [ 66%]
tests/data/ingestion/test_market_data_persister.py::TestMarketDataPersisterSave::test_save_events_to_storage_with_parquet_service SKIPPED [ 66%]
tests/data/ingestion/test_market_data_persister.py::TestMarketDataPersisterSave::test_save_events_to_storage_fallback SKIPPED [ 66%]
tests/data/ingestion/test_market_data_persister.py::TestMarketDataPersisterSave::test_save_events_to_storage_empty FAILED [ 66%]
tests/data/ingestion/test_market_data_persister.py::TestMarketDataPersisterSave::test_save_events_to_storage_handles_exception SKIPPED [ 66%]
tests/data/ingestion/test_market_data_persister.py::TestMarketDataPersisterConvertToDataFrame::test_convert_events_to_dataframe_with_pandas FAILED [ 66%]
tests/data/ingestion/test_market_data_persister.py::TestMarketDataPersisterConvertToDataFrame::test_convert_events_to_dataframe_with_polars FAILED [ 66%]
tests/data/ingestion/test_market_data_persister.py::TestMarketDataPersisterConvertToDataFrame::test_convert_events_to_dataframe_no_library FAILED [ 66%]
tests/data/ingestion/test_market_data_persister.py::TestMarketDataPersisterIntegration::test_full_workflow FAILED [ 66%]
tests/data/storage/backends/test_base.py::TestDataFrameProtocol::test_protocol_has_required_members PASSED [ 66%]
tests/data/storage/backends/test_base.py::TestStorageBackend::test_backend_is_abstract PASSED [ 66%]
tests/data/storage/backends/test_base.py::TestStorageBackend::test_backend_initialization FAILED [ 66%]
tests/data/storage/backends/test_base.py::TestStorageBackend::test_validate_data_method FAILED [ 67%]
tests/data/storage/backends/test_base.py::TestStorageBackend::test_supports_format_method FAILED [ 67%]
tests/data/storage/backends/test_base.py::TestStorageBackend::test_repr_method FAILED [ 67%]
tests/data/storage/backends/test_base.py::TestStorageBackend::test_all_abstract_methods_called FAILED [ 67%]
tests/data/storage/backends/test_base.py::TestStorageBackend::test_validate_data_edge_cases FAILED [ 67%]
tests/data/storage/backends/test_pandas_backend.py::TestPandasDataFrame::test_init FAILED [ 67%]
tests/data/storage/backends/test_pandas_backend.py::TestPandasDataFrame::test_import_pandas FAILED [ 67%]
tests/data/storage/backends/test_pandas_backend.py::TestPandasDataFrame::test_pd_property FAILED [ 67%]
tests/data/storage/backends/test_pandas_backend.py::TestPandasDataFrame::test_fp_property FAILED [ 67%]
tests/data/storage/backends/test_pandas_backend.py::TestPandasBackend::test_init ERROR [ 67%]
tests/data/storage/backends/test_pandas_backend.py::TestPandasBackend::test_ensure_initialized ERROR [ 67%]
tests/data/storage/backends/test_pandas_backend.py::TestPandasBackend::test_write_basic ERROR [ 67%]
tests/data/storage/backends/test_pandas_backend.py::TestPandasBackend::test_write_with_compression ERROR [ 67%]
tests/data/storage/backends/test_pandas_backend.py::TestPandasBackend::test_write_invalid_data ERROR [ 67%]
tests/data/storage/backends/test_pandas_backend.py::TestPandasBackend::test_write_invalid_path ERROR [ 67%]
tests/data/storage/backends/test_pandas_backend.py::TestPandasBackend::test_read_basic ERROR [ 67%]
tests/data/storage/backends/test_pandas_backend.py::TestPandasBackend::test_read_with_columns ERROR [ 68%]
tests/data/storage/backends/test_pandas_backend.py::TestPandasBackend::test_read_file_not_found ERROR [ 68%]
tests/data/storage/backends/test_pandas_backend.py::TestPandasBackend::test_read_chunked ERROR [ 68%]
tests/data/storage/backends/test_pandas_backend.py::TestPandasBackend::test_append_to_new_file ERROR [ 68%]
tests/data/storage/backends/test_pandas_backend.py::TestPandasBackend::test_append_to_existing_file ERROR [ 68%]
tests/data/storage/backends/test_pandas_backend.py::TestPandasBackend::test_append_with_schema_validation_valid ERROR [ 68%]
tests/data/storage/backends/test_pandas_backend.py::TestPandasBackend::test_append_with_schema_validation_invalid ERROR [ 68%]
tests/data/storage/backends/test_pandas_backend.py::TestPandasBackend::test_append_invalid_data ERROR [ 68%]
tests/data/storage/backends/test_pandas_backend.py::TestPandasBackend::test_supports_format ERROR [ 68%]
tests/data/storage/backends/test_pandas_backend.py::TestPandasBackend::test_get_info ERROR [ 68%]
tests/data/storage/backends/test_pandas_backend.py::TestPandasBackend::test_get_info_file_not_found ERROR [ 68%]
tests/data/storage/backends/test_pandas_backend.py::TestPandasBackend::test_validate_data ERROR [ 68%]
tests/data/storage/backends/test_pandas_backend.py::TestPandasBackend::test_repr ERROR [ 68%]
tests/data/storage/backends/test_pandas_backend.py::TestPandasBackend::test_write_partitioned ERROR [ 68%]
tests/data/storage/backends/test_pandas_backend.py::TestPandasBackend::test_write_with_index ERROR [ 68%]
tests/data/storage/backends/test_pandas_backend.py::TestPandasBackend::test_read_with_filters ERROR [ 68%]
tests/data/storage/backends/test_pandas_backend.py::TestPandasBackend::test_validate_schema_valid ERROR [ 68%]
tests/data/storage/backends/test_pandas_backend.py::TestPandasBackend::test_validate_schema_invalid ERROR [ 69%]
tests/data/storage/backends/test_pandas_backend.py::TestPandasBackend::test_validate_schema_exception ERROR [ 69%]
tests/data/storage/backends/test_polars_backend.py::TestPolarsDataFrame::test_init FAILED [ 69%]
tests/data/storage/backends/test_polars_backend.py::TestPolarsDataFrame::test_import_polars FAILED [ 69%]
tests/data/storage/backends/test_polars_backend.py::TestPolarsDataFrame::test_pl_property FAILED [ 69%]
tests/data/storage/backends/test_polars_backend.py::TestPolarsDataFrame::test_pa_property FAILED [ 69%]
tests/data/storage/backends/test_polars_backend.py::TestPolarsDataFrame::test_pq_property FAILED [ 69%]
tests/data/storage/backends/test_polars_backend.py::TestPolarsBackend::test_init ERROR [ 69%]
tests/data/storage/backends/test_polars_backend.py::TestPolarsBackend::test_ensure_initialized ERROR [ 69%]
tests/data/storage/backends/test_polars_backend.py::TestPolarsBackend::test_write_basic ERROR [ 69%]
tests/data/storage/backends/test_polars_backend.py::TestPolarsBackend::test_write_with_compression ERROR [ 69%]
tests/data/storage/backends/test_polars_backend.py::TestPolarsBackend::test_write_invalid_data ERROR [ 69%]
tests/data/storage/backends/test_polars_backend.py::TestPolarsBackend::test_write_invalid_path ERROR [ 69%]
tests/data/storage/backends/test_polars_backend.py::TestPolarsBackend::test_read_basic ERROR [ 69%]
tests/data/storage/backends/test_polars_backend.py::TestPolarsBackend::test_read_with_columns ERROR [ 69%]
tests/data/storage/backends/test_polars_backend.py::TestPolarsBackend::test_read_file_not_found ERROR [ 69%]
tests/data/storage/backends/test_polars_backend.py::TestPolarsBackend::test_read_chunked ERROR [ 69%]
tests/data/storage/backends/test_polars_backend.py::TestPolarsBackend::test_append_to_new_file ERROR [ 70%]
tests/data/storage/backends/test_polars_backend.py::TestPolarsBackend::test_append_to_existing_file ERROR [ 70%]
tests/data/storage/backends/test_polars_backend.py::TestPolarsBackend::test_append_with_schema_validation_valid ERROR [ 70%]
tests/data/storage/backends/test_polars_backend.py::TestPolarsBackend::test_append_with_schema_validation_invalid ERROR [ 70%]
tests/data/storage/backends/test_polars_backend.py::TestPolarsBackend::test_append_invalid_data ERROR [ 70%]
tests/data/storage/backends/test_polars_backend.py::TestPolarsBackend::test_supports_format ERROR [ 70%]
tests/data/storage/backends/test_polars_backend.py::TestPolarsBackend::test_get_info ERROR [ 70%]
tests/data/storage/backends/test_polars_backend.py::TestPolarsBackend::test_get_info_file_not_found ERROR [ 70%]
tests/data/storage/backends/test_polars_backend.py::TestPolarsBackend::test_validate_data ERROR [ 70%]
tests/data/storage/backends/test_polars_backend.py::TestPolarsBackend::test_repr ERROR [ 70%]
tests/data/storage/backends/test_polars_backend.py::TestPolarsBackend::test_write_partitioned ERROR [ 70%]
tests/data/storage/backends/test_polars_backend.py::TestPolarsBackend::test_read_with_filters ERROR [ 70%]
tests/data/storage/backends/test_polars_backend.py::TestPolarsBackend::test_validate_schema_valid ERROR [ 70%]
tests/data/storage/backends/test_polars_backend.py::TestPolarsBackend::test_validate_schema_invalid ERROR [ 70%]
tests/data/storage/backends/test_polars_backend.py::TestPolarsBackend::test_validate_schema_exception ERROR [ 70%]
tests/data/storage/backends/test_polars_backend.py::TestPolarsBackend::test_read_chunked_implementation ERROR [ 70%]
tests/data/storage/implementations/test_file_storage.py::TestFileStorage::test_init_default_path FAILED [ 71%]
tests/data/storage/implementations/test_file_storage.py::TestFileStorage::test_init_custom_path FAILED [ 71%]
tests/data/storage/implementations/test_file_storage.py::TestFileStorage::test_init_with_logger PASSED [ 71%]
tests/data/storage/implementations/test_file_storage.py::TestFileStorage::test_get_full_path_absolute ERROR [ 71%]
tests/data/storage/implementations/test_file_storage.py::TestFileStorage::test_get_full_path_relative ERROR [ 71%]
tests/data/storage/implementations/test_file_storage.py::TestFileStorage::test_exists_true ERROR [ 71%]
tests/data/storage/implementations/test_file_storage.py::TestFileStorage::test_exists_false ERROR [ 71%]
tests/data/storage/implementations/test_file_storage.py::TestFileStorage::test_save_dataframe_csv ERROR [ 71%]
tests/data/storage/implementations/test_file_storage.py::TestFileStorage::test_save_dataframe_excel ERROR [ 71%]
tests/data/storage/implementations/test_file_storage.py::TestFileStorage::test_save_dataframe_invalid_format ERROR [ 71%]
tests/data/storage/implementations/test_file_storage.py::TestFileStorage::test_load_dataframe_not_found ERROR [ 71%]
tests/data/storage/implementations/test_file_storage.py::TestFileStorage::test_save_object_json ERROR [ 71%]
tests/data/storage/implementations/test_file_storage.py::TestFileStorage::test_save_object_invalid_format ERROR [ 71%]
tests/data/storage/implementations/test_file_storage.py::TestFileStorage::test_load_object_not_found ERROR [ 71%]
tests/data/storage/implementations/test_file_storage.py::TestFileStorage::test_load_object_invalid_json ERROR [ 71%]
tests/data/storage/implementations/test_file_storage.py::TestFileStorage::test_get_metadata_file ERROR [ 71%]
tests/data/storage/implementations/test_file_storage.py::TestFileStorage::test_get_metadata_not_found ERROR [ 71%]
tests/data/storage/implementations/test_file_storage.py::TestFileStorage::test_delete_file ERROR [ 72%]
tests/data/storage/implementations/test_file_storage.py::TestFileStorage::test_delete_not_found ERROR [ 72%]
tests/data/storage/implementations/test_file_storage.py::TestFileStorage::test_list_dir ERROR [ 72%]
tests/data/storage/implementations/test_file_storage.py::TestFileStorage::test_list_dir_with_pattern ERROR [ 72%]
tests/data/storage/implementations/test_file_storage.py::TestFileStorage::test_list_dir_not_found ERROR [ 72%]
tests/data/storage/implementations/test_file_storage.py::TestFileStorage::test_check_permissions_read_only ERROR [ 72%]
tests/data/storage/implementations/test_file_storage.py::TestFileStorage::test_get_storage_info ERROR [ 72%]
tests/data/storage/implementations/test_file_storage.py::TestFileStorage::test_atomic_write_json ERROR [ 72%]
tests/data/storage/implementations/test_file_storage.py::TestFileStorage::test_atomic_write_dataframe ERROR [ 72%]
tests/data/storage/implementations/test_file_storage.py::TestFileStorage::test_setup_format_handlers ERROR [ 72%]
tests/data/storage/implementations/test_file_storage.py::TestFileStorage::test_save_dataframe_with_kwargs ERROR [ 72%]
tests/data/storage/implementations/test_file_storage.py::TestFileStorage::test_load_dataframe_with_kwargs ERROR [ 72%]
tests/data/storage/implementations/test_file_storage.py::TestFileStorage::test_save_object_with_kwargs ERROR [ 72%]
tests/data/storage/implementations/test_file_storage.py::TestFileStorage::test_load_object_with_kwargs ERROR [ 72%]
tests/data/storage/implementations/test_file_storage.py::TestFileStorage::test_check_disk_space_sufficient ERROR [ 72%]
tests/data/storage/implementations/test_file_storage.py::TestFileStorage::test_check_disk_space_insufficient ERROR [ 72%]
tests/data/storage/implementations/test_file_storage.py::TestFileStorage::test_check_disk_space_os_error ERROR [ 73%]
tests/data/storage/implementations/test_file_storage.py::TestFileStorage::test_check_permissions_write_denied ERROR [ 73%]
tests/data/storage/implementations/test_file_storage.py::TestFileStorage::test_check_permissions_read_denied ERROR [ 73%]
tests/data/storage/implementations/test_file_storage.py::TestFileStorage::test_check_permissions_parent_not_exists ERROR [ 73%]
tests/data/storage/implementations/test_file_storage.py::TestFileStorage::test_get_storage_info_os_error ERROR [ 73%]
tests/data/storage/implementations/test_file_storage.py::TestFileStorage::test_atomic_write_bytes ERROR [ 73%]
tests/data/storage/implementations/test_file_storage.py::TestFileStorage::test_atomic_write_string ERROR [ 73%]
tests/data/storage/implementations/test_file_storage.py::TestFileStorage::test_atomic_write_invalid_format ERROR [ 73%]
tests/data/storage/implementations/test_file_storage.py::TestFileStorage::test_atomic_write_os_error_save ERROR [ 73%]
tests/data/storage/implementations/test_file_storage.py::TestFileStorage::test_save_dataframe_format_detection_failure ERROR [ 73%]
tests/data/storage/implementations/test_file_storage.py::TestFileStorage::test_save_dataframe_excel_format_detection ERROR [ 73%]
tests/data/storage/implementations/test_file_storage.py::TestFileStorage::test_save_dataframe_disk_space_check_failure ERROR [ 73%]
tests/data/storage/implementations/test_file_storage.py::TestFileStorage::test_save_dataframe_io_error ERROR [ 73%]
tests/data/storage/implementations/test_file_storage.py::TestFileStorage::test_load_dataframe_format_detection_failure ERROR [ 73%]
tests/data/storage/implementations/test_file_storage.py::TestFileStorage::test_load_dataframe_excel_format_detection ERROR [ 73%]
tests/data/storage/implementations/test_file_storage.py::TestFileStorage::test_load_dataframe_io_error ERROR [ 73%]
tests/data/storage/implementations/test_file_storage.py::TestFileStorage::test_save_object_format_detection_failure ERROR [ 73%]
tests/data/storage/implementations/test_file_storage.py::TestFileStorage::test_save_object_serialization_error ERROR [ 74%]
tests/data/storage/implementations/test_file_storage.py::TestFileStorage::test_save_object_io_error ERROR [ 74%]
tests/data/storage/implementations/test_file_storage.py::TestFileStorage::test_load_object_format_detection_failure ERROR [ 74%]
tests/data/storage/implementations/test_file_storage.py::TestFileStorage::test_load_object_deserialization_error ERROR [ 74%]
tests/data/storage/implementations/test_file_storage.py::TestFileStorage::test_load_object_os_error ERROR [ 74%]
tests/data/storage/implementations/test_file_storage.py::TestFileStorage::test_get_metadata_os_error ERROR [ 74%]
tests/data/storage/implementations/test_file_storage.py::TestFileStorage::test_delete_directory ERROR [ 74%]
tests/data/storage/implementations/test_file_storage.py::TestFileStorage::test_delete_io_error ERROR [ 74%]
tests/data/storage/implementations/test_file_storage.py::TestFileStorage::test_list_dir_not_directory ERROR [ 74%]
tests/data/storage/implementations/test_file_storage.py::TestFileStorage::test_list_dir_glob_error ERROR [ 74%]
tests/data/storage/implementations/test_parquet_storage.py::TestParquetStorageService::test_initialization_with_hardware_and_logger PASSED [ 74%]
tests/data/storage/implementations/test_parquet_storage.py::TestParquetStorageService::test_initialization_without_hardware_and_logger FAILED [ 74%]
tests/data/storage/implementations/test_parquet_storage.py::TestParquetStorageService::test_backend_selection_avx2 FAILED [ 74%]
tests/data/storage/implementations/test_parquet_storage.py::TestParquetStorageService::test_backend_selection_no_avx2 FAILED [ 74%]
tests/data/storage/implementations/test_parquet_storage.py::TestParquetStorageService::test_get_path_with_unique_id PASSED [ 74%]
tests/data/storage/implementations/test_parquet_storage.py::TestParquetStorageService::test_get_path_without_unique_id PASSED [ 74%]
tests/data/storage/implementations/test_parquet_storage.py::TestParquetStorageService::test_store_tick_data_success FAILED [ 74%]
tests/data/storage/implementations/test_parquet_storage.py::TestParquetStorageService::test_store_tick_data_empty_dataframe PASSED [ 75%]
tests/data/storage/implementations/test_parquet_storage.py::TestParquetStorageService::test_store_tick_data_missing_columns PASSED [ 75%]
tests/data/storage/implementations/test_parquet_storage.py::TestParquetStorageService::test_read_tick_data_no_files FAILED [ 75%]
tests/data/storage/implementations/test_parquet_storage.py::TestParquetStorageService::test_read_tick_data_with_files FAILED [ 75%]
tests/data/storage/implementations/test_parquet_storage.py::TestParquetStorageService::test_get_available_dates FAILED [ 75%]
tests/data/storage/implementations/test_parquet_storage.py::TestParquetStorageService::test_get_available_dates_no_symbol PASSED [ 75%]
tests/data/storage/implementations/test_parquet_storage.py::TestParquetStorageService::test_calculate_checksum_no_files PASSED [ 75%]
tests/data/storage/implementations/test_parquet_storage.py::TestParquetStorageService::test_calculate_checksum_with_files FAILED [ 75%]
tests/data/storage/implementations/test_parquet_storage.py::TestParquetStorageService::test_verify_data_integrity_valid FAILED [ 75%]
tests/data/storage/implementations/test_parquet_storage.py::TestParquetStorageService::test_verify_data_integrity_no_files PASSED [ 75%]
tests/data/storage/implementations/test_parquet_storage.py::TestParquetStorageService::test_verify_data_integrity_missing_columns PASSED [ 75%]
tests/data/storage/implementations/test_parquet_storage.py::TestParquetStorageService::test_get_storage_stats FAILED [ 75%]
tests/data/storage/implementations/test_parquet_storage.py::TestParquetStorageService::test_concat_dataframes_polars FAILED [ 75%]
tests/data/storage/implementations/test_parquet_storage.py::TestParquetStorageService::test_concat_dataframes_pandas FAILED [ 75%]
tests/data/storage/implementations/test_parquet_storage.py::TestParquetStorageService::test_deduplicate_data_polars FAILED [ 75%]
tests/data/storage/implementations/test_parquet_storage.py::TestParquetStorageService::test_deduplicate_data_pandas FAILED [ 75%]
tests/data/storage/implementations/test_parquet_storage.py::TestParquetStorageService::test_sort_by_timestamp_polars FAILED [ 76%]
tests/data/storage/implementations/test_parquet_storage.py::TestParquetStorageService::test_sort_by_timestamp_pandas FAILED [ 76%]
tests/data/storage/implementations/test_parquet_storage.py::TestParquetStorageService::test_filter_by_timestamp FAILED [ 76%]
tests/data/storage/implementations/test_parquet_storage.py::TestParquetStorageService::test_read_parquet_async PASSED [ 76%]
tests/data/storage/implementations/test_parquet_storage.py::TestParquetStorageService::test_save_dataframe FAILED [ 76%]
tests/data/storage/implementations/test_parquet_storage.py::TestParquetStorageService::test_load_dataframe FAILED [ 76%]
tests/data/storage/implementations/test_parquet_storage.py::TestParquetStorageService::test_exists FAILED [ 76%]
tests/data/storage/implementations/test_parquet_storage.py::TestParquetStorageService::test_get_metadata FAILED [ 76%]
tests/data/storage/implementations/test_parquet_storage.py::TestParquetStorageService::test_delete_file FAILED [ 76%]
tests/data/storage/implementations/test_parquet_storage.py::TestParquetStorageService::test_delete_directory FAILED [ 76%]
tests/data/storage/implementations/test_parquet_storage.py::TestParquetStorageService::test_list_dir FAILED [ 76%]
tests/data/storage/interfaces/test_storage_factory_interface.py::TestStorageFactoryInterface::test_is_protocol PASSED [ 76%]
tests/data/storage/interfaces/test_storage_factory_interface.py::TestStorageFactoryInterface::test_has_register_storage_method PASSED [ 76%]
tests/data/storage/interfaces/test_storage_factory_interface.py::TestStorageFactoryInterface::test_has_get_storage_method PASSED [ 76%]
tests/data/storage/interfaces/test_storage_factory_interface.py::TestStorageFactoryInterface::test_cannot_instantiate_directly PASSED [ 76%]
tests/data/storage/interfaces/test_storage_factory_interface.py::TestStorageFactoryInterface::test_register_storage_signature PASSED [ 76%]
tests/data/storage/interfaces/test_storage_factory_interface.py::TestStorageFactoryInterface::test_get_storage_signature PASSED [ 76%]
tests/data/storage/interfaces/test_storage_interface.py::TestStorageInterface::test_is_protocol PASSED [ 77%]
tests/data/storage/interfaces/test_storage_interface.py::TestStorageInterface::test_has_required_methods PASSED [ 77%]
tests/data/storage/interfaces/test_storage_interface.py::TestStorageInterface::test_cannot_instantiate_directly PASSED [ 77%]
tests/data/storage/interfaces/test_storage_interface.py::TestStorageInterface::test_save_dataframe_signature PASSED [ 77%]
tests/data/storage/interfaces/test_storage_interface.py::TestStorageInterface::test_load_dataframe_signature PASSED [ 77%]
tests/data/storage/interfaces/test_storage_interface.py::TestStorageInterface::test_save_object_signature PASSED [ 77%]
tests/data/storage/interfaces/test_storage_interface.py::TestStorageInterface::test_load_object_signature PASSED [ 77%]
tests/data/storage/interfaces/test_storage_interface.py::TestStorageInterface::test_exists_signature PASSED [ 77%]
tests/data/storage/interfaces/test_storage_interface.py::TestStorageInterface::test_get_metadata_signature PASSED [ 77%]
tests/data/storage/interfaces/test_storage_interface.py::TestStorageInterface::test_delete_signature PASSED [ 77%]
tests/data/storage/interfaces/test_storage_interface.py::TestStorageInterface::test_list_dir_signature PASSED [ 77%]
tests/data/storage/test_storage_factory.py::TestStorageFactory::test_register_storage PASSED [ 77%]
tests/data/storage/test_storage_factory.py::TestStorageFactory::test_register_storage_invalid_class PASSED [ 77%]
tests/data/storage/test_storage_factory.py::TestStorageFactory::test_get_storage_file_type FAILED [ 77%]
tests/data/storage/test_storage_factory.py::TestStorageFactory::test_get_storage_parquet_type FAILED [ 77%]
tests/data/storage/test_storage_factory.py::TestStorageFactory::test_get_storage_with_kwargs FAILED [ 77%]
tests/data/storage/test_storage_factory.py::TestStorageFactory::test_get_storage_invalid_type PASSED [ 77%]
tests/data/storage/test_storage_factory.py::TestStorageFactory::test_get_storage_instantiation_failure FAILED [ 78%]
tests/data/storage/test_storage_factory.py::TestStorageFactory::test_get_storage_unexpected_error FAILED [ 78%]
tests/data/storage/test_storage_factory.py::TestStorageFactory::test_get_storage_default_base_path FAILED [ 78%]
tests/data/storage/test_storage_factory.py::TestStorageFactory::test_get_storage_with_hardware_none FAILED [ 78%]
tests/data/storage/test_storage_factory.py::TestStorageFactory::test_initial_storage_types PASSED [ 78%]
tests/data/storage/test_storage_init.py::TestStorageInit::test_version_is_available PASSED [ 78%]
tests/data/storage/test_storage_init.py::TestStorageInit::test_schema_version_is_available PASSED [ 78%]
tests/data/storage/test_storage_init.py::TestStorageInit::test_all_list_is_exported PASSED [ 78%]
tests/data/storage/test_storage_init.py::TestStorageInit::test_version_fallback_on_package_not_found PASSED [ 78%]
tests/data/storage/test_storage_init.py::TestStorageInit::test_version_is_final PASSED [ 78%]
tests/integration/test_d1_full.py::test_full_pipeline 