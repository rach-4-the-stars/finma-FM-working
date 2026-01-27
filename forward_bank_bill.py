from instrument_classes import Bank_bill, Bond, Portfolio, CashFlows
from curve_classes_and_functions import YieldCurve
import numpy as np
import pandas as pd

class Forward_bank_bill(Bank_bill):
    def __init__(self, start_date=0, face_value=100, maturity=3, coupon=0, frequency=4, ytm=0, price=100):
        super().__init__()
        self.start_date = start_date

    def set_start_date(self, start_date):
        self.start_date = start_date
    
    def get_start_date(self):
        return self.start_date
    
    def get_forward_period(self):
        return self.maturity - self.start_date

    def set_cash_flows(self):
        self.add_cash_flow(self.start_date, -self.price)
        self.add_cash_flow(self.maturity, self.face_value)

if __name__ == "__main__":
    # A 3-month bill starting in 6 months (6x9 forward)
    fwd_bill = Forward_bank_bill(face_value=100, start_date=0.5, maturity=0.75)
    fwd_bill.set_ytm(0.04)  # 4% forward rate
    fwd_bill.set_cash_flows()
    print(fwd_bill.get_cash_flows())