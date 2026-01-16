# neural_ai/data/storage/interfaces/storage_interface.py

StorageInterface - Tárolási műveletek absztrakt interfésze.

Ez a protokoll definiálja a tárolási műveletek közös interfészét a különböző
tárolási backend-ek számára. Lehetővé teszi a polimorfikus használatot és
a könnyű tesztelhetőséget.

## Protokollok

### `StorageInterface`

Tárolási műveletek protokollja.

Ez a protokoll definiálja a szükséges metódusokat minden tárolási implementációhoz.

## Metódusok

- `save_dataframe`: DataFrame mentése
- `load_dataframe`: DataFrame betöltése
- `save_object`: Objektum mentése
- `load_object`: Objektum betöltése
- `exists`: Ellenőrzés, hogy létezik-e az útvonal
- `get_metadata`: Fájl metaadatainak lekérdezése
- `delete`: Fájl vagy könyvtár törlése
- `list_dir`: Könyvtár tartalmának listázása

---

**Forrásfájl:** [`neural_ai/data/storage/interfaces/storage_interface.py`](../../../neural_ai/data/storage/interfaces/storage_interface.py)