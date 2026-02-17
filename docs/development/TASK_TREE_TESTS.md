# 🧪 NEURAL AI NEXT - TESTS

**Generálva:** 2026-02-17 20:26:42 UTC
**Módszer:** Hibrid (AST + Pytest + Coverage + Ruff + Mypy + Pylance)
**Fájlok száma:** 107

## 📊 Statisztika

- ✅ **SECURE:** 53 (49.5%)
- 🟡 **WARNING:** 32 (29.9%)
- 🔴 **VULNERABLE:** 22 (20.6%)

---

## 6. Tests Layer (`tests/`)

| Fájl | Státusz | Pass/Fail/Err/Skip | Lint/Mypy/Pylance | Src Warn | Teendők |
|:-----|:--------|:-------------------|:------------------|:---------|:--------|
| `tests/neural_ai/collectors/__init__.py` | ✅ SECURE | - | 0 / 0 / 0 | - | - |
| `tests/neural_ai/collectors/jforex/__init__.py` | ✅ SECURE | - | 0 / 0 / 0 | - | - |
| `tests/neural_ai/collectors/jforex/exceptions/__init__.py` | ✅ SECURE | - | 0 / 0 / 0 | - | - |
| `tests/neural_ai/collectors/jforex/exceptions/test_exceptions_init.py` | ✅ SECURE | **5**/0/0/0 | 0 / 0 / 0 | - | - |
| `tests/neural_ai/collectors/jforex/implementations/__init__.py` | ✅ SECURE | - | 0 / 0 / 0 | - | - |
| `tests/neural_ai/collectors/jforex/interfaces/__init__.py` | ✅ SECURE | - | 0 / 0 / 0 | - | - |
| `tests/neural_ai/collectors/jforex/interfaces/test_interfaces_init.py` | ✅ SECURE | **3**/0/0/0 | 0 / 0 / 0 | - | - |
| `tests/neural_ai/collectors/jforex/mocks/__init__.py` | ✅ SECURE | - | 0 / 0 / 0 | - | - |
| `tests/neural_ai/collectors/jforex/test_bi5_downloader.py` | 🟡 WARNING | **43**/0/0/0 | 0 / 0 / 286 | - | 🔎 Pylance: 286 hiba javítása |
| `tests/neural_ai/collectors/jforex/test_factory.py` | ✅ SECURE | **10**/0/0/0 | 0 / 0 / 0 | - | - |
| `tests/neural_ai/collectors/jforex/test_jforex_init.py` | ✅ SECURE | **2**/0/0/0 | 0 / 0 / 0 | - | - |
| `tests/neural_ai/collectors/jforex/test_live_feed.py` | 🟡 WARNING | **12**/0/0/0 | 0 / 0 / 25 | - | 🔎 Pylance: 25 hiba javítása |
| `tests/neural_ai/collectors/jforex/test_live_feed_integration.py` | 🟡 WARNING | **8**/0/0/0 | 0 / 0 / 17 | - | 🔎 Pylance: 17 hiba javítása |
| `tests/neural_ai/core/base/exceptions/test_base_error.py` | ✅ SECURE | **42**/0/0/0 | 0 / 0 / 0 | - | - |
| `tests/neural_ai/core/base/exceptions/test_exceptions_init.py` | ✅ SECURE | **18**/0/0/0 | 0 / 0 / 0 | - | - |
| `tests/neural_ai/core/base/implementations/test_component_bundle.py` | ✅ SECURE | **39**/0/0/0 | 0 / 0 / 0 | - | - |
| `tests/neural_ai/core/base/implementations/test_di_container.py` | 🟡 WARNING | **24**/0/0/0 | 0 / 0 / 20 | - | 🔎 Pylance: 20 hiba javítása |
| `tests/neural_ai/core/base/implementations/test_implementations_init.py` | ✅ SECURE | **13**/0/0/0 | 0 / 0 / 0 | - | - |
| `tests/neural_ai/core/base/implementations/test_lazy_loader.py` | ✅ SECURE | **10**/0/0/0 | 0 / 0 / 0 | - | - |
| `tests/neural_ai/core/base/implementations/test_singleton.py` | ✅ SECURE | **10**/0/0/0 | 0 / 0 / 0 | - | - |
| `tests/neural_ai/core/base/interfaces/test_component_interface.py` | 🟡 WARNING | **13**/0/0/0 | 0 / 0 / 3 | - | 🔎 Pylance: 3 hiba javítása |
| `tests/neural_ai/core/base/interfaces/test_container_interface.py` | 🟡 WARNING | **20**/0/0/0 | 0 / 0 / 6 | - | 🔎 Pylance: 6 hiba javítása |
| `tests/neural_ai/core/base/interfaces/test_interfaces_init.py` | 🟡 WARNING | **12**/0/0/0 | 0 / 0 / 4 | - | 🔎 Pylance: 4 hiba javítása |
| `tests/neural_ai/core/base/test_base_init.py` | ✅ SECURE | **8**/0/0/0 | 0 / 0 / 0 | - | - |
| `tests/neural_ai/core/base/test_factory.py` | 🟡 WARNING | **35**/0/0/0 | 0 / 0 / 37 | - | 🔎 Pylance: 37 hiba javítása |
| `tests/neural_ai/core/config/exceptions/test_config_error.py` | ✅ SECURE | **15**/0/0/0 | 0 / 0 / 0 | - | - |
| `tests/neural_ai/core/config/implementations/test_config_implementations_init.py` | ✅ SECURE | **4**/0/0/0 | 0 / 0 / 0 | - | - |
| `tests/neural_ai/core/config/implementations/test_dynamic_config_manager.py` | 🟡 WARNING | **48**/0/0/0 | 0 / 0 / 54 | - | 🔎 Pylance: 54 hiba javítása |
| `tests/neural_ai/core/config/implementations/test_dynamic_config_manager_comprehensive.py` | 🟡 WARNING | **13**/0/0/0 | 0 / 0 / 9 | - | 🔎 Pylance: 9 hiba javítása |
| `tests/neural_ai/core/config/implementations/test_yaml_config_manager.py` | 🟡 WARNING | **65**/0/0/0 | 0 / 0 / 17 | - | 🔎 Pylance: 17 hiba javítása |
| `tests/neural_ai/core/config/interfaces/test_async_config_interface.py` | 🟡 WARNING | **25**/0/0/0 | 0 / 0 / 1 | - | 🔎 Pylance: 1 hiba javítása |
| `tests/neural_ai/core/config/interfaces/test_config_interface.py` | 🟡 WARNING | **17**/0/0/0 | 0 / 0 / 1 | - | 🔎 Pylance: 1 hiba javítása |
| `tests/neural_ai/core/config/interfaces/test_factory_interface.py` | 🟡 WARNING | **23**/0/0/0 | 0 / 0 / 11 | - | 🔎 Pylance: 11 hiba javítása |
| `tests/neural_ai/core/config/test_config_factory.py` | 🔴 VULNERABLE | **21**/10/0/0 | 0 / 0 / 1 | - | 🔴 **Tesztek javítása: 10 failed, 0 error** | 🔎 Pylance: 1 hiba javítása |
| `tests/neural_ai/core/config/test_processors_config.py` | 🔴 VULNERABLE | **0**/26/0/0 | 0 / 0 / 44 | - | 🔴 **Tesztek javítása: 26 failed, 0 error** | 🔎 Pylance: 44 hiba javítása |
| `tests/neural_ai/core/config/test_yaml_config_manager_validation.py` | ✅ SECURE | **11**/0/0/0 | 0 / 0 / 0 | - | - |
| `tests/neural_ai/core/db/exceptions/test_db_error.py` | ✅ SECURE | **9**/0/0/0 | 0 / 0 / 0 | - | - |
| `tests/neural_ai/core/db/exceptions/test_db_exceptions_init.py` | ✅ SECURE | **5**/0/0/0 | 0 / 0 / 0 | - | - |
| `tests/neural_ai/core/db/implementations/test_db_implementations_init.py` | 🟡 WARNING | **8**/0/0/0 | 0 / 0 / 3 | - | 🔎 Pylance: 3 hiba javítása |
| `tests/neural_ai/core/db/implementations/test_model_base.py` | 🟡 WARNING | **12**/0/0/0 | 0 / 0 / 2 | - | 🔎 Pylance: 2 hiba javítása |
| `tests/neural_ai/core/db/implementations/test_models.py` | 🟡 WARNING | **22**/0/0/0 | 0 / 0 / 13 | - | 🔎 Pylance: 13 hiba javítása |
| `tests/neural_ai/core/db/implementations/test_sqlalchemy_session.py` | 🟡 WARNING | **22**/0/0/3 | 0 / 0 / 0 | - | ⏭️ 3 skipped teszt aktiválása |
| `tests/neural_ai/core/db/interfaces/test_db_interfaces_init.py` | 🟡 WARNING | **4**/0/0/0 | 0 / 0 / 1 | - | 🔎 Pylance: 1 hiba javítása |
| `tests/neural_ai/core/db/test_db_factory.py` | 🔴 VULNERABLE | **21**/1/0/0 | 0 / 1 / 7 | - | 🔴 **Tesztek javítása: 1 failed, 0 error** | 🔬 Mypy: 1 type hiba javítása | 🔎 Pylance: 7 hiba javítása |
| `tests/neural_ai/core/db/test_db_init.py` | ✅ SECURE | **8**/0/0/0 | 0 / 0 / 0 | - | - |
| `tests/neural_ai/core/events/exceptions/test_event_error.py` | ✅ SECURE | **9**/0/0/0 | 0 / 0 / 0 | - | - |
| `tests/neural_ai/core/events/exceptions/test_events_exceptions_init.py` | ✅ SECURE | **5**/0/0/0 | 0 / 0 / 0 | - | - |
| `tests/neural_ai/core/events/implementations/test_events_implementations_init.py` | ✅ SECURE | **4**/0/0/0 | 0 / 0 / 0 | - | - |
| `tests/neural_ai/core/events/implementations/test_zeromq_bus.py` | 🔴 VULNERABLE | **24**/25/0/0 | 0 / 0 / 0 | - | 🔴 **Tesztek javítása: 25 failed, 0 error** |
| `tests/neural_ai/core/events/interfaces/test_event_bus_interface.py` | ✅ SECURE | **27**/0/0/0 | 0 / 0 / 0 | - | - |
| `tests/neural_ai/core/events/interfaces/test_event_models.py` | 🟡 WARNING | **26**/0/0/0 | 0 / 0 / 8 | - | 🔎 Pylance: 8 hiba javítása |
| `tests/neural_ai/core/events/interfaces/test_events_interfaces_init.py` | ✅ SECURE | **11**/0/0/0 | 0 / 0 / 0 | - | - |
| `tests/neural_ai/core/events/test_events_factory.py` | 🔴 VULNERABLE | **11**/1/0/0 | 0 / 0 / 0 | - | 🔴 **Tesztek javítása: 1 failed, 0 error** |
| `tests/neural_ai/core/events/test_events_init.py` | ✅ SECURE | **10**/0/0/0 | 0 / 0 / 0 | - | - |
| `tests/neural_ai/core/logger/exceptions/test_logger_error.py` | ✅ SECURE | **14**/0/0/0 | 0 / 0 / 0 | - | - |
| `tests/neural_ai/core/logger/formatters/test_logger_formatters.py` | ✅ SECURE | **6**/0/0/0 | 0 / 0 / 0 | - | - |
| `tests/neural_ai/core/logger/implementations/test_colored_logger.py` | ✅ SECURE | **12**/0/0/0 | 0 / 0 / 0 | - | - |
| `tests/neural_ai/core/logger/implementations/test_default_logger.py` | ✅ SECURE | **9**/0/0/0 | 0 / 0 / 0 | - | - |
| `tests/neural_ai/core/logger/implementations/test_rotating_file_logger.py` | ✅ SECURE | **22**/0/0/0 | 0 / 0 / 0 | - | - |
| `tests/neural_ai/core/logger/interfaces/test_logger_factory_interface.py` | 🟡 WARNING | **5**/0/0/0 | 0 / 0 / 2 | - | 🔎 Pylance: 2 hiba javítása |
| `tests/neural_ai/core/logger/interfaces/test_logger_interface.py` | 🟡 WARNING | **3**/0/0/0 | 0 / 0 / 1 | - | 🔎 Pylance: 1 hiba javítása |
| `tests/neural_ai/core/logger/interfaces/test_logger_interfaces_init.py` | ✅ SECURE | **4**/0/0/0 | 0 / 0 / 0 | - | - |
| `tests/neural_ai/core/logger/test_logger_factory.py` | ✅ SECURE | **5**/0/0/0 | 0 / 0 / 0 | - | - |
| `tests/neural_ai/core/logger/test_logger_init.py` | 🟡 WARNING | **14**/0/0/0 | 0 / 0 / 2 | - | 🔎 Pylance: 2 hiba javítása |
| `tests/neural_ai/core/system/implementations/test_health_monitor.py` | 🟡 WARNING | **28**/0/0/0 | 0 / 0 / 1 | - | 🔎 Pylance: 1 hiba javítása |
| `tests/neural_ai/core/system/interfaces/test_health_interface.py` | 🟡 WARNING | **22**/0/0/0 | 0 / 0 / 16 | - | 🔎 Pylance: 16 hiba javítása |
| `tests/neural_ai/core/system/test_system_factory.py` | 🟡 WARNING | **19**/0/0/0 | 0 / 0 / 2 | - | 🔎 Pylance: 2 hiba javítása |
| `tests/neural_ai/core/test_core_init.py` | 🔴 VULNERABLE | **11**/8/0/0 | 0 / 0 / 26 | - | 🔴 **Tesztek javítása: 8 failed, 0 error** | 🔎 Pylance: 26 hiba javítása |
| `tests/neural_ai/core/test_init_version_fallback.py` | 🔴 VULNERABLE | **4**/1/0/0 | 0 / 0 / 2 | - | 🔴 **Tesztek javítása: 1 failed, 0 error** | 🔎 Pylance: 2 hiba javítása |
| `tests/neural_ai/core/test_pyproject_ui_dependencies.py` | 🔴 VULNERABLE | **0**/6/0/0 | 0 / 0 / 0 | - | 🔴 **Tesztek javítása: 6 failed, 0 error** |
| `tests/neural_ai/core/utils/exceptions/test_util_errors.py` | ✅ SECURE | **12**/0/0/0 | 0 / 0 / 0 | - | - |
| `tests/neural_ai/core/utils/interfaces/test_hardware_interface.py` | ✅ SECURE | **3**/0/0/0 | 0 / 0 / 0 | - | - |
| `tests/neural_ai/core/utils/test_decorators.py` | 🔴 VULNERABLE | **2**/11/0/0 | 0 / 0 / 0 | - | 🔴 **Tesztek javítása: 11 failed, 0 error** |
| `tests/neural_ai/core/utils/test_hardware_info.py` | ✅ SECURE | **15**/0/0/0 | 0 / 0 / 0 | - | - |
| `tests/neural_ai/core/utils/test_utils_factory.py` | ✅ SECURE | **11**/0/0/0 | 0 / 0 / 0 | - | - |
| `tests/neural_ai/data/ingestion/test_market_data_persister.py` | 🟡 WARNING | **20**/0/0/5 | 0 / 0 / 0 | - | ⏭️ 5 skipped teszt aktiválása |
| `tests/neural_ai/data/storage/backends/test_base.py` | 🔴 VULNERABLE | **2**/6/0/0 | 0 / 0 / 76 | - | 🔴 **Tesztek javítása: 6 failed, 0 error** | 🔎 Pylance: 76 hiba javítása |
| `tests/neural_ai/data/storage/backends/test_pandas_backend.py` | 🟡 WARNING | **30**/0/0/0 | 0 / 0 / 22 | - | 🔎 Pylance: 22 hiba javítása |
| `tests/neural_ai/data/storage/backends/test_polars_backend.py` | 🔴 VULNERABLE | **13**/13/0/4 | 0 / 0 / 13 | - | 🔴 **Tesztek javítása: 13 failed, 0 error** | 🔎 Pylance: 13 hiba javítása | ⏭️ 4 skipped teszt aktiválása |
| `tests/neural_ai/data/storage/implementations/test_file_storage.py` | 🔴 VULNERABLE | **46**/4/0/2 | 0 / 0 / 30 | - | 🔴 **Tesztek javítása: 4 failed, 0 error** | 🔎 Pylance: 30 hiba javítása | ⏭️ 2 skipped teszt aktiválása |
| `tests/neural_ai/data/storage/implementations/test_parquet_storage.py` | 🔴 VULNERABLE | **33**/1/0/0 | 0 / 0 / 2 | - | 🔴 **Tesztek javítása: 1 failed, 0 error** | 🔎 Pylance: 2 hiba javítása |
| `tests/neural_ai/data/storage/interfaces/test_storage_factory_interface.py` | ✅ SECURE | **6**/0/0/0 | 0 / 0 / 0 | - | - |
| `tests/neural_ai/data/storage/interfaces/test_storage_interface.py` | ✅ SECURE | **11**/0/0/0 | 0 / 0 / 0 | - | - |
| `tests/neural_ai/data/storage/test_storage_factory.py` | 🟡 WARNING | **12**/0/0/0 | 0 / 0 / 8 | - | 🔎 Pylance: 8 hiba javítása |
| `tests/neural_ai/data/storage/test_storage_init.py` | ✅ SECURE | **5**/0/0/0 | 0 / 0 / 0 | - | - |
| `tests/neural_ai/processors/__init__.py` | ✅ SECURE | - | 0 / 0 / 0 | - | - |
| `tests/neural_ai/processors/dimensions/d02_support/test_processor.py` | 🔴 VULNERABLE | **3**/1/0/0 | 0 / 0 / 28 | - | 🔴 **Tesztek javítása: 1 failed, 0 error** | 🔎 Pylance: 28 hiba javítása |
| `tests/neural_ai/processors/test_factory.py` | 🟡 WARNING | **3**/0/0/0 | 0 / 0 / 14 | - | 🔎 Pylance: 14 hiba javítása |
| `tests/neural_ai/processors/test_time_alignment_service.py` | 🔴 VULNERABLE | **1**/7/0/0 | 0 / 0 / 2 | - | 🔴 **Tesztek javítása: 7 failed, 0 error** | 🔎 Pylance: 2 hiba javítása |
| `tests/neural_ai/ui/interfaces/test_data_service_interface.py` | ✅ SECURE | **19**/0/0/0 | 0 / 0 / 0 | - | - |
| `tests/neural_ai/ui/pages/test_data_hub_page.py` | ✅ SECURE | **11**/0/0/0 | 0 / 0 / 0 | - | - |
| `tests/neural_ai/ui/pages/test_launchpad_page.py` | ✅ SECURE | **10**/0/0/0 | 0 / 0 / 0 | - | - |
| `tests/neural_ai/ui/pages/test_strategy_lab_page.py` | ✅ SECURE | **26**/0/0/0 | 0 / 0 / 0 | - | - |
| `tests/neural_ai/ui/services/test_dashboard_service.py` | ✅ SECURE | **13**/0/0/0 | 0 / 0 / 0 | - | - |
| `tests/neural_ai/ui/services/test_data_service.py` | ✅ SECURE | **26**/0/0/0 | 0 / 0 / 0 | - | - |
| `tests/neural_ai/ui/services/test_strategy_service.py` | 🟡 WARNING | **24**/0/0/0 | 0 / 0 / 18 | - | 🔎 Pylance: 18 hiba javítása |
| `tests/neural_ai/ui/test_app.py` | ✅ SECURE | **15**/0/0/0 | 0 / 0 / 0 | - | - |
| `tests/neural_ai/ui/test_core_bridge.py` | ✅ SECURE | **21**/0/0/0 | 0 / 0 / 0 | - | - |
| `tests/neural_ai/ui/test_ui_factory.py` | ✅ SECURE | **28**/0/0/0 | 0 / 0 / 0 | - | - |
| `tests/scripts/test_data_reset.py` | 🔴 VULNERABLE | **12**/2/0/0 | 0 / 0 / 0 | - | 🔴 **Tesztek javítása: 2 failed, 0 error** |
| `tests/scripts/test_download_history.py` | 🔴 VULNERABLE | **9**/2/0/0 | 0 / 0 / 1 | - | 🔴 **Tesztek javítása: 2 failed, 0 error** | 🔎 Pylance: 1 hiba javítása |
| `tests/scripts/test_migrate_structure.py` | 🔴 VULNERABLE | **12**/1/0/0 | 0 / 0 / 10 | - | 🔴 **Tesztek javítása: 1 failed, 0 error** | 🔎 Pylance: 10 hiba javítása |
| `tests/scripts/test_test_tick_pipeline.py` | 🟡 WARNING | - | 0 / 0 / 8 | - | 🔎 Pylance: 8 hiba javítása |
| `tests/scripts/test_validation_end_to_end.py` | 🔴 VULNERABLE | **2**/1/0/0 | 0 / 0 / 0 | - | 🔴 **Tesztek javítása: 1 failed, 0 error** |
| `tests/test_dashboard_command.py` | 🔴 VULNERABLE | **6**/7/0/0 | 0 / 0 / 5 | - | 🔴 **Tesztek javítása: 7 failed, 0 error** | 🔎 Pylance: 5 hiba javítása |
| `tests/test_main.py` | 🔴 VULNERABLE | **5**/6/0/0 | 0 / 0 / 10 | - | 🔴 **Tesztek javítása: 6 failed, 0 error** | 🔎 Pylance: 10 hiba javítása |
| `tests/test_neural_ai_init.py` | 🔴 VULNERABLE | **4**/1/0/0 | 0 / 0 / 2 | - | 🔴 **Tesztek javítása: 1 failed, 0 error** | 🔎 Pylance: 2 hiba javítása |
