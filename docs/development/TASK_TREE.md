# 🌳 NEURAL AI NEXT - TASK TREE

**Generálva:** 2026-02-16 19:15:34 UTC
**Módszer:** Hibrid (AST + Pytest + Coverage + Ruff + Mypy + Pylance)
**Fájlok száma:** 214

## 📊 Statisztika

- ✅ **SECURE:** 137 (64.0%)
- 🟡 **WARNING:** 17 (7.9%)
- 🔴 **VULNERABLE:** 60 (28.0%)

---

## 1. Infrastructure Layer (`neural_ai/core/`)

| Modul / Fájl | Státusz | Teszt Pár | Pass/Fail/Err/Warn | Coverage (Stmt/Brch) | Lint/Mypy/Pylance | Config | Logger | Teendők |
|:-------------|:--------|:----------|:-------------------|:---------------------|:------------------|:-------|:-------|:--------|
| `core/base/exceptions/base_error.py` | ✅ SECURE | ✅ FOUND | **42**/0/0/0 | 100% / 100% | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/base/factory.py` | ✅ SECURE | ✅ FOUND | **35**/0/0/0 | 23% / 0% | 0 / 0 / 0 | ✅ OK | ⚪ N/A | - |
| `core/base/implementations/component_bundle.py` | ✅ SECURE | ✅ FOUND | **39**/0/0/0 | 39% / 100% | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/base/implementations/di_container.py` | ✅ SECURE | ✅ FOUND | **24**/0/0/0 | 28% / 0% | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/base/implementations/lazy_loader.py` | ✅ SECURE | ✅ FOUND | **10**/0/0/0 | 43% / 0% | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/base/implementations/singleton.py` | ✅ SECURE | ✅ FOUND | **10**/0/0/0 | 43% / 0% | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/base/interfaces/component_interface.py` | ✅ SECURE | ✅ FOUND | **13**/0/0/0 | 76% / 100% | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/base/interfaces/container_interface.py` | ✅ SECURE | ✅ FOUND | **20**/0/0/0 | 75% / 100% | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/config/exceptions/config_error.py` | ✅ SECURE | ✅ FOUND | **15**/0/0/0 | 40% / 100% | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/config/factory.py` | ✅ SECURE | ✅ FOUND | **31**/0/0/0 | 26% / 0% | 0 / 0 / 4 | ⚪ N/A | ⚪ N/A | - |
| `core/config/implementations/dynamic_config_manager.py` | 🟡 WARNING | ✅ FOUND | **48**/0/0/0 | 10% / 0% | 0 / 0 / 0 | ⚪ N/A | ⚠️ UNUSED | - |
| `core/config/implementations/yaml_config_manager.py` | 🟡 WARNING | ✅ FOUND | **65**/0/0/0 | 13% / 0% | 0 / 0 / 22 | ⚪ N/A | ⚠️ UNUSED | - |
| `core/config/interfaces/async_config_interface.py` | 🟡 WARNING | ✅ FOUND | **25**/0/0/0 | 100% / 100% | 0 / 0 / 0 | ⚪ N/A | ⚠️ UNUSED | - |
| `core/config/interfaces/config_interface.py` | ✅ SECURE | ✅ FOUND | **17**/0/0/0 | 100% / 100% | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/config/interfaces/factory_interface.py` | ✅ SECURE | ✅ FOUND | **23**/0/0/0 | 80% / 100% | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/config/interfaces/types.py` | 🔴 VULNERABLE | ❌ MISSING | - | 84% / 0% | 0 / 0 / 0 | ✅ OK | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `core/db/exceptions/db_error.py` | ✅ SECURE | ✅ FOUND | **9**/0/0/0 | 54% / 100% | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/db/factory.py` | 🟡 WARNING | ✅ FOUND | **21**/1/0/0 | 62% / 100% | 0 / 0 / 0 | ⚪ N/A | ⚠️ UNUSED | - |
| `core/db/implementations/model_base.py` | ✅ SECURE | ✅ FOUND | **12**/0/0/0 | 52% / 0% | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/db/implementations/models.py` | ✅ SECURE | ✅ FOUND | **22**/0/0/0 | 92% / 100% | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/db/implementations/sqlalchemy_session.py` | ✅ SECURE | ✅ FOUND | **22**/0/0/0 | 17% / 0% | 0 / 0 / 10 | ⚪ N/A | ✅ OK | - |
| `core/events/exceptions/event_error.py` | ✅ SECURE | ✅ FOUND | **9**/0/0/0 | 54% / 100% | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/events/factory.py` | 🟡 WARNING | ✅ FOUND | **11**/1/0/0 | 28% / 100% | 0 / 0 / 0 | ⚪ N/A | ⚠️ UNUSED | - |
| `core/events/implementations/zeromq_bus.py` | 🟡 WARNING | ✅ FOUND | **24**/25/0/0 | 14% / 0% | 0 / 1 / 20 | ✅ OK | ⚠️ UNUSED | - |
| `core/events/interfaces/event_bus_interface.py` | ✅ SECURE | ✅ FOUND | **27**/0/0/0 | 100% / 100% | 0 / 0 / 0 | ✅ OK | ⚪ N/A | - |
| `core/events/interfaces/event_models.py` | ✅ SECURE | ✅ FOUND | **26**/0/0/0 | 64% / 0% | 0 / 0 / 0 | ✅ OK | ⚪ N/A | - |
| `core/logger/exceptions/logger_error.py` | ✅ SECURE | ✅ FOUND | **14**/0/0/0 | 100% / 100% | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/logger/factory.py` | ✅ SECURE | ✅ FOUND | **5**/0/0/0 | 30% / 11% | 0 / 2 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/logger/formatters/logger_formatters.py` | ✅ SECURE | ✅ FOUND | **6**/0/0/0 | 45% / 0% | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/logger/implementations/colored_logger.py` | 🔴 VULNERABLE | ✅ FOUND | **12**/0/0/0 | 32% / 0% | 0 / 0 / 0 | ⚪ N/A | 🔴 MISSING | **Logger DI hiányzik!** |
| `core/logger/implementations/default_logger.py` | 🔴 VULNERABLE | ✅ FOUND | **9**/0/0/0 | 70% / 100% | 0 / 0 / 0 | ⚪ N/A | 🔴 MISSING | **Logger DI hiányzik!** |
| `core/logger/implementations/rotating_file_logger.py` | 🔴 VULNERABLE | ✅ FOUND | **22**/0/0/0 | 22% / 0% | 0 / 0 / 0 | ⚪ N/A | 🔴 MISSING | **Logger DI hiányzik!** |
| `core/logger/interfaces/factory_interface.py` | 🔴 VULNERABLE | ❌ MISSING | - | 81% / 100% | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `core/logger/interfaces/logger_interface.py` | ✅ SECURE | ✅ FOUND | **3**/0/0/0 | 70% / 100% | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/system/exceptions/health_error.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `core/system/factory.py` | ✅ SECURE | ✅ FOUND | **19**/0/0/0 | 35% / 0% | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/system/implementations/health_monitor.py` | 🟡 WARNING | ✅ FOUND | **28**/0/0/0 | 11% / 0% | 0 / 1 / 0 | ⚪ N/A | ⚠️ UNUSED | - |
| `core/system/interfaces/health_interface.py` | ✅ SECURE | ✅ FOUND | **22**/0/0/0 | 100% / 100% | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/utils/decorators.py` | ✅ SECURE | ✅ FOUND | **2**/11/0/0 | 39% / 0% | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/utils/exceptions/util_error.py` | 🔴 VULNERABLE | ❌ MISSING | - | 56% / 100% | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `core/utils/factory.py` | ✅ SECURE | ✅ FOUND | **11**/0/0/0 | 60% / 100% | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/utils/implementations/hardware_info.py` | ✅ SECURE | ✅ FOUND | **15**/0/0/0 | 19% / 0% | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/utils/interfaces/hardware_interface.py` | ✅ SECURE | ✅ FOUND | **3**/0/0/0 | 100% / 100% | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |

## 2. Input Layer (`neural_ai/collectors/`)

| Modul / Fájl | Státusz | Teszt Pár | Pass/Fail/Err/Warn | Coverage (Stmt/Brch) | Lint/Mypy/Pylance | Config | Logger | Teendők |
|:-------------|:--------|:----------|:-------------------|:---------------------|:------------------|:-------|:-------|:--------|
| `collectors/jforex/exceptions/jforex_error.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `collectors/jforex/factory.py` | ✅ SECURE | ✅ FOUND | **10**/0/0/0 | 19% / 0% | 0 / 12 / 2 | ⚪ N/A | ⚪ N/A | - |
| `collectors/jforex/implementations/bi5_downloader.py` | 🟡 WARNING | ✅ FOUND | **43**/0/0/0 | 8% / 0% | 0 / 0 / 2 | ⚪ N/A | ⚠️ UNUSED | - |
| `collectors/jforex/implementations/live_feed.py` | ✅ SECURE | ✅ FOUND | **12**/0/0/0 | 13% / 0% | 0 / 0 / 3 | ⚪ N/A | ✅ OK | - |
| `collectors/jforex/interfaces/downloader_interface.py` | 🔴 VULNERABLE | ❌ MISSING | - | 75% / 100% | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `collectors/jforex/interfaces/live_interface.py` | 🔴 VULNERABLE | ❌ MISSING | - | 73% / 100% | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `collectors/jforex/interfaces/tick_data.py` | 🔴 VULNERABLE | ❌ MISSING | - | 88% / 100% | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |

## 3. Persistence Layer (`neural_ai/data/`)

| Modul / Fájl | Státusz | Teszt Pár | Pass/Fail/Err/Warn | Coverage (Stmt/Brch) | Lint/Mypy/Pylance | Config | Logger | Teendők |
|:-------------|:--------|:----------|:-------------------|:---------------------|:------------------|:-------|:-------|:--------|
| `data/ingestion/market_data_persister.py` | ✅ SECURE | ✅ FOUND | **20**/0/0/0 | 7% / 0% | 0 / 6 / 10 | ⚪ N/A | ✅ OK | - |
| `data/storage/backends/base.py` | 🟡 WARNING | ✅ FOUND | **2**/6/0/0 | 32% / 6% | 0 / 0 / 0 | ⚪ N/A | ⚠️ UNUSED | - |
| `data/storage/backends/pandas_backend.py` | 🟡 WARNING | ✅ FOUND | **30**/0/0/0 | 19% / 3% | 0 / 0 / 0 | ⚪ N/A | ⚠️ UNUSED | - |
| `data/storage/backends/polars_backend.py` | 🟡 WARNING | ✅ FOUND | **13**/13/0/0 | 16% / 2% | 0 / 0 / 0 | ⚪ N/A | ⚠️ UNUSED | - |
| `data/storage/factory.py` | ✅ SECURE | ✅ FOUND | **12**/0/0/0 | 28% / 0% | 0 / 0 / 5 | ⚪ N/A | ⚪ N/A | - |
| `data/storage/implementations/file_storage.py` | ✅ SECURE | ✅ FOUND | **46**/4/0/0 | 11% / 0% | 0 / 5 / 6 | ⚪ N/A | ✅ OK | - |
| `data/storage/implementations/parquet_storage.py` | ✅ SECURE | ✅ FOUND | **33**/1/0/0 | 12% / 0% | 0 / 1 / 21 | ✅ OK | ✅ OK | - |
| `data/storage/interfaces/factory_interface.py` | 🔴 VULNERABLE | ❌ MISSING | - | 83% / 100% | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `data/storage/interfaces/storage_interface.py` | ✅ SECURE | ✅ FOUND | **11**/0/0/0 | 100% / 100% | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |

## 4. Domain Layer (`neural_ai/processors/`)

| Modul / Fájl | Státusz | Teszt Pár | Pass/Fail/Err/Warn | Coverage (Stmt/Brch) | Lint/Mypy/Pylance | Config | Logger | Teendők |
|:-------------|:--------|:----------|:-------------------|:---------------------|:------------------|:-------|:-------|:--------|
| `processors/dimensions/base.py` | 🔴 VULNERABLE | ❌ MISSING | - | 47% / 0% | 0 / 0 / 0 | ⚪ N/A | ✅ OK | **KRITIKUS: Teszt írás!** |
| `processors/dimensions/d01_price/factory.py` | 🔴 VULNERABLE | ❌ MISSING | - | 86% / 100% | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `processors/dimensions/d01_price/processor.py` | 🔴 VULNERABLE | ❌ MISSING | - | 8% / 0% | 0 / 0 / 0 | ⚪ N/A | ✅ OK | **KRITIKUS: Teszt írás!** |
| `processors/dimensions/d02_support/exceptions/support_error.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `processors/dimensions/d02_support/factory.py` | 🔴 VULNERABLE | ❌ MISSING | - | 86% / 100% | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `processors/dimensions/d02_support/implementations/support_processor.py` | 🔴 VULNERABLE | ❌ MISSING | - | 6% / 0% | 0 / 9 / 41 | ⚪ N/A | ✅ OK | **KRITIKUS: Teszt írás!** |
| `processors/factory.py` | ✅ SECURE | ✅ FOUND | **3**/0/0/0 | 37% / 0% | 0 / 2 / 0 | ⚪ N/A | ⚪ N/A | - |
| `processors/implementations/time_alignment_service.py` | 🟡 WARNING | ✅ FOUND | **1**/7/0/0 | 18% / 0% | 0 / 2 / 3 | ⚪ N/A | ⚠️ UNUSED | - |
| `processors/interfaces/dimension_processor_interface.py` | 🔴 VULNERABLE | ❌ MISSING | - | 80% / 100% | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `processors/interfaces/tensor_converter_interface.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `processors/interfaces/time_alignment_interface.py` | 🔴 VULNERABLE | ❌ MISSING | - | 78% / 100% | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `processors/resampler_service/exceptions/resampler_error.py` | 🔴 VULNERABLE | ❌ MISSING | - | 41% / 100% | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `processors/resampler_service/factory.py` | 🔴 VULNERABLE | ❌ MISSING | - | 39% / 100% | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `processors/resampler_service/implementations/resampler_service.py` | 🔴 VULNERABLE | ❌ MISSING | - | 12% / 0% | 0 / 2 / 1 | ⚪ N/A | ⚠️ UNUSED | **KRITIKUS: Teszt írás!** |
| `processors/resampler_service/interfaces/resampler_interface.py` | 🔴 VULNERABLE | ❌ MISSING | - | 86% / 100% | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |

## 5. Presentation Layer (`neural_ai/ui/`)

| Modul / Fájl | Státusz | Teszt Pár | Pass/Fail/Err/Warn | Coverage (Stmt/Brch) | Lint/Mypy/Pylance | Config | Logger | Teendők |
|:-------------|:--------|:----------|:-------------------|:---------------------|:------------------|:-------|:-------|:--------|
| `ui/app.py` | 🟡 WARNING | ✅ FOUND | **15**/0/0/0 | 34% / 0% | 0 / 0 / 0 | ⚪ N/A | ⚠️ UNUSED | - |
| `ui/components/base_widget.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `ui/core_bridge.py` | ✅ SECURE | ✅ FOUND | **21**/0/0/0 | 14% / 0% | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `ui/factory.py` | ✅ SECURE | ✅ FOUND | **28**/0/0/0 | 15% / 0% | 0 / 17 / 20 | ⚪ N/A | ⚪ N/A | - |
| `ui/interfaces/ai_service_interface.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `ui/interfaces/core_bridge_interface.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `ui/interfaces/dashboard_service_interface.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `ui/interfaces/data_service_interface.py` | ✅ SECURE | ✅ FOUND | **19**/0/0/0 | 100% / 100% | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `ui/interfaces/live_ops_service_interface.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `ui/interfaces/navigation_service_interface.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `ui/interfaces/page_interface.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `ui/interfaces/strategy_service_interface.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `ui/pages/01_🚀_Launchpad.py` | 🔴 VULNERABLE | ❌ MISSING | - | 24% / 50% | 0 / 0 / 0 | ⚪ N/A | ⚠️ UNUSED | **KRITIKUS: Teszt írás!** |
| `ui/pages/02_🛠️_Dev_Center.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `ui/pages/03_📥_Data_Hub.py` | 🔴 VULNERABLE | ❌ MISSING | - | 9% / 2% | 0 / 1 / 3 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `ui/pages/04_🧠_AI_Lab.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `ui/pages/05_🪲_Strategy_Lab.py` | 🔴 VULNERABLE | ❌ MISSING | - | 6% / 1% | 0 / 15 / 99 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `ui/pages/06_⚡_Live_Ops.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `ui/services/ai_service.py` | 🔴 VULNERABLE | ❌ MISSING | - | 17% / 0% | 0 / 0 / 2 | ⚪ N/A | ⚠️ UNUSED | **KRITIKUS: Teszt írás!** |
| `ui/services/dashboard_service.py` | 🟡 WARNING | ✅ FOUND | **13**/0/0/0 | 17% / 0% | 0 / 1 / 0 | ⚪ N/A | ⚠️ UNUSED | - |
| `ui/services/data_service.py` | 🟡 WARNING | ✅ FOUND | **26**/0/0/0 | 8% / 0% | 0 / 6 / 18 | ⚪ N/A | ⚠️ UNUSED | - |
| `ui/services/live_ops_service.py` | 🔴 VULNERABLE | ❌ MISSING | - | 18% / 0% | 0 / 0 / 2 | ⚪ N/A | ⚠️ UNUSED | **KRITIKUS: Teszt írás!** |
| `ui/services/navigation_service.py` | 🔴 VULNERABLE | ❌ MISSING | - | 20% / 0% | 0 / 0 / 0 | ⚪ N/A | ⚠️ UNUSED | **KRITIKUS: Teszt írás!** |
| `ui/services/strategy_service.py` | 🟡 WARNING | ✅ FOUND | **24**/0/0/0 | 8% / 0% | 0 / 8 / 69 | ⚪ N/A | ⚠️ UNUSED | - |
| `ui/streamlit_app.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |

## 6. Tests Layer (`tests/`)

| Modul / Fájl | Státusz | Teszt Pár | Pass/Fail/Err/Warn | Coverage (Stmt/Brch) | Lint/Mypy/Pylance | Config | Logger | Teendők |
|:-------------|:--------|:----------|:-------------------|:---------------------|:------------------|:-------|:-------|:--------|
| `tests/collectors/jforex/exceptions/test_exceptions_init.py` | ✅ SECURE | ✅ FOUND | **5**/0/0/0 | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `tests/collectors/jforex/interfaces/test_interfaces_init.py` | ✅ SECURE | ✅ FOUND | **3**/0/0/0 | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `tests/collectors/jforex/test_bi5_downloader.py` | ✅ SECURE | ✅ FOUND | **43**/0/0/0 | N/A | 0 / 0 / 286 | ⚪ N/A | ⚪ N/A | - |
| `tests/collectors/jforex/test_factory.py` | ✅ SECURE | ✅ FOUND | **10**/0/0/0 | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `tests/collectors/jforex/test_jforex_init.py` | ✅ SECURE | ✅ FOUND | **2**/0/0/0 | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `tests/collectors/jforex/test_live_feed.py` | ✅ SECURE | ✅ FOUND | **12**/0/0/0 | N/A | 0 / 0 / 25 | ⚪ N/A | ⚪ N/A | - |
| `tests/collectors/jforex/test_live_feed_integration.py` | 🔴 VULNERABLE | ✅ FOUND | **8**/0/0/0 | N/A | 0 / 0 / 17 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `tests/core/base/exceptions/test_base_error.py` | ✅ SECURE | ✅ FOUND | **42**/0/0/0 | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `tests/core/base/exceptions/test_exceptions_init.py` | ✅ SECURE | ✅ FOUND | **18**/0/0/0 | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `tests/core/base/implementations/test_component_bundle.py` | ✅ SECURE | ✅ FOUND | **39**/0/0/0 | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `tests/core/base/implementations/test_di_container.py` | ✅ SECURE | ✅ FOUND | **24**/0/0/0 | N/A | 0 / 0 / 20 | ⚪ N/A | ⚪ N/A | - |
| `tests/core/base/implementations/test_implementations_init.py` | ✅ SECURE | ✅ FOUND | **13**/0/0/0 | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `tests/core/base/implementations/test_lazy_loader.py` | ✅ SECURE | ✅ FOUND | **10**/0/0/0 | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `tests/core/base/implementations/test_singleton.py` | ✅ SECURE | ✅ FOUND | **10**/0/0/0 | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `tests/core/base/interfaces/test_component_interface.py` | ✅ SECURE | ✅ FOUND | **13**/0/0/0 | N/A | 0 / 0 / 3 | ⚪ N/A | ⚪ N/A | - |
| `tests/core/base/interfaces/test_container_interface.py` | ✅ SECURE | ✅ FOUND | **20**/0/0/0 | N/A | 0 / 0 / 6 | ⚪ N/A | ⚪ N/A | - |
| `tests/core/base/interfaces/test_interfaces_init.py` | ✅ SECURE | ✅ FOUND | **12**/0/0/0 | N/A | 0 / 0 / 4 | ⚪ N/A | ⚪ N/A | - |
| `tests/core/base/test_base_init.py` | ✅ SECURE | ✅ FOUND | **8**/0/0/0 | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `tests/core/base/test_factory.py` | ✅ SECURE | ✅ FOUND | **35**/0/0/0 | N/A | 0 / 0 / 37 | ⚪ N/A | ⚪ N/A | - |
| `tests/core/config/exceptions/test_config_error.py` | ✅ SECURE | ✅ FOUND | **15**/0/0/0 | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `tests/core/config/implementations/test_config_implementations_init.py` | ✅ SECURE | ✅ FOUND | **4**/0/0/0 | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `tests/core/config/implementations/test_dynamic_config_manager.py` | ✅ SECURE | ✅ FOUND | **48**/0/0/0 | N/A | 0 / 0 / 54 | ⚪ N/A | ⚪ N/A | - |
| `tests/core/config/implementations/test_dynamic_config_manager_comprehensive.py` | 🔴 VULNERABLE | ✅ FOUND | **13**/0/0/0 | N/A | 0 / 0 / 9 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `tests/core/config/implementations/test_yaml_config_manager.py` | ✅ SECURE | ✅ FOUND | **65**/0/0/0 | N/A | 0 / 0 / 17 | ⚪ N/A | ⚪ N/A | - |
| `tests/core/config/interfaces/test_async_config_interface.py` | 🟡 WARNING | ✅ FOUND | **25**/0/0/0 | N/A | 0 / 0 / 1 | ⚪ N/A | ⚠️ UNUSED | - |
| `tests/core/config/interfaces/test_config_interface.py` | ✅ SECURE | ✅ FOUND | **17**/0/0/0 | N/A | 0 / 0 / 1 | ⚪ N/A | ⚪ N/A | - |
| `tests/core/config/interfaces/test_factory_interface.py` | ✅ SECURE | ✅ FOUND | **23**/0/0/0 | N/A | 0 / 0 / 11 | ⚪ N/A | ⚪ N/A | - |
| `tests/core/config/test_config_factory.py` | ✅ SECURE | ✅ FOUND | **31**/0/0/0 | N/A | 0 / 0 / 1 | ⚪ N/A | ⚪ N/A | - |
| `tests/core/config/test_processors_config.py` | ✅ SECURE | ✅ FOUND | **0**/26/0/0 | N/A | 0 / 0 / 44 | ⚪ N/A | ⚪ N/A | - |
| `tests/core/config/test_yaml_config_manager_validation.py` | ✅ SECURE | ✅ FOUND | **11**/0/0/0 | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `tests/core/db/exceptions/test_db_error.py` | ✅ SECURE | ✅ FOUND | **9**/0/0/0 | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `tests/core/db/exceptions/test_db_exceptions_init.py` | ✅ SECURE | ✅ FOUND | **5**/0/0/0 | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `tests/core/db/implementations/test_db_implementations_init.py` | ✅ SECURE | ✅ FOUND | **8**/0/0/0 | N/A | 0 / 0 / 3 | ⚪ N/A | ⚪ N/A | - |
| `tests/core/db/implementations/test_model_base.py` | ✅ SECURE | ✅ FOUND | **12**/0/0/0 | N/A | 0 / 0 / 2 | ⚪ N/A | ⚪ N/A | - |
| `tests/core/db/implementations/test_models.py` | ✅ SECURE | ✅ FOUND | **22**/0/0/0 | N/A | 0 / 0 / 13 | ⚪ N/A | ⚪ N/A | - |
| `tests/core/db/implementations/test_sqlalchemy_session.py` | ✅ SECURE | ✅ FOUND | **22**/0/0/0 | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `tests/core/db/interfaces/test_db_interfaces_init.py` | ✅ SECURE | ✅ FOUND | **4**/0/0/0 | N/A | 0 / 0 / 1 | ⚪ N/A | ⚪ N/A | - |
| `tests/core/db/test_db_factory.py` | ✅ SECURE | ✅ FOUND | **21**/1/0/0 | N/A | 0 / 0 / 7 | ⚪ N/A | ⚪ N/A | - |
| `tests/core/db/test_db_init.py` | ✅ SECURE | ✅ FOUND | **8**/0/0/0 | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `tests/core/events/exceptions/test_event_error.py` | ✅ SECURE | ✅ FOUND | **9**/0/0/0 | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `tests/core/events/exceptions/test_events_exceptions_init.py` | ✅ SECURE | ✅ FOUND | **5**/0/0/0 | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `tests/core/events/implementations/test_events_implementations_init.py` | ✅ SECURE | ✅ FOUND | **4**/0/0/0 | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `tests/core/events/implementations/test_zeromq_bus.py` | ✅ SECURE | ✅ FOUND | **24**/25/0/0 | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `tests/core/events/interfaces/test_event_bus_interface.py` | ✅ SECURE | ✅ FOUND | **27**/0/0/0 | N/A | 0 / 0 / 0 | ✅ OK | ⚪ N/A | - |
| `tests/core/events/interfaces/test_event_models.py` | ✅ SECURE | ✅ FOUND | **26**/0/0/0 | N/A | 0 / 0 / 8 | ⚪ N/A | ⚪ N/A | - |
| `tests/core/events/interfaces/test_events_interfaces_init.py` | ✅ SECURE | ✅ FOUND | **11**/0/0/0 | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `tests/core/events/test_events_factory.py` | ✅ SECURE | ✅ FOUND | **11**/1/0/0 | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `tests/core/events/test_events_init.py` | ✅ SECURE | ✅ FOUND | **10**/0/0/0 | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `tests/core/logger/exceptions/test_logger_error.py` | ✅ SECURE | ✅ FOUND | **14**/0/0/0 | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `tests/core/logger/formatters/test_logger_formatters.py` | ✅ SECURE | ✅ FOUND | **6**/0/0/0 | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `tests/core/logger/implementations/test_colored_logger.py` | ✅ SECURE | ✅ FOUND | **12**/0/0/0 | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `tests/core/logger/implementations/test_default_logger.py` | ✅ SECURE | ✅ FOUND | **9**/0/0/0 | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `tests/core/logger/implementations/test_rotating_file_logger.py` | ✅ SECURE | ✅ FOUND | **22**/0/0/0 | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `tests/core/logger/interfaces/test_logger_factory_interface.py` | ✅ SECURE | ✅ FOUND | **5**/0/0/0 | N/A | 0 / 0 / 2 | ⚪ N/A | ⚪ N/A | - |
| `tests/core/logger/interfaces/test_logger_interface.py` | ✅ SECURE | ✅ FOUND | **3**/0/0/0 | N/A | 0 / 0 / 1 | ⚪ N/A | ⚪ N/A | - |
| `tests/core/logger/interfaces/test_logger_interfaces_init.py` | ✅ SECURE | ✅ FOUND | **4**/0/0/0 | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `tests/core/logger/test_logger_factory.py` | ✅ SECURE | ✅ FOUND | **5**/0/0/0 | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `tests/core/logger/test_logger_init.py` | ✅ SECURE | ✅ FOUND | **14**/0/0/0 | N/A | 0 / 0 / 2 | ⚪ N/A | ⚪ N/A | - |
| `tests/core/system/implementations/test_health_monitor.py` | ✅ SECURE | ✅ FOUND | **28**/0/0/0 | N/A | 0 / 0 / 1 | ⚪ N/A | ⚪ N/A | - |
| `tests/core/system/interfaces/test_health_interface.py` | ✅ SECURE | ✅ FOUND | **22**/0/0/0 | N/A | 0 / 0 / 16 | ⚪ N/A | ⚪ N/A | - |
| `tests/core/system/test_system_factory.py` | ✅ SECURE | ✅ FOUND | **19**/0/0/0 | N/A | 0 / 0 / 2 | ⚪ N/A | ⚪ N/A | - |
| `tests/core/test_core_init.py` | ✅ SECURE | ✅ FOUND | **11**/8/0/0 | N/A | 0 / 0 / 26 | ⚪ N/A | ⚪ N/A | - |
| `tests/core/test_init_version_fallback.py` | ✅ SECURE | ✅ FOUND | **4**/1/0/0 | N/A | 0 / 0 / 2 | ⚪ N/A | ⚪ N/A | - |
| `tests/core/test_pyproject_ui_dependencies.py` | ✅ SECURE | ✅ FOUND | **6**/0/0/0 | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `tests/core/utils/exceptions/test_util_errors.py` | ✅ SECURE | ✅ FOUND | **12**/0/0/0 | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `tests/core/utils/interfaces/test_hardware_interface.py` | ✅ SECURE | ✅ FOUND | **3**/0/0/0 | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `tests/core/utils/test_decorators.py` | ✅ SECURE | ✅ FOUND | **2**/11/0/0 | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `tests/core/utils/test_hardware_info.py` | ✅ SECURE | ✅ FOUND | **15**/0/0/0 | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `tests/core/utils/test_utils_factory.py` | ✅ SECURE | ✅ FOUND | **11**/0/0/0 | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `tests/data/ingestion/test_market_data_persister.py` | ✅ SECURE | ✅ FOUND | **20**/0/0/0 | N/A | 0 / 0 / 0 | ✅ OK | ⚪ N/A | - |
| `tests/data/storage/backends/test_base.py` | ✅ SECURE | ✅ FOUND | **2**/6/0/0 | N/A | 0 / 0 / 76 | ⚪ N/A | ⚪ N/A | - |
| `tests/data/storage/backends/test_pandas_backend.py` | ✅ SECURE | ✅ FOUND | **30**/0/0/0 | N/A | 0 / 0 / 22 | ⚪ N/A | ⚪ N/A | - |
| `tests/data/storage/backends/test_polars_backend.py` | ✅ SECURE | ✅ FOUND | **13**/13/0/0 | N/A | 0 / 0 / 13 | ⚪ N/A | ⚪ N/A | - |
| `tests/data/storage/implementations/test_file_storage.py` | ✅ SECURE | ✅ FOUND | **46**/4/0/0 | N/A | 0 / 0 / 30 | ⚪ N/A | ⚪ N/A | - |
| `tests/data/storage/implementations/test_parquet_storage.py` | ✅ SECURE | ✅ FOUND | **33**/1/0/0 | N/A | 0 / 0 / 2 | ⚪ N/A | ⚪ N/A | - |
| `tests/data/storage/interfaces/test_storage_factory_interface.py` | ✅ SECURE | ✅ FOUND | **6**/0/0/0 | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `tests/data/storage/interfaces/test_storage_interface.py` | ✅ SECURE | ✅ FOUND | **11**/0/0/0 | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `tests/data/storage/test_storage_factory.py` | ✅ SECURE | ✅ FOUND | **12**/0/0/0 | N/A | 0 / 0 / 8 | ⚪ N/A | ⚪ N/A | - |
| `tests/data/storage/test_storage_init.py` | ✅ SECURE | ✅ FOUND | **5**/0/0/0 | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `tests/processors/dimensions/d02_support/test_processor.py` | ✅ SECURE | ✅ FOUND | **3**/1/0/0 | N/A | 0 / 0 / 28 | ⚪ N/A | ⚪ N/A | - |
| `tests/processors/test_factory.py` | ✅ SECURE | ✅ FOUND | **3**/0/0/0 | N/A | 0 / 0 / 14 | ⚪ N/A | ⚪ N/A | - |
| `tests/processors/test_time_alignment_service.py` | ✅ SECURE | ✅ FOUND | **1**/7/0/0 | N/A | 0 / 0 / 2 | ⚪ N/A | ⚪ N/A | - |
| `tests/scripts/test_data_reset.py` | ✅ SECURE | ✅ FOUND | **12**/2/0/0 | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `tests/scripts/test_download_history.py` | ✅ SECURE | ✅ FOUND | **9**/2/0/0 | N/A | 0 / 0 / 1 | ⚪ N/A | ⚪ N/A | - |
| `tests/scripts/test_migrate_structure.py` | ✅ SECURE | ✅ FOUND | **12**/1/0/0 | N/A | 0 / 0 / 10 | ⚪ N/A | ⚪ N/A | - |
| `tests/scripts/test_test_tick_pipeline.py` | ✅ SECURE | ✅ FOUND | **4**/1/0/0 | N/A | 0 / 0 / 8 | ⚪ N/A | ⚪ N/A | - |
| `tests/scripts/test_validation_end_to_end.py` | ✅ SECURE | ✅ FOUND | **2**/1/0/0 | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `tests/test_dashboard_command.py` | ✅ SECURE | ✅ FOUND | **6**/7/0/0 | N/A | 0 / 0 / 5 | ⚪ N/A | ⚪ N/A | - |
| `tests/test_main.py` | ✅ SECURE | ✅ FOUND | **5**/6/0/0 | N/A | 0 / 0 / 10 | ⚪ N/A | ⚪ N/A | - |
| `tests/test_neural_ai_init.py` | ✅ SECURE | ✅ FOUND | **4**/1/0/0 | N/A | 0 / 0 / 2 | ⚪ N/A | ⚪ N/A | - |
| `tests/ui/interfaces/test_data_service_interface.py` | ✅ SECURE | ✅ FOUND | **19**/0/0/0 | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `tests/ui/pages/test_data_hub_page.py` | ✅ SECURE | ✅ FOUND | **11**/0/0/0 | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `tests/ui/pages/test_launchpad_page.py` | ✅ SECURE | ✅ FOUND | **10**/0/0/0 | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `tests/ui/pages/test_strategy_lab_page.py` | ✅ SECURE | ✅ FOUND | **26**/0/0/0 | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `tests/ui/services/test_dashboard_service.py` | ✅ SECURE | ✅ FOUND | **13**/0/0/0 | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `tests/ui/services/test_data_service.py` | ✅ SECURE | ✅ FOUND | **26**/0/0/0 | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `tests/ui/services/test_strategy_service.py` | ✅ SECURE | ✅ FOUND | **24**/0/0/0 | N/A | 0 / 0 / 18 | ⚪ N/A | ⚪ N/A | - |
| `tests/ui/test_app.py` | ✅ SECURE | ✅ FOUND | **15**/0/0/0 | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `tests/ui/test_core_bridge.py` | ✅ SECURE | ✅ FOUND | **21**/0/0/0 | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `tests/ui/test_ui_factory.py` | ✅ SECURE | ✅ FOUND | **28**/0/0/0 | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | - |

## 7. Scripts Layer (`scripts/`)

| Modul / Fájl | Státusz | Teszt Pár | Pass/Fail/Err/Warn | Coverage (Stmt/Brch) | Lint/Mypy/Pylance | Config | Logger | Teendők |
|:-------------|:--------|:----------|:-------------------|:---------------------|:------------------|:-------|:-------|:--------|
| `scripts/audit_data.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `scripts/bootstrap_integration_test.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `scripts/bootstrap_test.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `scripts/data_reset.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `scripts/deploy_jforex.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `scripts/download_history.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 2 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `scripts/force_kill.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `scripts/generate_docs.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `scripts/generate_task_tree.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 54 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `scripts/install.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `scripts/migrate_structure.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `scripts/smart_pack.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `scripts/test_d2_standalone.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 25 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `scripts/test_tick_pipeline.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 1 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `scripts/validation_end_to_end.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 11 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
