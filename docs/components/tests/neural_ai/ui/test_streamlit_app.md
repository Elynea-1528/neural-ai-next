# 🧪 Teszt: tests/neural_ai/ui/test_streamlit_app.py

**Tesztelt modul:** [`neural_ai/ui/streamlit_app.py`](../../neural_ai/ui/streamlit_app.py)

Unit tesztek a streamlit_app modulhoz.

Ez a modul teszteli a Streamlit dashboard alkalmazás funkcióit.

## Teszt Osztály: `TestSetupPageConfig`

Tesztek a setup_page_config függvényhez.

### ✓ `test_setup_page_config_calls_set_page_config()`

Ellenőrzi, hogy a setup_page_config meghívja a st.set_page_config-ot.

## Teszt Osztály: `TestRenderHeader`

Tesztek a render_header függvényhez.

### ✓ `test_render_header_displays_markdown()`

Ellenőrzi, hogy a render_header megjeleníti a fejléc markdown-t.

## Teszt Osztály: `TestRenderSystemOverview`

Tesztek a render_system_overview függvényhez.

### ✓ `test_render_system_overview_displays_health_status()`

Ellenőrzi, hogy a render_system_overview megjeleníti a rendszer állapotot.

### ✓ `test_render_system_overview_handles_warning_status()`

Ellenőrzi, hogy a render_system_overview kezeli a WARNING státuszt.

### ✓ `test_render_system_overview_handles_error_status()`

Ellenőrzi, hogy a render_system_overview kezeli az ERROR státuszt.

### ✓ `test_render_system_overview_handles_exception()`

Ellenőrzi, hogy a render_system_overview kezeli a kivételeket.

## Teszt Osztály: `TestMain`

Tesztek a main függvényhez.

### ✓ `test_main_initializes_and_renders()`

Ellenőrzi, hogy a main inicializálja és rendereli az alkalmazást.

### ✓ `test_main_handles_initialization_error()`

Ellenőrzi, hogy a main kezeli az inicializálási hibákat.

---

**Teszt fájl:** [`tests/neural_ai/ui/test_streamlit_app.py`](../../tests/neural_ai/ui/test_streamlit_app.py)

**Tesztelt modul:** [`neural_ai/ui/streamlit_app.py`](../../neural_ai/ui/streamlit_app.py)
