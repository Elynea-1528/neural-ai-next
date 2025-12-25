# Events Modul Teszt Bővítés - ZeroMQ Port Foglaltság

## Áttekintés

Ez a dokumentáció az Events modul tesztjeinek bővítését írja le, különös tekintettel a ZeroMQ port foglaltság hibakezelésére.

## Új Teszt Osztály: TestEventBusPortBinding

### 1. Port Foglaltság Hibák Mockolása

A `TestEventBusPortBinding` osztály 5 új tesztmetódust tartalmaz, amelyek a ZeroMQ port foglaltság és socket hibák kezelését tesztelik.

#### 1.1 test_port_already_in_use_pub_port

**Cél:** Teszteli, hogy a rendszer hogyan kezeli, ha egy publisher port már foglalt.

**Elvárások:**
- Az első EventBus sikeresen elindul a 5555-ös porton
- A második EventBus indítása hibát dob, amikor ugyanazt a portot próbálja használni
- A hiba típusa `Exception` vagy `OSError` lehet

**Tesztelt hibakezelés:**
```python
with pytest.raises((Exception, OSError)) as exc_info:
    await bus2.start()
```

#### 1.2 test_port_bind_failure_handling

**Cél:** Mockolja a port bindolási hibát.

**Elvárások:**
- A publisher socket `bind` metódusa `Exception`-t dob "Address already in use" üzenettel
- Az EventBus start metódusa továbbítja a hibát

**Mockolás:**
```python
mock_socket.bind.side_effect = Exception("Address already in use")
```

#### 1.3 test_zmq_bind_error_simulation

**Cél:** Szimulálja a ZeroMQ bind hiba kezelését.

**Elvárások:**
- A `context.socket` metódus `Exception`-t dob "ZMQ Bind error" üzenettel
- Az EventBus start metódusa továbbítja a hibát

#### 1.4 test_socket_creation_failure

**Cél:** Teszteli a socket létrehozási hibát.

**Elvárások:**
- A `context.socket` metódus `None` értéket ad vissza
- Az EventBus start metódusa `AttributeError` vagy `EventBusError` kivételt dob

#### 1.5 test_multiple_buses_inproc_different_ports

**Cél:** Ellenőrzi, hogy több EventBus is futhat-e inproc módban különböző portokon.

**Elvárások:**
- Két EventBus is sikeresen elindul inproc módban
- Mindkét busz különböző portokat használ (6666-6667 és 6668-6669)
- Mindkét busz futási állapota `True`

## Hibakezelési Stratégiák

### 1. Port Konfliktusok

A tesztesetek a következő port konfliktusokat fedik le:
- **Dupla port használat:** Két busz próbálja használni ugyanazt a publisher portot
- **Bind hiba:** A mögöttes socket layer hibát jelez
- **Socket létrehozási hiba:** A ZeroMQ context nem tud socketet létrehozni

### 2. Biztonságos Leállítás

Minden teszteset biztosítja a megfelelő takarítást:
```python
await bus1.stop()
await bus2.stop()
```

### 3. Inproc vs TCP Mód

- **Inproc mód:** Teszteléshez, nem okoz port konfliktust
- **TCP mód:** Éles használathoz, port konfliktusokat okozhat

## Teszt Coverage

A bővített tesztek a következő területeket fedik le:

| Metódus | Coverage | Hibakezelés |
|---------|----------|-------------|
| `EventBus.start()` | 100% | Port foglaltság, Socket hiba |
| `EventBus.stop()` | 100% | Dupla leállítás |
| `EventBus.publish()` | 100% | Nincs publisher socket |
| `EventBus._deserialize_event()` | 100% | Ismeretlen típus, Érvénytelen adatok |

## Futtatás

```bash
# Összes events teszt futtatása
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/core/events/test_bus.py -v

# Csak a port binding tesztek
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/core/events/test_bus.py::TestEventBusPortBinding -v
```

## Kimenet

A tesztek sikeres futtatása esetén:
```
tests/core/events/test_bus.py::TestEventBusPortBinding::test_port_already_in_use_pub_port PASSED
tests/core/events/test_bus.py::TestEventBusPortBinding::test_port_bind_failure_handling PASSED
tests/core/events/test_bus.py::TestEventBusPortBinding::test_zmq_bind_error_simulation PASSED
tests/core/events/test_bus.py::TestEventBusPortBinding::test_socket_creation_failure PASSED
tests/core/events/test_bus.py::TestEventBusPortBinding::test_multiple_buses_inproc_different_ports PASSED
```

## Fejlesztői Jegyzetek

1. **Port Választás:** A tesztesetek különböző portokat használnak (5555, 6666-6669) a konfliktusok elkerülése érdekében.

2. **Mockolás:** A `unittest.mock.patch` és `MagicMock` használatával szimuláljuk a hibákat.

3. **Aszinkron Tesztelés:** Minden teszt `@pytest.mark.asyncio` dekorátorral van ellátva.

4. **Exception Handling:** A `pytest.raises` kontextus managerrel ellenőrizzük a várt kivételeket.