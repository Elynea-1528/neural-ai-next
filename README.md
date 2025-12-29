# 🧠 Neural AI Next - Institutional Trading Ecosystem

**Version:** 1.0.0 | **Status:** 🟡 Architecture Phase | **License:** Proprietary

---

## 🎯 Vision & Mission

**Neural AI Next** is an institutional-grade, event-driven trading ecosystem designed for high-frequency tick data processing (25+ years), real-time execution, and AI-powered strategy deployment. Built with **zero compromises** for reliability, scalability, and performance.

**Philosophy:** *"Loose Coupling, High Cohesion"* - Every component is isolated, testable, and replaceable.

**Focus:** Premium instruments only (EURUSD, XAUUSD, GBPUSD, USDJPY, USDCHF) - High Liquidity, Low Spread.

---

## 🏗️ System Architecture

### Event-Driven Core

```
┌─────────────────────────────────────────────────────────┐
│                    NEURAL AI NEXT                        │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │  JForex      │  │  MT5         │  │  IBKR        │ │
│  │  Bi5 + Java  │  │  FastAPI     │  │  TWS API     │ │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘ │
│         │                 │                 │          │
│         └─────────────────┼─────────────────┘          │
│                           ▼                            │
│              ┌────────────────────────┐                │
│              │   EVENT BUS (ZeroMQ)   │                │
│              └────────────┬───────────┘                │
│                           │                            │
│         ┌─────────────────┼─────────────────┐          │
│         ▼                 ▼                 ▼          │
│  ┌──────────┐    ┌──────────────┐    ┌──────────┐    │
│  │ Parquet  │    │   Strategy   │    │   AI     │    │
│  │ Storage  │    │   Engine     │    │  Models  │    │
│  └──────────┘    └──────────────┘    └──────────┘    │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

**Key Principles:**
- **No Direct Calls:** Components communicate exclusively through events
- **Database-First:** All state is persisted in SQL database
- **Async Everywhere:** Python 3.12 + `asyncio` for maximum performance
- **Big Data Ready:** Parquet storage for 25+ years of tick data

---

## 📚 Documentation Structure

### 🗺️ Master Blueprint

All development is guided by the **System Specifications** in [`docs/planning/specs/`](docs/planning/specs/):

1. **[System Architecture](docs/planning/specs/01_system_architecture.md)** - Event-Driven Core Design
2. **[Dynamic Configuration](docs/planning/specs/02_dynamic_configuration.md)** - Hybrid Config System (.env + SQL)
3. **[Observability & Logging](docs/planning/specs/03_observability_logging.md)** - Structured Logging with `structlog`
4. **[Data Warehouse](docs/planning/specs/04_data_warehouse.md)** - Parquet Storage & Resampling
5. **[Collectors Strategy](docs/planning/specs/05_collectors_strategy.md)** - JForex Bi5 + Java Bridge + MT5

### 📚 Component Documentation

**Auto-Generated API Documentation** from source code with docstrings:

- **[Components Overview](docs/components/)** - Complete API documentation for all core modules
- **Mirror Structure:** Documentation follows the exact same structure as the source code
- **Source Links:** Each documentation file links back to the original source file
- **Auto-Updated:** Run `python scripts/generate_docs.py` to regenerate documentation

**Core Modules:**
- [Base Architecture](docs/components/core/base/index.md) - DI Container, Factory, Interfaces
- [Configuration](docs/components/core/config/index.md) - Dynamic & YAML Config
- [Logging](docs/components/core/logger/index.md) - Structured Logging System
- [Storage](docs/components/core/storage/index.md) - Parquet & File Storage
- [Database](docs/components/core/db/index.md) - SQLAlchemy ORM
- [Events](docs/components/core/events/index.md) - ZeroMQ Event Bus
- [System](docs/components/core/system/index.md) - Health Monitoring
- [Utilities](docs/components/core/utils/index.md) - Helper Functions

### 🧠 AI Models

The system implements a **hierarchical AI architecture** for multi-timeframe analysis:

- **[Hierarchical Model Structure](docs/models/hierarchical/structure.md)** - D1, H4, H1, M15, M5, M1 models
- **Ensemble Learning** - Combines predictions from multiple timeframes
- **PyTorch + Lightning** - CUDA-accelerated training and inference

### ⚙️ Data Processors

15-dimensional feature engineering for tick data:

- **[Dimension Processors Overview](docs/processors/dimensions/overview.md)** - D1-D15 feature extraction
- **Real-time Processing** - On-the-fly feature calculation
- **VectorBT Integration** - Backtesting and validation

### 🛠️ Development Guidelines

- **[Unified Development Guide](docs/development/unified_development_guide.md)** - Pylance Strict, Hungarian Docstrings
- **[Core Dependencies](docs/development/core_dependencies.md)** - DI Container, Factory Pattern, NullObject
- **[Task Tree Dashboard](docs/development/TASK_TREE.md)** - Real-time project status and telemetry
- **[Architecture Standards](docs/development/architecture_standards.md)** - Module structure & naming conventions

### 📖 Documentation Generation

The system includes an **automated documentation generator** that extracts docstrings from source code:

```bash
# Generate/update all component documentation
python scripts/generate_docs.py
```

**Features:**
- ✅ Extracts module, class, and function docstrings using AST
- ✅ Creates mirror documentation structure in `docs/components/`
- ✅ Generates index files for each directory
- ✅ Links back to source files for easy navigation
- ✅ Supports Hungarian docstrings (as per project standards)

---

## 🚀 Quick Start

### Prerequisites

- **Python:** 3.12+
- **Conda:** Miniconda3
- **CUDA:** 12.1 (for GPU acceleration)
- **Java:** 11+ (for JForex Bridge)

### Installation

**🚀 UNIFIED ZERO-TOUCH INSTALLER (RECOMMENDED)**

Run the unified installer that automatically detects hardware, installs dependencies, and sets up brokers:

```bash
# 1. Clone the repository
git clone https://github.com/your-org/neural-ai-next.git
cd neural-ai-next

