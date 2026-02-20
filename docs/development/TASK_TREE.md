# 🌳 NEURAL AI NEXT - TASK TREE

**Generálva:** 2026-02-20 19:02:41 UTC
**Módszer:** Hibrid (AST + Pytest + Coverage + Ruff + Mypy + Pylance)
**Fájlok száma:** 0

## 📊 Statisztika

- ✅ **SECURE:** 0 (0.0%)
- 🟡 **WARNING:** 0 (0.0%)
- 🔴 **VULNERABLE:** 0 (0.0%)

---

## Root Layer

| Modul / Fájl | Státusz | Teszt Pár | Teendők |
|:-------------|:--------|:----------|:--------|
| `__init__.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |

## Infrastructure Layer

| Modul / Fájl | Státusz | Teszt Pár | Teendők |
|:-------------|:--------|:----------|:--------|
| `core/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/base/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/base/exceptions/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/base/exceptions/base_error.py` | 🟡 WARNING | ✅ FOUND | 📝 Dokumentáció írása (docs/components/) |
| `core/base/factory.py` | 🟡 WARNING | ✅ FOUND | 📝 Dokumentáció írása (docs/components/) |
| `core/base/implementations/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/base/implementations/component_bundle.py` | 🟡 WARNING | ✅ FOUND | 📝 Dokumentáció írása (docs/components/) |
| `core/base/implementations/di_container.py` | 🟡 WARNING | ✅ FOUND | 📝 Dokumentáció írása (docs/components/) |
| `core/base/implementations/lazy_loader.py` | 🟡 WARNING | ✅ FOUND | 📝 Dokumentáció írása (docs/components/) |
| `core/base/implementations/singleton.py` | 🟡 WARNING | ✅ FOUND | 📝 Dokumentáció írása (docs/components/) |
| `core/base/interfaces/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/base/interfaces/component_interface.py` | 🟡 WARNING | ✅ FOUND | 📝 Dokumentáció írása (docs/components/) |
| `core/base/interfaces/container_interface.py` | 🟡 WARNING | ✅ FOUND | 📝 Dokumentáció írása (docs/components/) |
| `core/config/__init__.py` | 🟡 WARNING | ✅ FOUND | 📝 Dokumentáció írása (docs/components/) |
| `core/config/exceptions/__init__.py` | 🟡 WARNING | ✅ FOUND | 📝 Dokumentáció írása (docs/components/) |
| `core/config/exceptions/config_error.py` | 🟡 WARNING | ✅ FOUND | 📝 Dokumentáció írása (docs/components/) |
| `core/config/factory.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/config/implementations/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/config/implementations/dynamic_config_manager.py` | 🟡 WARNING | ✅ FOUND | 📝 Dokumentáció írása (docs/components/) |
| `core/config/implementations/yaml_config_manager.py` | 🟡 WARNING | ✅ FOUND | 📝 Dokumentáció írása (docs/components/) |
| `core/config/interfaces/__init__.py` | 🟡 WARNING | ✅ FOUND | 📝 Dokumentáció írása (docs/components/) |
| `core/config/interfaces/async_config_interface.py` | 🟡 WARNING | ✅ FOUND | 📝 Dokumentáció írása (docs/components/) |
| `core/config/interfaces/config_interface.py` | 🟡 WARNING | ✅ FOUND | 📝 Dokumentáció írása (docs/components/) |
| `core/config/interfaces/factory_interface.py` | 🟡 WARNING | ✅ FOUND | 📝 Dokumentáció írása (docs/components/) |
| `core/config/interfaces/types.py` | 🟡 WARNING | ✅ FOUND | 📝 Dokumentáció írása (docs/components/) |
| `core/db/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/db/exceptions/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/db/exceptions/db_error.py` | 🟡 WARNING | ✅ FOUND | 📝 Dokumentáció írása (docs/components/) |
| `core/db/factory.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/db/implementations/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/db/implementations/model_base.py` | 🟡 WARNING | ✅ FOUND | 📝 Dokumentáció írása (docs/components/) |
| `core/db/implementations/models.py` | 🟡 WARNING | ✅ FOUND | 📝 Dokumentáció írása (docs/components/) |
| `core/db/implementations/sqlalchemy_session.py` | 🟡 WARNING | ✅ FOUND | 📝 Dokumentáció írása (docs/components/) |
| `core/db/interfaces/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/events/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/events/exceptions/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/events/exceptions/event_error.py` | 🟡 WARNING | ✅ FOUND | 📝 Dokumentáció írása (docs/components/) |
| `core/events/factory.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/events/implementations/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/events/implementations/zeromq_bus.py` | 🟡 WARNING | ✅ FOUND | 📝 Dokumentáció írása (docs/components/) |
| `core/events/interfaces/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/events/interfaces/event_bus_interface.py` | 🟡 WARNING | ✅ FOUND | 📝 Dokumentáció írása (docs/components/) |
| `core/events/interfaces/event_models.py` | 🟡 WARNING | ✅ FOUND | 📝 Dokumentáció írása (docs/components/) |
| `core/logger/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/logger/exceptions/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/logger/exceptions/logger_error.py` | 🟡 WARNING | ✅ FOUND | 📝 Dokumentáció írása (docs/components/) |
| `core/logger/factory.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/logger/formatters/logger_formatters.py` | 🟡 WARNING | ✅ FOUND | 📝 Dokumentáció írása (docs/components/) |
| `core/logger/implementations/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/logger/implementations/colored_logger.py` | 🟡 WARNING | ✅ FOUND | 📝 Dokumentáció írása (docs/components/) |
| `core/logger/implementations/default_logger.py` | 🟡 WARNING | ✅ FOUND | 📝 Dokumentáció írása (docs/components/) |
| `core/logger/implementations/rotating_file_logger.py` | 🟡 WARNING | ✅ FOUND | 📝 Dokumentáció írása (docs/components/) |
| `core/logger/interfaces/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/logger/interfaces/factory_interface.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/logger/interfaces/logger_interface.py` | 🟡 WARNING | ✅ FOUND | 📝 Dokumentáció írása (docs/components/) |
| `core/system/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/system/exceptions/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/system/exceptions/health_error.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/system/factory.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/system/implementations/health_monitor.py` | 🟡 WARNING | ✅ FOUND | 📝 Dokumentáció írása (docs/components/) |
| `core/system/interfaces/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/system/interfaces/health_interface.py` | 🟡 WARNING | ✅ FOUND | 📝 Dokumentáció írása (docs/components/) |
| `core/utils/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/utils/decorators.py` | 🟡 WARNING | ✅ FOUND | 📝 Dokumentáció írása (docs/components/) |
| `core/utils/exceptions/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/utils/exceptions/util_error.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/utils/factory.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/utils/implementations/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/utils/implementations/hardware_info.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/utils/interfaces/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/utils/interfaces/hardware_interface.py` | 🟡 WARNING | ✅ FOUND | 📝 Dokumentáció írása (docs/components/) |

## Input Layer

| Modul / Fájl | Státusz | Teszt Pár | Teendők |
|:-------------|:--------|:----------|:--------|
| `collectors/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `collectors/jforex/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `collectors/jforex/exceptions/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `collectors/jforex/exceptions/jforex_error.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `collectors/jforex/factory.py` | 🟡 WARNING | ✅ FOUND | 📝 Dokumentáció írása (docs/components/) |
| `collectors/jforex/implementations/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `collectors/jforex/implementations/bi5_downloader.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `collectors/jforex/implementations/live_feed.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `collectors/jforex/interfaces/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `collectors/jforex/interfaces/downloader_interface.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `collectors/jforex/interfaces/live_interface.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `collectors/jforex/interfaces/tick_data.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |

