# AGENTS.md

Ez a fájl útmutatást nyújt az AI assztensek számára ebben a repositoryban való munkához.

## Projekt Áttekintés
- **Adatok**: 25 évnyi TICK ADAT (nem OHLCV!)
- **Stack**: Python 3.12, Polars, PyTorch 2.5.1 (CUDA:12.1), Lightning 2.5.5, VectorBT Pro, FastParquet
- **Források**: Dukascopy (Native .bi5 decoding), MT5, IBKR
- **Architektúra**: Domain-Driven (DDD), Eseményvezérelt (ZeroMQ/AsyncIO), Adatbázis-Első

## Kritikus Projekt Szabályok (Nem Nyilvánvaló)
- **Magyar Nyelv**: Minden kommunikáció (chat, commit üzenetek, docstringek, kommentek, gondolkodás, feladatleírások) magyarul kötelező.
- **Abszolút Parancs Útvonalak**: Teljes útvonalak használata Python, Ruff és Pytest futtatható fájlokhoz:
  - Python: `/home/elynea/miniconda3/envs/neural-ai-next/bin/python`
  - Ruff: `/home/elynea/miniconda3/envs/neural-ai-next/bin/ruff`
  - Pytest: `/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest`
- **Tükör Dokumentáció**: A dokumentáció követi a kód szerkezetét (pl. `docs/components/core/logger/factory.md` a `neural_ai/core/logger/factory.py`-hoz)
- **Atomikus Commitok**: Minden fájl módosítás után azonnali `git commit` kötelező (nincs kötegelés)
- **Modul Szerkezet**: Minden funkcionális modul követi: `interfaces/`, `implementations/`, `exceptions/`, `factory.py`, `__init__.py`
- **Dependency Injection**: Soha ne importálj konkrét implementációkat közvetlenül; használd az interfészeket és factory mintát
- **Import Szabályok**: Abszolút importok modulok között, relatív importok modulon belül
- **Konfiguráció Kezelés**: Mindig castold a `config.get()` eredményeket TypedDict-re (pl. `cast(JForexConfig, raw_config)`)
- **Szigorú Típusozás**: Nincs `Any` típus; minden paraméter és visszatérési érték teljes mértékben típusozott kell legyen
- **Polars Első**: Használj `pl.DataFrame`-et kizárólag processzorokban; Pandas csak UI rétegben
- **Logolási Policy**: Nincs `print()` utasítás; strukturált logolás `logger.info("üzenet", extra={"kulcs": érték})`
- **Adattárolás**: Csak particionált Parquet fájlok (FastParquet); CSV/JSON TILOS
- **QA Kapu**: Minden változás előtt kötelező a `ruff check` és `pytest` sikeres lefutása
- **Típus Ellenőrzés**: Pylance strict mód kényszerített (`python.analysis.typeCheckingMode: "strict"`)
- **Problems Tab Compliance**: Minden VSCode Problems fülben látható linter/Ruff/MyPy hiba SZIGORÚAN javítandó

## Architektúra Szabványok (v4.0 kivonat)
- **Réteges Architektúra**: Presentation→Domain→Persistence→Input→Infrastructure (függőségek csak lefelé)
- **Bootstrap Lánc**: HardwareInfo→Config→Logger→EventBus→Storage→Database→SystemMonitor (függőségi sorrend)
- **DDD Minta**: Domain-Driven Design event-driven (ZeroMQ/AsyncIO), adatbázis-első megközelítéssel
- **Modul Minta**: Minden modul: interfaces/ABC, implementations/konkret, exceptions/tipizált, factory/létrehozás, __init__/facade

## Dimenzió Processzorok (D1-D15)
- **Pipeline Használat**: Minden dimenzió processzor implementálja az `IDimensionProcessor` interfészt
- **Adatfolyam**: Time Aligned OHLCV bemenet → Feature DataFrame kimenet (ugyanannyi sor, új oszlopokkal)
- **Hierarchikus Rendszer**: L1-L6 szintek (Base Analyzers → Meta-Learning) a `docs/architecture/hierarchical_system/overview.md` és `docs/models/hierarchical/structure.md` szerint
- **Részletes Specifikáció**: Lásd `docs/processors/dimensions/overview.md` a D1-D15 dimenziók teljes leírásáért