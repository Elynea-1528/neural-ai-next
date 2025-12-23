# 05 - Adatgyűjtők Stratégiája (Collectors Strategy)

## 🎯 Cél és Szándék

Ez a dokumentum definiálja a **Neural AI Next** adatgyűjtő rendszerét, amely natív .bi5 fájlok dekódolását, MT5 integrációt és kritikusan fontos Java-Python Bridge-et valósít meg a JForex kereskedéshez. A Dukascopy egy megbízható svájci bank, ezért a kereskedésnek itt is mennie kell!

**Filozófia:** *"Native protocols, real-time execution, zero compromise"*

---

## 🏗️ Architektúra Áttekintés

### Collector Típusok

```
┌─────────────────────────────────────────┐
│         COLLECTOR ARCHITECTURE          │
├─────────────────────────────────────────┤
│                                         │
│  ┌──────────────────────────────┐      │
│  │   JFOREX COLLECTOR           │      │
│  │   - Bi5 Downloader (LZMA)    │      │
│  │   - Java Bridge (Trading)    │      │
│  └──────────────┬───────────────┘      │
│                 │                       │
│  ┌──────────────▼───────────────┐      │
│  │   MT5 COLLECTOR              │      │
│  │   - FastAPI Server           │      │
│  │   - WebSocket Events         │      │
│  └──────────────┬───────────────┘      │
│                 │                       │
│  ┌──────────────▼───────────────┐      │
│  │   IBKR COLLECTOR (Future)    │      │
│  │   - TWS API                  │      │
│  └──────────────┬───────────────┘      │
│                 │                       │
│                 ▼                       │
│  ┌──────────────────────────────┐      │
│  │   EVENT BUS                  │      │
│  └──────────────────────────────┘      │
│                                         │
└─────────────────────────────────────────┘
```

---

## 📦 1. JForex Bi5 Downloader

### Technológia

- **Formátum:** Natív .bi5 (LZMA tömörített bináris)
- **Dekódolás:** `lzma` + `struct` modulok
- **Forrás:** Dukascopy Tick Data Suite

### Implementáció

```python
import lzma
import struct
import asyncio
import aiohttp
from datetime import datetime, timedelta
from typing import List

class Bi5Downloader:
    """JForex natív Bi5 adatletöltő és dekódoló."""
    
    BASE_URL = "https://www.dukascopy.com/datafeed"
    
    def __init__(self, symbols: List[str]):
        self.symbols = symbols
    
    async def download_tick_data(
        self,
        symbol: str,
        date: datetime
    ) -> List[TickData]:
        """Tick adatok letöltése egy adott napra."""
        
        # URL összeállítása
        url = self._build_url(symbol, date)
        
        logger.info(
            "bi5_download_started",
            symbol=symbol,
            date=date.isoformat(),
            url=url
        )
        
        try:
            # Bináris adatok letöltése
            content = await self._download_binary(url)
            
            # LZMA dekompresszió
            decompressed = lzma.decompress(content)
            
            # Struct unpacking
            ticks = self._unpack_bi5_data(decompressed, symbol, date)
            
            logger.info(
                "bi5_download_completed",
                symbol=symbol,
                date=date.isoformat(),
                ticks=len(ticks)
            )
            
            return ticks
            
        except Exception as e:
            logger.error(
                "bi5_download_failed",
                symbol=symbol,
                date=date.isoformat(),
                error=str(e)
            )
            raise
    
    def _build_url(self, symbol: str, date: datetime) -> str:
        """URL összeállítása."""
        return (
            f"{self.BASE_URL}/{symbol.upper()}/"
            f"{date.year}/{date.month-1:02d}/{date.day:02d}/"
            "00h_ticks.bi5"
        )
    
    async def _download_binary(self, url: str) -> bytes:
        """Bináris adatok letöltése."""
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.read()
    
    def _unpack_bi5_data(
        self,
        data: bytes,
        symbol: str,
        date: datetime
    ) -> List[TickData]:
        """Bi5 bináris adatok dekódolása."""
        ticks = []
        
        # Bi5 formátum: [timestamp_delta, ask, bid]
        # Minden rekord 12 bájt
        record_size = 12
        num_records = len(data) // record_size
        
        base_timestamp = int(date.timestamp()) * 1000
        
        for i in range(num_records):
            offset = i * record_size
            record = data[offset:offset + record_size]
            
            # Big-endian unpack
            timestamp_delta, ask, bid = struct.unpack('>Iff', record)
            
            # Timestamp számítása
            timestamp_ms = base_timestamp + timestamp_delta
            timestamp = datetime.fromtimestamp(timestamp_ms / 1000)
            
            tick = TickData(
                timestamp=timestamp,
                symbol=symbol,
                bid=bid,
                ask=ask,
                source="jforex"
            )
            
            ticks.append(tick)
        
        return ticks
```

