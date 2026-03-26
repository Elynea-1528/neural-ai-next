# 🌳 NEURAL AI NEXT - TASK TREE

**Generálva:** 2026-03-26 08:40:06 UTC
**Módszer:** Hibrid (AST + Pytest + Coverage + Ruff + Mypy + Pylance)
**Fájlok száma:** 296

## 📊 Statisztika

- ✅ **SECURE:** 133 (44.9%)
- 🟡 **WARNING:** 71 (24.0%)
- 🔴 **VULNERABLE:** 92 (31.1%)

---

## 0. Root Layer (`./`)

| Modul / Fájl | Státusz | Teszt Pár | Pass/Fail/Err/Skip | Coverage (Stmt/Brch) | Lint/Mypy/Pylance | Src Warn | Config | Logger | Dokumentálva | Teendők |
|:-------------|:--------|:----------|:-------------------|:---------------------|:------------------|:---------|:-------|:-------|:-------------|:--------|
| `main.py` | ✅ SECURE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `neural_ai/__init__.py` | ✅ SECURE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |

## 1. Infrastructure Layer (`neural_ai/core/`)

| Modul / Fájl | Státusz | Teszt Pár | Pass/Fail/Err/Skip | Coverage (Stmt/Brch) | Lint/Mypy/Pylance | Src Warn | Config | Logger | Dokumentálva | Teendők |
|:-------------|:--------|:----------|:-------------------|:---------------------|:------------------|:---------|:-------|:-------|:-------------|:--------|
| `core/__init__.py` | ✅ SECURE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/base/__init__.py` | ✅ SECURE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/base/exceptions/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `core/base/exceptions/base_error.py` | ✅ SECURE | ✅ FOUND | **42**/0/0/0 | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/base/factory.py` | ✅ SECURE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ✅ OK | ⚪ N/A | ✅ | - |
| `core/base/implementations/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `core/base/implementations/component_bundle.py` | 🔴 VULNERABLE | ✅ FOUND | **0**/39/0/0 | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Tesztek javítása: 39 failed, 0 error** |
| `core/base/implementations/di_container.py` | 🔴 VULNERABLE | ✅ FOUND | **4**/5/0/0 | N/A | 0 / 0 / 25 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Tesztek javítása: 5 failed, 0 error** | 🔎 Pylance: 25 hiba javítása |
| `core/base/implementations/lazy_loader.py` | ✅ SECURE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/base/implementations/singleton.py` | ✅ SECURE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/base/interfaces/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `core/base/interfaces/component_interface.py` | ✅ SECURE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/base/interfaces/container_interface.py` | ✅ SECURE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/config/__init__.py` | ✅ SECURE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/config/exceptions/__init__.py` | ✅ SECURE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/config/exceptions/config_error.py` | ✅ SECURE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/config/factory.py` | 🟡 WARNING | ✅ FOUND | - | N/A | 0 / 0 / 2 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔎 Pylance: 2 hiba javítása |
| `core/config/implementations/__init__.py` | ✅ SECURE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/config/implementations/dynamic_config_manager.py` | ✅ SECURE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ✅ | - |
| `core/config/implementations/yaml_config_manager.py` | 🟡 WARNING | ✅ FOUND | - | N/A | 0 / 0 / 22 | - | ✅ OK | ⚠️ UNUSED | ✅ | 🔎 Pylance: 22 hiba javítása |
| `core/config/interfaces/__init__.py` | ✅ SECURE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/config/interfaces/async_config_interface.py` | ✅ SECURE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ✅ | - |
| `core/config/interfaces/config_interface.py` | ✅ SECURE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/config/interfaces/factory_interface.py` | ✅ SECURE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/config/interfaces/types.py` | ✅ SECURE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ✅ OK | ⚪ N/A | ✅ | - |
| `core/db/__init__.py` | ✅ SECURE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/db/exceptions/__init__.py` | ✅ SECURE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/db/exceptions/db_error.py` | ✅ SECURE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/db/factory.py` | ✅ SECURE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ✅ | - |
| `core/db/implementations/__init__.py` | ✅ SECURE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/db/implementations/model_base.py` | ✅ SECURE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/db/implementations/models.py` | ✅ SECURE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/db/implementations/sqlalchemy_session.py` | 🟡 WARNING | ✅ FOUND | - | N/A | 0 / 0 / 10 | - | ⚪ N/A | ✅ OK | ✅ | 🔎 Pylance: 10 hiba javítása |
| `core/db/interfaces/__init__.py` | ✅ SECURE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/events/__init__.py` | ✅ SECURE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/events/exceptions/__init__.py` | ✅ SECURE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/events/exceptions/event_error.py` | ✅ SECURE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/events/factory.py` | ✅ SECURE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ✅ | - |
| `core/events/implementations/__init__.py` | ✅ SECURE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/events/implementations/zeromq_bus.py` | 🟡 WARNING | ✅ FOUND | - | N/A | 0 / 0 / 1 | - | ✅ OK | ✅ OK | ✅ | 🔎 Pylance: 1 hiba javítása |
| `core/events/interfaces/__init__.py` | ✅ SECURE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/events/interfaces/event_bus_interface.py` | ✅ SECURE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ✅ OK | ⚪ N/A | ✅ | - |
| `core/events/interfaces/event_models.py` | ✅ SECURE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ✅ OK | ⚪ N/A | ✅ | - |
| `core/logger/__init__.py` | ✅ SECURE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/logger/exceptions/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `core/logger/exceptions/logger_error.py` | ✅ SECURE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/logger/factory.py` | ✅ SECURE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/logger/formatters/logger_formatters.py` | ✅ SECURE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/logger/implementations/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `core/logger/implementations/colored_logger.py` | 🔴 VULNERABLE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | 🔴 MISSING | ✅ | 🔴 **Logger DI hiányzik!** |
| `core/logger/implementations/default_logger.py` | 🔴 VULNERABLE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | 🔴 MISSING | ✅ | 🔴 **Logger DI hiányzik!** |
| `core/logger/implementations/rotating_file_logger.py` | 🔴 VULNERABLE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | 🔴 MISSING | ✅ | 🔴 **Logger DI hiányzik!** |
| `core/logger/interfaces/__init__.py` | ✅ SECURE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/logger/interfaces/factory_interface.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `core/logger/interfaces/logger_interface.py` | ✅ SECURE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/system/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `core/system/exceptions/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `core/system/exceptions/health_error.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `core/system/factory.py` | ✅ SECURE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/system/implementations/health_monitor.py` | ✅ SECURE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ✅ | - |
| `core/system/interfaces/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `core/system/interfaces/health_interface.py` | ✅ SECURE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/utils/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `core/utils/decorators.py` | ✅ SECURE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/utils/exceptions/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `core/utils/exceptions/util_error.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `core/utils/factory.py` | ✅ SECURE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/utils/implementations/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `core/utils/implementations/hardware_info.py` | ✅ SECURE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/utils/interfaces/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `core/utils/interfaces/hardware_interface.py` | ✅ SECURE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |

## 2. Input Layer (`neural_ai/collectors/`)

| Modul / Fájl | Státusz | Teszt Pár | Pass/Fail/Err/Skip | Coverage (Stmt/Brch) | Lint/Mypy/Pylance | Src Warn | Config | Logger | Dokumentálva | Teendők |
|:-------------|:--------|:----------|:-------------------|:---------------------|:------------------|:---------|:-------|:-------|:-------------|:--------|
| `collectors/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `collectors/jforex/__init__.py` | ✅ SECURE | ✅ FOUND | **2**/0/0/0 | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `collectors/jforex/exceptions/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `collectors/jforex/exceptions/jforex_error.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `collectors/jforex/factory.py` | 🟡 WARNING | ✅ FOUND | **10**/0/0/0 | N/A | 0 / 0 / 2 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔎 Pylance: 2 hiba javítása |
| `collectors/jforex/implementations/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `collectors/jforex/implementations/bi5_downloader.py` | 🟡 WARNING | ✅ FOUND | **43**/0/0/0 | N/A | 0 / 0 / 2 | - | ⚪ N/A | ⚠️ UNUSED | ✅ | 🔎 Pylance: 2 hiba javítása |
| `collectors/jforex/implementations/live_feed.py` | 🟡 WARNING | ✅ FOUND | **12**/0/0/0 | N/A | 0 / 0 / 3 | - | ⚪ N/A | ✅ OK | ✅ | 🔎 Pylance: 3 hiba javítása |
| `collectors/jforex/interfaces/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `collectors/jforex/interfaces/downloader_interface.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `collectors/jforex/interfaces/live_interface.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `collectors/jforex/interfaces/tick_data.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |

