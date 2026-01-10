# Validation End-to-End Script

## Áttekintés

A `scripts/validation_end_to_end.py` szkript végrehajtja a teljes end-to-end validációs folyamatot a CORE DATA PIPELINE teljes refaktorálásának ellenőrzésére.

## Funkciók

### 1. Adat Letöltés
- Letölti az EURUSD adatokat 2024-03-20-ra
- Használja a `scripts/download_history.py` szkriptet
- Ellenőrzi a letöltés sikerességét

### 2. Dashboard Indítás Tesztelése
- Indítja el a Streamlit dashboard-ot headless módban
- Vár 5 másodpercet az indulásra
- Ellenőrzi, hogy a folyamat stabilan fut
- Leállítja a dashboard-ot a teszt után

### 3. Adatok Validálása
- Használja a `StrategyService.get_candles()` metódust
- Ellenőrzi az új oszlopok jelenlétét:
  - `mid_open`, `mid_high`, `mid_low`, `mid_close`
  - `spread`
  - `rolling_z_score`
- Validálja az adatok minőségét:
  - Spread értékek nem NaN, nem 0
  - Z-Score értékek nem NaN, nem 0
  - Mid árak helyes számítása

## Használat

```bash
python scripts/validation_end_to_end.py
```

## Kimenet

A szkript részletes log üzeneteket ad:
- ✅ Sikeres műveletek
- ❌ Hibák és problémák
- 📊 Összegzés a végén

## Kapcsolódó Komponensek

- **scripts/download_history.py**: Adat letöltés
- **main.py dashboard**: Dashboard indítás
- **neural_ai/ui/services/strategy_service.py**: Adat lekérés és validálás
- **neural_ai/core/processing/resampler_service**: Adat feldolgozás

## Tesztelés

A szkriptet a `tests/scripts/test_validation_end_to_end.py` pytest teszt futtatja és validálja.