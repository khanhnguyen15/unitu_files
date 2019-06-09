package com.trafficmon;

import java.time.LocalTime;
import java.time.temporal.ChronoUnit;
import java.util.List;

public class EventListHandling {


    private static final int OFF_PEAK_CHARGE = 4;
    private static final int PEAK_CHARGE = 6;
    private static final int MAX_CHARGE = 12;
    private static final int TOTAL_HOURS_STAY = 4;
    private static final int HOURS_GAP = 4;
    private static final int END_OF_PEEK_HOUR = 14;


   public int calculateChargeForTimeInZone(List<ZoneBoundaryCrossing> crossings) {

        int charge = 0;
        int minutesInZone = 0;

        ZoneBoundaryCrossing lastEvent = crossings.get(0);
        LocalTime lastPaid = LocalTime.now();

        for (ZoneBoundaryCrossing crossing : crossings.subList(1, crossings.size())) {

            if (crossing instanceof ExitEvent) {
                LocalTime entranceTime = lastEvent.timestamp();
                LocalTime exitTime = crossing.timestamp();

                minutesInZone += entranceTime.until(exitTime, ChronoUnit.MINUTES);
                if (minutesInZone > TOTAL_HOURS_STAY * 60)
                {
                    return MAX_CHARGE;
                }
                if (charge == 0)
                {
                    charge += getCharge(entranceTime);
                    lastPaid = entranceTime;
                }
                else if (lastPaid.until(entranceTime, ChronoUnit.HOURS) >= HOURS_GAP)
                    {

                        charge += getCharge(entranceTime);
                        lastPaid = entranceTime;
                    }
                }
            lastEvent = crossing;
        }
        if (charge > MAX_CHARGE)
        {
            return MAX_CHARGE;
        }

        return charge;
    }


    private int getCharge(LocalTime entranceTime) {
        return chargeByEntranceHour(entranceTime.getHour());
    }

    private int chargeByEntranceHour(int entranceHour)
    {
        if (entranceHour < END_OF_PEEK_HOUR)
        {
            return PEAK_CHARGE;
        }
        else
        {
            return OFF_PEAK_CHARGE;
        }

    }



    public boolean checkOrderingOf(List<ZoneBoundaryCrossing> crossings) {

        ZoneBoundaryCrossing lastEvent = crossings.get(0);

        for (ZoneBoundaryCrossing crossing : crossings.subList(1, crossings.size())) {

            if (crossing.timestamp().compareTo(lastEvent.timestamp()) < 0) {
                return false;
            }
            if (crossing instanceof EntryEvent && lastEvent instanceof EntryEvent) {
                return false;
            }
            if (crossing instanceof ExitEvent && lastEvent instanceof ExitEvent) {
                return false;
            }
            lastEvent = crossing;
        }

        return true;
    }

}