## 3. Persistence Layer (`neural_ai/data/`)

| Modul / Fájl | Státusz | Teszt Pár | Pass/Fail/Err/Skip | Coverage (Stmt/Brch) | Lint/Mypy/Pylance | Src Warn | Config | Logger | Dokumentálva | Teendők |
|:-------------|:--------|:----------|:-------------------|:---------------------|:------------------|:---------|:-------|:-------|:-------------|:--------|
| `data/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `data/ingestion/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `data/ingestion/market_data_persister.py` | 🟡 WARNING | ✅ FOUND | - | N/A | 0 / 0 / 10 | - | ⚪ N/A | ✅ OK | ✅ | 🔎 Pylance: 10 hiba javítása |
| `data/storage/__init__.py` | ✅ SECURE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `data/storage/backends/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `data/storage/backends/base.py` | ✅ SECURE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ✅ | - |
| `data/storage/backends/pandas_backend.py` | ✅ SECURE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ✅ | - |
| `data/storage/backends/polars_backend.py` | ✅ SECURE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ✅ | - |
| `data/storage/exceptions/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `data/storage/factory.py` | 🟡 WARNING | ✅ FOUND | - | N/A | 0 / 0 / 5 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔎 Pylance: 5 hiba javítása |
| `data/storage/implementations/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `data/storage/implementations/file_storage.py` | 🟡 WARNING | ✅ FOUND | - | N/A | 0 / 0 / 6 | - | ⚪ N/A | ✅ OK | ✅ | 🔎 Pylance: 6 hiba javítása |
| `data/storage/implementations/parquet_storage.py` | 🟡 WARNING | ✅ FOUND | - | N/A | 0 / 0 / 19 | - | ✅ OK | ✅ OK | ✅ | 🔎 Pylance: 19 hiba javítása |
| `data/storage/interfaces/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `data/storage/interfaces/factory_interface.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `data/storage/interfaces/storage_interface.py` | ✅ SECURE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |

## 4. Domain Layer (`neural_ai/processors/`)

| Modul / Fájl | Státusz | Teszt Pár | Pass/Fail/Err/Skip | Coverage (Stmt/Brch) | Lint/Mypy/Pylance | Src Warn | Config | Logger | Dokumentálva | Teendők |
|:-------------|:--------|:----------|:-------------------|:---------------------|:------------------|:---------|:-------|:-------|:-------------|:--------|
| `processors/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `processors/dimensions/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `processors/dimensions/base.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ✅ OK | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `processors/dimensions/d01_price/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `processors/dimensions/d01_price/factory.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `processors/dimensions/d01_price/processor.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ✅ OK | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `processors/dimensions/d02_support/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `processors/dimensions/d02_support/exceptions/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `processors/dimensions/d02_support/exceptions/support_error.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `processors/dimensions/d02_support/factory.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `processors/dimensions/d02_support/implementations/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `processors/dimensions/d02_support/implementations/support_processor.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ✅ OK | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `processors/dimensions/d02_support/interfaces/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `processors/factory.py` | ✅ SECURE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `processors/implementations/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `processors/implementations/time_alignment_service.py` | 🟡 WARNING | ✅ FOUND | - | N/A | 0 / 0 / 3 | - | ⚪ N/A | ⚠️ UNUSED | ✅ | 🔎 Pylance: 3 hiba javítása |
| `processors/interfaces/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `processors/interfaces/dimension_processor_interface.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `processors/interfaces/tensor_converter_interface.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `processors/interfaces/time_alignment_interface.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `processors/resampler_service/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `processors/resampler_service/exceptions/resampler_error.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `processors/resampler_service/factory.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `processors/resampler_service/implementations/resampler_service.py` | 🟡 WARNING | ✅ FOUND | - | N/A | 0 / 0 / 1 | - | ⚪ N/A | ⚠️ UNUSED | ✅ | 🔎 Pylance: 1 hiba javítása |
| `processors/resampler_service/interfaces/resampler_interface.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |

## 5. Presentation Layer (`neural_ai/ui/`)

| Modul / Fájl | Státusz | Teszt Pár | Pass/Fail/Err/Skip | Coverage (Stmt/Brch) | Lint/Mypy/Pylance | Src Warn | Config | Logger | Dokumentálva | Teendők |
|:-------------|:--------|:----------|:-------------------|:---------------------|:------------------|:---------|:-------|:-------|:-------------|:--------|
| `ui/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `ui/app.py` | ✅ SECURE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ✅ | - |
| `ui/components/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `ui/components/base_widget.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `ui/core_bridge.py` | ✅ SECURE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `ui/factory.py` | 🟡 WARNING | ✅ FOUND | - | N/A | 0 / 0 / 20 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔎 Pylance: 20 hiba javítása |
| `ui/interfaces/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `ui/interfaces/ai_service_interface.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `ui/interfaces/core_bridge_interface.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `ui/interfaces/dashboard_service_interface.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `ui/interfaces/data_service_interface.py` | ✅ SECURE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `ui/interfaces/live_ops_service_interface.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `ui/interfaces/navigation_service_interface.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `ui/interfaces/page_interface.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `ui/interfaces/strategy_service_interface.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `ui/pages/01_🚀_Launchpad.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `ui/pages/02_🛠️_Dev_Center.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `ui/pages/03_📥_Data_Hub.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 3 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** | 🔎 Pylance: 3 hiba javítása |
| `ui/pages/04_🧠_AI_Lab.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `ui/pages/05_🪲_Strategy_Lab.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 17 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** | 🔎 Pylance: 17 hiba javítása |
| `ui/pages/06_⚡_Live_Ops.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `ui/pages/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `ui/services/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `ui/services/ai_service.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 2 | - | ⚪ N/A | ⚠️ UNUSED | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** | 🔎 Pylance: 2 hiba javítása |
| `ui/services/dashboard_service.py` | ✅ SECURE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ✅ | - |
| `ui/services/data_service.py` | 🟡 WARNING | ✅ FOUND | - | N/A | 0 / 0 / 18 | - | ⚪ N/A | ⚠️ UNUSED | ✅ | 🔎 Pylance: 18 hiba javítása |
| `ui/services/live_ops_service.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 2 | - | ⚪ N/A | ⚠️ UNUSED | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** | 🔎 Pylance: 2 hiba javítása |
| `ui/services/navigation_service.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |
| `ui/services/strategy_service.py` | 🟡 WARNING | ✅ FOUND | - | N/A | 0 / 0 / 69 | - | ⚪ N/A | ⚠️ UNUSED | ✅ | 🔎 Pylance: 69 hiba javítása |
| `ui/streamlit_app.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Teszt írás KÖTELEZŐ!** |

