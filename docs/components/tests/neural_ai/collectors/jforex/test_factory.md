# tests/neural_ai/collectors/jforex/test_factory.py

JForexFactory tesztek.

## Importok

```python
from unittest.mock import ANY
from unittest.mock import MagicMock
from unittest.mock import patch
from neural_ai.collectors.jforex.factory import JForexFactory
```

## Osztály: `TestJForexFactory`

JForexFactory tesztek.

### Metódusok

#### `test_create_downloader_valid_config()`

```python
def test_create_downloader_valid_config(self, mock_session: MagicMock, mock_downloader: MagicMock) -> None
```

Teszteli a downloader létrehozását érvényes konfiggal.

**Paraméterek:**

- **`self`**
- **`mock_session`** (`MagicMock`)
- **`mock_downloader`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_create_downloader_invalid_config()`

```python
def test_create_downloader_invalid_config(self, mock_session: MagicMock, mock_downloader: MagicMock) -> None
```

Teszteli a downloader létrehozását érvénytelen konfiggal (defaults).

**Paraméterek:**

- **`self`**
- **`mock_session`** (`MagicMock`)
- **`mock_downloader`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_create_live_feed_valid_config()`

```python
def test_create_live_feed_valid_config(self, mock_live_feed: MagicMock) -> None
```

Teszteli a live feed létrehozását érvényes konfiggal.

**Paraméterek:**

- **`self`**
- **`mock_live_feed`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_create_live_feed_invalid_port()`

```python
def test_create_live_feed_invalid_port(self, mock_live_feed: MagicMock) -> None
```

Teszteli a live feed létrehozását érvénytelen porttal.

**Paraméterek:**

- **`self`**
- **`mock_live_feed`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_create_live_feed_disabled_config()`

```python
def test_create_live_feed_disabled_config(self, mock_live_feed: MagicMock) -> None
```

Teszteli a live feed létrehozását disabled konfiggal.

**Paraméterek:**

- **`self`**
- **`mock_live_feed`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_create_live_feed_missing_config()`

```python
def test_create_live_feed_missing_config(self, mock_live_feed: MagicMock) -> None
```

Teszteli a live feed létrehozását hiányzó konfiggal.

**Paraméterek:**

- **`self`**
- **`mock_live_feed`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_create_downloader_none_config()`

```python
def test_create_downloader_none_config(self, mock_session: MagicMock, mock_downloader: MagicMock) -> None
```

Teszteli a downloader létrehozását None konfiggal.

**Paraméterek:**

- **`self`**
- **`mock_session`** (`MagicMock`)
- **`mock_downloader`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_create_live_feed_empty_host()`

```python
def test_create_live_feed_empty_host(self, mock_live_feed: MagicMock) -> None
```

Teszteli a live feed létrehozását üres host stringgel.

**Paraméterek:**

- **`self`**
- **`mock_live_feed`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_create_downloader_returns_correct_interface()`

```python
def test_create_downloader_returns_correct_interface(self, mock_session: MagicMock, mock_downloader: MagicMock) -> None
```

Teszteli, hogy a downloader a helyes interface-t implementálja.

**Paraméterek:**

- **`self`**
- **`mock_session`** (`MagicMock`)
- **`mock_downloader`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

#### `test_create_live_feed_returns_correct_interface()`

```python
def test_create_live_feed_returns_correct_interface(self, mock_live_feed: MagicMock) -> None
```

Teszteli, hogy a live feed a helyes interface-t implementálja.

**Paraméterek:**

- **`self`**
- **`mock_live_feed`** (`MagicMock`)

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/neural_ai/collectors/jforex/test_factory.py`](../../tests/neural_ai/collectors/jforex/test_factory.py)
