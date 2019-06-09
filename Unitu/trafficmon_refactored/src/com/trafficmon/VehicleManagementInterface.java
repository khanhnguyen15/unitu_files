package com.trafficmon;

import java.util.List;
import java.util.Set;

public interface VehicleManagementInterface {
    void add(ZoneBoundaryCrossing event);

    boolean previouslyRegistered(Vehicle vehicle);

    int numVehicles();

    Set<Vehicle> vehicleSet();

    List<ZoneBoundaryCrossing> getEventByVehicle(Vehicle vehicle);

    void newDayReset();
}
