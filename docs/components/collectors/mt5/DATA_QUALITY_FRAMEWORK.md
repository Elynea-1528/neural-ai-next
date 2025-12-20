# Data Quality Framework - MT5 Collector

## Áttekintés

A Data Quality Framework egy komprehenzív adatminőség-ellenőrzési és validációs keretrendszer, amely a historikus adatok minőségét biztosítja az MT5 Collector komponensben.

### Főbb jellemzők

- **3-szintű validációs rendszer**: Alap, logikai és statisztikai validáció
- **Kiugró érték detektálás**: IQR, Z-Score és Moving Average módszerekkel
- **Automatikus javítás**: Intelligens adatkorrekciós képességek
- **Minőségjelentések**: CSV és JSON formátumban
- **Minőségkövetés**: Trendanalízis és teljesítménymetrikák
- **API végpontok**: RESTful API a minőségadatok lekérdezéséhez

---

## Architektúra

### Komponensek

```
┌─────────────────────────────────────────────────────────────┐
│                    Data Quality Framework                    │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────────┐  ┌─────────────────┐                   │
│  │  OutlierDetector│  │  DataValidator  │                   │
│  │  - IQR          │  │  - Level 1      │                   │
│  │  - Z-Score      │  │  - Level 2      │                   │
│  │  - Moving Avg   │  │  - Level 3      │                   │
│  └─────────────────┘  └─────────────────┘                   │
│                                                               │
│  ┌─────────────────┐  ┌─────────────────┐                   │
│  │  Auto-Corrector │  │  QualityMetrics │                   │
│  │  - Interpolation│  │  - Completeness │                   │
│  │  - Swap values  │  │  - Accuracy     │                   │
│  │  - Gap filling  │  │  - Consistency  │                   │
│  └─────────────────┘  └─────────────────┘                   │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Report Generator                                    │   │
│  │  - JSON reports                                      │   │
│  │  - CSV reports                                       │   │
│  │  - Quality trends                                    │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 3-szintű validációs rendszer

### Level 1 - Alap validálás

**Cél**: Adatstruktúra, típusok és kötelező mezők ellenőrzése

**Ellenőrzések**:
- Kötelező mezők jelenléte
- Adattípusok helyessége
- Üres értékek detektálása
- Alapvető formátumellenőrzés

**Példa**:
```python
# Hiányzó kötelező mezők
Missing required fields: ['open', 'high']

# Érvénytelen adattípusok
Invalid types: ['volume']

# Üres értékek
Missing values: 15
```

### Level 2 - Logikai validálás

**Cél**: Ártartományok, időbélyegek és konzisztencia ellenőrzése

**Ellenőrzések**:
- OHLC kapcsolatok (High >= Low, stb.)
- Bid-Ask kapcsolat (Ask >= Bid)
- Időbeli kronológia
- Volume értékek (nem negatív)
- Spread ellenőrzés

**Példa**:
```python
# High < Low esetek
Invalid OHLC: 3 cases

# Időbeli visszafordulások
Time sequence: 2 cases

# Nagy spread értékek
Large spread: 8 cases
```

### Level 3 - Statisztikai validálás

**Cél**: Kiugró értékek, trendek és volatilitás ellenőrzése

**Ellenőrzések**:
- Kiugró értékek detektálása (IQR, Z-Score, Moving Average)
- Volatilitás analízis
- Trendek ellenőrzése
- Anomália detektálás

**Példa**:
```python
# Kiugró értékek IQR módszerrel
Outliers (IQR): 12 cases (1.2%)

# Magas volatilitás
High volatility: 5 cases

