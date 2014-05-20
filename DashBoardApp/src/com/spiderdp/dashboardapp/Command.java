package com.spiderdp.dashboardapp;

public class Command {
	public int command;
	public String data;
	
	public Command(int command, String data){
		this.command = command;
		this.data = data;
	}
	
	public Command(String line){
		System.out.println(line);
		String[] splitted = line.split("<;>", 2);
		
		this.command = Integer.parseInt(splitted[0]);
		this.data = splitted[1];
	}
	
	public String[] dataAsArray(){
		return data.split("<;>");
	}
}
