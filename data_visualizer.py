import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mplcursors
import pandas as pd
import numpy as np
import os
import sys

def _try_maximize_window(fig):
    try:
        manager = plt.get_current_fig_manager()
        try:
            manager.window.state('zoomed')
            return
        except Exception:
            pass
        try:
            manager.window.showMaximized()
            return
        except Exception:
            pass
        fig.set_size_inches(16, 9)
    except Exception:
        fig.set_size_inches(16, 9)

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mplcursors
import pandas as pd
import numpy as np

def create_matplotlib_dashboard(df: pd.DataFrame, show: bool = True):
    """
    Show three interactive matplotlib figures (Temperature trend, Pollution trend, and Scatter).
    Each opens in a separate window with hover tooltips using mplcursors.
    """
    plot_df = df.copy()
    plot_df['Date'] = pd.to_datetime(plot_df['Date'], errors='coerce')
    plot_df = plot_df.sort_values('Date').reset_index(drop=True)

    fig1, ax1 = plt.subplots(figsize=(10, 5))
    grouped = plot_df.groupby(['Country', 'State'])
    for (country, state), g in grouped:
        ax1.plot(g['Date'], g['Temperature'], marker='o', linestyle='-', alpha=0.8, label=f"{country} / {state}")
    ax1.set_title("Temperature Trend Over Time")
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Temperature (°C)")
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax1.tick_params(axis='x', rotation=30)
    ax1.legend(fontsize=8)
    ax1.grid(True)

    cursor1 = mplcursors.cursor(ax1.lines, hover=True)
    @cursor1.connect("add")
    def on_hover1(sel):
        line = sel.artist
        x, y = line.get_data()
        idx = sel.index
        date_str = pd.to_datetime(x[idx]).strftime("%Y-%m-%d")
        sel.annotation.set_text(
            f"Country/State: {line.get_label()}\nDate: {date_str}\nTemp: {y[idx]:.1f} °C"
        )

    # ---- 2️⃣ POLLUTION TREND ----
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    for (country, state), g in grouped:
        ax2.plot(g['Date'], g['PollutionIndex'], marker='o', linestyle='-', alpha=0.8, label=f"{country} / {state}")
    ax2.set_title("Pollution Index Trend Over Time")
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Pollution Index")
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax2.tick_params(axis='x', rotation=30)
    ax2.legend(fontsize=8)
    ax2.grid(True)

    cursor2 = mplcursors.cursor(ax2.lines, hover=True)
    @cursor2.connect("add")
    def on_hover2(sel):
        line = sel.artist
        x, y = line.get_data()
        idx = sel.index
        date_str = pd.to_datetime(x[idx]).strftime("%Y-%m-%d")
        sel.annotation.set_text(
            f"Country/State: {line.get_label()}\nDate: {date_str}\nPollution: {y[idx]:.1f}"
        )

    fig3, ax3 = plt.subplots(figsize=(7, 6))
    colors = plt.cm.tab10.colors
    for i, (country, g) in enumerate(plot_df.groupby('Country')):
        ax3.scatter(g['Temperature'], g['PollutionIndex'],
                    color=colors[i % len(colors)], label=country, alpha=0.8)
    ax3.set_title("Temperature vs Pollution Index")
    ax3.set_xlabel("Temperature (°C)")
    ax3.set_ylabel("Pollution Index")
    ax3.legend(fontsize=8)
    ax3.grid(True)

    cursor3 = mplcursors.cursor(ax3.collections, hover=True)
    @cursor3.connect("add")
    def on_hover3(sel):
        ind = sel.index
        artist = sel.artist
        offsets = artist.get_offsets()
        temp, poll = offsets[ind]
        country = artist.get_label()
        sel.annotation.set_text(
            f"Country: {country}\nTemp: {temp:.1f} °C\nPollution: {poll:.1f}"
        )
        
    if show:
        plt.show()