# Alacsony volatilitás
Low volatility: 150 cases
```

---

## Kiugró érték detektálás

### IQR (Interquartile Range) módszer

**Elv**: A kiugró értékeket a kvartilisek alapján azonosítja.

**Képlet**:
```
IQR = Q3 - Q1
Lower Bound = Q1 - 1.5 * IQR
Upper Bound = Q3 + 1.5 * IQR
```

**Konfiguráció**:
```python
detector.detect_iqr(data, threshold=1.5)
```

**Használat**: Általános célú kiugró érték detektálásra

### Z-Score módszer

**Elv**: A standard eltérések számát használja a kiugró értékek azonosításához.

**Képlet**:
```
Z = (X - μ) / σ
Outlier if |Z| > threshold
```

**Konfiguráció**:
```python
detector.detect_z_score(data, threshold=3.0)
```

**Használat**: Statisztikailag szignifikáns kiugró értékekre

### Moving Average módszer

**Elv**: Mozgóátlag és szórás alapján azonosítja a kiugró értékeket.

**Képlet**:
```
MA = Rolling Mean(window=20)
Upper Bound = MA + 2 * Rolling Std
Lower Bound = MA - 2 * Rolling Std
```

**Konfiguráció**:
```python
detector.detect_moving_average(data, window=20, threshold=2.0)
```

**Használat**: Idősor-adatok kiugró értékeinek detektálására

---

## Automatikus javítás

### Támogatott javítási módszerek

#### 1. Hiányzó értékek interpolációja

**Módszer**: Lineáris interpoláció

**Használat**:
```python
corrected_data, corrections = framework.auto_correct_data(data, "ohlcv")
```

**Példa**:
```python
{
    "original_value": null,
    "corrected_value": 1.1050,
    "correction_method": "interpolation",
    "reason": "Hiányzó open interpolációja",
    "confidence": 0.7
}
```

#### 2. High < Low javítása

**Módszer**: Értékek cseréje

**Példa**:
```python
{
    "original_value": 1.09,  # high
    "corrected_value": 1.11,  # low (swapped)
    "correction_method": "swap_high_low",
    "reason": "High < Low korrekció",
    "confidence": 0.9
}
```

#### 3. Ask < Bid javítása

**Módszer**: Értékek cseréje

**Példa**:
```python
{
    "original_value": 1.1000,  # ask
    "corrected_value": 1.1005,  # bid (swapped)
    "correction_method": "swap_bid_ask",
    "reason": "Ask < Bid korrekció",
    "confidence": 0.9
}
```

### Konfiguráció

```python
framework.config = {
    "auto_correction": {
        "enabled": True,
        "max_corrections_per_batch": 100
    }
}
```

---

## Minőségi metrikák

### Metrikák típusai

#### 1. Completeness (Komplettség)

**Képlet**:
```
Completeness = 100 - (Missing Values / Total Records * 100)
```

**Súly**: 30%

**Jelentés**: Az adatok hiányosságainak mértéke

#### 2. Accuracy (Pontosság)

**Képlet**:
```
Accuracy = 100 - (Critical Errors * 10)
```

**Súly**: 30%

**Jelentés**: A kritikus hibák hiányának mértéke

#### 3. Consistency (Konzisztencia)

**Képlet**:
```
Consistency = 100 - (Logical Errors * 5)
```

**Súly**: 20%

**Jelentés**: Az adatok logikai konzisztenciája

#### 4. Timeliness (Időbeliség)

**Képlet**:
```
Timeliness = 100 - (Time Issues * 2)
```

**Súly**: 20%

**Jelentés**: Az időbeli problémák hiánya

### Összesített pontszám

```
Overall Score = Completeness * 0.3 +
                Accuracy * 0.3 +
                Consistency * 0.2 +
                Timeliness * 0.2
