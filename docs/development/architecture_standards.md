# ARCHITECTURE STANDARDS v2.0

## 1. MODUL STRUKTÚRA
Minden `neural_ai/core/[MODUL]` könyvtárnak így KELL kinéznie:

- `__init__.py`: Kiexportálja a Factory-t és a publikus Interfészt. Tilos mást!
- `factory.py`: A modul EGYETLEN belépési pontja.
- `interfaces/`:
  - `__init__.py`: Kiexportálja az ABC osztályokat.
  - `[modul]_interface.py`: Az absztrakt bázisosztály.
- `implementations/`:
  - `__init__.py`: ÜRES vagy csak belső használatra.
  - `[konkrét_tech].py`: A tényleges kód (pl. `zeromq_bus.py`).
- `exceptions/`:
  - `__init__.py`: Kiexportálja a hibákat (`from .base_error import MyError`).
  - `[modul]_error.py`: A specifikus kivételek.

## 2. IMPORT SZABÁLYOK
- **TILOS:** Relatív import (`from .. import`).
- **KÖTELEZŐ:** Abszolút import (`from neural_ai.core.logger.interfaces import LoggerInterface`).
- **KÖTELEZŐ:** Az `exceptions` mappából való importálásnál az `__init__.py`-on keresztül kell hivatkozni!
  - Helyes: `from neural_ai.core.base.exceptions import ComponentNotFoundError`
  - Helytelen: `from neural_ai.core.base.exceptions.base_error import ComponentNotFoundError`