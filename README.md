# Quant Portfolio Analysis

> 📝 **Article:** *[Link coming soon — a full writeup on the findings from this project will be published here]*

---

## What This Project Does

A from-scratch implementation of Modern Portfolio Theory applied to a real 8-asset portfolio, with a deliberate focus on stress-testing MPT's assumptions against empirical data.

The core question: **does mathematical optimization actually beat a naive equal-weight portfolio out-of-sample?**

The analysis covers:
- Asset-level statistics: returns, volatility, covariance matrix
- Equal-weight portfolio as a baseline (the benchmark everything is measured against)
- CAPM: predicted vs actual returns — how well does beta explain realized performance?
- MPT optimization: Tangency Portfolio (max Sharpe), Global Minimum Variance, and the full Efficient Frontier
- Sensitivity analysis: how much do optimal weights shift across different time windows?
- Out-of-sample backtest: weights fitted on years 1–3, evaluated on years 4–5 vs equal-weight

**The uncomfortable finding:** Markowitz optimization is highly sensitive to covariance inputs. Small changes in the estimation window produce large swings in optimal weights. The equal-weight portfolio, despite being mathematically "suboptimal," holds up surprisingly well out-of-sample — a direct consequence of estimation error in the covariance matrix.

---

## Assets

`TSM, AAPL, JPM, XOM, EEM, SPY, GLD, BND`

Period: 2019-01-01 to 2024-01-01 (5 years, daily adjusted close prices via Yahoo Finance)

Risk-free rate: 10-year US Treasury yield (`^TNX`), averaged over the sample period.

---

## Project Structure

```
quant-portfolio-analysis/
│
├── data/
│   ├── prices.csv          # fetched by data_loader.py, never edited manually
│   └── rfr.csv             # risk-free rate, also fetched by data_loader.py
│
├── notebooks/              # analysis and visualization — thin wrappers around src/
│   ├── 01_data_exp.ipynb
│   ├── 02_equal_weight_stats.ipynb
│   ├── 03_mpt_optimization.ipynb
│   ├── 04_capm.ipynb
│   └── 05_out_of_sample_test.ipynb
│
├── src/                    # reusable function logic
│   ├── __init__.py
│   ├── portfolio_stats.py  # returns, volatility, Sharpe, drawdowns
│   ├── optimizations.py    # MPT: tangency, GMV, efficient frontier, sensitivity
│   └── vizualizations.py  # shared plotting helpers
│
├── tests/
├── data_loader.py          # run once to fetch and save all data
├── requirements.txt
└── README.md
```

**Design principle:** notebooks contain plots and narrative. All reusable computation lives in `src/` as pure functions that accept DataFrames and return results. This makes the logic testable and independent of notebook state.

---

## Getting Started

**1. Install dependencies**

```bash
pip install -r requirements.txt
```

**2. Fetch data (run once)**

```bash
python data_loader.py
```

This pulls adjusted close prices from Yahoo Finance and saves `data/prices.csv` and `data/rfr.csv`. You only need to re-run this if you want to update the data.

**3. Run the notebooks in order**

Open the `notebooks/` folder and run them sequentially — each one assumes the previous notebook's data outputs are available.

---

## Requirements

| Package | Purpose |
|---|---|
| `pandas` | data manipulation and time series |
| `numpy` | matrix operations, return calculations |
| `matplotlib` | all plotting and visualization |
| `scipy` | portfolio optimization (`scipy.optimize`) |
| `yfinance` | fetching market data from Yahoo Finance |
| `jupyter` | running code in notebooks (ipynb files) |

Install all at once:

```bash
pip install pandas numpy matplotlib scipy yfinance
```

Or via the requirements file:

```bash
pip install -r requirements.txt
```