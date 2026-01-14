# validation_end_to_end.py

## Áttekintés

Az `validation_end_to_end.py` szkript a Neural AI Next rendszer teljes end-to-end validációját végzi el. Ez a szkript ellenőrzi a CORE DATA PIPELINE helyes működését az adatletöltéstől a dashboard indításán keresztül az adatok validálásáig.

## Architektúra

### Inicializálás
A szkript a `CoreBridge` komponenst használja a rendszer inicializálására és a `StrategyService` elérésére:

```python
bridge = CoreBridge()
bridge.initialize()
strategy_service = bridge.get_component("strategy_service")
```

Ez a Dependency Injection minta szerint biztosítja, hogy a rendszer komponensek helyesen legyenek inicializálva és összekapcsolva.

### Validációs Lépések

1. **Adat letöltés**: EURUSD adatokat tölt le egy napra a JForex rendszerből
2. **Dashboard indítás**: Ellenőrzi a Streamlit dashboard headless indítását
3. **Adat validáció**: A Strategy Service-en keresztül ellenőrzi az adatok helyességét

## Használat

```bash
python scripts/validation_end_to_end.py
```

## Validációs Ellenőrzések

### Kötelező Oszlopok
- `timestamp`
- `bid_open`, `bid_high`, `bid_low`, `bid_close`
- `mid_close`

### Új Oszlopok
- `mid_open`, `mid_high`, `mid_low`, `mid_close`
- `spread`
- `real_volume`, `tick_volume`
- `bid_volume`, `ask_volume`

### Adat Minőségi Ellenőrzések
- Spread értékek: nem NaN, nem 0
- Z-Score értékek: nem NaN, nem 0
- Mid árak: érvényes numerikus értékek

## Kimenet

Sikeres validáció esetén:
```
🧠 NEURAL AI NEXT - END-TO-END VALIDÁCIÓ
============================================================
📥 Adat letöltés indítása: EURUSD 2024-03-20
✅ Adat letöltés sikeres
🖥️ Dashboard indítás tesztelése (headless mód)
✅ Dashboard sikeresen indult (Xs)
🔍 Adatok validálása Strategy Service-en keresztül
✅ X gyertya adat betöltve
✅ Minden új oszlop jelen van: [...]
✅ Spread értékek rendben (átlag: X.XXXXXX)
✅ Z-Score értékek rendben (átlag: X.XXXXXX)
✅ Minden adat validáció sikeres
============================================================
📊 VALIDÁCIÓ EREDMÉNYE
============================================================
✅ Sikeres lépések: 3/3
🎉 END-TO-END VALIDÁCIÓ SIKERES!
A CORE DATA PIPELINE teljes refaktorálása helyesen működik.
```

## Függőségek

- `CoreBridge`: Rendszer inicializálás
- `StrategyService`: Adatok elérés és validáció
- `requests`: Dashboard health check
- `subprocess`: Külső szkriptek futtatása
- `pandas`: Adat manipuláció

## Hiba Kezelés

A szkript részletes hiba üzeneteket ad minden lépésnél, és azonnal leállítja a validációt az első hiba esetén.</content>
</xai:function_call">Lagarde