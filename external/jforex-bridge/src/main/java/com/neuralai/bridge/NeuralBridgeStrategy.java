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

    // Konfiguráció
    private static final int TICK_PORT = 5557;
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
        this.tickPublisher.bind(BIND_ADDRESS + TICK_PORT);

        // REP Socket (Parancs befelé)
        this.commandReceiver = this.context.socket(ZMQ.REP);
        this.commandReceiver.bind(BIND_ADDRESS + COMMAND_PORT);

        console.getOut().println("Neural Bridge started - Ports: " + TICK_PORT + ", " + COMMAND_PORT);

        // Feliratkozás az instrumentumokra
        Set<Instrument> instruments = new HashSet<>();
        instruments.add(Instrument.EURUSD);
        instruments.add(Instrument.GBPUSD);
        instruments.add(Instrument.USDJPY);
        instruments.add(Instrument.XAUUSD);

        context.setSubscribedInstruments(instruments, true);
        console.getOut().println("Subscribed to instruments: " + instruments);

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

            String json = gson.toJson(data);
            tickPublisher.send(json.getBytes(StandardCharsets.UTF_8), 0);
            
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