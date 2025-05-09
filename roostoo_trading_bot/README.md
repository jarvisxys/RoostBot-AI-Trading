# RoostBot AI Trading Bot

A machine learning-based algorithmic trading bot developed for the Roostoo AI Web3 Trading Hackathon. This bot is designed to maximize portfolio returns while minimizing risk, measured through the Sharpe Ratio.

## Overview

RoostBot uses a Random Forest classifier to make trading decisions based on technical indicators like RSI (Relative Strength Index), MACD (Moving Average Convergence Divergence), and SMA (Simple Moving Average). The bot interfaces with the Roostoo exchange API to fetch real-time market data and execute trades.

## Features

- **AI-Driven Trading Strategy**: Uses machine learning to identify optimal entry and exit points
- **Real-Time Market Data Analysis**: Processes market data with technical indicators
- **Risk Management**: Implements position sizing and dynamic asset allocation
- **Portfolio Tracking**: Calculates performance metrics like Sharpe Ratio
- **Rate Limit Handling**: Built-in retry mechanisms for API rate limits
- **Error Recovery**: Robust error handling for 24/7 operation

## Project Structure

```
roostbot/
├── data/
│   ├── historical/       # Historical market data for training
│   ├── models/           # Trained machine learning models
│   └── portfolio_logs/   # Portfolio performance logs
├── src/
│   ├── api/
│   │   └── roostoo_api.py    # API client for Roostoo exchange
│   ├── strategies/
│   │   └── ml_strategy.py    # ML-based trading strategy
│   └── utils/
│       ├── data_utils.py     # Data preprocessing utilities
│       └── portfolio_utils.py # Portfolio tracking utilities
├── add_indicators.py     # Script to add technical indicators to data
├── main.py               # Entry point to run the bot
├── record_historical_data.py # Script to record historical data
└── train_model.py        # Script to train the ML model
```

## Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/roostbot.git
   cd roostbot
   ```

2. Install the required dependencies:
   ```
   pip install pandas numpy scikit-learn pandas-ta joblib requests
   ```

3. Configure your API credentials in `main.py`:
   ```python
   api_key = "YOUR_API_KEY"
   secret_key = "YOUR_SECRET_KEY"
   ```

## Usage

### Record Historical Data

```
python record_historical_data.py
```

### Add Technical Indicators to Historical Data

```
python add_indicators.py
```

### Train the ML Model

```
python train_model.py
```

### Run the Trading Bot

```
python main.py
```

## Strategy Details

RoostBot uses a combination of technical indicators and machine learning to make trading decisions:

1. **Data Collection**: Continuously fetches market data at specified intervals
2. **Feature Engineering**: Calculates technical indicators (RSI, MACD, SMA)
3. **Prediction**: Uses a trained Random Forest model to predict buy/sell signals
4. **Risk Management**: Calculates position size based on portfolio value and risk tolerance
5. **Execution**: Places orders through the Roostoo API
6. **Monitoring**: Tracks portfolio performance and calculates Sharpe Ratio

## Risk Management

The bot implements several risk management techniques:

- **Position Sizing**: Limits each trade to 2% of the total portfolio value
- **Dynamic Asset Allocation**: Allocates 20% of the portfolio to each asset
- **Stop-Loss Logic**: Uses technical indicators as implicit stop-loss mechanisms

## Performance Evaluation

Performance is primarily evaluated using the Sharpe Ratio:

```
Sharpe Ratio = (Portfolio Return - Risk-Free Rate) / Standard Deviation of Portfolio's Excess Return
```

A higher Sharpe Ratio indicates better risk-adjusted returns.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This software is for educational purposes only. Use it at your own risk. Trading cryptocurrencies involves substantial risk of loss and is not suitable for every investor.