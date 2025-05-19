# --- Do not remove these libs ---
import numpy as np
import pandas as pd
from pandas import DataFrame
from datetime import datetime
from typing import Optional, Union

from freqtrade.strategy import (IStrategy, DecimalParameter, IntParameter, 
                               CategoricalParameter)
from freqtrade.strategy.interface import IStrategy
from freqtrade.persistence import Trade

import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib


class SimpleProfit(IStrategy):
    """
    Simple strategy aiming for 5% profit on each trade.
    This strategy uses RSI and moving averages to determine entry points,
    and exits when profit reaches 5% or stop loss is triggered.
    
    How it works:
    1. Buy when RSI is oversold (below 30) and price is above the 200 SMA
    2. Sell when profit reaches 5% or stop loss of 5% is triggered
    3. Uses minimal indicators to keep strategy simple and understandable
    
    This is designed as a beginner-friendly strategy with dollar cost averaging in mind.
    """
    
    # Strategy interface version - allow new iterations of the strategy interface.
    # Check the documentation or the Sample strategy to get the latest version.
    INTERFACE_VERSION = 3

    # Minimal ROI designed for 5% profit target
    minimal_roi = {
        "0": 0.05,  # 5% profit is our target
    }

    # Stoploss:
    stoploss = -0.05  # 5% stop loss

    # Trailing stop (disabled by default)
    trailing_stop = False
    
    # Optimal timeframe for the strategy
    timeframe = '1h'
    
    # Run "populate_indicators()" only for new candle.
    process_only_new_candles = True
    
    # These values can be overridden in the config.
    use_exit_signal = True
    exit_profit_only = False
    ignore_roi_if_entry_signal = False
    
    # Number of candles the strategy requires before producing valid signals
    startup_candle_count: int = 30
    
    # Optional parameters for fine-tuning
    buy_rsi = IntParameter(10, 40, default=30, space="buy")
    sell_rsi = IntParameter(60, 90, default=70, space="sell")
    
    def informative_pairs(self):
        """
        Define additional, informative pair/interval combinations to be cached from the exchange.
        These pair/interval combinations are non-tradeable, unless they are part
        of the whitelist as well.
        For more information, please consult the documentation
        :return: List of tuples in the format (pair, interval)
            Sample: return [("ETH/USDT", "5m"),
                            ("BTC/USDT", "15m"),
                            ]
        """
        return []

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Adds several different TA indicators to the given DataFrame

        Performance Note: For the best performance be frugal on the number of indicators
        you are using. Let uncomment only the indicator you are using in your strategies
        or your hyperopt configuration, otherwise you will waste your memory and CPU usage.
        :param dataframe: Dataframe with data from the exchange
        :param metadata: Additional information, like the currently traded pair
        :return: a Dataframe with all mandatory indicators for the strategies
        """
        
        # RSI
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
        
        # Moving Averages
        dataframe['sma_200'] = ta.SMA(dataframe, timeperiod=200)
        dataframe['sma_50'] = ta.SMA(dataframe, timeperiod=50)
        
        # MACD
        macd = ta.MACD(dataframe)
        dataframe['macd'] = macd['macd']
        dataframe['macdsignal'] = macd['macdsignal']
        dataframe['macdhist'] = macd['macdhist']
        
        # Volume
        dataframe['volume_mean_12'] = dataframe['volume'].rolling(12).mean()
        
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators, populates the entry signal for the given dataframe
        :param dataframe: DataFrame with data from the exchange
        :param metadata: Additional information, like the currently traded pair
        :return: DataFrame with entry columns populated
        """
        dataframe.loc[
            (
                # RSI oversold
                (dataframe['rsi'] < self.buy_rsi.value) &
                # Price above 200 SMA (long term trend is up)
                (dataframe['close'] > dataframe['sma_200']) &
                # Volume is above average
                (dataframe['volume'] > dataframe['volume_mean_12']) &
                # MACD histogram is positive or turning positive
                (dataframe['macdhist'] > 0)
            ),
            'enter_long'] = 1
        
        # No short entries
        dataframe.loc[:, 'enter_short'] = 0
        
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators, populates the exit signal for the given dataframe
        :param dataframe: DataFrame with data from the exchange
        :param metadata: Additional information, like the currently traded pair
        :return: DataFrame with exit columns populated
        """
        dataframe.loc[
            (
                # RSI overbought
                (dataframe['rsi'] > self.sell_rsi.value) |
                # Price below 50 SMA (medium term trend is down)
                (dataframe['close'] < dataframe['sma_50'])
            ),
            'exit_long'] = 1
        
        # No short exits
        dataframe.loc[:, 'exit_short'] = 0
        
        return dataframe
    
    def custom_exit(self, pair: str, trade: 'Trade', current_time: 'datetime', current_rate: float,
                   current_profit: float, **kwargs):
        """
        Custom exit logic, return 'target_reached' if 5% profit reached
        This helps ensure we exit exactly at 5% profit regardless of candle timeframe
        """
        if current_profit >= 0.05:
            return 'target_reached'
        
        return None
    
    def position_adjustment_enable(self, pair: str, trade: Trade, current_time: datetime, 
                                  current_rate: float, current_profit: float, **kwargs) -> bool:
        """
        Enable position adjustment (for dollar cost averaging)
        """
        # Allow averaging down when price has dropped since entry
        return current_profit < -0.02
    
    def adjust_trade_position(self, trade: Trade, current_time: datetime,
                             current_rate: float, current_profit: float, 
                             min_stake: float, max_stake: float, **kwargs) -> float:
        """
        Implement dollar cost averaging by adding to position when price drops
        """
        # Add to position if price has dropped 3% or more
        if current_profit <= -0.03:
            # Calculate adjustment based on current profit
            adjustment = 0.25  # Add 25% of initial position
            return adjustment
        
        return None  # No adjustment needed
