package com.spiderdp.dashboardapp;

import com.jjoe64.graphview.GraphView;
import com.jjoe64.graphview.GraphView.LegendAlign;
import com.jjoe64.graphview.GraphViewSeries;
import com.jjoe64.graphview.GraphViewSeries.GraphViewSeriesStyle;
import com.jjoe64.graphview.LineGraphView;

import android.graphics.Color;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.LinearLayout;

public class HellingsHoekFragment extends Fragment {

	private View view;
	private GraphView graphView;
	private GraphViewSeries series1;
	private GraphViewSeries series2;
	private GraphViewSeries series3;
	
	@Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View rootView = inflater.inflate(R.layout.hellings_hoek_fragment, container, false);
        this.view = rootView;
        if(MainActivity.connected){
        	ServerClient.getInstance().sendMessage(ServerClient.SEND_SENSOR_DATA, null);
        }
        return rootView;
    }
	
	public void showChart(String[] data){
		if (graphView != null){
			this.updateChart(data);
			return;
		}
		GraphViewData[] dataYaw = new GraphViewData[data.length];
		GraphViewData[] dataPitch = new GraphViewData[data.length];
		GraphViewData[] dataRoll = new GraphViewData[data.length];
		
		for(int i = 0; i < data.length; i++){
			String yaw = data[i].split("y:")[1].split(",")[0];
			String pitch = data[i].split("p:")[1].split(",")[0];
			String roll = data[i].split("r:")[1].split(",")[0];
			
			dataYaw[i] = new GraphViewData(i+1, Double.parseDouble(yaw));
			dataPitch[i] = new GraphViewData(i+1, Double.parseDouble(pitch));
			dataRoll[i] = new GraphViewData(i+1, Double.parseDouble(roll));
		}

		series1 = new GraphViewSeries("Yaw", new GraphViewSeriesStyle(Color.RED, 5), dataYaw);
		series2 = new GraphViewSeries("Pitch", new GraphViewSeriesStyle(Color.GREEN, 5), dataPitch);
		series3 = new GraphViewSeries("Roll", new GraphViewSeriesStyle(Color.BLUE, 5), dataRoll);
		
		
		graphView = new LineGraphView(view.getContext(), "Hellingshoek");
		graphView.addSeries(series1); // data
		graphView.addSeries(series2);
		graphView.addSeries(series3);
		
		graphView.setShowLegend(true);
		graphView.setLegendAlign(LegendAlign.BOTTOM);
		graphView.setLegendWidth(200);
		 
		LinearLayout layout = (LinearLayout) view.findViewById(R.id.hellings_hoek_graph);
		layout.addView(graphView);
	}
	
	public void updateChart(String[] data){
		GraphViewData[] dataYaw = new GraphViewData[data.length];
		GraphViewData[] dataPitch = new GraphViewData[data.length];
		GraphViewData[] dataRoll = new GraphViewData[data.length];
		
		for(int i = 0; i < data.length; i++){
			String yaw = data[i].split("y:")[1].split(",")[0];
			String pitch = data[i].split("p:")[1].split(",")[0];
			String roll = data[i].split("r:")[1].split(",")[0];
			
			dataYaw[i] = new GraphViewData(i+1, Double.parseDouble(yaw));
			dataPitch[i] = new GraphViewData(i+1, Double.parseDouble(pitch));
			dataRoll[i] = new GraphViewData(i+1, Double.parseDouble(roll));
		}
		
		series1.resetData(dataYaw);
		series2.resetData(dataPitch);
		series3.resetData(dataRoll);
	}
}
