# 🏛️ Kódolási Szabványok (Coding Standards)

Ez a dokumentum tartalmazza a Neural AI Next projekt kötelező érvényű technikai szabályait. Minden AI Agent-nek (Code, Debug, QA) szigorúan követnie kell.

## 1. Típusrendszer és Konfiguráció

- **Pydantic Kötelező:** Konfigurációs objektumok validálására (`config.get()` eredménye) MINDIG Pydantic modellt (`BaseModel`) használj.
- **TypedDict TILOS:** A Pydantic helyettesíti.
- **Strict Typing:** `Any` típus használata TILOS. Minden függvény paramétert és visszatérési értéket típus hinttel kell ellátni.

## 2. Adatkezelés (Polars First)

- **Polars (`pl.DataFrame`):** KÖTELEZŐ a `neural_ai/processors/` és `neural_ai/data/` rétegekben.
- **Pandas:** KIZÁRÓLAG a `neural_ai/ui/` rétegben engedélyezett (Streamlit kompatibilitás miatt).
- **Iteráció TILOS:** `for row in df` használata szigorúan tilos. Használj vektorizált `pl.Expr` műveleteket.

## 3. Logolás (Strukturált)

- **Formátum:** `logger.info("Üzenet", extra={"kulcs": "érték"})`
- **TILOS:** f-stringek log üzenetekben (`logger.info(f"Érték: {val}")` ❌).
- **TILOS:** `print()` utasítás használata (kivéve CLI belépési pontok `if __name__ == "__main__"` blokkjában).

## 4. Import Szabályok

- **Körkörös Import:** Használd az `if TYPE_CHECKING:` blokkot és string annotációkat (`storage: "StorageInterface"`).
- **Implementáció Rejtése:** Konkrét osztályokat (`ConcreteClass`) SOHA ne importálj a modulon kívül. Csak `Interface` és `Factory` publikus.
- **Factory Pattern:** Az `implementations/` mappa tartalmát CSAK a `factory.py` importálhatja.

## 5. Fájlformátumok

- **JForex:** KIZÁRÓLAG `.bi5` (LZMA tömörített bináris). CSV/JSON használata TILOS a `neural_ai/collectors/jforex/` modulban.
- **Storage:** KIZÁRÓLAG particionált Parquet (`fastparquet`). CSV/JSON használata TILOS a `neural_ai/data/storage/` modulban.

## 6. Dokumentáció

- **Nyelv:** MINDEN docstring, komment és commit üzenet **MAGYAR** (Google Style).
- **Mirror Dokumentáció:** Minden `neural_ai/X/Y.py` fájlhoz léteznie kell egy `docs/components/X/Y.md` fájlnak.

## 7. Tesztelés

- **Útvonalak:** Abszolút útvonalakat használj: `/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest`.
- **Lefedettség:** Domain réteg (Processors, Data) 100% teszt lefedettséget igényel.
