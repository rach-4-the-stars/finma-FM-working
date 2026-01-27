# OOP
- encapsulated (self-contained)
- attributes
- methods

## Blueprint for object
```class CashFlows:
    def __init__(self):
        self.maturities = []  # An attribute to store when cash flows occur
        self.amounts = []     # An attribute to store the cash flow amounts
    
    def add_cash_flow(self, maturity, amount):
        """Add a cash flow to the cash flow list."""
        self.maturities.append(maturity)
        self.amounts.append(amount)
    
    def get_cash_flow(self, maturity):
        """Get the cash flow amount for a specific maturity."""
        if maturity in self.maturities:
            return self.amounts[self.maturities.index(maturity)]
        else:
            return None
    
    def get_maturities(self):
        """Return a list of all maturities."""
        return list(self.maturities)
    
    def get_amounts(self):
        """Return a list of all cash flow amounts."""
        return list(self.amounts)
    
    def get_cash_flows(self):
        """Return all cash flows as (maturity, amount) pairs."""
        return list(zip(self.maturities, self.amounts))
```
Using dict

``` class CashFlows:
    def __init__(self):
        self.cash_flows = {} # an attribute to store maturities mapped to amounts
    
    def add_cash_flow(self, maturity, amount):
        """Add a cash flow to the cash flow list."""
        self.cash_flows[maturity] = amount
    
    def get_cash_flow(self, maturity):
        """Get the cash flow amount for a specific maturity."""
        return self.cash_flows.get(maturity)
    
    def get_maturities(self):
        """Return a list of all maturities."""
        return list(self.cash_flows.keys())
    
    def get_amounts(self):
        """Return a list of all cash flow amounts."""
        return list(self.cash_flows.values())
    
    def get_cash_flows(self):
        """Return all cash flows as (maturity, amount) pairs."""
        return self.cash_flows
    
    # Create a CashFlows object
my_cash_flows = CashFlows()

# Add some cash flows (e.g., initial investment and future payments)
my_cash_flows.add_cash_flow(0, -100)      # Pay $100 today
my_cash_flows.add_cash_flow(0.5, 5)       # Receive $5 in 6 months
my_cash_flows.add_cash_flow(1.0, 105)     # Receive $105 in 1 year

# Access the data using methods
print("All maturities:", my_cash_flows.get_maturities())
print("All amounts:", my_cash_flows.get_amounts())
print("\nCash flow at time 1.0:", my_cash_flows.get_cash_flow(1.0))
print("\nAll cash flows as pairs:", my_cash_flows.get_cash_flows())
```

# Zero curve
- Used to calculate present value of cash flow
    - *zero rates*: interest rates for zero coupon bonds of different maturities
    - *discount factors*: present values of 1 unit of currency paid at future dates
    - *exponential interpolation*: A method for estimating rates between known points on the curve
    - *Amount at Maturity (AtMat)*: Future value based on zero rates
Dependencies
``` import math
import numpy as np
import importlib
import pandas as pd
import tabulate as tb
```


