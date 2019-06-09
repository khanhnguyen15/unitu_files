package com.trafficmon;


import java.time.LocalTime;

public abstract class ZoneBoundaryCrossing {

    private final Vehicle vehicle;
    private final LocalTime time;

    public ZoneBoundaryCrossing(Vehicle vehicle, LocalTime time) {
        this.vehicle = vehicle;
        this.time = time;
    }

    public ZoneBoundaryCrossing(Vehicle vehicle) {
        this.vehicle = vehicle;
        this.time = LocalTime.now();
    }


    public Vehicle getVehicle() {
        return vehicle;
    }

    public LocalTime timestamp() {
        return time;
    }
}
