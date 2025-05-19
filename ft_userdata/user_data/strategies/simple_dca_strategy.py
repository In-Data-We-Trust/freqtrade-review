from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame

class SimpleDCA5ProfitStrategy(IStrategy):
    """
    A simple strategy that buys and sells based on a 5% profit target.
    """

    # Minimal ROI designed for the strategy
    minimal_roi = {
        "0": 0.05  # Sell when 5% profit is reached
    }

    # Stoploss
    stoploss = -0.10  # Stoploss at 10%

    # Optimal timeframe for the strategy
    timeframe = '1h'

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Add indicators to the given DataFrame.
        """
        # No indicators needed for this simple strategy
        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Populate the buy signal based on conditions.
        """
        dataframe.loc[:, 'buy'] = 1  # Always buy
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Populate the sell signal based on conditions.
        """
        dataframe.loc[:, 'sell'] = dataframe['close'] >= dataframe['close'].shift(1) * 1.05
        return dataframe
