# neural_ai/__init__.py

## Áttekintés

Ez a modul a Neural-AI-Next projekt fő inicializációs pontja. Felelős a projekt verziószámának és alapvető publikus API-jának exportálásáért.

## Verziókezelés

A modul exportálja a projekt verziószámát a `__version__` változón keresztül, amely a `pyproject.toml` fájlból származik.

## Publikus API

### Verzió információk

```python
__version__: str
```

A projekt aktuális verziószáma (pl. "0.1.0").

## Használat

```python
import neural_ai

print(f"Neural-AI-Next verzió: {neural_ai.__version__}")
```

## Függőségek

Ez a modul nem rendelkezik belső függőségekkel, mivel csak a verziószámot exportálja. A tényleges funkcionalitás a `neural_ai.core` modulban található.

## Jövőbeli Fejlesztések

- Alapértelmezett konfiguráció exportálása
- Gyors inicializáló függvények hozzáadása
- Publikus API bővítése a leggyakrabban használt komponensekkel