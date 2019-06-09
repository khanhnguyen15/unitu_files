package com.trafficmon;

import org.junit.Test;

import static org.hamcrest.CoreMatchers.is;
import static org.junit.Assert.*;

public class ZoneBoundaryCrossingTest {
    Vehicle vehicle = Vehicle.withRegistration("");

    ZoneBoundaryCrossing entry = new EntryEvent(vehicle);
    ZoneBoundaryCrossing exit = new ExitEvent(vehicle);

    @Test
    public void returnVehicle() {
        assertThat(entry.getVehicle(), is(vehicle));
        assertThat(exit.getVehicle(), is(vehicle));
    }
}