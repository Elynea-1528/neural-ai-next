# 🌳 NEURAL AI NEXT - TASK TREE

**Generálva:** 2026-07-10 20:07:56 UTC
**Módszer:** Hibrid (AST + Pytest + Coverage + Ruff + Mypy + Pylance)
**Fájlok száma:** 175

## 📊 Statisztika

- ✅ **PERFECT:** 0 (0.0%)
- 🟢 **STABLE:** 0 (0.0%)
- 🟡 **WIP:** 0 (0.0%)
- 🔴 **CRITICAL:** 175 (100.0%)

---

## 0. Root Layer (`./`)

| Modul / Fájl | Státusz | Teszt Pár | Pass/Fail/Err/Skip/Warn | Coverage (Stmt/Brch) | Lint/Mypy/Pylance | Src Warn | Config | Logger | Dokumentálva | Teendők |
|:-------------|:--------|:----------|:-------------------|:---------------------|:------------------|:---------|:-------|:-------|:-------------|:--------|
| `neural_ai/__init__.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ❌ | - |

## 1. Infrastructure Layer (`neural_ai/core/`)

| Modul / Fájl | Státusz | Teszt Pár | Pass/Fail/Err/Skip/Warn | Coverage (Stmt/Brch) | Lint/Mypy/Pylance | Src Warn | Config | Logger | Dokumentálva | Teendők |
|:-------------|:--------|:----------|:-------------------|:---------------------|:------------------|:---------|:-------|:-------|:-------------|:--------|
| `neural_ai/core/__init__.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ✅ OK | ❌ | - |
| `neural_ai/core/base/__init__.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/core/base/exceptions/__init__.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/core/base/exceptions/base_error.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/core/base/factory.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ✅ OK | ✅ OK | ❌ | - |
| `neural_ai/core/base/implementations/__init__.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/core/base/implementations/component_bundle.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ❌ | - |
| `neural_ai/core/base/implementations/di_container.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ✅ OK | ❌ | - |
| `neural_ai/core/base/implementations/lazy_loader.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ❌ | - |
| `neural_ai/core/base/implementations/singleton.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ❌ | - |
| `neural_ai/core/base/interfaces/__init__.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/core/base/interfaces/component_interface.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ❌ | - |
| `neural_ai/core/base/interfaces/container_interface.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/core/config/__init__.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/core/config/exceptions/__init__.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/core/config/exceptions/config_error.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/core/config/factory.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ✅ OK | ⚠️ UNUSED | ❌ | - |
| `neural_ai/core/config/implementations/__init__.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/core/config/implementations/dynamic_config_manager.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ❌ | - |
| `neural_ai/core/config/implementations/yaml_config_manager.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ✅ OK | ⚠️ UNUSED | ❌ | - |
| `neural_ai/core/config/interfaces/__init__.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/core/config/interfaces/async_config_interface.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ❌ | - |
| `neural_ai/core/config/interfaces/config_interface.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/core/config/interfaces/factory_interface.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/core/config/interfaces/types.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ✅ OK | ⚪ N/A | ❌ | - |
| `neural_ai/core/db/__init__.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/core/db/exceptions/__init__.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/core/db/exceptions/db_error.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/core/db/factory.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ❌ | - |
| `neural_ai/core/db/implementations/__init__.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/core/db/implementations/model_base.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/core/db/implementations/models.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/core/db/implementations/sqlalchemy_session.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ✅ OK | ❌ | - |
| `neural_ai/core/db/interfaces/__init__.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/core/events/__init__.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/core/events/exceptions/__init__.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/core/events/exceptions/event_error.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/core/events/factory.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ❌ | - |
| `neural_ai/core/events/implementations/__init__.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/core/events/implementations/zeromq_bus.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ✅ OK | ⚠️ UNUSED | ❌ | - |
| `neural_ai/core/events/interfaces/__init__.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/core/events/interfaces/event_bus_interface.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ✅ OK | ⚪ N/A | ❌ | - |
| `neural_ai/core/events/interfaces/event_models.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ✅ OK | ⚪ N/A | ❌ | - |
| `neural_ai/core/logger/__init__.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ❌ | - |
| `neural_ai/core/logger/exceptions/__init__.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ❌ | - |
| `neural_ai/core/logger/exceptions/logger_error.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/core/logger/factory.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ❌ | - |
| `neural_ai/core/logger/formatters/logger_formatters.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/core/logger/implementations/__init__.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/core/logger/implementations/colored_logger.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ❌ | - |
| `neural_ai/core/logger/implementations/default_logger.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ❌ | - |
| `neural_ai/core/logger/implementations/rotating_file_logger.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ❌ | - |
| `neural_ai/core/logger/interfaces/__init__.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ❌ | - |
| `neural_ai/core/logger/interfaces/factory_interface.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ❌ | - |
| `neural_ai/core/logger/interfaces/logger_interface.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/core/system/__init__.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/core/system/exceptions/__init__.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/core/system/exceptions/health_error.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/core/system/factory.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ❌ | - |
| `neural_ai/core/system/implementations/health_monitor.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ❌ | - |
| `neural_ai/core/system/interfaces/__init__.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/core/system/interfaces/health_interface.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/core/utils/__init__.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/core/utils/decorators.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ❌ | - |
| `neural_ai/core/utils/exceptions/__init__.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/core/utils/exceptions/util_error.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/core/utils/factory.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/core/utils/implementations/__init__.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/core/utils/implementations/hardware_info.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ❌ | - |
| `neural_ai/core/utils/interfaces/__init__.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/core/utils/interfaces/hardware_interface.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |

