import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def fetch_data(tickers: list, start_date: str, end_date: str) -> dict:
    """
    [cite_start]Fetches intraday or daily stock data for a list of NIFTY 50 stocks[cite: 10].
    
    Args:
        tickers (list): List of stock tickers.
        start_date (str): Start date for data fetching (YYYY-MM-DD).
        end_date (str): End date for data fetching (YYYY-MM-DD).

    Returns:
        dict: A dictionary where keys are tickers and values are pandas DataFrames.
    """
    if not tickers:
        print("Error: No tickers provided")
        return {}
    
    # Validate date format
    try:
        datetime.strptime(start_date, '%Y-%m-%d')
        datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        print("Error: Invalid date format. Use YYYY-MM-DD format.")
        return {}
    
    stock_data = {}
    for ticker in tickers:
        try:
            print(f"Fetching data for {ticker}...")
            data = yf.download(ticker, start=start_date, end=end_date, progress=False)
            
            if not data.empty:
                if len(data) < 50:  # Minimum required for technical indicators
                    print(f"Warning: {ticker} has insufficient data ({len(data)} rows). Minimum 50 required.")
                    continue
                
                # Check available columns and handle column name differences
                print(f"Available columns for {ticker}: {list(data.columns)}")
                
                # Handle different column names - yfinance might use 'Close' instead of 'Adj Close'
                if 'Adj Close' not in data.columns and 'Close' in data.columns:
                    data['Adj Close'] = data['Close']
                    print(f"Using 'Close' as 'Adj Close' for {ticker}")
                
                stock_data[ticker] = data
                print(f"Successfully fetched data for {ticker} ({len(data)} rows)")
            else:
                print(f"No data found for {ticker} for the given date range.")
        except Exception as e:
            print(f"Could not fetch data for {ticker}: {e}")
    
    if not stock_data:
        print("Warning: No data was successfully fetched for any ticker.")
    
    return stock_data