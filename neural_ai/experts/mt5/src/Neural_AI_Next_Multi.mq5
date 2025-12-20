//+------------------------------------------------------------------+
//|                                           Neural_AI_Next_Multi.mq5 |
//|                                  Copyright 2025, MetaQuotes Ltd. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2025, MetaQuotes Ltd."
#property link "https://www.mql5.com"
#property version "1.00"
#property description "Multi-instrument, multi-timeframe data collector for Neural AI Next"

// Input parameters
input string FastAPI_Server = "http://localhost:8000"; // FastAPI server address
input int Update_Interval = 60;                        // Update interval in seconds
input bool Enable_HTTP_Logs = true;                    // Enable HTTP request logging

// Kikapcsolható adatküldési opciók
input bool Enable_Tick_Sending = true;       // Engedélyezi a tick küldést
input bool Enable_OHLC_Sending = true;       // Engedélyezi az OHLC küldést
input bool Enable_Historical_Sending = true; // Engedélyezi a historikus adat küldést

// Multi-instrument and multi-timeframe configuration
input string Instruments = "EURUSD,GBPUSD,USDJPY,XAUUSD"; // Comma-separated symbols
input string Timeframes = "M1,M5,M15,H1,H4,D1";           // Comma-separated timeframes

// Történelmi adatgyűjtés beállítások
input bool Enable_Historical_Collection = true; // Történelmi adatgyűjtés engedélyezése
input int Historical_Batch_Size = 99000;        // Historikus batch méret (MT5 limit: 100,000)
input int Historical_Request_Timeout = 300;     // Timeout másodpercben
input bool Log_Historical_Requests = true;      // Történelmi kérések naplózása

// Gyors historikus ellenőrzés beállítások
input int Historical_Check_Interval_Seconds = 1; // Historikus ellenőrzés gyakorisága (másodperc)
input bool Check_Historical_On_Tick = true;      // Historikus ellenőrzés minden Tick-en

// Global variables
bool isConnected = false;
string symbolArray[];
int timeframeArray[];
int totalInstruments;
int totalTimeframes;

// Történelmi adatgyűjtés
bool historicalJobActive = false;
string currentJobId = "";
datetime currentJobStartTime;
int currentBatchNumber = 0;
int totalBatches = 0;

// Gyors historikus ellenőrzés
datetime LastHistoricalCheckTime = 0; // Utolsó historikus ellenőrzés ideje

// Történelmi kérés követés
struct HistoricalRequest
{
    string job_id;
    string symbol;
    int timeframe;
    datetime start_date;
    datetime end_date;
    int batch_size;
    string status; // "pending", "in_progress", "completed", "failed"
};

HistoricalRequest activeRequest;

