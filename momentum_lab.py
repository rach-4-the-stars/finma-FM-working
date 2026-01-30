import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def trading_algorithm_1(df: pd.DataFrame, share_size: int = 100) -> pd.DataFrame:
    """Baseline trading algorithm (Step 2 from Simple_Strategy).

    Rules implemented:
    - Ensure columns: `trade_type`, `costs_proceeds`, `accumulated_shares`.
    - Use `share_size` shares per buy (default 100).
    - Buy on first row (previous_price == 0).
    - Otherwise, buy when today's price is less than yesterday's price.
    - On the last day, sell all accumulated shares.

    Buys record negative cashflow in `costs_proceeds` and sells record positive cashflow.
    """
    df = df.copy().reset_index(drop=True)
    n = len(df)

    # Initialize columns
    df['trade_type'] = ''
    df['costs_proceeds'] = 0.0
    df['accumulated_shares'] = 0

    accumulated = 0
    prev_price = 0.0

    for i in range(n):
        price = float(df.loc[i, 'close'])

        # First row: buy (previous price treated as 0)
        if i == 0 and prev_price == 0:
            accumulated += share_size
            df.at[i, 'trade_type'] = 'buy'
            df.at[i, 'costs_proceeds'] = -share_size * price

        # Last day: sell all accumulated shares
        elif i == n - 1:
            if accumulated > 0:
                df.at[i, 'trade_type'] = 'sell'
                df.at[i, 'costs_proceeds'] = accumulated * price
                accumulated = 0

        # Intermediate days: buy if price < previous day's price
        else:
            if price < prev_price:
                accumulated += share_size
                df.at[i, 'trade_type'] = 'buy'
                df.at[i, 'costs_proceeds'] = -share_size * price

        df.at[i, 'accumulated_shares'] = accumulated
        prev_price = price

    return df

def profit_and_loss(results: pd.DataFrame) -> float:
    return float(results['costs_proceeds'].sum())

def return_on_investment(total_pl: float, results: pd.DataFrame) -> float:
    capital_invested = results.loc[results['costs_proceeds'] < 0, 'costs_proceeds'].sum()
    # capital_invested is negative, so flip sign to make denominator positive
    if capital_invested == 0:
        return np.nan
    roi = (total_pl / (-capital_invested)) * 100
    return float(roi)

def profit_taking_strategy(df: pd.DataFrame, profit_take_percentage: float = 0.20, share_size: int = 100) -> pd.DataFrame:
    """Profit-taking strategy (Step 5 Option A from Simple_Strategy).
    
    Rules implemented:
    - Keep baseline buy logic (buy on first row, or when price < previous price).
    - Track average purchase price (weighted by shares bought).
    - Sell HALF of accumulated shares if price rises by profit_take_percentage above avg purchase price.
    - On the last day, sell all remaining accumulated shares.
    
    Args:
        df: DataFrame with 'date' and 'close' columns.
        profit_take_percentage: Threshold for profit-taking (e.g., 0.20 = 20%).
        share_size: Number of shares per buy.
    
    Returns:
        DataFrame with columns: trade_type, costs_proceeds, accumulated_shares, avg_purchase_price.
    """
    df = df.copy().reset_index(drop=True)
    n = len(df)
    
    # Initialize columns
    df['trade_type'] = ''
    df['costs_proceeds'] = 0.0
    df['accumulated_shares'] = 0
    df['avg_purchase_price'] = 0.0
    
    accumulated = 0
    total_cost = 0.0  # Sum of (share_size * price) for all buys
    prev_price = 0.0
    
    for i in range(n):
        price = float(df.loc[i, 'close'])
        
        # First row: buy
        if i == 0 and prev_price == 0:
            accumulated += share_size
            total_cost += share_size * price
            avg_purchase_price = total_cost / accumulated if accumulated > 0 else 0
            df.at[i, 'trade_type'] = 'buy'
            df.at[i, 'costs_proceeds'] = -share_size * price
            df.at[i, 'accumulated_shares'] = accumulated
            df.at[i, 'avg_purchase_price'] = avg_purchase_price
        
        else:
            # Calculate current average purchase price
            avg_purchase_price = total_cost / accumulated if accumulated > 0 else 0
            
            # Check profit-taking condition: if price > avg_purchase_price * (1 + profit_take_percentage)
            profit_threshold = avg_purchase_price * (1 + profit_take_percentage)
            
            if accumulated > 0 and price > profit_threshold:
                # Sell half of accumulated shares (profit-taking)
                sell_quantity = accumulated // 2
                if sell_quantity > 0:
                    accumulated -= sell_quantity
                    df.at[i, 'trade_type'] = 'sell (profit-take)'
                    df.at[i, 'costs_proceeds'] = sell_quantity * price
                    # Update total_cost proportionally
                    total_cost -= (sell_quantity / (accumulated + sell_quantity)) * total_cost if (accumulated + sell_quantity) > 0 else 0
            
            # Baseline buy logic: buy if price < previous price
            if price < prev_price:
                accumulated += share_size
                total_cost += share_size * price
                df.at[i, 'trade_type'] = 'buy'
                df.at[i, 'costs_proceeds'] = -share_size * price
            
            df.at[i, 'accumulated_shares'] = accumulated
            avg_purchase_price = total_cost / accumulated if accumulated > 0 else 0
            df.at[i, 'avg_purchase_price'] = avg_purchase_price
        
        # Last day: sell all remaining accumulated shares
        if i == n - 1 and accumulated > 0:
            df.at[i, 'trade_type'] = 'sell (close)'
            df.at[i, 'costs_proceeds'] = accumulated * price
            accumulated = 0
        
        prev_price = price
    
    return df


