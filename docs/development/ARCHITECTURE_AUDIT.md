# 🔍 ARCHITECTURE AUDIT REPORT

**Generálva:** 2026-03-26 13:16:31
**Szkennelt fájlok:** 295
**Problémák száma:** 134

## 📊 Összefoglaló

- 🔴 **Kritikus problémák:** 52
- 🟡 **Figyelmeztetések:** 82

## 🔴 Kritikus Problémák (Azonnal javítandó)


### Relatív Importok (21 db)

- `neural_ai/collectors/jforex/interfaces/__init__.py` (sor 6)
  - Relatív import: .downloader_interface
- `neural_ai/collectors/jforex/interfaces/__init__.py` (sor 7)
  - Relatív import: .live_interface
- `neural_ai/collectors/jforex/interfaces/__init__.py` (sor 8)
  - Relatív import: .tick_data
- `neural_ai/collectors/jforex/implementations/__init__.py` (sor 3)
  - Relatív import: .bi5_downloader
- `neural_ai/collectors/jforex/implementations/__init__.py` (sor 4)
  - Relatív import: .live_feed
- `neural_ai/core/db/__init__.py` (sor 7)
  - Relatív import: .factory
- `neural_ai/core/db/__init__.py` (sor 8)
  - Relatív import: .implementations.model_base
- `neural_ai/core/db/__init__.py` (sor 9)
  - Relatív import: .implementations.models
- `neural_ai/core/db/__init__.py` (sor 10)
  - Relatív import: .implementations.sqlalchemy_session
- `neural_ai/core/events/exceptions/__init__.py` (sor 6)
  - Relatív import: .event_error
- `neural_ai/core/db/implementations/__init__.py` (sor 6)
  - Relatív import: .model_base
- `neural_ai/core/db/implementations/__init__.py` (sor 7)
  - Relatív import: .models
- `neural_ai/core/db/implementations/__init__.py` (sor 8)
  - Relatív import: .sqlalchemy_session
- `neural_ai/core/db/implementations/sqlalchemy_session.py` (sor 265)
  - Relatív import: .models
- `neural_ai/core/db/implementations/sqlalchemy_session.py` (sor 352)
  - Relatív import: .models
- `neural_ai/core/db/implementations/sqlalchemy_session.py` (sor 402)
  - Relatív import: .models
- `neural_ai/core/db/implementations/models.py` (sor 13)
  - Relatív import: .model_base
- `neural_ai/core/config/exceptions/__init__.py` (sor 6)
  - Relatív import: .config_error
- `neural_ai/core/config/implementations/__init__.py` (sor 29)
  - Relatív import: .yaml_config_manager
- `neural_ai/core/config/implementations/__init__.py` (sor 27)
  - Relatív import: .yaml_config_manager

... és még 1 probléma

### Implementáció Exportok (31 db)

- `neural_ai/core/__init__.py` (sor 24)
  - Implementáció import: neural_ai.core.base.implementations.component_bundle
- `neural_ai/core/__init__.py` (sor 28)
  - Implementáció import: neural_ai.core.db.implementations.sqlalchemy_session
- `neural_ai/core/__init__.py` (sor 116)
  - Implementáció import: neural_ai.core.base.implementations.component_bundle
- `neural_ai/core/__init__.py` (sor 117)
  - Implementáció import: neural_ai.core.base.implementations.di_container
- `neural_ai/core/__init__.py` (sor 121)
  - Implementáció import: neural_ai.core.db.implementations.sqlalchemy_session
- `neural_ai/data/storage/__init__.py` (sor 24)
  - Implementáció import: neural_ai.data.storage.implementations
- `neural_ai/data/storage/__init__.py` (sor 17)
  - Implementáció import: neural_ai.data.storage.implementations.file_storage
- `neural_ai/data/storage/__init__.py` (sor 18)
  - Implementáció import: neural_ai.data.storage.implementations.parquet_storage
- `neural_ai/data/storage/implementations/__init__.py` (sor 3)
  - Implementáció import: neural_ai.data.storage.implementations.file_storage
- `neural_ai/data/storage/implementations/__init__.py` (sor 4)
  - Implementáció import: neural_ai.data.storage.implementations.parquet_storage
- `neural_ai/core/db/__init__.py` (sor 8)
  - Implementáció import: implementations.model_base
- `neural_ai/core/db/__init__.py` (sor 9)
  - Implementáció import: implementations.models
- `neural_ai/core/db/__init__.py` (sor 10)
  - Implementáció import: implementations.sqlalchemy_session
- `neural_ai/core/config/__init__.py` (sor 49)
  - Implementáció import: neural_ai.core.config.implementations.yaml_config_manager