//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
{
    //--- Instrumentumok feldolgozása
    ParseInstruments();

    //--- Időkeretek feldolgozása
    ParseTimeframes();

    //--- Részletes inicializációs logolás
    Print("=== EXPERT INITIALIZATION ===");
    Print("FastAPI Server: ", FastAPI_Server);
    Print("Update Interval: ", Update_Interval, " seconds");
    Print("Enable Tick Sending: ", Enable_Tick_Sending ? "YES" : "NO");
    Print("Enable OHLC Sending: ", Enable_OHLC_Sending ? "YES" : "NO");
    Print("Enable Historical Sending: ", Enable_Historical_Sending ? "YES" : "NO");
    Print("Enable Historical Collection: ", Enable_Historical_Collection ? "YES" : "NO");
    Print("Log Historical Requests: ", Log_Historical_Requests ? "YES" : "NO");

    //--- időzítő létrehozása (1 másodperc a historikus ellenőrzéshez)
    EventSetMillisecondTimer(1000);
    Print("=== TIMER SET ===");
    Print("Timer interval: 1 SECOND (1000 ms)");
    Print("Historical Check Interval: ", Historical_Check_Interval_Seconds, " seconds");
    Print("Check Historical On Tick: ", Check_Historical_On_Tick ? "YES" : "NO");

    //--- Kapcsolat tesztelése FastAPI szerverrel
    if (TestConnection())
    {
        isConnected = true;
        Print("✓ Csatlakozva a FastAPI szerverhez: ", FastAPI_Server);
        Print("✓ Figyelés ", totalInstruments, " instrumentum");
        Print("✓ Figyelés ", totalTimeframes, " időkeret");

        if (Enable_Historical_Collection)
        {
            Print("✓ Történelmi adatgyűjtés: ENGEDÉLYEZVE");
            Print("✓ Batch méret: ", Historical_Batch_Size, " gyertya");
        }
        else
        {
            Print("⚠ Történelmi adatgyűjtés: LETILTVA");
        }
    }
    else
    {
        Print("⚠ Figyelmeztetés: Nem sikerült csatlakozni a FastAPI szerverhez");
        Print("  Szerver: ", FastAPI_Server);
        Print("  Az EA folytatja de az adatgyűjtés sikertelen lehet");
    }

    Print("=== INITIALIZATION COMPLETE ===");

    //---
    return (INIT_SUCCEEDED);
}
//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
{
    //--- destroy timer
    EventKillTimer();
}
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
{
    //--- Collect and send tick data for all instruments
    if (Enable_Tick_Sending)
    {
        CollectAndSendTickData();
    }

    //--- Historikus ellenőrzés minden Tick-en (ha engedélyezve van)
    if (Check_Historical_On_Tick && Enable_Historical_Collection && Enable_Historical_Sending)
    {
        datetime current_time = TimeCurrent();
        if (current_time - LastHistoricalCheckTime >= Historical_Check_Interval_Seconds)
        {
            CheckForHistoricalRequests();
            LastHistoricalCheckTime = current_time;
        }
    }
}
//+------------------------------------------------------------------+
//| Timer function                                                   |
//+------------------------------------------------------------------+
void OnTimer()
{
    //--- OHLCV adatok gyűjtése és küldése
    if (Enable_OHLC_Sending)
    {
        CollectAndSendOHLCVData();
    }

    //--- Történelmi kérések ellenőrzése (másodpercenként, ha nincs Tick-en történő ellenőrzés)
    if (Enable_Historical_Sending && !Check_Historical_On_Tick)
    {
        datetime current_time = TimeCurrent();
        if (current_time - LastHistoricalCheckTime >= Historical_Check_Interval_Seconds)
        {
            CheckForHistoricalRequests();
            LastHistoricalCheckTime = current_time;
        }
    }

    //--- Történelmi adatgyűjtés feldolgozása ha aktív
    if (Enable_Historical_Collection && historicalJobActive)
    {
        CollectAndSendHistoricalBatch();
    }
}
//+------------------------------------------------------------------+
//| Trade function                                                   |
//+------------------------------------------------------------------+
void OnTrade()
{
    //--- Send trade event to FastAPI
    Print("Trade event detected");
}
//+------------------------------------------------------------------+
//| TradeTransaction function                                        |
//+------------------------------------------------------------------+
void OnTradeTransaction(const MqlTradeTransaction &trans,
                        const MqlTradeRequest &request,
                        const MqlTradeResult &result)
{
    //---
}
//+------------------------------------------------------------------+
//| ChartEvent function                                              |
//+------------------------------------------------------------------+
void OnChartEvent(const int32_t id,
                  const long &lparam,
                  const double &dparam,
                  const string &sparam)
{
    //---
}
//+------------------------------------------------------------------+
//| BookEvent function                                               |
//+------------------------------------------------------------------+
void OnBookEvent(const string &symbol)
{
    //---
}
//+------------------------------------------------------------------+

//+------------------------------------------------------------------+
//| Parse instruments from input string                             |
//+------------------------------------------------------------------+
void ParseInstruments()
{
    string instruments = Instruments;
    StringReplace(instruments, " ", "");  // Remove spaces
    StringReplace(instruments, "\t", ""); // Remove tabs

    ushort sep = StringGetCharacter(",", 0);
    int count = StringSplit(instruments, sep, symbolArray);
    totalInstruments = count;

    if (totalInstruments == 0)
    {
        // Default to current symbol if none specified
        ArrayResize(symbolArray, 1);
        symbolArray[0] = _Symbol;
        totalInstruments = 1;
    }
}
//+------------------------------------------------------------------+
//| Parse timeframes from input string                              |
//+------------------------------------------------------------------+
void ParseTimeframes()
{
    string timeframes = Timeframes;
    StringReplace(timeframes, " ", "");  // Remove spaces
    StringReplace(timeframes, "\t", ""); // Remove tabs

    ushort sep = StringGetCharacter(",", 0);
    string tfArray[];
    int count = StringSplit(timeframes, sep, tfArray);

    ArrayResize(timeframeArray, count);

    for (int i = 0; i < count; i++)
    {
        timeframeArray[i] = StringToTimeframe(tfArray[i]);
    }

    totalTimeframes = count;

    if (totalTimeframes == 0)
    {
        // Default to current timeframe if none specified
        ArrayResize(timeframeArray, 1);
        timeframeArray[0] = _Period;
        totalTimeframes = 1;
    }
}
//+------------------------------------------------------------------+
//| Convert timeframe string to ENUM_TIMEFRAMES                     |
//+------------------------------------------------------------------+
int StringToTimeframe(string tf)
{
    StringToUpper(tf);

    if (tf == "M1")
        return PERIOD_M1;
    if (tf == "M2")
        return PERIOD_M2;
    if (tf == "M3")
        return PERIOD_M3;
    if (tf == "M4")
        return PERIOD_M4;
    if (tf == "M5")
        return PERIOD_M5;
    if (tf == "M6")
        return PERIOD_M6;
    if (tf == "M10")
        return PERIOD_M10;
    if (tf == "M12")
        return PERIOD_M12;
    if (tf == "M15")
        return PERIOD_M15;
    if (tf == "M20")
        return PERIOD_M20;
    if (tf == "M30")
        return PERIOD_M30;
    if (tf == "H1")
        return PERIOD_H1;
    if (tf == "H2")
        return PERIOD_H2;
    if (tf == "H3")
        return PERIOD_H3;
    if (tf == "H4")
        return PERIOD_H4;
    if (tf == "H6")
        return PERIOD_H6;
    if (tf == "H8")
        return PERIOD_H8;
    if (tf == "H12")
        return PERIOD_H12;
    if (tf == "D1")
        return PERIOD_D1;
    if (tf == "W1")
        return PERIOD_W1;
    if (tf == "MN1")
        return PERIOD_MN1;

    return PERIOD_CURRENT;
}
//+------------------------------------------------------------------+
//| Test connection to FastAPI server                                |
//+------------------------------------------------------------------+
bool TestConnection()
{
    string url = FastAPI_Server + "/api/v1/ping";

    // Send HTTP GET request
    string headers;
    char post[];
    char result[];
    string result_headers;
    int response_code;

    int res = WebRequest("GET", url, headers, 5000, post, result, result_headers);

    if (res == 200) // HTTP 200 OK
    {
        string response = CharArrayToString(result);
        if (Enable_HTTP_Logs)
        {
            Print("Connection test successful: ", response);
        }
        return true;
    }
    else
    {
        if (Enable_HTTP_Logs)
        {
            Print("Connection test failed. Response code: ", res);
            if (res > 0)
            {
                string response = CharArrayToString(result);
                Print("Response: ", response);
            }
        }
        return false;
    }
}

//+------------------------------------------------------------------+
//| Collect and send tick data for all instruments                  |
//+------------------------------------------------------------------+
void CollectAndSendTickData()
{
    for (int i = 0; i < totalInstruments; i++)
    {
        string symbol = symbolArray[i];

        // Get current tick data
        MqlTick last_tick;
        if (SymbolInfoTick(symbol, last_tick) != true)
        {
            if (Enable_HTTP_Logs)
            {
                Print("Error: Failed to get tick data for ", symbol);
            }
            continue; // Skip to next symbol
        }

        // Prepare JSON data
        string json_data = "{";
        json_data += "\"symbol\":\"" + symbol + "\",";
        json_data += "\"bid\":" + DoubleToString(last_tick.bid, (int)SymbolInfoInteger(symbol, SYMBOL_DIGITS)) + ",";
        json_data += "\"ask\":" + DoubleToString(last_tick.ask, (int)SymbolInfoInteger(symbol, SYMBOL_DIGITS)) + ",";
        json_data += "\"time\":" + IntegerToString((int)last_tick.time) + ",";
        json_data += "\"volume\":" + IntegerToString((int)last_tick.volume);
        json_data += "}";

        // Send HTTP POST request
        string url = FastAPI_Server + "/api/v1/collect/tick";
        string headers = "Content-Type: application/json\r\n";

        char post[];
        char result[];
        string result_headers;
        int response_code;

        StringToCharArray(json_data, post, 0, StringLen(json_data));

        int res = WebRequest("POST", url, headers, 5000, post, result, result_headers);

        if (Enable_HTTP_Logs)
        {
            if (res == 200)
            {
                string response = CharArrayToString(result);
                Print("Tick sent: ", symbol, " Bid=", DoubleToString(last_tick.bid, (int)SymbolInfoInteger(symbol, SYMBOL_DIGITS)),
                      " Ask=", DoubleToString(last_tick.ask, (int)SymbolInfoInteger(symbol, SYMBOL_DIGITS)));
            }
            else
            {
                Print("Error sending tick for ", symbol, ": HTTP ", res);
                if (res > 0)
                {
                    string response = CharArrayToString(result);
                    Print("Response: ", response);
                }
            }
        }
    }
}

