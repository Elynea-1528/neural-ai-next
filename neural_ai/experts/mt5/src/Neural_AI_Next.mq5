//+------------------------------------------------------------------+
//|                                               Neural_AI_Next.mq5 |
//|                                  Copyright 2025, MetaQuotes Ltd. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2025, MetaQuotes Ltd."
#property link "https://www.mql5.com"
#property version "1.00"

// Input parameters
input string FastAPI_Server = "http://localhost:8000"; // FastAPI server address
input int Update_Interval = 60;                        // Update interval in seconds
input bool Enable_HTTP_Logs = true;                    // Enable HTTP request logging

// Global variables
bool isConnected = false;

//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
{
    //--- create timer
    EventSetTimer(Update_Interval);

    //--- Test connection to FastAPI server
    if (TestConnection())
    {
        isConnected = true;
        Print("✓ Connected to FastAPI server: ", FastAPI_Server);
    }
    else
    {
        Print("⚠ Warning: Could not connect to FastAPI server");
        Print("  Server: ", FastAPI_Server);
        Print("  EA will continue but data collection may fail");
    }

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
    //--- Collect and send tick data
    CollectAndSendTickData();
}
//+------------------------------------------------------------------+
//| Timer function                                                   |
//+------------------------------------------------------------------+
void OnTimer()
{
    //--- Collect and send OHLCV data periodically
    CollectAndSendOHLCVData();
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
//| Collect and send tick data                                       |
//+------------------------------------------------------------------+
void CollectAndSendTickData()
{
    // Get current tick data
    MqlTick last_tick;
    if (SymbolInfoTick(_Symbol, last_tick) != true)
    {
        Print("Error: Failed to get tick data for ", _Symbol);
        return;
    }

    // Prepare JSON data
    string json_data = "{";
    json_data += "\"symbol\":\"" + _Symbol + "\",";
    json_data += "\"bid\":" + DoubleToString(last_tick.bid, _Digits) + ",";
    json_data += "\"ask\":" + DoubleToString(last_tick.ask, _Digits) + ",";
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
            Print("Tick sent: ", _Symbol, " Bid=", DoubleToString(last_tick.bid, _Digits), " Ask=", DoubleToString(last_tick.ask, _Digits));
        }
        else
        {
            Print("Error sending tick: HTTP ", res);
            if (res > 0)
            {
                string response = CharArrayToString(result);
                Print("Response: ", response);
            }
        }
    }
}

//+------------------------------------------------------------------+
//| Collect and send OHLCV data                                      |
//+------------------------------------------------------------------+
void CollectAndSendOHLCVData()
{
    // Get current OHLCV data (last 10 bars)
    int bars_to_send = 10;
    datetime current_time = TimeCurrent();

    // Prepare JSON data
    string json_data = "{";
    json_data += "\"symbol\":\"" + Symbol() + "\",";
    json_data += "\"timeframe\":\"" + IntegerToString(Period()) + "\",";
    json_data += "\"timestamp\":" + IntegerToString((int)current_time) + ",";
    json_data += "\"bars\":[";

    // Get all rates at once
    MqlRates rates[];
    int copied = CopyRates(_Symbol, _Period, 0, bars_to_send, rates);

    if (copied > 0)
    {
        for (int i = copied - 1; i >= 0; i--)
        {
            if (i < copied - 1)
                json_data += ",";
            json_data += "{";
            json_data += "\"time\":" + IntegerToString((int)rates[i].time) + ",";
            json_data += "\"open\":" + DoubleToString(rates[i].open, _Digits) + ",";
            json_data += "\"high\":" + DoubleToString(rates[i].high, _Digits) + ",";
            json_data += "\"low\":" + DoubleToString(rates[i].low, _Digits) + ",";
            json_data += "\"close\":" + DoubleToString(rates[i].close, _Digits) + ",";
            json_data += "\"volume\":" + IntegerToString((int)rates[i].tick_volume);
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
            Print("OHLCV sent: ", Symbol(), " TF=", Period(), " Bars=", bars_to_send);
        }
        else
        {
            Print("Error sending OHLCV: HTTP ", res);
            if (res > 0)
            {
                string response = CharArrayToString(result);
                Print("Response: ", response);
            }
        }
    }
}

//+------------------------------------------------------------------+
