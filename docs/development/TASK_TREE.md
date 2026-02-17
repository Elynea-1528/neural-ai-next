# 🌳 NEURAL AI NEXT - TASK TREE

**Generálva:** 2026-02-17 19:49:20 UTC
**Módszer:** Hibrid (AST + Pytest + Coverage + Ruff + Mypy + Pylance)
**Fájlok száma:** 156

## 📊 Statisztika

- ✅ **SECURE:** 0 (0.0%)
- 🟡 **WARNING:** 56 (35.9%)
- 🔴 **VULNERABLE:** 100 (64.1%)

---

## 0. Root Layer (`./`)

| Modul / Fájl | Státusz | Teszt Pár | Pass/Fail/Err/Skip | Coverage (Stmt/Brch) | Lint/Mypy/Pylance | Src Warn | Config | Logger | Dokumentálva | Teendők |
|:-------------|:--------|:----------|:-------------------|:---------------------|:------------------|:---------|:-------|:-------|:-------------|:--------|
| `main.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `neural_ai/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | 83% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |

## 1. Infrastructure Layer (`neural_ai/core/`)

| Modul / Fájl | Státusz | Teszt Pár | Pass/Fail/Err/Skip | Coverage (Stmt/Brch) | Lint/Mypy/Pylance | Src Warn | Config | Logger | Dokumentálva | Teendők |
|:-------------|:--------|:----------|:-------------------|:---------------------|:------------------|:---------|:-------|:-------|:-------------|:--------|
| `core/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | 11% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) | 📊 Coverage növelése: 11% → 80%+ |
| `core/base/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/base/exceptions/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/base/exceptions/base_error.py` | 🟡 WARNING | ✅ FOUND | - | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 📝 Dokumentáció írása (docs/components/) |
| `core/base/factory.py` | 🟡 WARNING | ✅ FOUND | - | 23% / 0% | 0 / 0 / 0 | - | ✅ OK | ⚪ N/A | ❌ | 📝 Dokumentáció írása (docs/components/) | 📊 Coverage növelése: 23% → 80%+ |
| `core/base/implementations/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/base/implementations/component_bundle.py` | 🟡 WARNING | ✅ FOUND | - | 39% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 📝 Dokumentáció írása (docs/components/) | 📊 Coverage növelése: 39% → 80%+ |
| `core/base/implementations/di_container.py` | 🟡 WARNING | ✅ FOUND | - | 28% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 📝 Dokumentáció írása (docs/components/) | 📊 Coverage növelése: 28% → 80%+ |
| `core/base/implementations/lazy_loader.py` | 🟡 WARNING | ✅ FOUND | - | 43% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 📝 Dokumentáció írása (docs/components/) | 📊 Coverage növelése: 43% → 80%+ |
| `core/base/implementations/singleton.py` | 🟡 WARNING | ✅ FOUND | - | 43% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 📝 Dokumentáció írása (docs/components/) | 📊 Coverage növelése: 43% → 80%+ |
| `core/base/interfaces/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/base/interfaces/component_interface.py` | 🟡 WARNING | ✅ FOUND | - | 76% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 📝 Dokumentáció írása (docs/components/) | 📊 Coverage növelése: 76% → 80%+ |
| `core/base/interfaces/container_interface.py` | 🟡 WARNING | ✅ FOUND | - | 75% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 📝 Dokumentáció írása (docs/components/) | 📊 Coverage növelése: 75% → 80%+ |
| `core/config/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/config/exceptions/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/config/exceptions/config_error.py` | 🟡 WARNING | ✅ FOUND | - | 40% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 📝 Dokumentáció írása (docs/components/) | 📊 Coverage növelése: 40% → 80%+ |
| `core/config/factory.py` | 🟡 WARNING | ✅ FOUND | - | 26% / 0% | 0 / 0 / 4 | - | ⚪ N/A | ⚪ N/A | ❌ | 📝 Dokumentáció írása (docs/components/) | 🔎 Pylance: 4 hiba javítása | 📊 Coverage növelése: 26% → 80%+ |
| `core/config/implementations/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | 78% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) | 📊 Coverage növelése: 78% → 80%+ |
| `core/config/implementations/dynamic_config_manager.py` | 🟡 WARNING | ✅ FOUND | - | 10% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ❌ | 📝 Dokumentáció írása (docs/components/) | 📊 Coverage növelése: 10% → 80%+ |
| `core/config/implementations/yaml_config_manager.py` | 🟡 WARNING | ✅ FOUND | - | 13% / 0% | 0 / 0 / 22 | - | ⚪ N/A | ⚠️ UNUSED | ❌ | 📝 Dokumentáció írása (docs/components/) | 🔎 Pylance: 22 hiba javítása | 📊 Coverage növelése: 13% → 80%+ |
| `core/config/interfaces/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/config/interfaces/async_config_interface.py` | 🟡 WARNING | ✅ FOUND | - | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ❌ | 📝 Dokumentáció írása (docs/components/) |
| `core/config/interfaces/config_interface.py` | 🟡 WARNING | ✅ FOUND | - | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 📝 Dokumentáció írása (docs/components/) |
| `core/config/interfaces/factory_interface.py` | 🟡 WARNING | ✅ FOUND | - | 80% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 📝 Dokumentáció írása (docs/components/) |
| `core/config/interfaces/types.py` | 🔴 VULNERABLE | ❌ MISSING | - | 84% / 0% | 0 / 0 / 0 | - | ✅ OK | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/db/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/db/exceptions/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/db/exceptions/db_error.py` | 🟡 WARNING | ✅ FOUND | - | 54% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 📝 Dokumentáció írása (docs/components/) | 📊 Coverage növelése: 54% → 80%+ |
| `core/db/factory.py` | 🟡 WARNING | ✅ FOUND | - | 62% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ❌ | 📝 Dokumentáció írása (docs/components/) | 📊 Coverage növelése: 62% → 80%+ |
| `core/db/implementations/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/db/implementations/model_base.py` | 🟡 WARNING | ✅ FOUND | - | 52% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 📝 Dokumentáció írása (docs/components/) | 📊 Coverage növelése: 52% → 80%+ |
| `core/db/implementations/models.py` | 🟡 WARNING | ✅ FOUND | - | 92% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 📝 Dokumentáció írása (docs/components/) |
| `core/db/implementations/sqlalchemy_session.py` | 🟡 WARNING | ✅ FOUND | - | 17% / 0% | 0 / 0 / 10 | - | ⚪ N/A | ✅ OK | ❌ | 📝 Dokumentáció írása (docs/components/) | 🔎 Pylance: 10 hiba javítása | 📊 Coverage növelése: 17% → 80%+ |
| `core/db/interfaces/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/events/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/events/exceptions/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/events/exceptions/event_error.py` | 🟡 WARNING | ✅ FOUND | - | 54% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 📝 Dokumentáció írása (docs/components/) | 📊 Coverage növelése: 54% → 80%+ |
| `core/events/factory.py` | 🟡 WARNING | ✅ FOUND | - | 28% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ❌ | 📝 Dokumentáció írása (docs/components/) | 📊 Coverage növelése: 28% → 80%+ |
| `core/events/implementations/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/events/implementations/zeromq_bus.py` | 🟡 WARNING | ✅ FOUND | - | 14% / 0% | 0 / 0 / 20 | - | ✅ OK | ⚠️ UNUSED | ❌ | 📝 Dokumentáció írása (docs/components/) | 🔎 Pylance: 20 hiba javítása | 📊 Coverage növelése: 14% → 80%+ |
| `core/events/interfaces/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/events/interfaces/event_bus_interface.py` | 🟡 WARNING | ✅ FOUND | - | 100% / 100% | 0 / 0 / 0 | - | ✅ OK | ⚪ N/A | ❌ | 📝 Dokumentáció írása (docs/components/) |
| `core/events/interfaces/event_models.py` | 🟡 WARNING | ✅ FOUND | - | 64% / 0% | 0 / 0 / 0 | - | ✅ OK | ⚪ N/A | ❌ | 📝 Dokumentáció írása (docs/components/) | 📊 Coverage növelése: 64% → 80%+ |
| `core/logger/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | 88% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/logger/exceptions/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/logger/exceptions/logger_error.py` | 🟡 WARNING | ✅ FOUND | - | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 📝 Dokumentáció írása (docs/components/) |
| `core/logger/factory.py` | 🟡 WARNING | ✅ FOUND | - | 30% / 11% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 📝 Dokumentáció írása (docs/components/) | 📊 Coverage növelése: 30% → 80%+ |
| `core/logger/formatters/logger_formatters.py` | 🟡 WARNING | ✅ FOUND | - | 45% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 📝 Dokumentáció írása (docs/components/) | 📊 Coverage növelése: 45% → 80%+ |
| `core/logger/implementations/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/logger/implementations/colored_logger.py` | 🔴 VULNERABLE | ✅ FOUND | - | 32% / 0% | 0 / 0 / 0 | - | ⚪ N/A | 🔴 MISSING | ❌ | 🔴 **Logger DI hiányzik!** | 📝 Dokumentáció írása (docs/components/) | 📊 Coverage növelése: 32% → 80%+ |
| `core/logger/implementations/default_logger.py` | 🔴 VULNERABLE | ✅ FOUND | - | 70% / 100% | 0 / 0 / 0 | - | ⚪ N/A | 🔴 MISSING | ❌ | 🔴 **Logger DI hiányzik!** | 📝 Dokumentáció írása (docs/components/) | 📊 Coverage növelése: 70% → 80%+ |
| `core/logger/implementations/rotating_file_logger.py` | 🔴 VULNERABLE | ✅ FOUND | - | 22% / 0% | 0 / 0 / 0 | - | ⚪ N/A | 🔴 MISSING | ❌ | 🔴 **Logger DI hiányzik!** | 📝 Dokumentáció írása (docs/components/) | 📊 Coverage növelése: 22% → 80%+ |
| `core/logger/interfaces/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | 78% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) | 📊 Coverage növelése: 78% → 80%+ |
| `core/logger/interfaces/factory_interface.py` | 🔴 VULNERABLE | ❌ MISSING | - | 81% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/logger/interfaces/logger_interface.py` | 🟡 WARNING | ✅ FOUND | - | 70% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 📝 Dokumentáció írása (docs/components/) | 📊 Coverage növelése: 70% → 80%+ |
| `core/system/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/system/exceptions/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/system/exceptions/health_error.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/system/factory.py` | 🟡 WARNING | ✅ FOUND | - | 35% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 📝 Dokumentáció írása (docs/components/) | 📊 Coverage növelése: 35% → 80%+ |
| `core/system/implementations/health_monitor.py` | 🟡 WARNING | ✅ FOUND | - | 11% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ❌ | 📝 Dokumentáció írása (docs/components/) | 📊 Coverage növelése: 11% → 80%+ |
| `core/system/interfaces/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/system/interfaces/health_interface.py` | 🟡 WARNING | ✅ FOUND | - | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 📝 Dokumentáció írása (docs/components/) |
| `core/utils/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/utils/decorators.py` | 🟡 WARNING | ✅ FOUND | - | 39% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 📝 Dokumentáció írása (docs/components/) | 📊 Coverage növelése: 39% → 80%+ |
| `core/utils/exceptions/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/utils/exceptions/util_error.py` | 🔴 VULNERABLE | ❌ MISSING | - | 56% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) | 📊 Coverage növelése: 56% → 80%+ |
| `core/utils/factory.py` | 🟡 WARNING | ✅ FOUND | - | 60% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 📝 Dokumentáció írása (docs/components/) | 📊 Coverage növelése: 60% → 80%+ |
| `core/utils/implementations/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/utils/implementations/hardware_info.py` | 🟡 WARNING | ✅ FOUND | - | 19% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 📝 Dokumentáció írása (docs/components/) | 📊 Coverage növelése: 19% → 80%+ |
| `core/utils/interfaces/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `core/utils/interfaces/hardware_interface.py` | 🟡 WARNING | ✅ FOUND | - | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 📝 Dokumentáció írása (docs/components/) |

