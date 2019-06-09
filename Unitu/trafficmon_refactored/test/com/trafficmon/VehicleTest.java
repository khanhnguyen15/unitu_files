package com.trafficmon;

import org.junit.Test;

import static org.hamcrest.CoreMatchers.is;
import static org.junit.Assert.*;

public class VehicleTest {
    Vehicle vehicle = Vehicle.withRegistration("ABC");

    @Test
    public void sameVehicles() {
        assertThat(vehicle.equals(vehicle), is(true));
    }

    @Test
            public void similarVehicles() {
        Vehicle sameVehicle = Vehicle.withRegistration("ABC");
        assertThat(vehicle.equals(sameVehicle), is(true));
    }

    @Test
            public void differentVehicles() {
        Object differentTypeVehicle = new Object();
        assertThat(vehicle.equals(differentTypeVehicle), is(false));

        Vehicle differentVehicle = Vehicle.withRegistration("ACB");
        assertThat(vehicle.equals(differentVehicle), is(false));
    }
}