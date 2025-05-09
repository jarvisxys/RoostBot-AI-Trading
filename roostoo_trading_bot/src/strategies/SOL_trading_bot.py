import time
import pandas as pd
import joblib
from src.api.roostoo_api import RoostooAPI
from src.api.roostoo_api import DataRecorder
from src.utils.data_utils import preprocess_data

# Configuration
api_key = "xSh5rchczNi8bC0086086700kj8JHNTMNxhFemJIepIrf2vJuv0ekP4h6dGKCcpM"
secret_key = "G0dplHtb6rc9oPhmh5ygTNUFaSAvnQ6FTOn6mnkugwwFryJlmA1MjxH2JsmenCbr"
pair = "SOL/USD"  # Trading pair
fetch_interval = 300  # Fetch data every 5 minutes (300 seconds)
model_path = "data/models/sol_model.pkl"  # Path to the trained model (if using ML)

# Initialize the Roostoo API client
api = RoostooAPI(api_key, secret_key)

# Simple strategy parameters
rsi_buy_threshold = 30  # Buy when RSI < 30 (oversold)
rsi_sell_threshold = 70  # Sell when RSI > 70 (overbought)

def decide_trade(market_data):
    """
    Use a simple RSI-based strategy to decide whether to buy or sell.

    Args:
        market_data (pd.DataFrame): Market data with technical indicators.

    Returns:
        str: "BUY", "SELL", or None.
    """
    # Ensure the required features are present
    if 'RSI' not in market_data.columns:
        print("Missing RSI indicator. No trade action taken.")
        return None

    # Use the latest data point for decision
    latest_data = market_data.iloc[-1]
    rsi = latest_data['RSI']

    # Simple RSI-based strategy
    if rsi < rsi_buy_threshold:
        return "BUY"
    elif rsi > rsi_sell_threshold:
        return "SELL"
    else:
        return None

def calculate_quantity(latest_price, portfolio_value):
    """
    Calculate the quantity to buy or sell based on risk management.

    Args:
        latest_price (float): Latest price of the asset.
        portfolio_value (float): Current portfolio value.

    Returns:
        float: Quantity to trade.
    """
    risk_per_trade = 0.02  # Risk 2% of the portfolio per trade
    risk_amount = portfolio_value * risk_per_trade
    quantity = risk_amount / latest_price
    return round(quantity, 4)  # Round to 4 decimal places

def execute_trade(pair, portfolio_value):
    """
    Execute a trade based on the simple strategy.

    Args:
        pair (str): Trading pair (e.g., "SOL/USD").
        portfolio_value (float): Current portfolio value.
    """
    try:
        # Record market data
        recorder = DataRecorder(api, pair, fetch_interval=5)  # Fetch data every 5 seconds
        recorder.record(300)  # Record data for 5 minutes
        market_data = recorder.get_dataframe()

        # Preprocess and analyze market data
        market_data = preprocess_data(market_data)

        # Check if market_data is empty after preprocessing
        if market_data.empty:
            print(f"No valid data for {pair} after preprocessing. No trade action taken.")
            return

        # Decide trade action (only BUY or SELL)
        decision = decide_trade(market_data)

        # Execute trade if a decision is made
        if decision == "BUY" or decision == "SELL":
            latest_price = market_data['close'].iloc[-1]
            quantity = 1

            print(f"Executing {decision} order for {pair} with quantity {quantity}...")
            order_response = api.place_order(pair, decision, quantity)
            print(f"Order Response: {order_response}")

            # Update portfolio value after the trade
            if order_response.get("Success"):
                trade_value = latest_price * quantity
                if decision == "BUY":
                    portfolio_value -= trade_value
                elif decision == "SELL":
                    portfolio_value += trade_value

                print(f"Updated Portfolio Value: {portfolio_value}")
            else:
                print(f"Order failed. No changes to portfolio value.")
        else:
            print(f"No trade action taken for {pair}.")
    except Exception as e:
        print(f"Error occurred during trade execution: {e}")

# Main loop
if __name__ == "__main__":
    portfolio_value = 8000  # Initial portfolio value
    while True:
        try:
            # Execute a trade for SOL/USD
            execute_trade(pair, portfolio_value)

            # Sleep for the fetch interval before the next iteration
            time.sleep(fetch_interval)
        except Exception as e:
            print(f"Error occurred: {e}")
            time.sleep(5)  # Wait 5 seconds before retrying