//+------------------------------------------------------------------+
//| Collect and send OHLCV data for all instruments and timeframes  |
//+------------------------------------------------------------------+
void CollectAndSendOHLCVData()
{
    for (int i = 0; i < totalInstruments; i++)
    {
        string symbol = symbolArray[i];

        for (int j = 0; j < totalTimeframes; j++)
        {
            int timeframe = timeframeArray[j];

            // Get current OHLCV data (last 10 bars)
            int bars_to_send = 10;
            datetime current_time = TimeCurrent();

            // Prepare JSON data
            string json_data = "{";
            json_data += "\"symbol\":\"" + symbol + "\",";
            json_data += "\"timeframe\":" + IntegerToString(timeframe) + ",";
            json_data += "\"timestamp\":" + IntegerToString((int)current_time) + ",";
            json_data += "\"bars\":[";

            // Get all rates at once
            MqlRates rates[];
            int copied = CopyRates(symbol, (ENUM_TIMEFRAMES)timeframe, 0, bars_to_send, rates);

            if (copied > 0)
            {
                for (int k = copied - 1; k >= 0; k--)
                {
                    if (k < copied - 1)
                        json_data += ",";
                    json_data += "{";
                    json_data += "\"time\":" + IntegerToString((int)rates[k].time) + ",";
                    json_data += "\"open\":" + DoubleToString(rates[k].open, (int)SymbolInfoInteger(symbol, SYMBOL_DIGITS)) + ",";
                    json_data += "\"high\":" + DoubleToString(rates[k].high, (int)SymbolInfoInteger(symbol, SYMBOL_DIGITS)) + ",";
                    json_data += "\"low\":" + DoubleToString(rates[k].low, (int)SymbolInfoInteger(symbol, SYMBOL_DIGITS)) + ",";
                    json_data += "\"close\":" + DoubleToString(rates[k].close, (int)SymbolInfoInteger(symbol, SYMBOL_DIGITS)) + ",";
                    json_data += "\"volume\":" + IntegerToString((int)rates[k].tick_volume);
                    json_data += "}";
                }
            }

            json_data += "]}";

            // Send HTTP POST request
            string url = FastAPI_Server + "/api/v1/collect/ohlcv";
            string headers = "Content-Type: application/json\r\n";

            char post[];
            char result[];
            string result_headers;
            int response_code;

            StringToCharArray(json_data, post, 0, StringLen(json_data));

            int res = WebRequest("POST", url, headers, 5000, post, result, result_headers);

            if (Enable_HTTP_Logs)
            {
                if (res == 200)
                {
                    Print("OHLCV sent: ", symbol, " TF=", TimeframeToString(timeframe), " Bars=", bars_to_send);
                }
                else
                {
                    Print("Error sending OHLCV for ", symbol, " TF=", TimeframeToString(timeframe), ": HTTP ", res);
                    if (res > 0)
                    {
                        string response = CharArrayToString(result);
                        Print("Response: ", response);
                    }
                }
            }
        }
    }
}

