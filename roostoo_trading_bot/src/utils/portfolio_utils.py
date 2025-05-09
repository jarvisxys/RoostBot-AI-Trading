import pandas as pd
import numpy as np
import os

class PortfolioTracker:
    def __init__(self, initial_balance=49870.33, initial_btc_holdings=0.4376):
        """
        Initialize the portfolio tracker for multiple assets.

        Args:
            initial_balance (float): Initial balance in the portfolio (default: $10,000).
            initial_btc_holdings (float): Initial BTC holdings (default: 0.0).
        """
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.portfolio_value = initial_balance
        self.returns = []  # List to store daily returns
        self.portfolio_logs = []  # List to store portfolio performance logs
        self.asset_allocation = {}  # Dictionary to track allocation for each asset
        self.btc_holdings = initial_btc_holdings  # Track BTC holdings
        self.log_file = "data/portfolio_logs/portfolio_performance.csv"

        # Create the portfolio logs directory if it doesn't exist
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        

    def update_portfolio_value(self, current_value, asset=None):
        """
        Update the portfolio value and calculate returns.

        Args:
            current_value (float): Current value of the portfolio.
            asset (str, optional): Name of the asset being traded (e.g., "BTC/USD").
        """
        self.portfolio_value = current_value
        daily_return = (self.portfolio_value - self.balance) / self.balance
        self.returns.append(daily_return)
        self.balance = self.portfolio_value

        # Update asset allocation
        if asset:
            self.asset_allocation[asset] = current_value

    def update_btc_holdings(self, quantity, action):
        """
        Update BTC holdings based on the trade action.

        Args:
            quantity (float): Quantity of BTC traded.
            action (str): "BUY" or "SELL".
        """
        if action == "BUY":
            self.btc_holdings += quantity
        elif action == "SELL":
            self.btc_holdings -= quantity

    def get_btc_holdings(self):
        """
        Get the current BTC holdings.

        Returns:
            float: Current BTC holdings.
        """
        return self.btc_holdings

    def calculate_sharpe_ratio(self, risk_free_rate=0.01):
        """
        Calculate the Sharpe Ratio for the portfolio.

        Args:
            risk_free_rate (float): Risk-free rate (default: 1%).

        Returns:
            float: Sharpe Ratio.
        """
        if len(self.returns) == 0:
            return 0.0

        # Calculate the average return and standard deviation
        avg_return = np.mean(self.returns)
        std_dev = np.std(self.returns)

        # Avoid division by zero
        if std_dev == 0:
            return 0.0

        # Calculate the Sharpe Ratio
        sharpe_ratio = (avg_return - risk_free_rate) / std_dev
        return sharpe_ratio

    def log_portfolio_performance(self):
        """
        Log the portfolio performance to a CSV file.
        """
        performance_data = {
            "Portfolio Value": self.portfolio_value,
            "Daily Return": self.returns[-1] if self.returns else 0.0,
            "Sharpe Ratio": self.calculate_sharpe_ratio(),
            "Asset Allocation": self.asset_allocation,
            "BTC Holdings": self.btc_holdings,
        }
        self.portfolio_logs.append(performance_data)

        # Save the logs to a CSV file
        df = pd.DataFrame(self.portfolio_logs)
        df.to_csv(self.log_file, index=False)

    def get_portfolio_summary(self):
        """
        Get a summary of the portfolio performance.

        Returns:
            dict: Portfolio performance summary.
        """
        return {
            "Initial Balance": self.initial_balance,
            "Current Portfolio Value": self.portfolio_value,
            "Total Returns (%)": (self.portfolio_value - self.initial_balance) / self.initial_balance * 100,
            "Sharpe Ratio": self.calculate_sharpe_ratio(),
            "Asset Allocation": self.asset_allocation,
            "BTC Holdings": self.btc_holdings,
        }

    def get_asset_allocation(self):
        """
        Get the current allocation of assets in the portfolio.

        Returns:
            dict: Dictionary with asset names as keys and their values as values.
        """
        return self.asset_allocation