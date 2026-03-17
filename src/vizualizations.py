import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from src.portfolio_stats import calculate_return_path


#plotting function for return path and drawdown
def plot_return_and_drawdown(weights, data):
    return_path = calculate_return_path(weights, data)
    return_viz_series = pd.Series(return_path, index=data.index)
    
    # Plot Return Path
    plt.figure(figsize=(12, 6))
    plt.plot(return_viz_series, label='Investment Return Path', color='blue')
    plt.axhline(y=1, color='red', linestyle='--', alpha=0.5, label='Initial Capital')
    plt.title('Portfolio (Returns)', fontsize=20, pad=15, fontweight='bold')
    plt.ylabel('Portfolio Value (Relative to Initial Capital)')
    plt.legend()
    plt.show()

    print(f'Total Return: {(return_path[-1] - 1):.2%}')
    
    # Compute and Plot Drawdowns
    drawdowns = (return_viz_series - return_viz_series.cummax()) / return_viz_series.cummax()
    plt.figure(figsize=(12, 6))
    plt.plot(drawdowns, label='Drawdown', color='orange')
    plt.axhline(0, color='black', linestyle='--', alpha=0.5)
    plt.title('Drawdown Over Time', fontsize=20, pad=15, fontweight='bold')
    plt.ylabel('Drawdown')
    plt.legend()
    plt.show()
    
    max_drawdown = drawdowns.min()
    print(f"Maximum Drawdown: {max_drawdown:.2%}")