## 2. Input Layer (`neural_ai/collectors/`)

| Modul / Fájl | Státusz | Teszt Pár | Pass/Fail/Err/Skip/Warn | Coverage (Stmt/Brch) | Lint/Mypy/Pylance | Src Warn | Config | Logger | Dokumentálva | Teendők |
|:-------------|:--------|:----------|:-------------------|:---------------------|:------------------|:---------|:-------|:-------|:-------------|:--------|
| `neural_ai/collectors/__init__.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/collectors/jforex/__init__.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/collectors/jforex/exceptions/__init__.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/collectors/jforex/exceptions/jforex_error.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/collectors/jforex/factory.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ✅ OK | ✅ OK | ❌ | - |
| `neural_ai/collectors/jforex/implementations/__init__.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/collectors/jforex/implementations/bi5_downloader.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ❌ | - |
| `neural_ai/collectors/jforex/implementations/live_feed.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ❌ | - |
| `neural_ai/collectors/jforex/interfaces/__init__.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/collectors/jforex/interfaces/downloader_interface.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/collectors/jforex/interfaces/live_interface.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/collectors/jforex/interfaces/tick_data.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |

## 3. Persistence Layer (`neural_ai/data/`)

| Modul / Fájl | Státusz | Teszt Pár | Pass/Fail/Err/Skip/Warn | Coverage (Stmt/Brch) | Lint/Mypy/Pylance | Src Warn | Config | Logger | Dokumentálva | Teendők |
|:-------------|:--------|:----------|:-------------------|:---------------------|:------------------|:---------|:-------|:-------|:-------------|:--------|
| `neural_ai/data/__init__.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/data/ingestion/__init__.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/data/ingestion/market_data_persister.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ❌ | - |
| `neural_ai/data/storage/__init__.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ❌ | - |
| `neural_ai/data/storage/backends/__init__.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/data/storage/backends/base.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ❌ | - |
| `neural_ai/data/storage/backends/pandas_backend.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/data/storage/backends/polars_backend.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/data/storage/exceptions/__init__.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/data/storage/factory.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ✅ OK | ❌ | - |
| `neural_ai/data/storage/implementations/__init__.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/data/storage/implementations/file_storage.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ❌ | - |
| `neural_ai/data/storage/implementations/parquet_storage.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ✅ OK | ⚠️ UNUSED | ❌ | - |
| `neural_ai/data/storage/interfaces/__init__.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/data/storage/interfaces/factory_interface.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ❌ | - |
| `neural_ai/data/storage/interfaces/storage_interface.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |

## 4. Domain Layer (`neural_ai/processors/`)