//+------------------------------------------------------------------+
//| Convert ENUM_TIMEFRAMES to string                               |
//+------------------------------------------------------------------+
string TimeframeToString(int tf)
{
    switch (tf)
    {
    case PERIOD_M1:
        return "M1";
    case PERIOD_M2:
        return "M2";
    case PERIOD_M3:
        return "M3";
    case PERIOD_M4:
        return "M4";
    case PERIOD_M5:
        return "M5";
    case PERIOD_M6:
        return "M6";
    case PERIOD_M10:
        return "M10";
    case PERIOD_M12:
        return "M12";
    case PERIOD_M15:
        return "M15";
    case PERIOD_M20:
        return "M20";
    case PERIOD_M30:
        return "M30";
    case PERIOD_H1:
        return "H1";
    case PERIOD_H2:
        return "H2";
    case PERIOD_H3:
        return "H3";
    case PERIOD_H4:
        return "H4";
    case PERIOD_H6:
        return "H6";
    case PERIOD_H8:
        return "H8";
    case PERIOD_H12:
        return "H12";
    case PERIOD_D1:
        return "D1";
    case PERIOD_W1:
        return "W1";
    case PERIOD_MN1:
        return "MN1";
    }
    return "UNKNOWN";
}
//+------------------------------------------------------------------+

//+------------------------------------------------------------------+
//| Sztring érték kinyerése JSONből                                   |
//+------------------------------------------------------------------+
string ExtractJsonString(const string &json, const string &key)
{
    string search_pattern = "\"" + key + "\":\"";
    int start_pos = StringFind(json, search_pattern);

    if (start_pos == -1)
        return "";

    start_pos += StringLen(search_pattern);
    int end_pos = StringFind(json, "\"", start_pos);

    if (end_pos == -1)
        return "";

    return StringSubstr(json, start_pos, end_pos - start_pos);
}

//+------------------------------------------------------------------+
//| Egész szám érték kinyerése JSONből                                |
//+------------------------------------------------------------------+
long ExtractJsonInteger(const string &json, const string &key)
{
    string search_pattern = "\"" + key + "\":";
    int start_pos = StringFind(json, search_pattern);

    if (start_pos == -1)
        return 0;

    start_pos += StringLen(search_pattern);

    // Szám végének megtalálása (vessző, zárójel, vagy kapcsos zárójel)
    int end_pos = start_pos;
    while (end_pos < StringLen(json))
    {
        string ch = StringSubstr(json, end_pos, 1);
        if (ch == "," || ch == "}" || ch == "]")
            break;
        end_pos++;
    }

    string value_str = StringSubstr(json, start_pos, end_pos - start_pos);
    StringTrimLeft(value_str);
    StringTrimRight(value_str);

    return StringToInteger(value_str);
}

//+------------------------------------------------------------------+
//| Dátum sztring konvertálása datetime értékre (YYYY-MM-DD formátum) |
//+------------------------------------------------------------------+
datetime ParseDateString(const string &date_str)
{
    string parts[];
    ushort sep = StringGetCharacter("-", 0);
    int count = StringSplit(date_str, sep, parts);

    if (count != 3)
        return 0;

    int year = (int)StringToInteger(parts[0]);
    int month = (int)StringToInteger(parts[1]);
    int day = (int)StringToInteger(parts[2]);

    if (year < 1970 || year > 3000)
        return 0;
    if (month < 1 || month > 12)
        return 0;
    if (day < 1 || day > 31)
        return 0;

    return StringToTime(IntegerToString(year) + "." + IntegerToString(month) + "." + IntegerToString(day));
}

