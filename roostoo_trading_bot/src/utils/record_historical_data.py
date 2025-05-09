# script to record data(Historical data) for 4 hours (14,400 seconds) and save it to a CSV file.
from src.api.roostoo_api import RoostooAPI, DataRecorder

# Configuration
api_key = "xSh5rchczNi8bC0086086700kj8JHNTMNxhFemJIepIrf2vJuv0ekP4h6dGKCcpM"
secret_key = "G0dplHtb6rc9oPhmh5ygTNUFaSAvnQ6FTOn6mnkugwwFryJlmA1MjxH2JsmenCbr"
pair = "BTC/USD"  # Trading pair
fetch_interval = 5  # Fetch data every 10 seconds
record_duration = 10800  # Record data for 4 hours (14,400 seconds)
output_file = "data/historical/market_data.csv"  # Path to save the CSV file

# Initialize the Roostoo API client
roostoo_api = RoostooAPI(api_key, secret_key)

# Initialize the DataRecorder
recorder = DataRecorder(roostoo_api, pair, fetch_interval=fetch_interval)

# Record market data
recorder.record(record_duration)

# Save the recorded data to a CSV file
recorder.save_to_csv(output_file)
