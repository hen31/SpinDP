package com.spiderdp.dashboardapp;

import android.support.v4.app.FragmentPagerAdapter;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;

public class PagerAdapter extends FragmentPagerAdapter {
	public static HellingsHoekFragment hellingsHoek = new HellingsHoekFragment();
	public static AccuSpanningFragment accuSpanning = new AccuSpanningFragment();
	public static LogFragment log = new LogFragment();
	public static LivestreamFragment livestream = new LivestreamFragment();
	
    public PagerAdapter(FragmentManager fm) {
        super(fm);
    }

    @Override
    public Fragment getItem(int index) {
 
        switch (index) {
        case 0:
            return PagerAdapter.hellingsHoek;
        case 1:
            return PagerAdapter.accuSpanning;
        case 2:
            return PagerAdapter.log;
        case 3:
        	return PagerAdapter.livestream;
        }
 
        return null;
    }
 
    @Override
    public int getCount() {
        // get item count - equal to number of tabs
        return 4;
    }
}