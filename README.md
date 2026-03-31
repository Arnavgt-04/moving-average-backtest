# Moving Average Crossover Backtesting Engine
### Ferrari (RACE) Stock | 2018–2024

A Python backtesting engine that tests whether a moving average crossover trading strategy on Ferrari's stock (NYSE: RACE) would have been profitable from 2018 to 2024.

---

## Strategy

**Rule:** When the 20-day moving average crosses *above* the 50-day moving average → **Buy**. When it crosses *below* → **Sell**.

This is one of the most widely studied systematic trading strategies. The hypothesis is that short-term momentum crossing above long-term trend signals the start of an upward move.

---

## Results

| Metric | MA Crossover Strategy | Buy & Hold Benchmark |
|---|---|---|
| Total Return | ~109% | ~234% |
| Sharpe Ratio | ~0.74 | ~0.83 |
| Maximum Drawdown | ~-27% | ~-38% |

**The strategy underperformed buy and hold on both total return and Sharpe ratio.** This was an expected finding as Ferrari had an amazingly bullish run from 2018 to 2024 and the crossover strategy periodically exits the market, inevitably missing portions of the sustained bullish uptrend over the 6-year period.

However, the strategy achieved a smaller maximum drawdown (-27% vs -38%), meaning it offered some downside protection at the cost of significant upside.

---

## Methodology & Assumptions

- **Starting capital:** £10,000
- **Transaction cost:** 0.1% per trade (applied on both buy and sell)
- **Execution:** Trades executed at same-day closing price. In practice, signals would only be known at close, so execution would realistically occur at next-day open — a known simplification.
- **Share sizing:** Whole shares only, purchased using floor division. Remainder cash is retained.
- **Benchmark:** £10,000 invested at Jan 2018 closing price, held to Jan 2024.

---

## Limitations

- **Overfitting risk:** The 20/50 MA parameters were not optimised — they were chosen as a standard pair. Testing across a range of parameters would risk overfitting to this specific stock and time period.
- **Single asset:** Results are specific to Ferrari's price behaviour during this period. A trending bull market favours buy and hold over crossover strategies by design.
- **No slippage modelled:** Real execution would involve bid/ask spread costs beyond the flat 0.1% commission.
- **Same-day execution assumption:** As noted above, real signals would only be actionable the following day.

---

## Files

```
backtest.py          — Main backtesting script
backtest_results.png — Output chart (auto-generated on run)
README.md            — This file
```

---

## Libraries

| Library | Version | Purpose |
|---|---|---|
| yfinance | latest | Download historical OHLCV price data |
| pandas | latest | DataFrame operations and time series manipulation |
| numpy | latest | Vectorised mathematical operations |
| matplotlib | latest | Chart visualisation |

---

## How to Run

```bash
pip install yfinance pandas numpy matplotlib
python backtest.py
```

---

## Background

Built as a personal project to develop Python and quantitative finance skills simultaneously. The project directly complements participation in the WorldQuant Brain alpha generation competition, where similar signal generation and backtesting concepts apply.

The choice of Ferrari (RACE) reflects personal interest in Formula 1, being a supporter of the constructor in the championship. RACE is listed on NYSE with clean historical data going back to its 2015 IPO, making the data reliable, traceable and clean.

## What I Learned

Throughout the project I learned how to translate my thought out logic into python code blocks while leveraging AI as a learning tool to understand complex python coding concepts and how to mold them to match my intention for the final program. I reinforced my understanding of 'for' loops and operators like iterrows and how to plot complex financial charts.
