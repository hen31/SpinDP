package com.spiderdp.spidercontroller;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.ArrayList;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;

import android.app.Activity;
import android.widget.Toast;

public class ServerClient {

	public static final int TO_AUTO1 = 1;
	public static final int TO_AUTO2 = 2;
	public static final int TO_AUTO3 = 3;
	public static final int TO_AUTO4 = 10;
	public static  final int MOVE_INTERNAL = 8;
	public static  final  int KILL = 6;
	public static  final int IDENTYFY = -2;
	public static  final int MOVE = 7;
	public static final int TO_MANUAL = 0;
	public static final int MOVE_HEIGHT = 9;
	static private ServerClient instance = null;
	public static ServerClient getInstance()
	{
		if(instance == null)
		{
			instance = new ServerClient("192.168.10.1");
		}
		return instance;
	}
	public static ServerClient getInstance(Activity activity)
	{
		if(instance == null)
		{
			instance = new ServerClient("192.168.10.1");
		}
		instance.activity = activity;
		return instance;
	}
	private String serverName;//server host
    private int port;//port number of server
    private BufferedReader input;//input stream from client
    private Socket client;//client's socket connection
    private PrintWriter output;//output stream from client
   private Activity activity;

  private List<Object> paramList =  new ArrayList<Object>();

    public ServerClient( String ipAdress) {
        serverName = ipAdress;
        port = 15;
        //this.activity = mainActivity;
        Thread listenerThread = new Thread(new Runnable() {
            public void run() {
            	ServerClient.this.run();
            }
        });
        listenerThread.start();
        
	}

	/**
     * main methoded that is listining to server
     */
    public void run() {
        try {
            System.out.println("Connecting to " + serverName
                    + " on port " + port);
            client = new Socket(serverName, port);
            System.out.println("Just connected to "
                    + client.getRemoteSocketAddress());
            OutputStream outToServer = client.getOutputStream();
            output =
                    new PrintWriter(outToServer, true);

            input = new BufferedReader(new InputStreamReader(client.getInputStream()));
            paramList.clear();
            paramList.add("controller");
            sendMessage(ServerClient.IDENTYFY, paramList);
        } catch (UnknownHostException ex) {
            Logger.getLogger(ServerClient.class.getName()).log(Level.SEVERE, null, ex);
        } catch (IOException ex) {
            Logger.getLogger(ServerClient.class.getName()).log(Level.SEVERE, null, ex);
        }
         
         
        while (true) {
            try {
                if (input.ready()) {
                	final	String s = input.readLine();
                    activity.runOnUiThread(new Runnable(){

						@Override
						public void run() {
						    System.out.println("message from ip:" + client.getRemoteSocketAddress());
	                        Toast.makeText(ServerClient.this.activity.getApplicationContext(), s, 
	                        		   Toast.LENGTH_LONG).show();
							
						}});
                }
            } catch (IOException ex) {
                Logger.getLogger(ServerClient.class.getName()).log(Level.SEVERE, null, ex);
            }

        }

    }

    /**
     * Send message to server
     * @param message the message you want to send
     */
    void sendMessage(int Command, List<Object> params) {
        System.out.println("message to ip:" + client.getRemoteSocketAddress());
        String line = "";
        if(params !=null && params.size() >0)
        {
        	line = Integer.toString(Command) + "<;>";
        	for(Object obj : params)
        	{
        		line+= obj.toString() +"<;>";
        	}
        }
        else{
        	line = Integer.toString(Command) + "<;>";
        }
        output.println(line);
    }
	
	
	
}
