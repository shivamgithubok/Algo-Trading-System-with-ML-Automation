# ml_model.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

def calculate_macd(prices, fast=12, slow=26, signal=9):
    """Calculate MACD manually to avoid pandas-ta dependency issues."""
    ema_fast = prices.ewm(span=fast).mean()
    ema_slow = prices.ewm(span=slow).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal).mean()
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram

def calculate_rsi(prices, period=14):
    """Calculate RSI manually."""
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def train_and_predict(df: pd.DataFrame) -> float:
    """
    [cite_start]Trains a basic ML model (Logistic Regression) to predict next-day movement[cite: 16].
    
    Args:
        df (pd.DataFrame): DataFrame with stock data.

    Returns:
        [cite_start]float: The prediction accuracy of the model[cite: 17].
    """
    if len(df) < 20: # Ensure enough data for feature calculation
        return 0.0

    try:
        # Determine which price column to use
        price_column = 'Adj Close' if 'Adj Close' in df.columns else 'Close'
        if price_column not in df.columns:
            print(f"Error: No price column found. Available columns: {list(df.columns)}")
            return 0.0
        
        print(f"ML Model using '{price_column}' column for price data")
        
        # [cite_start]Feature Engineering: Use RSI, MACD, and Volume [cite: 16]
        df['RSI_14'] = calculate_rsi(df[price_column], 14)
        macd_line, signal_line, histogram = calculate_macd(df[price_column])
        df['MACD_12_26_9'] = macd_line
        df['Volume'] = df['Volume']
        
        # Target Variable: 1 if next day's close is higher, 0 otherwise
        df['Target'] = (df[price_column].shift(-1) > df[price_column]).astype(int)
        df.dropna(inplace=True)
        
        if len(df) < 2:
            return 0.0

        features = ['RSI_14', 'MACD_12_26_9', 'Volume']
        X = df[features]
        y = df['Target']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        if len(X_train) == 0 or len(X_test) == 0:
            return 0.0
            
        model = LogisticRegression()
        model.fit(X_train, y_train)
        
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred) * 100
        
        return accuracy
    except Exception as e:
        print(f"Error in ML model training: {e}")
        return 0.0