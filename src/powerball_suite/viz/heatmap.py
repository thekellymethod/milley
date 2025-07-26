import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from powerball_suite.window import rolling_window   # absolute!

def plot_heat(df: pd.DataFrame, window: int = 100):
    rolled = rolling_window(df, window)
    sns.heatmap(rolled, cmap="rocket_r")
    plt.show()
