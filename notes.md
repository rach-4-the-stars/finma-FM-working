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
