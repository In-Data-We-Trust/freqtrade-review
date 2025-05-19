# Dollar Cost Averaging with Freqtrade

This document outlines how to implement a Dollar Cost Averaging (DCA) strategy using Freqtrade.

## What is Dollar Cost Averaging?

Dollar Cost Averaging (DCA) is an investment strategy where you invest a fixed amount of money at regular intervals, regardless of the asset's price. This approach:

- Reduces the impact of market volatility
- Removes emotional decision-making
- Typically results in a lower average cost per unit over time

## How DCA is Implemented in Our SimpleProfit Strategy

### 1. Initial Position

When the strategy identifies a potential entry point, it opens a position with the initial stake amount defined in the configuration:

```json
"stake_amount": "20",
```

### 2. Position Adjustment Logic

The `SimpleProfit` strategy includes methods for implementing DCA:

- `position_adjustment_enable`: Determines when additional buys should be allowed
- `adjust_trade_position`: Calculates how much to add to existing positions

The strategy is configured to add to a position when:
- The current profit is below -3% (price has dropped 3% from entry)
- The additional buy amount is 25% of the initial position

### 3. Maximum Entries and Stake

To control risk, we limit how much can be invested in a single position:

```json
"dollar_cost_averaging": {
    "enabled": true,
    "initial_stake": 20,
    "max_stake": 100,
    "max_entries": 4,
    "schedule": "weekly"
}
```

This configuration means:
- Initial position: $20
- Maximum investment in any single coin: $100
- Maximum number of entries for DCA: 4
- Regular schedule: Weekly

## Customizing Your DCA Strategy

### Adjusting the DCA Parameters

To modify the DCA behavior for your risk tolerance:

1. **Change trigger points**: Edit the `position_adjustment_enable` method in `SimpleProfit.py`
   ```python
   # Change the threshold from -0.02 to your desired value
   return current_profit < -0.02
   ```

2. **Adjust the DCA amount**: Modify the `adjust_trade_position` method
   ```python
   # Change the adjustment value from 0.25 to your desired percentage
   adjustment = 0.25  # Percentage of initial position
   ```

3. **Update the configuration**: Edit the `dollar_cost_averaging` section in `config.json`

### Different DCA Strategies

1. **Fixed Interval DCA**: Buy at regular time intervals regardless of price
   - Set `schedule` to "daily", "weekly", or "monthly"

2. **Threshold-based DCA**: Buy when price drops by certain percentages
   - Current implementation uses this approach

3. **Scaled DCA**: Increase buy amounts as price drops further
   - Modify `adjust_trade_position` to return larger percentages at lower profit levels

## Monitoring Your DCA Strategy

1. Use the Freqtrade web UI to track your positions and average entry prices
2. Enable Telegram notifications to get updates on new DCA buys
3. Run regular backtests to validate your DCA parameters

## Risk Management with DCA

1. **Set maximum exposure**: Limit the total capital allocated to DCA
2. **Use stoploss**: Always maintain a stoploss, even with DCA strategies
3. **Limit DCA levels**: Don't indefinitely average down; set a maximum number of entries
