import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

def fetch_stock_data(ticker, period='1mo', interval='1d'):
    """
    Fetch historical stock data for a given ticker symbol.

    Parameters:
    ticker (str): The stock ticker symbol.
    period (str): The period over which to fetch data (default is '1mo').
    interval (str): The data interval (default is '1d').

    Returns:
    DataFrame: A pandas DataFrame containing the historical stock data.
    """
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period, interval=interval)
    return hist

def display_data(data, ticker):
    # Reset index to make Date a column (yfinance returns Date as the index)
    data = data.reset_index()

    # Normalize column names to make life easier
    cols = {c: c.strip().replace(' ', '').replace('.', '') for c in data.columns}
    data = data.rename(columns=cols)

    # Build aapl_df with (date, close)
    aapl_df = pd.DataFrame({
        'date': pd.to_datetime(data['Date']),
        'close': pd.to_numeric(data['Close'], errors='coerce')
    })

    aapl_df = aapl_df.dropna().sort_values('date').reset_index(drop=True)
    aapl_df.head()

    plt.figure()
    plt.plot(aapl_df['date'], aapl_df['close'])
    plt.title(f'{ticker} Adjusted Close')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.show()

if __name__ == "__main__":
    # testing using AAPL stock data
    data = fetch_stock_data('AAPL', period='3mo', interval='1d')
    display_data(data, 'AAPL')
