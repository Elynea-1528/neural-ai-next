# Data Hub Page

## Áttekintés

A `DataHubPage` osztály a Neural AI Next rendszer adatkezelő központját reprezentálja. Ez az oldal felelős az adatok listázásáért, történelmi adatok letöltéséért és az adatok exportálásáért a DataService segítségével.

## Osztály Struktúra

### Név
`neural_ai.ui.pages.03_📥_Data_Hub.DataHubPage`

### Ősosztály
`PageInterface`

### Konstruktor

```python
def __init__(self, bridge: "CoreBridgeInterface", **kwargs: Any) -> None
```

**Paraméterek:**
- `bridge`: A CoreBridge példány, amelyen keresztül elérjük a backendet
- `**kwargs`: További opcionális argumentumok

## Metódusok

### `render()`

Az oldal megjelenítése Streamlit segítségével.

**Visszatérési érték:** `None`

**Stabilizálás:**
A metódus egy try-except blokkal van védve, amely lefedi a teljes metódus törzsét. Ha hiba történik, a rendszer `st.error` segítségével jelzi a hibát, majd `st.exception(e)` segítségével megjeleníti a teljes traceback-et, ezzel megelőzve a "fehér képernyő" problémát.

**Implementáció:**
```python
def render(self) -> None:
    """Az oldal megjelenítése Streamlit segítségével."""
    try:
        st.title(self._title)
        
        # Adatszolgáltatás lekérdezése a factory-n keresztül
        if self._data_service is None:
            from neural_ai.ui.factory import UIServiceFactory
            
            factory = UIServiceFactory()
            if not factory.is_initialized:
                st.error("A UI Service Factory nincs inicializálva")
                return
            
            self._data_service = factory.get_data_service()
        
        # Oldalsáv menü
        menu_options = [
            "Adatok listázása",
            "Történelmi adatok letöltése",
            "Adatok exportálása",
        ]
        selected_menu = st.sidebar.selectbox("Menü", menu_options)
        
        if selected_menu == "Adatok listázása":
            self._render_data_listing()
        elif selected_menu == "Történelmi adatok letöltése":
            self._render_download_history()
        elif selected_menu == "Adatok exportálása":
            self._render_data_export()
    
    except Exception as e:
        st.error("Váratlan hiba történt a Data Hub oldal megjelenítése során.")
        st.exception(e)
```

### `_render_data_listing()`

Elérhető adatok listázásának megjelenítése.

**Visszatérési érték:** `None`

### `_render_download_history()`

Történelmi adatok letöltésének megjelenítése.

**Visszatérési érték:** `None`

### `_render_data_export()`

Adatok exportálásának megjelenítése.

**Visszatérési érték:** `None`

### `on_navigate_to(params: dict[str, Any] | None = None)`

Az oldalra navigáláskor meghívott metódus.

**Paraméterek:**
- `params`: Opcionális navigációs paraméterek

**Visszatérési érték:** `None`

### `on_navigate_from()`

Az oldalról navigáláskor meghívott metódus.

**Visszatérési érték:** `None`

## Property-k

### `title`

Az oldal címe.

**Típus:** `str`

**Érték:** `"📥 Data Hub"`

### `is_loaded`

Az oldal betöltöttségi állapota.

**Típus:** `bool`

**Érték:** `True`, ha az oldal betöltődött, egyébként `False`

## Függőségek

- `neural_ai.ui.interfaces.data_service_interface.DataServiceInterface`: Adatszolgáltatás interfész
- `neural_ai.ui.interfaces.page_interface.PageInterface`: Oldal interfész
- `neural_ai.ui.interfaces.core_bridge_interface.CoreBridgeInterface`: CoreBridge interfész
- `neural_ai.ui.factory.UIServiceFactory`: UI Service Factory

## Használat

```python
from neural_ai.ui.pages.data_hub_page import DataHubPage
from neural_ai.ui.interfaces.core_bridge_interface import CoreBridgeInterface

# CoreBridge létrehozása
bridge = CoreBridgeInterface()

# DataHubPage létrehozása
data_hub_page = DataHubPage(bridge)

# Oldal megjelenítése
data_hub_page.render()
```

## Stabilizálás

A `render()` metódus stabilizálva van egy try-except blokkal, amely biztosítja, hogy a váratlan hibák ne vezessenek "fehér képernyő" problémához. Hiba esetén a rendszer:

1. Megjeleníti a hibaüzenetet `st.error` segítségével
2. Kiírja a teljes traceback-et `st.exception(e)` segítségével
3. Lehetővé teszi a felhasználó számára, hogy továbbra is használhassa az alkalmazást

## Tesztelés

A DataHubPage osztályt a `tests/ui/pages/test_data_hub_page.py` fájlban lévő tesztek ellenőrzik. A tesztek a következőket ellenőrzik:

- Inicializálás
- Property-k helyes működése
- Navigációs metódusok
- Renderelés sikeres esetben
- Renderelés factory inicializálatlan állapotban
- Renderelés kivétel esetén (stabilizálás tesztje)
- Belső renderelő metódusok

**Teszt eredmény:** 11/11 teszt sikeres

## Kapcsolódó Dokumentáció

- [UI Factory](ui/factory.md)
- [Data Service Interface](ui/interfaces/data_service_interface.md)
- [Page Interface](ui/interfaces/page_interface.md)
- [Core Bridge Interface](ui/interfaces/core_bridge_interface.md)