from instrument_classes import Bank_bill, Bond, Portfolio
from curve_classes_and_functions import ZeroCurve, YieldCurve
import pandas as pd
import copy
if __name__ == "__main__":
    reference_portfolio = Portfolio()
    # regular 3-month bank bill
    reg_3_mo_bill = Bank_bill(face_value=100, maturity=.25, ytm=0.03, price=100)
    reg_3_mo_bill.set_ytm(0.03)
    reg_3_mo_bill.set_cash_flows()
    reference_portfolio.add_bank_bill(reg_3_mo_bill)

     # regular 6-month bank bill
    reg_6_mo_bill = Bank_bill(face_value=100, maturity=.5, ytm=0.03, price=100)
    reg_6_mo_bill.set_ytm(0.03)
    reg_6_mo_bill.set_cash_flows()
    reference_portfolio.add_bank_bill(reg_6_mo_bill)

    # coupon bond
    coupon_bond = Bond(face_value=100, maturity=1, coupon=0.04, frequency=4, ytm=0.038, price=100)
    coupon_bond.set_ytm(0.038)
    coupon_bond.set_cash_flows()
    reference_portfolio.add_bond(coupon_bond)

    coupon_bond1 = Bond(face_value=100, maturity=2, coupon=0.045, frequency=1, ytm=0.042, price=100)
    coupon_bond1.set_ytm(0.042)
    coupon_bond1.set_cash_flows()
    reference_portfolio.add_bond(coupon_bond1)


    yield_curve = YieldCurve()
    yield_curve.set_constituent_portfolio(reference_portfolio)
    yield_curve.bootstrap()

    # Create a bond position to hedge
    position = Bond()
    position.set_face_value(1000)
    position.set_maturity(2.5)
    position.set_coupon(0.05)
    position.set_frequency(2)
    position.set_ytm(0.045)
    position.set_cash_flows()

    position_npv = yield_curve.npv(position)
    print(f"Position NPV: ${position_npv:.2f}")

    print("\nBootstrapped Yield Curve:")
    print("="*50)
    maturities, discount_factors = yield_curve.get_zero_curve()
    for mat, df in zip(maturities, discount_factors):
        zero_rate = yield_curve.get_zero_rate(mat)
        print(f"Maturity: {mat:5.2f} years | Zero Rate: {zero_rate:6.2%} | DF: {df:.6f}")
    
    print("\nPosition to Hedge:")
    print("="*50)
    print(f"Cash Flow Amount: ${position.get_amounts()[0]:.2f}")
    print(f"Cash Flow Maturity: {position.get_maturities()[0]} years")
    print(f"NPV (using yield curve): ${position_npv:.2f}")
    print(f"Discount Factor at 3Y: {yield_curve.get_discount_factor(3.0):.6f}")

# Create a new class that extends YieldCurve
class YieldCurveWithHedge(YieldCurve):
    """
    Extends YieldCurve to add hedging capabilities.
    """
    
    def calculate_hedge(self, position, bump_size=0.0001, position_npv=0):
        """
        Calculate hedge positions for a given position.
        
        Your implementation here.
        """
        # copy
        copy_bill = position.copy.deepcopy()
        # bump ytm
        copy_bill.set_ytm(copy_bill.get_ytm() + bump_size)
        # # recalc cash flows
        # copy_bill.set_cash_flows()
        # # npv calc
        # copy_bill_npv = self.npv(copy_bill)
        # print(f"Copy bill NPV: ${copy_bill_npv:.2f}")
        # # delta npv
        # delta_npv = copy_bill_npv - position_npv



# Your implementation here: