# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Projekt Áttekintés
- **Adatok**: 25 évnyi TICK ADAT (nem OHLCV!)
- **Stack**: Python 3.12, Polars, PyTorch 2.5.1, Lightning 2.5.5, VectorBT Pro, FastParquet
- **Architektúra**: Domain-Driven (DDD), Eseményvezérelt (ZeroMQ), Adatbázis-Első

## Kritikus Projekt Szabályok (Nem Nyilvánvaló)
- **Magyar Nyelv**: Minden kommunikáció (chat, commit, docstring, gondolkodás) MAGYARUL kötelező.
- **Abszolút Útvonalak**: Parancsokhoz KÖTELEZŐ az abszolút útvonal:
  - Python: `/home/elynea/miniconda3/envs/neural-ai-next/bin/python`
  - Ruff: `/home/elynea/miniconda3/envs/neural-ai-next/bin/ruff`
  - Pytest: `/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest`
- **🛡️ BIZTONSÁGI PROTOKOLL**: **TESZTEK FUTTATÁSA TILOS!** (pytest, python main.py). Csak Statikus Kódanalízis és Kódírás.
- **👁️ OBSERVABILITY**: 
  - Csak `LoggerFactory.get_logger(__name__)` engedélyezett. `structlog` direkt hívás és `print()` TILOS.
  - `@trace` dekorátor KÖTELEZŐ minden kritikus függvényre.
- **🧬 TÍPUSBIZTONSÁG**: `config.get()` eredményét KÖTELEZŐ `TypedDict`-re castolni a Factory-ban. `Any` TILOS.
- **🏗️ MODUL SZERKEZET**: `interfaces/`, `implementations/`, `exceptions/`, `factory.py`, `__init__.py`.
- **📦 ADAT**: Csak particionált Parquet. `.bi5` bináris dekódolás JForexhez (CSV TILOS).
- **📝 DASHBOARD**: `docs/development/TASK_TREE.md` az SSOT. Fájl szintű követés kötelező.
- **⚠️ PROBLEMS TAB**: Minden piros hiba (Ruff/MyPy) SZIGORÚAN javítandó commit előtt.
