package com.spiderdp.dashboardapp;

import com.jjoe64.graphview.GraphView;
import com.jjoe64.graphview.GraphView.LegendAlign;
import com.jjoe64.graphview.GraphViewSeries;
import com.jjoe64.graphview.GraphViewSeries.GraphViewSeriesStyle;
import com.jjoe64.graphview.GraphViewStyle;
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
		GraphViewData[] dataHoek1 = new GraphViewData[data.length];
		GraphViewData[] dataHoek2 = new GraphViewData[data.length];
		
		for(int i = 0; i < data.length; i++){
			String hoek1 = data[i].split("h1:")[1].split(",")[0];
			String hoek2 = data[i].split("h2:")[1].split(",")[0];
			
			System.out.println("Hoek1 " +hoek1);
			System.out.println("Hoek2 " +hoek2);
			
			dataHoek1[i] = new GraphViewData(i+1, Double.parseDouble(hoek1));
			dataHoek2[i] = new GraphViewData(i+1, Double.parseDouble(hoek2));
		}

		series1 = new GraphViewSeries("Hoek 1", new GraphViewSeriesStyle(Color.BLUE, 5), dataHoek1);

		series2 = new GraphViewSeries("Hoek 2", new GraphViewSeriesStyle(Color.BLACK, 5), dataHoek2);
		 
		GraphView graphView = new LineGraphView(view.getContext(), "Hellingshoek");
		graphView.addSeries(series1); // data
		graphView.addSeries(series2);
		
		graphView.setShowLegend(true);
		graphView.setLegendAlign(LegendAlign.BOTTOM);
		graphView.setLegendWidth(200);
		 
		LinearLayout layout = (LinearLayout) view.findViewById(R.id.hellings_hoek_graph);
		layout.addView(graphView);
	}
	
	public void updateChart(String[] data){
		GraphViewData[] dataHoek1 = new GraphViewData[data.length];
		GraphViewData[] dataHoek2 = new GraphViewData[data.length];
		
		for(int i = 0; i < data.length; i++){
			String hoek1 = data[i].split("h1:")[1].split(",")[0];
			String hoek2 = data[i].split("h2:")[1].split(",")[0];
			
			System.out.println("Hoek1 " +hoek1);
			System.out.println("Hoek2 " +hoek2);
			
			dataHoek1[i] = new GraphViewData(i+1, Double.parseDouble(hoek1));
			dataHoek2[i] = new GraphViewData(i+1, Double.parseDouble(hoek2));
		}
		
		series1.resetData(dataHoek1);
		series2.resetData(dataHoek2);
	}
}
