# D02SupportProcessor

## Áttekintés

A D02SupportProcessor felelős a support és resistance szintek azonosításáért és számításáért swing pontok alapján különböző timeframe-ekre.

## Főbb Metódusok

### `process`

**Aláírás:**
```python
def process(self, df: pl.DataFrame, timeframe: str = "H1") -> pl.DataFrame
```

**Leírás:**
Support/Resistance szintek számítása swing pontok alapján. Detektálja a swingeket Body és Wick alapján, gyűjti őket listába VolumeFactor-ral, futtatja a szintek összevonását, erősség számítását és kategorizálását. Idősoros vetítés minden gyertyánál a legközelebbi support/resistance-hez.

**Paraméterek:**
- `df`: Bemeneti Polars DataFrame (time-aligned OHLCV adatok)
- `timeframe`: Időkeret ("H1", "H4", "D1"), default "H1"

**Visszatérési érték:**
Polars DataFrame frissített oszlopokkal: swing_high_body, swing_low_body, swing_high_wick, swing_low_wick, nearest_resistance, nearest_support, resistance_strength, support_strength.

**Logika:**
1. Swing pontok keresése záró/nyitó árak alapján (_find_swing_points_close_open)
2. Swing pontok keresése high/low értékeken (_find_swing_points_high_low)
3. Volume factor számítása minden swing típushoz (_confirm_with_volume)
4. Swing pontok gyűjtése listába: [{"timestamp": timestamp, "price": price, "type": type, "volume_factor": factor}]
5. Szintek összevonása (_merge_levels)
6. Szintek erősségének számítása (_calculate_level_strength)
7. Szintek kategorizálása (_categorize_zones) - opcionális, jelenleg nem használjuk tovább
8. Idősoros vetítés: minden sorhoz megtalálja a legközelebbi support (max price <= close) és resistance (min price >= close) az összes szint közül, strength-szel együtt
9. Frissített DataFrame visszaadása

### `_merge_levels`

**Aláírás:**
```python
def _merge_levels(self, swings: List[Dict[str, Union[float, str]]]) -> List[Dict[str, Union[float, int, str]]]
```

**Leírás:**
A swing pontokat ár szerint rendezi, majd iteratívan összevonja azokat, amelyek a `level_merge` távolságon belül vannak. Az összevonás során súlyozott átlagot számol az árak és volumenek alapján, és összeadja az érintéseket (touches).

**Paraméterek:**
- `swings`: Swing pontok listája, ahol minden dict tartalmazza:
  - `"price"`: float (ár)
  - `"volume_factor"`: float (volumen faktor)
  - `"type"`: str ("high" vagy "low")

**Visszatérési érték:**
List[Dict[str, Union[float, int, str]]]: Összevont szintek listája [{"price": float, "touches": int, "type": "support"|"resistance", "strength": float}]

**Logika:**
1. Rendezés ár szerint (price kulcs alapján).
2. Iteratív összevonás: ha két swing közötti távolság <= level_merge, súlyozott átlag az áraknak volume_factor alapján, touches összeadás.
3. Type mapping: "high" -> "resistance", "low" -> "support"
4. Strength = touches (float-ként)

**Konfiguráció:**
- `level_merge`: Küszöb távolság az összevonáshoz (alapértelmezett: 0.0005)

### `_calculate_level_strength`

**Aláírás:**
```python
def _calculate_level_strength(self, levels: List[Dict[str, Union[float, int, str]]]) -> List[Dict[str, Union[float, int, str]]]
```

**Leírás:**
Minden szinthez kiszámolja a strength értéket az érintések, súly és volumen tényező alapján, majd normalizálja 0-1 közé.

**Paraméterek:**
- `levels`: Szintek listája dict-ekkel, amelyek tartalmazzák 'touches' és opcionálisan 'volume_factor'.

**Visszatérési érték:**
List[Dict[str, Union[float, int, str]]]: Frissített szintek listája 'strength' kulccsal.

**Logika:**
1. Minden szinthez: strength = (touches * base_weight) * volume_factor, ahol base_weight = 0.1, volume_factor alapértelmezett 1.0.
2. Normalizálás 0-1 közé a lista maximális strength értékéhez viszonyítva.

**Konfiguráció:**
- `strength_window`: Visszatekintési ablak paraméter (alapértelmezett: 10), releváns a strength számításnál.

### `_categorize_zones`

**Aláírás:**
```python
def _categorize_zones(self, levels: List[Dict[str, Union[str, float, int]]]) -> Dict[str, Dict[str, List[Dict[str, Union[str, float, int]]]]]
```

**Leírás:**
A szinteket kategorizálja strength és touches alapján support és resistance kategóriákba, majd minden kategóriában további alcsoportokba: strong, moderate, weak.

**Paraméterek:**
- `levels`: Szintek listája dict-ekkel, melyek tartalmazzák 'strength', 'touches', 'type' stb.

**Visszatérési érték:**
Dict[str, Dict[str, List[Dict[str, Union[str, float, int]]]]]: Kategorizált szintek struktúrája:
```python
{
    "support": {"strong": [...], "moderate": [...], "weak": [...]},
    "resistance": {"strong": [...], "moderate": [...], "weak": [...]}
}
```

**Logika:**
1. Inicializálja az eredmény struktúrát üres listákkal.
2. Minden szinthez ellenőrzi a kategorizálási szabályokat:
   - Strong: strength > 0.7 és touches >= min_touches
   - Moderate: strength 0.3-0.7 vagy (touches < min_touches és strength > 0.4)
   - Weak: minden más eset
3. Hozzáadja a megfelelő lista végéhez a szintet.

**Konfiguráció:**
- `min_touches`: Minimális érintések száma a strong kategorizáláshoz (alapértelmezett: 1)

## Architektúra

- **Base**: `BaseDimensionProcessor`
- **DI**: Constructor injection config és logger interfészeken keresztül
- **Adattípusok**: Szigorú Type Hints, Any tiltott
- **Importok**: Circular imports elkerülése `if TYPE_CHECKING` blokkal