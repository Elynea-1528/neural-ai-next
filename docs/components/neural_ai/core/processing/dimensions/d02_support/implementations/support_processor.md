# D02SupportProcessor

## Áttekintés

A D02SupportProcessor felelős a support és resistance szintek azonosításáért és számításáért swing pontok alapján különböző timeframe-ekre.

## Főbb Metódusok

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
  - `"volume"`: float (volumen)
  - `"type"`: str ("high" vagy "low")

**Visszatérési érték:**
List[Dict[str, Union[float, int, str]]]: Összevont szintek listája [{"price": float, "touches": int, "type": "support"|"resistance", "strength": float}]

**Logika:**
1. Rendezés ár szerint (price kulcs alapján).
2. Iteratív összevonás: ha két swing közötti távolság <= level_merge, súlyozott átlag és touches összeadás.
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

## Architektúra

- **Base**: `BaseDimensionProcessor`
- **DI**: Constructor injection config és logger interfészeken keresztül
- **Adattípusok**: Szigorú Type Hints, Any tiltott
- **Importok**: Circular imports elkerülése `if TYPE_CHECKING` blokkal