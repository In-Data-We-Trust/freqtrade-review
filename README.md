# Freqtrade Crypto Trading Bot Guide

This repository contains a setup for the Freqtrade crypto trading bot with a simple profitable strategy and dollar cost averaging implementation.

## What is Freqtrade?

Freqtrade is an open-source crypto trading bot written in Python. It implements a range of technical analysis indicators and provides a backtesting and hyperopt (optimization) framework.

## Quick Start Guide

1. [Setting Up Freqtrade with Docker](#setup)
2. [Simple 5% Profit Strategy](#strategy)
3. [Dollar Cost Averaging Implementation](#dca)
4. [Monitoring and Tracking](#monitoring)
5. [Backtesting Your Strategy](#backtesting)

<a name="setup"></a>
## Setting Up Freqtrade with Docker

### Prerequisites
- Docker installed on your system
- Basic knowledge of command line
- Exchange API keys (Binance recommended for beginners)

### Installation Steps

1. **Pull the Freqtrade Docker image**:
   ```bash
   docker pull freqtradeorg/freqtrade:stable
   ```

2. **Create the configuration**:
   Run the following command to create a new configuration:
   ```bash
   docker run -it --rm --user $(id -u):$(id -g) -v $(pwd)/user_data:/freqtrade/user_data freqtradeorg/freqtrade:stable create-userdir --userdir user_data
   ```

3. **Configure your API keys**:
   Edit the `user_data/config.json` file and add your exchange API keys.

4. **Run Freqtrade**:
   ```bash
   docker run -d --name freqtrade -v $(pwd)/user_data:/freqtrade/user_data freqtradeorg/freqtrade:stable trade --strategy SimpleProfit --config user_data/config.json
   ```

<a name="strategy"></a>
## Simple 5% Profit Strategy

The `SimpleProfit` strategy is designed to:
1. Buy coins based on basic indicators (RSI and moving averages)
2. Sell when profit reaches 5% or stop loss is triggered
3. Implement a simple but effective approach for beginners

See the strategy file at `user_data/strategies/SimpleProfit.py`.

<a name="dca"></a>
## Dollar Cost Averaging Implementation

The DCA implementation in this repository:
1. Allocates a fixed amount of capital for each trade
2. Spreads buys over time to average the purchase price
3. Can be adjusted based on market conditions

Configuration is done via the `config.json` file.

<a name="monitoring"></a>
## Monitoring and Tracking

1. **Real-time monitoring**:
   ```bash
   docker logs -f freqtrade
   ```

2. **Web UI**:
   Enable the web UI in your config and access it at `http://localhost:8080`.

3. **Telegram integration**:
   Configure Telegram in your config for mobile notifications.

<a name="backtesting"></a>
## Backtesting Your Strategy

Before live trading, always backtest your strategy:
```bash
docker run -it --rm -v $(pwd)/user_data:/freqtrade/user_data freqtradeorg/freqtrade:stable backtesting --strategy SimpleProfit --timerange 20210101-20210201
```

## Disclaimer

Trading cryptocurrencies involves significant risk. This project is for educational purposes only. Always start with small amounts and never trade with money you cannot afford to lose.
