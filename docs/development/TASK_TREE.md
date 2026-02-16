# 🌳 NEURAL AI NEXT - TASK TREE v4.0 (ULTIMATE AUDIT)

**Generálva:** 2026-02-16 18:17:06 UTC
**Módszer:** Hibrid (AST + Pytest + Coverage + Ruff + Mypy)
**Fájlok száma:** 99 elemezve

---

## 📊 ÖSSZESÍTŐ STATISZTIKA

- **✅ SECURE**: 40 fájl (40.4%)
- **🟡 WARNING**: 16 fájl (16.2%)
- **🔴 VULNERABLE**: 43 fájl (43.4%)
- **Teszt lefedettség**: 59/99 fájl (59.6%)

---

## 📂 RÉSZLETES AUDIT EREDMÉNYEK (DDD RÉTEGEK)

### 1. Infrastructure Layer (`neural_ai/core/`)

| Modul / Fájl | Státusz | Teszt Pár | Pass/Fail/Err/Warn | Cov (Stmt/Brch) | Lint/Type | Config | Logger | Teendők |
|--------------|---------|-----------|-------------------|-----------------|-----------|--------|--------|---------|
| `core/base/exceptions/base_error.py` | ✅ SECURE | ✅ FOUND | **42**/0/0/0 | 100% / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/base/factory.py` | ✅ SECURE | ✅ FOUND | **35**/0/0/0 | **23%** / 0% | 0 / 0 | ✅ OK | ⚪ N/A | - |
| `core/base/implementations/component_bundle.py` | ✅ SECURE | ✅ FOUND | **39**/0/0/0 | **39%** / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/base/implementations/di_container.py` | ✅ SECURE | ✅ FOUND | **24**/0/0/0 | **28%** / 0% | 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/base/implementations/lazy_loader.py` | ✅ SECURE | ✅ FOUND | **10**/0/0/0 | **43%** / 0% | 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/base/implementations/singleton.py` | ✅ SECURE | ✅ FOUND | **10**/0/0/0 | **43%** / 0% | 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/base/interfaces/component_interface.py` | ✅ SECURE | ✅ FOUND | **13**/0/0/0 | **76%** / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/base/interfaces/container_interface.py` | ✅ SECURE | ✅ FOUND | **20**/0/0/0 | **75%** / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/config/exceptions/config_error.py` | ✅ SECURE | ✅ FOUND | **15**/0/0/0 | **40%** / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/config/factory.py` | ✅ SECURE | ✅ FOUND | **31**/0/0/0 | **26%** / 0% | 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/config/implementations/dynamic_config_manager.py` | 🟡 WARNING | ✅ FOUND | **48**/0/0/0 | **10%** / 0% | 0 / 0 | ⚪ N/A | ⚠️ UNUSED | - |
| `core/config/implementations/yaml_config_manager.py` | 🟡 WARNING | ✅ FOUND | **65**/0/0/0 | **13%** / 0% | 0 / 0 | ⚪ N/A | ⚠️ UNUSED | - |
| `core/config/interfaces/async_config_interface.py` | 🟡 WARNING | ✅ FOUND | **25**/0/0/0 | 100% / 100% | 0 / 0 | ⚪ N/A | ⚠️ UNUSED | - |
| `core/config/interfaces/config_interface.py` | ✅ SECURE | ✅ FOUND | **17**/0/0/0 | 100% / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/config/interfaces/factory_interface.py` | ✅ SECURE | ✅ FOUND | **23**/0/0/0 | 80% / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/config/interfaces/types.py` | 🔴 VULNERABLE | ❌ MISSING | - | 84% / 0% | 0 / 0 | ✅ OK | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `core/db/exceptions/db_error.py` | ✅ SECURE | ✅ FOUND | **9**/0/0/0 | **54%** / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/db/factory.py` | 🟡 WARNING | ✅ FOUND | **21**/**1**/0/0 | **62%** / 100% | 0 / 0 | ⚪ N/A | ⚠️ UNUSED | - |
| `core/db/implementations/model_base.py` | ✅ SECURE | ✅ FOUND | **12**/0/0/0 | **52%** / 0% | 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/db/implementations/models.py` | ✅ SECURE | ✅ FOUND | **22**/0/0/0 | 92% / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/db/implementations/sqlalchemy_session.py` | ✅ SECURE | ✅ FOUND | **22**/0/0/0 | **17%** / 0% | 0 / 0 | ⚪ N/A | ✅ OK | - |
| `core/events/exceptions/event_error.py` | ✅ SECURE | ✅ FOUND | **9**/0/0/0 | **54%** / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/events/factory.py` | 🟡 WARNING | ✅ FOUND | **11**/**1**/0/0 | **28%** / 100% | 0 / 0 | ⚪ N/A | ⚠️ UNUSED | - |
| `core/events/implementations/zeromq_bus.py` | 🟡 WARNING | ✅ FOUND | **24**/**25**/0/0 | **14%** / 0% | 0 / **1** | ✅ OK | ⚠️ UNUSED | - |
| `core/events/interfaces/event_bus_interface.py` | ✅ SECURE | ✅ FOUND | **27**/0/0/0 | 100% / 100% | 0 / 0 | ✅ OK | ⚪ N/A | - |
| `core/events/interfaces/event_models.py` | ✅ SECURE | ✅ FOUND | **26**/0/0/0 | **64%** / 0% | 0 / 0 | ✅ OK | ⚪ N/A | - |
| `core/logger/exceptions/logger_error.py` | ✅ SECURE | ✅ FOUND | **14**/0/0/0 | 100% / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/logger/factory.py` | ✅ SECURE | ✅ FOUND | **5**/0/0/0 | **30%** / 11% | 0 / **2** | ⚪ N/A | ⚪ N/A | - |
| `core/logger/formatters/logger_formatters.py` | ✅ SECURE | ✅ FOUND | **6**/0/0/0 | **45%** / 0% | 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/logger/implementations/colored_logger.py` | 🔴 VULNERABLE | ✅ FOUND | **12**/0/0/0 | **32%** / 0% | 0 / 0 | ⚪ N/A | 🔴 MISSING | **Logger DI hiányzik!** |
| `core/logger/implementations/default_logger.py` | 🔴 VULNERABLE | ✅ FOUND | **9**/0/0/0 | **70%** / 100% | 0 / 0 | ⚪ N/A | 🔴 MISSING | **Logger DI hiányzik!** |
| `core/logger/implementations/rotating_file_logger.py` | 🔴 VULNERABLE | ✅ FOUND | **22**/0/0/0 | **22%** / 0% | 0 / 0 | ⚪ N/A | 🔴 MISSING | **Logger DI hiányzik!** |
| `core/logger/interfaces/factory_interface.py` | 🔴 VULNERABLE | ❌ MISSING | - | 81% / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `core/logger/interfaces/logger_interface.py` | ✅ SECURE | ✅ FOUND | **3**/0/0/0 | **70%** / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/system/exceptions/health_error.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `core/system/factory.py` | ✅ SECURE | ✅ FOUND | **19**/0/0/0 | **35%** / 0% | 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/system/implementations/health_monitor.py` | 🟡 WARNING | ✅ FOUND | **28**/0/0/0 | **11%** / 0% | 0 / **1** | ⚪ N/A | ⚠️ UNUSED | - |
| `core/system/interfaces/health_interface.py` | ✅ SECURE | ✅ FOUND | **22**/0/0/0 | 100% / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/utils/decorators.py` | ✅ SECURE | ✅ FOUND | **2**/**11**/0/0 | **39%** / 0% | 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/utils/exceptions/util_error.py` | 🔴 VULNERABLE | ❌ MISSING | - | **56%** / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `core/utils/factory.py` | ✅ SECURE | ✅ FOUND | **11**/0/0/0 | **60%** / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/utils/implementations/hardware_info.py` | ✅ SECURE | ✅ FOUND | **15**/0/0/0 | **19%** / 0% | 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/utils/interfaces/hardware_interface.py` | ✅ SECURE | ✅ FOUND | **3**/0/0/0 | 100% / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | - |

---

### 2. Input Layer (`neural_ai/collectors/`)

| Modul / Fájl | Státusz | Teszt Pár | Pass/Fail/Err/Warn | Cov (Stmt/Brch) | Lint/Type | Config | Logger | Teendők |
|--------------|---------|-----------|-------------------|-----------------|-----------|--------|--------|---------|
| `collectors/jforex/exceptions/jforex_error.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `collectors/jforex/factory.py` | ✅ SECURE | ✅ FOUND | **10**/0/0/0 | **19%** / 0% | 0 / **12** | ⚪ N/A | ⚪ N/A | - |
| `collectors/jforex/implementations/bi5_downloader.py` | 🟡 WARNING | ✅ FOUND | **43**/0/0/0 | **8%** / 0% | 0 / 0 | ⚪ N/A | ⚠️ UNUSED | - |
| `collectors/jforex/implementations/live_feed.py` | ✅ SECURE | ✅ FOUND | **12**/0/0/0 | **13%** / 0% | 0 / 0 | ⚪ N/A | ✅ OK | - |
| `collectors/jforex/interfaces/downloader_interface.py` | 🔴 VULNERABLE | ❌ MISSING | - | **75%** / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `collectors/jforex/interfaces/live_interface.py` | 🔴 VULNERABLE | ❌ MISSING | - | **73%** / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `collectors/jforex/interfaces/tick_data.py` | 🔴 VULNERABLE | ❌ MISSING | - | 88% / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |

---

### 3. Persistence Layer (`neural_ai/data/`)

| Modul / Fájl | Státusz | Teszt Pár | Pass/Fail/Err/Warn | Cov (Stmt/Brch) | Lint/Type | Config | Logger | Teendők |
|--------------|---------|-----------|-------------------|-----------------|-----------|--------|--------|---------|
| `data/ingestion/market_data_persister.py` | ✅ SECURE | ✅ FOUND | **20**/0/0/0 | **7%** / 0% | 0 / **6** | ⚪ N/A | ✅ OK | - |
| `data/storage/backends/base.py` | 🟡 WARNING | ✅ FOUND | **2**/**6**/0/0 | **32%** / 6% | 0 / 0 | ⚪ N/A | ⚠️ UNUSED | - |
| `data/storage/backends/pandas_backend.py` | 🟡 WARNING | ✅ FOUND | **30**/0/0/0 | **19%** / 3% | 0 / 0 | ⚪ N/A | ⚠️ UNUSED | - |
| `data/storage/backends/polars_backend.py` | 🟡 WARNING | ✅ FOUND | **13**/**13**/0/0 | **16%** / 2% | 0 / 0 | ⚪ N/A | ⚠️ UNUSED | - |
| `data/storage/factory.py` | ✅ SECURE | ✅ FOUND | **12**/0/0/0 | **28%** / 0% | 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `data/storage/implementations/file_storage.py` | ✅ SECURE | ✅ FOUND | **46**/**4**/0/0 | **11%** / 0% | 0 / **5** | ⚪ N/A | ✅ OK | - |
| `data/storage/implementations/parquet_storage.py` | ✅ SECURE | ✅ FOUND | **33**/**1**/0/0 | **12%** / 0% | 0 / **1** | ✅ OK | ✅ OK | - |
| `data/storage/interfaces/factory_interface.py` | 🔴 VULNERABLE | ❌ MISSING | - | 83% / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `data/storage/interfaces/storage_interface.py` | ✅ SECURE | ✅ FOUND | **11**/0/0/0 | 100% / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | - |

---

### 4. Domain Layer (`neural_ai/processors/`)

| Modul / Fájl | Státusz | Teszt Pár | Pass/Fail/Err/Warn | Cov (Stmt/Brch) | Lint/Type | Config | Logger | Teendők |
|--------------|---------|-----------|-------------------|-----------------|-----------|--------|--------|---------|
| `processors/dimensions/base.py` | 🔴 VULNERABLE | ❌ MISSING | - | **47%** / 0% | 0 / 0 | ⚪ N/A | ✅ OK | **KRITIKUS: Teszt írás!** |
| `processors/dimensions/d01_price/factory.py` | 🔴 VULNERABLE | ❌ MISSING | - | 86% / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `processors/dimensions/d01_price/processor.py` | 🔴 VULNERABLE | ❌ MISSING | - | **8%** / 0% | 0 / 0 | ⚪ N/A | ✅ OK | **KRITIKUS: Teszt írás!** |
| `processors/dimensions/d02_support/exceptions/support_error.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `processors/dimensions/d02_support/factory.py` | 🔴 VULNERABLE | ❌ MISSING | - | 86% / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `processors/dimensions/d02_support/implementations/support_processor.py` | 🔴 VULNERABLE | ❌ MISSING | - | **6%** / 0% | 0 / **9** | ⚪ N/A | ✅ OK | **KRITIKUS: Teszt írás!** |
| `processors/factory.py` | ✅ SECURE | ✅ FOUND | **3**/0/0/0 | **37%** / 0% | 0 / **2** | ⚪ N/A | ⚪ N/A | - |
| `processors/implementations/time_alignment_service.py` | 🟡 WARNING | ✅ FOUND | **1**/**7**/0/0 | **18%** / 0% | 0 / **2** | ⚪ N/A | ⚠️ UNUSED | - |
| `processors/interfaces/dimension_processor_interface.py` | 🔴 VULNERABLE | ❌ MISSING | - | 80% / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `processors/interfaces/tensor_converter_interface.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `processors/interfaces/time_alignment_interface.py` | 🔴 VULNERABLE | ❌ MISSING | - | **78%** / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `processors/resampler_service/exceptions/resampler_error.py` | 🔴 VULNERABLE | ❌ MISSING | - | **41%** / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `processors/resampler_service/factory.py` | 🔴 VULNERABLE | ❌ MISSING | - | **39%** / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `processors/resampler_service/implementations/resampler_service.py` | 🔴 VULNERABLE | ❌ MISSING | - | **12%** / 0% | 0 / **2** | ⚪ N/A | ⚠️ UNUSED | **KRITIKUS: Teszt írás!** |
| `processors/resampler_service/interfaces/resampler_interface.py` | 🔴 VULNERABLE | ❌ MISSING | - | 86% / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |

---

### 5. Presentation Layer (`neural_ai/ui/`)

| Modul / Fájl | Státusz | Teszt Pár | Pass/Fail/Err/Warn | Cov (Stmt/Brch) | Lint/Type | Config | Logger | Teendők |
|--------------|---------|-----------|-------------------|-----------------|-----------|--------|--------|---------|
| `ui/app.py` | 🟡 WARNING | ✅ FOUND | **15**/0/0/0 | **34%** / 0% | 0 / 0 | ⚪ N/A | ⚠️ UNUSED | - |
| `ui/components/base_widget.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `ui/core_bridge.py` | ✅ SECURE | ✅ FOUND | **21**/0/0/0 | **14%** / 0% | 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `ui/factory.py` | ✅ SECURE | ✅ FOUND | **28**/0/0/0 | **15%** / 0% | 0 / **17** | ⚪ N/A | ⚪ N/A | - |
| `ui/interfaces/ai_service_interface.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `ui/interfaces/core_bridge_interface.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `ui/interfaces/dashboard_service_interface.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `ui/interfaces/data_service_interface.py` | ✅ SECURE | ✅ FOUND | **19**/0/0/0 | 100% / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `ui/interfaces/live_ops_service_interface.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `ui/interfaces/navigation_service_interface.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `ui/interfaces/page_interface.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `ui/interfaces/strategy_service_interface.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `ui/pages/01_🚀_Launchpad.py` | 🔴 VULNERABLE | ❌ MISSING | - | **24%** / 50% | 0 / 0 | ⚪ N/A | ⚠️ UNUSED | **KRITIKUS: Teszt írás!** |
| `ui/pages/02_🛠️_Dev_Center.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `ui/pages/03_📥_Data_Hub.py` | 🔴 VULNERABLE | ❌ MISSING | - | **9%** / 2% | 0 / **1** | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `ui/pages/04_🧠_AI_Lab.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `ui/pages/05_🪲_Strategy_Lab.py` | 🔴 VULNERABLE | ❌ MISSING | - | **6%** / 1% | 0 / **15** | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `ui/pages/06_⚡_Live_Ops.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `ui/services/ai_service.py` | 🔴 VULNERABLE | ❌ MISSING | - | **17%** / 0% | 0 / 0 | ⚪ N/A | ⚠️ UNUSED | **KRITIKUS: Teszt írás!** |
| `ui/services/dashboard_service.py` | 🟡 WARNING | ✅ FOUND | **13**/0/0/0 | **17%** / 0% | 0 / **1** | ⚪ N/A | ⚠️ UNUSED | - |
| `ui/services/data_service.py` | 🟡 WARNING | ✅ FOUND | **26**/0/0/0 | **8%** / 0% | 0 / **6** | ⚪ N/A | ⚠️ UNUSED | - |
| `ui/services/live_ops_service.py` | 🔴 VULNERABLE | ❌ MISSING | - | **18%** / 0% | 0 / 0 | ⚪ N/A | ⚠️ UNUSED | **KRITIKUS: Teszt írás!** |
| `ui/services/navigation_service.py` | 🔴 VULNERABLE | ❌ MISSING | - | **20%** / 0% | 0 / 0 | ⚪ N/A | ⚠️ UNUSED | **KRITIKUS: Teszt írás!** |
| `ui/services/strategy_service.py` | 🟡 WARNING | ✅ FOUND | **24**/0/0/0 | **8%** / 0% | 0 / **8** | ⚪ N/A | ⚠️ UNUSED | - |
| `ui/streamlit_app.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |

---