NOTE: requires cash flow class
``` class ZeroCurve:
    def __init__(self):
        # set up empty lists to store the curve data
        self.maturities = []
        self.zero_rates = []
        self.AtMats = []
        self.discount_factors = []
    
    def add_zero_rate(self, maturity, zero_rate):
        """Add a zero rate to the curve and calculate corresponding discount factor and AtMat"""
        self.maturities.append(maturity)
        self.zero_rates.append(zero_rate)
        self.AtMats.append(math.exp(zero_rate*maturity))
        self.discount_factors.append(1/self.AtMats[-1])

    def add_discount_factor(self, maturity, discount_factor):
        """Add a discount factor to the curve and calculate corresponding zero rate and AtMat"""
        self.maturities.append(maturity)
        self.discount_factors.append(discount_factor)
        self.AtMats.append(1/discount_factor)
        self.zero_rates.append(math.log(1/discount_factor)/maturity)
    
    def get_AtMat(self, maturity):
        """Get the amount at maturity for a given time point (with interpolation if needed)"""
        if maturity in self.maturities:
            return self.AtMats[self.maturities.index(maturity)]
        else:
            return exp_interp(self.maturities, self.AtMats, maturity)

    def get_discount_factor(self, maturity):
        """Get the discount factor for a given maturity (with interpolation if needed)"""
        if maturity in self.maturities:
            return self.discount_factors[self.maturities.index(maturity)]
        else:
            return exp_interp(self.maturities, self.discount_factors, maturity)

    def get_zero_rate(self, maturity):
        """Get the zero rate for a given maturity (with interpolation if needed)"""
        if maturity in self.maturities:
            return self.zero_rates[self.maturities.index(maturity)]
        else:
            return math.log(self.get_AtMat(maturity))/maturity
        
    def get_zero_curve(self):
        """Return the complete zero curve as maturities and discount factors"""
        return self.maturities, self.discount_factors
    
    def npv(self, cash_flows):
        """Calculate the net present value of a cash flow stream"""
        npv = 0
        for maturity in cash_flows.get_maturities():
            npv += cash_flows.get_cash_flow(maturity)*self.get_discount_factor(maturity)
        return npv
        

def exp_interp(xs, ys, x):
    """
    Interpolates a single point for a given value of x 
    using continuously compounded rates.

    Parameters:
    xs (list or np.array): Vector of x values sorted by x.
    ys (list or np.array): Vector of y values.
    x (float): The x value to interpolate.

    Returns:
    float: Interpolated y value.
    """
    xs = np.array(xs)
    ys = np.array(ys)
    
    # Find the interval [x0, x1] where x0 <= x <= x1
    idx = np.searchsorted(xs, x) - 1
    x0, x1 = xs[idx], xs[idx + 1]
    y0, y1 = ys[idx], ys[idx + 1]
    
    # Calculate the continuously compounded rate
    rate = (np.log(y1) - np.log(y0)) / (x1 - x0)
    
    # Interpolate the y value for the given x
    y = y0 * np.exp(rate * (x - x0))
    
    return y
```
Using zero curve
```
# Create an instance of the ZeroCurve class
# This initializes an empty curve ready to accept rate data
zc = ZeroCurve()

# Add zero rates to the curve
# These rates represent annual interest rates for zero-coupon bonds
zc.add_zero_rate(0.5, 0.0125)  # 6-month rate
zc.add_zero_rate(1, 0.015)  # 1.5% for 1 year
zc.add_zero_rate(2, 0.025)  # 2.5% for 2 years
zc.add_zero_rate(3, 0.035)  # 3.5% for 3 years
zc.add_zero_rate(4, 0.045)  # 4.5% for 4 years

# Demonstrate retrieving zero rates
print("2.5-year zero rate:", zc.get_zero_rate(2.5))

# Calculate and display discount factors
# Discount factors represent the present value of 1 unit of currency
print("1-year discount factor:", zc.get_discount_factor(1))
print("2-year discount factor:", zc.get_discount_factor(2))
print("3-year discount factor:", zc.get_discount_factor(3))
print("4-year discount factor:", zc.get_discount_factor(4))

# Demonstrate interpolation for a non-standard maturity
maturity_lookup = 1.5
print(f"Zero rate for {maturity_lookup} years:", zc.get_zero_rate(maturity_lookup))
print(f"Amount at Maturity for {maturity_lookup} years:", zc.get_AtMat(maturity_lookup))
print(f"Discount factor for {maturity_lookup} years:", zc.get_discount_factor(maturity_lookup))

# Get the complete zero curve data
print("Complete zero curve:", zc.get_zero_curve())

# Create a pandas DataFrame for better data visualization and analysis
zcT = np.transpose(zc.get_zero_curve())
zc_dataframe = pd.DataFrame(zcT, columns=['Maturity', 'Discount Factor'])
zc_dataframe.set_index('Maturity', inplace=True)
print("\nZero Curve DataFrame:")
print(zc_dataframe)
zc_dataframe
```
refer to https://github.com/howesrichard/FM_yield_curve/blob/main/1_adding_a_zero_curve.ipynb for more 

## Inheritance
- create new classes based on existing ones

