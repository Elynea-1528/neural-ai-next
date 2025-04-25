//+------------------------------------------------------------------+
//|                                              NeuralAICollector.mq5 |
//|                                  Copyright 2025, Neural-AI Project |
//|                                                neural-ai-next.org |
//+------------------------------------------------------------------+
#property copyright "Copyright 2025, Neural-AI Project"
#property link      "neural-ai-next.org"
#property version   "1.00"
#property strict

// WebSocket könyvtárak
#include <WebSocket/WebSocketServer.mqh>
#include <WebSocket/WebSocketClient.mqh>
#include <WebSocket/SocketMessages.mqh>

// JSON kezelés
#include <JAson.mqh>

// Konstansok
#define WS_PORT 8765
#define MAX_CLIENTS 10
#define TICK_BUFFER_SIZE 1000
#define HEARTBEAT_INTERVAL 30  // másodperc

// Globális változók
CWebSocketServer* Server = NULL;
CJAson* JsonParser = NULL;
bool isConnected = false;
string authToken = "";
datetime lastHeartbeat;

//+------------------------------------------------------------------+
//| Expert initialization function                                     |
//+------------------------------------------------------------------+
int OnInit() {
   // WebSocket szerver inicializálása
   Server = new CWebSocketServer();
   if (!Server.Start(WS_PORT, MAX_CLIENTS)) {
      Print("Hiba a WebSocket szerver indításakor: ", GetLastError());
      return INIT_FAILED;
   }

   // JSON parser inicializálása
   JsonParser = new CJAson();

   // Kezdeti időbélyeg
   lastHeartbeat = TimeLocal();

   Print("NeuralAI Collector elindult - Port: ", WS_PORT);
   return INIT_SUCCEEDED;
}

//+------------------------------------------------------------------+
//| Expert deinitialization function                                  |
//+------------------------------------------------------------------+
void OnDeinit(const int reason) {
   // Szerver leállítása
   if (Server != NULL) {
      Server.Stop();
      delete Server;
   }

   // JSON parser felszabadítása
   if (JsonParser != NULL) {
      delete JsonParser;
   }

   Print("NeuralAI Collector leállítva");
}

//+------------------------------------------------------------------+
//| Expert tick function                                              |
//+------------------------------------------------------------------+
void OnTick() {
   // Kapcsolat ellenőrzése
   if (!isConnected) return;

   // Heartbeat küldése
   if (TimeLocal() - lastHeartbeat >= HEARTBEAT_INTERVAL) {
      SendHeartbeat();
      lastHeartbeat = TimeLocal();
   }

   // Market data küldése
   SendMarketData();
}

//+------------------------------------------------------------------+
//| Szerver üzenet kezelése                                           |
//+------------------------------------------------------------------+
void OnWebSocketMessage(const string& message) {
   // JSON üzenet feldolgozása
   JsonParser.Clear();
   if (!JsonParser.Parse(message)) {
      Print("Hibás JSON üzenet: ", message);
      return;
   }

   // Üzenet típus ellenőrzése
   string msgType = JsonParser.GetString("type");

   if (msgType == "auth") {
      HandleAuth();
   }
   else if (msgType == "subscribe") {
      HandleSubscribe();
   }
   else if (msgType == "unsubscribe") {
      HandleUnsubscribe();
   }
}

//+------------------------------------------------------------------+
//| Authentikáció kezelése                                            |
//+------------------------------------------------------------------+
void HandleAuth() {
   string token = JsonParser.GetString("token");
   if (ValidateToken(token)) {
      authToken = token;
      isConnected = true;
      SendResponse("auth", "success");
   }
   else {
      SendResponse("auth", "failed");
   }
}

//+------------------------------------------------------------------+
//| Market data küldése                                               |
//+------------------------------------------------------------------+
void SendMarketData() {
   MqlTick lastTick;
   if (!SymbolInfoTick(_Symbol, lastTick)) return;

   // JSON üzenet összeállítása
   string json = StringFormat(
      "{\"type\":\"tick\",\"symbol\":\"%s\",\"data\":{\"bid\":%f,\"ask\":%f,\"last\":%f,\"volume\":%d,\"time\":%d}}",
      _Symbol,
      lastTick.bid,
      lastTick.ask,
      lastTick.last,
      lastTick.volume,
      lastTick.time
   );

   // Üzenet küldése
   Server.SendToAll(json);
}

//+------------------------------------------------------------------+
//| Heartbeat üzenet küldése                                          |
//+------------------------------------------------------------------+
void SendHeartbeat() {
   SendMessage("heartbeat", "");
}

//+------------------------------------------------------------------+
//| Válasz üzenet küldése                                             |
//+------------------------------------------------------------------+
void SendResponse(const string& type, const string& status) {
   string json = StringFormat(
      "{\"type\":\"%s\",\"status\":\"%s\",\"timestamp\":%d}",
      type,
      status,
      TimeLocal()
   );
   Server.SendToAll(json);
}

//+------------------------------------------------------------------+
//| Token validálás                                                    |
//+------------------------------------------------------------------+
bool ValidateToken(const string& token) {
   // TODO: Implementálni a token validációt
   return true;
}
