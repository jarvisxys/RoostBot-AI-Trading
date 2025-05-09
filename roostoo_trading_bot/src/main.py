# Entry point to run the bot
from src.api.roostoo_api import RoostooAPI
from src.strategies.ml_strategy import MLTradingStrategy
from src.utils.portfolio_utils import PortfolioTracker
import time

# Configuration
api_key = "xSh5rchczNi8bC0086086700kj8JHNTMNxhFemJIepIrf2vJuv0ekP4h6dGKCcpM"
secret_key = "G0dplHtb6rc9oPhmh5ygTNUFaSAvnQ6FTOn6mnkugwwFryJlmA1MjxH2JsmenCbr"
model_path = "data/models/random_forest_model.pkl"  # Path to the trained model
pairs = ["BTC/USD"]  # List of trading pairs
fetch_interval = 300  # Fetch data every 5 minutes (300 seconds)

# Initialize the ML-based trading strategy
trading_bot = MLTradingStrategy(api_key, secret_key, model_path, initial_balance=49870.33)

# Initialize the PortfolioTracker with initial BTC holdings
trading_bot.portfolio_tracker = PortfolioTracker(initial_balance=49870.33, initial_btc_holdings=0.4376)

# Run the bot continuously
while True:
    try:
        for pair in pairs:
            # Execute a trade for each pair
            trading_bot.execute_trade(pair, record_duration=fetch_interval)
        
        # Sleep for the fetch interval before the next iteration
        time.sleep(fetch_interval)
    except Exception as e:
        print(f"Error occurred: {e}")
        # Sleep for a short duration before retrying
        time.sleep(5)  # Wait 5 sec before retrying