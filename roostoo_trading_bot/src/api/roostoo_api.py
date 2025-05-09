# Code for fetching market data and executing trades
import requests
import time
import hmac
import hashlib
import pandas as pd
from datetime import datetime

class RoostooAPI:
    def __init__(self, api_key, secret_key):
        """
        Initialize the Roostoo API client.

        Args:
            api_key (str): Your Roostoo API key.
            secret_key (str): Your Roostoo API secret key.
        """
        self.api_key = api_key
        self.secret_key = secret_key
        self.base_url = "https://mock-api.roostoo.com/v3"

    def _generate_signature(self, params):
        """
        Generate HMAC SHA256 signature for API requests.

        Args:
            params (dict): Dictionary of request parameters.

        Returns:
            str: HMAC SHA256 signature.
        """
        query_string = "&".join([f"{k}={v}" for k, v in sorted(params.items())])
        return hmac.new(self.secret_key.encode(), query_string.encode(), hashlib.sha256).hexdigest()

    def fetch_market_data(self, pair, max_retries=3, retry_delay=1):
        """
        Fetch real-time market data for a trading pair with rate limit handling.

        Args:
            pair (str): Trading pair (e.g., "BTC/USD").
            max_retries (int): Maximum number of retries on rate limit errors (default: 3).
            retry_delay (int): Delay (in seconds) between retries (default: 1 second).

        Returns:
            pd.DataFrame: DataFrame containing market data with a 'close' column.
        """
        retries = 0
        while retries < max_retries:
            try:
                endpoint = f"{self.base_url}/ticker"
                params = {
                    "pair": pair,
                    "timestamp": int(time.time() * 1000)  # Current timestamp in milliseconds
                }
                signature = self._generate_signature(params)
                headers = {
                    "RST-API-KEY": self.api_key,
                    "MSG-SIGNATURE": signature
                }
                response = requests.get(endpoint, headers=headers, params=params)
                
                # Handle rate limit errors
                if response.status_code == 429:
                    print(f"Rate limit exceeded. Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    retries += 1
                    continue

                # Handle other errors
                if response.status_code != 200:
                    raise Exception(f"Failed to fetch market data: {response.status_code} - {response.text}")

                # Parse the API response
                data = response.json()
                if data.get("Success"):
                    pair_data = data["Data"].get(pair)
                    if pair_data:
                        market_data = pd.DataFrame([pair_data])
                        market_data.rename(columns={"LastPrice": "close"}, inplace=True)
                        return market_data
                    else:
                        raise Exception(f"No data found for pair: {pair}")
                else:
                    raise Exception(f"API returned an error: {data.get('ErrMsg')}")
            except Exception as e:
                print(f"Error fetching market data: {e}")
                retries += 1
                time.sleep(retry_delay)

        raise Exception(f"Failed to fetch market data after {max_retries} retries.")

    def place_order(self, pair, side, quantity, order_type="MARKET"):
        """
        Place an order using the Roostoo API.

        Args:
            pair (str): Trading pair (e.g., "BTC/USD").
            side (str): Order side ("BUY" or "SELL").
            quantity (float): Quantity of the asset to trade.
            order_type (str): Order type ("MARKET" or "LIMIT").

        Returns:
            dict: Response from the API.
        """
        endpoint = f"{self.base_url}/place_order"
        params = {
            "pair": pair,
            "side": side.upper(),  # BUY or SELL
            "type": order_type.upper(),  # MARKET or LIMIT
            "quantity": str(quantity),
            "timestamp": int(time.time() * 1000)  # Current timestamp in milliseconds
        }
        signature = self._generate_signature(params)
        headers = {
            "RST-API-KEY": self.api_key,
            "MSG-SIGNATURE": signature
        }
        response = requests.post(endpoint, headers=headers, data=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to place order: {response.status_code} - {response.text}")


class DataRecorder:
    def __init__(self, api, pair, fetch_interval=10):
        """
        Initialize the DataRecorder.

        Args:
            api (RoostooAPI): Instance of the Roostoo API client.
            pair (str): Trading pair (e.g., "BTC/USD").
            fetch_interval (int): Time interval (in seconds) between data fetches.
        """
        self.api = api
        self.pair = pair
        self.fetch_interval = fetch_interval
        self.data = []  # List to store market data

    def record(self, duration_sec):
        """
        Record market data for a specified duration.

        Args:
            duration_sec (int): Duration (in seconds) to record data.
        """
        print(f"Recording market data for {duration_sec} seconds...")
        start_time = time.time()
        while time.time() - start_time < duration_sec:
            try:
                # Fetch market data with rate limit handling
                market_data = self.api.fetch_market_data(self.pair)
                if market_data is not None:
                    # Add formatted timestamp and price to the data list
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Format timestamp
                    self.data.append({
                        "timestamp": timestamp,  # Use formatted timestamp
                        "close": market_data["close"].iloc[0]  # Use the latest price
                    })
                    print(f"Recorded data: {self.data[-1]}")
                else:
                    print("Failed to fetch market data.")
            except Exception as e:
                print(f"Error during data recording: {e}")
            
            # Sleep for the fetch interval before the next iteration
            time.sleep(self.fetch_interval)
        print("Data recording completed.")

    def get_dataframe(self):
        """
        Convert recorded data to a DataFrame.

        Returns:
            pd.DataFrame: DataFrame containing recorded market data.
        """
        return pd.DataFrame(self.data)
    
    def save_to_csv(self, file_path):
        """
        Save the recorded data to a CSV file.

        Args:
            file_path (str): Path to save the CSV file.
        """
        df = self.get_dataframe()
        df.to_csv(file_path, index=False)
        print(f"Data saved to {file_path}")


# Example usage
if __name__ == "__main__":
    # Replace with your actual API key and secret key
    api_key = "xSh5rchczNi8bC0086086700kj8JHNTMNxhFemJIepIrf2vJuv0ekP4h6dGKCcpM"
    secret_key = "G0dplHtb6rc9oPhmh5ygTNUFaSAvnQ6FTOn6mnkugwwFryJlmA1MjxH2JsmenCbr"

    # Initialize the Roostoo API client
    roostoo_api = RoostooAPI(api_key, secret_key)

    # Example: Record market data for 60 seconds
    recorder = DataRecorder(roostoo_api, "BTC/USD", fetch_interval=10)
    recorder.record(60)
    recorded_data = recorder.get_dataframe()
    print("Recorded Data:")
    print(recorded_data)