//+------------------------------------------------------------------+
//| Történelmi adatkérés kezelése a szervertől                        |
//+------------------------------------------------------------------+
bool HandleHistoricalRequest(const string &json_request)
{
    // JSON kérés feldolgozása
    // Várt formátum:
    // {
    //   "job_id": "job_12345",
    //   "symbol": "EURUSD",
    //   "timeframe": "M1",
    //   "start_date": "2000-01-01",
    //   "end_date": "2025-12-31",
    //   "batch_size_days": 365
    // }

    if (Log_Historical_Requests)
    {
        Print("Történelmi adatkérés fogadva: ", json_request);
    }

    // JSON feldolgozás
    string job_id = ExtractJsonString(json_request, "job_id");
    string symbol = ExtractJsonString(json_request, "symbol");
    string timeframe_str = ExtractJsonString(json_request, "timeframe");
    string start_date_str = ExtractJsonString(json_request, "start_date");
    string end_date_str = ExtractJsonString(json_request, "end_date");
    string batch_size_str = ExtractJsonString(json_request, "batch_size_days");

    // Bemenetek validálása
    if (job_id == "" || symbol == "" || timeframe_str == "" ||
        start_date_str == "" || end_date_str == "")
    {
        Print("Hiba: Érvénytelen történelmi kérés paraméterek");
        return false;
    }

    // Időkeret sztring konvertálása enumra
    int timeframe = StringToTimeframe(timeframe_str);
    if (timeframe == PERIOD_CURRENT)
    {
        Print("Hiba: Érvénytelen időkeret: ", timeframe_str);
        return false;
    }

    // Dátumok konvertálása
    datetime start_date = ParseDateString(start_date_str);
    datetime end_date = ParseDateString(end_date_str);

    if (start_date == 0 || end_date == 0 || start_date >= end_date)
    {
        Print("Hiba: Érvénytelen dátumtartomány");
        return false;
    }

    // Kötegméret kiszámítása
    int batch_size = (int)StringToInteger(batch_size_str);
    if (batch_size <= 0)
    {
        batch_size = Historical_Batch_Size;
    }

    // Kérés tárolása
    activeRequest.job_id = job_id;
    activeRequest.symbol = symbol;
    activeRequest.timeframe = timeframe;
    activeRequest.start_date = start_date;
    activeRequest.end_date = end_date;
    activeRequest.batch_size = batch_size;
    activeRequest.status = "pending";

    // Összes köteg kiszámítása (99,000 gyertya per batch)
    int timeframe_minutes = GetTimeframeMinutes(timeframe);
    int total_bars = (int)((end_date - start_date) / (timeframe_minutes * 60));
    totalBatches = (int)MathCeil((double)total_bars / batch_size);

    if (Log_Historical_Requests)
    {
        Print("Történelmi kérés validálva:");
        Print("  Job ID: ", job_id);
        Print("  Szimbólum: ", symbol);
        Print("  Időkeret: ", TimeframeToString(timeframe));
        Print("  Dátumtartomány: ", TimeToString(start_date), " to ", TimeToString(end_date));
        Print("  Kötegméret: ", batch_size, " gyertya");
        Print("  Összes köteg: ", totalBatches);
        Print("  Összes bar: ", total_bars);
    }

    return true;
}

