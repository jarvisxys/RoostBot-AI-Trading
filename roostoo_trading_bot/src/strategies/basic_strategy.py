# Basic trading strategy

import pandas as pd
import pandas_ta as ta
from src.api.roostoo_api import RoostooAPI   #roostoo_trading_bot\src\api\roostoo_api.py

class BasicTradingStrategy:
    def __init__(self, api_key, secret_key):
        self.api = RoostooAPI(api_key, secret_key)

    def analyze_market_data(self, market_data):
        """
        Analyze market data by calculating technical indicators.
        """
        # Ensure 'close' column exists
        if 'close' not in market_data.columns:
            raise ValueError("Market data must contain a 'close' column.")

        # Calculate RSI (Relative Strength Index)
        market_data['RSI'] = ta.rsi(market_data['close'], length=14)

        # Calculate MACD (Moving Average Convergence Divergence)
        macd = ta.macd(market_data['close'], fast=12, slow=26, signal=9)
        market_data = pd.concat([market_data, macd], axis=1)

        # Drop rows with NaN values (due to indicator calculations)
        market_data.dropna(inplace=True)

        return market_data


    def decide_trade(self, market_data):
        """
        Decide whether to buy, sell, or hold based on technical indicators.
        Returns 'BUY', 'SELL', or None.
        """
        # Check if required columns exist
        if 'RSI' not in market_data.columns or 'MACD_12_26_9' not in market_data.columns:
            print("Required indicators (RSI or MACD) are missing. No trade action taken.")
            return None

        # Example: Buy if RSI < 30 (oversold) and MACD > 0 (bullish)
        last_row = market_data.iloc[-1]
        if last_row['RSI'] < 30 and last_row['MACD_12_26_9'] > 0:
            return "BUY"
        elif last_row['RSI'] > 70 and last_row['MACD_12_26_9'] < 0:
            return "SELL"
        else:
            return None
        

    def execute_trade(self, pair, quantity):
        """
        Execute a trade based on the strategy's decision.
        """
        # Fetch market data
        market_data = self.api.fetch_market_data(pair)

        # Analyze market data (calculate indicators)
        market_data = self.analyze_market_data(market_data)

        # Check if market_data is empty after preprocessing
        if market_data.empty:
            print("No valid data after preprocessing. No trade action taken.")
            return

        # Decide trade action
        decision = self.decide_trade(market_data)

        # Execute trade if a decision is made
        if decision:
            print(f"Executing {decision} order for {pair}...")
            order_response = self.api.place_order(pair, decision, quantity)
            print("Order Response:", order_response)
        else:
            print("No trade action taken.")