## 6. Tests Layer (`tests/`)

| Fájl | Státusz | Pass/Fail/Err/Skip | Coverage (Stmt/Brch) | Lint/Mypy/Pylance | Src Warn | Dokumentálva | Teendők |
|:-----|:--------|:-------------------|:---------------------|:------------------|:---------|:-------------|:--------|
| `tests/__init__.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/conftest.py` | 🟡 WARNING | - | N/A | 0 / 0 / 13 | - | ✅ | 🔎 Pylance: 13 hiba javítása |
| `tests/neural_ai/__init__.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/collectors/__init__.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/collectors/jforex/__init__.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/collectors/jforex/exceptions/__init__.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/collectors/jforex/exceptions/test_exceptions_init.py` | ✅ SECURE | **5**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/collectors/jforex/implementations/__init__.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/collectors/jforex/interfaces/__init__.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/collectors/jforex/interfaces/test_interfaces_init.py` | ✅ SECURE | **3**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/collectors/jforex/mocks/__init__.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/collectors/jforex/test_bi5_downloader.py` | 🟡 WARNING | **43**/0/0/0 | N/A | 0 / 0 / 286 | - | ✅ | 🔎 Pylance: 286 hiba javítása |
| `tests/neural_ai/collectors/jforex/test_factory.py` | ✅ SECURE | **10**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/collectors/jforex/test_jforex_init.py` | ✅ SECURE | **2**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/collectors/jforex/test_live_feed.py` | 🟡 WARNING | **12**/0/0/0 | N/A | 0 / 0 / 25 | - | ✅ | 🔎 Pylance: 25 hiba javítása |
| `tests/neural_ai/collectors/jforex/test_live_feed_integration.py` | 🟡 WARNING | **8**/0/0/0 | N/A | 0 / 0 / 17 | - | ✅ | 🔎 Pylance: 17 hiba javítása |
| `tests/neural_ai/core/base/exceptions/test_base_error.py` | ✅ SECURE | **42**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/base/exceptions/test_exceptions_init.py` | ✅ SECURE | **18**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/base/implementations/test_component_bundle.py` | 🔴 VULNERABLE | **0**/39/0/0 | N/A | 0 / 0 / 0 | - | ✅ | 🔴 **Tesztek javítása: 39 failed, 0 error** |
| `tests/neural_ai/core/base/implementations/test_di_container.py` | 🔴 VULNERABLE | **4**/5/0/0 | N/A | 0 / 0 / 0 | - | ✅ | 🔴 **Tesztek javítása: 5 failed, 0 error** |
| `tests/neural_ai/core/base/implementations/test_implementations_init.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/base/implementations/test_lazy_loader.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/base/implementations/test_singleton.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/base/interfaces/test_component_interface.py` | 🟡 WARNING | - | N/A | 0 / 0 / 3 | - | ✅ | 🔎 Pylance: 3 hiba javítása |
| `tests/neural_ai/core/base/interfaces/test_container_interface.py` | 🟡 WARNING | - | N/A | 0 / 0 / 6 | - | ✅ | 🔎 Pylance: 6 hiba javítása |
| `tests/neural_ai/core/base/interfaces/test_interfaces_init.py` | 🟡 WARNING | - | N/A | 0 / 0 / 4 | - | ✅ | 🔎 Pylance: 4 hiba javítása |
| `tests/neural_ai/core/base/test_base_init.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/base/test_factory.py` | 🟡 WARNING | - | N/A | 0 / 0 / 52 | - | ✅ | 🔎 Pylance: 52 hiba javítása |
| `tests/neural_ai/core/config/exceptions/test_config_error.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/config/exceptions/test_config_exceptions_init.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/config/implementations/test_config_implementations_init.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/config/implementations/test_dynamic_config_manager.py` | 🟡 WARNING | - | N/A | 0 / 0 / 54 | - | ✅ | 🔎 Pylance: 54 hiba javítása |
| `tests/neural_ai/core/config/implementations/test_dynamic_config_manager_comprehensive.py` | 🟡 WARNING | - | N/A | 0 / 0 / 9 | - | ✅ | 🔎 Pylance: 9 hiba javítása |
| `tests/neural_ai/core/config/implementations/test_yaml_config_manager.py` | 🟡 WARNING | - | N/A | 0 / 0 / 17 | - | ✅ | 🔎 Pylance: 17 hiba javítása |
| `tests/neural_ai/core/config/interfaces/test_async_config_interface.py` | 🟡 WARNING | - | N/A | 0 / 0 / 1 | - | ✅ | 🔎 Pylance: 1 hiba javítása |
| `tests/neural_ai/core/config/interfaces/test_config_interface.py` | 🟡 WARNING | - | N/A | 0 / 0 / 1 | - | ✅ | 🔎 Pylance: 1 hiba javítása |
| `tests/neural_ai/core/config/interfaces/test_config_interfaces_init.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/config/interfaces/test_factory_interface.py` | 🟡 WARNING | - | N/A | 0 / 0 / 11 | - | ✅ | 🔎 Pylance: 11 hiba javítása |
| `tests/neural_ai/core/config/interfaces/test_types.py` | 🟡 WARNING | - | N/A | 0 / 0 / 4 | - | ✅ | 🔎 Pylance: 4 hiba javítása |
| `tests/neural_ai/core/config/test_config_factory.py` | 🟡 WARNING | - | N/A | 0 / 0 / 1 | - | ✅ | 🔎 Pylance: 1 hiba javítása |
| `tests/neural_ai/core/config/test_config_init.py` | 🟡 WARNING | - | N/A | 0 / 0 / 3 | - | ✅ | 🔎 Pylance: 3 hiba javítása |
| `tests/neural_ai/core/config/test_processors_config.py` | 🟡 WARNING | - | N/A | 0 / 0 / 33 | - | ✅ | 🔎 Pylance: 33 hiba javítása |
| `tests/neural_ai/core/config/test_yaml_config_manager_validation.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/db/conftest.py` | 🟡 WARNING | - | N/A | 0 / 0 / 13 | - | ✅ | 🔎 Pylance: 13 hiba javítása |
| `tests/neural_ai/core/db/exceptions/test_db_error.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/db/exceptions/test_db_exceptions_init.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/db/implementations/test_db_implementations_init.py` | 🟡 WARNING | - | N/A | 0 / 0 / 3 | - | ✅ | 🔎 Pylance: 3 hiba javítása |
| `tests/neural_ai/core/db/implementations/test_model_base.py` | 🟡 WARNING | - | N/A | 0 / 0 / 2 | - | ✅ | 🔎 Pylance: 2 hiba javítása |
| `tests/neural_ai/core/db/implementations/test_models.py` | 🟡 WARNING | - | N/A | 0 / 0 / 13 | - | ✅ | 🔎 Pylance: 13 hiba javítása |
| `tests/neural_ai/core/db/implementations/test_sqlalchemy_session.py` | 🟡 WARNING | - | N/A | 0 / 0 / 14 | - | ✅ | 🔎 Pylance: 14 hiba javítása |
| `tests/neural_ai/core/db/interfaces/test_db_interfaces_init.py` | 🟡 WARNING | - | N/A | 0 / 0 / 1 | - | ✅ | 🔎 Pylance: 1 hiba javítása |
| `tests/neural_ai/core/db/test_db_factory.py` | 🟡 WARNING | - | N/A | 0 / 1 / 7 | - | ✅ | 🔬 Mypy: 1 type hiba javítása | 🔎 Pylance: 7 hiba javítása |
| `tests/neural_ai/core/db/test_db_init.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/events/exceptions/test_event_error.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/events/exceptions/test_events_exceptions_init.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/events/implementations/test_events_implementations_init.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/events/implementations/test_zeromq_bus.py` | 🟡 WARNING | - | N/A | 0 / 0 / 49 | - | ✅ | 🔎 Pylance: 49 hiba javítása |
| `tests/neural_ai/core/events/interfaces/test_event_bus_interface.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/events/interfaces/test_event_models.py` | 🟡 WARNING | - | N/A | 0 / 0 / 8 | - | ✅ | 🔎 Pylance: 8 hiba javítása |
| `tests/neural_ai/core/events/interfaces/test_events_interfaces_init.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/events/test_events_factory.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/events/test_events_init.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/logger/exceptions/test_logger_error.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/logger/formatters/test_logger_formatters.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/logger/implementations/test_colored_logger.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/logger/implementations/test_default_logger.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/logger/implementations/test_rotating_file_logger.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/logger/interfaces/test_logger_factory_interface.py` | 🟡 WARNING | - | N/A | 0 / 0 / 2 | - | ✅ | 🔎 Pylance: 2 hiba javítása |
| `tests/neural_ai/core/logger/interfaces/test_logger_interface.py` | 🟡 WARNING | - | N/A | 0 / 0 / 1 | - | ✅ | 🔎 Pylance: 1 hiba javítása |
| `tests/neural_ai/core/logger/interfaces/test_logger_interfaces_init.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/logger/test_logger_factory.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/logger/test_logger_init.py` | 🟡 WARNING | - | N/A | 0 / 0 / 2 | - | ✅ | 🔎 Pylance: 2 hiba javítása |
| `tests/neural_ai/core/system/implementations/test_health_monitor.py` | 🟡 WARNING | - | N/A | 0 / 0 / 1 | - | ✅ | 🔎 Pylance: 1 hiba javítása |
| `tests/neural_ai/core/system/interfaces/test_health_interface.py` | 🟡 WARNING | - | N/A | 0 / 0 / 16 | - | ✅ | 🔎 Pylance: 16 hiba javítása |
| `tests/neural_ai/core/system/test_system_factory.py` | 🟡 WARNING | - | N/A | 0 / 0 / 2 | - | ✅ | 🔎 Pylance: 2 hiba javítása |
| `tests/neural_ai/core/test_core_init.py` | 🟡 WARNING | - | N/A | 0 / 0 / 28 | - | ✅ | 🔎 Pylance: 28 hiba javítása |
| `tests/neural_ai/core/test_core_init_missing_coverage.py` | 🟡 WARNING | - | N/A | 0 / 0 / 8 | - | ✅ | 🔎 Pylance: 8 hiba javítása |
| `tests/neural_ai/core/test_init_version_fallback.py` | 🟡 WARNING | - | N/A | 0 / 0 / 2 | - | ✅ | 🔎 Pylance: 2 hiba javítása |
| `tests/neural_ai/core/test_pyproject_ui_dependencies.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/utils/exceptions/test_util_errors.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/utils/interfaces/test_hardware_interface.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/utils/test_decorators.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/utils/test_hardware_info.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/utils/test_utils_factory.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/data/ingestion/test_market_data_persister.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/data/storage/backends/test_base.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/data/storage/backends/test_pandas_backend.py` | 🟡 WARNING | - | N/A | 0 / 0 / 22 | - | ✅ | 🔎 Pylance: 22 hiba javítása |
| `tests/neural_ai/data/storage/backends/test_polars_backend.py` | 🟡 WARNING | - | N/A | 0 / 0 / 13 | - | ✅ | 🔎 Pylance: 13 hiba javítása |
| `tests/neural_ai/data/storage/implementations/test_file_storage.py` | 🟡 WARNING | - | N/A | 0 / 0 / 30 | - | ✅ | 🔎 Pylance: 30 hiba javítása |
| `tests/neural_ai/data/storage/implementations/test_parquet_storage.py` | 🟡 WARNING | - | N/A | 0 / 0 / 9 | - | ✅ | 🔎 Pylance: 9 hiba javítása |
| `tests/neural_ai/data/storage/interfaces/test_storage_factory_interface.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/data/storage/interfaces/test_storage_interface.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/data/storage/test_storage_factory.py` | 🟡 WARNING | - | N/A | 0 / 0 / 8 | - | ✅ | 🔎 Pylance: 8 hiba javítása |
| `tests/neural_ai/data/storage/test_storage_init.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/processors/__init__.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/processors/conftest.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/processors/dimensions/d01_price/test_d01_processor.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/processors/dimensions/d02_support/test_d02_exceptions.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/processors/dimensions/d02_support/test_d02_factory.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/processors/dimensions/d02_support/test_d02_processor.py` | 🟡 WARNING | - | N/A | 0 / 0 / 28 | - | ✅ | 🔎 Pylance: 28 hiba javítása |
| `tests/neural_ai/processors/dimensions/d02_support/test_d02_processor_coverage.py` | 🟡 WARNING | - | N/A | 0 / 0 / 59 | - | ✅ | 🔎 Pylance: 59 hiba javítása |
| `tests/neural_ai/processors/dimensions/d02_support/test_d02_processor_extended.py` | 🟡 WARNING | - | N/A | 0 / 0 / 133 | - | ✅ | 🔎 Pylance: 133 hiba javítása |
| `tests/neural_ai/processors/resampler_service/__init__.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/processors/resampler_service/test_resampler_service.py` | 🟡 WARNING | - | N/A | 0 / 0 / 13 | - | ✅ | 🔎 Pylance: 13 hiba javítása |
| `tests/neural_ai/processors/test_factory.py` | 🟡 WARNING | - | N/A | 0 / 0 / 14 | - | ✅ | 🔎 Pylance: 14 hiba javítása |
| `tests/neural_ai/processors/test_time_alignment_service.py` | 🟡 WARNING | - | N/A | 0 / 0 / 2 | - | ✅ | 🔎 Pylance: 2 hiba javítása |
| `tests/neural_ai/test___init__.py` | 🟡 WARNING | - | N/A | 0 / 0 / 1 | - | ✅ | 🔎 Pylance: 1 hiba javítása |
| `tests/neural_ai/ui/interfaces/test_data_service_interface.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/ui/pages/test_data_hub_page.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/ui/pages/test_launchpad_page.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/ui/pages/test_strategy_lab_page.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/ui/services/test_dashboard_service.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/ui/services/test_data_service.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/ui/services/test_strategy_service.py` | 🟡 WARNING | - | N/A | 0 / 0 / 18 | - | ✅ | 🔎 Pylance: 18 hiba javítása |
| `tests/neural_ai/ui/test_app.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/ui/test_core_bridge.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/ui/test_ui_factory.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/scripts/__init__.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/scripts/test_data_reset.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/scripts/test_download_history.py` | 🟡 WARNING | - | N/A | 0 / 0 / 1 | - | ✅ | 🔎 Pylance: 1 hiba javítása |
| `tests/scripts/test_migrate_structure.py` | 🟡 WARNING | - | N/A | 0 / 0 / 10 | - | ✅ | 🔎 Pylance: 10 hiba javítása |
| `tests/scripts/test_test_tick_pipeline.py` | 🟡 WARNING | - | N/A | 0 / 0 / 8 | - | ✅ | 🔎 Pylance: 8 hiba javítása |
| `tests/scripts/test_validation_end_to_end.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/test_main.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |

## 7. Scripts Layer (`scripts/`)

| Fájl | Státusz | Teszt Pár | Pass/Fail/Err/Skip | Coverage (Stmt/Brch) | Lint/Mypy/Pylance | Src Warn | Config | Logger | Dokumentálva | Teendők |
|:-----|:--------|:----------|:-------------------|:---------------------|:------------------|:---------|:-------|:-------|:-------------|:--------|
| `scripts/__init__.py` | ✅ SECURE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `scripts/audit_data.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | ⚠️ Teszt fájl létrehozása |
| `scripts/bootstrap_integration_test.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | ⚠️ Teszt fájl létrehozása |
| `scripts/bootstrap_test.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | ⚠️ Teszt fájl létrehozása |
| `scripts/data_reset.py` | ✅ SECURE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `scripts/deploy_jforex.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | ⚠️ Teszt fájl létrehozása |
| `scripts/download_history.py` | 🟡 WARNING | ✅ FOUND | - | N/A | 0 / 0 / 10 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔎 Pylance: 10 hiba javítása |
| `scripts/force_kill.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | ⚠️ Teszt fájl létrehozása |
| `scripts/generate.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 1 | - | ⚪ N/A | ⚪ N/A | ✅ | ⚠️ Teszt fájl létrehozása | 🔎 Pylance: 1 hiba javítása |
| `scripts/generate_docs.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 10 | - | ⚪ N/A | ⚪ N/A | ✅ | ⚠️ Teszt fájl létrehozása | 🔎 Pylance: 10 hiba javítása |
| `scripts/install.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | ⚠️ Teszt fájl létrehozása |
| `scripts/migrate_structure.py` | ✅ SECURE | ✅ FOUND | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `scripts/smart_pack.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | ⚠️ Teszt fájl létrehozása |
| `scripts/test_d2_standalone.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 25 | - | ⚪ N/A | ⚪ N/A | ✅ | ⚠️ Teszt fájl létrehozása | 🔎 Pylance: 25 hiba javítása |
| `scripts/test_tick_pipeline.py` | 🟡 WARNING | ✅ FOUND | - | N/A | 0 / 0 / 1 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔎 Pylance: 1 hiba javítása |
| `scripts/validation_end_to_end.py` | 🟡 WARNING | ✅ FOUND | - | N/A | 0 / 0 / 11 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔎 Pylance: 11 hiba javítása |
