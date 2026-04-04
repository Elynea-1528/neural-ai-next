# 🌳 NEURAL AI NEXT - TASK TREE

**Generálva:** 2026-04-04 11:33:43 UTC
**Módszer:** Hibrid (AST + Pytest + Coverage + Ruff + Mypy + Pylance)
**Fájlok száma:** 366

## 📊 Statisztika

- ✅ **SECURE:** 324 (88.5%)
- 🟡 **WARNING:** 37 (10.1%)
- 🔴 **VULNERABLE:** 5 (1.4%)

---

## 0. Root Layer (`./`)

| Modul / Fájl | Státusz | Teszt Pár | Pass/Fail/Err/Skip | Coverage (Stmt/Brch) | Lint/Mypy/Pylance | Src Warn | Config | Logger | Dokumentálva | Teendők |
|:-------------|:--------|:----------|:-------------------|:---------------------|:------------------|:---------|:-------|:-------|:-------------|:--------|
| `main.py` | ✅ SECURE | ✅ FOUND | **29**/0/0/0 | 96% / 85% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `neural_ai/__init__.py` | ✅ SECURE | ✅ FOUND | **21**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |

## 1. Infrastructure Layer (`neural_ai/core/`)

| Modul / Fájl | Státusz | Teszt Pár | Pass/Fail/Err/Skip | Coverage (Stmt/Brch) | Lint/Mypy/Pylance | Src Warn | Config | Logger | Dokumentálva | Teendők |
|:-------------|:--------|:----------|:-------------------|:---------------------|:------------------|:---------|:-------|:-------|:-------------|:--------|
| `core/__init__.py` | 🔴 VULNERABLE | ✅ FOUND | **15**/7/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Tesztek javítása: 7 failed, 0 error** |
| `core/base/__init__.py` | ✅ SECURE | ✅ FOUND | **7**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/base/exceptions/__init__.py` | ✅ SECURE | ✅ FOUND | **18**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/base/exceptions/base_error.py` | ✅ SECURE | ✅ FOUND | **42**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/base/factory.py` | ✅ SECURE | ✅ FOUND | **35**/0/0/0 | 90% / 69% | 0 / 0 / 0 | - | ✅ OK | ⚪ N/A | ✅ | - |
| `core/base/implementations/__init__.py` | ✅ SECURE | ✅ FOUND | **3**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/base/implementations/component_bundle.py` | ✅ SECURE | ✅ FOUND | **39**/0/0/0 | 97% / 83% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ✅ | - |
| `core/base/implementations/di_container.py` | ✅ SECURE | ✅ FOUND | **32**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/base/implementations/lazy_loader.py` | ✅ SECURE | ✅ FOUND | **10**/0/0/0 | 96% / 83% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ✅ | - |
| `core/base/implementations/singleton.py` | 🟡 WARNING | ✅ FOUND | **10**/0/0/0 | 71% / 38% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 📊 Coverage növelése: 71% → 100% |
| `core/base/interfaces/__init__.py` | ✅ SECURE | ✅ FOUND | **12**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/base/interfaces/component_interface.py` | 🟡 WARNING | ✅ FOUND | **13**/0/0/0 | 76% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 📊 Coverage növelése: 76% → 100% |
| `core/base/interfaces/container_interface.py` | ✅ SECURE | ✅ FOUND | **20**/0/0/0 | 97% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/config/__init__.py` | ✅ SECURE | ✅ FOUND | **10**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/config/exceptions/__init__.py` | ✅ SECURE | ✅ FOUND | **22**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/config/exceptions/config_error.py` | ✅ SECURE | ✅ FOUND | **15**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/config/factory.py` | ✅ SECURE | ✅ FOUND | **27**/0/0/0 | 97% / 97% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/config/implementations/__init__.py` | 🔴 VULNERABLE | ✅ FOUND | **5**/1/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔴 **Tesztek javítása: 1 failed, 0 error** |
| `core/config/implementations/dynamic_config_manager.py` | ✅ SECURE | ✅ FOUND | **61**/0/0/0 | 98% / 93% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/config/implementations/yaml_config_manager.py` | 🟡 WARNING | ✅ FOUND | **76**/0/0/0 | 78% / 90% | 0 / 0 / 0 | - | ✅ OK | ⚪ N/A | ✅ | 📊 Coverage növelése: 78% → 100% |
| `core/config/interfaces/__init__.py` | ✅ SECURE | ✅ FOUND | **16**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/config/interfaces/async_config_interface.py` | ✅ SECURE | ✅ FOUND | **25**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ✅ | - |
| `core/config/interfaces/config_interface.py` | ✅ SECURE | ✅ FOUND | **17**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/config/interfaces/factory_interface.py` | ✅ SECURE | ✅ FOUND | **23**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/config/interfaces/types.py` | ✅ SECURE | ✅ FOUND | **28**/0/0/0 | 92% / 44% | 0 / 0 / 0 | - | ✅ OK | ⚪ N/A | ✅ | - |
| `core/db/__init__.py` | ✅ SECURE | ✅ FOUND | **20**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/db/exceptions/__init__.py` | ✅ SECURE | ✅ FOUND | **5**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/db/exceptions/db_error.py` | ✅ SECURE | ✅ FOUND | **9**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/db/factory.py` | ✅ SECURE | ✅ FOUND | **22**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ✅ | - |
| `core/db/implementations/__init__.py` | ✅ SECURE | ✅ FOUND | **3**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/db/implementations/model_base.py` | ✅ SECURE | ✅ FOUND | **12**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/db/implementations/models.py` | ✅ SECURE | ✅ FOUND | **22**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/db/implementations/sqlalchemy_session.py` | 🟡 WARNING | ✅ FOUND | **21**/0/0/16 | 71% / 62% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 📊 Coverage növelése: 71% → 100% | ⏭️ 16 skipped teszt aktiválása |
| `core/db/interfaces/__init__.py` | ✅ SECURE | ✅ FOUND | **4**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/events/__init__.py` | ✅ SECURE | ✅ FOUND | **10**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/events/exceptions/__init__.py` | ✅ SECURE | ✅ FOUND | **5**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/events/exceptions/event_error.py` | ✅ SECURE | ✅ FOUND | **9**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/events/factory.py` | ✅ SECURE | ✅ FOUND | **14**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ✅ | - |
| `core/events/implementations/__init__.py` | ✅ SECURE | ✅ FOUND | **3**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/events/implementations/zeromq_bus.py` | ✅ SECURE | ✅ FOUND | **49**/0/0/0 | 97% / 90% | 0 / 0 / 0 | - | ✅ OK | ⚪ N/A | ✅ | - |
| `core/events/interfaces/__init__.py` | ✅ SECURE | ✅ FOUND | **11**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/events/interfaces/event_bus_interface.py` | ✅ SECURE | ✅ FOUND | **27**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ✅ OK | ⚪ N/A | ✅ | - |
| `core/events/interfaces/event_models.py` | ✅ SECURE | ✅ FOUND | **26**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ✅ OK | ⚪ N/A | ✅ | - |
| `core/logger/__init__.py` | ✅ SECURE | ✅ FOUND | **7**/0/0/0 | 87% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/logger/exceptions/__init__.py` | ✅ SECURE | ✅ FOUND | **16**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/logger/exceptions/logger_error.py` | ✅ SECURE | ✅ FOUND | **14**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/logger/factory.py` | ✅ SECURE | ✅ FOUND | **12**/0/0/0 | 98% / 93% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/logger/formatters/logger_formatters.py` | ✅ SECURE | ✅ FOUND | **6**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/logger/implementations/__init__.py` | ✅ SECURE | ✅ FOUND | **5**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/logger/implementations/colored_logger.py` | ✅ SECURE | ✅ FOUND | **9**/0/0/0 | 86% / 67% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/logger/implementations/default_logger.py` | ✅ SECURE | ✅ FOUND | **8**/0/0/0 | 94% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/logger/implementations/rotating_file_logger.py` | 🟡 WARNING | ✅ FOUND | **7**/0/0/0 | 64% / 45% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 📊 Coverage növelése: 64% → 100% |
| `core/logger/interfaces/__init__.py` | 🟡 WARNING | ✅ FOUND | **15**/0/0/0 | 78% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 📊 Coverage növelése: 78% → 100% |
| `core/logger/interfaces/factory_interface.py` | ✅ SECURE | ✅ FOUND | **5**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/logger/interfaces/logger_interface.py` | ✅ SECURE | ✅ FOUND | **3**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/system/__init__.py` | ✅ SECURE | ✅ FOUND | **24**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/system/exceptions/__init__.py` | ✅ SECURE | ✅ FOUND | **18**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/system/exceptions/health_error.py` | ✅ SECURE | ✅ FOUND | **17**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/system/factory.py` | ✅ SECURE | ✅ FOUND | **19**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/system/implementations/health_monitor.py` | ✅ SECURE | ✅ FOUND | **28**/0/0/0 | 94% / 88% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ✅ | - |
| `core/system/interfaces/__init__.py` | ✅ SECURE | ✅ FOUND | **22**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/system/interfaces/health_interface.py` | ✅ SECURE | ✅ FOUND | **22**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/utils/__init__.py` | ✅ SECURE | ✅ FOUND | **6**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/utils/decorators.py` | ✅ SECURE | ✅ FOUND | **13**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/utils/exceptions/__init__.py` | ✅ SECURE | ✅ FOUND | **5**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/utils/exceptions/util_error.py` | ✅ SECURE | ✅ FOUND | **12**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/utils/factory.py` | ✅ SECURE | ✅ FOUND | **11**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/utils/implementations/__init__.py` | ✅ SECURE | ✅ FOUND | **5**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/utils/implementations/hardware_info.py` | ✅ SECURE | ✅ FOUND | **15**/0/0/0 | 97% / 90% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/utils/interfaces/__init__.py` | ✅ SECURE | ✅ FOUND | **4**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `core/utils/interfaces/hardware_interface.py` | ✅ SECURE | ✅ FOUND | **3**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |

