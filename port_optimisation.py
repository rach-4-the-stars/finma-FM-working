import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set random seed for reproducibility
np.random.seed(42)

class MultiAssetOptimisation:
    """
    Multi-asset portfolio optimization using Monte Carlo simulation.
    """
    ALPHA = 0.3  # Dirichlet concentration parameter
    
    def __init__(self, returns, volatilities, corr_matrix, asset_names, 
                 num_portfolios=50000, risk_free_rate=0.04, weighting_style='normalised'):
        self.returns = np.array(returns)
        self.volatilities = np.array(volatilities)
        self.corr_matrix = np.array(corr_matrix)
        self.asset_names = asset_names
        self.num_portfolios = num_portfolios
        self.risk_free_rate = risk_free_rate
        self.weighting_style = weighting_style
        
        # Create covariance matrix from correlation and volatilities
        self.cov_matrix = self.corr_matrix * np.outer(self.volatilities, self.volatilities)
    
    def _get_weights(self):
        n = len(self.returns)
        
        if self.weighting_style == 'normalised':
            weights = np.random.random((self.num_portfolios, n))
            weights = weights / weights.sum(axis=1, keepdims=True)
        
        elif self.weighting_style == 'dirichlet':
            weights = np.random.dirichlet(self.ALPHA * np.ones(n), size=self.num_portfolios)
        
        elif self.weighting_style == 'constrain-assets':
            weights = []
            for _ in range(self.num_portfolios):
                w = np.zeros(n)
                i, j = np.random.choice(n, size=2, replace=False)
                vals = np.random.random(2)
                vals /= vals.sum()
                w[i], w[j] = vals
                weights.append(w)
            weights = np.array(weights)
        
        else:
            raise ValueError("Invalid weighting_style.")
        
        return weights
    
    def plot_efficient_frontier(self):
        weights = self._get_weights()
        
        portfolio_returns = weights @ self.returns
        portfolio_vols = np.array([
            np.sqrt(w.T @ self.cov_matrix @ w) for w in weights
        ])
        sharpe_ratios = (portfolio_returns - self.risk_free_rate) / portfolio_vols
        
        # Optimal portfolios
        max_sharpe_idx = np.argmax(sharpe_ratios)
        min_vol_idx = np.argmin(portfolio_vols)
        
        # Plot
        plt.figure(figsize=(14, 10))
        scatter = plt.scatter(portfolio_vols, portfolio_returns, 
                            c=sharpe_ratios, cmap='viridis', alpha=0.5, s=10)
        plt.colorbar(scatter).set_label('Sharpe Ratio')
        
        # Optimal points
        plt.scatter(portfolio_vols[max_sharpe_idx], portfolio_returns[max_sharpe_idx], 
                   c='red', marker='*', s=300, label='Maximum Sharpe')
        plt.scatter(portfolio_vols[min_vol_idx], portfolio_returns[min_vol_idx], 
                   c='green', marker='*', s=300, label='Minimum Volatility')
        
        # Plot individual assets
        for i, name in enumerate(self.asset_names):
            plt.scatter(self.volatilities[i], self.returns[i], 
                       s=100, marker='D', edgecolors='black', linewidths=2)
            plt.annotate(name, (self.volatilities[i], self.returns[i]), 
                        fontsize=9, alpha=0.7, ha='right')
        
        plt.xlabel('Volatility (Standard Deviation)')
        plt.ylabel('Expected Return')
        plt.title('Efficient Frontier')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()
        
        # Print optimal portfolios
        print("-" * 50)
        print("Maximum Sharpe Ratio Portfolio Allocation\n")
        for i, name in enumerate(self.asset_names):
            print(f"{name}: {weights[max_sharpe_idx][i]*100:.2f}%")
        print(f"Expected Return: {portfolio_returns[max_sharpe_idx]*100:.2f}%")
        print(f"Expected Volatility: {portfolio_vols[max_sharpe_idx]*100:.2f}%")
        print(f"Sharpe Ratio: {sharpe_ratios[max_sharpe_idx]:.2f}")
        
        print("\n" + "-" * 50)
        print("Minimum Volatility Portfolio Allocation\n")
        for i, name in enumerate(self.asset_names):
            print(f"{name}: {weights[min_vol_idx][i]*100:.2f}%")
        print(f"Expected Return: {portfolio_returns[min_vol_idx]*100:.2f}%")
        print(f"Expected Volatility: {portfolio_vols[min_vol_idx]*100:.2f}%")
        print(f"Sharpe Ratio: {sharpe_ratios[min_vol_idx]:.2f}")    
    def get_max_sharpe_portfolio(self):
        """Calculate and return the maximum Sharpe ratio portfolio metrics."""
        weights = self._get_weights()
        
        portfolio_returns = weights @ self.returns
        portfolio_vols = np.array([
            np.sqrt(w.T @ self.cov_matrix @ w) for w in weights
        ])
        sharpe_ratios = (portfolio_returns - self.risk_free_rate) / portfolio_vols
        
        max_sharpe_idx = np.argmax(sharpe_ratios)
        
        return {
            'weights': weights[max_sharpe_idx],
            'return': portfolio_returns[max_sharpe_idx],
            'volatility': portfolio_vols[max_sharpe_idx],
            'sharpe_ratio': sharpe_ratios[max_sharpe_idx]
        }
    
    def get_optimal_portfolios(self):
        """Calculate and return both max Sharpe and min volatility portfolios."""
        weights = self._get_weights()
        
        portfolio_returns = weights @ self.returns
        portfolio_vols = np.array([
            np.sqrt(w.T @ self.cov_matrix @ w) for w in weights
        ])
        sharpe_ratios = (portfolio_returns - self.risk_free_rate) / portfolio_vols
        
        max_sharpe_idx = np.argmax(sharpe_ratios)
        min_vol_idx = np.argmin(portfolio_vols)
        
        return {
            'max_sharpe': {
                'weights': weights[max_sharpe_idx],
                'return': portfolio_returns[max_sharpe_idx],
                'volatility': portfolio_vols[max_sharpe_idx],
                'sharpe_ratio': sharpe_ratios[max_sharpe_idx]
            },
            'min_vol': {
                'weights': weights[min_vol_idx],
                'return': portfolio_returns[min_vol_idx],
                'volatility': portfolio_vols[min_vol_idx],
                'sharpe_ratio': sharpe_ratios[min_vol_idx]
            }
        }

