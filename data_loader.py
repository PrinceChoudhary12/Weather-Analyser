import pandas as pd

def load_weather_data(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    print(f"Loaded {len(df)} rows from {file_path}")
    return df
