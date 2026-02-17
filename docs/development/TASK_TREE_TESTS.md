# 🧪 NEURAL AI NEXT - TESTS

**Generálva:** 2026-02-17 14:13:42 UTC
**Módszer:** Hibrid (AST + Pytest + Coverage + Ruff + Mypy + Pylance)
**Fájlok száma:** 214

## 📊 Statisztika

- ✅ **SECURE:** 137 (64.0%)
- 🟡 **WARNING:** 17 (7.9%)
- 🔴 **VULNERABLE:** 60 (28.0%)

---

## 6. Tests Layer (`tests/`)

| Fájl | Státusz | Pass/Fail/Err/Skip | Lint/Mypy/Pylance |
|:-----|:--------|:-------------------|:------------------|
| `tests/collectors/jforex/exceptions/test_exceptions_init.py` | ✅ SECURE | **5**/0/0/0 | 0 / 0 / 0 |
| `tests/collectors/jforex/interfaces/test_interfaces_init.py` | ✅ SECURE | **3**/0/0/0 | 0 / 0 / 0 |
| `tests/collectors/jforex/test_bi5_downloader.py` | ✅ SECURE | **43**/0/0/0 | 0 / 0 / 286 |
| `tests/collectors/jforex/test_factory.py` | ✅ SECURE | **10**/0/0/0 | 0 / 0 / 0 |
| `tests/collectors/jforex/test_jforex_init.py` | ✅ SECURE | **2**/0/0/0 | 0 / 0 / 0 |
| `tests/collectors/jforex/test_live_feed.py` | ✅ SECURE | **12**/0/0/0 | 0 / 0 / 25 |
| `tests/collectors/jforex/test_live_feed_integration.py` | 🔴 VULNERABLE | **8**/0/0/0 | 0 / 0 / 17 |
| `tests/core/base/exceptions/test_base_error.py` | ✅ SECURE | **42**/0/0/0 | 0 / 0 / 0 |
| `tests/core/base/exceptions/test_exceptions_init.py` | ✅ SECURE | **18**/0/0/0 | 0 / 0 / 0 |
| `tests/core/base/implementations/test_component_bundle.py` | ✅ SECURE | **39**/0/0/0 | 0 / 0 / 0 |
| `tests/core/base/implementations/test_di_container.py` | ✅ SECURE | **24**/0/0/0 | 0 / 0 / 20 |
| `tests/core/base/implementations/test_implementations_init.py` | ✅ SECURE | **13**/0/0/0 | 0 / 0 / 0 |
| `tests/core/base/implementations/test_lazy_loader.py` | ✅ SECURE | **10**/0/0/0 | 0 / 0 / 0 |
| `tests/core/base/implementations/test_singleton.py` | ✅ SECURE | **10**/0/0/0 | 0 / 0 / 0 |
| `tests/core/base/interfaces/test_component_interface.py` | ✅ SECURE | **13**/0/0/0 | 0 / 0 / 3 |
| `tests/core/base/interfaces/test_container_interface.py` | ✅ SECURE | **20**/0/0/0 | 0 / 0 / 6 |
| `tests/core/base/interfaces/test_interfaces_init.py` | ✅ SECURE | **12**/0/0/0 | 0 / 0 / 4 |
| `tests/core/base/test_base_init.py` | ✅ SECURE | **8**/0/0/0 | 0 / 0 / 0 |
| `tests/core/base/test_factory.py` | ✅ SECURE | **35**/0/0/0 | 0 / 0 / 37 |
| `tests/core/config/exceptions/test_config_error.py` | ✅ SECURE | **15**/0/0/0 | 0 / 0 / 0 |
| `tests/core/config/implementations/test_config_implementations_init.py` | ✅ SECURE | **4**/0/0/0 | 0 / 0 / 0 |
| `tests/core/config/implementations/test_dynamic_config_manager.py` | ✅ SECURE | **48**/0/0/0 | 0 / 0 / 54 |
| `tests/core/config/implementations/test_dynamic_config_manager_comprehensive.py` | 🔴 VULNERABLE | **13**/0/0/0 | 0 / 0 / 9 |
| `tests/core/config/implementations/test_yaml_config_manager.py` | ✅ SECURE | **65**/0/0/0 | 0 / 0 / 17 |
| `tests/core/config/interfaces/test_async_config_interface.py` | 🟡 WARNING | **25**/0/0/0 | 0 / 0 / 1 |
| `tests/core/config/interfaces/test_config_interface.py` | ✅ SECURE | **17**/0/0/0 | 0 / 0 / 1 |
| `tests/core/config/interfaces/test_factory_interface.py` | ✅ SECURE | **23**/0/0/0 | 0 / 0 / 11 |
| `tests/core/config/test_config_factory.py` | ✅ SECURE | **31**/0/0/0 | 0 / 0 / 1 |
| `tests/core/config/test_processors_config.py` | ✅ SECURE | **0**/26/0/0 | 0 / 0 / 44 |
| `tests/core/config/test_yaml_config_manager_validation.py` | ✅ SECURE | **11**/0/0/0 | 0 / 0 / 0 |
| `tests/core/db/exceptions/test_db_error.py` | ✅ SECURE | **9**/0/0/0 | 0 / 0 / 0 |
| `tests/core/db/exceptions/test_db_exceptions_init.py` | ✅ SECURE | **5**/0/0/0 | 0 / 0 / 0 |
| `tests/core/db/implementations/test_db_implementations_init.py` | ✅ SECURE | **8**/0/0/0 | 0 / 0 / 3 |
| `tests/core/db/implementations/test_model_base.py` | ✅ SECURE | **12**/0/0/0 | 0 / 0 / 2 |
| `tests/core/db/implementations/test_models.py` | ✅ SECURE | **22**/0/0/0 | 0 / 0 / 13 |
| `tests/core/db/implementations/test_sqlalchemy_session.py` | ✅ SECURE | **22**/0/0/3 | 0 / 0 / 0 |
| `tests/core/db/interfaces/test_db_interfaces_init.py` | ✅ SECURE | **4**/0/0/0 | 0 / 0 / 1 |
| `tests/core/db/test_db_factory.py` | ✅ SECURE | **21**/1/0/0 | 0 / 0 / 7 |
| `tests/core/db/test_db_init.py` | ✅ SECURE | **8**/0/0/0 | 0 / 0 / 0 |
| `tests/core/events/exceptions/test_event_error.py` | ✅ SECURE | **9**/0/0/0 | 0 / 0 / 0 |
| `tests/core/events/exceptions/test_events_exceptions_init.py` | ✅ SECURE | **5**/0/0/0 | 0 / 0 / 0 |
| `tests/core/events/implementations/test_events_implementations_init.py` | ✅ SECURE | **4**/0/0/0 | 0 / 0 / 0 |
| `tests/core/events/implementations/test_zeromq_bus.py` | ✅ SECURE | **24**/25/0/0 | 0 / 0 / 0 |
| `tests/core/events/interfaces/test_event_bus_interface.py` | ✅ SECURE | **27**/0/0/0 | 0 / 0 / 0 |
| `tests/core/events/interfaces/test_event_models.py` | ✅ SECURE | **26**/0/0/0 | 0 / 0 / 8 |
| `tests/core/events/interfaces/test_events_interfaces_init.py` | ✅ SECURE | **11**/0/0/0 | 0 / 0 / 0 |
| `tests/core/events/test_events_factory.py` | ✅ SECURE | **11**/1/0/0 | 0 / 0 / 0 |
| `tests/core/events/test_events_init.py` | ✅ SECURE | **10**/0/0/0 | 0 / 0 / 0 |
| `tests/core/logger/exceptions/test_logger_error.py` | ✅ SECURE | **14**/0/0/0 | 0 / 0 / 0 |
| `tests/core/logger/formatters/test_logger_formatters.py` | ✅ SECURE | **6**/0/0/0 | 0 / 0 / 0 |
| `tests/core/logger/implementations/test_colored_logger.py` | ✅ SECURE | **12**/0/0/0 | 0 / 0 / 0 |
| `tests/core/logger/implementations/test_default_logger.py` | ✅ SECURE | **9**/0/0/0 | 0 / 0 / 0 |
| `tests/core/logger/implementations/test_rotating_file_logger.py` | ✅ SECURE | **22**/0/0/0 | 0 / 0 / 0 |
| `tests/core/logger/interfaces/test_logger_factory_interface.py` | ✅ SECURE | **5**/0/0/0 | 0 / 0 / 2 |
| `tests/core/logger/interfaces/test_logger_interface.py` | ✅ SECURE | **3**/0/0/0 | 0 / 0 / 1 |
| `tests/core/logger/interfaces/test_logger_interfaces_init.py` | ✅ SECURE | **4**/0/0/0 | 0 / 0 / 0 |
| `tests/core/logger/test_logger_factory.py` | ✅ SECURE | **5**/0/0/0 | 0 / 0 / 0 |
| `tests/core/logger/test_logger_init.py` | ✅ SECURE | **14**/0/0/0 | 0 / 0 / 2 |
| `tests/core/system/implementations/test_health_monitor.py` | ✅ SECURE | **28**/0/0/0 | 0 / 0 / 1 |
| `tests/core/system/interfaces/test_health_interface.py` | ✅ SECURE | **22**/0/0/0 | 0 / 0 / 16 |
| `tests/core/system/test_system_factory.py` | ✅ SECURE | **19**/0/0/0 | 0 / 0 / 2 |
| `tests/core/test_core_init.py` | ✅ SECURE | **11**/8/0/0 | 0 / 0 / 26 |
| `tests/core/test_init_version_fallback.py` | ✅ SECURE | **4**/1/0/0 | 0 / 0 / 2 |
| `tests/core/test_pyproject_ui_dependencies.py` | ✅ SECURE | **6**/0/0/0 | 0 / 0 / 0 |
| `tests/core/utils/exceptions/test_util_errors.py` | ✅ SECURE | **12**/0/0/0 | 0 / 0 / 0 |
| `tests/core/utils/interfaces/test_hardware_interface.py` | ✅ SECURE | **3**/0/0/0 | 0 / 0 / 0 |
| `tests/core/utils/test_decorators.py` | ✅ SECURE | **2**/11/0/0 | 0 / 0 / 0 |
| `tests/core/utils/test_hardware_info.py` | ✅ SECURE | **15**/0/0/0 | 0 / 0 / 0 |
| `tests/core/utils/test_utils_factory.py` | ✅ SECURE | **11**/0/0/0 | 0 / 0 / 0 |
| `tests/data/ingestion/test_market_data_persister.py` | ✅ SECURE | **20**/0/0/5 | 0 / 0 / 0 |
| `tests/data/storage/backends/test_base.py` | ✅ SECURE | **2**/6/0/0 | 0 / 0 / 76 |
| `tests/data/storage/backends/test_pandas_backend.py` | ✅ SECURE | **30**/0/0/0 | 0 / 0 / 22 |
| `tests/data/storage/backends/test_polars_backend.py` | ✅ SECURE | **13**/13/0/4 | 0 / 0 / 13 |
| `tests/data/storage/implementations/test_file_storage.py` | ✅ SECURE | **46**/4/0/2 | 0 / 0 / 30 |
| `tests/data/storage/implementations/test_parquet_storage.py` | ✅ SECURE | **33**/1/0/0 | 0 / 0 / 2 |
| `tests/data/storage/interfaces/test_storage_factory_interface.py` | ✅ SECURE | **6**/0/0/0 | 0 / 0 / 0 |
| `tests/data/storage/interfaces/test_storage_interface.py` | ✅ SECURE | **11**/0/0/0 | 0 / 0 / 0 |
| `tests/data/storage/test_storage_factory.py` | ✅ SECURE | **12**/0/0/0 | 0 / 0 / 8 |
| `tests/data/storage/test_storage_init.py` | ✅ SECURE | **5**/0/0/0 | 0 / 0 / 0 |
| `tests/processors/dimensions/d02_support/test_processor.py` | ✅ SECURE | **3**/1/0/0 | 0 / 0 / 28 |
| `tests/processors/test_factory.py` | ✅ SECURE | **3**/0/0/0 | 0 / 0 / 14 |
| `tests/processors/test_time_alignment_service.py` | ✅ SECURE | **1**/7/0/0 | 0 / 0 / 2 |
| `tests/scripts/test_data_reset.py` | ✅ SECURE | **12**/2/0/0 | 0 / 0 / 0 |
| `tests/scripts/test_download_history.py` | ✅ SECURE | **9**/2/0/0 | 0 / 0 / 1 |
| `tests/scripts/test_migrate_structure.py` | ✅ SECURE | **12**/1/0/0 | 0 / 0 / 10 |
| `tests/scripts/test_test_tick_pipeline.py` | ✅ SECURE | **4**/1/0/0 | 0 / 0 / 8 |
| `tests/scripts/test_validation_end_to_end.py` | ✅ SECURE | **2**/1/0/0 | 0 / 0 / 0 |
| `tests/test_dashboard_command.py` | ✅ SECURE | **6**/7/0/0 | 0 / 0 / 5 |
| `tests/test_main.py` | ✅ SECURE | **5**/6/0/0 | 0 / 0 / 10 |
| `tests/test_neural_ai_init.py` | ✅ SECURE | **4**/1/0/0 | 0 / 0 / 2 |
| `tests/ui/interfaces/test_data_service_interface.py` | ✅ SECURE | **19**/0/0/0 | 0 / 0 / 0 |
| `tests/ui/pages/test_data_hub_page.py` | ✅ SECURE | **11**/0/0/0 | 0 / 0 / 0 |
| `tests/ui/pages/test_launchpad_page.py` | ✅ SECURE | **10**/0/0/0 | 0 / 0 / 0 |
| `tests/ui/pages/test_strategy_lab_page.py` | ✅ SECURE | **26**/0/0/0 | 0 / 0 / 0 |
| `tests/ui/services/test_dashboard_service.py` | ✅ SECURE | **13**/0/0/0 | 0 / 0 / 0 |
| `tests/ui/services/test_data_service.py` | ✅ SECURE | **26**/0/0/0 | 0 / 0 / 0 |
| `tests/ui/services/test_strategy_service.py` | ✅ SECURE | **24**/0/0/0 | 0 / 0 / 18 |
| `tests/ui/test_app.py` | ✅ SECURE | **15**/0/0/0 | 0 / 0 / 0 |
| `tests/ui/test_core_bridge.py` | ✅ SECURE | **21**/0/0/0 | 0 / 0 / 0 |
| `tests/ui/test_ui_factory.py` | ✅ SECURE | **28**/0/0/0 | 0 / 0 / 0 |
