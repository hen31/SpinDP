package com.spiderdp.dashboardapp;

import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.webkit.WebSettings.LayoutAlgorithm;
import android.webkit.WebView;

public class LivestreamFragment extends Fragment {
	
	View view;
	
	@Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View rootView = inflater.inflate(R.layout.livestream_fragment, container, false);
        view = rootView;

        WebView webView = (WebView) view.findViewById(R.id.webView);
        webView.getSettings().setLayoutAlgorithm(LayoutAlgorithm.SINGLE_COLUMN);
        webView.setInitialScale(200);
        webView.loadUrl("http://192.168.10.1:8080/stream_simple.html");  
        
        return rootView;
    }
}
