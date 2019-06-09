package com.trafficmon;

import java.math.BigDecimal;

public interface OperationHandlingInterface {
    void handlingCharge(Vehicle vehicle, BigDecimal charge);

    void investigateInto(Vehicle vehicle);
}
