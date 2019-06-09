package com.trafficmon;

import java.math.BigDecimal;

public class OperationHandling implements OperationHandlingInterface {

    private static OperationHandling INSTANCE = new OperationHandling();

    private OperationHandling() {}

    @Override
    public void handlingCharge(Vehicle vehicle, BigDecimal charge) {
        try {
            RegisteredCustomerAccountsService.getInstance().accountFor(vehicle).deduct(charge);
        } catch (InsufficientCreditException ice) {
            OperationsTeam.getInstance().issuePenaltyNotice(vehicle, charge);
        } catch (AccountNotRegisteredException e) {
            OperationsTeam.getInstance().issuePenaltyNotice(vehicle, charge);
        }
    }

    @Override
    public void investigateInto(Vehicle vehicle) {
        OperationsTeam.getInstance().triggerInvestigationInto(vehicle);
    }

    public static OperationHandlingInterface getInstance() {
        return INSTANCE;
    }
}
