
import pandas as pd
import pandas_ta as ta

# Load the recorded data
input_file = "data/historical/market_data.csv"
output_file = "data/historical/market_data_with_indicators.csv"
data = pd.read_csv(input_file)

# Calculate technical indicators
data['RSI'] = ta.rsi(data['close'], length=14)
data['SMA_20'] = ta.sma(data['close'], length=20)
macd = ta.macd(data['close'], fast=12, slow=26, signal=9)
data = pd.concat([data, macd], axis=1)

# Drop rows with NaN values (due to indicator calculations)
data.dropna(inplace=True)

# Define a function to calculate the target values (only BUY or SELL)
def calculate_target(row):
    """
    Determine the target value (BUY or SELL) based on RSI and MACD.

    Returns:
        int: 1 for BUY, 0 for SELL.
    """
    if row['RSI'] < 30 and row['MACD_12_26_9'] > 0:  # Buy condition
        return 1  # 1 for BUY
    elif row['RSI'] > 70 and row['MACD_12_26_9'] < 0:  # Sell condition
        return 0  # 0 for SELL
    else:
        return -1  # -1 for NO ACTION (to be filtered out later)

# Add the target column to the DataFrame
data['target'] = data.apply(calculate_target, axis=1)

# Filter out rows with NO ACTION (target = -1)
data = data[data['target'] != -1]

# Save the data with indicators and target values to a new CSV file
data.to_csv(output_file, index=False)
print(f"Data with indicators and target values saved to {output_file}")