# 2. Run the unified installer (automated everything!)
python scripts/install.py

# 3. Activate the environment
conda activate neural-ai-next

# 4. Configure environment (if needed)
cp .env.example .env
# Edit .env with your settings

# 5. Start the system
python main.py
```

**What the installer does automatically:**
- ✅ Detects NVIDIA GPU and installs CUDA-enabled PyTorch
- ✅ Checks AVX2 support and installs optimal data libraries (Polars/PyArrow or fastparquet)
- ✅ Creates Conda environment with Python 3.12
- ✅ Installs all dependencies (dev + trader + jupyter)
- ✅ Downloads and launches broker installers (JForex4, TWS, MT5)
- ✅ Sets up Wine prefix for MT5

**Manual Installation (Legacy)**

If you prefer manual installation:

```bash
# 1. Create environment
conda create -n neural-ai-next python=3.12 -y
conda activate neural-ai-next

# 2. Install PyTorch (GPU or CPU)
conda install -y pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia  # GPU
# OR
conda install -y pytorch torchvision torchaudio cpuonly -c pytorch  # CPU

# 3. Install project dependencies
pip install -e .[dev,trader,jupyter]

# 4. Configure environment
cp .env.example .env
# Edit .env with your settings

# 5. Start the system
python main.py
```

### Configuration

Edit [`.env`](.env.example) to configure:

- **Database:** SQLite (dev) or PostgreSQL (prod)
- **Brokers:** JForex, MT5, IBKR credentials
- **Symbols:** Trading instrument list
- **Logging:** Log level and output format
- **API:** FastAPI server settings

---

## 🧪 Testing

```bash
# Run all tests
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest

# Run with coverage
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest --cov=neural_ai --cov-report=html