```

### Minőségi szintek

| Pontszám | Minősítés  | Leírás                  |
| -------- | ---------- | ----------------------- |
| 95-100   | Excellent  | Kiváló adatminőség      |
| 85-94    | Good       | Jó adatminőség          |
| 75-84    | Acceptable | Elfogadható adatminőség |
| 60-74    | Poor       | Gyenge adatminőség      |
| 0-59     | Critical   | Kritikus adatminőség    |

---

## API végpontok

### 1. Minőségi metrikák lekérdezése

**Végpont**: `GET /api/v1/quality/metrics`

**Válasz**:
```json
{
    "status": "success",
    "metrics": {
        "completeness": 98.5,
        "accuracy": 95.0,
        "consistency": 92.0,
        "timeliness": 96.0,
        "overall_score": 95.4
    }
}
```

### 2. Összesített minőségi összefoglaló

**Végpont**: `GET /api/v1/quality/summary`

**Válasz**:
```json
{
    "period": "last_30_days",
    "average_score": 95.4,
    "min_score": 92.1,
    "max_score": 97.8,
    "trend": "improving",
    "total_issues": 15,
    "total_corrections": 8,
    "last_update": "2025-12-16T21:30:00Z"
}
```

### 3. Minőségjelentés generálása

**Végpont**: `POST /api/v1/quality/report`

**Kérés**:
```json
{
    "symbol": "EURUSD",
    "timeframe": "M1",
    "format": "json",
    "include_corrections": true
}
```

**Válasz**:
```json
{
    "status": "success",
    "message": "Quality report generated",
    "files": [
        "logs/quality_reports/quality_report_20251216_213000_EURUSD_M1.json"
    ],
    "output_path": "logs/quality_reports/quality_report_20251216_213000.json"
}
```

### 4. Kötegelt validálás

**Végpont**: `POST /api/v1/quality/validate-batch`

**Kérés**:
```json
{
    "data": [
        {
            "symbol": "EURUSD",
            "timeframe": 16385,
            "time": 1765841400,
            "open": 1.1050,
            "high": 1.1060,
            "low": 1.1040,
            "close": 1.1055,
            "volume": 1000
        }
    ],
    "data_type": "ohlcv",
    "auto_correct": true
}
```

**Válasz**:
```json
{
    "overall_status": "passed",
    "metrics": {
        "overall_score": 95.4
    },
    "issues": [],
    "corrections": []
}
```

### 5. Automatikus javítás

**Végpont**: `POST /api/v1/quality/auto-correct`

**Kérés**:
```json
{
    "data": [...],
    "data_type": "ohlcv"
}
```

**Válasz**:
```json
{
    "status": "success",
    "message": "Auto-corrected 3 issues",
    "corrected_data": [...],
    "corrections": [
        {
            "original_value": 1.09,
            "corrected_value": 1.11,
            "correction_method": "swap_high_low",
            "reason": "High < Low korrekció",
            "confidence": 0.9
        }
    ],
    "corrections_count": 3
}
```

### 6. Minőségtörténet lekérdezése

**Végpont**: `GET /api/v1/quality/history?symbol=EURUSD&timeframe=M1&limit=30`

**Válasz**:
```json
{
    "status": "success",
    "history": [
        {
            "timestamp": "2025-12-16T21:00:00Z",
            "symbol": "EURUSD",
            "timeframe": "M1",
            "metrics": {
                "overall_score": 95.4
            }
        }
    ],
    "total_entries": 30
}
```

### 7. Minőség nyomon követése

**Végpont**: `POST /api/v1/quality/track?symbol=EURUSD&timeframe=M1`

**Válasz**:
```json
{
    "status": "success",
    "message": "Quality tracking enabled for EURUSD M1"
}
```

---

## Használati példák

### 1. Alap validálás

```python
from neural_ai.collectors.mt5.data_validator import DataValidator

# Validátor létrehozása
validator = DataValidator(enable_quality_framework=True)

# Tick adat validálása
tick_data = {
    "symbol": "EURUSD",
    "bid": 1.1000,
    "ask": 1.1005,
    "time": 1765841400
}

result = validator.validate_tick(tick_data)
print(f"Valid: {result.is_valid}")
print(f"Quality Score: {result.quality_score}")
```

### 2. Komprehenzív validálás

```python
import pandas as pd
from neural_ai.collectors.mt5.implementations.data_quality_framework import (
    DataQualityFramework
)

# Framework létrehozása
framework = DataQualityFramework()

# Adatok betöltése
data = pd.read_parquet("data/warehouse/validated/EURUSD_M1.parquet")

# Komprehenzív validálás
result = framework.validate_comprehensive(data, data_type="ohlcv")

print(f"Overall Status: {result['overall_status']}")
print(f"Quality Score: {result['metrics']['overall_score']:.2f}")
print(f"Issues: {len(result['issues'])}")
```

### 3. Automatikus javítás

```python
# Adatok javítása
corrected_data, corrections = framework.auto_correct_data(data, "ohlcv")

print(f"Corrections made: {len(corrections)}")
for correction in corrections[:5]:
    print(f"- {correction.correction_method}: {correction.reason}")
```

### 4. Minőségjelentés generálása

```python
# Jelentés generálása JSON formátumban
framework.generate_quality_report(
    "logs/quality_report.json",
    format="json"
)

# Jelentés generálása CSV formátumban
framework.generate_quality_report(
    "logs/quality_report.csv",
    format="csv"
)
```

### 5. Kiugró értékek detektálása

```python
from neural_ai.collectors.mt5.implementations.data_quality_framework import (
    OutlierDetector
)

# Detektor létrehozása
detector = OutlierDetector()

# Adatok betöltése
close_prices = data["close"]

