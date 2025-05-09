import pandas as pd
import pandas_ta as ta

def preprocess_data(market_data):
    """
    Preprocess market data and create features for the ML model.

    Args:
        market_data (pd.DataFrame): Market data with a 'close' column.

    Returns:
        pd.DataFrame: Processed market data with technical indicators.
    """
    
    # Ensure 'close' column exists
    if 'close' not in market_data.columns:
        raise ValueError("Market data must contain a 'close' column.")

    # Check if there's enough data to calculate indicators
    if len(market_data) < 26:  # Minimum rows required for MACD (26 rows)
        print("Not enough data to calculate indicators. Skipping preprocessing.")
        return pd.DataFrame()  # Return an empty DataFrame

    # Calculate technical indicators only if there are enough rows
    
    # Calculate RSI (Relative Strength Index)
    market_data['RSI'] = ta.rsi(market_data['close'], length=14)  
                 
    # Calculate SMA (Simple Moving Average)
    market_data['SMA_20'] = ta.sma(market_data['close'], length=20)
    
    # Calculate MACD (Moving Average Convergence Divergence)
    macd = ta.macd(market_data['close'], fast=12, slow=26, signal=9)
    market_data = pd.concat([market_data, macd], axis=1)

    # Drop rows with NaN values (due to indicator calculations)
    market_data.dropna(inplace=True)

    return market_data