## 2. Input Layer (`neural_ai/collectors/`)

| Modul / Fájl | Státusz | Teszt Pár | Pass/Fail/Err/Skip | Coverage (Stmt/Brch) | Lint/Mypy/Pylance | Src Warn | Config | Logger | Dokumentálva | Teendők |
|:-------------|:--------|:----------|:-------------------|:---------------------|:------------------|:---------|:-------|:-------|:-------------|:--------|
| `collectors/__init__.py` | ✅ SECURE | ✅ FOUND | **10**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `collectors/jforex/__init__.py` | ✅ SECURE | ✅ FOUND | **2**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `collectors/jforex/exceptions/__init__.py` | ✅ SECURE | ✅ FOUND | **5**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `collectors/jforex/exceptions/jforex_error.py` | ✅ SECURE | ✅ FOUND | **15**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `collectors/jforex/factory.py` | ✅ SECURE | ✅ FOUND | **10**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `collectors/jforex/implementations/__init__.py` | ✅ SECURE | ✅ FOUND | **5**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `collectors/jforex/implementations/bi5_downloader.py` | ✅ SECURE | ✅ FOUND | **43**/0/0/0 | 99% / 95% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ✅ | - |
| `collectors/jforex/implementations/live_feed.py` | ✅ SECURE | ✅ FOUND | **12**/0/0/0 | 95% / 80% | 0 / 0 / 0 | - | ⚪ N/A | ✅ OK | ✅ | - |
| `collectors/jforex/interfaces/__init__.py` | ✅ SECURE | ✅ FOUND | **3**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `collectors/jforex/interfaces/downloader_interface.py` | 🟡 WARNING | ✅ FOUND | **7**/0/0/0 | 75% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 📊 Coverage növelése: 75% → 100% |
| `collectors/jforex/interfaces/live_interface.py` | 🟡 WARNING | ✅ FOUND | **7**/0/0/0 | 73% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 📊 Coverage növelése: 73% → 100% |
| `collectors/jforex/interfaces/tick_data.py` | ✅ SECURE | ✅ FOUND | **10**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |

## 3. Persistence Layer (`neural_ai/data/`)

| Modul / Fájl | Státusz | Teszt Pár | Pass/Fail/Err/Skip | Coverage (Stmt/Brch) | Lint/Mypy/Pylance | Src Warn | Config | Logger | Dokumentálva | Teendők |
|:-------------|:--------|:----------|:-------------------|:---------------------|:------------------|:---------|:-------|:-------|:-------------|:--------|
| `data/__init__.py` | ✅ SECURE | ✅ FOUND | **2**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `data/ingestion/__init__.py` | ✅ SECURE | ✅ FOUND | **4**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `data/ingestion/market_data_persister.py` | 🟡 WARNING | ✅ FOUND | **20**/0/0/5 | 79% / 76% | 0 / 0 / 0 | 1 | ⚪ N/A | ✅ OK | ✅ | ⚠️ 1 warning javítása | 📊 Coverage növelése: 79% → 100% | ⏭️ 5 skipped teszt aktiválása |
| `data/storage/__init__.py` | ✅ SECURE | ✅ FOUND | **5**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `data/storage/backends/__init__.py` | ✅ SECURE | ✅ FOUND | **5**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `data/storage/backends/base.py` | ✅ SECURE | ✅ FOUND | **8**/0/0/0 | 83% / 78% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ✅ | - |
| `data/storage/backends/pandas_backend.py` | ✅ SECURE | ✅ FOUND | **30**/0/0/0 | 91% / 83% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ✅ | - |
| `data/storage/backends/polars_backend.py` | 🟡 WARNING | ✅ FOUND | **24**/0/0/6 | 79% / 70% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ✅ | 📊 Coverage növelése: 79% → 100% | ⏭️ 6 skipped teszt aktiválása |
| `data/storage/exceptions/__init__.py` | ✅ SECURE | ✅ FOUND | **23**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `data/storage/factory.py` | ✅ SECURE | ✅ FOUND | **12**/0/0/0 | 96% / 83% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `data/storage/implementations/__init__.py` | ✅ SECURE | ✅ FOUND | **5**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `data/storage/implementations/file_storage.py` | 🟡 WARNING | ✅ FOUND | **50**/0/0/2 | 88% / 83% | 0 / 0 / 0 | - | ⚪ N/A | ✅ OK | ✅ | ⏭️ 2 skipped teszt aktiválása |
| `data/storage/implementations/parquet_storage.py` | 🟡 WARNING | ✅ FOUND | **34**/0/0/0 | 73% / 65% | 0 / 0 / 0 | - | ✅ OK | ✅ OK | ✅ | 📊 Coverage növelése: 73% → 100% |
| `data/storage/interfaces/__init__.py` | ✅ SECURE | ✅ FOUND | **13**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `data/storage/interfaces/factory_interface.py` | ✅ SECURE | ✅ FOUND | **6**/0/0/0 | 83% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `data/storage/interfaces/storage_interface.py` | ✅ SECURE | ✅ FOUND | **11**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |

## 4. Domain Layer (`neural_ai/processors/`)

