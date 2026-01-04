# Streamlit Dashboard Application

## Áttekintés

Ez a dokumentáció a Neural AI Next Streamlit dashboard alkalmazását mutatja be. A dashboard a rendszer állapotát és teljesítményét jeleníti meg vizuális felületen keresztül.

## Fájl

- **Elérési út:** [`neural_ai/ui/streamlit_app.py`](../neural_ai/ui/streamlit_app.py:1)
- **Típus:** Streamlit Application
- **Verzió:** 0.5.0

## Funkciók

### Főbb Komponensek

1. **Rendszer Áttekintés (System Overview)**
   - Core komponensek állapota
   - Adatbázis kapcsolat
   - Event Bus állapota
   - Adatgyűjtők állapota

2. **Egészségügyi Állapot (Health Status)**
   - Komponensek egészségügyi státusza
   - OK/WARNING/ERROR státuszok
   - Progress bar-ok a státuszok megjelenítéséhez

3. **Teljesítmény Metrikák (Performance Metrics)**
   - CPU használat
   - Memória használat
   - Disk használat
   - Válaszidő

4. **Legutóbbi Tevékenységek (Recent Activities)**
   - Rendszer események listája
   - Timestamp-ekkel
   - Típusok szerinti csoportosítás (INFO, SUCCESS, WARNING, ERROR)

### Oldalsáv (Sidebar)

- Frissítés gomb
- Navigáció
- Verzió információ
- Rendszer státusz

## Használat

### Alapértelmezett indítás

```bash
python main.py dashboard
```

### Opcionális argumentumok

```bash
# Egyéni hoszt és port
python main.py dashboard --host 0.0.0.0 --port 8501

# Headless mód (nincs browser automatikus megnyitása)
python main.py dashboard --headless

# Összes opció együtt
python main.py dashboard --host 0.0.0.0 --port 9999 --headless
```

## Argumentumok

| Argumentum | Alias | Típus | Alapértelmezett | Leírás |
|------------|-------|-------|-----------------|---------|
| `--host` | - | string | `localhost` | A szerver hosztja |
| `--port` | - | integer | `8501` | A szerver portja |
| `--headless` | - | flag | `False` | Headless mód (nincs browser automatikus megnyitása) |

## Függőségek

- `streamlit>=1.30.0` - A Streamlit web framework
- `neural_ai.ui.app.UIApplication` - A fő UI alkalmazás
- `neural_ai.ui.factory.UIServiceFactory` - UI szolgáltatások factory-ja
- `neural_ai.ui.interfaces.dashboard_service_interface.DashboardServiceInterface` - Dashboard szolgáltatás interfész

## Architektúra

### Komponensek

```
streamlit_app.py
├── setup_page_config()          # Oldal konfiguráció
├── render_header()              # Fejléc renderelés
├── render_system_overview()     # Rendszer áttekintés
├── render_health_status()       # Egészségügyi állapot
├── render_performance_metrics() # Teljesítmény metrikák
├── render_recent_activities()   # Tevékenységek listázása
├── render_sidebar()             # Oldalsáv
└── main()                       # Fő alkalmazás
```

### Adatfolyam

1. **Inicializálás:** A `UIApplication` létrehozása és inicializálása
2. **Szolgáltatások lekérése:** Dashboard service lekérése a factory-n keresztül
3. **Adatok lekérdezése:** A dashboard service metódusainak hívása
4. **Renderelés:** A kapott adatok vizuális megjelenítése
5. **Leállítás:** Az alkalmazás leállítása és erőforrások felszabadítása

## Hibakezelés

A dashboard robusztus hibakezeléssel rendelkezik:

- **Inicializálási hibák:** Hibaüzenet megjelenítése és alkalmazás leállítása
- **Szolgáltatás hibák:** Hibaüzenet a hibás komponensnél, de a többi komponens tovább működik
- **Adatlekérdezési hibák:** Hibaüzenet megjelenítése és a felhasználó értesítése

## Testreszabás

### Stílus

A dashboard testreszabható CSS segítségével:

```python
st.markdown("""
    <style>
    .stMetric {
        background-color: #f0f0f0;
        padding: 10px;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)
```

### Új Komponensek

Új komponensek hozzáadása:

```python
def render_custom_component(app: UIApplication) -> None:
    """Egyéni komponens renderelése."""
    st.header("Egyéni Komponens")
    # Implementáció
```

## Fejlesztés

### Helyi fejlesztés

```bash
# Streamlit indítása fejlesztési módban
streamlit run neural_ai/ui/streamlit_app.py --server.headless true

# Vagy a main.py-n keresztül
python main.py dashboard --headless
```

### Hot Reload

A Streamlit automatikusan újratölti az alkalmazást fájlmódosítás esetén.

## Biztonság

- **Hoszt kötés:** Alapértelmezésben csak localhost-ra köt, de konfigurálható 0.0.0.0-ra
- **Port választás:** Konfigurálható port használata
- **Headless mód:** Lehetőség szerver környezetben való futtatásra

## Kapcsolódó Dokumentáció

- [UI Architecture](architecture.md) - UI architektúra áttekintése
- [Dashboard Service](../services/dashboard_service.md) - Dashboard szolgáltatás dokumentációja
- [UI Application](app.md) - Fő UI alkalmazás dokumentációja
- [Main CLI Entry Point](../../main.md) - Fő CLI belépési pont dokumentációja

## Verziótörténet

- **0.5.0** - Kezdeti verzió
  - Rendszer áttekintés
  - Egészségügyi állapot
  - Teljesítmény metrikák
  - Tevékenységek listázása
  - Oldalsáv navigáció