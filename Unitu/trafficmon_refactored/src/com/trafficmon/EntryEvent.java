package com.trafficmon;

import java.time.LocalTime;

public class EntryEvent extends ZoneBoundaryCrossing {
    public EntryEvent(Vehicle vehicle) { super(vehicle); }
    public EntryEvent(Vehicle vehicle, LocalTime time) { super(vehicle, time);}
}
