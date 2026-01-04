# pyproject.toml - Projekt konfiguráció

## Áttekintés

Ez a fájl a projekt konfigurációját tartalmazza a Poetry szabvány szerint. Itt vannak definiálva a projekt metaadatok, függőségek, opcionális függőségi csoportok, valamint a fejlesztői eszközök konfigurációi.

## Szerkezet

### [project] szekció

A projekt alapvető metaadatait és kötelező függőségeit tartalmazza:

- **Név és verzió**: `neural-ai-next` v0.5.0
- **Python követelmény**: >=3.12
- **Licenc**: MIT
- **Szerző**: Elynea-1528

### Kötelező függőségek (dependencies)

A projekt működéséhez elengedhetetlen csomagok:

#### Web Framework
- `fastapi>=0.104.0` - Modern web framework
- `uvicorn>=0.24.0` - ASGI szerver
- `websockets>=12.0` - WebSocket támogatás

#### Adat validáció & szerializáció
- `pydantic>=2.4.0` - Adatvalidáció
- `pydantic-settings>=2.1.0` - Beállítások kezelése

#### Adatbázis
- `sqlalchemy[asyncio]>=2.0.0` - ORM aszinkron támogatással
- `aiosqlite>=0.19.0` - Aszinkron SQLite adapter
- `alembic>=1.12.0` - Adatbázis migrációk

#### Logging
- `structlog>=23.1.0` - Strukturált logging

#### CLI
- `typer>=0.9.0` - CLI framework

#### HTTP kliens
- `requests>=2.31.0` - HTTP kérések
- `aiohttp>=3.9.0` - Aszinkron HTTP (JForex Collector)

#### Konfiguráció
- `pyyaml>=6.0` - YAML feldolgozás
- `python-multipart>=0.0.6` - Multipart form adatok

#### Segédeszközök
- `packaging>=23.1` - Csomagkezelés
- `tenacity>=8.2.0` - Retry mechanizmus (JForex Collector)

### Opcionális függőségi csoportok

#### [project.optional-dependencies]

##### dev
Fejlesztői eszközök és teszteléshez:
- `pytest>=7.4.0` - Tesztelési keretrendszer
- `pytest-cov>=4.1.0` - Code coverage
- `pytest-asyncio>=0.21.0` - Aszinkron tesztelés
- `mypy>=1.5.0` - Statikus típusellenőrzés
- `bandit>=1.7.7` - Biztonsági ellenőrzés
- `ruff>=0.1.0` - Linter (REPLACES Black, Isort, Flake8)
- `pre-commit>=3.4.0` - Pre-commit hookok
- Típusdefiníciók: `types-*` csomagok

##### trader
Trading-specifikus funkcionalitás:
- `ib_insync>=0.9.70` - Interactive Brokers API
- `vectorbt>=0.25.0` - Vektorizált backtesting
- `dukascopy-python` - Dukascopy adatgyűjtés
- `python-socketio>=5.0.0` - Valós idejű kommunikáció
- `redis>=4.0.0` - Gyorsítótár és pub/sub

##### jupyter
Jupyter notebook környezet:
- `jupyterlab>=4.0.0` - JupyterLab IDE
- `notebook>=7.0.0` - Jupyter notebook
- `ipykernel>=6.0.0` - Python kernel
- `matplotlib>=3.5.0` - Plotolás
- `seaborn>=0.12.0` - Statisztikai vizualizáció
- `plotly>=5.0.0` - Interaktív plotok
- `kaggle>=1.5.0` - Kaggle API
- `tensorboard>=2.14.0` - ML kísérlet követés

##### ui (ÚJ)
UI dashboard és vizualizáció:
- `streamlit>=1.30.0` - Webes dashboard keretrendszer
- `plotly>=5.18.0` - Interaktív vizualizációk
- `streamlit-aggrid` - Fejlett adattáblák
- `watchdog` - Auto-reload funkcionalitás
- `tensorboard` - ML kísérletek monitorozása
- `torchinfo` - PyTorch modellek összegzése

##### full
Minden opcionális csoportot tartalmaz:
- `neural-ai-next[dev]`
- `neural-ai-next[trader]`
- `neural-ai-next[jupyter]`
- `neural-ai-next[ui]`

## Eszköz konfigurációk

### [tool.ruff]
A Ruff linter konfigurációja, amely lecseréli a Black, Isort és Flake8 eszközöket:
- Sorhossz: 100 karakter
- Cél Python verzió: 3.12
- Engedélyezett szabályok: E, W, F, I, B, C4, UP, D
- Docstring konvenció: Google style

### [tool.mypy]
Strik típusellenőrzési konfiguráció:
- Python verzió: 3.12
- Szigorú beállítások: warn_return_any, disallow_untyped_defs, stb.
- Teszteknél engedélyezett az untyped defs

### [tool.pytest.ini_options]
Pytest konfiguráció:
- Tesztelési útvonalak: `tests`
- Python fájlok: `test_*.py`, `*_test.py`
- Aszinkron mód: auto
- Markerek: unit, integration, asyncio

## Telepítési lehetőségek

### Alap telepítés
```bash
pip install -e .
```

### Fejlesztői környezet
```bash
pip install -e ".[dev]"
```

### Teljes környezet (minden opcionális függőséggel)
```bash
pip install -e ".[full]"
```

### UI dashboard
```bash
pip install -e ".[ui]"
```

### Kombinált telepítés
```bash
pip install -e ".[dev,ui,trader]"
```

## Kapcsolódó dokumentáció

- [Architektúra szabványok](development/architecture_standards.md)
- [TASK_TREE](development/TASK_TREE.md)
- [Függőség kezelés](development/dependency_management.md)