**Függőségek:** `aiohttp`, `lzma`, `struct`

---

## 🔗 2. JForex Java-Python Bridge (KRITIKUS)

### Cél

A JForex platformon keresztül történő kereskedés megvalósítása. Mivel a Dukascopy egy megbízható svájci bank, a kereskedésnek itt is működnie kell!

### Architektúra

```
┌─────────────────┐
│   PYTHON SIDE   │
│   (Client)      │
│   - Strategy    │
│   - Signals     │
└────────┬────────┘
         │ WebSocket / ZeroMQ
         │ JSON Messages
         ▼
┌─────────────────┐
│   JAVA SIDE     │
│   (Slave)       │
│   - JForex API  │
│   - Execution   │
└─────────────────┘
```

### Java Oldal (Slave Stratégia)

```java
// JForexSlaveStrategy.java
package com.neuralai.jforex;

import com.dukascopy.api.*;
import com.dukascopy.api.IEngine.OrderCommand;
import org.java_websocket.WebSocket;
import org.java_websocket.handshake.ClientHandshake;
import org.java_websocket.server.WebSocketServer;

import java.net.InetSocketAddress;
import java.util.concurrent.ConcurrentHashMap;

public class JForexSlaveStrategy extends WebSocketServer implements IStrategy {
    
    private IEngine engine;
    private IConsole console;
    private ConcurrentHashMap<String, WebSocket> clients = new ConcurrentHashMap<>();
    
    public JForexSlaveStrategy(InetSocketAddress address) {
        super(address);
    }
    
    @Override
    public void onStart(IContext context) throws JFException {
        this.engine = context.getEngine();
        this.console = context.getConsole();
        
        console.getOut().println("JForex Slave Strategy started");
        start(); // WebSocket server start
    }
    
    @Override
    public void onMessage(WebSocket conn, String message) {
        // Üzenet feldolgozása Python oldalról
        try {
            JSONObject msg = new JSONObject(message);
            String action = msg.getString("action");
            
            switch (action) {
                case "OPEN":
                    executeOpenOrder(msg);
                    break;
                case "CLOSE":
                    executeCloseOrder(msg);
                    break;
                case "MODIFY":
                    executeModifyOrder(msg);
                    break;
                case "HOLD":
                    // Várakozás
                    break;
                default:
                    conn.send("{\"error\": \"Unknown action\"}");
            }
        } catch (Exception e) {
            conn.send("{\"error\": \"" + e.getMessage() + "\"}");
        }
    }
    
    private void executeOpenOrder(JSONObject msg) throws JFException {
        String symbol = msg.getString("symbol");
        String direction = msg.getString("direction");
        double volume = msg.getDouble("volume");
        
        OrderCommand command = direction.equals("BUY") 
            ? OrderCommand.BUY 
            : OrderCommand.SELL;
        
        IOrder order = engine.submitOrder(
            "order_" + System.currentTimeMillis(),
            symbol,
            command,
            volume
        );
        
        // Visszajelzés küldése
        JSONObject response = new JSONObject();
        response.put("status", "OPENED");
        response.put("order_id", order.getLabel());
        response.put("price", order.getOpenPrice());
        
        broadcast(response.toString());
    }
    
    private void executeCloseOrder(JSONObject msg) throws JFException {
        String orderId = msg.getString("order_id");
        IOrder order = engine.getOrder(orderId);
        
        if (order != null && order.getState() == IOrder.State.FILLED) {
            order.close();
            
            JSONObject response = new JSONObject();
            response.put("status", "CLOSED");
            response.put("order_id", orderId);
            response.put("profit", order.getProfitLossInUSD());
            
            broadcast(response.toString());
        }
    }
    
    private void executeModifyOrder(JSONObject msg) throws JFException {
        String orderId = msg.getString("order_id");
        Double stopLoss = msg.optDouble("stop_loss");
        Double takeProfit = msg.optDouble("take_profit");
        
        IOrder order = engine.getOrder(orderId);
        
        if (order != null) {
            if (stopLoss != null) {
                order.setStopLossPrice(stopLoss);
            }
            if (takeProfit != null) {
                order.setTakeProfitPrice(takeProfit);
            }
            
            JSONObject response = new JSONObject();
            response.put("status", "MODIFIED");
            response.put("order_id", orderId);
            
            broadcast(response.toString());
        }
    }
    
    @Override
    public void onTick(Instrument instrument, ITick tick) {
        // Tick adatok küldése Python oldalnak (opcionális)
        JSONObject tickData = new JSONObject();
        tickData.put("type", "TICK");
        tickData.put("symbol", instrument.toString());
        tickData.put("bid", tick.getBid());
        tickData.put("ask", tick.getAsk());
        tickData.put("timestamp", tick.getTime());
        
        broadcast(tickData.toString());
    }
    
    @Override
    public void onBar(Instrument instrument, Period period, IBar askBar, IBar bidBar) {
        // Nem szükséges
    }
    
    @Override
    public void onMessage(IMessage message) {
        // JForex üzenetek kezelése
    }
    
    @Override
    public void onStop() {
        try {
            stop(); // WebSocket server leállítása
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    
    private void broadcast(String message) {
        for (WebSocket conn : clients.values()) {
            conn.send(message);
        }
    }
}
```

