package com.trafficmon;

import org.jmock.Expectations;
import org.jmock.integration.junit4.JUnitRuleMockery;
import org.junit.Rule;
import org.junit.Test;

import java.math.BigDecimal;

public class CongestionChargeSystemTest {

    @Rule
    public JUnitRuleMockery context = new JUnitRuleMockery();

    private  OperationHandlingInterface operation = context.mock(OperationHandlingInterface.class);
    private VehicleManagementInterface eventManagement = context.mock(VehicleManagementInterface.class);

    private final CongestionChargeSystem congestionChargeSystem = new CongestionChargeSystem(operation);

    private Vehicle vehicle = Vehicle.withRegistration("A123 XYZ");


    @Test
    public void addEnteringVehicle() {
        context.checking(new Expectations() {{
            exactly(1).of(eventManagement).add(with(any(EntryEvent.class)));
        }});

        congestionChargeSystem.vehicleEnteringZone(vehicle, eventManagement);
    }

    @Test
    public void addExitingVehicleWhichIsNotRegistered() {
        context.checking(new Expectations() {{
            exactly(1).of(eventManagement).previouslyRegistered(vehicle); will(returnValue(false));
            never(eventManagement).add(with(any(ExitEvent.class)));
        }});

        congestionChargeSystem.vehicleLeavingZone(vehicle, eventManagement);
    }

    @Test
    public void addExitingVehicle() {
        context.checking(new Expectations() {{
            ignoring(eventManagement).add(with(any(EntryEvent.class)));
            exactly(1).of(eventManagement).previouslyRegistered(vehicle); will(returnValue(true));
            exactly(1).of(eventManagement).add(with(any(ExitEvent.class)));
        }});

        congestionChargeSystem.vehicleEnteringZone(vehicle, eventManagement);
        congestionChargeSystem.vehicleLeavingZone(vehicle, eventManagement);
    }

    @Test
    public void operationalChargeHandling() {
        VehicleManagement.getInstance().newDayReset();
        context.checking(new Expectations() {{
            exactly(1).of(operation).handlingCharge(with(equal(vehicle)), with(any(BigDecimal.class)));
        }});

        congestionChargeSystem.vehicleEnteringZone(vehicle, VehicleManagement.getInstance());
        congestionChargeSystem.vehicleLeavingZone(vehicle, VehicleManagement.getInstance());
        congestionChargeSystem.calculateCharges(VehicleManagement.getInstance());
    }

    @Test
    public void operationInvestigateHandling() {
        context.checking(new Expectations() {{
            exactly(1).of(operation).investigateInto(with(equal(vehicle)));
        }});


        congestionChargeSystem.vehicleEnteringZone(vehicle, VehicleManagement.getInstance());
        congestionChargeSystem.vehicleEnteringZone(vehicle, VehicleManagement.getInstance());
        congestionChargeSystem.calculateCharges(VehicleManagement.getInstance());
    }

}