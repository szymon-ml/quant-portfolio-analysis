import pandas as pd
import numpy as np
from data_loader import read_rfr

trading_days = 252
start_date = "2019-01-01"
end_date = "2024-01-01"
rfr = read_rfr(start_date, end_date)

# VOLATILITY
def calculate_volatility(weights, data):
    portfolio_returns = data.pct_change() @ weights
    annualized_variance = portfolio_returns.var() * trading_days
    annualized_volatility = np.sqrt(annualized_variance)
    return annualized_volatility

# MAX DRAWDOWN
def calculate_max_drawdown(weights, data):
    return_path = pd.Series(calculate_return_path(weights, data))
    cum_max = return_path.cummax()
    drawdowns = (cum_max - return_path) / cum_max
    max_drawdown = max(drawdowns[1:])
    return max_drawdown


# MEAN PORTFOLIO RETURNS
def calculate_mean_portfolio_returns(weights, data):
    portfolio_returns = data.pct_change() @ weights
    annualized_return = portfolio_returns.mean() * trading_days
    return annualized_return


def calculate_return_path(weights, data):
    simple_port_ret = data.pct_change() @ weights
    log_port_ret = np.log(1 + simple_port_ret)
    return_path = np.exp(log_port_ret.cumsum())
    return return_path.to_numpy()


# COMPOUND ANNUAL GROWTH RATE (actual)
def calculate_cagr(weights, data):
    years = data.shape[0] / 252
    cagr = (calculate_return_path(weights, data)[-1]) ** (1 / years) - 1
    return cagr

#SHARPE RATIO
def calculate_sharpe_ratio(weights, data):
    sharpe_ratio = (calculate_mean_portfolio_returns(weights, data) - rfr) / calculate_volatility(weights, data)
    return sharpe_ratio