# Define the 10 equity sectors
sectors = [
    "Energy", "Materials", "Industrials", "Consumer Discretionary",
    "Consumer Staples", "Health Care", "Financials", "Information Technology",
    "Telecom", "Utilities"
]

# Expected annual returns (as decimals, e.g., 0.0877 = 8.77%)
sector_returns = np.array([0.0877, 0.0983, 0.1203, 0.1312, 0.0761,
                           0.1112, 0.0726, 0.1493, 0.0942, 0.0829])

# Annual volatilities (standard deviations)
sector_volatilities = np.array([0.20, 0.22, 0.18, 0.19, 0.13,
                                0.15, 0.20, 0.27, 0.21, 0.15])

# Correlation matrix (10x10)
sector_corr = np.array([
    [1.00, 0.72, 0.62, 0.49, 0.36, 0.37, 0.51, 0.41, 0.33, 0.52],
    [0.72, 1.00, 0.78, 0.71, 0.51, 0.43, 0.65, 0.52, 0.40, 0.38],
    [0.62, 0.78, 1.00, 0.88, 0.63, 0.60, 0.83, 0.69, 0.55, 0.43],
    [0.49, 0.71, 0.88, 1.00, 0.60, 0.57, 0.80, 0.75, 0.46, 0.33],
    [0.36, 0.51, 0.63, 0.60, 1.00, 0.64, 0.68, 0.35, 0.45, 0.42],
    [0.37, 0.43, 0.60, 0.57, 0.64, 1.00, 0.61, 0.53, 0.46, 0.43],
    [0.51, 0.65, 0.83, 0.80, 0.68, 0.61, 1.00, 0.52, 0.49, 0.43],
    [0.41, 0.52, 0.69, 0.75, 0.35, 0.53, 0.52, 1.00, 0.49, 0.17],
    [0.33, 0.40, 0.55, 0.46, 0.45, 0.46, 0.49, 0.49, 1.00, 0.28],
    [0.52, 0.38, 0.43, 0.33, 0.42, 0.43, 0.43, 0.17, 0.28, 1.00],
])

print("Baseline data loaded successfully!")
print(f"Number of sectors: {len(sectors)}")
print(f"Correlation matrix shape: {sector_corr.shape}")

 #Create optimizer with equity sectors only
opt_baseline = MultiAssetOptimisation(
    sector_returns, 
    sector_volatilities, 
    sector_corr, 
    sectors, 
    weighting_style='dirichlet'
)

# Plot the efficient frontier
print("BASELINE: Equity Sectors Only\n")
opt_baseline.plot_efficient_frontier()

# Exercise 1: Add TLT to sectors list
# TODO: Your code here
sectors.append("Long-Term Treasuries (TLT)")

# Test your code
print(f"Number of sectors: {len(sectors)}")
print(f"Last sector: {sectors[-1]}")
assert len(sectors) == 11, "You should have 11 sectors now!"
assert "TLT" in sectors[-1] or "Treasuries" in sectors[-1], "Last sector should be TLT!"
print("✓ Exercise 1 complete!")

# Exercise 2: Add TLT's expected return
# TODO: Your code here
sector_returns = np.append(sector_returns, 0.05)


# Test your code
print(f"Number of returns: {len(sector_returns)}")
print(f"TLT expected return: {sector_returns[-1]*100:.2f}%")
assert len(sector_returns) == 11, "You should have 11 returns now!"
assert abs(sector_returns[-1] - 0.05) < 0.001, "TLT return should be 0.05!"
print("✓ Exercise 2 complete!")

# Exercise 3: Add TLT's volatility
# TODO: Your code here
# sector_volatilities = ...
sector_volatilities = np.append(sector_volatilities, 0.12)



# Test your code
print(f"Number of volatilities: {len(sector_volatilities)}")
print(f"TLT volatility: {sector_volatilities[-1]*100:.2f}%")
assert len(sector_volatilities) == 11, "You should have 11 volatilities now!"
assert abs(sector_volatilities[-1] - 0.12) < 0.001, "TLT volatility should be 0.12!"
print("✓ Exercise 3 complete!")

# Exercise 4: Define TLT's correlations with the 10 equity sectors
# TODO: Your code here
# tlt_corr_with_sectors = np.array([...])

tlt_corr_with_sectors = np.array([-0.35,-0.3,-0.4,-0.45,-0.25,-0.3,-0.45,-0.25,-0.4,-0.3])
# Test your code
print(f"TLT correlations: {tlt_corr_with_sectors}")
print(f"Number of correlations: {len(tlt_corr_with_sectors)}")
assert len(tlt_corr_with_sectors) == 10, "Should have 10 correlations (one for each equity sector)!"
assert tlt_corr_with_sectors.min() < 0, "At least some correlations should be negative!"
print("✓ Exercise 4 complete!")

# Exercise 5: Add TLT as a new row at the bottom
# TODO: Your code here
sector_corr = np.vstack([sector_corr, tlt_corr_with_sectors])


# Test your code
print(f"Correlation matrix shape after adding row: {sector_corr.shape}")
assert sector_corr.shape == (11, 10), "Matrix should be 11×10 now (11 rows, 10 columns)!"
print(f"Last row (TLT correlations with sectors): {sector_corr[-1, :]}")
print("✓ Exercise 5 complete!")

# Exercise 6: Create TLT column (including its self-correlation of 1.0)
# TODO: Your code here
# Step 1: Append 1.0 to tlt_corr_with_sectors
tlt_full_column = np.append(tlt_corr_with_sectors, 1.0)

# Step 2: Reshape to column vector
tlt_column = tlt_full_column.reshape(11,1)


# Test your code
print(f"TLT column shape: {tlt_column.shape}")
print(f"TLT column:\n{tlt_column}")
assert tlt_column.shape == (11, 1), "TLT column should be 11×1!"
assert abs(tlt_column[-1, 0] - 1.0) < 0.001, "Last value should be 1.0 (TLT's self-correlation)!"
print("✓ Exercise 6 complete!")

# Exercise 7: Add TLT column to the right side of the matrix
# TODO: Your code here
sector_corr = np.hstack([sector_corr, tlt_column])


# Test your code
print(f"Final correlation matrix shape: {sector_corr.shape}")
assert sector_corr.shape == (11, 11), "Matrix should be 11×11 now!"
assert abs(sector_corr[-1, -1] - 1.0) < 0.001, "Bottom-right corner should be 1.0!"
assert abs(sector_corr[0, -1] + 0.35) < 0.001, "Top-right should be Energy-TLT correlation (-0.35)!"
print("✓ Exercise 7 complete!")
print("\n🎉 Congratulations! You've successfully expanded the correlation matrix!")