| Modul / Fájl | Státusz | Teszt Pár | Pass/Fail/Err/Skip/Warn | Coverage (Stmt/Brch) | Lint/Mypy/Pylance | Src Warn | Config | Logger | Dokumentálva | Teendők |
|:-------------|:--------|:----------|:-------------------|:---------------------|:------------------|:---------|:-------|:-------|:-------------|:--------|
| `neural_ai/processors/__init__.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/processors/dimensions/__init__.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/processors/dimensions/base.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ❌ | - |
| `neural_ai/processors/dimensions/d01_price/__init__.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/processors/dimensions/d01_price/factory.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ❌ | - |
| `neural_ai/processors/dimensions/d01_price/processor.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ❌ | - |
| `neural_ai/processors/dimensions/d02_support/__init__.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/processors/dimensions/d02_support/exceptions/__init__.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/processors/dimensions/d02_support/exceptions/support_error.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/processors/dimensions/d02_support/factory.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ❌ | - |
| `neural_ai/processors/dimensions/d02_support/implementations/__init__.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/processors/dimensions/d02_support/implementations/support_processor.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ❌ | - |
| `neural_ai/processors/dimensions/d02_support/interfaces/__init__.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/processors/factory.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ✅ OK | ✅ OK | ❌ | - |
| `neural_ai/processors/implementations/__init__.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/processors/implementations/time_alignment_service.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ❌ | - |
| `neural_ai/processors/interfaces/__init__.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/processors/interfaces/dimension_processor_interface.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/processors/interfaces/tensor_converter_interface.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/processors/interfaces/time_alignment_interface.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/processors/resampler_service/__init__.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/processors/resampler_service/exceptions/resampler_error.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/processors/resampler_service/factory.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ❌ | - |
| `neural_ai/processors/resampler_service/implementations/resampler_service.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ❌ | - |
| `neural_ai/processors/resampler_service/interfaces/resampler_interface.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |

## 5. Presentation Layer (`neural_ai/ui/`)

| Modul / Fájl | Státusz | Teszt Pár | Pass/Fail/Err/Skip/Warn | Coverage (Stmt/Brch) | Lint/Mypy/Pylance | Src Warn | Config | Logger | Dokumentálva | Teendők |
|:-------------|:--------|:----------|:-------------------|:---------------------|:------------------|:---------|:-------|:-------|:-------------|:--------|
| `neural_ai/ui/__init__.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/ui/app.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ✅ OK | ❌ | - |
| `neural_ai/ui/components/__init__.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/ui/components/base_widget.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/ui/core_bridge.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ✅ OK | ❌ | - |
| `neural_ai/ui/factory.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ❌ | - |
| `neural_ai/ui/interfaces/__init__.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/ui/interfaces/ai_service_interface.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/ui/interfaces/core_bridge_interface.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/ui/interfaces/dashboard_service_interface.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/ui/interfaces/data_service_interface.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/ui/interfaces/live_ops_service_interface.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/ui/interfaces/navigation_service_interface.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/ui/interfaces/page_interface.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/ui/interfaces/strategy_service_interface.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/ui/pages/01_🚀_Launchpad.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ❌ | - |
| `neural_ai/ui/pages/02_🛠️_Dev_Center.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/ui/pages/03_📥_Data_Hub.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/ui/pages/04_🧠_AI_Lab.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/ui/pages/05_🪲_Strategy_Lab.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/ui/pages/06_⚡_Live_Ops.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/ui/pages/__init__.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ❌ | - |
| `neural_ai/ui/services/__init__.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/ui/services/ai_service.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/ui/services/dashboard_service.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/ui/services/data_service.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/ui/services/live_ops_service.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/ui/services/navigation_service.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `neural_ai/ui/services/strategy_service.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ❌ | - |
| `neural_ai/ui/streamlit_app.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |

## 7. Scripts Layer (`scripts/`)

| Fájl | Státusz | Teszt Pár | Pass/Fail/Err/Skip/Warn | Coverage (Stmt/Brch) | Lint/Mypy/Pylance | Src Warn | Config | Logger | Dokumentálva | Teendők |
|:-----|:--------|:----------|:-------------------|:---------------------|:------------------|:---------|:-------|:-------|:-------------|:--------|
| `scripts/__init__.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `scripts/audit_architecture.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `scripts/audit_architecture_detailed.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `scripts/audit_data.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `scripts/bootstrap_integration_test.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `scripts/bootstrap_test.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `scripts/data_reset.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `scripts/deploy_jforex.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `scripts/download_history.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ✅ OK | ❌ | - |
| `scripts/fix_fixture_scope.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `scripts/force_kill.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `scripts/generate.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 4 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `scripts/generate_docs.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `scripts/generate_v2.py` | 🔴 | ❌ MISSING | - | 0% / 0% | 1 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `scripts/install.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `scripts/migrate_structure.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `scripts/smart_pack.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `scripts/test_d2_standalone.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | - |
| `scripts/test_tick_pipeline.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ✅ OK | ❌ | - |
| `scripts/validation_end_to_end.py` | 🔴 | ✅ FOUND | - | 0% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ❌ | - |
