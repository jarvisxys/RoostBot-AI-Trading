import sys
from src.api.roostoo_api import RoostooAPI

class SolanaTrader:
    def __init__(self, api_key, secret_key):
        """
        Initialize the Solana trader.

        Args:
            api_key (str): Roostoo API key.
            secret_key (str): Roostoo API secret key.
        """
        self.api = RoostooAPI(api_key, secret_key)
        self.pair = "SOL/USD"  # Trading pair

    def execute_buy_order(self, quantity):
        """
        Execute a buy order for the specified quantity of SOL.

        Args:
            quantity (float): Quantity of SOL to purchase.
        """
        try:
            # Execute the buy order
            print(f"Executing BUY order for {self.pair} with quantity {quantity}...")
            order_response = self.api.place_order(self.pair, "BUY", quantity)
            print(f"Order Response: {order_response}")
        except Exception as e:
            print(f"Error occurred during trade execution: {e}")

def main():
    # API credentials
    api_key = "xSh5rchczNi8bC0086086700kj8JHNTMNxhFemJIepIrf2vJuv0ekP4h6dGKCcpM"
    secret_key = "G0dplHtb6rc9oPhmh5ygTNUFaSAvnQ6FTOn6mnkugwwFryJlmA1MjxH2JsmenCbr"

    # Check if the quantity argument is provided
    if len(sys.argv) != 2:
        print("Usage: python buy_sol.py <quantity>")
        sys.exit(1)

    try:
        # Parse the quantity argument
        quantity = float(sys.argv[1])
        if quantity <= 0:
            print("Quantity must be a positive number.")
            sys.exit(1)

        # Initialize the Solana trader
        trader = SolanaTrader(api_key, secret_key)

        # Execute the buy order
        trader.execute_buy_order(quantity)
    except ValueError:
        print("Invalid quantity. Please provide a valid number.")
        sys.exit(1)

if __name__ == "__main__":
    main()