package com.spiderdp.dashboardapp;

import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.text.method.ScrollingMovementMethod;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

public class LogFragment extends Fragment{

	private View view;
	
	@Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View rootView = inflater.inflate(R.layout.log_fragment, container, false);
        view = rootView;
		TextView textView = (TextView) view.findViewById(R.id.log_text_view);
		textView.setMovementMethod(new ScrollingMovementMethod());
        return rootView;
    }
	
	public void addLine(String line){
		if(view == null) return;
		TextView textView = (TextView) view.findViewById(R.id.log_text_view);
		
		
		
		String text = line +"\n" + textView.getText() + "";
		String[] lines = text.split("\n");
		
		int max;
		
		if(lines.length > 50){
			max = 49;
		}
		else{
			max = lines.length;
		}
		String newString = "";
		for(int i = 0; i < max; i++){
		 newString+= lines[i] +"\n";
		}
		
		textView.setText(newString );
		
	}
	
}