| Modul / Fájl | Státusz | Teszt Pár | Pass/Fail/Err/Skip | Coverage (Stmt/Brch) | Lint/Mypy/Pylance | Src Warn | Config | Logger | Dokumentálva | Teendők |
|:-------------|:--------|:----------|:-------------------|:---------------------|:------------------|:---------|:-------|:-------|:-------------|:--------|
| `processors/__init__.py` | ✅ SECURE | ✅ FOUND | **4**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `processors/dimensions/__init__.py` | ✅ SECURE | ✅ FOUND | **2**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `processors/dimensions/base.py` | ✅ SECURE | ✅ FOUND | **8**/0/0/0 | 95% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ✅ OK | ✅ | - |
| `processors/dimensions/d01_price/__init__.py` | ✅ SECURE | ✅ FOUND | **2**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `processors/dimensions/d01_price/factory.py` | ✅ SECURE | ✅ FOUND | **2**/0/0/0 | 86% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `processors/dimensions/d01_price/processor.py` | ✅ SECURE | ✅ FOUND | **18**/0/0/0 | 97% / 88% | 0 / 0 / 0 | - | ⚪ N/A | ✅ OK | ✅ | - |
| `processors/dimensions/d02_support/__init__.py` | ✅ SECURE | ✅ FOUND | **2**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `processors/dimensions/d02_support/exceptions/__init__.py` | ✅ SECURE | ✅ FOUND | **2**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `processors/dimensions/d02_support/exceptions/support_error.py` | ✅ SECURE | ✅ FOUND | **9**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `processors/dimensions/d02_support/factory.py` | ✅ SECURE | ✅ FOUND | **2**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `processors/dimensions/d02_support/implementations/__init__.py` | ✅ SECURE | ✅ FOUND | **2**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `processors/dimensions/d02_support/implementations/support_processor.py` | ✅ SECURE | ✅ FOUND | **26**/0/0/0 | 93% / 88% | 0 / 0 / 0 | - | ⚪ N/A | ✅ OK | ✅ | - |
| `processors/dimensions/d02_support/interfaces/__init__.py` | ✅ SECURE | ✅ FOUND | **2**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `processors/factory.py` | ✅ SECURE | ✅ FOUND | **3**/0/0/0 | 89% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `processors/implementations/__init__.py` | ✅ SECURE | ✅ FOUND | **2**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `processors/implementations/time_alignment_service.py` | ✅ SECURE | ✅ FOUND | **8**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ✅ | - |
| `processors/interfaces/__init__.py` | ✅ SECURE | ✅ FOUND | **3**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `processors/interfaces/dimension_processor_interface.py` | ✅ SECURE | ✅ FOUND | **7**/0/0/0 | 80% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `processors/interfaces/tensor_converter_interface.py` | ✅ SECURE | ✅ FOUND | **7**/0/0/0 | 83% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `processors/interfaces/time_alignment_interface.py` | 🟡 WARNING | ✅ FOUND | **8**/0/0/0 | 78% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 📊 Coverage növelése: 78% → 100% |
| `processors/resampler_service/__init__.py` | ✅ SECURE | ✅ FOUND | **6**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `processors/resampler_service/exceptions/resampler_error.py` | ✅ SECURE | ✅ FOUND | **17**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `processors/resampler_service/factory.py` | ✅ SECURE | ✅ FOUND | **7**/0/0/0 | 94% / 50% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `processors/resampler_service/implementations/resampler_service.py` | ✅ SECURE | ✅ FOUND | **35**/0/0/0 | 95% / 88% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ✅ | - |
| `processors/resampler_service/interfaces/resampler_interface.py` | ✅ SECURE | ✅ FOUND | **7**/0/0/0 | 86% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |

## 5. Presentation Layer (`neural_ai/ui/`)

| Modul / Fájl | Státusz | Teszt Pár | Pass/Fail/Err/Skip | Coverage (Stmt/Brch) | Lint/Mypy/Pylance | Src Warn | Config | Logger | Dokumentálva | Teendők |
|:-------------|:--------|:----------|:-------------------|:---------------------|:------------------|:---------|:-------|:-------|:-------------|:--------|
| `ui/__init__.py` | ✅ SECURE | ✅ FOUND | **9**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `ui/app.py` | ✅ SECURE | ✅ FOUND | **16**/0/0/0 | 85% / 75% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ✅ | - |
| `ui/components/__init__.py` | ✅ SECURE | ✅ FOUND | **9**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `ui/components/base_widget.py` | ✅ SECURE | ✅ FOUND | **10**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `ui/core_bridge.py` | 🟡 WARNING | ✅ FOUND | **20**/0/0/0 | 60% / 43% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 📊 Coverage növelése: 60% → 100% |
| `ui/factory.py` | 🟡 WARNING | ✅ FOUND | **15**/0/0/0 | 80% / 65% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 📊 Coverage növelése: 80% → 100% |
| `ui/interfaces/__init__.py` | ✅ SECURE | ✅ FOUND | **17**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `ui/interfaces/ai_service_interface.py` | ✅ SECURE | ✅ FOUND | **11**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `ui/interfaces/core_bridge_interface.py` | ✅ SECURE | ✅ FOUND | **13**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `ui/interfaces/dashboard_service_interface.py` | ✅ SECURE | ✅ FOUND | **10**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `ui/interfaces/data_service_interface.py` | ✅ SECURE | ✅ FOUND | **19**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `ui/interfaces/live_ops_service_interface.py` | ✅ SECURE | ✅ FOUND | **14**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `ui/interfaces/navigation_service_interface.py` | ✅ SECURE | ✅ FOUND | **12**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `ui/interfaces/page_interface.py` | ✅ SECURE | ✅ FOUND | **11**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `ui/interfaces/strategy_service_interface.py` | ✅ SECURE | ✅ FOUND | **17**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `ui/pages/01_🚀_Launchpad.py` | ✅ SECURE | ✅ FOUND | **10**/0/0/0 | 89% / 50% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ✅ | - |
| `ui/pages/02_🛠️_Dev_Center.py` | ✅ SECURE | ✅ FOUND | **10**/0/0/0 | 81% / 50% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `ui/pages/03_📥_Data_Hub.py` | 🟡 WARNING | ✅ FOUND | **11**/0/0/0 | 39% / 23% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 📊 Coverage növelése: 39% → 100% |
| `ui/pages/04_🧠_AI_Lab.py` | ✅ SECURE | ✅ FOUND | **10**/0/0/0 | 81% / 50% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `ui/pages/05_🪲_Strategy_Lab.py` | 🟡 WARNING | ✅ FOUND | **26**/0/0/0 | 39% / 32% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 📊 Coverage növelése: 39% → 100% |
| `ui/pages/06_⚡_Live_Ops.py` | 🟡 WARNING | ✅ FOUND | **10**/0/0/0 | 79% / 50% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 📊 Coverage növelése: 79% → 100% |
| `ui/pages/__init__.py` | ✅ SECURE | ✅ FOUND | **10**/0/0/0 | 88% / 50% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `ui/services/__init__.py` | ✅ SECURE | ✅ FOUND | **9**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `ui/services/ai_service.py` | ✅ SECURE | ✅ FOUND | **15**/0/0/0 | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ✅ | - |
| `ui/services/dashboard_service.py` | ✅ SECURE | ✅ FOUND | **13**/0/0/0 | 98% / 95% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ✅ | - |
| `ui/services/data_service.py` | 🟡 WARNING | ✅ FOUND | **17**/0/0/0 | 35% / 27% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ✅ | 📊 Coverage növelése: 35% → 100% |
| `ui/services/live_ops_service.py` | ✅ SECURE | ✅ FOUND | **16**/0/0/0 | 95% / 83% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ✅ | - |
| `ui/services/navigation_service.py` | ✅ SECURE | ✅ FOUND | **16**/0/0/0 | 98% / 92% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ✅ | - |
| `ui/services/strategy_service.py` | 🟡 WARNING | ✅ FOUND | **19**/0/0/0 | 56% / 46% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ✅ | 📊 Coverage növelése: 56% → 100% |
| `ui/streamlit_app.py` | 🟡 WARNING | ✅ FOUND | **8**/0/0/0 | 58% / 31% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | 📊 Coverage növelése: 58% → 100% |

