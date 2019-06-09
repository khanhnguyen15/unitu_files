package com.trafficmon;

public class Example {
    public static void main(String[] args) throws Exception {

        VehicleManagementInterface vehicleManagement = VehicleManagement.getInstance();

        CongestionChargeSystem congestionChargeSystem = new CongestionChargeSystem(new OperationHandling());
        congestionChargeSystem.vehicleEnteringZone(Vehicle.withRegistration("A123 XYZ"), vehicleManagement);
        delaySeconds(1);
        congestionChargeSystem.vehicleEnteringZone(Vehicle.withRegistration("J091 4PY"), vehicleManagement);
        delaySeconds(1);
        congestionChargeSystem.vehicleLeavingZone(Vehicle.withRegistration("A123 XYZ"), vehicleManagement);
        delaySeconds(1);
        congestionChargeSystem.vehicleLeavingZone(Vehicle.withRegistration("J091 4PY"), vehicleManagement);
        congestionChargeSystem.calculateCharges(vehicleManagement);
    }

    private static void delaySeconds(int secs) throws InterruptedException {
        Thread.sleep(secs * 1000);
    } }