```
class Bank_bill(CashFlows):  # Bank_bill inherits from CashFlows
    
    def __init__(self, face_value=100, maturity=0.25, ytm=0.00, price=100):
        # Call the parent class's __init__ method
        super().__init__()
        # Add attributes specific to bank bills
        self.face_value = face_value
        self.maturity = maturity
        self.ytm = ytm
        self.price = price
    
    def set_ytm(self, ytm):
        """Set yield to maturity and calculate the corresponding price."""
        self.ytm = ytm
        # Simple interest formula for bank bills
        self.price = self.face_value / (1 + ytm * self.maturity)
    
    def set_price(self, price):
        """Set price and calculate the implied yield to maturity."""
        self.price = price
        # Solve for ytm from the pricing formula
        self.ytm = (self.face_value / price - 1) / self.maturity
    
    def get_price(self):
        return self.price
    
    def get_ytm(self):
        return self.ytm
    
    def set_cash_flows(self):
        """Generate the cash flows for this bank bill."""
        self.add_cash_flow(0, -self.price)
        self.add_cash_flow(self.maturity, self.face_value)
```

Can see more at https://github.com/howesrichard/FM_yield_curve/blob/main/0_OOP_intro_financial_instruments.ipynb 


# Options
- financial contracts that give the holder the right, but not obligation, to buy or sell an underlying asset at a specific price (strike price) on or before a certain date (the _expiration date_)

## Types of options
- *Call Option*: Gives the holder the right to buy the underlying asset at the strike price.

             /
            /
___________/

    - max call value is unlimited
    - payoff = max(S - K, 0)
        - S: asset price
        - K: strike price

- *Put Option*: Gives the holder the right to sell the underlying asset at the strike price.

\
 \
  \________

    - max put value capped at y intercept
    - payoff = max(K - S, 0)

- never lose money, just oppurtunity to make money

## Code: generate payoff diagram
```
import numpy as np
import matplotlib.pyplot as plt

# Parameters
K = 100  # Strike price
S = np.linspace(50, 150, 200)  # Range of underlying prices at expiry

# Payoff calculations
call_payoff = np.maximum(S - K, 0)
put_payoff = np.maximum(K - S, 0)

# Plot Call Option Payoff
plt.figure(figsize=(8, 4))
plt.plot(S, call_payoff, label='Call Option Payoff', color='blue')
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(K, color='gray', linestyle='--', label='Strike Price (K)')
plt.title('Call Option Payoff at Expiry')
plt.xlabel('Stock Price at Expiry ($S$)')
plt.ylabel('Payoff')
plt.legend()
plt.grid(True)
plt.show()

# Plot Put Option Payoff
plt.figure(figsize=(8, 4))
plt.plot(S, put_payoff, label='Put Option Payoff', color='red')
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(K, color='gray', linestyle='--', label='Strike Price (K)')
plt.title('Put Option Payoff at Expiry')
plt.xlabel('Stock Price at Expiry ($S$)')
plt.ylabel('Payoff')
plt.legend()
plt.grid(True)
plt.show()
```

## The Black–Scholes Formula

The **Black–Scholes formula** is a fundamental result in financial mathematics used to calculate the theoretical price of European call and put options, which are options that can only be exercised at expiration. It assumes that the price of the underlying asset follows a *Geometric Brownian Motion* with constant drift and volatility.

### Black–Scholes Formula for a European Call Option

$$
C = S_0 N\!\left(\frac{\ln(S_0/K) + \left(r + \frac{1}{2}\sigma^2\right)T}{\sigma \sqrt{T}}\right)
- K e^{-rT} N\!\left(\frac{\ln(S_0/K) + \left(r + \frac{1}{2}\sigma^2\right)T}{\sigma \sqrt{T}} - \sigma \sqrt{T}\right)
$$

where:

- $C$ = price of the European call option  
- $S_0$ = current price of the underlying asset  
- $K$ = strike price  
- $r$ = risk-free interest rate (annualized)  
- $T$ = time to maturity (in years)  
- $N(\cdot)$ = cumulative distribution function of the standard normal distribution  

<br><br>

The formula can be written in a slightly more readable and understandable form as:

$$
C = S_0 N(d_1) - K e^{-rT} N(d_2)
$$

The terms $d_1$ and $d_2$ are defined as:

$$
d_1 = \frac{\ln(S_0/K) + \left(r + \frac{1}{2}\sigma^2\right)T}{\sigma \sqrt{T}}
$$

$$
d_2 = d_1 - \sigma \sqrt{T}
$$

where:

- $\sigma$ = volatility of the underlying asset (annualized)
