# neural_ai/core/base/implementations/__init__.py

Implementációk a base modulhoz.

Ez a csomag tartalmazza a base modul különböző implementációit.
FIGYELEM: Ez a fájl ÜRES kell legyen! Implementációkat CSAK a factory.py importálhatja.

A DDD Architecture Standards szerint az implementations/ mappa __init__.py fájlja
NEM exportálhat semmit. Minden importot közvetlenül a konkrét fájlokból kell végezni:

Helyes:
    from neural_ai.core.base.implementations.di_container import DIContainer

Helytelen:
    from neural_ai.core.base.implementations import DIContainer

---

**Forrásfájl:** [`neural_ai/core/base/implementations/__init__.py`](../../neural_ai/core/base/implementations/__init__.py)
