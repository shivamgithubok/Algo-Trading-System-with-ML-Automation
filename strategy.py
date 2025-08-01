# strategy.py
import pandas as pd
import numpy as np

def calculate_rsi(prices, period=14):
    """Calculate RSI manually to avoid pandas-ta dependency issues."""
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_sma(prices, period):
    """Calculate Simple Moving Average."""
    return prices.rolling(window=period).mean()

def apply_trading_strategy(df: pd.DataFrame) -> list:
    """
    [cite_start]Applies the RSI + Moving Average crossover strategy and returns a list of trades[cite: 5].
    
    Args:
        df (pd.DataFrame): DataFrame with stock data.

    Returns:
        list: A list of dictionaries, where each dictionary represents a trade.
    """
    if df is None or df.empty:
        print("Error: No data provided for strategy analysis")
        return []
    
    if len(df) < 50:  # Need at least 50 days for the 50-DMA
        print(f"Error: Insufficient data for strategy analysis. Need at least 50 rows, got {len(df)}")
        return []

    try:
        # Determine which price column to use
        price_column = 'Adj Close' if 'Adj Close' in df.columns else 'Close'
        if price_column not in df.columns:
            print(f"Error: No price column found. Available columns: {list(df.columns)}")
            return []
        
        print(f"Using '{price_column}' column for price data")
        
        # Calculate technical indicators manually
        df['RSI_14'] = calculate_rsi(df[price_column], 14)
        df['SMA_20'] = calculate_sma(df[price_column], 20)
        df['SMA_50'] = calculate_sma(df[price_column], 50)
        df.dropna(inplace=True) # Remove rows with NaN values after indicator calculation
        df.reset_index(inplace=True)
        
        if len(df) < 2:  # Need at least 2 rows after indicator calculation
            print("Error: Insufficient data after indicator calculation")
            return []
    except Exception as e:
        print(f"Error calculating technical indicators: {e}")
        return []

    trades = []
    position_open = False
    
    for i in range(1, len(df)):
        try:
            # [cite_start]Buy Signal: RSI < 30 and 20-DMA crosses above 50-DMA [cite: 12, 13]
            if (not position_open and 
                df['RSI_14'][i] < 30 and 
                df['SMA_20'][i-1] <= df['SMA_50'][i-1] and 
                df['SMA_20'][i] > df['SMA_50'][i]):
                
                buy_price = df[price_column][i]
                trade = {'buy_date': df['Date'][i], 'buy_price': buy_price}
                trades.append(trade)
                position_open = True

            # Sell Signal: 20-DMA crosses below 50-DMA
            elif (position_open and 
                  df['SMA_20'][i-1] >= df['SMA_50'][i-1] and 
                  df['SMA_20'][i] < df['SMA_50'][i]):
                
                sell_price = df[price_column][i]
                trades[-1].update({'sell_date': df['Date'][i], 'sell_price': sell_price})
                position_open = False
        except Exception as e:
            print(f"Error processing trade at index {i}: {e}")
            continue
            
    return trades