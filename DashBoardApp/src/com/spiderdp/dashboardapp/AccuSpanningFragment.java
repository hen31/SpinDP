package com.spiderdp.dashboardapp;

import com.jjoe64.graphview.GraphView;
import com.jjoe64.graphview.GraphViewSeries;
import com.jjoe64.graphview.LineGraphView;
import com.jjoe64.graphview.GraphView.LegendAlign;
import com.jjoe64.graphview.GraphViewSeries.GraphViewSeriesStyle;

import android.graphics.Color;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.LinearLayout;

public class AccuSpanningFragment extends Fragment{

	private View view;
	private GraphView graphView;
	private GraphViewSeries series;
	
	@Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View rootView = inflater.inflate(R.layout.accu_spanning_fragment, container, false);
        this.view = rootView;
        if(MainActivity.connected){
        	ServerClient.getInstance().sendMessage(ServerClient.SEND_ACCU_DATA, null);
        }
        return rootView;
    }
	
	public void showChart(String[] data){
		if(graphView != null){
			this.updateChart(data);
			return;
		}
		GraphViewData[] dataAccuSpanning = new GraphViewData[data.length];
		
		for(int i = 0; i < data.length; i++){			
			dataAccuSpanning[i] = new GraphViewData(i+1, Double.parseDouble(data[i]));
		}

		series = new GraphViewSeries("Accu spanning", new GraphViewSeriesStyle(Color.BLUE, 3), dataAccuSpanning);
		
		graphView = new LineGraphView(view.getContext(), "Accu spanning");
		graphView.addSeries(series); // data
		
		graphView.setShowLegend(true);
		graphView.setLegendAlign(LegendAlign.BOTTOM);
		graphView.setLegendWidth(300);
		 
		LinearLayout layout = (LinearLayout) view.findViewById(R.id.accu_spanning_graph);
		layout.addView(graphView);
	}
	
	public void updateChart(String[] data){
		GraphViewData[] dataAccuSpanning = new GraphViewData[data.length];
		
		for(int i = 0; i < data.length; i++){			
			dataAccuSpanning[i] = new GraphViewData(i+1, Double.parseDouble(data[i]));
		}
		
		series.resetData(dataAccuSpanning);
	}
	
}
