from instrument_classes import Bond
import pandas as pd

class CorporateBond(Bond):
    def __init__(self):
        super().__init__()
        self.credit_spread = 0.0
        self.reference_bond = None
    
    def set_credit_spread(self, spread):
        self.credit_spread = spread
    
    def set_reference_bond(self, bond):
        self.reference_bond = bond

    def get_credit_spread(self):
        return self.credit_spread
    
    def get_reference_bond(self):
        return self.reference_bond 

    def set_ytm(self):
        """Calculate corporate bond YTM as reference bond YTM + credit spread"""
        calculated_ytm = self.reference_bond.get_ytm() + self.credit_spread
        super().set_ytm(calculated_ytm)
        

if __name__ == "__main__":
    # Create a 2-year government bond
    gov_bond_2y = Bond()
    gov_bond_2y.set_face_value(100)
    gov_bond_2y.set_maturity(2)
    gov_bond_2y.set_coupon(0.03)  # 3% coupon
    gov_bond_2y.set_frequency(2)  # semi-annual
    gov_bond_2y.set_ytm(0.03)     # 3% yield
    gov_bond_2y.set_cash_flows()

    # # Create a 5-year government bond
    # gov_bond_5y = Bond()
    # gov_bond_5y.set_face_value(100)
    # gov_bond_5y.set_maturity(5)
    # gov_bond_5y.set_coupon(0.03)  # 3% coupon
    # gov_bond_5y.set_frequency(2)  # semi-annual
    # gov_bond_5y.set_ytm(0.03)     # 3% yield
    # gov_bond_5y.set_cash_flows()

    # # Create a 10-year government bond
    # gov_bond_10y = Bond()
    # gov_bond_10y.set_face_value(100)
    # gov_bond_10y.set_maturity(5)
    # gov_bond_10y.set_coupon(0.03)  # 3% coupon
    # gov_bond_10y.set_frequency(2)  # semi-annual
    # gov_bond_10y.set_ytm(0.03)     # 3% yield
    # gov_bond_10y.set_cash_flows()

    # Create a corporate bond
    corp_bond_2y = CorporateBond()
    corp_bond_2y.set_face_value(100)
    corp_bond_2y.set_maturity(2)
    corp_bond_2y.set_coupon(0.03)  # Same coupon as government bond
    corp_bond_2y.set_frequency(2)
    corp_bond_2y.set_reference_bond(gov_bond_2y)
    corp_bond_2y.set_credit_spread(0.015)  # 150 basis points
    corp_bond_2y.set_ytm()  # This should calculate: 0.03 + 0.015 = 0.045
    corp_bond_2y.set_cash_flows()

    print("Gov bond 2y ytm:", gov_bond_2y.get_ytm())
    print("Credit spread:", corp_bond_2y.get_credit_spread())
    print("Corp bond ytm:", corp_bond_2y.get_ytm())
    print("Corp bond price:", corp_bond_2y.get_price())