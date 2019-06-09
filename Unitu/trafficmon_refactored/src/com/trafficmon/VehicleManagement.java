package com.trafficmon;

import java.util.*;

public class VehicleManagement implements VehicleManagementInterface {

    private static VehicleManagement INSTANCE = new VehicleManagement();

    private final Map<Vehicle, List<ZoneBoundaryCrossing>> vehicleEventLog;

    private VehicleManagement() {

        this.vehicleEventLog = new HashMap<>();
    }

    @Override
    public void add(ZoneBoundaryCrossing event) {
        if (!previouslyRegistered(event.getVehicle())) {
            vehicleEventLog.put(event.getVehicle(), new ArrayList<>());
        }
        vehicleEventLog.get(event.getVehicle()).add(event);
    }

    @Override
    public boolean previouslyRegistered(Vehicle vehicle) {
        return vehicleEventLog.containsKey(vehicle);
    }

    @Override
    public int numVehicles() {
        return vehicleEventLog.size();
    }

    @Override
    public Set<Vehicle> vehicleSet() {
        return vehicleEventLog.keySet();
    }

    @Override
    public List<ZoneBoundaryCrossing> getEventByVehicle(Vehicle vehicle) {
        if (vehicleEventLog.get(vehicle) == null) {
            return new ArrayList<ZoneBoundaryCrossing>();
        }
        else {
            return vehicleEventLog.get(vehicle);
        }
    }

    @Override
    public void newDayReset() {
        vehicleEventLog.clear();
    }

    public static VehicleManagementInterface getInstance() {
        return  INSTANCE;
    }
}
