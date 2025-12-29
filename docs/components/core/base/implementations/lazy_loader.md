# core/base/implementations/lazy_loader.py

Lustatöltés (lazy loading) segédeszközök.

Ez a modul a lustatöltés mechanizmust valósítja meg, amely lehetővé teszi,
hogy a drága erőforrások csak akkor töltődjenek be, amikor valóban szükség van rájuk.
Ez jelentősen javítja az alkalmazás indítási idejét és a memóriahasználatot.

## Osztályok

### `LazyLoader`

Drága erőforrások lustatöltője.

    Ez az osztály lehetővé teszi, hogy a drága erőforrások (pl. konfigurációk,
    adatbázis kapcsolatok, nagy adathalmazok) csak akkor töltődjenek be,
    amikor valóban szükség van rájuk.

    A lustatöltés szálbiztos, így többszálú környezetben is biztonságosan
    használható.


## Függvények

### `__init__`

Inicializálja a lustatöltőt.

        Args:
            loader_func: A függvény, amely betölti az erőforrást.
                Ennek a függvénynek vissza kell térnie a betöltött erőforrással.

### `_load`

Betölti az erőforrást, ha még nincs betöltve.

        Returns:
            A betöltött erőforrás.

        Note:
            Ez egy belső metódus, általában nem kell közvetlenül használni.
            Ehelyett használd a __call__ metódust.

### `__call__`

Visszaadja a betöltött erőforrást.

        Ha az erőforrás még nincs betöltve, először meghívja a betöltő függvényt.

        Returns:
            A betöltött erőforrás.

### `is_loaded`

Ellenőrzi, hogy az erőforrás betöltve van-e.

        Returns:
            True, ha az erőforrás betöltve van, egyébként False.

### `reset`

Visszaállítja a betöltőt az alaphelyzetbe.

        Ez kiüríti a betöltött erőforrást, lehetővé téve az újratöltést.
        Hasznos lehet tesztelés során vagy ha újra szeretnénk tölteni
        az erőforrást.

### `lazy_property`

Dekorátor lustatöltésű property-k létrehozásához.

    Ez a dekorátor egy olyan property-t hoz létre, amelynek értéke csak
    az első hozzáféréskor számolódik ki, majd gyorsítótárba kerül.
    A későbbi hozzáférések már a gyorsítótárazott értéket adják vissza.

    Args:
        func: A függvény, amely kiszámolja a property értékét.

    Returns:
        Egy property objektum lustatöltéssel.

    Példa:
        >>> class DataProcessor:
        ...     def __init__(self, data):
        ...         self._data = data
        ...     @lazy_property
        ...     def processed_data(self):
        ...         # Ez a kód csak egyszer fut le
        ...         return [x * 2 for x in self._data]
        >>> processor = DataProcessor([1, 2, 3])
        >>> # A processed_data még nincs kiszámolva
        >>> result = processor.processed_data  # Most fut le először
        >>> result2 = processor.processed_data  # Már gyorsítótárból jön

### `wrapper`

Nincs docstring.


---

**Forrásfájl:** [`core/base/implementations/lazy_loader.py`](../../../neural_ai/core/base/implementations/lazy_loader.py)
