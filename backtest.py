# -*- coding: utf-8 -*-
"""
Moving Average Crossover Backtesting Engine
Ferrari (RACE) Stock | 2018-2024
Author: pc
"""

# =============================================================================
# BLOCK 1: IMPORTS
# =============================================================================
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# =============================================================================
# BLOCK 2: DOWNLOAD HISTORICAL PRICE DATA
# yfinance returns a pandas DataFrame with OHLCV data (Open, High, Low, Close, Volume)
# We flatten the multi-level column index that yfinance sometimes produces
# =============================================================================
data = yf.download("RACE", start="2018-01-01", end="2024-01-01")
data.columns = data.columns.get_level_values(0)  # Flatten multi-level columns

# =============================================================================
# BLOCK 3: CALCULATE MOVING AVERAGES
# MA20 = 20-day rolling average (short-term trend)
# MA50 = 50-day rolling average (long-term trend)
# First 19/49 rows will be NaN as there is insufficient data to calculate
# =============================================================================
data['MA20'] = data['Close'].rolling(20).mean()
data['MA50'] = data['Close'].rolling(50).mean()

# =============================================================================
# BLOCK 4: GENERATE BUY/SELL SIGNALS
# Signal = 1 means MA20 is above MA50 (bullish), 0 means below (bearish)
# Position = diff of Signal: +1 = crossover up (buy), -1 = crossover down (sell)
# Using diff() detects state *changes* rather than states themselves
# =============================================================================
data['Signal'] = np.where(data['MA20'] >= data['MA50'], 1, 0)
data['Position'] = data['Signal'].diff()

# =============================================================================
# BLOCK 5: PORTFOLIO SIMULATION
# Starting capital: £10,000 | Transaction cost: 0.1% applied on each trade
# Buy logic: purchase maximum whole shares using floor division (//)
#            remainder cash is kept (% operator)
# Sell logic: liquidate all shares, convert to cash
# Portfolio value tracked daily: (shares × close price) + cash
# Note: iterrows() used here due to path dependency — each day's portfolio
# value depends on the previous day's state, so vectorisation is not possible
# =============================================================================
STARTING_CASH = 10000
TRANSACTION_COST = 0.001  # 0.1%

cash = STARTING_CASH
shares = 0
portfolio = []

for _, row in data.iterrows():
    if row['Position'] == 1:
        # Buy signal: invest all cash into shares
        shares = cash // row['Close']
        trade_value = shares * row['Close']
        cash = cash - trade_value  # pay for shares
        cash = cash - (trade_value * TRANSACTION_COST)  # pay commission
    elif row['Position'] == -1:
        # Sell signal: liquidate all shares
        proceeds = shares * row['Close']
        cash = cash + proceeds - (proceeds * TRANSACTION_COST)
        shares = 0

    # Record portfolio value at end of each day
    portfolio.append(shares * row['Close'] + cash)

data['Portfolio_Value'] = portfolio

# =============================================================================
# BLOCK 6: BUY AND HOLD BENCHMARK
# Simulates investing £10,000 in RACE on day one and holding until end of period
# Uses floor division to buy whole shares only, remainder stays as cash
# =============================================================================
bh_cash = STARTING_CASH
bh_shares = bh_cash // data['Close'].iloc[0]
bh_cash_remainder = bh_cash % data['Close'].iloc[0]
holdportfolio = (bh_shares * data['Close']) + bh_cash_remainder

# =============================================================================
# BLOCK 7: PERFORMANCE METRICS
# Total Return: percentage gain/loss on starting capital
# Sharpe Ratio: risk-adjusted return (annualised using √252 trading days)
#               >1.0 = good, >0.5 = acceptable, <0 = worse than risk-free rate
# Maximum Drawdown: worst peak-to-trough decline during the period
# =============================================================================

