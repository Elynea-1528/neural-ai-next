# 🧪 Teszt: tests/neural_ai/ui/services/test_navigation_service.py

**Tesztelt modul:** [`neural_ai/ui/services/navigation_service.py`](../../neural_ai/ui/services/navigation_service.py)

Unit tesztek a navigation_service modulhoz.

Ez a modul teszteli a NavigationService osztály funkcióit.

## Teszt Osztály: `TestNavigationServiceInit`

Tesztek a NavigationService inicializálásához.

### ✓ `test_init_creates_instance()`

Ellenőrzi, hogy a NavigationService létrehozható.

## Teszt Osztály: `TestNavigationServiceRegisterPage`

Tesztek a register_page metódushoz.

### ✓ `test_register_page_adds_page()`

Ellenőrzi, hogy az oldal regisztrálása működik.

### ✓ `test_register_first_page_sets_current()`

Ellenőrzi, hogy az első oldal automatikusan aktuális lesz.

## Teszt Osztály: `TestNavigationServiceNavigateTo`

Tesztek a navigate_to metódushoz.

### ✓ `test_navigate_to_raises_error_for_unknown_page()`

Ellenőrzi, hogy hiba dobódik ismeretlen oldalra navigáláskor.

### ✓ `test_navigate_to_calls_on_navigate_from_on_current_page()`

Ellenőrzi, hogy az aktuális oldal on_navigate_from metódusa meghívódik.

### ✓ `test_navigate_to_calls_on_navigate_to_on_new_page()`

Ellenőrzi, hogy az új oldal on_navigate_to metódusa meghívódik.

### ✓ `test_navigate_to_updates_history()`

Ellenőrzi, hogy a navigáció frissíti az előzményeket.

### ✓ `test_navigate_to_notifies_subscribers()`

Ellenőrzi, hogy a navigáció értesíti a feliratkozókat.

## Teszt Osztály: `TestNavigationServiceGoBack`

Tesztek a go_back metódushoz.

### ✓ `test_go_back_does_nothing_when_no_history()`

Ellenőrzi, hogy a go_back nem csinál semmit, ha nincs előzmény.

### ✓ `test_go_back_navigates_to_previous_page()`

Ellenőrzi, hogy a go_back visszanavigál az előző oldalra.

### ✓ `test_go_back_notifies_subscribers()`

Ellenőrzi, hogy a go_back értesíti a feliratkozókat.

## Teszt Osztály: `TestNavigationServiceGetCurrentPage`

Tesztek a get_current_page metódushoz.

### ✓ `test_get_current_page_returns_none_when_no_page()`

Ellenőrzi, hogy None-t ad vissza, ha nincs aktuális oldal.

### ✓ `test_get_current_page_returns_current_page()`

Ellenőrzi, hogy az aktuális oldalt adja vissza.

## Teszt Osztály: `TestNavigationServiceGetPageHistory`

Tesztek a get_page_history metódushoz.

### ✓ `test_get_page_history_returns_copy()`

Ellenőrzi, hogy az előzmények másolatát adja vissza.

## Teszt Osztály: `TestNavigationServiceSubscribe`

Tesztek a subscribe metódushoz.

### ✓ `test_subscribe_adds_callback()`

Ellenőrzi, hogy a feliratkozás hozzáadja a callback-et.

### ✓ `test_subscribe_callback_handles_exception()`

Ellenőrzi, hogy a callback kivétel esetén sem állítja le a rendszert.

---

**Teszt fájl:** [`tests/neural_ai/ui/services/test_navigation_service.py`](../../tests/neural_ai/ui/services/test_navigation_service.py)

**Tesztelt modul:** [`neural_ai/ui/services/navigation_service.py`](../../neural_ai/ui/services/navigation_service.py)