# Run specific test
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/core/test_event_bus.py -v
```

---

## 📊 Technology Stack

### Core Framework
- **Python 3.12** - Modern async/await syntax
- **Pydantic** - Data validation and settings management
- **SQLAlchemy 2.0** - Async ORM with type safety
- **FastAPI** - High-performance API server

### Data Processing
- **Polars** - Blazing-fast DataFrame operations
- **FastParquet** - Efficient columnar storage
- **VectorBT Pro** - Backtesting and portfolio analysis

### AI/ML
- **PyTorch 2.5.1** - Deep learning framework
- **Lightning 2.5.5** - Training orchestration
- **CUDA 12.1** - GPU acceleration

### Observability
- **structlog** - Structured JSON logging
- **OpenTelemetry** - Distributed tracing (planned)
- **Prometheus** - Metrics collection (planned)

### Messaging
- **ZeroMQ** - High-performance event bus
- **WebSockets** - Real-time communication
- **Redis** - Caching and pub/sub

### Brokers
- **JForex** - Dukascopy (Bi5 + Java Bridge)
- **MT5** - MetaTrader 5 (FastAPI integration)
- **IBKR** - Interactive Brokers (TWS API)

---

## 🏗️ Project Structure

### 📚 Core Components Documentation

A teljes rendszer dokumentációja a forráskódból automatikusan generálva. Minden komponenshez tartozik részletes API dokumentáció a [`docs/components/`](docs/components/) mappában.

#### 🏛️ Base Architecture
- **[Base Components Overview](docs/components/core/base/index.md)** - DI Container, Factory, Interfaces
  - [`factory.py`](docs/components/core/base/factory.md) - Abstract Factory Pattern
  - [`implementations/`](docs/components/core/base/implementations/index.md) - DI Container, Component Bundle, Singleton, Lazy Loader
  - [`interfaces/`](docs/components/core/base/interfaces/index.md) - Component & Container Interfaces
  - [`exceptions/`](docs/components/core/base/exceptions/index.md) - Base Error Classes

#### ⚙️ Configuration System
- **[Configuration Overview](docs/components/core/config/index.md)** - Dynamic & YAML Config Managers
  - [`factory.py`](docs/components/core/config/factory.md) - Config Factory
  - [`implementations/`](docs/components/core/config/implementations/index.md) - Dynamic & YAML Config Managers
  - [`interfaces/`](docs/components/core/config/interfaces/index.md) - Config, Async Config & Factory Interfaces
  - [`exceptions/`](docs/components/core/config/exceptions/index.md) - Configuration Errors

#### 📝 Logging Framework
- **[Logging Overview](docs/components/core/logger/index.md)** - Structured Logging System
  - [`factory.py`](docs/components/core/logger/factory.md) - Logger Factory
  - [`implementations/`](docs/components/core/logger/implementations/index.md) - Colored, Default & Rotating File Loggers
  - [`interfaces/`](docs/components/core/logger/interfaces/index.md) - Logger & Factory Interfaces
  - [`formatters/`](docs/components/core/logger/formatters/index.md) - Log Formatters
  - [`exceptions/`](docs/components/core/logger/exceptions/index.md) - Logging Errors

#### 💾 Storage System
- **[Storage Overview](docs/components/core/storage/index.md)** - Parquet & File Storage
  - [`factory.py`](docs/components/core/storage/factory.md) - Storage Factory
  - [`implementations/`](docs/components/core/storage/implementations/index.md) - File & Parquet Storage
  - [`interfaces/`](docs/components/core/storage/interfaces/index.md) - Storage & Factory Interfaces
  - [`backends/`](docs/components/core/storage/backends/index.md) - Polars, Pandas & Base Backends
  - [`exceptions/`](docs/components/core/storage/exceptions/index.md) - Storage Errors

#### 🗄️ Database Layer
- **[Database Overview](docs/components/core/db/index.md)** - SQLAlchemy ORM & Models
  - [`factory.py`](docs/components/core/db/factory.md) - Database Factory
  - [`implementations/`](docs/components/core/db/implementations/index.md) - Models, Model Base & SQLAlchemy Session
  - [`exceptions/`](docs/components/core/db/exceptions/index.md) - Database Errors

#### 📡 Event System
- **[Event System Overview](docs/components/core/events/index.md)** - ZeroMQ Event Bus
  - [`factory.py`](docs/components/core/events/factory.md) - Event Bus Factory
  - [`implementations/`](docs/components/core/events/implementations/index.md) - ZeroMQ Event Bus
  - [`interfaces/`](docs/components/core/events/interfaces/index.md) - Event Bus Interface & Event Models
  - [`exceptions/`](docs/components/core/events/exceptions/index.md) - Event Errors

#### 🖥️ System Monitoring
- **[System Overview](docs/components/core/system/index.md)** - Health Monitoring
  - [`factory.py`](docs/components/core/system/factory.md) - System Factory
  - [`implementations/`](docs/components/core/system/implementations/index.md) - Health Monitor
  - [`interfaces/`](docs/components/core/system/interfaces/index.md) - Health Interface

#### 🛠️ Utilities
- **[Utilities Overview](docs/components/core/utils/index.md)** - Helper Functions & Hardware Info
  - [`factory.py`](docs/components/core/utils/factory.md) - Utils Factory
  - [`decorators.py`](docs/components/core/utils/decorators.md) - Utility Decorators
  - [`implementations/`](docs/components/core/utils/implementations/index.md) - Hardware Info
  - [`interfaces/`](docs/components/core/utils/interfaces/index.md) - Hardware Interface
  - [`exceptions/`](docs/components/core/utils/exceptions/index.md) - Utility Errors

---

## 📈 Development Phases

### Phase 1: Core Infrastructure (85% Complete)
- ✅ DI Container
- ✅ Configuration System
- ✅ Logging Framework
- ✅ Base Interfaces
- 🚧 Event Bus
- 🔴 Database Layer
- 🔴 Parquet Storage

### Phase 2: Data Collectors (10% Complete)
- 🔴 JForex Bi5 Downloader
- 🔴 MT5 FastAPI Server
- 🔴 Java-Python Bridge
- 🔴 IBKR TWS Integration

### Phase 3: AI/ML Pipeline (0% Complete)
- 🔴 Hierarchical Models
- 🔴 Feature Processors
- 🔴 Training Pipeline
- 🔴 Inference Engine

### Phase 4: Strategy Engine (0% Complete)
- 🔴 Backtesting Framework
- 🔴 Risk Management
- 🔴 Execution Engine
- 🔴 Performance Monitoring

**Overall Progress:** 35% [███████░░░░░░░░░░░░░]

---

## 🤝 Contributing

This is a proprietary institutional trading system. All contributions require:

1. **Architecture Review** - All changes must align with specifications
2. **100% Test Coverage** - No code merges without tests
3. **Documentation** - Mirror documentation for every component
4. **Code Review** - Senior architect approval required

### Development Workflow

```bash
# 1. Create feature branch
git checkout -b feature/your-feature

