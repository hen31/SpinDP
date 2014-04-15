package com.spiderdp.spidercontroller;

import java.util.ArrayList;

import android.app.Activity;
import android.app.ActionBar;
import android.app.Fragment;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.View.OnTouchListener;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.RelativeLayout;
import android.os.Build;

public class MainActivity extends Activity {
	RelativeLayout layout_joystick_left;
	RelativeLayout layout_joystick_right;
	Button exitBtn;
	JoyStickClass js;
	JoyStickClass js_right;
	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);

		if (savedInstanceState == null) {
			getFragmentManager().beginTransaction()
					.add(R.id.container, new PlaceholderFragment()).commit();
		}
	
		exitBtn = (Button)findViewById(R.id.button3);
		exitBtn.setOnClickListener(new OnClickListener() {

			@Override
			public void onClick(View v) {
				ServerClient.getInstance().sendMessage(ServerClient.KILL, null);
				
			}
		
		});

		
		
		layout_joystick_left = (RelativeLayout)findViewById(R.id.leftJoystick);
		layout_joystick_right = (RelativeLayout)findViewById(R.id.rightJoystick);
		
        js = new JoyStickClass(getApplicationContext()
        		, layout_joystick_left, R.drawable.image_button);
	    js.setStickSize(150, 150);
	    js.setLayoutSize(500, 500);
	    js.setLayoutAlpha(150);
	    js.setStickAlpha(100);
	    js.setOffset(90);
	    js.setMinimumDistance(50);	
	    layout_joystick_left.setOnTouchListener(new OnTouchListener() {
	 			public boolean onTouch(View arg0, 	android.view.MotionEvent arg1) {
	 				js.drawStick(arg1);
	 				return true;
	 			}
	    });
	    
	    
	    
	   
	    js_right = new JoyStickClass(getApplicationContext()
        		, layout_joystick_right, R.drawable.image_button);
	    js_right.setStickSize(150, 150);
	    js_right.setLayoutSize(500, 500);
	    js_right.setLayoutAlpha(150);
	    js_right.setStickAlpha(100);
	    js_right.setOffset(90);
	    js_right.setMinimumDistance(50);	
	    layout_joystick_right.setOnTouchListener(new OnTouchListener() {
	 			public boolean onTouch(View arg0, 	android.view.MotionEvent arg1) {
	 				js_right.drawStick(arg1);
	 				return true;
	 			}
	    });
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {

		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.main, menu);
		return true;
	}

	@Override
	public boolean onOptionsItemSelected(MenuItem item) {
		// Handle action bar item clicks here. The action bar will
		// automatically handle clicks on the Home/Up button, so long
		// as you specify a parent activity in AndroidManifest.xml.
		int id = item.getItemId();
		if (id == R.id.action_settings) {
			ServerClient.getInstance(this);
		}
		return super.onOptionsItemSelected(item);
	}

	/**
	 * A placeholder fragment containing a simple view.
	 */
	public static class PlaceholderFragment extends Fragment {

		public PlaceholderFragment() {
		}

		@Override
		public View onCreateView(LayoutInflater inflater, ViewGroup container,
				Bundle savedInstanceState) {
			View rootView = inflater.inflate(R.layout.fragment_main, container,
					false);
			return rootView;
		}
	}

}
