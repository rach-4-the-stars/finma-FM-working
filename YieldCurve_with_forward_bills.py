from curve_classes_and_functions import YieldCurve
from forward_bank_bill import Forward_bank_bill
from instrument_classes import Portfolio, Bank_bill, CashFlows, Bond
import numpy as np
import pandas as pd
class YieldCurve_with_forward_bills(YieldCurve):
    def __init__(self):
        super().__init__()

    def bootstrap(self):
        bank_bills = self.portfolio.get_bank_bills()
        forward_bank_bills = self.portfolio.get_forward_bank_bills()
        bonds = self.portfolio.get_bonds()
        
        self.add_zero_rate(0,0)
        for bank_bill in bank_bills:
            self.add_discount_factor(bank_bill.get_maturity(),bank_bill.get_price()/bank_bill.get_face_value())

        for bill in forward_bank_bills:
            # calculate the PV of the bond cashflows excluding the maturity cashflow 
            print("LOOK", self.maturities)  
            print(bill.get_maturity(), bill.get_start_date())
            
            self.add_discount_factor(bill.get_maturity(),(bill.get_price()/bill.get_face_value())*self.get_discount_factor(bill.get_start_date()))
        
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

if __name__ == "__main__":
    reference_portfolio = Portfolio()
    # regular 3-month bank bill
    reg_3_mo_bill = Bank_bill(face_value=100, maturity=.25, ytm=0.03, price=100)
    reg_3_mo_bill.set_ytm(0.03)
    reg_3_mo_bill.set_cash_flows()
    reference_portfolio.add_bank_bill(reg_3_mo_bill)

    # 3 forward bank bills
    for_bill_1 = Forward_bank_bill(start_date=0.25, face_value=100, maturity=.5, ytm=0.032, price=100)
    for_bill_1.set_ytm(0.032)
    for_bill_1.set_cash_flows()
    reference_portfolio.add_forward_bank_bill(for_bill_1)

    for_bill_2 = Forward_bank_bill(start_date=0.5, face_value=100, maturity=.75, ytm=0.034, price=100)
    for_bill_2.set_ytm(0.034)
    for_bill_2.set_cash_flows()
    reference_portfolio.add_forward_bank_bill(for_bill_2)

    for_bill_3 = Forward_bank_bill(start_date=0.7, face_value=100, maturity=1, ytm=0.036, price=100)
    for_bill_3.set_ytm(0.036)
    for_bill_3.set_cash_flows()
    reference_portfolio.add_forward_bank_bill(for_bill_3)

    # coupon bond
    coupon_bond = Bond(face_value=100, maturity=1, coupon=0.04, frequency=4, ytm=0.038, price=100)
    coupon_bond.set_ytm(0.038)
    coupon_bond.set_cash_flows()
    reference_portfolio.add_bond(coupon_bond)

    coupon_bond1 = Bond(face_value=100, maturity=2, coupon=0.045, frequency=1, ytm=0.042, price=100)
    coupon_bond1.set_ytm(0.042)
    coupon_bond1.set_cash_flows()
    reference_portfolio.add_bond(coupon_bond1)


    yield_curve = YieldCurve_with_forward_bills()
    yield_curve.set_constituent_portfolio(reference_portfolio)
    yield_curve.bootstrap()

curve_data = {
    'Maturity (years)': yield_curve.maturities,
    'Discount Factor': yield_curve.discount_factors,
    'Zero Rate (%)': [r * 100 for r in yield_curve.zero_rates]
}

df_curve = pd.DataFrame(curve_data)
print("\n=== Yield Curve Results ===")
print(df_curve.to_string(index=False))

# Also display the full curve details
print("\n=== Detailed Curve Information ===")
for i in range(len(yield_curve.maturities)):
    mat = yield_curve.maturities[i]
    df = yield_curve.discount_factors[i]
    zr = yield_curve.zero_rates[i]
    print(f"T = {mat:.2f} years: DF = {df:.6f}, Zero Rate = {zr*100:.4f}%")

test_cashflows = CashFlows()
test_cashflows.add_cash_flow(0.5, 25)
test_cashflows.add_cash_flow(1.0, 30)
test_cashflows.add_cash_flow(1.5, 35)
test_cashflows.add_cash_flow(2.0, 110)

print("Test cash flow schedule:")
for maturity, amount in test_cashflows.get_cash_flows():
    print(f"  T = {maturity:.2f} years: ${amount:.2f}")

npv = yield_curve.npv(test_cashflows)

print(f"\n=== NPV Calculation ===")
print(f"Total NPV = ${npv:.4f}")

# Show the detailed calculation
print("\nDetailed breakdown:")
total_pv = 0
for maturity, amount in test_cashflows.get_cash_flows():
    df = yield_curve.get_discount_factor(maturity)
    pv = amount * df
    total_pv += pv
    print(f"  T = {maturity:.2f}: ${amount:.2f} × {df:.6f} = ${pv:.4f}")

print(f"\nTotal: ${total_pv:.4f}")

# Note: The 1.5 year cash flow requires interpolation
print(f"\nNote: The discount factor at T=1.5 years was interpolated (not a direct maturity point)")
print(f"Interpolated DF(1.5) = {yield_curve.get_discount_factor(1.5):.6f}")