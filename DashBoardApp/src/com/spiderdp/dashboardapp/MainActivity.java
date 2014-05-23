package com.spiderdp.dashboardapp;

import java.util.Timer;
import java.util.TimerTask;

import android.os.Bundle;
import android.app.ActionBar;
import android.app.FragmentTransaction;
import android.app.ActionBar.Tab;
import android.support.v4.app.FragmentActivity;
import android.support.v4.view.ViewPager;
import android.view.Menu;
import android.view.MenuItem;

public class MainActivity extends FragmentActivity implements ActionBar.TabListener {
	static public Boolean connected = false;
	private ViewPager viewPager;
	private PagerAdapter mAdapter;
	private ActionBar actionBar;
	private String[] tabs = { "Hellings hoek", "Accu spanning", "Log", "Livestream" };

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		
		// Initilization
        viewPager = (ViewPager) findViewById(R.id.pager);
        actionBar = getActionBar();
        mAdapter = new PagerAdapter(getSupportFragmentManager());
 
        viewPager.setAdapter(mAdapter);
        actionBar.setHomeButtonEnabled(false);
        actionBar.setNavigationMode(ActionBar.NAVIGATION_MODE_TABS);        
        
        // Adding Tabs
        for (String tab_name : tabs) {
            actionBar.addTab(
            		actionBar.newTab()
            		.setText(tab_name)
                    .setTabListener(this));
        }
        
        viewPager.setOnPageChangeListener(new ViewPager.OnPageChangeListener(){
	        @Override
	        public void onPageSelected(int position) {
	        	// on changing the page
	        	// make respected tab selected
	        	actionBar.setSelectedNavigationItem(position);
	        }
	        
	        @Override
	        public void onPageScrolled(int arg0, float arg1, int arg2) {
	        	
	        }
	        
	        @Override
	        public void onPageScrollStateChanged(int arg0) {
	        
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
		switch (item.getItemId()) {
		case R.id.menu_connect:
			ServerClient.getInstance(this);
			
			Timer timer = new Timer();
			timer.schedule(new TimerTask(){
				
				@Override
				public void run(){
					MainActivity.getData();
				}
				
			}, 5000, 5000);
			
			return true;

		case R.id.menu_get_data:
			if (connected){
				getData();
			}
			return true;
		default:
			return true;
		}
	}
	
	public static void getData(){
		if(!MainActivity.connected){
			return;
		}
		
		ServerClient.getInstance().sendMessage(
				ServerClient.SEND_SENSOR_DATA, null);
		ServerClient.getInstance().sendMessage(
						ServerClient.SEND_ACCU_DATA, null);
	}

	@Override
	public void onTabReselected(Tab tab, FragmentTransaction ft) {
		// TODO Auto-generated method stub

	}

	@Override
	public void onTabSelected(Tab tab, FragmentTransaction ft) {
		viewPager.setCurrentItem(tab.getPosition());

	}

	@Override
	public void onTabUnselected(Tab tab, FragmentTransaction ft) {
		// TODO Auto-generated method stub

	}

}
