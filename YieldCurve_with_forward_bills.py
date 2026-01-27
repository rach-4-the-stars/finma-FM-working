from curve_classes_and_functions import YieldCurve
from forward_bank_bill import Forward_bank_bill
import numpy as np
import pandas as pd
class YieldCurve_with_forward_bills(YieldCurve):
    def __init__():
        pass

    def bootstrap(self):
        bank_bills = self.portfolio.get_bank_bills()
        bonds = self.portfolio.get_bonds()
        self.add_zero_rate(0,0)
        for bank_bill in bank_bills:
            self.add_discount_factor(bank_bill.get_maturity(),bank_bill.get_price()/bank_bill.get_face_value())
        
        for bond in bonds:
            # calculate the PV of the bond cashflows excluding the maturity cashflow
            pv = 0
            bond_dates = bond.get_maturities()
            bond_amounts = bond.get_amounts()
            for i in range(1, len(bond_amounts)-1):
                pv += bond_amounts[i]*self.get_discount_factor(bond_dates[i])
            # print("PV of all the cashflows except maturity is: ", pv)
            # print("The bond price is: ", bond.get_price())
            # print("The last cashflow is: ", bond_amounts[-1])
            self.add_discount_factor(bond.get_maturity(),(bond.get_price()-pv)/bond.get_amounts()[-1])