### Python Oldal (JForexExecutionService)

```python
import asyncio
import websockets
import json
from typing import Dict, Any, Optional

class JForexExecutionService:
    """JForex kereskedési szolgáltatás."""
    
    def __init__(self, ws_url: str = "ws://localhost:8765"):
        self.ws_url = ws_url
        self.ws: Optional[websockets.WebSocketClientProtocol] = None
    
    async def connect(self) -> None:
        """Kapcsolódás a Java WebSocket szerverhez."""
        try:
            self.ws = await websockets.connect(self.ws_url)
            logger.info("jforex_ws_connected", url=self.ws_url)
        except Exception as e:
            logger.error("jforex_ws_connection_failed", error=str(e))
            raise
    
    async def disconnect(self) -> None:
        """Kapcsolat bontása."""
        if self.ws:
            await self.ws.close()
            logger.info("jforex_ws_disconnected")
    
    async def open_position(
        self,
        symbol: str,
        direction: str,  # 'BUY' or 'SELL'
        volume: float
    ) -> Dict[str, Any]:
        """Pozíció nyitása."""
        message = {
            "action": "OPEN",
            "symbol": symbol,
            "direction": direction,
            "volume": volume,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        await self.ws.send(json.dumps(message))
        
        # Válasz fogadása
        response = await self.ws.recv()
        result = json.loads(response)
        
        if result.get("status") == "OPENED":
            logger.info(
                "position_opened",
                symbol=symbol,
                direction=direction,
                volume=volume,
                order_id=result["order_id"],
                price=result["price"]
            )
        
        return result
    
    async def close_position(self, order_id: str) -> Dict[str, Any]:
        """Pozíció lezárása."""
        message = {
            "action": "CLOSE",
            "order_id": order_id,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        await self.ws.send(json.dumps(message))
        
        response = await self.ws.recv()
        result = json.loads(response)
        
        if result.get("status") == "CLOSED":
            logger.info(
                "position_closed",
                order_id=order_id,
                profit=result.get("profit")
            )
        
        return result
    
    async def modify_position(
        self,
        order_id: str,
        stop_loss: Optional[float] = None,
        take_profit: Optional[float] = None
    ) -> Dict[str, Any]:
        """Pozíció módosítása."""
        message = {
            "action": "MODIFY",
            "order_id": order_id,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        if stop_loss is not None:
            message["stop_loss"] = stop_loss
        if take_profit is not None:
            message["take_profit"] = take_profit
        
        await self.ws.send(json.dumps(message))
        
        response = await self.ws.recv()
        result = json.loads(response)
        
        if result.get("status") == "MODIFIED":
            logger.info(
                "position_modified",
                order_id=order_id,
                stop_loss=stop_loss,
                take_profit=take_profit
            )
        
        return result
    
    async def hold(self) -> None:
        """Várakozás (HOLD parancs)."""
        message = {
            "action": "HOLD",
            "timestamp": datetime.utcnow().isoformat()
        }
        
        await self.ws.send(json.dumps(message))
```

