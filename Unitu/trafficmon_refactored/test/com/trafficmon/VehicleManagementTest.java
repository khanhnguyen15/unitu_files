package com.trafficmon;

import org.junit.Rule;
import org.junit.Test;
import org.junit.rules.ExpectedException;

import static org.hamcrest.CoreMatchers.is;
import static org.junit.Assert.*;

public class VehicleManagementTest {

    @Rule

    public ExpectedException exception = ExpectedException.none();



    VehicleManagementInterface vehicleManagement = VehicleManagement.getInstance();
    Vehicle vehicle1 = Vehicle.withRegistration("NEW WORLD");
    Vehicle vehicle2 = Vehicle.withRegistration("NO 007");
    Vehicle vehicle3 = Vehicle.withRegistration("NOT APPEAR");



    @Test
    public void checkEmptyMap() {
        VehicleManagement.getInstance().newDayReset();
        assertThat(vehicleManagement.numVehicles(), is(0));
        assertThat(vehicleManagement.previouslyRegistered(vehicle1), is(false));
    }

    @Test
    public void addNewEvents() {
        vehicleManagement.newDayReset();
        getAdd(vehicle1);
        getAdd(vehicle2);
        getAdd();
        assertThat(vehicleManagement.numVehicles(), is(2));
        assertThat(vehicleManagement.previouslyRegistered(vehicle1), is(true));
    }

    @Test
    public void addMoreNewEvents(){
        vehicleManagement.newDayReset();
        getAdd(vehicle1);
        getAdd(vehicle2);
        getAdd(vehicle3);
        getAdd();
        assertThat(vehicleManagement.numVehicles(), is(3));
        assertThat(vehicleManagement.previouslyRegistered(vehicle2), is(true));
    }

    private void getAdd(Vehicle vehicle1) {
        vehicleManagement.add(new EntryEvent(vehicle1));
    }

    private void getAdd() {
        vehicleManagement.add(new ExitEvent(vehicle1));
    }

    @Test
    public void retrieveVehicleSet() {
        assertThat(vehicleManagement.vehicleSet().size(), is(2));
        assertThat(vehicleManagement.vehicleSet().contains(vehicle1), is(true));
        assertThat(vehicleManagement.vehicleSet().contains(vehicle2), is(true));
        assertThat(vehicleManagement.vehicleSet().contains(vehicle3), is(false));
    }

    @Test
    public void retrieveEventsByVehicle() {
        assertThat(vehicleManagement.getEventByVehicle(vehicle1).size(), is(2));
        assertThat(vehicleManagement.getEventByVehicle(vehicle2).size(), is(1));
        assertThat(vehicleManagement.getEventByVehicle(vehicle3).size(), is(0));
    }

    @Test
    public void appliedByOtherClasses() {
        getAdd(vehicle1);
        getAdd(vehicle2);
        getAdd();
        getAdd(vehicle2);
        getAdd(vehicle1);
        EventListHandling eventHandling = new EventListHandling();
        assertThat(eventHandling.checkOrderingOf(vehicleManagement.getEventByVehicle(vehicle1)), is(true));
        assertThat(eventHandling.checkOrderingOf(vehicleManagement.getEventByVehicle(vehicle2)), is(false));
    }
}