# core/utils/decorators.py

Funkcionális dekorátorok a Neural AI Next rendszerhez.

Ez a modul a rendszer által használt dekorátorokat tartalmazza, beleértve
a `@trace` dekorátort, amely funkcióhívások nyomon követését és logolását
teszi lehetővé structlog segítségével.

## Függvények

### `_serialize_arg`

Egy argumentum biztonságos szöveges reprezentációját adja vissza.

    Csak biztonságos típusokat (str, int, float, bool, None) konvertál
    közvetlenül, minden egyéb típus esetén "UNSAFE_ARG" értéket ad vissza.

    Args:
        arg: A konvertálandó argumentum.

    Returns:
        Az argumentum szöveges reprezentációja, vagy "UNSAFE_ARG" ha a
        típus nem biztonságos.

### `trace`

Dekorátor a funkcióhívások nyomon követéséhez és logolásához.

    A dekorátor minden függvényhíváskor logolja a következő információkat:
    - call_id: Egyedi azonosító (UUID4)
    - function: A hívott függvény neve
    - args: A függvény argumentumainak biztonságos reprezentációja
    - duration_ms: A függvény futási ideje milliszekundumban

    A logolás DEBUG szinten történik a "neural_ai.trace" loggeren keresztül.

    Args:
        func: A dekorálandó függvény.

    Returns:
        A dekorált függvény, amely automatikusan logolja a hívásokat.

    Examples:
        >>> @trace
        ... def add(a: int, b: int) -> int:
        ...     return a + b
        ...
        >>> result = add(5, 3)
        # Log output:
        # call_id=... function=add args=['5', '3'] duration_ms=0.123

### `wrapper`

A dekorált függvényt becsomagoló wrapper függvény.

        Args:
            *args: Pozicionális argumentumok.
            **kwargs: Kulcsszavas argumentumok.

        Returns:
            A dekorált függvény visszatérési értéke.


---

**Forrásfájl:** [`core/utils/decorators.py`](../../../neural_ai/core/utils/decorators.py)