//+------------------------------------------------------------------+
//| Történelmi adatok gyűjtése és küldése kötegben                    |
//+------------------------------------------------------------------+
bool CollectAndSendHistoricalBatch()
{
    if (activeRequest.status != "in_progress" && activeRequest.status != "pending")
    {
        return false;
    }

    if (activeRequest.status == "pending")
    {
        activeRequest.status = "in_progress";
        currentJobId = activeRequest.job_id;
        currentJobStartTime = TimeCurrent();
        currentBatchNumber = 0;
    }

    // Köteg dátumtartomány kiszámítása (99,000 gyertya per batch)
    int timeframe_minutes = GetTimeframeMinutes(activeRequest.timeframe);
    datetime batch_start = activeRequest.start_date + (currentBatchNumber * activeRequest.batch_size * timeframe_minutes * 60);
    datetime batch_end = MathMin(batch_start + (activeRequest.batch_size * timeframe_minutes * 60), activeRequest.end_date);

    if (batch_start >= activeRequest.end_date)
    {
        // Minden köteg befejezve
        activeRequest.status = "completed";
        historicalJobActive = false;

        if (Log_Historical_Requests)
        {
            Print("Történelmi adatgyűjtés befejezve jobhoz: ", currentJobId);
        }

        return true;
    }

    // Történelmi adatok lekérése
    MqlRates rates[];
    int bars_count = CopyRates(
        activeRequest.symbol,
        (ENUM_TIMEFRAMES)activeRequest.timeframe,
        batch_start,
        batch_end,
        rates);

    if (bars_count <= 0)
    {
        Print("Figyelmeztetés: Nem található adat a(z) ", currentBatchNumber + 1, ". kötethez",
              " (", TimeToString(batch_start), " to ", TimeToString(batch_end), ")");

        // Továbbra is növeljük a kötegszámot és folytatjuk
        currentBatchNumber++;
        return true;
    }

    if (Log_Historical_Requests)
    {
        Print("Lekérve ", bars_count, " bar a(z) ", currentBatchNumber + 1, ". kötethez",
              " (", TimeToString(batch_start), " to ", TimeToString(batch_end), ")");
    }

    // JSON adatok előkészítése
    string json_data = "{";
    json_data += "\"job_id\":\"" + currentJobId + "\",";
    json_data += "\"batch_number\":" + IntegerToString(currentBatchNumber) + ",";
    json_data += "\"symbol\":\"" + activeRequest.symbol + "\",";
    json_data += "\"timeframe\":" + IntegerToString(activeRequest.timeframe) + ",";
    json_data += "\"date_range\":{";
    json_data += "\"start\":\"" + TimeToString(batch_start, TIME_DATE | TIME_MINUTES | TIME_SECONDS) + "\",";
    json_data += "\"end\":\"" + TimeToString(batch_end, TIME_DATE | TIME_MINUTES | TIME_SECONDS) + "\"";
    json_data += "},";
    json_data += "\"bars\":[";

    // Barok adatok hozzáadása
    for (int i = 0; i < bars_count; i++)
    {
        if (i > 0)
            json_data += ",";
        json_data += "{";
        json_data += "\"time\":" + IntegerToString((int)rates[i].time) + ",";
        json_data += "\"open\":" + DoubleToString(rates[i].open, (int)SymbolInfoInteger(activeRequest.symbol, SYMBOL_DIGITS)) + ",";
        json_data += "\"high\":" + DoubleToString(rates[i].high, (int)SymbolInfoInteger(activeRequest.symbol, SYMBOL_DIGITS)) + ",";
        json_data += "\"low\":" + DoubleToString(rates[i].low, (int)SymbolInfoInteger(activeRequest.symbol, SYMBOL_DIGITS)) + ",";
        json_data += "\"close\":" + DoubleToString(rates[i].close, (int)SymbolInfoInteger(activeRequest.symbol, SYMBOL_DIGITS)) + ",";
        json_data += "\"volume\":" + IntegerToString((int)rates[i].tick_volume);
        json_data += "}";
    }

    json_data += "]}";

    // HTTP POST kérés küldése
    string url = FastAPI_Server + "/api/v1/historical/collect";
    string headers = "Content-Type: application/json\r\n";

    char post[];
    char result[];
    string result_headers;
    int response_code;

    StringToCharArray(json_data, post, 0, StringLen(json_data));

    int res = WebRequest("POST", url, headers, Historical_Request_Timeout, post, result, result_headers);

    if (res == 200)
    {
        string response = CharArrayToString(result);

        if (Log_Historical_Requests)
        {
            Print("Köteg ", currentBatchNumber + 1, " sikeresen elküldve: ", bars_count, " bar");
        }

        currentBatchNumber++;

        // Folyamat jelentése
        ReportProgress();

        return true;
    }
    else
    {
        Print("Hiba a(z) ", currentBatchNumber + 1, ". köteg küldésénél: HTTP ", res);

        if (res > 0)
        {
            string response = CharArrayToString(result);
            Print("Válasz: ", response);
        }

        return false;
    }
}

//+------------------------------------------------------------------+
//| Folyamat jelentése a szervernek                                   |
//+------------------------------------------------------------------+
void ReportProgress()
{
    if (currentJobId == "")
        return;

    int progress_percentage = (int)((double)currentBatchNumber / totalBatches * 100);
    int total_bars = totalBatches * activeRequest.batch_size;

    string json_data = "{";
    json_data += "\"job_id\":\"" + currentJobId + "\",";
    json_data += "\"progress\":" + IntegerToString(progress_percentage) + ",";
    json_data += "\"total_bars\":" + IntegerToString(total_bars) + ",";
    json_data += "\"current_batch\":" + IntegerToString(currentBatchNumber);
    json_data += "}";

    string url = FastAPI_Server + "/api/v1/historical/progress";
    string headers = "Content-Type: application/json\r\n";

    char post[];
    char result[];
    string result_headers;
    int response_code;

    StringToCharArray(json_data, post, 0, StringLen(json_data));

    int res = WebRequest("POST", url, headers, 10, post, result, result_headers);

    if (res == 200 && Log_Historical_Requests)
    {
        Print("Progress updated: ", progress_percentage, "% (", currentBatchNumber, "/", totalBatches, ")");
    }
}

