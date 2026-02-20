# neural_ai/core/system/exceptions/health_error.py

Rendszer egészségügyi komponens kivételei.

Ez a modul tartalmazza a rendszer egészségügyi komponenshez tartozó kivételeket.

## Osztály: `HealthError(Exception)`

Alap kivétel a rendszer egészségügyi komponenshez.

## Osztály: `HealthMonitorError(HealthError)`

HealthMonitor általános hiba.

## Osztály: `HealthCheckError(HealthError)`

Egészségügyi ellenőrzés hiba.

## Osztály: `ComponentNotFoundError(HealthMonitorError)`

Komponens nem található hiba.

---

**Forrásfájl:** [`neural_ai/core/system/exceptions/health_error.py`](../../neural_ai/core/system/exceptions/health_error.py)
