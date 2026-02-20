# neural_ai/data/ingestion/__init__.py

Ingestion komponensek.

Ez a modul a rendszer adatbetöltési (ingestion) komponenseit tartalmazza,
beleértve a MarketDataPersister-t, amely felelős a bejövő market data
eventek bufferezéséért és időzített mentéséért a Parquet tárolóba.

Author: Neural AI Next Team
Version: 1.0.0

## Importok

```python
from neural_ai.data.ingestion.market_data_persister import MarketDataPersister
```

## Konstansok

- **`__all__`**
: `['MarketDataPersister']`


---

**Forrásfájl:** [`neural_ai/data/ingestion/__init__.py`](../../neural_ai/data/ingestion/__init__.py)