# --- Strategy metrics ---
strategy_total_return = ((data['Portfolio_Value'].iloc[-1] - STARTING_CASH) / STARTING_CASH) * 100
strategy_daily_returns = data['Portfolio_Value'].pct_change()
strategy_sharpe = (strategy_daily_returns.mean() / strategy_daily_returns.std()) * np.sqrt(252)
strategy_rolling_max = data['Portfolio_Value'].cummax()
strategy_drawdown = (data['Portfolio_Value'] - strategy_rolling_max) / strategy_rolling_max
strategy_max_drawdown = strategy_drawdown.min() * 100

# --- Buy and hold metrics ---
bh_total_return = ((holdportfolio.iloc[-1] - STARTING_CASH) / STARTING_CASH) * 100
bh_daily_returns = holdportfolio.pct_change()
bh_sharpe = (bh_daily_returns.mean() / bh_daily_returns.std()) * np.sqrt(252)
bh_rolling_max = holdportfolio.cummax()
bh_drawdown = (holdportfolio - bh_rolling_max) / bh_rolling_max
bh_max_drawdown = bh_drawdown.min() * 100

# =============================================================================
# BLOCK 8: VISUALISATION
# Chart 1 (top): RACE closing price with MA20, MA50, and buy/sell signals
# Chart 2 (bottom): Strategy portfolio value vs buy and hold benchmark
# =============================================================================
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

# --- Chart 1: Price, moving averages, and trade signals ---
ax1.plot(data.index, data['Close'], label='RACE Close Price', color='blue', linewidth=1)
ax1.plot(data.index, data['MA20'], label='MA20', color='orange', linewidth=1.2)
ax1.plot(data.index, data['MA50'], label='MA50', color='purple', linewidth=1.2)

# Filter to only rows where a crossover occurred
buy_signals = data[data['Position'] == 1]
sell_signals = data[data['Position'] == -1]

ax1.scatter(buy_signals.index, buy_signals['Close'],
            marker='^', color='green', label='Buy Signal', zorder=5, s=80)
ax1.scatter(sell_signals.index, sell_signals['Close'],
            marker='v', color='red', label='Sell Signal', zorder=5, s=80)

ax1.set_title('Ferrari (RACE) — MA20/MA50 Crossover Strategy (2018–2024)')
ax1.set_ylabel('Price (USD)')
ax1.legend()
ax1.grid(alpha=0.3)

# --- Chart 2: Portfolio value vs buy and hold benchmark ---
ax2.plot(data.index, data['Portfolio_Value'], label='MA Crossover Strategy', color='green', linewidth=1.2)
ax2.plot(data.index, holdportfolio, label='Buy and Hold Benchmark', color='blue', linewidth=1.2)

ax2.set_title('Strategy Portfolio Value vs Buy and Hold Benchmark')
ax2.set_ylabel('Portfolio Value (£)')
ax2.set_xlabel('Date')
ax2.legend()
ax2.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('backtest_results.png', dpi=150, bbox_inches='tight')
plt.show()

# =============================================================================
# BLOCK 9: RESULTS SUMMARY
# =============================================================================
print("=" * 55)
print("   BACKTEST RESULTS — FERRARI (RACE) | 2018–2024")
print("=" * 55)
print(f"{'Metric':<30} {'Strategy':>10} {'Buy & Hold':>12}")
print("-" * 55)
print(f"{'Total Return':<30} {strategy_total_return:>9.2f}% {bh_total_return:>11.2f}%")
print(f"{'Annualised Sharpe Ratio':<30} {strategy_sharpe:>10.3f} {bh_sharpe:>12.3f}")
print(f"{'Maximum Drawdown':<30} {strategy_max_drawdown:>9.2f}% {bh_max_drawdown:>11.2f}%")
print("=" * 55)
print(f"Starting Capital: £{STARTING_CASH:,}")
print(f"Transaction Cost: {TRANSACTION_COST*100}% per trade")
print(f"Crossover Events: {int(data['Position'].abs().sum())} signals over 6 years")
print("=" * 55)