# Összes módszerrel történő detektálás
results = detector.detect_all_methods(close_prices)

for method, (outliers, stats) in results.items():
    print(f"{method}: {stats['outlier_count']} outliers detected")
```

### 6. Minőség trend nyomon követése

```python
# Validálás
result = framework.validate_comprehensive(data, "ohlcv")
metrics = QualityMetrics(**result['metrics'])

# Trend nyomon követése
framework.track_quality_trend("EURUSD", "M1", metrics)

# Összefoglaló lekérdezése
summary = framework.get_quality_summary()
print(f"Trend: {summary['trend']}")
print(f"Average Score: {summary['average_score']:.2f}")
```

---

## Konfiguráció

### DataValidator konfiguráció

```python
validator = DataValidator(
    logger=None,
    enable_quality_framework=True
)
```

### DataQualityFramework konfiguráció

```python
framework = DataQualityFramework()
framework.config = {
    "outlier_detection": {
        "iqr_threshold": 1.5,
        "z_score_threshold": 3.0,
        "ma_window": 20,
        "ma_threshold": 2.0
    },
    "quality_thresholds": {
        "excellent": 95.0,
        "good": 85.0,
        "acceptable": 75.0,
        "poor": 60.0
    },
    "auto_correction": {
        "enabled": True,
        "max_corrections_per_batch": 100
    }
}
```

---

## Tesztelés

### Tesztesetek futtatása

```bash
# Összes teszt futtatása
python -m pytest tests/test_data_quality_framework.py -v

# Konkrét tesztosztály
python -m pytest tests/test_data_quality_framework.py::TestDataQualityFramework -v

# Konkrét teszteset
python -m pytest tests/test_data_quality_framework.py::TestDataQualityFramework::test_validate_comprehensive_valid_data -v
```

### Tesztlefedettség

```bash
# Tesztlefedettség mérése
python -m pytest tests/test_data_quality_framework.py --cov=neural_ai.collectors.mt5 --cov-report=html
```

---

## Hibaelhárítás

### Gyakori problémák

#### 1. Data Quality Framework nincs engedélyezve

**Hiba**:
```
Data Quality Framework not enabled
```

**Megoldás**:
```python
validator = DataValidator(enable_quality_framework=True)
```

#### 2. Nincs elég adat a statisztikai validáláshoz

**Hiba**:
```
Insufficient data for statistical validation
```

**Megoldás**: Gyűjtsön több adatot (legalább 100 rekord)

#### 3. Import hiba

**Hiba**:
```
ModuleNotFoundError: No module named 'pandas'
```

**Megoldás**:
```bash
pip install pandas numpy
```

---

## Teljesítményoptimalizálás

### Tippek

1. **Kötegelt validálás**: Használja a `validate_batch` metódust nagy adatmennyiségekhez
2. **Párhuzamos feldolgozás**: Több szimbólum párhuzamos validálása
3. **Gyorsítótárazás**: Validációs eredmények gyorsítótárazása
4. **Időszakos validálás**: Ne validálja folyamatosan ugyanazokat az adatokat

---

## Fejlesztői információk

### Fájlok

- **Fő implementáció**: [`data_quality_framework.py`](../neural_ai/collectors/mt5/implementations/data_quality_framework.py)
- **Validátor integráció**: [`data_validator.py`](../neural_ai/collectors/mt5/data_validator.py)
- **API végpontok**: [`mt5_collector.py`](../neural_ai/collectors/mt5/implementations/mt5_collector.py)
- **Tesztek**: [`test_data_quality_framework.py`](../../../tests/test_data_quality_framework.py)

### Függőségek

- pandas >= 2.0.0
- numpy >= 1.24.0
- fastparquet >= 2023.4.0

---

## Verziótörténet

### v1.0.0 (2025-12-16)

- Kezdeti kiadás
- 3-szintű validációs rendszer
- Kiugró érték detektálás (IQR, Z-Score, Moving Average)
- Automatikus javítási képességek
- Minőségjelentések generálása
- API végpontok
- Komprehenzív tesztelés

---

## Kapcsolódó dokumentáció

- [MT5 Collector API](../mt5/api.md)
- [Historical Data Collection](HISTORICAL_DATA_COLLECTION.md)
- [Data Collection Strategy](../../../plans/data_collection_strategy_overhaul.md)

---

**Author**: Neural AI Next Team
**Date**: 2025-12-16
**Version**: 1.0.0
