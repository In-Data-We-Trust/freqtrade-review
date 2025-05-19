# Freqtrade Quick Start Guide

This guide will help you quickly set up and run Freqtrade with the SimpleProfit strategy.

## Prerequisites

- Docker and Docker Compose installed
- Basic understanding of cryptocurrency trading
- Exchange account (Binance recommended)

## Step 1: Configure Your API Keys

1. Edit the `user_data/config/config.json` file and add your exchange API keys:

```json
"exchange": {
    "name": "binance",
    "key": "YOUR_API_KEY",
    "secret": "YOUR_API_SECRET",
    ...
}
```

## Step 2: Start Freqtrade

From the repository root directory, run:

```powershell
docker-compose up -d
```

This will start Freqtrade in the background using the SimpleProfit strategy.

## Step 3: Monitor Your Trades

1. **Web UI**: Access the web interface at http://localhost:8080
   - Default credentials: 
     - Username: freqtrader
     - Password: SuperSecretPassword

2. **Logs**: View the logs with:
   ```powershell
   docker-compose logs -f
   ```

## Step 4: Backtest Your Strategy

Before trading with real money, you should backtest the strategy:

```powershell
docker-compose run --rm freqtrade backtesting --strategy SimpleProfit --timerange 20240101-20240501
```

## Strategy Settings

The SimpleProfit strategy is designed to:
- Buy when RSI is below 30 and price is above the 200 SMA
- Sell when profit reaches 5% or stop loss of 5% is triggered
- Implement dollar cost averaging by adding to positions when price drops by 3%

## Configuration Options

To adjust the strategy behavior, you can modify:

1. **Risk Management**:
   - `max_open_trades`: Maximum number of simultaneous open trades
   - `stake_amount`: Amount to invest per trade
   - `stoploss`: Stop loss percentage

2. **Strategy Parameters**:
   - Edit `SimpleProfit.py` to change buy/sell indicators

3. **Dollar Cost Averaging**:
   - `dollar_cost_averaging` section in config.json controls DCA behavior

## Transitioning to Live Trading

When you're ready to trade with real money:

1. Set `"dry_run": false` in your config.json
2. Double-check your API keys have trading permissions
3. Start with a small amount of capital
4. Monitor closely for the first few days

## Getting Help

1. **Freqtrade Documentation**: https://www.freqtrade.io/en/stable/
2. **Freqtrade Discord**: https://discord.gg/p7nuUNVfP7
3. **Freqtrade GitHub**: https://github.com/freqtrade/freqtrade
