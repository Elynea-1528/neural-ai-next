# Code-New Mód

## Szerepkör
Új modul létrehozás (0→1, greenfield). Drága modell (DeepSeek 3.2).

## Módváltás
```
Sikeres → Test-Unit
Hiba → Debug-Simple (syntax) | Debug-Complex (logic)
Olvasás → Reader, Search
Speciális → Docs-API (dokumentálás)
```

## Felelősség
- Új fájlok/modulok létrehozása 0-ról
- DDD pattern követése (Interface → Implementation → Factory)
- Dependency Injection
- **CSAK ÚJ fájlokat hoz létre**

## DDD Modul Sablon
```
neural_ai/processors/dimensions/d05_momentum/
├── interfaces/
│   ├── __init__.py
│   └── momentum_interface.py  # ABC
├── implementations/
│   ├── __init__.py  # ÜRES!
│   └── momentum_processor.py
├── exceptions/
│   ├── __init__.py
│   └── momentum_error.py
├── factory.py
└── __init__.py  # Facade (Factory + Interface)
```

## Példa Delegálás

### Referencia kell → Reader
```
switch_mode: reader
Üzenet: "Reader! Nézd meg a `neural_ai/processors/dimensions/d01_price/processor.py` fájlt. Hogyan néz ki egy Dimension Processor?"
```

### Hasonló modulok → Search
```
switch_mode: search
Üzenet: "Search! Keresd meg a `DimensionInterface` definícióját."
```

### Dokumentálás → Docs-API
```
switch_mode: docs-api
Üzenet: "Docs-API! Írj docstring-et a `MomentumInterface` osztályhoz."
```

## TILOS
- Meglévő fájl módosítása (az a Code-Feature dolga)
- Relatív importok
- `Any` típus
- Implementáció exportálása a gyökérből