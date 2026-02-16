# 🌳 NEURAL AI NEXT - TASK TREE v4.0 (ULTIMATE AUDIT)

**Generálva:** 2026-02-16 15:37:21 UTC
**Módszer:** Hibrid (AST + Pytest + Coverage + Ruff + Mypy)
**Fájlok száma:** 99 elemezve

---

## 📊 ÖSSZESÍTŐ STATISZTIKA

- **✅ SECURE**: 34 fájl (34.3%)
- **🟡 WARNING**: 14 fájl (14.1%)
- **🔴 VULNERABLE**: 51 fájl (51.5%)
- **Teszt lefedettség**: 51/99 fájl (51.5%)

---

## 📂 RÉSZLETES AUDIT EREDMÉNYEK (DDD RÉTEGEK)

### 1. Infrastructure Layer (`neural_ai/core/`)

| Modul / Fájl | Státusz | Teszt Pár | Tesztek | Cov (Stmt/Brch) | Lint/Type | Config | Logger | Teendők |
|--------------|---------|-----------|---------|-----------------|-----------|--------|--------|---------|
| `core/base/exceptions/base_error.py` | ✅ SECURE | ✅ FOUND | 42 | 100% / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/base/factory.py` | ✅ SECURE | ✅ FOUND | 35 | **23%** / 0% | 0 / 0 | ✅ OK | ⚪ N/A | - |
| `core/base/implementations/component_bundle.py` | ✅ SECURE | ✅ FOUND | 39 | **39%** / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/base/implementations/di_container.py` | ✅ SECURE | ✅ FOUND | 24 | **28%** / 0% | 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/base/implementations/lazy_loader.py` | ✅ SECURE | ✅ FOUND | 10 | **43%** / 0% | 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/base/implementations/singleton.py` | ✅ SECURE | ✅ FOUND | 10 | **43%** / 0% | 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/base/interfaces/component_interface.py` | ✅ SECURE | ✅ FOUND | 13 | **76%** / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/base/interfaces/container_interface.py` | ✅ SECURE | ✅ FOUND | 20 | **75%** / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/config/exceptions/config_error.py` | ✅ SECURE | ✅ FOUND | 15 | **40%** / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/config/factory.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | **26%** / 0% | 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `core/config/implementations/dynamic_config_manager.py` | 🟡 WARNING | ✅ FOUND | 13 | **10%** / 0% | 0 / 0 | ⚪ N/A | ⚠️ UNUSED | - |
| `core/config/implementations/yaml_config_manager.py` | 🟡 WARNING | ✅ FOUND | 65 | **13%** / 0% | 0 / 0 | ⚪ N/A | ⚠️ UNUSED | - |
| `core/config/interfaces/async_config_interface.py` | 🟡 WARNING | ✅ FOUND | 11 | 100% / 100% | 0 / 0 | ⚪ N/A | ⚠️ UNUSED | - |
| `core/config/interfaces/config_interface.py` | ✅ SECURE | ✅ FOUND | 17 | 100% / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/config/interfaces/factory_interface.py` | ✅ SECURE | ✅ FOUND | 23 | 80% / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/config/interfaces/types.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | 84% / 0% | 0 / 0 | ✅ OK | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `core/db/exceptions/db_error.py` | ✅ SECURE | ✅ FOUND | 9 | **54%** / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/db/factory.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | **62%** / 100% | 0 / 0 | ⚪ N/A | ⚠️ UNUSED | **KRITIKUS: Teszt írás!** |
| `core/db/implementations/model_base.py` | ✅ SECURE | ✅ FOUND | 12 | **52%** / 0% | 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/db/implementations/models.py` | ✅ SECURE | ✅ FOUND | 22 | 92% / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/db/implementations/sqlalchemy_session.py` | ✅ SECURE | ✅ FOUND | 10 | **17%** / 0% | 0 / 0 | ⚪ N/A | ✅ OK | - |
| `core/events/exceptions/event_error.py` | ✅ SECURE | ✅ FOUND | 9 | **54%** / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/events/factory.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | **28%** / 100% | 0 / 0 | ⚪ N/A | ⚠️ UNUSED | **KRITIKUS: Teszt írás!** |
| `core/events/implementations/zeromq_bus.py` | 🟡 WARNING | ✅ FOUND | 17 | **14%** / 0% | 0 / **1** | ✅ OK | ⚠️ UNUSED | - |
| `core/events/interfaces/event_bus_interface.py` | ✅ SECURE | ✅ FOUND | 27 | 100% / 100% | 0 / 0 | ✅ OK | ⚪ N/A | - |
| `core/events/interfaces/event_models.py` | ✅ SECURE | ✅ FOUND | 26 | **64%** / 0% | 0 / 0 | ✅ OK | ⚪ N/A | - |
| `core/logger/exceptions/logger_error.py` | ✅ SECURE | ✅ FOUND | 14 | 100% / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/logger/factory.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | **30%** / 11% | 0 / **2** | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `core/logger/formatters/logger_formatters.py` | ✅ SECURE | ✅ FOUND | 6 | **45%** / 0% | 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/logger/implementations/colored_logger.py` | 🔴 VULNERABLE | ✅ FOUND | 12 | **32%** / 0% | 0 / 0 | ⚪ N/A | 🔴 MISSING | **Logger DI hiányzik!** |
| `core/logger/implementations/default_logger.py` | 🔴 VULNERABLE | ✅ FOUND | 9 | **70%** / 100% | 0 / 0 | ⚪ N/A | 🔴 MISSING | **Logger DI hiányzik!** |
| `core/logger/implementations/rotating_file_logger.py` | 🔴 VULNERABLE | ✅ FOUND | 22 | **22%** / 0% | 0 / 0 | ⚪ N/A | 🔴 MISSING | **Logger DI hiányzik!** |
| `core/logger/interfaces/factory_interface.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | 81% / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `core/logger/interfaces/logger_interface.py` | ✅ SECURE | ✅ FOUND | 3 | **70%** / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/system/exceptions/health_error.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | N/A | 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `core/system/factory.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | **35%** / 0% | 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `core/system/implementations/health_monitor.py` | 🟡 WARNING | ✅ FOUND | 9 | **11%** / 0% | 0 / **1** | ⚪ N/A | ⚠️ UNUSED | - |
| `core/system/interfaces/health_interface.py` | ✅ SECURE | ✅ FOUND | 22 | 100% / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/utils/decorators.py` | ✅ SECURE | ✅ FOUND | 13 | **39%** / 0% | 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/utils/exceptions/util_error.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | **56%** / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `core/utils/factory.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | **60%** / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `core/utils/implementations/hardware_info.py` | ✅ SECURE | ✅ FOUND | 15 | **19%** / 0% | 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `core/utils/interfaces/hardware_interface.py` | ✅ SECURE | ✅ FOUND | 3 | 100% / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | - |

---

### 2. Input Layer (`neural_ai/collectors/`)

| Modul / Fájl | Státusz | Teszt Pár | Tesztek | Cov (Stmt/Brch) | Lint/Type | Config | Logger | Teendők |
|--------------|---------|-----------|---------|-----------------|-----------|--------|--------|---------|
| `collectors/jforex/exceptions/jforex_error.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | 100% / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `collectors/jforex/factory.py` | ✅ SECURE | ✅ FOUND | 10 | **19%** / 0% | 0 / **12** | ⚪ N/A | ⚪ N/A | - |
| `collectors/jforex/implementations/bi5_downloader.py` | 🟡 WARNING | ✅ FOUND | 33 | **8%** / 0% | 0 / 0 | ⚪ N/A | ⚠️ UNUSED | - |
| `collectors/jforex/implementations/live_feed.py` | ✅ SECURE | ✅ FOUND | 3 | **13%** / 0% | 0 / 0 | ⚪ N/A | ✅ OK | - |
| `collectors/jforex/interfaces/downloader_interface.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | **75%** / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `collectors/jforex/interfaces/live_interface.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | **73%** / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `collectors/jforex/interfaces/tick_data.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | 88% / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |

---

### 3. Persistence Layer (`neural_ai/data/`)

| Modul / Fájl | Státusz | Teszt Pár | Tesztek | Cov (Stmt/Brch) | Lint/Type | Config | Logger | Teendők |
|--------------|---------|-----------|---------|-----------------|-----------|--------|--------|---------|
| `data/ingestion/market_data_persister.py` | ✅ SECURE | ✅ FOUND | 5 | **7%** / 0% | 0 / **6** | ⚪ N/A | ✅ OK | - |
| `data/storage/backends/base.py` | 🟡 WARNING | ✅ FOUND | 8 | **32%** / 6% | 0 / 0 | ⚪ N/A | ⚠️ UNUSED | - |
| `data/storage/backends/pandas_backend.py` | 🟡 WARNING | ✅ FOUND | 30 | **19%** / 3% | 0 / 0 | ⚪ N/A | ⚠️ UNUSED | - |
| `data/storage/backends/polars_backend.py` | 🟡 WARNING | ✅ FOUND | 30 | **16%** / 2% | 0 / 0 | ⚪ N/A | ⚠️ UNUSED | - |
| `data/storage/factory.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | **28%** / 0% | 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `data/storage/implementations/file_storage.py` | ✅ SECURE | ✅ FOUND | 52 | **11%** / 0% | 0 / **5** | ⚪ N/A | ✅ OK | - |
| `data/storage/implementations/parquet_storage.py` | ✅ SECURE | ✅ FOUND | 19 | **12%** / 0% | 0 / **1** | ✅ OK | ✅ OK | - |
| `data/storage/interfaces/factory_interface.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | 83% / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `data/storage/interfaces/storage_interface.py` | ✅ SECURE | ✅ FOUND | 11 | 100% / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | - |

---

### 4. Domain Layer (`neural_ai/processors/`)

| Modul / Fájl | Státusz | Teszt Pár | Tesztek | Cov (Stmt/Brch) | Lint/Type | Config | Logger | Teendők |
|--------------|---------|-----------|---------|-----------------|-----------|--------|--------|---------|
| `processors/dimensions/base.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | **47%** / 0% | 0 / 0 | ⚪ N/A | ✅ OK | **KRITIKUS: Teszt írás!** |
| `processors/dimensions/d01_price/factory.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | 86% / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `processors/dimensions/d01_price/processor.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | **8%** / 0% | 0 / 0 | ⚪ N/A | ✅ OK | **KRITIKUS: Teszt írás!** |
| `processors/dimensions/d02_support/exceptions/support_error.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | N/A | 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `processors/dimensions/d02_support/factory.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | 86% / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `processors/dimensions/d02_support/implementations/support_processor.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | **6%** / 0% | 0 / **9** | ⚪ N/A | ✅ OK | **KRITIKUS: Teszt írás!** |
| `processors/factory.py` | ✅ SECURE | ✅ FOUND | 3 | **37%** / 0% | 0 / **2** | ⚪ N/A | ⚪ N/A | - |
| `processors/implementations/time_alignment_service.py` | 🟡 WARNING | ✅ FOUND | 8 | **18%** / 0% | 0 / **2** | ⚪ N/A | ⚠️ UNUSED | - |
| `processors/interfaces/dimension_processor_interface.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | 80% / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `processors/interfaces/tensor_converter_interface.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | N/A | 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `processors/interfaces/time_alignment_interface.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | **78%** / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `processors/resampler_service/exceptions/resampler_error.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | **41%** / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `processors/resampler_service/factory.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | **39%** / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `processors/resampler_service/implementations/resampler_service.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | **12%** / 0% | 0 / **2** | ⚪ N/A | ⚠️ UNUSED | **KRITIKUS: Teszt írás!** |
| `processors/resampler_service/interfaces/resampler_interface.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | 86% / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |

---

### 5. Presentation Layer (`neural_ai/ui/`)

| Modul / Fájl | Státusz | Teszt Pár | Tesztek | Cov (Stmt/Brch) | Lint/Type | Config | Logger | Teendők |
|--------------|---------|-----------|---------|-----------------|-----------|--------|--------|---------|
| `ui/app.py` | 🟡 WARNING | ✅ FOUND | 15 | **34%** / 0% | 0 / 0 | ⚪ N/A | ⚠️ UNUSED | - |
| `ui/components/base_widget.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | N/A | 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `ui/core_bridge.py` | ✅ SECURE | ✅ FOUND | 21 | **14%** / 0% | 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `ui/factory.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | **15%** / 0% | 0 / **17** | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `ui/interfaces/ai_service_interface.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | 100% / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `ui/interfaces/core_bridge_interface.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | 100% / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `ui/interfaces/dashboard_service_interface.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | 100% / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `ui/interfaces/data_service_interface.py` | ✅ SECURE | ✅ FOUND | 17 | 100% / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | - |
| `ui/interfaces/live_ops_service_interface.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | 100% / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `ui/interfaces/navigation_service_interface.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | 100% / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `ui/interfaces/page_interface.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | 100% / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `ui/interfaces/strategy_service_interface.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | 100% / 100% | 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `ui/pages/01_🚀_Launchpad.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | **24%** / 50% | 0 / 0 | ⚪ N/A | ⚠️ UNUSED | **KRITIKUS: Teszt írás!** |
| `ui/pages/02_🛠️_Dev_Center.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | N/A | 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `ui/pages/03_📥_Data_Hub.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | **9%** / 2% | 0 / **1** | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `ui/pages/04_🧠_AI_Lab.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | N/A | 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `ui/pages/05_🪲_Strategy_Lab.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | **6%** / 1% | 0 / **15** | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `ui/pages/06_⚡_Live_Ops.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | N/A | 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |
| `ui/services/ai_service.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | **17%** / 0% | 0 / 0 | ⚪ N/A | ⚠️ UNUSED | **KRITIKUS: Teszt írás!** |
| `ui/services/dashboard_service.py` | 🟡 WARNING | ✅ FOUND | 13 | **17%** / 0% | 0 / **1** | ⚪ N/A | ⚠️ UNUSED | - |
| `ui/services/data_service.py` | 🟡 WARNING | ✅ FOUND | 24 | **8%** / 0% | 0 / **6** | ⚪ N/A | ⚠️ UNUSED | - |
| `ui/services/live_ops_service.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | **18%** / 0% | 0 / 0 | ⚪ N/A | ⚠️ UNUSED | **KRITIKUS: Teszt írás!** |
| `ui/services/navigation_service.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | **20%** / 0% | 0 / 0 | ⚪ N/A | ⚠️ UNUSED | **KRITIKUS: Teszt írás!** |
| `ui/services/strategy_service.py` | 🟡 WARNING | ✅ FOUND | 13 | **8%** / 0% | 0 / **8** | ⚪ N/A | ⚠️ UNUSED | - |
| `ui/streamlit_app.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | N/A | 0 / 0 | ⚪ N/A | ⚪ N/A | **KRITIKUS: Teszt írás!** |

---