**Függőségek (Java):** `JForex API`, `Java-WebSocket`
**Függőségek (Python):** `websockets`, `asyncio`

---

## 🖥️ 3. MT5 FastAPI Server

### Cél

MT5 Expert Advisorokból érkező Tick és Trade események fogadása.

### Implementáció

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from typing import List, Dict
import asyncio

app = FastAPI(title="Neural AI Next - MT5 Collector")

class TickEvent(BaseModel):
    """Tick esemény modell."""
    symbol: str
    timestamp: datetime
    bid: float
    ask: float
    volume: Optional[int] = None

class TradeEvent(BaseModel):
    """Trade esemény modell."""
    symbol: str
    timestamp: datetime
    direction: str  # 'BUY' or 'SELL'
    price: float
    volume: float
    order_id: str

# WebSocket kapcsolatok kezelése
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info("mt5_ws_connected", client=websocket.client)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        logger.info("mt5_ws_disconnected", client=websocket.client)
    
    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()

@app.websocket("/api/v1/tick")
async def tick_endpoint(websocket: WebSocket):
    """Tick adatok fogadása."""
    await manager.connect(websocket)
    
    try:
        while True:
            data = await websocket.receive_json()
            event = TickEvent(**data)
            
            # EventBus-ra küldés
            await event_bus.publish("market_data", event)
            
            logger.debug(
                "tick_received",
                symbol=event.symbol,
                bid=event.bid,
                ask=event.ask
            )
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.websocket("/api/v1/trade")
async def trade_endpoint(websocket: WebSocket):
    """Trade események fogadása."""
    await manager.connect(websocket)
    
    try:
        while True:
            data = await websocket.receive_json()
            event = TradeEvent(**data)
            
            # EventBus-ra küldés
            await event_bus.publish("trade", event)
            
            logger.info(
                "trade_received",
                symbol=event.symbol,
                direction=event.direction,
                price=event.price,
                volume=event.volume
            )
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "active_connections": len(manager.active_connections)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**Függőségek:** `fastapi`, `uvicorn`, `websockets`

---

## 🔄 4. IBKR Collector (Jövőbeli)

### Tervezés

```python
from ib_insync import IB, Stock, Forex

class IBKRCollector:
    """Interactive Brokers TWS API collector."""
    
    def __init__(self):
        self.ib = IB()
    
    async def connect(self, host: str = '127.0.0.1', port: int = 7497):
        """Kapcsolódás a TWS-hez."""
        await self.ib.connectAsync(host, port, clientId=1)
        logger.info("ibkr_connected", host=host, port=port)
    
    async def subscribe_to_ticks(self, symbol: str):
        """Tick adatokra való feliratkozás."""
        contract = Forex(symbol)
        self.ib.reqMktData(contract, '', False, False)
        
        # Tick események kezelése
        @self.ib.tickEvent
        def on_tick(ticker):
            event = TickData(
                timestamp=datetime.utcnow(),
                symbol=symbol,
                bid=ticker.bid,
                ask=ticker.ask,
                source="ibkr"
            )
            asyncio.create_task(event_bus.publish("market_data", event))
```

**Függőség:** `ib_insync`

---

## 📋 Következő Lépések

1. **System Bootstrap:** Lásd [`main.py`](main.py) és [`.env.example`](.env.example)
2. **Master README:** Lásd [`README.md`](README.md)

---

## 🔗 Kapcsolódó Dokumentumok

- [Rendszerarchitektúra](01_system_architecture.md)
- [Dinamikus Konfiguráció](02_dynamic_configuration.md)
- [Adattárház](04_data_warehouse.md)
- [Fejlesztési Útmutató](docs/development/unified_development_guide.md)