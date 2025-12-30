package com.neuralai.bridge;

import com.dukascopy.api.*;
import org.zeromq.ZMQ;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import java.util.HashMap;
import java.util.Map;
import java.nio.charset.StandardCharsets;

/**
 * JForex Strategy for Neural AI Bridge.
 * Publishes tick data via ZeroMQ PUB socket and receives trading commands via REP socket.
 * 
 * @author Neural AI Team
 * @version 1.0.0
 */
@RequiresFullAccess
public class NeuralBridgeStrategy implements IStrategy {

    private ZMQ.Context context;
    private ZMQ.Socket tickPublisher;
    private ZMQ.Socket commandReceiver;
    private Gson gson;

    private IEngine engine;
    private IConsole console;

    // Konfiguráció
    private static final int TICK_PORT = 5555;
    private static final int COMMAND_PORT = 5556;
    private static final String BIND_ADDRESS = "tcp://*:";

    /**
     * Strategy start callback.
     * Initializes ZeroMQ sockets and starts command listener thread.
     * 
     * @param context JForex context
     * @throws JFException if initialization fails
     */
    @Override
    public void onStart(IContext context) throws JFException {
        this.engine = context.getEngine();
        this.console = context.getConsole();

        // ZeroMQ kontextus inicializálása
        this.context = ZMQ.context(1);

        // Tick publisher socket (PUB)
        this.tickPublisher = this.context.socket(ZMQ.PUB);
        this.tickPublisher.bind(BIND_ADDRESS + TICK_PORT);

        // Command receiver socket (REP)
        this.commandReceiver = this.context.socket(ZMQ.REP);
        this.commandReceiver.bind(BIND_ADDRESS + COMMAND_PORT);

        console.getOut().println("Neural Bridge started - Ports: " + TICK_PORT + ", " + COMMAND_PORT);

        // Gson inicializálása
        this.gson = new GsonBuilder().create();

        // Command listener indítása külön szálban
        Thread commandThread = new Thread(this::commandListener, "command-listener");
        commandThread.setDaemon(true);
        commandThread.start();
    }

    /**
     * Tick data callback.
     * Publishes tick data to ZeroMQ PUB socket.
     * 
     * @param instrument Trading instrument
     * @param tick Tick data
     * @throws JFException if tick processing fails
     */
    @Override
    public void onTick(Instrument instrument, ITick tick) throws JFException {
        // Tick adatok gyűjtése Map-be
        Map<String, Object> data = new HashMap<>();
        data.put("type", "TICK");
        data.put("symbol", instrument.name().replace("/", ""));
        data.put("bid", tick.getBid());
        data.put("ask", tick.getAsk());
        data.put("timestamp", tick.getTime());
        data.put("source", "jforex_live");

        // JSON szerializálás
        String json = gson.toJson(data);

        // Küldés a ZeroMQ PUB socketen
        tickPublisher.send(json.getBytes(StandardCharsets.UTF_8), 0);

        // Logolás JForex konzolra
        console.getOut().println("PUB: " + json);
    }

    /**
     * Command listener thread.
     * Listens for trading commands on REP socket and responds.
     */
    private void commandListener() {
        console.getOut().println("Command listener thread started");

        while (!Thread.currentThread().isInterrupted()) {
            try {
                // Parancs fogadása
                byte[] request = commandReceiver.recv(0);
                String command = new String(request, ZMQ.CHARSET);

                console.getOut().println("Command received: " + command);

                // Egyszerű válasz
                String response = "OK: " + command;

                // Válasz küldése
                commandReceiver.send(response.getBytes(ZMQ.CHARSET), 0);

            } catch (Exception e) {
                console.getErr().println("Command processing error: " + e.getMessage());
                String errorResponse = "ERROR: " + e.getMessage();
                commandReceiver.send(errorResponse.getBytes(ZMQ.CHARSET), 0);
            }
        }

        console.getOut().println("Command listener thread stopped");
    }

    /**
     * Strategy stop callback.
     * Closes ZeroMQ sockets and terminates context.
     * 
     * @throws JFException if cleanup fails
     */
    @Override
    public void onStop() throws JFException {
        // Socket-ek lezárása
        if (tickPublisher != null) {
            tickPublisher.close();
        }
        if (commandReceiver != null) {
            commandReceiver.close();
        }
        if (context != null) {
            context.term();
        }

        console.getOut().println("Neural Bridge stopped");
    }

    /**
     * Account callback (not used).
     */
    @Override
    public void onAccount(IAccount account) throws JFException {
        // Not implemented
    }

    /**
     * Message callback (not used).
     */
    @Override
    public void onMessage(IMessage message) throws JFException {
        // Not implemented
    }

    /**
     * Stop loss callback (not used).
     */
    @Override
    public void onStopLoss(ITradeOrder order) throws JFException {
        // Not implemented
    }
}