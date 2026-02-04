# AGENTS.md

Ez a fájl útmutatást nyújt az AI agenteknek a repository kódjával való munkavégzéshez.

## 🏛️ HIERARCHIKUS VÉGREHAJTÁSI PROTOKOLL

A Neural AI Next rendszer hierarchikus AI ágensrendszert használ. Minden komplex feladatot ebben a láncban kell végrehajtani:

```
1. ARCHITECT (Tervező)
   ├─> 2. ORCHESTRATOR (Delegáló)
        ├─> 3. CODE (Végrehajtó) [taskonként]
        └─> 4. DEBUG (Javító) [szükség esetén]
```

**Feladatmegosztás:**
- **ARCHITECT:** Tervez, elemez, TASK_TREE-t vezet. Nem nyúl kódhoz.
- **ORCHESTRATOR:** Lebontja a tervet fájlműveletekre, delegál Code Agent-nek.
- **CODE:** Kódot ír, tesztel, commitol az orchestrator utasításai alapján.
- **DEBUG:** Hibákat javít, teszteket helyreállít.
- **ASK:** Read-only információszolgáltatás.

**Kritikus szabály:** Az architect NEM írhat kódot közvetlenül, csak az orchestrator-on keresztül delegálhat!

---

## Build/Test/Lint Parancsok

```bash
# Tesztek futtatása abszolút útvonallal (conda activate nem működik nem-interaktív shell-ben)
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest

# Egyetlen teszt fájl futtatása
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/path/to/test_file.py -v

# Linter futtatása
/home/elynea/miniconda3/envs/neural-ai-next/bin/ruff check .

# Alkalmazás módok futtatása
python main.py live                    # Élő kereskedési mód
python main.py download --symbol EURUSD --start 2024-03-20 --end 2024-03-20
python main.py dashboard               # Streamlit UI
```

---

## Kritikus Nem-Nyilvánvaló Szabályok

**TypedDict KÖTELEZŐ a Config-oknál:** Minden `config.get()` `Any`-t ad vissza - Factory metódusokban KÖTELEZŐ TypedDict-re castolni `cast()` használatával. Példa: `neural_ai/core/base/factory.py:220-235`.

**TILOS direkt import az implementations/-ból:** Factory-ban lazy load, máshol csak Interface import. Konkrét osztályok (`ConcreteClass`) TILOS a modulon kívül.

**Körkörös importok:** Használd az `if TYPE_CHECKING:` blokkot + string típus hinteket (pl. `storage: "StorageInterface"`).

**Strukturált logolás KÖTELEZŐ:** `logger.info("msg", extra={"key": val})` - string összefűzés (f-stringek log üzenetekben) TILOS.

**Polars First:** Használj `pl.DataFrame`-et adatfeldolgozáshoz. Pandas csak UI rétegben (`neural_ai/ui/`). Sor iteráció (`for row in df`) TILOS.

**JForex TILOS CSV:** Csak `.bi5` (LZMA) bináris formátum engedélyezett. Lásd: `neural_ai/collectors/jforex/`.

**Storage TILOS CSV/JSON:** Csak particionált Parquet (`fastparquet`). Helye: `neural_ai/data/storage/`.

**Magyar docstringek:** MINDEN docstring, komment, commit KÖTELEZŐEN magyar (Google Style). Kód kulcsszavak angolul.

**Mirror dokumentáció:** Minden kódfájl `neural_ai/X/Y.py` igényel `docs/components/X/Y.md` fájlt (auto-generált: `python scripts/generate_docs.py`).

**Atomic commitok KÖTELEZŐ:** Minden fájlmódosítás azonnali `git commit`-ot igényel. Nincs commit = BUKOTT feladat.

**Bootstrap sorrend fontos:** `HardwareInfo` → `ConfigManager` → `Logger` → `EventBus` → `Storage` → `Database` → `SystemMonitor`. Lásd: `neural_ai/core/base/factory.py:120-147`.
