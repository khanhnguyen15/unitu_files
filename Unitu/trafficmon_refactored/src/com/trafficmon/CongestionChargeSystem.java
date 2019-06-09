package com.trafficmon;

import java.math.BigDecimal;
import java.util.*;

public class CongestionChargeSystem {

    private EventListHandling eventListHandling = new EventListHandling();
    private OperationHandlingInterface operation = new OperationHandling();

    public CongestionChargeSystem() {

    }

    public CongestionChargeSystem(OperationHandlingInterface operation) {
        this.operation = operation;
    }

    public void vehicleEnteringZone(Vehicle vehicle, VehicleManagementInterface vehicleManagement) {
        vehicleManagement.add(new EntryEvent(vehicle));
    }

    public void vehicleLeavingZone(Vehicle vehicle, VehicleManagementInterface vehicleManagement) {
        if (!vehicleManagement.previouslyRegistered(vehicle)) {
            return;
        }
        vehicleManagement.add(new ExitEvent(vehicle));
    }

    public void calculateCharges(/*OperationHandlingInterface operation, */VehicleManagementInterface vehicleManagement) {

        for (Vehicle vehicle : vehicleManagement.vehicleSet()) {
            List<ZoneBoundaryCrossing> crossingsByVehicle = vehicleManagement.getEventByVehicle(vehicle);

            if (!eventListHandling.checkOrderingOf(crossingsByVehicle)) {
                operation.investigateInto(vehicle);
            } else {

                int fee = eventListHandling.calculateChargeForTimeInZone(crossingsByVehicle);
                BigDecimal charge = new BigDecimal(fee);
                operation.handlingCharge(vehicle, charge);
            }
        }
    }
}

