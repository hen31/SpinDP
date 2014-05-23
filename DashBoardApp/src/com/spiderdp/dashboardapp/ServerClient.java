package com.spiderdp.dashboardapp;

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

public class ServerClient {

	public static final int TO_BALLOON_MODE = 1;
	public static final int TO_TEERBAL_MODE = 2;
	public static final int TO_DANCE_MODE = 3;
	public static final int TO_DERBY_MODE = 10;
	public static  final int MOVE_INTERNAL = 8;
	public static  final  int KILL = 6;
	public static  final int IDENTYFY = -2;
	public static  final int MOVE = 7;
	public static final int TO_MANUAL = 0;
	public static final int MOVE_HEIGHT = 9;
	public static final int SEND_SENSOR_DATA = 4;
	public static final int LOG = 10;
	public static final int SEND_ACCU_DATA = 11;
	
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
        MainActivity.connected =true;
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
            paramList.add("dashboard");
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
						    //System.out.println("message from ip:" + client.getRemoteSocketAddress());
						    //System.out.println(s);
						    this.handleLine(s);
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
	
	public void handleLine(String line){
		final Command cmd = new Command(line);
		if(cmd.command == ServerClient.SEND_SENSOR_DATA){
			activity.runOnUiThread(new Runnable(){
				@Override
				public void run(){
					PagerAdapter.hellingsHoek.showChart(cmd.dataAsArray());
				}
			});
		}
		else if(cmd.command == ServerClient.LOG){
			activity.runOnUiThread(new Runnable(){
				@Override
				public void run(){
					PagerAdapter.log.addLine(cmd.data);
				}
			});
		}
		
		else if(cmd.command == ServerClient.SEND_ACCU_DATA){
			activity.runOnUiThread(new Runnable(){
				@Override
				public void run(){
					PagerAdapter.accuSpanning.showChart(cmd.dataAsArray());
				}
			});
		}
		
	}
	
}