- `neural_ai/core/logger/__init__.py` (sor 46)
  - Implementáció import: neural_ai.core.logger.implementations
- `neural_ai/core/logger/__init__.py` (sor 33)
  - Implementáció import: neural_ai.core.logger.implementations
- `neural_ai/core/base/__init__.py` (sor 15)
  - Implementáció import: neural_ai.core.base.implementations.component_bundle
- `neural_ai/core/base/__init__.py` (sor 16)
  - Implementáció import: neural_ai.core.base.implementations.di_container
- `neural_ai/core/base/__init__.py` (sor 11)
  - Implementáció import: neural_ai.core.base.implementations.component_bundle
- `neural_ai/core/base/__init__.py` (sor 12)
  - Implementáció import: neural_ai.core.base.implementations.di_container

... és még 11 probléma

## 🟡 Figyelmeztetések (Javítandó)


### Mirror Testing (82 db)

- `neural_ai/data/__init__.py`
  - Hiányzó mirror teszt: tests/neural_ai/data/test_init.py
- `neural_ai/collectors/__init__.py`
  - Hiányzó mirror teszt: tests/neural_ai/collectors/test_init.py
- `neural_ai/processors/__init__.py`
  - Hiányzó mirror teszt: tests/neural_ai/processors/test_init.py
- `neural_ai/ui/__init__.py`
  - Hiányzó mirror teszt: tests/neural_ai/ui/test_init.py
- `neural_ai/ui/streamlit_app.py`
  - Hiányzó mirror teszt: tests/neural_ai/ui/test_streamlit_app.py
- `neural_ai/data/storage/factory.py`
  - Hiányzó mirror teszt: tests/neural_ai/data/storage/test_factory.py
- `neural_ai/data/ingestion/__init__.py`
  - Hiányzó mirror teszt: tests/neural_ai/data/ingestion/test_init.py
- `neural_ai/data/storage/interfaces/__init__.py`
  - Hiányzó mirror teszt: tests/neural_ai/data/storage/interfaces/test_init.py
- `neural_ai/data/storage/interfaces/factory_interface.py`
  - Hiányzó mirror teszt: tests/neural_ai/data/storage/interfaces/test_factory_interface.py
- `neural_ai/data/storage/backends/__init__.py`
  - Hiányzó mirror teszt: tests/neural_ai/data/storage/backends/test_init.py
- `neural_ai/data/storage/exceptions/__init__.py`
  - Hiányzó mirror teszt: tests/neural_ai/data/storage/exceptions/test_init.py
- `neural_ai/data/storage/implementations/__init__.py`
  - Hiányzó mirror teszt: tests/neural_ai/data/storage/implementations/test_init.py
- `neural_ai/collectors/jforex/interfaces/tick_data.py`
  - Hiányzó mirror teszt: tests/neural_ai/collectors/jforex/interfaces/test_tick_data.py
- `neural_ai/collectors/jforex/interfaces/live_interface.py`
  - Hiányzó mirror teszt: tests/neural_ai/collectors/jforex/interfaces/test_live_interface.py
- `neural_ai/collectors/jforex/interfaces/downloader_interface.py`
  - Hiányzó mirror teszt: tests/neural_ai/collectors/jforex/interfaces/test_downloader_interface.py
- `neural_ai/collectors/jforex/exceptions/jforex_error.py`
  - Hiányzó mirror teszt: tests/neural_ai/collectors/jforex/exceptions/test_jforex_error.py
- `neural_ai/collectors/jforex/implementations/__init__.py`
  - Hiányzó mirror teszt: tests/neural_ai/collectors/jforex/implementations/test_init.py
- `neural_ai/collectors/jforex/implementations/live_feed.py`
  - Hiányzó mirror teszt: tests/neural_ai/collectors/jforex/implementations/test_live_feed.py
- `neural_ai/collectors/jforex/implementations/bi5_downloader.py`
  - Hiányzó mirror teszt: tests/neural_ai/collectors/jforex/implementations/test_bi5_downloader.py
- `neural_ai/processors/interfaces/__init__.py`
  - Hiányzó mirror teszt: tests/neural_ai/processors/interfaces/test_init.py

... és még 62 probléma

## 📋 Részletes Statisztika

| Kategória | Kritikus | Figyelmeztetés | Összesen |
|:----------|:---------|:---------------|:---------|
| Fájlnév | 0 | 0 | 0 |
| Import | 21 | 0 | 21 |
| Struktúra | 0 | 0 | 0 |
| Mirror Test | 0 | 82 | 82 |
| Export | 31 | 0 | 31 |
| **Összesen** | **52** | **82** | **134** |
