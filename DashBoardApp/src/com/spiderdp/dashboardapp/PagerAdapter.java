package com.spiderdp.dashboardapp;

import android.support.v4.app.FragmentPagerAdapter;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;

public class PagerAdapter extends FragmentPagerAdapter {
	public static HellingsHoekFragment hellingsHoek = new HellingsHoekFragment();
	public static AccuSpanningFragment accuSpanning = new AccuSpanningFragment();
	public static LogFragment log = new LogFragment();
	
    public PagerAdapter(FragmentManager fm) {
        super(fm);
    }

    @Override
    public Fragment getItem(int index) {
 
        switch (index) {
        case 0:
            // Top Rated fragment activity
            return PagerAdapter.hellingsHoek;
        case 1:
            // Games fragment activity
            return PagerAdapter.accuSpanning;
        case 2:
            // Movies fragment activity
            return PagerAdapter.log;
        }
 
        return null;
    }
 
    @Override
    public int getCount() {
        // get item count - equal to number of tabs
        return 3;
    }
}