//+------------------------------------------------------------------+
//| Történelmi adatkérések ellenőrzése                                |
//+------------------------------------------------------------------+
void CheckForHistoricalRequests()
{
    if (!Enable_Historical_Collection)
    {
        return;
    }

    // Logolás optimalizálása - csak az első alkalommal részletesen
    static bool first_check = true;
    if (first_check)
    {
        Print("=== HISTORICAL REQUEST CHECK ===");
        Print("Time: ", TimeToString(TimeCurrent(), TIME_DATE | TIME_SECONDS));
        Print("FastAPI Server: ", FastAPI_Server);
        Print("Check Interval: ", Historical_Check_Interval_Seconds, " seconds");
        first_check = false;
    }

    string url = FastAPI_Server + "/api/v1/historical/poll";
    string cookie = NULL;
    string headers_received;
    char post[];
    char result_data[];
    int response_code;

    ResetLastError();
    int res = WebRequest("GET", url, cookie, NULL, 5000, post, 0, result_data, headers_received);

    int error_code = GetLastError();

    if (res == 200)
    {
        string response = CharArrayToString(result_data);

        if (response != "" && response != "{}")
        {
            // Új kérés fogadva
            if (Log_Historical_Requests)
            {
                Print("New historical job received: ", response);
            }

            if (HandleHistoricalRequest(response))
            {
                historicalJobActive = true;
                Print("✓ Historical job started: ", activeRequest.job_id);
            }
            else
            {
                Print("✗ Failed to handle historical request");
            }
        }
        else
        {
            // Nincs job, de a kapcsolat működik
            static int last_logged = 0;
            if (TimeCurrent() - last_logged >= 60) // Csak percenként logoljuk
            {
                Print("No historical jobs available");
                last_logged = TimeCurrent();
            }
        }
    }
    else
    {
        static int error_count = 0;
        error_count++;

        if (error_count <= 3 || error_count % 60 == 0) // Csak az első 3-at és utána percenként
        {
            Print("Error checking historical requests: ", res);
            if (error_code != 0)
            {
                Print("Error Code: ", error_code);
            }
            if (res > 0)
            {
                string response = CharArrayToString(result_data);
                Print("Error response: ", response);
            }
        }
    }
}

//+------------------------------------------------------------------+
//| Történelmi gyűjtési hiba kezelése                                 |
//+------------------------------------------------------------------+
void HandleHistoricalError(const string &error_message)
{
    Print("Történelmi gyűjtési hiba: ", error_message);

    // Hiba jelentése a szervernek
    string json_data = "{";
    json_data += "\"job_id\":\"" + currentJobId + "\",";
    json_data += "\"status\":\"error\",";
    json_data += "\"error\":\"" + error_message + "\",";
    json_data += "\"batch_number\":" + IntegerToString(currentBatchNumber);
    json_data += "}";

    string url = FastAPI_Server + "/api/v1/historical/error";
    string headers = "Content-Type: application/json\r\n";

    char post[];
    char result[];
    string result_headers;
    int response_code;

    StringToCharArray(json_data, post, 0, StringLen(json_data));

    WebRequest("POST", url, headers, 10, post, result, result_headers);

    // Állapot visszaállítása
    historicalJobActive = false;
    currentJobId = "";
    activeRequest.status = "failed";
}

//+------------------------------------------------------------------+
//| Optimális kötegméret az időkeret alapján                          |
//+------------------------------------------------------------------+
int GetOptimalBatchSize(int timeframe)
{
    int base_batch_days = 365; // Alapértelmezett 365 nap

    // Beállítás nagyfrekvenciás időkeretekhez
    if (timeframe <= PERIOD_M1)
    {
        return MathMin(base_batch_days, 30); // 1 hónap max M1hez
    }
    else if (timeframe <= PERIOD_M5)
    {
        return MathMin(base_batch_days, 90); // 3 hónap max M5höz
    }
    else if (timeframe <= PERIOD_M15)
    {
        return MathMin(base_batch_days, 180); // 6 hónap max M15höz
    }
    else
    {
        return base_batch_days; // Teljes köteg magasabb időkeretekhez
    }
}

//+------------------------------------------------------------------+
//| Időkeret percekben kiszámítása                                    |
//+------------------------------------------------------------------+
int GetTimeframeMinutes(int tf)
{
    switch (tf)
    {
    case PERIOD_M1:
        return 1;
    case PERIOD_M5:
        return 5;
    case PERIOD_M15:
        return 15;
    case PERIOD_H1:
        return 60;
    case PERIOD_H4:
        return 240;
    case PERIOD_D1:
        return 1440;
    default:
        return 60;
    }
}
