# 🌳 NEURAL AI NEXT - TASK TREE v3.0 (DEEP AUDIT)

**Generálva:** 2026-02-05 10:36:01 UTC
**Módszer:** AST Statikus Analízis
**Fájlok száma:** 99 elemezve

---

## 📊 ÖSSZESÍTŐ STATISZTIKA

- **✅ SECURE**: 32 fájl (32.3%)
- **🟡 WARNING**: 12 fájl (12.1%)
- **🔴 VULNERABLE**: 55 fájl (55.6%)
- **Teszt lefedettség**: 47/99 fájl (47.5%)

---

## 📂 RÉSZLETES AUDIT EREDMÉNYEK (DDD RÉTEGEK)

### 1. Infrastructure Layer (`neural_ai/core/`)

| Modul / Fájl | Státusz | Teszt Pár | Tesztek Száma | Config (Pydantic) | Logger (DI) | Coverage | Teendők / Megjegyzés |
|--------------|---------|-----------|---------------|-------------------|-------------|----------|----------------------|
| `core/base/exceptions/base_error.py` | ✅ SECURE | ✅ FOUND | 42 | ⚪ N/A | ⚪ N/A | N/A | - |
| `core/base/factory.py` | ✅ SECURE | ✅ FOUND | 35 | ✅ OK | ⚪ N/A | N/A | - |
| `core/base/implementations/component_bundle.py` | ✅ SECURE | ✅ FOUND | 39 | ⚪ N/A | ⚪ N/A | N/A | - |
| `core/base/implementations/di_container.py` | ✅ SECURE | ✅ FOUND | 24 | ⚪ N/A | ⚪ N/A | N/A | - |
| `core/base/implementations/lazy_loader.py` | ✅ SECURE | ✅ FOUND | 10 | ⚪ N/A | ⚪ N/A | N/A | - |
| `core/base/implementations/singleton.py` | ✅ SECURE | ✅ FOUND | 10 | ⚪ N/A | ⚪ N/A | N/A | - |
| `core/base/interfaces/component_interface.py` | ✅ SECURE | ✅ FOUND | 13 | ⚪ N/A | ⚪ N/A | N/A | - |
| `core/base/interfaces/container_interface.py` | ✅ SECURE | ✅ FOUND | 20 | ⚪ N/A | ⚪ N/A | N/A | - |
| `core/config/exceptions/config_error.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | ⚪ N/A | ⚪ N/A | N/A | **KRITIKUS: Teszt írás!** |
| `core/config/factory.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | ⚪ N/A | ⚪ N/A | N/A | **KRITIKUS: Teszt írás!** |
| `core/config/implementations/dynamic_config_manager.py` | 🟡 WARNING | ✅ FOUND | 13 | ⚪ N/A | ⚠️ UNUSED | N/A | - |
| `core/config/implementations/yaml_config_manager.py` | 🟡 WARNING | ✅ FOUND | 65 | ⚪ N/A | ⚠️ UNUSED | N/A | - |
| `core/config/interfaces/async_config_interface.py` | 🟡 WARNING | ✅ FOUND | 11 | ⚪ N/A | ⚠️ UNUSED | N/A | - |
| `core/config/interfaces/config_interface.py` | ✅ SECURE | ✅ FOUND | 17 | ⚪ N/A | ⚪ N/A | N/A | - |
| `core/config/interfaces/factory_interface.py` | ✅ SECURE | ✅ FOUND | 23 | ⚪ N/A | ⚪ N/A | N/A | - |
| `core/config/interfaces/types.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | ✅ OK | ⚪ N/A | N/A | **KRITIKUS: Teszt írás!** |
| `core/db/exceptions/db_error.py` | ✅ SECURE | ✅ FOUND | 9 | ⚪ N/A | ⚪ N/A | N/A | - |
| `core/db/factory.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | ⚪ N/A | ⚠️ UNUSED | N/A | **KRITIKUS: Teszt írás!** |
| `core/db/implementations/model_base.py` | ✅ SECURE | ✅ FOUND | 12 | ⚪ N/A | ⚪ N/A | N/A | - |
| `core/db/implementations/models.py` | ✅ SECURE | ✅ FOUND | 22 | ⚪ N/A | ⚪ N/A | N/A | - |
| `core/db/implementations/sqlalchemy_session.py` | ✅ SECURE | ✅ FOUND | 10 | ⚪ N/A | ✅ OK | N/A | - |
| `core/events/exceptions/event_error.py` | ✅ SECURE | ✅ FOUND | 9 | ⚪ N/A | ⚪ N/A | N/A | - |
| `core/events/factory.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | ⚪ N/A | ⚠️ UNUSED | N/A | **KRITIKUS: Teszt írás!** |
| `core/events/implementations/zeromq_bus.py` | 🟡 WARNING | ✅ FOUND | 17 | ✅ OK | ⚠️ UNUSED | N/A | - |
| `core/events/interfaces/event_bus_interface.py` | ✅ SECURE | ✅ FOUND | 27 | ✅ OK | ⚪ N/A | N/A | - |
| `core/events/interfaces/event_models.py` | ✅ SECURE | ✅ FOUND | 26 | ✅ OK | ⚪ N/A | N/A | - |
| `core/logger/exceptions/logger_error.py` | ✅ SECURE | ✅ FOUND | 14 | ⚪ N/A | ⚪ N/A | N/A | - |
| `core/logger/factory.py` | ✅ SECURE | ✅ FOUND | 5 | ⚪ N/A | ⚪ N/A | N/A | - |
| `core/logger/formatters/logger_formatters.py` | ✅ SECURE | ✅ FOUND | 6 | ⚪ N/A | ⚪ N/A | N/A | - |
| `core/logger/implementations/colored_logger.py` | 🔴 VULNERABLE | ✅ FOUND | 12 | ⚪ N/A | 🔴 MISSING | N/A | **Logger DI hiányzik!** |
| `core/logger/implementations/default_logger.py` | 🔴 VULNERABLE | ✅ FOUND | 9 | ⚪ N/A | 🔴 MISSING | N/A | **Logger DI hiányzik!** |
| `core/logger/implementations/rotating_file_logger.py` | 🔴 VULNERABLE | ✅ FOUND | 22 | ⚪ N/A | 🔴 MISSING | N/A | **Logger DI hiányzik!** |
| `core/logger/interfaces/factory_interface.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | ⚪ N/A | ⚪ N/A | N/A | **KRITIKUS: Teszt írás!** |
| `core/logger/interfaces/logger_interface.py` | ✅ SECURE | ✅ FOUND | 3 | ⚪ N/A | ⚪ N/A | N/A | - |
| `core/system/exceptions/health_error.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | ⚪ N/A | ⚪ N/A | N/A | **KRITIKUS: Teszt írás!** |
| `core/system/factory.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | ⚪ N/A | ⚪ N/A | N/A | **KRITIKUS: Teszt írás!** |
| `core/system/implementations/health_monitor.py` | 🟡 WARNING | ✅ FOUND | 9 | ⚪ N/A | ⚠️ UNUSED | N/A | - |
| `core/system/interfaces/health_interface.py` | ✅ SECURE | ✅ FOUND | 22 | ⚪ N/A | ⚪ N/A | N/A | - |
| `core/utils/decorators.py` | ✅ SECURE | ✅ FOUND | 13 | ⚪ N/A | ⚪ N/A | N/A | - |
| `core/utils/exceptions/util_error.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | ⚪ N/A | ⚪ N/A | N/A | **KRITIKUS: Teszt írás!** |
| `core/utils/factory.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | ⚪ N/A | ⚪ N/A | N/A | **KRITIKUS: Teszt írás!** |
| `core/utils/implementations/hardware_info.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | ⚪ N/A | ⚪ N/A | N/A | **KRITIKUS: Teszt írás!** |
| `core/utils/interfaces/hardware_interface.py` | ✅ SECURE | ✅ FOUND | 3 | ⚪ N/A | ⚪ N/A | N/A | - |

---

### 2. Input Layer (`neural_ai/collectors/`)

| Modul / Fájl | Státusz | Teszt Pár | Tesztek Száma | Config (Pydantic) | Logger (DI) | Coverage | Teendők / Megjegyzés |
|--------------|---------|-----------|---------------|-------------------|-------------|----------|----------------------|
| `collectors/jforex/exceptions/jforex_error.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | ⚪ N/A | ⚪ N/A | N/A | **KRITIKUS: Teszt írás!** |
| `collectors/jforex/factory.py` | ✅ SECURE | ✅ FOUND | 4 | ⚪ N/A | ⚪ N/A | N/A | - |
| `collectors/jforex/implementations/bi5_downloader.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | ⚪ N/A | ⚠️ UNUSED | N/A | **KRITIKUS: Teszt írás!** |
| `collectors/jforex/implementations/live_feed.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | ⚪ N/A | ✅ OK | N/A | **KRITIKUS: Teszt írás!** |
| `collectors/jforex/interfaces/downloader_interface.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | ⚪ N/A | ⚪ N/A | N/A | **KRITIKUS: Teszt írás!** |
| `collectors/jforex/interfaces/live_interface.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | ⚪ N/A | ⚪ N/A | N/A | **KRITIKUS: Teszt írás!** |
| `collectors/jforex/interfaces/tick_data.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | ⚪ N/A | ⚪ N/A | N/A | **KRITIKUS: Teszt írás!** |

---

### 3. Persistence Layer (`neural_ai/data/`)

| Modul / Fájl | Státusz | Teszt Pár | Tesztek Száma | Config (Pydantic) | Logger (DI) | Coverage | Teendők / Megjegyzés |
|--------------|---------|-----------|---------------|-------------------|-------------|----------|----------------------|
| `data/ingestion/market_data_persister.py` | ✅ SECURE | ✅ FOUND | 5 | ⚪ N/A | ✅ OK | N/A | - |
| `data/storage/backends/base.py` | 🟡 WARNING | ✅ FOUND | 8 | ⚪ N/A | ⚠️ UNUSED | N/A | - |
| `data/storage/backends/pandas_backend.py` | 🟡 WARNING | ✅ FOUND | 30 | ⚪ N/A | ⚠️ UNUSED | N/A | - |
| `data/storage/backends/polars_backend.py` | 🟡 WARNING | ✅ FOUND | 30 | ⚪ N/A | ⚠️ UNUSED | N/A | - |
| `data/storage/factory.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | ⚪ N/A | ⚪ N/A | N/A | **KRITIKUS: Teszt írás!** |
| `data/storage/implementations/file_storage.py` | ✅ SECURE | ✅ FOUND | 52 | ⚪ N/A | ✅ OK | N/A | - |
| `data/storage/implementations/parquet_storage.py` | ✅ SECURE | ✅ FOUND | 19 | ✅ OK | ✅ OK | N/A | - |
| `data/storage/interfaces/factory_interface.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | ⚪ N/A | ⚪ N/A | N/A | **KRITIKUS: Teszt írás!** |
| `data/storage/interfaces/storage_interface.py` | ✅ SECURE | ✅ FOUND | 11 | ⚪ N/A | ⚪ N/A | N/A | - |

---

### 4. Domain Layer (`neural_ai/processors/`)

| Modul / Fájl | Státusz | Teszt Pár | Tesztek Száma | Config (Pydantic) | Logger (DI) | Coverage | Teendők / Megjegyzés |
|--------------|---------|-----------|---------------|-------------------|-------------|----------|----------------------|
| `processors/dimensions/base.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | ⚪ N/A | ✅ OK | N/A | **KRITIKUS: Teszt írás!** |
| `processors/dimensions/d01_price/factory.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | ⚪ N/A | ⚪ N/A | N/A | **KRITIKUS: Teszt írás!** |
| `processors/dimensions/d01_price/processor.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | ⚪ N/A | ✅ OK | N/A | **KRITIKUS: Teszt írás!** |
| `processors/dimensions/d02_support/exceptions/support_error.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | ⚪ N/A | ⚪ N/A | N/A | **KRITIKUS: Teszt írás!** |
| `processors/dimensions/d02_support/factory.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | ⚪ N/A | ⚪ N/A | N/A | **KRITIKUS: Teszt írás!** |
| `processors/dimensions/d02_support/implementations/support_processor.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | ⚪ N/A | ✅ OK | N/A | **KRITIKUS: Teszt írás!** |
| `processors/factory.py` | ✅ SECURE | ✅ FOUND | 3 | ⚪ N/A | ⚪ N/A | N/A | - |
| `processors/implementations/time_alignment_service.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | ⚪ N/A | ⚠️ UNUSED | N/A | **KRITIKUS: Teszt írás!** |
| `processors/interfaces/dimension_processor_interface.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | ⚪ N/A | ⚪ N/A | N/A | **KRITIKUS: Teszt írás!** |
| `processors/interfaces/tensor_converter_interface.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | ⚪ N/A | ⚪ N/A | N/A | **KRITIKUS: Teszt írás!** |
| `processors/interfaces/time_alignment_interface.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | ⚪ N/A | ⚪ N/A | N/A | **KRITIKUS: Teszt írás!** |
| `processors/resampler_service/exceptions/resampler_error.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | ⚪ N/A | ⚪ N/A | N/A | **KRITIKUS: Teszt írás!** |
| `processors/resampler_service/factory.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | ⚪ N/A | ⚪ N/A | N/A | **KRITIKUS: Teszt írás!** |
| `processors/resampler_service/implementations/resampler_service.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | ⚪ N/A | ⚠️ UNUSED | N/A | **KRITIKUS: Teszt írás!** |
| `processors/resampler_service/interfaces/resampler_interface.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | ⚪ N/A | ⚪ N/A | N/A | **KRITIKUS: Teszt írás!** |

---

### 5. Presentation Layer (`neural_ai/ui/`)

| Modul / Fájl | Státusz | Teszt Pár | Tesztek Száma | Config (Pydantic) | Logger (DI) | Coverage | Teendők / Megjegyzés |
|--------------|---------|-----------|---------------|-------------------|-------------|----------|----------------------|
| `ui/app.py` | 🟡 WARNING | ✅ FOUND | 15 | ⚪ N/A | ⚠️ UNUSED | N/A | - |
| `ui/components/base_widget.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | ⚪ N/A | ⚪ N/A | N/A | **KRITIKUS: Teszt írás!** |
| `ui/core_bridge.py` | ✅ SECURE | ✅ FOUND | 21 | ⚪ N/A | ⚪ N/A | N/A | - |
| `ui/factory.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | 🔴 TYPED_DICT | ⚪ N/A | N/A | **KRITIKUS: Teszt írás!** | **Migráld Pydantic-ra!** |
| `ui/interfaces/ai_service_interface.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | ⚪ N/A | ⚪ N/A | N/A | **KRITIKUS: Teszt írás!** |
| `ui/interfaces/core_bridge_interface.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | ⚪ N/A | ⚪ N/A | N/A | **KRITIKUS: Teszt írás!** |
| `ui/interfaces/dashboard_service_interface.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | ⚪ N/A | ⚪ N/A | N/A | **KRITIKUS: Teszt írás!** |
| `ui/interfaces/data_service_interface.py` | ✅ SECURE | ✅ FOUND | 17 | ⚪ N/A | ⚪ N/A | N/A | - |
| `ui/interfaces/live_ops_service_interface.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | ⚪ N/A | ⚪ N/A | N/A | **KRITIKUS: Teszt írás!** |
| `ui/interfaces/navigation_service_interface.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | ⚪ N/A | ⚪ N/A | N/A | **KRITIKUS: Teszt írás!** |
| `ui/interfaces/page_interface.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | ⚪ N/A | ⚪ N/A | N/A | **KRITIKUS: Teszt írás!** |
| `ui/interfaces/strategy_service_interface.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | ⚪ N/A | ⚪ N/A | N/A | **KRITIKUS: Teszt írás!** |
| `ui/pages/01_🚀_Launchpad.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | ⚪ N/A | ⚠️ UNUSED | N/A | **KRITIKUS: Teszt írás!** |
| `ui/pages/02_🛠️_Dev_Center.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | ⚪ N/A | ⚪ N/A | N/A | **KRITIKUS: Teszt írás!** |
| `ui/pages/03_📥_Data_Hub.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | ⚪ N/A | ⚪ N/A | N/A | **KRITIKUS: Teszt írás!** |
| `ui/pages/04_🧠_AI_Lab.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | ⚪ N/A | ⚪ N/A | N/A | **KRITIKUS: Teszt írás!** |
| `ui/pages/05_🪲_Strategy_Lab.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | ⚪ N/A | ⚪ N/A | N/A | **KRITIKUS: Teszt írás!** |
| `ui/pages/06_⚡_Live_Ops.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | ⚪ N/A | ⚪ N/A | N/A | **KRITIKUS: Teszt írás!** |
| `ui/services/ai_service.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | ⚪ N/A | ⚠️ UNUSED | N/A | **KRITIKUS: Teszt írás!** |
| `ui/services/dashboard_service.py` | 🟡 WARNING | ✅ FOUND | 14 | ⚪ N/A | ⚠️ UNUSED | N/A | - |
| `ui/services/data_service.py` | 🟡 WARNING | ✅ FOUND | 24 | ⚪ N/A | ⚠️ UNUSED | N/A | - |
| `ui/services/live_ops_service.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | ⚪ N/A | ⚠️ UNUSED | N/A | **KRITIKUS: Teszt írás!** |
| `ui/services/navigation_service.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | ⚪ N/A | ⚠️ UNUSED | N/A | **KRITIKUS: Teszt írás!** |
| `ui/services/strategy_service.py` | 🟡 WARNING | ✅ FOUND | 13 | ⚪ N/A | ⚠️ UNUSED | N/A | - |
| `ui/streamlit_app.py` | 🔴 VULNERABLE | ❌ MISSING | 0 | ⚪ N/A | ⚪ N/A | N/A | **KRITIKUS: Teszt írás!** |

---