# 2. Implement changes (follow specs)
# 3. Write tests
# 4. Update documentation (mirror structure)
# 5. Run linter
/home/elynea/miniconda3/envs/neural-ai-next/bin/ruff check

# 6. Run tests
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest

# 7. Commit (atomic commits required)
git add .
git commit -m "feat(scope): description"

# 8. Push and create PR
git push origin feature/your-feature
```

---

## ⚠️ Critical Rules (NO-GO ZONE)

### 1. 🇭🇺 Language Protocol
- **ALL** communication (Chat, Commit, Docstring, Comments) in **HUNGARIAN**
- Exception: Code keywords (def, class, import) and technical terms

### 2. 🪞 Mirror Structure & Atomic Commit
- Documentation MUST mirror code structure
- **Every file change requires immediate `git commit`**
- No commit = ❌ FAILED

### 3. 🐍 Technical Strictness
- **JForex:** TILOS CSV! Only native .bi5 (LZMA) processing
- **Storage:** TILOS CSV/JSON! Only partitioned Parquet
- **Types:** TILOS `Any`! Strict type hints required
- **Imports:** `if TYPE_CHECKING:` for circular dependencies

### 4. 🧠 Memory Management
- **NO CONDENSING!** Never compress context without explicit user instruction
- Use the full 128k/200k token window

### 5. 🔍 Context Awareness
- **TILOS** to generate files without reading related documentation!
- README must link to `docs/models` and `docs/processors`

---

## 📞 Support & Contact

- **Architecture Questions:** See [System Specifications](docs/planning/specs/)
- **AI Model Questions:** See [Hierarchical Structure](docs/models/hierarchical/structure.md)
- **Processor Questions:** See [Dimension Overview](docs/processors/dimensions/overview.md)
- **Development Questions:** See [Development Guide](docs/development/unified_development_guide.md)

---

## 📄 License

**Proprietary & Confidential** - Neural AI Next v1.0.0

© 2025 Neural AI Next. All rights reserved.

---

## 🏆 Acknowledgments

Built with institutional-grade engineering practices:
- Event-Driven Architecture
- Dependency Injection
- Factory Pattern
- Strategy Pattern
- Repository Pattern
- NullObject Pattern
- Lazy Loading
- Singleton (where appropriate)

**Stack:** Python 3.12 | PyTorch 2.5.1 | Lightning 2.5.5 | VectorBT Pro | FastParquet | SQLAlchemy 2.0 | FastAPI | ZeroMQ

---

**Status:** 🟡 Architecture Phase | **Last Updated:** 2025-12-24 | **Version:** 1.0.0