import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import DateFormatter

class IndicatorPlotter:
    def __init__(self, indicators: pd.DataFrame, sharpe_windows=[20, 60, 120], date_col='date'):
        """
        Parameters
        ----------
        indicators : pd.DataFrame
            DataFrame containing all indicators.
        sharpe_windows : list[int]
            List of rolling windows for Sharpe ratios.
        date_col : str
            Column name to use as x-axis. Defaults to 'date'.
        """
        self.sharpe_windows = sharpe_windows
        self.indicators = indicators.copy()
        
        # Ensure the x-axis is datetime
        if date_col in self.indicators.columns:
            self.indicators.index = pd.to_datetime(self.indicators[date_col])
        elif not pd.api.types.is_datetime64_any_dtype(self.indicators.index):
            raise ValueError("Index must be datetime or specify a valid date_col")

    def _format_xaxis(self, ax):
        ax.xaxis.set_major_formatter(DateFormatter("%Y-%m-%d"))
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

    def plot_price_bands(self):
        fig, ax = plt.subplots(figsize=(14, 6))
        
        # Price
        ax.plot(self.indicators.index, self.indicators["vw"], label="VWAP", color="black")
        
        # SMA / EMA
        for col, color in {
            "sma_short": "#1f77b4",  # blue
            "sma_long": "#0b3d91",   # dark blue
            "ema_short": "#BD608D",  # teal
            "ema_long": "#DA1233"    # dark teal
        }.items():
            ax.plot(self.indicators.index, self.indicators[col], label=col.replace("_", " ").title(), color=color)
        
        # Bollinger Bands
        ax.plot(self.indicators.index, self.indicators["bb_mid"], label="Bollinger Band Mid", color="#ff7f0e")  # mid band
        ax.fill_between(
            self.indicators.index,
            self.indicators["bb_lower"],
            self.indicators["bb_upper"],
            color="lightgray",
            alpha=0.3,
            label="Bollinger Bands Range"
        )
        
        ax.set_title("Price, Moving Averages & Bollinger Bands")
        ax.legend()
        ax.grid(True)
        self._format_xaxis(ax)
        plt.show()


    def plot_momentum_rsi(self):
        fig, ax1 = plt.subplots(figsize=(14, 4))
        ax1.plot(self.indicators.index, self.indicators["momentum"], label="Momentum", color="green")
        ax1.set_ylabel("Momentum", color="green")
        ax1.tick_params(axis='y', labelcolor="green")

        ax2 = ax1.twinx()
        ax2.plot(self.indicators.index, self.indicators["rsi"], label="RSI (14)", color="blue")
        ax2.set_ylabel("RSI", color="blue")
        ax2.tick_params(axis='y', labelcolor="blue")
        ax2.set_ylim(0, 110)

        # Combine legends
        lines_1, labels_1 = ax1.get_legend_handles_labels()
        lines_2, labels_2 = ax2.get_legend_handles_labels()
        ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc="upper left")

        ax1.set_title("Momentum & RSI")
        ax1.grid(True)
        self._format_xaxis(ax1)
        plt.show()

    def plot_macd(self):
        fig, ax = plt.subplots(figsize=(14, 4))
        ax.plot(self.indicators.index, self.indicators["macd"], label="MACD", color="purple")
        ax.plot(self.indicators.index, self.indicators["macd_signal"], label="Signal", color="orange")
        ax.axhline(0, color="gray", linestyle="--")
        ax.set_ylabel("MACD")
        ax.set_title("MACD")
        ax.legend(loc="upper left")
        ax.grid(True)
        self._format_xaxis(ax)
        plt.show()

    def plot_volatility(self):
        fig, ax = plt.subplots(figsize=(14, 4))
        ax.plot(self.indicators.index, self.indicators["vol_20"], label="Volatility (20d)", color="brown")
        ax.set_title("Volatility")
        ax.legend()
        ax.grid(True)
        self._format_xaxis(ax)
        plt.show()

    def plot_sharpe(self):
        fig, ax = plt.subplots(figsize=(14, 4))
        for w in self.sharpe_windows:
            ax.plot(self.indicators.index, self.indicators[f"sharpe_{w}"], label=f"Sharpe ({w}d)")
        ax.axhline(0, color="gray", linestyle="--")
        ax.set_title("Rolling Sharpe Ratios")
        ax.legend()
        ax.grid(True)
        self._format_xaxis(ax)
        plt.show()

    def plot_all(self):
        self.plot_price_bands()
        self.plot_momentum_rsi()
        self.plot_macd()
        self.plot_volatility()
        self.plot_sharpe()
