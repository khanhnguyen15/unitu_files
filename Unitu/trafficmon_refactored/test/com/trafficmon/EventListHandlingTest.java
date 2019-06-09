package com.trafficmon;

import org.junit.Test;


import java.time.LocalTime;
import java.util.ArrayList;
import java.util.List;

import static org.hamcrest.core.Is.is;
import static org.junit.Assert.*;

public class EventListHandlingTest {
    private EventListHandling eventListHandling = new EventListHandling();

    private List<ZoneBoundaryCrossing> crossings = new ArrayList<>();

    private Vehicle vehicle = Vehicle.withRegistration("A123 XYZ");

    @Test
    public void checkNoEntryOrExit() {
        assertThat(crossings.size(), is(0));
    }

    @Test
    public void checkOrderOfEvent() {
        crossings.add(new EntryEvent(vehicle));
        crossings.add(new ExitEvent(vehicle));

        assertThat(eventListHandling.checkOrderingOf(crossings), is(true));

        crossings.add(new ExitEvent(vehicle));

        assertThat(eventListHandling.checkOrderingOf(crossings), is(false));
    }

    @Test
    public void offPeak() {
        crossings.add(new EntryEvent(vehicle, LocalTime.of(14,0)));
        crossings.add(new ExitEvent(vehicle, LocalTime.of(17,55)));

        assertThat(eventListHandling.calculateChargeForTimeInZone(crossings), is(4));
    }

    @Test
    public void peakHours() {
        crossings.add(new EntryEvent(vehicle, LocalTime.of(10,0)));
        crossings.add(new ExitEvent(vehicle, LocalTime.of(13,0)));

        assertThat(eventListHandling.calculateChargeForTimeInZone(crossings), is(6));
    }

    @Test
    public void longStayOffPeak() {
        crossings.add(new EntryEvent(vehicle, LocalTime.of(15,0)));
        crossings.add(new ExitEvent(vehicle, LocalTime.of(20,0)));

        assertThat(eventListHandling.calculateChargeForTimeInZone(crossings), is(12));
    }

    @Test
    public void longStayPeak() {
        crossings.add(new EntryEvent(vehicle, LocalTime.of(8,0)));
        crossings.add(new ExitEvent(vehicle, LocalTime.of(13,0)));

        assertThat(eventListHandling.calculateChargeForTimeInZone(crossings), is(12));
    }

    @Test
    public void twoStaysOffPeak() {
        crossings.add(new EntryEvent(vehicle, LocalTime.of(14,0)));
        crossings.add(new ExitEvent(vehicle, LocalTime.of(15,0)));

        crossings.add(new EntryEvent(vehicle, LocalTime.of(19,0)));
        crossings.add(new ExitEvent(vehicle, LocalTime.of(20,0)));

        assertThat(eventListHandling.calculateChargeForTimeInZone(crossings), is(8));
    }

    @Test
    public void twoStaysPeak() {
        crossings.add(new EntryEvent(vehicle, LocalTime.of(7,0)));
        crossings.add(new ExitEvent(vehicle, LocalTime.of(8,0)));

        crossings.add(new EntryEvent(vehicle, LocalTime.of(12,0)));
        crossings.add(new ExitEvent(vehicle, LocalTime.of(13,0)));

        assertThat(eventListHandling.calculateChargeForTimeInZone(crossings), is(12));
    }

    @Test
    public void peakAndOffPeak() {
        crossings.add(new EntryEvent(vehicle, LocalTime.of(7,0)));
        crossings.add(new ExitEvent(vehicle, LocalTime.of(8,0)));

        crossings.add(new EntryEvent(vehicle, LocalTime.of(14,0)));
        crossings.add(new ExitEvent(vehicle, LocalTime.of(15,0)));

        assertThat(eventListHandling.calculateChargeForTimeInZone(crossings), is(10));
    }

    @Test
    public void overFourHours() {
        crossings.add(new EntryEvent(vehicle, LocalTime.of(14,0)));
        crossings.add(new ExitEvent(vehicle, LocalTime.of(17,0)));

        crossings.add(new EntryEvent(vehicle, LocalTime.of(19,0)));
        crossings.add(new ExitEvent(vehicle, LocalTime.of(20,1)));

        assertThat(eventListHandling.calculateChargeForTimeInZone(crossings), is(12));
    }

    @Test
    public void cantPayMoreThanMaximumCharge() {
        crossings.add(new EntryEvent(vehicle, LocalTime.of(0,10)));
        crossings.add(new ExitEvent(vehicle, LocalTime.of(0,20)));

        crossings.add(new EntryEvent(vehicle, LocalTime.of(5,20)));
        crossings.add(new ExitEvent(vehicle, LocalTime.of(5,30)));

        crossings.add(new EntryEvent(vehicle, LocalTime.of(10,30)));
        crossings.add(new ExitEvent(vehicle, LocalTime.of(10,40)));

        crossings.add(new EntryEvent(vehicle, LocalTime.of(15,40)));
        crossings.add(new ExitEvent(vehicle, LocalTime.of(15,50)));

        assertThat(eventListHandling.calculateChargeForTimeInZone(crossings), is(12));
    }
}