# Architect Mód Szabályai (Csak Nem-Nyilvánvaló Tudás)

## DDD Réteg Architektúra

**5-rétegű szigorú hierarchia (lásd `docs/development/architecture_standards.md:28-41`):**
1. **Presentation** (`neural_ai/ui`) - Streamlit UI, mindentől függhet
2. **Domain** (`neural_ai/processors`) - Üzleti logika, D1-D15 processzorok, függ Data + Core-tól
3. **Persistence** (`neural_ai/data`) - Storage/DB, csak Core-tól függ
4. **Input** (`neural_ai/collectors`) - JForex/MT5/IBKR, csak Core-tól függ
5. **Infrastructure** (`neural_ai/core`) - Config/Logger/Events, önálló

**Függőségi szabálysértés = architektúra bukás.** Alsó rétegek SOHA nem importálnak felső rétegekből.

## Modul Tervezési Minta

**Atomi modul struktúra (lásd `docs/development/architecture_standards.md:79-104`):**
```
xyz_module/
├── interfaces/        # Szerződés (ABC) - EXPORTÁLT
├── implementations/   # Konkrét kód - REJTETT (soha nem exportált)
├── exceptions/        # Típusos hibák
├── factory.py         # EGYETLEN hely ami importálja az implementations/-t
└── __init__.py        # CSAK Interface + Factory exportálása
```

**Factory izoláció:** `implementations/` importálás TILOS a `factory.py`-on kívül. Factory-k lazy loading-ot használnak körkörös importok elkerülésére.

## Dependency Injection

**Konstruktor injektálás kötelező:** Osztályok a függőségeket (logger, config, event_bus) az `__init__`-ben kapják, soha nem példányosítják magukat. Példa minta: `neural_ai/core/base/factory.py:81-115`.

**DIContainer regisztráció:** Core komponensek regisztrálva a DIContainer-ben, factory-k által feloldva. Bootstrap sorrend számít: HardwareInfo → Config → Logger → EventBus → Storage → DB → SystemMonitor.

## Konfigurációs Architektúra

**TypedDict séma kötelező:** Minden `config.get()` `Any`-t ad vissza - factory-knak KÖTELEZŐ TypedDict-et definiálni és castolni. Példa sémák: `neural_ai/core/base/factory.py:25-48`.

**Hibrid config rétegek:**
- `.env` - Statikus környezet (DB URL-ek, secretek)
- YAML (`configs/*.yaml`) - Strukturális konfig (portok, útvonalak)
- SQL (dinamikus) - Futásidejű változtatások (stratégia paraméterek)

Lásd `docs/planning/specs/02_dynamic_configuration.md` az indoklásért.

## Adatfeldolgozási Stratégia

**Polars-first policy:** Nagy adattömeg feldolgozás `pl.DataFrame`-et használ a processors/data rétegekben. Pandas CSAK UI-ban megjelenítési kompatibilitásért. Sor iteráció (`for row in df`) TILOS - használj vektorizált `pl.Expr`-t.

**Backend kiválasztás:** Storage backend-ek auto-szelektálva HardwareInfo alapján (AVX2 → Polars backend, fallback → Pandas backend). Lásd `neural_ai/data/storage/backends/`.

## Eseményvezérelt Architektúra

**ZeroMQ Pub/Sub:** Komponensek az EventBus-on keresztül kommunikálnak (nincs direkt hívás). Async event loop a `main.py:64-65` háttérfolyamatban. MarketDataPersister feliratkozik tick eseményekre.

**Leállítási sorrend:** Persister áll le először (buffer flush), aztán LiveFeed, aztán EventBus. Lásd `main.py:92-111`.

## Kritikus Korlátozások

**JForex bináris formátum:** Dukascopy `.bi5` (LZMA) csak - CSV tilos. Natív dekóder: `neural_ai/collectors/jforex/implementations/bi5_downloader.py`.

**Storage csak Parquet:** Nincs CSV/JSON a `neural_ai/data/storage/`-ban. Particionált Parquet `fastparquet`-tel.

**Mirror dokumentáció:** Kód `neural_ai/X/Y.py` igényel `docs/components/X/Y.md`-t (auto-generált docstring-ekből `python scripts/generate_docs.py` via).

**Atomic commitok:** Minden fájlváltozás azonnali `git commit`-ot igényel. Formátum: `feat/fix/refactor(scope): [Magyar üzenet]`

## Tesztelési Stratégia

**Mirror teszt struktúra:** `neural_ai/processors/dimensions/d01_price/processor.py` → `tests/processors/dimensions/d01_price/test_processor.py`

**100% lefedettség Domain rétegre:** Processors és Data modulok teljes teszt lefedettséget igényelnek. UI réteg tesztek opcionálisak.

**Abszolút útvonalak:** Használd `/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest` - conda activate nem működik nem-interaktív shell-ekben.
