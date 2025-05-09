import pandas as pd
import joblib
from src.api.roostoo_api import RoostooAPI
from src.api.roostoo_api import DataRecorder
from src.utils.data_utils import preprocess_data
from src.utils.portfolio_utils import PortfolioTracker

class MLTradingStrategy:
    def __init__(self, api_key, secret_key, model_path, initial_balance=49870.33):
        """
        Initialize the ML-based trading strategy.

        Args:
            api_key (str): Roostoo API key.
            secret_key (str): Roostoo API secret key.
            model_path (str): Path to the trained ML model.
            initial_balance (float): Initial balance in the portfolio (default: $10,000).
        """
        self.api = RoostooAPI(api_key, secret_key)
        self.model = joblib.load(model_path)
        self.portfolio_tracker = PortfolioTracker(initial_balance)
        self.risk_per_trade = 0.02  # Risk 2% of the portfolio per trade
        self.asset_allocation = {}  # Dictionary to store allocation for each asset

    def decide_trade(self, market_data):
        """
        Use the ML model to decide whether to buy or sell.

        Args:
            market_data (pd.DataFrame): Market data with technical indicators.

        Returns:
            str: "BUY", "SELL", or None.
        """
        # Ensure the required features are present
        required_features = ['RSI', 'SMA_20', 'MACD_12_26_9', 'MACDs_12_26_9', 'MACDh_12_26_9']
        if not all(feature in market_data.columns for feature in required_features):
            print("Missing required features. No trade action taken.")
            return None

        # Use the latest data point for prediction
        latest_data = market_data.iloc[-1]
        features = latest_data[required_features].values.reshape(1, -1)

        # Convert features to a DataFrame with correct feature names
        features_df = pd.DataFrame(features, columns=required_features)

        # Make a prediction
        prediction = self.model.predict(features_df)
        
        # Additional rules
        rsi = latest_data['RSI']
        sma_20 = latest_data['SMA_20']
        latest_price = latest_data['close']

        # Trend filter: Only take BUY signals in an uptrend
        if prediction == 1 and latest_price > sma_20:
            return "BUY"
        # Only take SELL signals in a downtrend
        elif prediction == 0 and latest_price < sma_20:
            return "SELL"
        else:
            print("No trade action taken based on additional rules.")
            return None


    def calculate_quantity(self, latest_price, action, pair):
        """
        Calculate the quantity to buy or sell based on risk management and asset allocation.

        Args:
            latest_price (float): Latest price of the asset.
            action (str): "BUY" or "SELL".
            pair (str): Trading pair (e.g., "BTC/USD").

        Returns:
            float: Quantity to trade.
        """
        portfolio_value = self.portfolio_tracker.portfolio_value
        risk_amount = portfolio_value * self.risk_per_trade  # Risk 2% of the portfolio

        # Dynamic allocation: Allocate 20% of the portfolio to each asset
        allocation_percentage = 0.20  # 20% per asset
        allocated_amount = portfolio_value * allocation_percentage

        # Calculate quantity based on allocated amount
        quantity = allocated_amount / latest_price
        return round(quantity, 4)  # Round to 4 decimal places
    

    def execute_trade(self, pair, record_duration=300, fetch_interval=5):
        """
        Execute a trade based on the ML model's decision.

        Args:
            pair (str): Trading pair (e.g., "BTC/USD").
            record_duration (int): Duration (in seconds) to record market data (default: 300 seconds).
            fetch_interval (int): Time interval (in seconds) between data fetches (default: 5 seconds).
        """
        try:
            # Record market data
            recorder = DataRecorder(self.api, pair, fetch_interval=fetch_interval)
            recorder.record(record_duration)
            market_data = recorder.get_dataframe()

            # Preprocess and analyze market data
            market_data = preprocess_data(market_data)

            # Check if market_data is empty after preprocessing
            if market_data.empty:
                print(f"No valid data for {pair} after preprocessing. No trade action taken.")
                return

            # Decide trade action (only BUY or SELL)
            decision = self.decide_trade(market_data)

            # Execute trade if a decision is made
            if decision == "BUY" or decision == "SELL":
                latest_price = market_data['close'].iloc[-1]
                quantity = self.calculate_quantity(latest_price, decision, pair)

                # Check available BTC holdings for SELL orders
                if decision == "SELL":
                    btc_holdings = self.portfolio_tracker.get_btc_holdings()
                    if btc_holdings <= 0:
                        print(f"Insufficient BTC holdings to SELL {pair}. Available BTC: {btc_holdings}")
                        return
                    # Adjust quantity to available BTC holdings
                    quantity = min(quantity, btc_holdings)

                print(f"Executing {decision} order for {pair} with quantity {quantity}...")
                order_response = self.api.place_order(pair, decision, quantity)
                print(f"Order Response: {order_response}")

                # Only update portfolio value if the order was successful
                if order_response.get("Success"):
                    # Calculate the value of the trade
                    trade_value = latest_price * quantity
                    if decision == "BUY":
                        # Deduct the trade value from the portfolio for a BUY order
                        current_value = self.portfolio_tracker.portfolio_value - trade_value
                    elif decision == "SELL":
                        # Add the trade value to the portfolio for a SELL order
                        current_value = self.portfolio_tracker.portfolio_value + trade_value

                    # Update portfolio value after the trade
                    self.portfolio_tracker.update_portfolio_value(current_value, asset=pair)

                    # Update BTC holdings
                    self.portfolio_tracker.update_btc_holdings(quantity, decision)

                    # Log portfolio performance
                    self.portfolio_tracker.log_portfolio_performance()

                    # Print portfolio summary
                    print(f"Portfolio Summary: {self.portfolio_tracker.get_portfolio_summary()}")
                else:
                    print(f"Order failed. No changes to portfolio value.")
            else:
                print(f"No trade action taken for {pair}.")
        except Exception as e:
            print(f"Error occurred during trade execution: {e}")

    def calculate_portfolio_value(self, market_data, quantity):
        """
        Calculate the current portfolio value.

        Args:
            market_data (pd.DataFrame): Market data for the trading pair.
            quantity (float): Quantity of the asset traded.

        Returns:
            float: Current portfolio value.
        """
        # Example: Calculate portfolio value based on the latest price
        latest_price = market_data['close'].iloc[-1]
        return self.portfolio_tracker.portfolio_value + (latest_price * quantity)