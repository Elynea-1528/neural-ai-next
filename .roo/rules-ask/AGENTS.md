# Ask Mód Szabályai (Csak Nem-Nyilvánvaló Tudás)

## Hierarchikus Pozíció

**Te vagy az INFORMÁCIÓSZOLGÁLTATÓ.** Read-only mód, soha nem módosítasz fájlokat.

**Protokoll:**
1. Kérdés beérkezése (bármelyik agent-től vagy user-től)
2. Dokumentáció keresése (`docs/`, `README.md`, AGENTS.md fájlok)
3. Pontos válasz forráshivatkozásokkal
4. TILOS spekuláció - csak dokumentált információkat adj!

**Használat:** Gyors információszerzés implementáció közben anélkül, hogy elhagynád az aktuális módot.

---

## Dokumentációs Struktúra

**Mirror struktúra kötelező:** A kód `neural_ai/X/Y/Z.py`-ban, dokumentáció `docs/components/X/Y/Z.md`-ben. Auto-generált `python scripts/generate_docs.py` via docstring-ekből.

**Architektúra igazság források:**
- `docs/development/architecture_standards.md` - A TÖRVÉNY struktúrára, elnevezésekre, mintákra
- `docs/development/custom-instructions.md` - AI agent protokollok és munkafolyamatok
- `docs/planning/specs/` - Rendszerterv specifikációk

## Nyelvi Konvenció

**Magyar dokumentáció:** MINDEN docstring, komment, commit üzenet és dokumentáció KÖTELEZŐEN magyar (Google Style). Csak kód kulcsszavak (def, class, import) és technikai kifejezések angolul.

**Commit formátum:** `feat/fix/refactor(scope): [Magyar leírás]`

## Architektúra Rétegek

**Függőségi irány (lásd `docs/development/architecture_standards.md:28-41`):**
1. **UI** (`neural_ai/ui`) - Prezentáció, függhet az alatta lévő összes rétegtől
2. **Processors** (`neural_ai/processors`) - Domain logika, függ Data + Core-tól
3. **Data** (`neural_ai/data`) - Perzisztencia, függ csak Core-tól
4. **Collectors** (`neural_ai/collectors`) - Input, függ csak Core-tól
5. **Core** (`neural_ai/core`) - Infrastruktúra, önálló

Alsó rétegek SOHA nem tudnak a felső rétegekről.

## Modul Szervezési Minta

**Minden modulban van (lásd `docs/development/architecture_standards.md:79-104`):**
- `interfaces/` - Absztrakt szerződések (exportálva `__init__.py`-ban)
- `implementations/` - Konkrét kód (SOHA nem exportált, csak factory használja)
- `exceptions/` - Specifikus hibák
- `factory.py` - EGYETLEN hely ami importál `implementations/`-ból
- `__init__.py` - Exportál CSAK Interface + Factory-t

**Implementációk láthatatlanok:** Modulon kívül csak `XyzInterface`-t és `XyzFactory`-t látsz. Soha ne importálj `ConcreteXyz` osztályt.

## Config Minta

**TypedDict szükséges:** Minden `config.get()` hívás `Any`-t ad vissza. Factory-knak KÖTELEZŐ TypedDict sémát definiálni és castolni. Lásd `neural_ai/core/base/factory.py:25-48` példákért.

**Hibrid config rendszer:** `.env` statikushoz (környezet), YAML struktúrához, SQL dinamikus futásidejű változtatásokhoz (lásd `docs/planning/specs/02_dynamic_configuration.md`).

## Adat Formátumok

**JForex specifika:** Dukascopy `.bi5` (LZMA tömörített bináris) formátumot használ, NEM CSV-t. Dekóder: `neural_ai/collectors/jforex/implementations/bi5_downloader.py`.

**Storage formátum:** Csak particionált Parquet (`fastparquet` backend). CSV/JSON tilos `neural_ai/data/storage/`-ban. Backend kiválasztás hardver alapján (AVX2 → Polars, fallback → Pandas) `neural_ai/data/storage/backends/`-ban.

## Bootstrap Folyamat

**Inicializációs sorrend kritikus (lásd `neural_ai/core/base/factory.py:120-147`):**
1. HardwareInfo (AVX2/CUDA detektálás)
2. ConfigManager (.env + YAML betöltés)
3. Logger (config szükséges a szinthez)
4. EventBus (config szükséges portokhoz, logger)
5. Storage (config, logger, HardwareInfo szükséges backend választáshoz)
6. Database (config szükséges kapcsolathoz, logger)
7. SystemMonitor (az összes fenti szükséges)

Rossz sorrend = függőségi hibák.

## CLI Belépési Pontok

**Egységesített CLI `main.py`-ban:** Három mód - `live` (kereskedés), `download` (történeti adat), `dashboard` (Streamlit UI). Mindegyik abszolút útvonalakat használ conda env binárisokhoz a nem-interaktív shell limitáció miatt.
