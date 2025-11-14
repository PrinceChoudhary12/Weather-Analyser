import pandas as pd
import numpy as np

def cap_outliers(series: pd.Series, lower_percentile: float = 0.01, upper_percentile: float = 0.99) -> pd.Series:
    if series.dropna().empty:
        return series
    low, high = series.quantile([lower_percentile, upper_percentile])
    return series.clip(lower=low, upper=high)

def clean_weather_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [c.strip() for c in df.columns]
    required = ['Date', 'Country', 'State']
    for col in required:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Date'])

    numeric_cols = ['Temperature', 'Humidity', 'Rainfall', 'PollutionIndex']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    df = df.dropna(subset=['Country', 'State'])

    if 'Temperature' in df.columns:
        def fill_temp_with_group_mean(x):
            return x.fillna(x.mean())
        df['Temperature'] = df.groupby(['Country', 'State'])['Temperature'].transform(fill_temp_with_group_mean)
        df['Temperature'] = df['Temperature'].fillna(df['Temperature'].mean())

    if 'PollutionIndex' in df.columns:
        df = df.sort_values(['Country', 'State', 'Date']).reset_index(drop=True)

        def interp_group(g):
            g = g.set_index('Date').sort_index()
            g['PollutionIndex'] = g['PollutionIndex'].interpolate(method='time', limit_direction='both')
            return g.reset_index()
        df = df.groupby(['Country', 'State'], group_keys=False).apply(interp_group)
        df = df.reset_index(drop=True)
    df = df.sort_values(['Country', 'State', 'Date']).reset_index(drop=True)
    
    if 'Temperature' in df.columns:
        df['Temperature'] = cap_outliers(df['Temperature'], 0.01, 0.99)
    if 'PollutionIndex' in df.columns:
        df['PollutionIndex'] = cap_outliers(df['PollutionIndex'], 0.01, 0.99)

    return df
