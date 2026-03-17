import pandas as pd
import numpy as np
from scipy.optimize import minimize

from src.portfolio_stats import calculate_sharpe_ratio
from src.portfolio_stats import calculate_mean_portfolio_returns
from src.portfolio_stats import calculate_volatility
from src.portfolio_stats import calculate_max_drawdown
from src.portfolio_stats import calculate_cagr


def calculate_negative_sharpe_ratio(weights, data):
    return -(calculate_sharpe_ratio(weights, data))

def optimize_portfolios(data, vol_min, vol_max, n_points):
    n = len(data.columns)
    bounds = [(0,1)] * n
    init_guess = np.ones(n) * 8

    #the list of vols we want to maximize returns for
    vol_targets = np.linspace(vol_min, vol_max, n_points)

    #maximing mean returns is minimizing negative mean returns
    def calculate_neg_mean_portfolio_returns(weights, data):
        return -(calculate_mean_portfolio_returns(weights, data))

    #creating arrays to store variables for nice reading (will later put into a dataframe):
    opt_volatilities = vol_targets.copy()
    opt_max_drawdown = np.zeros(len(vol_targets))
    opt_mean_returns = np.zeros(len(vol_targets))
    opt_cagr = np.zeros(len(vol_targets))
    opt_sharpe_ratio = np.zeros(len(vol_targets))

    #creating matrix to store weights (for later plotting):
    opt_weights_matrix = np.zeros((len(opt_volatilities), n))

    #the optimization
    for count, vol in enumerate(vol_targets):

        #set constraints
        constraints = [
            {'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1},
            {'type': 'eq', 'fun': lambda weights, v=vol: calculate_volatility(weights, data) - v}
        ]

        #optimize
        current_opt = minimize(calculate_neg_mean_portfolio_returns, init_guess, args=(data), constraints=constraints, bounds=bounds)
        current_opt_weights = current_opt.x

        print(f'calculating optimal portfolio with {vol.round(4)} annualized volatility')

        #save data
        opt_volatilities[count] = vol
        opt_max_drawdown[count] = calculate_max_drawdown(current_opt_weights, data)
        opt_mean_returns[count] = calculate_mean_portfolio_returns(current_opt_weights, data)
        opt_cagr[count] = calculate_cagr(current_opt_weights, data)
        opt_sharpe_ratio[count] = calculate_sharpe_ratio(current_opt_weights, data)

        opt_weights_matrix[count] = current_opt_weights


    #put data into DataFrame
    optimized_portfolios = pd.DataFrame({
        'Volatility': opt_volatilities,
        'Max Drawdown': opt_max_drawdown,
        'Mean Return': opt_mean_returns,
        'CAGR': opt_cagr,
        'Sharpe Ratio': opt_sharpe_ratio
    })

    #put weights into dataframe:
    weights_df = pd.DataFrame(opt_weights_matrix, columns=data.columns)

    print('')
    print('done')

    return optimized_portfolios, weights_df
    