# Stock Trading Automation System

A comprehensive stock trading automation system that combines technical analysis, machine learning, and automated alerting for NIFTY 50 stocks.

## Features

- **Data Fetching**: Automated fetching of stock data using Yahoo Finance API
- **Technical Analysis**: RSI + Moving Average crossover strategy
- **Machine Learning**: Logistic Regression model for price movement prediction
- **Automated Alerts**: Telegram notifications for trading signals
- **Google Sheets Integration**: Automated logging of trades and P&L
- **Scheduling**: Automated scans at market hours

## Project Structure

```
stock/
├── main.py              # Main execution script
├── config.py            # Configuration and environment variables
├── data_handler.py      # Stock data fetching and processing
├── strategy.py          # Trading strategy implementation
├── ml_model.py          # Machine learning model
├── sheets_manager.py    # Google Sheets integration
├── alerter.py          # Telegram alerting system
├── setup.py            # Setup script for configuration
├── requirements.txt     # Python dependencies
└── README.md           # Project documentation
```

## Quick Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Setup Script
```bash
python setup.py
```

This will guide you through:
- Telegram bot configuration
- Google Sheets setup (optional)
- Testing both connections

### 3. Run the System
```bash
# Single scan
python main.py

# Scheduled scans
python main.py --schedule
```

## Configuration

### Telegram Setup
1. Create a bot using @BotFather on Telegram
2. Get the bot token
3. Send a message to your bot
4. Get your chat ID from the API
5. Run `python setup.py` to configure

### Google Sheets Setup (Optional)
1. Create a Google Cloud Project
2. Enable Google Sheets API
3. Create a service account and download credentials JSON
4. Create a Google Sheet and share it with the service account
5. Run `python setup.py` to configure

## Usage

### Single Scan
```bash
python main.py
```

### Scheduled Scans
```bash
python main.py --schedule
```

This will run automated scans:
- Daily at 9:30 AM (market open)
- Hourly from 10:00 AM to 3:00 PM

## Features in Detail

### Trading Strategy
- **RSI Strategy**: Buy when RSI < 30 (oversold)
- **Moving Average Crossover**: Buy when 20-DMA crosses above 50-DMA
- **Sell Signal**: Sell when 20-DMA crosses below 50-DMA

### Machine Learning Model
- Uses Logistic Regression
- Features: RSI, MACD, Volume
- Predicts next-day price movement
- Reports prediction accuracy

### Alerting System
- Sends Telegram alerts for buy signals
- Includes stock ticker, buy price, and date
- Supports Markdown formatting

### Google Sheets Integration
- **Trade Log**: Detailed trade information with P&L
- **Summary P&L**: Overall performance metrics
- **ML Analytics**: Model prediction accuracy

## What You'll See

### Telegram Alerts
```
🚨 *RELIANCE.NS* Buy Signal Alert!
💰 Buy Price: ₹2450.50
📅 Date: 2024-01-15
⏰ Time: 14:30:25
```

### Google Sheets Data
**Trade Log Sheet:**
| Ticker | Buy Date | Buy Price | Sell Date | Sell Price | P&L |
|--------|----------|-----------|-----------|------------|-----|
| RELIANCE.NS | 2024-01-15 | 2450.50 | 2024-01-20 | 2480.00 | 29.50 |

**Summary P&L Sheet:**
| Metric | Value |
|--------|-------|
| Total P&L | 29.50 |
| Total Trades | 1 |
| Win Ratio (%) | 100.00 |

## Dependencies

- `yfinance`: Stock data fetching
- `pandas`: Data manipulation
- `scikit-learn`: Machine learning
- `gspread`: Google Sheets integration
- `python-telegram-bot`: Telegram alerts
- `schedule`: Task scheduling
- `requests`: HTTP requests

## Notes

- Minimum 50 days of data required for technical analysis
- Market hours: 9:30 AM to 3:30 PM IST
- All times are in local system timezone
- Ensure stable internet connection for data fetching 