## Persistence Layer

| Modul / Fájl | Státusz | Teszt Pár | Teendők |
|:-------------|:--------|:----------|:--------|
| `data/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `data/ingestion/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `data/ingestion/market_data_persister.py` | 🟡 WARNING | ✅ FOUND | 📝 Dokumentáció írása (docs/components/) |
| `data/storage/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `data/storage/backends/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `data/storage/backends/base.py` | 🟡 WARNING | ✅ FOUND | 📝 Dokumentáció írása (docs/components/) |
| `data/storage/backends/pandas_backend.py` | 🟡 WARNING | ✅ FOUND | 📝 Dokumentáció írása (docs/components/) |
| `data/storage/backends/polars_backend.py` | 🟡 WARNING | ✅ FOUND | 📝 Dokumentáció írása (docs/components/) |
| `data/storage/exceptions/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `data/storage/factory.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `data/storage/implementations/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `data/storage/implementations/file_storage.py` | 🟡 WARNING | ✅ FOUND | 📝 Dokumentáció írása (docs/components/) |
| `data/storage/implementations/parquet_storage.py` | 🟡 WARNING | ✅ FOUND | 📝 Dokumentáció írása (docs/components/) |
| `data/storage/interfaces/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `data/storage/interfaces/factory_interface.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `data/storage/interfaces/storage_interface.py` | 🟡 WARNING | ✅ FOUND | 📝 Dokumentáció írása (docs/components/) |

## Domain Layer

| Modul / Fájl | Státusz | Teszt Pár | Teendők |
|:-------------|:--------|:----------|:--------|
| `processors/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `processors/dimensions/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `processors/dimensions/base.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `processors/dimensions/d01_price/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `processors/dimensions/d01_price/factory.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `processors/dimensions/d01_price/processor.py` | 🟡 WARNING | ✅ FOUND | 📝 Dokumentáció írása (docs/components/) |
| `processors/dimensions/d02_support/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `processors/dimensions/d02_support/exceptions/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `processors/dimensions/d02_support/exceptions/support_error.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `processors/dimensions/d02_support/factory.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `processors/dimensions/d02_support/implementations/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `processors/dimensions/d02_support/implementations/support_processor.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `processors/dimensions/d02_support/interfaces/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `processors/factory.py` | 🟡 WARNING | ✅ FOUND | 📝 Dokumentáció írása (docs/components/) |
| `processors/implementations/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `processors/implementations/time_alignment_service.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `processors/interfaces/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `processors/interfaces/dimension_processor_interface.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `processors/interfaces/tensor_converter_interface.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `processors/interfaces/time_alignment_interface.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `processors/resampler_service/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `processors/resampler_service/exceptions/resampler_error.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `processors/resampler_service/factory.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `processors/resampler_service/implementations/resampler_service.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `processors/resampler_service/interfaces/resampler_interface.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |

## Presentation Layer

| Modul / Fájl | Státusz | Teszt Pár | Teendők |
|:-------------|:--------|:----------|:--------|
| `ui/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `ui/app.py` | 🟡 WARNING | ✅ FOUND | 📝 Dokumentáció írása (docs/components/) |
| `ui/components/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `ui/components/base_widget.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `ui/core_bridge.py` | 🟡 WARNING | ✅ FOUND | 📝 Dokumentáció írása (docs/components/) |
| `ui/factory.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `ui/interfaces/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `ui/interfaces/ai_service_interface.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `ui/interfaces/core_bridge_interface.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `ui/interfaces/dashboard_service_interface.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `ui/interfaces/data_service_interface.py` | 🟡 WARNING | ✅ FOUND | 📝 Dokumentáció írása (docs/components/) |
| `ui/interfaces/live_ops_service_interface.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `ui/interfaces/navigation_service_interface.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `ui/interfaces/page_interface.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `ui/interfaces/strategy_service_interface.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `ui/pages/01_🚀_Launchpad.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `ui/pages/02_🛠️_Dev_Center.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `ui/pages/03_📥_Data_Hub.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `ui/pages/04_🧠_AI_Lab.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `ui/pages/05_🪲_Strategy_Lab.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `ui/pages/06_⚡_Live_Ops.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `ui/pages/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `ui/services/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `ui/services/ai_service.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `ui/services/dashboard_service.py` | 🟡 WARNING | ✅ FOUND | 📝 Dokumentáció írása (docs/components/) |
| `ui/services/data_service.py` | 🟡 WARNING | ✅ FOUND | 📝 Dokumentáció írása (docs/components/) |
| `ui/services/live_ops_service.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `ui/services/navigation_service.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `ui/services/strategy_service.py` | 🟡 WARNING | ✅ FOUND | 📝 Dokumentáció írása (docs/components/) |
| `ui/streamlit_app.py` | 🔴 VULNERABLE | ❌ MISSING | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