# Load data
# Expected columns include: Date, Adj Close (or Adj.Close)
raw = pd.read_csv('AMD.csv')

# Normalize column names to make life easier
cols = {c: c.strip().replace(' ', '').replace('.', '') for c in raw.columns}
raw = raw.rename(columns=cols)

# Build amd_df with (date, close)
amd_df = pd.DataFrame({
    'date': pd.to_datetime(raw['Date'], utc=True),
    # Try common variants: AdjClose / AdjClose, if not present you may need to change this
    'close': pd.to_numeric(raw.get('AdjClose', raw.get('AdjClose', raw.get('Close'))), errors='coerce')
})

amd_df = amd_df.dropna().sort_values('date').reset_index(drop=True)
amd_df.head()

plt.figure()
plt.plot(amd_df['date'], amd_df['close'])
plt.title('AMD Adjusted Close')
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()

# Choose and filter the dataset for your trading period
amd_df_filtered = amd_df[(amd_df['date'] >= '2022-01-01') & (amd_df['date'] <= '2022-12-31')].reset_index(drop=True)
print(f"Filtered data from {amd_df_filtered['date'].min().date()} to {amd_df_filtered['date'].max().date()}, total {len(amd_df_filtered)} rows.")  
results_1_filtered = trading_algorithm_1(amd_df_filtered)
pl_1 = profit_and_loss(results_1_filtered)
roi_1 = return_on_investment(pl_1, results_1_filtered)

# Summary outputs for Algorithm 1 (baseline)
capital_invested = -results_1_filtered.loc[results_1_filtered['costs_proceeds'] < 0, 'costs_proceeds'].sum()
buys = int((results_1_filtered['trade_type'] == 'buy').sum())
sells = int((results_1_filtered['trade_type'] == 'sell').sum())
final_shares = int(results_1_filtered['accumulated_shares'].iloc[-1])

print("\nSUMMARY: Algorithm 1 (Baseline)")
print("-" * 50)
print(f"Total P/L:           ${pl_1:,.2f}")
print(f"Capital Invested:    ${capital_invested:,.2f}")
print(f"Return on Investment:{roi_1:.2f}%")
print(f"Number of Buys:      {buys}")
print(f"Number of Sells:     {sells}")
print(f"Final Accumulated Shares: {final_shares}")

print("\nSample trades (first 20):")
print(results_1_filtered.loc[results_1_filtered['trade_type'] != '', ['date', 'trade_type', 'costs_proceeds', 'accumulated_shares']].head(20).to_string(index=False))

# ============================================================================
# STRATEGY 2: Profit-Taking (Option A from Step 5)
# ============================================================================
print("\n" + "=" * 70)
print("STRATEGY 2: Profit-Taking (20% above average purchase price)")
print("=" * 70)

results_2_filtered = profit_taking_strategy(amd_df_filtered, profit_take_percentage=0.20)
pl_2 = profit_and_loss(results_2_filtered)
roi_2 = return_on_investment(pl_2, results_2_filtered)

# Summary outputs for Strategy 2
capital_invested_2 = -results_2_filtered.loc[results_2_filtered['costs_proceeds'] < 0, 'costs_proceeds'].sum()
buys_2 = int((results_2_filtered['trade_type'] == 'buy').sum())
sells_2 = int((results_2_filtered['trade_type'].str.contains('sell', na=False)).sum())
final_shares_2 = int(results_2_filtered['accumulated_shares'].iloc[-1])

print("\nSUMMARY: Strategy 2 (Profit-Taking)")
print("-" * 50)
print(f"Total P/L:           ${pl_2:,.2f}")
print(f"Capital Invested:    ${capital_invested_2:,.2f}")
print(f"Return on Investment:{roi_2:.2f}%")
print(f"Number of Buys:      {buys_2}")
print(f"Number of Sells:     {sells_2}")
print(f"Final Accumulated Shares: {final_shares_2}")

print("\nSample trades (profit-taking events only):")
profit_take_trades = results_2_filtered[results_2_filtered['trade_type'] == 'sell (profit-take)']
if len(profit_take_trades) > 0:
    print(profit_take_trades[['date', 'trade_type', 'costs_proceeds', 'accumulated_shares', 'avg_purchase_price']].head(10).to_string(index=False))
else:
    print("No profit-taking events triggered during this period.")

# ============================================================================
# COMPARISON: Algorithm 1 vs Strategy 2
# ============================================================================
print("\n" + "=" * 70)
print("STRATEGY COMPARISON")
print("=" * 70)
comparison = pd.DataFrame([
    {
        'Strategy': 'Algorithm 1 (Baseline)',
        'Total P/L': f"${pl_1:,.2f}",
        'ROI (%)': f"{roi_1:.2f}%",
        'Buy Count': buys,
        'Sell Count': sells,
        'Capital Invested': f"${capital_invested:,.2f}"
    },
    {
        'Strategy': 'Strategy 2 (Profit-Taking @ 20%)',
        'Total P/L': f"${pl_2:,.2f}",
        'ROI (%)': f"{roi_2:.2f}%",
        'Buy Count': buys_2,
        'Sell Count': sells_2,
        'Capital Invested': f"${capital_invested_2:,.2f}"
    }
])
print("\n" + comparison.to_string(index=False))
print("\n" + "=" * 70)

# Return summary values for possible further use
(pl_1, pl_2, roi_1, roi_2)