## 6. Tests Layer (`tests/`)

| Fájl | Státusz | Pass/Fail/Err/Skip | Coverage (Stmt/Brch) | Lint/Mypy/Pylance | Src Warn | Dokumentálva | Teendők |
|:-----|:--------|:-------------------|:---------------------|:------------------|:---------|:-------------|:--------|
| `tests/__init__.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/conftest.py` | 🟡 WARNING | - | N/A | 0 / 0 / 9 | 6 | ✅ | 🔎 Pylance: 9 hiba javítása | ⚠️ 6 warning javítása |
| `tests/neural_ai/__init__.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/collectors/__init__.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/collectors/jforex/__init__.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/collectors/jforex/exceptions/__init__.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/collectors/jforex/exceptions/test_jforex_error.py` | ✅ SECURE | **15**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/collectors/jforex/exceptions/test_jforex_exceptions_init.py` | ✅ SECURE | **5**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/collectors/jforex/implementations/__init__.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/collectors/jforex/implementations/test_jforex_implementations_init.py` | ✅ SECURE | **5**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/collectors/jforex/interfaces/__init__.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/collectors/jforex/interfaces/test_jforex_downloader_interface.py` | ✅ SECURE | **7**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/collectors/jforex/interfaces/test_jforex_interfaces_init.py` | ✅ SECURE | **3**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/collectors/jforex/interfaces/test_jforex_live_interface.py` | ✅ SECURE | **7**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/collectors/jforex/interfaces/test_jforex_tick_data.py` | ✅ SECURE | **10**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/collectors/jforex/mocks/__init__.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/collectors/jforex/test_bi5_downloader.py` | ✅ SECURE | **43**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/collectors/jforex/test_jforex_factory.py` | ✅ SECURE | **10**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/collectors/jforex/test_jforex_init.py` | ✅ SECURE | **2**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/collectors/jforex/test_live_feed.py` | ✅ SECURE | **12**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/collectors/jforex/test_live_feed_integration.py` | ✅ SECURE | **8**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/collectors/test_collectors_init.py` | ✅ SECURE | **10**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/base/exceptions/test_base_error.py` | ✅ SECURE | **42**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/base/exceptions/test_base_exceptions_init.py` | ✅ SECURE | **18**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/base/implementations/test_base_implementations_init.py` | ✅ SECURE | **3**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/base/implementations/test_component_bundle.py` | ✅ SECURE | **39**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/base/implementations/test_di_container.py` | ✅ SECURE | **32**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/base/implementations/test_lazy_loader.py` | ✅ SECURE | **10**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/base/implementations/test_singleton.py` | ✅ SECURE | **10**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/base/interfaces/test_base_interfaces_init.py` | ✅ SECURE | **12**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/base/interfaces/test_component_interface.py` | ✅ SECURE | **13**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/base/interfaces/test_container_interface.py` | ✅ SECURE | **20**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/base/test_base_factory.py` | ✅ SECURE | **35**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/base/test_base_factory_functional.py` | 🟡 WARNING | **0**/0/0/1 | N/A | 0 / 0 / 0 | - | ✅ | ⏭️ 1 skipped teszt aktiválása |
| `tests/neural_ai/core/base/test_base_init.py` | ✅ SECURE | **7**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/config/exceptions/test_config_error.py` | ✅ SECURE | **15**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/config/exceptions/test_config_exceptions_init.py` | ✅ SECURE | **22**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/config/implementations/test_config_implementations_init.py` | 🔴 VULNERABLE | **5**/1/0/0 | N/A | 0 / 0 / 0 | - | ✅ | 🔴 **Tesztek javítása: 1 failed, 0 error** |
| `tests/neural_ai/core/config/implementations/test_dynamic_config_manager.py` | ✅ SECURE | **61**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/config/implementations/test_yaml_config_manager.py` | ✅ SECURE | **76**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/config/interfaces/test_async_config_interface.py` | ✅ SECURE | **25**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/config/interfaces/test_config_factory_interface.py` | 🟡 WARNING | **23**/0/0/0 | N/A | 0 / 0 / 0 | - | ❌ | 📝 Dokumentáció írása |
| `tests/neural_ai/core/config/interfaces/test_config_interface.py` | ✅ SECURE | **17**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/config/interfaces/test_config_interfaces_init.py` | ✅ SECURE | **16**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/config/interfaces/test_types.py` | ✅ SECURE | **28**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/config/test_config_factory.py` | ✅ SECURE | **27**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/config/test_config_init.py` | ✅ SECURE | **10**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/config/test_processors_config.py` | ✅ SECURE | **26**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/db/conftest.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/db/exceptions/test_db_error.py` | ✅ SECURE | **9**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/db/exceptions/test_db_exceptions_init.py` | ✅ SECURE | **5**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/db/implementations/test_db_implementations_init.py` | ✅ SECURE | **3**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/db/implementations/test_model_base.py` | ✅ SECURE | **12**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/db/implementations/test_models.py` | ✅ SECURE | **22**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/db/implementations/test_sqlalchemy_session.py` | 🟡 WARNING | **21**/0/0/16 | N/A | 0 / 1 / 3 | - | ✅ | 🔬 Mypy: 1 type hiba javítása | 🔎 Pylance: 3 hiba javítása | ⏭️ 16 skipped teszt aktiválása |
| `tests/neural_ai/core/db/interfaces/test_db_interfaces_init.py` | ✅ SECURE | **4**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/db/test_db_factory.py` | ✅ SECURE | **22**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/db/test_db_init.py` | ✅ SECURE | **20**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/events/exceptions/test_event_error.py` | ✅ SECURE | **9**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/events/exceptions/test_events_exceptions_init.py` | ✅ SECURE | **5**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/events/implementations/test_events_implementations_init.py` | ✅ SECURE | **3**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/events/implementations/test_zeromq_bus.py` | ✅ SECURE | **49**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/events/interfaces/test_event_bus_interface.py` | ✅ SECURE | **27**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/events/interfaces/test_event_models.py` | ✅ SECURE | **26**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/events/interfaces/test_events_interfaces_init.py` | ✅ SECURE | **11**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/events/test_events_factory.py` | ✅ SECURE | **14**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/events/test_events_init.py` | ✅ SECURE | **10**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/logger/exceptions/test_logger_error.py` | ✅ SECURE | **14**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/logger/exceptions/test_logger_exceptions_init.py` | ✅ SECURE | **16**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/logger/formatters/test_logger_formatters.py` | ✅ SECURE | **6**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/logger/implementations/test_colored_logger.py` | ✅ SECURE | **9**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/logger/implementations/test_default_logger.py` | ✅ SECURE | **8**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/logger/implementations/test_logger_implementations_init.py` | ✅ SECURE | **5**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/logger/implementations/test_rotating_file_logger.py` | ✅ SECURE | **7**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/logger/interfaces/test_logger_factory_interface.py` | ✅ SECURE | **5**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/logger/interfaces/test_logger_interface.py` | ✅ SECURE | **3**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/logger/interfaces/test_logger_interfaces_init.py` | ✅ SECURE | **15**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/logger/test_logger_factory.py` | ✅ SECURE | **12**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/logger/test_logger_init.py` | ✅ SECURE | **7**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/system/exceptions/test_health_error.py` | ✅ SECURE | **17**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/system/exceptions/test_system_exceptions_init.py` | ✅ SECURE | **18**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/system/implementations/test_health_monitor.py` | ✅ SECURE | **28**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/system/interfaces/test_health_interface.py` | ✅ SECURE | **22**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/system/interfaces/test_system_interfaces_init.py` | ✅ SECURE | **22**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/system/test_system_factory.py` | ✅ SECURE | **19**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/system/test_system_init.py` | ✅ SECURE | **24**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/test_core_init.py` | 🔴 VULNERABLE | **15**/7/0/0 | N/A | 0 / 0 / 0 | - | ✅ | 🔴 **Tesztek javítása: 7 failed, 0 error** |
| `tests/neural_ai/core/utils/exceptions/test_util_error.py` | ✅ SECURE | **12**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/utils/exceptions/test_utils_exceptions_init.py` | ✅ SECURE | **5**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/utils/implementations/test_utils_implementations_init.py` | ✅ SECURE | **5**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/utils/interfaces/test_hardware_interface.py` | ✅ SECURE | **3**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/utils/interfaces/test_utils_interfaces_init.py` | ✅ SECURE | **4**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/utils/test_decorators.py` | ✅ SECURE | **13**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/utils/test_hardware_info.py` | ✅ SECURE | **15**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/utils/test_utils_factory.py` | ✅ SECURE | **11**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/core/utils/test_utils_init.py` | ✅ SECURE | **6**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/data/ingestion/test_ingestion_init.py` | ✅ SECURE | **4**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/data/ingestion/test_market_data_persister.py` | 🟡 WARNING | **20**/0/0/5 | N/A | 0 / 0 / 0 | - | ✅ | ⏭️ 5 skipped teszt aktiválása |
| `tests/neural_ai/data/storage/backends/test_pandas_backend.py` | ✅ SECURE | **30**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/data/storage/backends/test_polars_backend.py` | 🟡 WARNING | **24**/0/0/6 | N/A | 0 / 0 / 0 | - | ✅ | ⏭️ 6 skipped teszt aktiválása |
| `tests/neural_ai/data/storage/backends/test_storage_backends_base.py` | 🟡 WARNING | **8**/0/0/0 | N/A | 0 / 0 / 0 | - | ❌ | 📝 Dokumentáció írása |
| `tests/neural_ai/data/storage/backends/test_storage_backends_init.py` | ✅ SECURE | **5**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/data/storage/exceptions/test_storage_exceptions_init.py` | ✅ SECURE | **23**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/data/storage/implementations/test_file_storage.py` | 🟡 WARNING | **50**/0/0/2 | N/A | 0 / 0 / 0 | - | ✅ | ⏭️ 2 skipped teszt aktiválása |
| `tests/neural_ai/data/storage/implementations/test_parquet_storage.py` | ✅ SECURE | **34**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/data/storage/implementations/test_storage_implementations_init.py` | ✅ SECURE | **5**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/data/storage/interfaces/test_storage_factory_interface.py` | ✅ SECURE | **6**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/data/storage/interfaces/test_storage_interface.py` | ✅ SECURE | **11**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/data/storage/interfaces/test_storage_interfaces_init.py` | ✅ SECURE | **13**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/data/storage/test_storage_factory.py` | ✅ SECURE | **12**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/data/storage/test_storage_init.py` | ✅ SECURE | **5**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/data/test_data_init.py` | ✅ SECURE | **2**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/processors/__init__.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/processors/conftest.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/processors/dimensions/d01_price/test_d01_factory.py` | ✅ SECURE | **2**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/processors/dimensions/d01_price/test_d01_price_init.py` | ✅ SECURE | **2**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/processors/dimensions/d01_price/test_d01_processor.py` | ✅ SECURE | **9**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/processors/dimensions/d01_price/test_processor.py` | ✅ SECURE | **18**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/processors/dimensions/d02_support/exceptions/test_d02_support_exceptions_init.py` | ✅ SECURE | **2**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/processors/dimensions/d02_support/exceptions/test_support_error.py` | ✅ SECURE | **9**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/processors/dimensions/d02_support/implementations/test_d02_support_implementations_init.py` | ✅ SECURE | **2**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/processors/dimensions/d02_support/implementations/test_support_processor.py` | ✅ SECURE | **26**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/processors/dimensions/d02_support/interfaces/test_d02_support_interfaces_init.py` | ✅ SECURE | **2**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/processors/dimensions/d02_support/test_d02_support_factory.py` | ✅ SECURE | **2**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/processors/dimensions/d02_support/test_d02_support_init.py` | ✅ SECURE | **2**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/processors/dimensions/test_dimensions_base.py` | 🟡 WARNING | **8**/0/0/0 | N/A | 0 / 0 / 0 | - | ❌ | 📝 Dokumentáció írása |
| `tests/neural_ai/processors/dimensions/test_dimensions_init.py` | ✅ SECURE | **2**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/processors/implementations/test_processors_implementations_init.py` | ✅ SECURE | **2**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/processors/implementations/test_time_alignment_service.py` | ✅ SECURE | **8**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/processors/interfaces/test_processors_dimension_processor_interface.py` | ✅ SECURE | **7**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/processors/interfaces/test_processors_interfaces_init.py` | ✅ SECURE | **3**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/processors/interfaces/test_processors_tensor_converter_interface.py` | ✅ SECURE | **7**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/processors/interfaces/test_processors_time_alignment_interface.py` | ✅ SECURE | **8**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/processors/resampler_service/__init__.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/processors/resampler_service/exceptions/test_resampler_error.py` | ✅ SECURE | **17**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/processors/resampler_service/interfaces/test_resampler_resampler_interface.py` | ✅ SECURE | **7**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/processors/resampler_service/test_resampler_factory.py` | ✅ SECURE | **7**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/processors/resampler_service/test_resampler_service.py` | ✅ SECURE | **35**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/processors/resampler_service/test_resampler_service_init.py` | ✅ SECURE | **6**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/processors/test_processors_factory.py` | ✅ SECURE | **3**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/processors/test_processors_init.py` | ✅ SECURE | **4**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/test_neural_ai_init.py` | ✅ SECURE | **21**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/ui/components/test_base_widget.py` | ✅ SECURE | **10**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/ui/components/test_components_init.py` | ✅ SECURE | **9**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/ui/interfaces/test_ai_service_interface.py` | ✅ SECURE | **11**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/ui/interfaces/test_core_bridge_interface.py` | ✅ SECURE | **13**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/ui/interfaces/test_dashboard_service_interface.py` | ✅ SECURE | **10**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/ui/interfaces/test_data_service_interface.py` | ✅ SECURE | **19**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/ui/interfaces/test_live_ops_service_interface.py` | ✅ SECURE | **14**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/ui/interfaces/test_navigation_service_interface.py` | ✅ SECURE | **12**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/ui/interfaces/test_page_interface.py` | ✅ SECURE | **11**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/ui/interfaces/test_strategy_service_interface.py` | ✅ SECURE | **17**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/ui/interfaces/test_ui_interfaces_init.py` | ✅ SECURE | **17**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/ui/pages/test_ai_lab_page.py` | ✅ SECURE | **10**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/ui/pages/test_data_hub_page.py` | ✅ SECURE | **11**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/ui/pages/test_dev_center_page.py` | ✅ SECURE | **10**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/ui/pages/test_launchpad_page.py` | ✅ SECURE | **10**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/ui/pages/test_live_ops_page.py` | ✅ SECURE | **10**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/ui/pages/test_pages_init.py` | ✅ SECURE | **10**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/ui/pages/test_strategy_lab_page.py` | ✅ SECURE | **26**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/ui/services/test_ai_service.py` | ✅ SECURE | **15**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/ui/services/test_dashboard_service.py` | ✅ SECURE | **13**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/ui/services/test_data_service.py` | ✅ SECURE | **17**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/ui/services/test_live_ops_service.py` | ✅ SECURE | **16**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/ui/services/test_navigation_service.py` | ✅ SECURE | **16**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/ui/services/test_services_init.py` | ✅ SECURE | **9**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/ui/services/test_strategy_service.py` | ✅ SECURE | **19**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/ui/test_app.py` | ✅ SECURE | **16**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/ui/test_core_bridge.py` | ✅ SECURE | **20**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/ui/test_streamlit_app.py` | ✅ SECURE | **8**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/neural_ai/ui/test_ui_factory.py` | 🟡 WARNING | **15**/0/0/0 | N/A | 0 / 2 / 2 | - | ✅ | 🔬 Mypy: 2 type hiba javítása | 🔎 Pylance: 2 hiba javítása |
| `tests/neural_ai/ui/test_ui_init.py` | ✅ SECURE | **9**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/scripts/__init__.py` | ✅ SECURE | - | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/scripts/test_audit_architecture.py` | 🟡 WARNING | **7**/0/0/0 | N/A | 0 / 0 / 0 | 1 | ✅ | ⚠️ 1 warning javítása |
| `tests/scripts/test_audit_architecture_detailed.py` | ✅ SECURE | **5**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/scripts/test_audit_data.py` | ✅ SECURE | **7**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/scripts/test_bootstrap_integration_test.py` | ✅ SECURE | **6**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/scripts/test_bootstrap_test.py` | ✅ SECURE | **7**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/scripts/test_data_reset.py` | ✅ SECURE | **14**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/scripts/test_deploy_jforex.py` | ✅ SECURE | **5**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/scripts/test_download_history.py` | ✅ SECURE | **11**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/scripts/test_force_kill.py` | ✅ SECURE | **5**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/scripts/test_generate.py` | ✅ SECURE | **5**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/scripts/test_generate_docs.py` | ✅ SECURE | **5**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/scripts/test_install.py` | ✅ SECURE | **5**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/scripts/test_migrate_structure.py` | ✅ SECURE | **13**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/scripts/test_scripts_init.py` | ✅ SECURE | **3**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/scripts/test_smart_pack.py` | ✅ SECURE | **5**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/scripts/test_test_d2_standalone.py` | ✅ SECURE | **5**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/scripts/test_test_tick_pipeline.py` | ✅ SECURE | **5**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |
| `tests/scripts/test_validation_end_to_end.py` | 🔴 VULNERABLE | **2**/1/0/0 | N/A | 0 / 0 / 0 | - | ✅ | 🔴 **Tesztek javítása: 1 failed, 0 error** |
| `tests/test_main.py` | ✅ SECURE | **29**/0/0/0 | N/A | 0 / 0 / 0 | - | ✅ | - |

## 7. Scripts Layer (`scripts/`)

| Fájl | Státusz | Teszt Pár | Pass/Fail/Err/Skip | Coverage (Stmt/Brch) | Lint/Mypy/Pylance | Src Warn | Config | Logger | Dokumentálva | Teendők |
|:-----|:--------|:----------|:-------------------|:---------------------|:------------------|:---------|:-------|:-------|:-------------|:--------|
| `scripts/__init__.py` | ✅ SECURE | ✅ FOUND | - | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `scripts/audit_architecture.py` | ✅ SECURE | ✅ FOUND | - | 18% / 9% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `scripts/audit_architecture_detailed.py` | 🟡 WARNING | ✅ FOUND | - | 9% / 1% | 0 / 0 / 3 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔎 Pylance: 3 hiba javítása |
| `scripts/audit_data.py` | ✅ SECURE | ✅ FOUND | - | 10% / 2% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `scripts/bootstrap_integration_test.py` | ✅ SECURE | ✅ FOUND | - | 10% / 6% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `scripts/bootstrap_test.py` | ✅ SECURE | ✅ FOUND | - | 9% / 8% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `scripts/data_reset.py` | ✅ SECURE | ✅ FOUND | - | 96% / 88% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `scripts/deploy_jforex.py` | ✅ SECURE | ✅ FOUND | - | 7% / 3% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `scripts/download_history.py` | ✅ SECURE | ✅ FOUND | - | 14% / 9% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `scripts/force_kill.py` | ✅ SECURE | ✅ FOUND | - | 8% / 5% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `scripts/generate.py` | 🟡 WARNING | ✅ FOUND | - | 8% / 0% | 0 / 0 / 1 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔎 Pylance: 1 hiba javítása |
| `scripts/generate_docs.py` | 🟡 WARNING | ✅ FOUND | - | 15% / 1% | 0 / 0 / 10 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔎 Pylance: 10 hiba javítása |
| `scripts/install.py` | ✅ SECURE | ✅ FOUND | - | 14% / 2% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `scripts/migrate_structure.py` | ✅ SECURE | ✅ FOUND | - | 93% / 88% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `scripts/smart_pack.py` | ✅ SECURE | ✅ FOUND | - | 13% / 2% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `scripts/test_d2_standalone.py` | 🟡 WARNING | ✅ FOUND | - | 12% / 6% | 0 / 0 / 23 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔎 Pylance: 23 hiba javítása |
| `scripts/test_tick_pipeline.py` | ✅ SECURE | ✅ FOUND | - | 79% / 64% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ✅ | - |
| `scripts/validation_end_to_end.py` | 🟡 WARNING | ✅ FOUND | - | N/A | 0 / 0 / 11 | - | ⚪ N/A | ⚪ N/A | ✅ | 🔎 Pylance: 11 hiba javítása |
