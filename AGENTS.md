# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Projekt Áttekintés
- **Adatok**: 25 évnyi TICK ADAT (nem OHLCV!)
- **Stack**: Python 3.12, Polars, PyTorch 2.5.1, Lightning 2.5.5, VectorBT Pro, FastParquet
- **Architektúra**: Domain-Driven (DDD), Eseményvezérelt (ZeroMQ), Adatbázis-Első

## Kritikus Projekt Szabályok (Nem Nyilvánvaló)
- **🇭🇺 NYELV**: Minden kommunikáció (chat, commit, docstring, gondolkodás) MAGYARUL kötelező.
- **🏗️ ARCHITEKTÚRA**: Rétegek csak LEFELÉ hívhatnak: Presentation → Domain → Persistence → Input → Infrastructure (Core).
- **🛡️ BIZTONSÁGI PROTOKOLL**: **TESZTEK FUTTATÁSA TILOS!** (pytest, python main.py). Kizárólag Statikus Kódanalízis és Kódírás.
- **📦 ADATKEZELÉS**: Csak particionált Parquet. `.bi5` bináris dekódolás JForexhez (CSV/JSON TILOS). Polars First Policy a processzorokban.
- **📝 DASHBOARD**: `docs/development/TASK_TREE.md` az SSOT. Fájl szintű követés (Stmt/Brch Coverage) kötelező.
- **⚠️ HIBAKEZELÉS**: Minden piros hiba (Ruff/MyPy) SZIGORÚAN javítandó commit előtt. `from e` láncolás kötelező.
- **👁️ OBSERVABILITY**: 
  - Csak `LoggerFactory.get_logger(__name__)` engedélyezett. `structlog` direkt hívás és `print()` TILOS.
  - `@trace` dekorátor KÖTELEZŐ minden kritikus függvényre.
- **🧬 TÍPUSBIZTONSÁG**: `config.get()` eredményét KÖTELEZŐ `TypedDict`-re castolni a Factory-ban. `Any` TILOS.
- **DI & MODUL SZERKEZET**: Konstruktor injektálás kötelező. Modul felépítés: `interfaces/`, `implementations/`, `exceptions/`, `factory.py` (TypedDict Config!), `__init__.py`.
- **🛠️ PARANCS ÚTVONALAK**: KÖTELEZŐ az abszolút útvonalak használata parancsfuttatáshoz (Python, Ruff, Pytest).
