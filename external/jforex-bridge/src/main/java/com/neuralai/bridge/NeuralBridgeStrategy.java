package com.neuralai.bridge;

import com.dukascopy.api.*;
import com.dukascopy.api.IEngine.OrderCommand;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import org.zeromq.ZMQ;

import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

/**
 * Neural AI Bridge Strategy for JForex 4.
 * Implements IStrategy to communicate with Python via ZeroMQ.
 */
@RequiresFullAccess
@Library("jeromq-0.5.4.jar:gson-2.10.1.jar")
public class NeuralBridgeStrategy implements IStrategy {

    private ZMQ.Context context;
    private ZMQ.Socket tickPublisher;
    private ZMQ.Socket commandReceiver;

    private IEngine engine;
    private IConsole console;
    private IHistory history;
    private Gson gson;

    // Tick számláló statisztikákhoz
    private Map<Instrument, Long> tickCounts;

    // Konfiguráció
    @Configurable("Subscribe EUR/USD")
    public boolean subEURUSD = true;

    @Configurable("Subscribe GBP/USD")
    public boolean subGBPUSD = true;

    @Configurable("Subscribe USD/JPY")
    public boolean subUSDJPY = true;

    @Configurable("Subscribe USD/CHF")
    public boolean subUSDCHF = true;
    
    @Configurable("Subscribe XAU/USD")
    public boolean subXAUUSD = true;

    @Configurable("ZMQ Tick Port")
    public int tickPort = 5557;

    private static final int COMMAND_PORT = 5558;
    private static final String BIND_ADDRESS = "tcp://*:";

    @Override
    public void onStart(IContext context) throws JFException {
        this.engine = context.getEngine();
        this.console = context.getConsole();
        this.history = context.getHistory();
        this.gson = new GsonBuilder().create();

        // ZeroMQ Init
        this.context = ZMQ.context(1);

        // PUB Socket (Adat kifelé)
        this.tickPublisher = this.context.socket(ZMQ.PUB);
        this.tickPublisher.bind(BIND_ADDRESS + tickPort);

        // REP Socket (Parancs befelé)
        this.commandReceiver = this.context.socket(ZMQ.REP);
        this.commandReceiver.bind(BIND_ADDRESS + COMMAND_PORT);

        console.getOut().println("Neural Bridge started - Ports: " + tickPort + ", " + COMMAND_PORT);

        // Tick számláló inicializálása
        this.tickCounts = new HashMap<>();

        // Feliratkozás az instrumentumokra (dinamikus konfiguráció alapján)
        Set<Instrument> instruments = new HashSet<>();
        
        if (subEURUSD) instruments.add(Instrument.EURUSD);
        if (subGBPUSD) instruments.add(Instrument.GBPUSD);
        if (subUSDJPY) instruments.add(Instrument.USDJPY);
        if (subUSDCHF) instruments.add(Instrument.USDCHF);
        if (subXAUUSD) instruments.add(Instrument.XAUUSD);
        
        if (instruments.isEmpty()) {
            console.getErr().println("WARNING: No instruments selected!");
        } else {
            context.setSubscribedInstruments(instruments, true);
            console.getOut().println("Subscribed to instruments: " + instruments);
        }

        // Parancsfigyelő szál indítása
        new Thread(this::commandListener).start();
    }

    @Override
    public void onTick(Instrument instrument, ITick tick) throws JFException {
        // Hangos debug log, hogy lássuk a bejövő tickeket
        console.getOut().println("TICK: " + instrument + " " + tick.getBid());
        
        try {
            Map<String, Object> data = new HashMap<>();
            data.put("type", "TICK");
            // A Python 'EURUSD' formátumot vár, a JForex 'EUR/USD'-t ad. Cseréljük.
            data.put("symbol", instrument.name().replace("/", ""));
            data.put("bid", tick.getBid());
            data.put("ask", tick.getAsk());
            data.put("timestamp", tick.getTime());
            data.put("source", "jforex");
            
            // Volume adatok hozzáadása a JForex Tester kompatibilitásért
            data.put("ask_volume", tick.getAskVolume());
            data.put("bid_volume", tick.getBidVolume());

            String json = gson.toJson(data);
            tickPublisher.send(json.getBytes(StandardCharsets.UTF_8), 0);
            
            // Tick számláló frissítése
            long count = tickCounts.getOrDefault(instrument, 0L);
            tickCounts.put(instrument, count + 1);

            // Opcionális: Minden 1000. ticknél logoljon egyet, hogy lássuk, hogy él
            if ((count + 1) % 1000 == 0) {
                console.getOut().println("STATS: Sent " + (count + 1) + " ticks for " + instrument);
            }
            
        } catch (Exception e) {
            console.getErr().println("Error sending tick: " + e.getMessage());
        }
    }

    // A JForex API megköveteli az onBar implementálását, még ha üres is.
    // JForex 4 esetén az aláírás: onBar(Instrument, Period, IBar, IBar)
    @Override
    public void onBar(Instrument instrument, Period period, IBar askBar, IBar bidBar) throws JFException {
        // Jelenleg nem használjuk a bar adatokat, csak a tickeket
    }

    @Override
    public void onMessage(IMessage message) throws JFException {
        // Itt kapjuk meg a visszajelzést a brókertől (pl. ORDER_FILLED)
        // Ezt később továbbíthatjuk a Pythonnak
    }

    @Override
    public void onAccount(IAccount account) throws JFException {
        // Számlaadatok változása
    }

    @Override
    public void onStop() throws JFException {
        // Takarítás
        if (tickPublisher != null) tickPublisher.close();
        if (commandReceiver != null) commandReceiver.close();
        if (context != null) context.term();
        
        // Statisztikák kiírása
        console.getOut().println("=== BRIDGE SESSION STATISTICS ===");
        for (Map.Entry<Instrument, Long> entry : tickCounts.entrySet()) {
            console.getOut().println(">> " + entry.getKey() + ": " + entry.getValue() + " ticks sent.");
        }
        console.getOut().println("=================================");
        
        console.getOut().println("Neural Bridge stopped");
    }

    // --- Belső metódusok ---

    private void commandListener() {
        while (!Thread.currentThread().isInterrupted() && context != null) {
            try {
                // Blokkoló hívás, várja a parancsot a Pythontól
                byte[] request = commandReceiver.recv(0);
                if (request == null) break; 

                String jsonRequest = new String(request, StandardCharsets.UTF_8);
                console.getOut().println("CMD Received: " + jsonRequest);

                // TODO: Itt dolgozzuk fel a Trade parancsot (SubmitOrder)
                // Egyelőre csak visszhangozzuk
                
                String response = "{\"status\": \"RECEIVED\"}";
                commandReceiver.send(response.getBytes(StandardCharsets.UTF_8), 0);

            } catch (Exception e) {
                console.getErr().println("Command Listener Error: " + e.getMessage());
                break;
            }
        }
    }
}