# Visualize correlation matrix
plt.figure(figsize=(12, 10))
sns.heatmap(sector_corr, annot=True, fmt='.2f', cmap='RdYlGn', 
            center=0, vmin=-1, vmax=1,
            xticklabels=sectors, yticklabels=sectors)
plt.title('Correlation Matrix with Government Bonds')
plt.tight_layout()
plt.show()

print("Notice the last row and column (TLT):")
print("- Most correlations are NEGATIVE (shown in red/orange)")
print("- This is why bonds are powerful diversifiers!")
print("- When stocks fall, bonds often rise (negative correlation)")

# Exercise 8: Run optimization with government bonds
# TODO: Your code here
opt_with_bonds = MultiAssetOptimisation(
    sector_returns,
    sector_volatilities,
    sector_corr,
    sectors,
    weighting_style='dirichlet'
)

# Plot the efficient frontier
print("WITH GOVERNMENT BONDS:\n")
opt_with_bonds.plot_efficient_frontier()

# ============================================================================
# SUMMARY: Before vs After Comparison
# ============================================================================
print("\n" + "="*70)
print("PORTFOLIO OPTIMIZATION SUMMARY: EQUITIES ONLY vs WITH BONDS")
print("="*70)

# Get metrics for both portfolios
baseline_metrics = opt_baseline.get_optimal_portfolios()
bonds_metrics = opt_with_bonds.get_optimal_portfolios()

# ============================================================================
# 1. MAXIMUM SHARPE RATIO COMPARISON
# ============================================================================
print("\n" + "-"*70)
print("MAXIMUM SHARPE RATIO STRATEGY")
print("-"*70)
print(f"\n{'Metric':<30} {'Equities Only':<20} {'With Bonds':<20}")
print("-" * 70)
print(f"{'Expected Return':<30} {baseline_metrics['max_sharpe']['return']*100:>18.2f}% {bonds_metrics['max_sharpe']['return']*100:>18.2f}%")
print(f"{'Volatility (Std Dev)':<30} {baseline_metrics['max_sharpe']['volatility']*100:>18.2f}% {bonds_metrics['max_sharpe']['volatility']*100:>18.2f}%")
print(f"{'Sharpe Ratio':<30} {baseline_metrics['max_sharpe']['sharpe_ratio']:>19.4f} {bonds_metrics['max_sharpe']['sharpe_ratio']:>19.4f}")

# Print detailed allocation for bonds portfolio (max Sharpe)
print("\nWITH BONDS: Maximum Sharpe Ratio Allocation")
print("-" * 70)
for i, name in enumerate(opt_with_bonds.asset_names):
    allocation = bonds_metrics['max_sharpe']['weights'][i] * 100
    print(f"{name:<30} {allocation:>6.2f}%")
tlt_idx = opt_with_bonds.asset_names.index("Long-Term Treasuries (TLT)")
tlt_allocation = bonds_metrics['max_sharpe']['weights'][tlt_idx] * 100
print(f"\n{'TLT Allocation':<30} {tlt_allocation:>6.2f}%")

# ============================================================================
# 2. MINIMUM VOLATILITY COMPARISON
# ============================================================================
print("\n" + "-"*70)
print("MINIMUM VOLATILITY STRATEGY")
print("-"*70)
print(f"\n{'Metric':<30} {'Equities Only':<20} {'With Bonds':<20}")
print("-" * 70)
print(f"{'Expected Return':<30} {baseline_metrics['min_vol']['return']*100:>18.2f}% {bonds_metrics['min_vol']['return']*100:>18.2f}%")
print(f"{'Volatility (Std Dev)':<30} {baseline_metrics['min_vol']['volatility']*100:>18.2f}% {bonds_metrics['min_vol']['volatility']*100:>18.2f}%")
print(f"{'Sharpe Ratio':<30} {baseline_metrics['min_vol']['sharpe_ratio']:>19.4f} {bonds_metrics['min_vol']['sharpe_ratio']:>19.4f}")

# Print detailed allocation for bonds portfolio (min vol)
print("\nWITH BONDS: Minimum Volatility Allocation")
print("-" * 70)
for i, name in enumerate(opt_with_bonds.asset_names):
    allocation = bonds_metrics['min_vol']['weights'][i] * 100
    print(f"{name:<30} {allocation:>6.2f}%")
tlt_allocation = bonds_metrics['min_vol']['weights'][tlt_idx] * 100
print(f"\n{'TLT Allocation':<30} {tlt_allocation:>6.2f}%")

print("\n" + "="*70)