## 2. Input Layer (`neural_ai/collectors/`)

| Modul / Fájl | Státusz | Teszt Pár | Pass/Fail/Err/Skip | Coverage (Stmt/Brch) | Lint/Mypy/Pylance | Src Warn | Config | Logger | Dokumentálva | Teendők |
|:-------------|:--------|:----------|:-------------------|:---------------------|:------------------|:---------|:-------|:-------|:-------------|:--------|
| `collectors/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `collectors/jforex/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `collectors/jforex/exceptions/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `collectors/jforex/exceptions/jforex_error.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `collectors/jforex/factory.py` | 🟡 WARNING | ✅ FOUND | - | 19% / 0% | 0 / 0 / 2 | - | ⚪ N/A | ⚪ N/A | ❌ | 📝 Dokumentáció írása (docs/components/) | 🔎 Pylance: 2 hiba javítása | 📊 Coverage növelése: 19% → 80%+ |
| `collectors/jforex/implementations/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `collectors/jforex/implementations/bi5_downloader.py` | 🟡 WARNING | ✅ FOUND | - | 8% / 0% | 0 / 0 / 2 | - | ⚪ N/A | ⚠️ UNUSED | ❌ | 📝 Dokumentáció írása (docs/components/) | 🔎 Pylance: 2 hiba javítása | 📊 Coverage növelése: 8% → 80%+ |
| `collectors/jforex/implementations/live_feed.py` | 🟡 WARNING | ✅ FOUND | - | 13% / 0% | 0 / 0 / 3 | - | ⚪ N/A | ✅ OK | ❌ | 📝 Dokumentáció írása (docs/components/) | 🔎 Pylance: 3 hiba javítása | 📊 Coverage növelése: 13% → 80%+ |
| `collectors/jforex/interfaces/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `collectors/jforex/interfaces/downloader_interface.py` | 🔴 VULNERABLE | ❌ MISSING | - | 75% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) | 📊 Coverage növelése: 75% → 80%+ |
| `collectors/jforex/interfaces/live_interface.py` | 🔴 VULNERABLE | ❌ MISSING | - | 73% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) | 📊 Coverage növelése: 73% → 80%+ |
| `collectors/jforex/interfaces/tick_data.py` | 🔴 VULNERABLE | ❌ MISSING | - | 88% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |

## 3. Persistence Layer (`neural_ai/data/`)

| Modul / Fájl | Státusz | Teszt Pár | Pass/Fail/Err/Skip | Coverage (Stmt/Brch) | Lint/Mypy/Pylance | Src Warn | Config | Logger | Dokumentálva | Teendők |
|:-------------|:--------|:----------|:-------------------|:---------------------|:------------------|:---------|:-------|:-------|:-------------|:--------|
| `data/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `data/ingestion/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `data/ingestion/market_data_persister.py` | 🟡 WARNING | ✅ FOUND | - | 7% / 0% | 0 / 0 / 10 | - | ⚪ N/A | ✅ OK | ❌ | 📝 Dokumentáció írása (docs/components/) | 🔎 Pylance: 10 hiba javítása | 📊 Coverage növelése: 7% → 80%+ |
| `data/storage/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | 83% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `data/storage/backends/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `data/storage/backends/base.py` | 🟡 WARNING | ✅ FOUND | - | 32% / 6% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ❌ | 📝 Dokumentáció írása (docs/components/) | 📊 Coverage növelése: 32% → 80%+ |
| `data/storage/backends/pandas_backend.py` | 🟡 WARNING | ✅ FOUND | - | 19% / 3% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ❌ | 📝 Dokumentáció írása (docs/components/) | 📊 Coverage növelése: 19% → 80%+ |
| `data/storage/backends/polars_backend.py` | 🟡 WARNING | ✅ FOUND | - | 16% / 2% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ❌ | 📝 Dokumentáció írása (docs/components/) | 📊 Coverage növelése: 16% → 80%+ |
| `data/storage/exceptions/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | 82% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `data/storage/factory.py` | 🟡 WARNING | ✅ FOUND | - | 28% / 0% | 0 / 0 / 5 | - | ⚪ N/A | ⚪ N/A | ❌ | 📝 Dokumentáció írása (docs/components/) | 🔎 Pylance: 5 hiba javítása | 📊 Coverage növelése: 28% → 80%+ |
| `data/storage/implementations/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `data/storage/implementations/file_storage.py` | 🟡 WARNING | ✅ FOUND | - | 11% / 0% | 0 / 0 / 6 | - | ⚪ N/A | ✅ OK | ❌ | 📝 Dokumentáció írása (docs/components/) | 🔎 Pylance: 6 hiba javítása | 📊 Coverage növelése: 11% → 80%+ |
| `data/storage/implementations/parquet_storage.py` | 🟡 WARNING | ✅ FOUND | - | 12% / 0% | 0 / 0 / 21 | - | ✅ OK | ✅ OK | ❌ | 📝 Dokumentáció írása (docs/components/) | 🔎 Pylance: 21 hiba javítása | 📊 Coverage növelése: 12% → 80%+ |
| `data/storage/interfaces/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `data/storage/interfaces/factory_interface.py` | 🔴 VULNERABLE | ❌ MISSING | - | 83% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `data/storage/interfaces/storage_interface.py` | 🟡 WARNING | ✅ FOUND | - | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 📝 Dokumentáció írása (docs/components/) |

## 4. Domain Layer (`neural_ai/processors/`)

| Modul / Fájl | Státusz | Teszt Pár | Pass/Fail/Err/Skip | Coverage (Stmt/Brch) | Lint/Mypy/Pylance | Src Warn | Config | Logger | Dokumentálva | Teendők |
|:-------------|:--------|:----------|:-------------------|:---------------------|:------------------|:---------|:-------|:-------|:-------------|:--------|
| `processors/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `processors/dimensions/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `processors/dimensions/base.py` | 🔴 VULNERABLE | ❌ MISSING | - | 47% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ✅ OK | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) | 📊 Coverage növelése: 47% → 80%+ |
| `processors/dimensions/d01_price/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `processors/dimensions/d01_price/factory.py` | 🔴 VULNERABLE | ❌ MISSING | - | 86% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `processors/dimensions/d01_price/processor.py` | 🔴 VULNERABLE | ❌ MISSING | - | 8% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ✅ OK | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) | 📊 Coverage növelése: 8% → 80%+ |
| `processors/dimensions/d02_support/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `processors/dimensions/d02_support/exceptions/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `processors/dimensions/d02_support/exceptions/support_error.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `processors/dimensions/d02_support/factory.py` | 🔴 VULNERABLE | ❌ MISSING | - | 86% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `processors/dimensions/d02_support/implementations/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `processors/dimensions/d02_support/implementations/support_processor.py` | 🔴 VULNERABLE | ❌ MISSING | - | 6% / 0% | 0 / 0 / 41 | - | ⚪ N/A | ✅ OK | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) | 🔎 Pylance: 41 hiba javítása | 📊 Coverage növelése: 6% → 80%+ |
| `processors/dimensions/d02_support/interfaces/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `processors/factory.py` | 🟡 WARNING | ✅ FOUND | - | 37% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 📝 Dokumentáció írása (docs/components/) | 📊 Coverage növelése: 37% → 80%+ |
| `processors/implementations/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `processors/implementations/time_alignment_service.py` | 🟡 WARNING | ✅ FOUND | - | 18% / 0% | 0 / 0 / 3 | - | ⚪ N/A | ⚠️ UNUSED | ❌ | 📝 Dokumentáció írása (docs/components/) | 🔎 Pylance: 3 hiba javítása | 📊 Coverage növelése: 18% → 80%+ |
| `processors/interfaces/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `processors/interfaces/dimension_processor_interface.py` | 🔴 VULNERABLE | ❌ MISSING | - | 80% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `processors/interfaces/tensor_converter_interface.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `processors/interfaces/time_alignment_interface.py` | 🔴 VULNERABLE | ❌ MISSING | - | 78% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) | 📊 Coverage növelése: 78% → 80%+ |
| `processors/resampler_service/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `processors/resampler_service/exceptions/resampler_error.py` | 🔴 VULNERABLE | ❌ MISSING | - | 41% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) | 📊 Coverage növelése: 41% → 80%+ |
| `processors/resampler_service/factory.py` | 🔴 VULNERABLE | ❌ MISSING | - | 39% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) | 📊 Coverage növelése: 39% → 80%+ |
| `processors/resampler_service/implementations/resampler_service.py` | 🔴 VULNERABLE | ❌ MISSING | - | 12% / 0% | 0 / 0 / 1 | - | ⚪ N/A | ⚠️ UNUSED | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) | 🔎 Pylance: 1 hiba javítása | 📊 Coverage növelése: 12% → 80%+ |
| `processors/resampler_service/interfaces/resampler_interface.py` | 🔴 VULNERABLE | ❌ MISSING | - | 86% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |

## 5. Presentation Layer (`neural_ai/ui/`)

| Modul / Fájl | Státusz | Teszt Pár | Pass/Fail/Err/Skip | Coverage (Stmt/Brch) | Lint/Mypy/Pylance | Src Warn | Config | Logger | Dokumentálva | Teendők |
|:-------------|:--------|:----------|:-------------------|:---------------------|:------------------|:---------|:-------|:-------|:-------------|:--------|
| `ui/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `ui/app.py` | 🟡 WARNING | ✅ FOUND | - | 34% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ❌ | 📝 Dokumentáció írása (docs/components/) | 📊 Coverage növelése: 34% → 80%+ |
| `ui/components/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `ui/components/base_widget.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `ui/core_bridge.py` | 🟡 WARNING | ✅ FOUND | - | 14% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 📝 Dokumentáció írása (docs/components/) | 📊 Coverage növelése: 14% → 80%+ |
| `ui/factory.py` | 🟡 WARNING | ✅ FOUND | - | 15% / 0% | 0 / 0 / 20 | - | ⚪ N/A | ⚪ N/A | ❌ | 📝 Dokumentáció írása (docs/components/) | 🔎 Pylance: 20 hiba javítása | 📊 Coverage növelése: 15% → 80%+ |
| `ui/interfaces/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `ui/interfaces/ai_service_interface.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `ui/interfaces/core_bridge_interface.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `ui/interfaces/dashboard_service_interface.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `ui/interfaces/data_service_interface.py` | 🟡 WARNING | ✅ FOUND | - | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 📝 Dokumentáció írása (docs/components/) |
| `ui/interfaces/live_ops_service_interface.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `ui/interfaces/navigation_service_interface.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `ui/interfaces/page_interface.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `ui/interfaces/strategy_service_interface.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `ui/pages/01_🚀_Launchpad.py` | 🔴 VULNERABLE | ❌ MISSING | - | 24% / 50% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) | 📊 Coverage növelése: 24% → 80%+ |
| `ui/pages/02_🛠️_Dev_Center.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `ui/pages/03_📥_Data_Hub.py` | 🔴 VULNERABLE | ❌ MISSING | - | 9% / 2% | 0 / 0 / 3 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) | 🔎 Pylance: 3 hiba javítása | 📊 Coverage növelése: 9% → 80%+ |
| `ui/pages/04_🧠_AI_Lab.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `ui/pages/05_🪲_Strategy_Lab.py` | 🔴 VULNERABLE | ❌ MISSING | - | 6% / 1% | 0 / 0 / 99 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) | 🔎 Pylance: 99 hiba javítása | 📊 Coverage növelése: 6% → 80%+ |
| `ui/pages/06_⚡_Live_Ops.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `ui/pages/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `ui/services/__init__.py` | 🔴 VULNERABLE | ❌ MISSING | - | 100% / 100% | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
| `ui/services/ai_service.py` | 🔴 VULNERABLE | ❌ MISSING | - | 17% / 0% | 0 / 0 / 2 | - | ⚪ N/A | ⚠️ UNUSED | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) | 🔎 Pylance: 2 hiba javítása | 📊 Coverage növelése: 17% → 80%+ |
| `ui/services/dashboard_service.py` | 🟡 WARNING | ✅ FOUND | - | 17% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ❌ | 📝 Dokumentáció írása (docs/components/) | 📊 Coverage növelése: 17% → 80%+ |
| `ui/services/data_service.py` | 🟡 WARNING | ✅ FOUND | - | 8% / 0% | 0 / 0 / 18 | - | ⚪ N/A | ⚠️ UNUSED | ❌ | 📝 Dokumentáció írása (docs/components/) | 🔎 Pylance: 18 hiba javítása | 📊 Coverage növelése: 8% → 80%+ |
| `ui/services/live_ops_service.py` | 🔴 VULNERABLE | ❌ MISSING | - | 18% / 0% | 0 / 0 / 2 | - | ⚪ N/A | ⚠️ UNUSED | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) | 🔎 Pylance: 2 hiba javítása | 📊 Coverage növelése: 18% → 80%+ |
| `ui/services/navigation_service.py` | 🔴 VULNERABLE | ❌ MISSING | - | 20% / 0% | 0 / 0 / 0 | - | ⚪ N/A | ⚠️ UNUSED | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) | 📊 Coverage növelése: 20% → 80%+ |
| `ui/services/strategy_service.py` | 🟡 WARNING | ✅ FOUND | - | 8% / 0% | 0 / 0 / 69 | - | ⚪ N/A | ⚠️ UNUSED | ❌ | 📝 Dokumentáció írása (docs/components/) | 🔎 Pylance: 69 hiba javítása | 📊 Coverage növelése: 8% → 80%+ |
| `ui/streamlit_app.py` | 🔴 VULNERABLE | ❌ MISSING | - | N/A | 0 / 0 / 0 | - | ⚪ N/A | ⚪ N/A | ❌ | 🔴 **Teszt írás KÖTELEZŐ!** | 📝 Dokumentáció írása (docs/components/) |
