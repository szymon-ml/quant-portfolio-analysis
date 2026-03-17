import pandas as pd
import numpy as np
import yfinance as yf


def read_rfr(start_date, end_date):
    rfr = yf.download("^TNX", start=start_date, end=end_date)["Close"].mean().item() / 100
    return rfr

# market data
tickers = ["TSM", "AAPL", "JPM", "XOM", "EEM", "SPY", "GLD", "BND"]

start_date = "2019-01-01"
end_date = "2024-01-01"

data = yf.download(tickers, start=start_date, end=end_date, auto_adjust=False)[
    "Adj Close"
]

data = data.dropna()

data.to_csv("data/prices.csv", index=True)